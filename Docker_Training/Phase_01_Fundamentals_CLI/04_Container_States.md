# Module 04: Container States & Lifecycle

## Introduction

Understanding the container lifecycle is crucial for effective container management. This module covers the various states a container can be in and how to manage transitions between states.

## Container Lifecycle Overview

```
                  docker run / create
                          │
                          ▼
                    ┌──────────┐
                    │ CREATED  │
                    └────┬─────┘
                         │ docker start
                         ▼
    ┌────────────────────────────────────┐
    │           RUNNING                  │
    │                                    │
    │  docker pause ──▶ PAUSED ──▶ unpause
    └────┬───────────────────────────┬───┘
         │                           │
         │ docker stop               │ exit/crash
         │ (SIGTERM)                 │
         ▼                           ▼
    ┌─────────┐                 ┌─────────┐
    │ STOPPED │                 │ EXITED  │
    └────┬────┘                 └────┬────┘
         │                           │
         │ docker start              │ docker start
         └────────────┬──────────────┘
                      │
                      │ docker rm
                      ▼
                 [REMOVED]
```

## Container States

### 1. Created

Container is created but not started.

```powershell
# Create container without starting
docker create --name myapp nginx

# Check status
docker ps -a --filter "name=myapp"
# Status: Created

# Inspect state
docker inspect --format='{{.State.Status}}' myapp
# Output: created
```

**Characteristics**:
- Container exists on disk
- Filesystem is prepared
- Not consuming CPU/memory
- Can be started later
- Can be removed without stopping

**When to use**:
- Prepare containers for later use
- Batch creation before orchestrated start
- Testing container configuration

### 2. Running

Container is actively running.

```powershell
# Start the created container
docker start myapp

# Or create and start in one command
docker run -d --name myapp2 nginx

# Verify running
docker ps --filter "name=myapp"

# Check state
docker inspect --format='{{.State.Status}}' myapp
# Output: running
```

**Characteristics**:
- Main process (PID 1) is active
- Consuming resources (CPU, memory)
- Can serve traffic
- Can execute commands with `docker exec`
- Logs are being generated

**State details**:
```powershell
docker inspect --format='{{json .State}}' myapp | ConvertFrom-Json
```

Shows:
- `Running: true`
- `Pid`: Process ID on host
- `StartedAt`: When container started
- `Status: "running"`

### 3. Paused

Container is frozen; processes are suspended.

```powershell
# Pause running container
docker pause myapp

# Check status
docker ps --filter "name=myapp"
# Status: Up X minutes (Paused)

# Inspect state
docker inspect --format='{{.State.Status}}' myapp
# Output: paused

# Resume
docker unpause myapp
```

**Characteristics**:
- All processes suspended via cgroups freezer
- Maintains memory state
- No CPU usage
- Network connections preserved
- Quick to resume
- **Does NOT work on Windows containers**

**Use cases**:
- Temporarily free CPU without stopping
- Checkpoint state before maintenance
- Debugging stuck processes

**Important**: Paused containers:
- Still count as "running" in `docker ps`
- Cannot execute commands (`docker exec` fails)
- Maintain network presence

### 4. Stopped (Exited)

Container stopped gracefully or crashed.

```powershell
# Stop running container
docker stop myapp
# Sends SIGTERM, waits 10s, then SIGKILL

# Immediate forceful stop
docker kill myapp
# Sends SIGKILL immediately

# Check status
docker ps -a --filter "name=myapp"
# Status: Exited (0) X seconds ago

# Inspect state
docker inspect --format='{{.State.Status}}' myapp
# Output: exited
```

**Characteristics**:
- Main process terminated
- No resource consumption
- Filesystem preserved
- Can be restarted with `docker start`
- Exit code indicates how it stopped

**Exit codes**:

