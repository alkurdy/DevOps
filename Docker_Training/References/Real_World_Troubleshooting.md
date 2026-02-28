# Real-World Docker Troubleshooting

A progressive, case-study-driven guide built from diagnosing a live self-hosted Node.js + SQLite service running under Docker Compose. Applies to Linux, macOS, and Windows (Docker Desktop / WSL2). Each level builds on the previous one — start at Level 1 and work down until the problem is found.

> **Companion to**: [Troubleshooting_Guide.md](Troubleshooting_Guide.md) — which covers general Docker issues.  
> **This guide covers**: production-pattern problems that only appear in real deployments — OOM crashes during builds, schema migrations, bind-mount permissions, dependency audits, and upstream upgrades.

---

## Level 1 — Is Docker Actually Running?

Before anything else, confirm the Docker daemon is up. On Linux, the daemon may not be enabled; on macOS/Windows, Docker Desktop may not be running.

```sh
# Quick check — if "Server:" section is missing, the engine is down
docker version

# Full daemon info
docker info

# Check if the Docker process is running
pgrep -fa docker   # Linux / macOS
```

**What to look for:**
- `Cannot connect to the Docker daemon` → daemon not running
- `failed to connect to the docker API` → Docker Desktop engine not started (macOS/Windows)
- CLI responds but no Server section → engine down, only the CLI is installed

**Fix — Linux (systemd):**
```sh
sudo systemctl start docker
sudo systemctl enable docker   # persist across reboots
```

**Fix — macOS / Windows (Docker Desktop):**
```sh
# macOS — open app via Spotlight or:
open -a Docker

# Windows (PowerShell)
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

**Wait loop (bash) — useful in scripts:**
```sh
timeout=120; elapsed=0
until docker version 2>&1 | grep -q 'Server:'; do
    sleep 5; elapsed=$((elapsed+5))
    echo "Waiting for Docker daemon... (${elapsed}s)"
    [ $elapsed -ge $timeout ] && echo 'Timed out' && exit 1
done
echo 'Docker daemon is up'
```

---

## Level 2 — Container Status Check

Once Docker is running, get a full picture of what containers exist and what state they are in.

```sh
# All containers — running AND stopped
docker ps -a

# Compact view with key fields
docker ps -a --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"

# Check a specific container
docker inspect --format='{{.State.Status}} (exit {{.State.ExitCode}}) restarts={{.RestartCount}}' <container>
```

**Status values and what they mean:**

| Status | Meaning |
|---|---|
| `Up X seconds` | Running normally |
| `Up X seconds (healthy)` | Running and passing healthcheck |
| `Up X seconds (health: starting)` | Healthcheck not yet passed — wait |
| `Restarting (1) X seconds ago` | Crash loop — check logs immediately |
| `Exited (0)` | Stopped cleanly (intentional or one-shot task) |
| `Exited (1)` | Application error |
| `Exited (137)` | OOM killed or `docker kill` |
| `Exited (143)` | SIGTERM (graceful stop) |

**Restart count matters.** A container at restart count 5+ with no uptime is in a crash loop:
```sh
docker inspect --format='RestartCount: {{.RestartCount}}' <container>
```

---

## Level 3 — Reading Logs

Logs are the single most useful source of truth.

```sh
# Last 50 lines
docker logs <container> --tail 50

# Follow live (Ctrl+C to stop)
docker logs <container> -f

# Timestamps
docker logs <container> --timestamps --tail 100

