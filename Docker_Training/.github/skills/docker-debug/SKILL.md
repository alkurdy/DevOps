---
name: docker-debug
description: Systematic Docker troubleshooting workflow for diagnosing broken containers, failed builds, networking issues, and volume problems. Use this when a container is not starting, exiting unexpectedly, unreachable on the network, or when a build fails.
argument-hint: "[container-name | image-name | error-message]"
---

# Docker Debug Workflow

## Step 1 – Determine What Is Broken

```powershell
# See all containers including stopped ones
docker ps -a

# Check recent events (last 60 seconds)
docker events --since 60s --until 0s
```

## Step 2 – Inspect the Failing Container

```powershell
# Full logs — most useful first step
docker logs <container> --tail 100

# Follow log stream for live errors
docker logs <container> -f

# Detailed state, restart count, exit code
docker inspect <container> --format '{{json .State}}' | ConvertFrom-Json
```

**Exit code reference:**

| Code | Meaning |
|------|---------|
| 0 | Clean exit |
| 1 | Application error |
| 125 | Docker daemon error |
| 126 | Container command not executable |
| 127 | Container command not found |
| 137 | Killed (OOM or `docker kill`) |
| 139 | Segfault |

## Step 3 – Container Won't Start

```powershell
# Does the image exist locally?
docker images <image-name>

# Pull the image explicitly to see registry errors
docker pull <image:tag>

# Validate the compose file before starting
docker compose config

# Start in foreground to see immediate output
docker compose up   # (not -d)
```

## Step 4 – Networking Issues

```powershell
# List networks and check which one the container is on
docker network ls
docker inspect <container> --format '{{json .NetworkSettings.Networks}}' | ConvertFrom-Json

# Test connectivity from inside the container
docker exec <container> ping -c 3 google.com
docker exec <container> curl -sv http://traefik:80/ping   # for Traefik mesh

# Inspect network for all connected containers
docker network inspect proxy
```

## Step 5 – Volume / Permission Issues

```powershell
# Check mounted volumes
docker inspect <container> --format '{{json .Mounts}}' | ConvertFrom-Json

# Enter the container and check directory permissions
docker exec -it <container> sh -c "ls -la /data"
```

## Step 6 – Build Failures

```powershell
# Build with no cache to rule out stale layers
docker build --no-cache -t <tag> .

# Enable BuildKit for better error output
$env:DOCKER_BUILDKIT=1; docker build -t <tag> .

# Show each layer during build (legacy builder)
docker build --progress=plain -t <tag> .
```

## Step 7 – Resource Issues

```powershell
# Container stats (CPU / memory)
docker stats <container> --no-stream

# System-wide disk usage
docker system df
```

## Quick Fixes Reference

| Symptom | Command |
|---------|---------|
| Restart a stuck container | `docker restart <container>` |
| Hard reset (stop + remove + recreate) | `docker compose down && docker compose up -d` |
| Remove dangling images clogging disk | `docker image prune` |
| Full system prune (careful) | `docker system prune -af` |
| Recreate single compose service | `docker compose up -d --force-recreate <service>` |

## When to Escalate
If the above steps don't resolve the issue, collect and share:
1. `docker inspect <container>` full JSON output
2. `docker logs <container>` last 200 lines
3. `docker compose config` output
4. The `docker-compose.yml` file (secrets redacted)