| Code | Meaning |
|------|---------|
| **0** | Normal exit, successful |
| **1** | Application error |
| **2** | Misuse of shell command |
| **125** | Docker daemon error |
| **126** | Command cannot execute |
| **127** | Command not found |
| **128+n** | Killed by signal n (e.g., 137 = SIGKILL, 143 = SIGTERM) |
| **137** | SIGKILL (killed) |
| **139** | SIGSEGV (segmentation fault) |
| **143** | SIGTERM (terminated) |

```powershell
# Check exit code
docker inspect --format='{{.State.ExitCode}}' myapp
```

### Difference: Stop vs Kill

```powershell
# Graceful stop (recommended)
docker stop myapp
# 1. Sends SIGTERM to container
# 2. Waits 10 seconds (configurable with -t)
# 3. Sends SIGKILL if still running
# Exit code: usually 143 (SIGTERM)

# Forceful kill
docker kill myapp
# Sends SIGKILL immediately
# No cleanup opportunity
# Exit code: usually 137 (SIGKILL)

# Custom timeout
docker stop -t 30 myapp  # Wait 30 seconds before SIGKILL
```

**Best Practice**: Always use `docker stop` unless absolutely necessary to force-kill.

### 5. Restarting

Container is in the process of restarting.

```powershell
# Restart container
docker restart myapp

# During restart, briefly shows:
docker inspect --format='{{.State.Status}}' myapp
# Output: restarting (transient state)
```

**Characteristics**:
- Transient state
- Usually lasts < 1 second
- Automatically triggered by restart policies
- Can be manually triggered

### 6. Removing

Container is being removed.

```powershell
# Remove stopped container
docker rm myapp

# Force remove running container
docker rm -f myapp

# Remove with volumes
docker rm -v myapp
```

**Characteristics**:
- Container and writable layer deleted
- Volumes preserved (unless `-v` flag used)
- Cannot be recovered
- Must be stopped first (unless `-f` used)

## Understanding Exit Codes

### Checking Why Container Stopped

```powershell
# Get exit code
docker inspect --format='{{.State.ExitCode}}' myapp

# Get full exit info
docker inspect --format='Status: {{.State.Status}}, Exit Code: {{.State.ExitCode}}, Error: {{.State.Error}}' myapp

# View finish time
docker inspect --format='{{.State.FinishedAt}}' myapp
```

### Common Exit Code Scenarios

#### Exit Code 0 - Success
```powershell
# Container completed task successfully
docker run --name task --rm alpine echo "Done"
# Exit code: 0
```

#### Exit Code 1 - Application Error
```powershell
# Application error
docker run --name error --rm alpine sh -c "exit 1"
# Exit code: 1

# Check it
docker ps -a --filter "name=error"
```

#### Exit Code 137 - Killed (SIGKILL)
```powershell
# Container was killed
docker run -d --name killtest alpine sleep 100
docker kill killtest
docker inspect --format='{{.State.ExitCode}}' killtest
# Exit code: 137
```

#### Exit Code 143 - Terminated (SIGTERM)
```powershell
# Container stopped gracefully
docker run -d --name stoptest alpine sleep 100
docker stop stoptest
docker inspect --format='{{.State.ExitCode}}' stoptest
# Exit code: 143
```

### Analyzing Your Containers' Exit Codes

```powershell
# Check all stopped containers
docker ps -a --filter "status=exited" --format "table {{.Names}}\t{{.Status}}"

# Get exit codes for all containers
docker ps -a --format '{{.Names}}' | ForEach-Object {
    $exitCode = docker inspect --format='{{.State.ExitCode}}' $_
    Write-Host "$_ : Exit Code $exitCode"
}
```

**Try it now**:
```powershell
# Check romantic_murdock (your stopped SQLite container)
docker inspect --format='Exit Code: {{.State.ExitCode}}' romantic_murdock
docker inspect --format='Finished At: {{.State.FinishedAt}}' romantic_murdock
docker logs --tail 20 romantic_murdock
```