# Search logs for errors/crashes
docker logs <container> 2>&1 | grep -iE 'error|fatal|crash|abort|killed|OOM'
```

**What to look for in order of severity:**

| Pattern | Severity | Meaning |
|---|---|---|
| `Server running on http://...` | ✅ Good | App started successfully |
| `[MCP] Server started` | ✅ Good | Sub-systems initialized |
| `No API key configured` | ℹ️ Info | Cosmetic warning — not an error |
| `SQLITE_ERROR: no such column` | ⚠️ Error | Schema migration needed |
| `SQLITE_READONLY` | ⚠️ Error | File permission problem |
| `FATAL ERROR: ... heap out of memory` | 🔴 Fatal | OOM — Node.js ran out of heap |
| `Aborted (core dumped)` | 🔴 Fatal | Native crash (usually OOM or SIGABRT) |
| `Cannot find module` | 🔴 Fatal | Missing dependency — `npm install` wasn't run |

**Crash loop pattern** — look for the same fatal line repeating:
```sh
# Count how many times the app has (re)started
docker logs <container> 2>&1 | grep -iE 'Starting on port|server starting'
```

---

## Level 4 — Dependency Health (npm audit)

For Node.js containers, security vulnerabilities in dependencies are common. Check them without restarting:

```sh
# Run audit inside running container
docker exec <container> npm audit

# Get a clean summary (requires jq)
docker exec <container> npm audit --json | jq '.metadata.vulnerabilities'

# Without jq — print raw JSON and read the "vulnerabilities" block manually
docker exec <container> npm audit --json | grep -A5 '"vulnerabilities"'
```

**Reading the output:**

```
13 vulnerabilities (2 moderate, 11 high)
```

**What to fix vs what to skip:**

| Type | Action |
|---|---|
| `high` / `critical` in runtime dependencies (express, ws, zod) | Fix ASAP — `npm audit fix` |
| `high` in build-tool chain only (tar, node-gyp, rimraf) | Lower priority — only triggered during `npm install`, not at runtime |
| `moderate` | Fix if `npm audit fix` handles it without breaking changes |
| Fix requires `--force` and a major downgrade | Evaluate manually — may break functionality |

**Applying fixes to the source (bind-mounted backend):**
```sh
# On your host, in the backend directory
cd path/to/backend
npm audit fix

# Then restart container to reinstall
docker compose restart <service>
```

**After fixing, check what changed:**
```sh
npm list <package>   # e.g. npm list @modelcontextprotocol/sdk
```

> **Key lesson from production**: `npm audit fix` on `@modelcontextprotocol/sdk` bumped it from `1.20.2` → `1.26.0`. That version introduced breaking API changes that caused TypeScript compile failures. Always test after dependency upgrades.

---

## Level 5 — OOM (Out of Memory) Crashes

The most insidious crash type. The container starts, runs for a bit, then dies without an obvious application error.

**Reading an OOM stack trace:**
```
FATAL ERROR: Ineffective mark-compacts near heap limit Allocation failed - JavaScript heap out of memory
 1: 0xb76dc5 node::OOMErrorHandler ...
 ...
 5: 0x10f84e4 v8::internal::Heap::RecomputeLimits ...
Aborted (core dumped)
```

The key line: `JavaScript heap out of memory` — Node.js (V8) ran out of heap space.

**What's actually using that memory?** Usually:
- TypeScript compilation (`tsc`) — especially with large dependency type definitions
- Large `node_modules` being loaded
- The application itself under load

**Check how much heap was in use at crash:**
```
31: Mark-Compact 2525.4 (2592.7) -> 2509.1 MB
```
That tells you it needed ~2.5 GB of heap before crashing.

**Fixes in order of preference:**

1. **Don't do the heavy work in the container** — if `tsc` is crashing, compile on the host (which has no container memory limit) and mount the pre-built `dist/`:
   ```sh
   # Run on host — no memory constraint
   npx tsc -p tsconfig.json
   # Container only runs: npm install && npm start
   ```

2. **Increase Node.js heap limit** via environment variable:
   ```yaml
   # docker-compose.yml
   environment:
     - NODE_OPTIONS=--max-old-space-size=2560  # 2.5 GB
   ```

3. **Increase the container memory limit** to match:
   ```yaml
   deploy:
     resources:
       limits:
         memory: 3G
   ```

   > **Important**: `NODE_OPTIONS` must be ≤ container memory limit. A 2560 MB heap inside a 2 GB container will still OOM.

4. **Switch to a smaller base image / use Bun for builds** — the upstream `Dockerfile` uses a Bun-based multi-stage build which avoids the `tsc` memory problem entirely by compiling with Bun's faster/leaner transpiler.

---

## Level 6 — Permission Errors on Bind Mounts

With bind mounts, the host filesystem controls file ownership. If the container runs as a non-root user (e.g., uid=1001) but the mounted files are owned by root or a different user, writes will fail with `SQLITE_READONLY`, `EACCES`, or `Permission denied`.

**Diagnosing permission problems:**
```sh
# Check what user the container runs as
docker inspect --format='{{.Config.User}}' <container>

# Check actual file permissions inside the container
docker exec <container> ls -la /data/
# Or if the container crashes too fast, use a one-shot:
docker run --rm -v /path/to/data:/data <image> ls -la /data/
```

**What you'll see:**
```
-rw-r--r-- 1 root root 4096 openmemory.sqlite
```
The file is owned by root, read-only to everyone else. If the container runs as uid=1001 (non-root), it can't write.

**Fixes:**

1. **Quickest (home lab)** — override `user` in `docker-compose.yml`:
   ```yaml
   services:
     myservice:
       user: "0:0"  # Run as root — acceptable for local/home lab
   ```

2. **Correct for production** — fix ownership before starting:
   ```sh
   # Linux / macOS host
   sudo chown -R 1001:1001 ./data

   # Any OS — use a one-shot container (avoids needing sudo on host)
   docker run --rm -v /path/to/data:/data alpine chown -R 1001:1001 /data
   ```

3. **Baked into Dockerfile** — ensure `/data` directory ownership is set at build time and the volume is a named volume (not a bind mount) which Docker manages with correct permissions.

> **Key lesson**: Named volumes (`myservice_data:`) give Docker full control of permissions and avoid this entirely. Bind mounts (`./data:/data`) are convenient but require manual permission management — particularly on Windows where `chown` is not available on the host.

---

## Level 7 — Schema Migrations After Upgrades

When upgrading a containerized service that uses a persistent database, the new version may require schema changes (new columns, new tables, index changes). The container will crash-loop with errors like:

```
SQLITE_ERROR: no such column: user_id
```

**Diagnostic approach:**
1. Check what version you're upgrading from → to
2. Find the migration file in the source (usually `src/core/migrate.ts`, `migrations/`, or similar)
3. Determine if migration runs automatically on startup or must be triggered manually

**Running a manual migration safely:**

```sh
# Step 1: Stop container to release database lock
docker stop <container>

# Step 2: Verify the database is unlocked (WAL files exist but container is stopped)
ls -la path/to/data/

# Step 3: Run migration using the same image (has correct sqlite3 bindings)
docker run --rm \
  --user root \
  -v /path/to/data:/data \
  --workdir /app \
  --env NODE_PATH=/app/node_modules \
  --entrypoint node \
  <image>:latest \
  /data/run-migrate.js

# Step 4: Start container again
docker compose up -d <service>
```

**Writing a one-shot migration script** for SQLite (save as `data/run-migrate.js`):
```javascript
const sqlite3 = require('sqlite3').verbose()
const db = new sqlite3.Database('/data/myapp.sqlite')

const run = (sql, label) => new Promise((ok, fail) =>
  db.run(sql, (err) => {
    if (err && !err.message.includes('duplicate column') && !err.message.includes('already exists')) {
      console.error(`[FAIL] ${label}: ${err.message}`); fail(err)
    } else {
      console.log(err ? `[SKIP] ${label}` : `[OK]   ${label}`); ok()
    }
  })
)

async function migrate() {
  await run('ALTER TABLE mytable ADD COLUMN new_col TEXT', 'new_col')
  await run('CREATE INDEX IF NOT EXISTS idx_new ON mytable(new_col)', 'idx_new')
  // Add more steps...
  console.log('Migration complete')
  db.close()
}
migrate().catch(err => { console.error(err); process.exit(1) })
```