## Restart Policies

Docker can automatically restart containers based on policies.

### Restart Policy Types

```powershell
# No restart (default)
docker run -d --restart no nginx

# Always restart
docker run -d --restart always nginx

# Restart on failure only
docker run -d --restart on-failure nginx

# Restart on failure with max attempts
docker run -d --restart on-failure:5 nginx

# Restart unless explicitly stopped
docker run -d --restart unless-stopped nginx
```

### Policy Comparison

| Policy | Behavior |
|--------|----------|
| **no** | Never restart |
| **always** | Always restart, even after Docker daemon restart |
| **on-failure** | Restart only if exit code is non-zero |
| **on-failure:n** | Restart max n times on failure |
| **unless-stopped** | Always restart unless manually stopped |

### Checking Restart Policy

```powershell
# Get restart policy
docker inspect --format='{{.HostConfig.RestartPolicy.Name}}' <container>

# Get max retry count (for on-failure)
docker inspect --format='{{.HostConfig.RestartPolicy.MaximumRetryCount}}' <container>

# Get restart count
docker inspect --format='{{.RestartCount}}' <container>
```

**Check your containers**:
```powershell
docker ps --format '{{.Names}}' | ForEach-Object {
    $policy = docker inspect --format='{{.HostConfig.RestartPolicy.Name}}' $_
    Write-Host "$_ : $policy"
}
```

### Updating Restart Policy

```powershell
# Update existing container
docker update --restart unless-stopped myapp

# Verify
docker inspect --format='{{.HostConfig.RestartPolicy.Name}}' myapp
```

### Restart Policy Best Practices

**Development**:
- Use `no` or `on-failure` for debugging
- Prevents infinite restart loops during development

**Production**:
- Use `unless-stopped` for most services
- Use `always` for critical infrastructure
- Use `on-failure:5` to prevent infinite restart on persistent errors

## Container Lifecycle Commands

### Complete Lifecycle Example

```powershell
# 1. Create container (not started)
docker create --name lifecycle-demo nginx
docker inspect --format='{{.State.Status}}' lifecycle-demo  # created

# 2. Start container
docker start lifecycle-demo
docker inspect --format='{{.State.Status}}' lifecycle-demo  # running

# 3. Pause container
docker pause lifecycle-demo
docker inspect --format='{{.State.Status}}' lifecycle-demo  # paused

# 4. Unpause container
docker unpause lifecycle-demo
docker inspect --format='{{.State.Status}}' lifecycle-demo  # running

# 5. Restart container
docker restart lifecycle-demo
docker inspect --format='{{.State.Status}}' lifecycle-demo  # running

# 6. Stop container
docker stop lifecycle-demo
docker inspect --format='{{.State.Status}}' lifecycle-demo  # exited

# 7. Start again
docker start lifecycle-demo
docker inspect --format='{{.State.Status}}' lifecycle-demo  # running

# 8. Kill container
docker kill lifecycle-demo
docker inspect --format='{{.State.Status}}' lifecycle-demo  # exited
docker inspect --format='{{.State.ExitCode}}' lifecycle-demo  # 137

# 9. Remove container
docker rm lifecycle-demo
docker ps -a --filter "name=lifecycle-demo"  # not found
```

### State Transition Times

```powershell
# When created
docker inspect --format='Created: {{.Created}}' <container>

# When started
docker inspect --format='Started: {{.State.StartedAt}}' <container>

# When finished
docker inspect --format='Finished: {{.State.FinishedAt}}' <container>

# Uptime calculation
$started = docker inspect --format='{{.State.StartedAt}}' traefik
$startTime = [DateTime]::Parse($started)
$uptime = (Get-Date) - $startTime
Write-Host "Uptime: $($uptime.ToString())"
```

## Auto-Start Containers on Boot

### On Windows with Docker Desktop

Docker Desktop's "Start Docker Desktop when you log in" setting handles this.