**Key safety rules:**
- Always backup the `.sqlite` file before running a migration
- Use `IF NOT EXISTS` and `IF NOT EXISTS` / `IF EXISTS` guards so the script is idempotent (safe to re-run)
- Ignore `duplicate column name` errors — means a step already ran
- Stop the container *before* running migration — SQLite WAL mode can corrupt under concurrent writes

---

## Level 8 — Inspect Container Configuration

When behavior is unexpected and logs don't explain it, inspect the full container config.

```sh
# Everything about a container
docker inspect <container>

# Key fields to check:
docker inspect --format='
Image:      {{.Config.Image}}
Command:    {{.Config.Cmd}}
Entrypoint: {{.Config.Entrypoint}}
User:       {{.Config.User}}
WorkDir:    {{.Config.WorkingDir}}
RestartPolicy: {{.HostConfig.RestartPolicy.Name}}
Memory:     {{.HostConfig.Memory}}
OOMKilled:  {{.State.OOMKilled}}
' <container>

# Environment variables (careful — may contain secrets)
docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' <container>

# Mounts / volumes
docker inspect --format='{{range .Mounts}}{{.Type}} {{.Source}} -> {{.Destination}}{{println}}{{end}}' <container>
```

**Critical things to verify after a `docker compose up`:**
- Is the right image being used? (`docker inspect --format='{{.Config.Image}}'`)
- Are the volumes mounted where the app expects them?
- Is the correct port bound? (`docker port <container>`)
- Is the compose file the right one? (Check the label: `com.docker.compose.project.config_files`)

---

## Level 9 — Upstream Upgrades

When a self-hosted service is behaving badly, checking whether there's a newer upstream version is often worthwhile. Bugs you're fighting may already be fixed.

**Step 1 — Identify the source**
```sh
# Check where the code came from
docker inspect --format='{{range $k,$v := .Config.Labels}}{{$k}}={{$v}}{{println}}{{end}}' <container>
# Look for: com.docker.compose.project.config_files, org.opencontainers.image.source

# Check package.json author / version (requires jq)
docker exec <container> cat /app/package.json | jq '{name, version, author}'

# Without jq
docker exec <container> cat /app/package.json
```

**Step 2 — Find the upstream repo**
- Search GitHub: `github.com/search?q=<project-name>&type=repositories`
- Check Docker Hub: `hub.docker.com/search?q=<project-name>&type=image`
- Look for the package on npm: `npmjs.com/package/<name>`

**Step 3 — Compare versions**

| Check | Command |
|---|---|
| Your version | `docker exec <c> cat /app/package.json` → `version` field |
| Upstream latest tag | GitHub Releases page |
| Upstream `main` version | Raw `package.json` from GitHub |
| What changed | GitHub `CHANGELOG.md` |

**Step 4 — Pull and rebuild**
```sh
# If using a built image (Dockerfile)
docker compose build --no-cache <service>
docker compose up -d --force-recreate <service>

# If using a registry image (image: nginx:latest)
docker compose pull <service>
docker compose up -d <service>
```

> **`--no-cache` matters** when the Dockerfile `RUN` steps haven't changed but upstream packages have. Without it, Docker reuses cached layers and you may get an older version of npm packages.

**Step 5 — Watch the first startup carefully**
```sh
# Follow logs during first start after upgrade
docker logs <container> -f

# Key things to watch for:
# ✅ Banner/version string matches new version
# ✅ "Server running" message
# ✅ No new SQLITE_ERROR or missing column errors
# ✅ Data (memories, records) loaded on init
# ❌ OOM / heap crash → new version has heavier dependencies (see Level 5)
# ❌ Schema error → migration needed (see Level 7)
# ❌ API error → breaking change in config env var names
```

---

## Level 10 — Full Rebuild Workflow

When things are badly broken and you want a clean slate while preserving data:

```sh
# 1. Backup data first
cp ./data/myapp.sqlite "./data/myapp.sqlite.backup-$(date +%Y-%m-%d)"

# 2. Stop and remove the container (not the image)
docker compose down

# 3. Remove the old image to force a full rebuild
docker rmi <image-name>

# 4. Pull latest base images
docker compose pull  # Only for services using registry images

# 5. Rebuild from scratch
docker compose build --no-cache <service>

# 6. Start fresh
docker compose up -d <service>

# 7. Watch logs
docker logs <container> -f
```

> **Windows (PowerShell) backup equivalent:**
> ```powershell
> Copy-Item ".\data\myapp.sqlite" ".\data\myapp.sqlite.backup-$(Get-Date -Format 'yyyy-MM-dd')"
> ```

**Cleaning up leftover build cache** (reclaim disk space after rebuilds):
```sh
docker builder prune        # Remove dangling build cache
docker image prune          # Remove unused images
docker system prune         # Everything unused (containers, networks, images)
docker system prune -a      # Aggressive — removes ALL unused images (not just dangling)
```

---

## Quick Diagnostic Checklist

Copy-paste this block when something is wrong:

```sh
c="your-container-name"

# 1. Daemon
docker version 2>&1 | grep 'Server:'

# 2. Status
docker ps -a --filter "name=$c" --format "{{.Names}} | {{.Status}} | {{.Image}}"

# 3. Restart count + OOM flag
docker inspect --format='OOMKilled={{.State.OOMKilled}} Restarts={{.RestartCount}}' "$c"

# 4. Last 30 lines of logs
docker logs "$c" --tail 30

# 5. Errors only
docker logs "$c" 2>&1 | grep -iE 'error|fatal|abort|readonly|OOM|heap'

# 6. Resource usage
docker stats --no-stream "$c"

# 7. Mounted paths
docker inspect --format='{{range .Mounts}}{{.Source}} -> {{.Destination}}{{println}}{{end}}' "$c"
```

> **Windows (PowerShell) equivalent for step 5:**
> ```powershell
> docker logs $c 2>&1 | Select-String -Pattern 'error|fatal|abort|readonly|OOM|heap' -CaseSensitive:$false
> ```

---

## Common Error Reference

| Error Message | Cause | Fix |
|---|---|---|
| `Cannot connect to the Docker daemon` | Daemon not running | `sudo systemctl start docker` (Linux) or start Docker Desktop (macOS/Windows) |
| `SQLITE_READONLY: attempt to write a readonly database` | Container running as non-root, files owned by root | Add `user: "0:0"` in compose or fix file ownership |
| `SQLITE_ERROR: no such column: user_id` | Schema out of date, needs migration | Run migration script (Level 7) |
| `FATAL ERROR: ... heap out of memory` | Node.js / tsc ran out of V8 heap | Compile on host, increase `--max-old-space-size`, increase container memory limit |
| `Aborted (core dumped)` | Usually OOM — check for heap message above it | Same as above |
| `Cannot find module 'sqlite3'` | `npm install` not run or wrong `NODE_PATH` | Set `--env NODE_PATH=/app/node_modules` or run in correct workdir |
| `duplicate column name: user_id` | Migration already partially applied | Safe to ignore — migration is idempotent |
| `npm audit fix` breaks TypeScript build | Dependency upgrade introduced breaking API change | Fix source code to match new API or pin to previous working version |
| `Bus error` (Node.js / Next.js) | Memory-mapped files incompatible with certain bind-mount backends (e.g., Windows WSL2, some NFS/FUSE mounts) | Disable the affected service, use named volumes, or move data to native filesystem |
| `version is obsolete` (compose warning) | `version: '3.8'` in compose file | Remove the `version:` line — it's ignored in Compose v2+ |