**Containers with `--restart unless-stopped` or `--restart always`** will auto-start when Docker Desktop starts.

```powershell
# Set container to auto-start
docker update --restart unless-stopped traefik
docker update --restart unless-stopped calibre-web
docker update --restart unless-stopped openmemory

# Verify
docker inspect --format='{{.Name}}: {{.HostConfig.RestartPolicy.Name}}' $(docker ps -aq)
```

### Testing Auto-Start

```powershell
# 1. Set restart policy
docker update --restart unless-stopped myapp

# 2. Restart Docker Desktop
# (Right-click Docker Desktop system tray icon -> Restart)

# 3. Check container auto-started
docker ps --filter "name=myapp"
```

## Monitoring State Changes

### Real-Time Event Monitoring

```powershell
# Watch all Docker events
docker events

# Filter container events only
docker events --filter 'type=container'

# Filter specific events
docker events --filter 'event=start'
docker events --filter 'event=stop'
docker events --filter 'event=die'

# Filter specific container
docker events --filter 'container=traefik'

# Combine filters
docker events --filter 'type=container' --filter 'event=start'
```

**Try it** (in a separate PowerShell window):
```powershell
# Window 1: Monitor events
docker events --filter 'type=container'

# Window 2: Trigger events
docker run -d --name test nginx
docker stop test
docker start test
docker rm test

# Watch events appear in Window 1
```

### Event Types

Common container events:
- `create` - Container created
- `start` - Container started
- `restart` - Container restarted
- `stop` - Container stopped
- `pause` - Container paused
- `unpause` - Container unpaused
- `die` - Container process died
- `kill` - Container killed
- `oom` - Out of memory occurred
- `destroy` - Container removed

## Handling Container Failures

### Detecting Failed Containers

```powershell
# Find exited containers
docker ps -a --filter "status=exited"

# Find containers with non-zero exit codes
docker ps -a --format '{{.Names}}' | ForEach-Object {
    $code = docker inspect --format='{{.State.ExitCode}}' $_
    $status = docker inspect --format='{{.State.Status}}' $_
    if ($status -eq "exited" -and [int]$code -ne 0) {
        Write-Host "$_ failed with exit code $code"
        docker logs --tail 10 $_
    }
}
```

### Restart Failed Container

```powershell
# Restart container that exited
docker start <container>

# View logs to diagnose
docker logs <container>

# If restart fails, check config
docker inspect <container>
```

### High Restart Count Investigation

```powershell
# Find containers restarting frequently
docker ps -q | ForEach-Object {
    $name = docker inspect --format='{{.Name}}' $_
    $restarts = docker inspect --format='{{.RestartCount}}' $_
    if ([int]$restarts -gt 10) {
        Write-Host "$name has restarted $restarts times!"
        Write-Host "Recent logs:"
        docker logs --tail 20 $_
    }
}
```

## Graceful Shutdown Handling

### SIGTERM Handling

Well-designed containers should handle SIGTERM gracefully:

```powershell
# Test graceful shutdown
docker run -d --name sigterm-test alpine sh -c 'trap "echo Caught SIGTERM; exit 0" TERM; sleep 100'

# Stop (sends SIGTERM)
docker stop sigterm-test

# Check logs - should see "Caught SIGTERM"
docker logs sigterm-test
```

### Timeout Considerations

```powershell
# Default timeout: 10 seconds
docker stop myapp

# Custom timeout for slow shutdowns
docker stop -t 30 myapp  # Wait 30 seconds

# No wait (immediate SIGKILL)
docker stop -t 0 myapp
docker kill myapp  # Equivalent
```

**Best Practice**: Set appropriate timeout for containers needing cleanup time (databases, file writers, etc.)

## Practical Scenarios

### Scenario 1: Restart All Stopped Containers

```powershell
# Find stopped containers
$stopped = docker ps -a --filter "status=exited" --format "{{.Names}}"

# Restart each
foreach ($container in $stopped) {
    Write-Host "Starting $container..."
    docker start $container
}
```

### Scenario 2: Clean Up Failed Containers

```powershell
# Remove containers that failed
docker ps -a --format '{{.Names}}' | ForEach-Object {
    $code = docker inspect --format='{{.State.ExitCode}}' $_
    $status = docker inspect --format='{{.State.Status}}' $_
    if ($status -eq "exited" -and [int]$code -ne 0) {
        Write-Host "Removing failed container: $_"
        docker rm $_
    }
}
```

### Scenario 3: Container Health Check

```powershell
# Create health check script
function Test-ContainerHealth {
    param([string]$Container)
    
    $status = docker inspect --format='{{.State.Status}}' $Container
    $running = docker inspect --format='{{.State.Running}}' $Container
    $health = docker inspect --format='{{.State.Health.Status}}' $Container
    $restarts = docker inspect --format='{{.RestartCount}}' $Container
    
    [PSCustomObject]@{
        Container = $Container
        Status = $status
        Running = $running
        Health = if ($health) { $health } else { "N/A" }
        Restarts = $restarts
    }
}

# Check all containers
docker ps --format '{{.Names}}' | ForEach-Object {
    Test-ContainerHealth $_
} | Format-Table
```

## Key Takeaways

1. **Six main states**: Created, Running, Paused, Stopped/Exited, Restarting, Removed
2. **Exit codes matter**: 0 = success, 137 = killed, 143 = terminated, 1 = app error
3. **`docker stop` vs `docker kill`**: Stop is graceful, kill is forceful
4. **Restart policies**: Control automatic restart behavior
5. **`docker events`**: Monitor state changes in real-time
6. **Pause is temporary**: Freeze container without stopping
7. **`docker ps -a`**: Shows ALL states, not just running
8. **Restart count**: Indicates instability if high

## State Command Quick Reference

```powershell
# Check state
docker ps -a
docker inspect --format='{{.State.Status}}' <container>

# Lifecycle commands
docker create <image>         # Create only
docker start <container>      # Start created/stopped
docker stop <container>       # Graceful stop (SIGTERM)
docker kill <container>       # Force stop (SIGKILL)
docker restart <container>    # Stop then start
docker pause <container>      # Freeze
docker unpause <container>    # Resume
docker rm <container>         # Remove

# Exit information
docker inspect --format='{{.State.ExitCode}}' <container>
docker inspect --format='{{.State.FinishedAt}}' <container>

# Restart policy
docker run --restart <policy> <image>
docker update --restart <policy> <container>
docker inspect --format='{{.HostConfig.RestartPolicy.Name}}' <container>

# Monitoring
docker events --filter 'type=container'
docker inspect --format='{{.RestartCount}}' <container>
```

## Phase 01 Complete!

Congratulations! You've completed Phase 01. You should now understand:
- Docker architecture and core concepts
- Essential CLI commands
- Container inspection techniques
- Container lifecycle and states

### Phase 01 Assessment

Before moving to Phase 02, ensure you can:
- [ ] Explain container vs VM differences
- [ ] List running and stopped containers
- [ ] Inspect container configuration
- [ ] View and filter container logs
- [ ] Monitor resource usage with stats
- [ ] Understand exit codes
- [ ] Use restart policies
- [ ] Manage container lifecycle

### Next Steps

Proceed to **[Phase 02: Images & Registries](../Phase_02_Images_Registries/README.md)** to learn about:
- Docker images in depth
- Creating custom images with Dockerfile
- Image layers and optimization
- Working with registries
- Multi-stage builds

---

**Module Complete!** ✓

**Time to Complete**: 45-60 minutes  
**Phase 01 Complete!** 🎉  
**Next Phase**: [Images & Registries](../Phase_02_Images_Registries/README.md)  
**Home**: [Training Path](../README.md)
