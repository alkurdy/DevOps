# Module 03: Inspecting Containers

## Introduction

Effective container management requires deep inspection capabilities. This module teaches you how to extract detailed information from running and stopped containers using various inspection tools.

## The docker inspect Command

`docker inspect` returns detailed configuration and state information in JSON format.

### Basic Usage

```powershell
# Inspect a container
docker inspect <container-name-or-id>

# Inspect an image
docker image inspect <image-name>

# Inspect multiple objects
docker inspect container1 container2 image1
```

### JSON Output Structure

The output contains comprehensive information:

```json
[
    {
        "Id": "c8f0a104b260...",
        "Created": "2024-02-16T10:00:00Z",
        "Path": "/init",
        "Args": [],
        "State": {
            "Status": "running",
            "Running": true,
            "Paused": false,
            "Restarting": false,
            "OOMKilled": false,
            "Dead": false,
            "Pid": 12345,
            "ExitCode": 0,
            "StartedAt": "2024-02-16T10:00:05Z"
        },
        "Image": "sha256:453218f67b13...",
        "Name": "/lazylibrarian",
        "Config": {
            "Hostname": "c8f0a104b260",
            "Env": ["PATH=/usr/local/bin:..."],
            "Cmd": ["/init"],
            "Image": "lscr.io/linuxserver/lazylibrarian:latest"
        },
        "NetworkSettings": {
            "Networks": {
                "bridge": {
                    "IPAddress": "172.17.0.2",
                    "Gateway": "172.17.0.1"
                }
            },
            "Ports": {
                "5299/tcp": [{"HostIp": "192.168.12.210", "HostPort": "5299"}]
            }
        },
        "Mounts": [...]
    }
]
```

### Extracting Specific Information

Use `--format` (or `-f`) with Go templates:

```powershell
# Get container status
docker inspect --format='{{.State.Status}}' traefik

# Get IP address
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' traefik

# Get running state
docker inspect --format='{{.State.Running}}' traefik

# Get start time
docker inspect --format='{{.State.StartedAt}}' traefik

# Get exit code
docker inspect --format='{{.State.ExitCode}}' traefik

# Get image ID
docker inspect --format='{{.Image}}' traefik

# Get restart count
docker inspect --format='{{.RestartCount}}' traefik
```

### Useful Inspection Fields

#### Container State
```powershell
# Current status
docker inspect --format='{{.State.Status}}' <container>

# Is it running?
docker inspect --format='{{.State.Running}}' <container>

# When did it start?
docker inspect --format='{{.State.StartedAt}}' <container>

# When did it finish?
docker inspect --format='{{.State.FinishedAt}}' <container>

# Exit code (0 = normal, >0 = error)
docker inspect --format='{{.State.ExitCode}}' <container>

# Process ID on host
docker inspect --format='{{.State.Pid}}' <container>
```

#### Network Configuration
```powershell
# IP address
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container>

# Gateway
docker inspect --format='{{range .NetworkSettings.Networks}}{{.Gateway}}{{end}}' <container>

# Network name
docker inspect --format='{{range $k, $v := .NetworkSettings.Networks}}{{$k}}{{end}}' <container>

# Port mappings
docker inspect --format='{{json .NetworkSettings.Ports}}' <container>

# MAC address
docker inspect --format='{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' <container>
```

#### Configuration
```powershell
# Hostname
docker inspect --format='{{.Config.Hostname}}' <container>

# Environment variables
docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' <container>

# Working directory
docker inspect --format='{{.Config.WorkingDir}}' <container>

# Command and args
docker inspect --format='{{.Config.Cmd}}' <container>

# Exposed ports
docker inspect --format='{{json .Config.ExposedPorts}}' <container>

# Labels
docker inspect --format='{{range $k, $v := .Config.Labels}}{{$k}}={{$v}}{{println}}{{end}}' <container>
```

#### Resource Limits
```powershell
# Memory limit
docker inspect --format='{{.HostConfig.Memory}}' <container>

# CPU shares
docker inspect --format='{{.HostConfig.CpuShares}}' <container>

# CPU quota
docker inspect --format='{{.HostConfig.CpuQuota}}' <container>
```

#### Volumes & Mounts
```powershell
# All mounts
docker inspect --format='{{json .Mounts}}' <container>

# Mount sources
docker inspect --format='{{range .Mounts}}{{.Source}}{{println}}{{end}}' <container>

# Mount destinations
docker inspect --format='{{range .Mounts}}{{.Destination}}{{println}}{{end}}' <container>
```

## Analyzing Your Containers

Let's inspect your existing containers:

### Traefik Analysis

```powershell
# Basic info
docker inspect traefik

# Specific details
docker inspect --format='Status: {{.State.Status}}' traefik
docker inspect --format='IP: {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' traefik
docker inspect --format='Started: {{.State.StartedAt}}' traefik

# Configuration
docker inspect --format='Image: {{.Config.Image}}' traefik
docker inspect --format='Hostname: {{.Config.Hostname}}' traefik

# Ports
docker inspect --format='{{json .NetworkSettings.Ports}}' traefik | ConvertFrom-Json
```

**Try it now**:
```powershell
# Run these commands for your Traefik container
docker inspect --format='{{.State.Status}}' traefik
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' traefik
docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' traefik
```

### Node Container (OpenMemory) Analysis

```powershell
# Check what version of Node
docker exec openmemory node --version

# View environment
docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' openmemory

# Check mounts (is data persistent?)
docker inspect --format='{{range .Mounts}}Type: {{.Type}}, Source: {{.Source}}, Dest: {{.Destination}}{{println}}{{end}}' openmemory
```

## Working with Container Logs

Logs are crucial for debugging and monitoring.

### Basic Log Viewing

```powershell
# View all logs
docker logs <container>

# Last N lines
docker logs --tail 50 <container>

# Follow logs (real-time)
docker logs -f <container>

# Show timestamps
docker logs -t <container>
```

### Advanced Log Filtering

```powershell
# Logs since specific time
docker logs --since "2024-02-16T10:00:00" <container>

# Logs from last 10 minutes
docker logs --since 10m <container>

# Logs from last hour
docker logs --since 1h <container>

# Logs until specific time
docker logs --until "2024-02-16T12:00:00" <container>

# Combine options
docker logs --tail 100 --since 30m -t -f <container>
```

### PowerShell Log Analysis

```powershell
# Search logs for errors
docker logs traefik 2>&1 | Select-String "error" -CaseSensitive:$false

# Count occurrences
docker logs traefik 2>&1 | Select-String "error" | Measure-Object

# Get unique error lines
docker logs traefik 2>&1 | Select-String "error" | Sort-Object -Unique

# Export logs to file
docker logs traefik > traefik-logs.txt

# Search with context
docker logs traefik 2>&1 | Select-String "error" -Context 2,2
```

### Log Drivers

Docker supports multiple logging drivers:

```powershell
# Check log driver for container
docker inspect --format='{{.HostConfig.LogConfig.Type}}' traefik

# Common drivers:
# - json-file (default)
# - none
# - syslog
# - journald
# - local
```

## Monitoring Container Resources

### docker stats

Real-time resource monitoring:

```powershell
# Monitor all containers
docker stats

# Monitor specific containers
docker stats traefik calibre-web openmemory

# Single snapshot
docker stats --no-stream

# Custom format
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

# JSON output
docker stats --format "{{json .}}" --no-stream
```

**Metrics Explained**:

| Metric | Description |
|--------|-------------|
| **CONTAINER ID** | Short container ID |
| **NAME** | Container name |
| **CPU %** | CPU usage percentage |
| **MEM USAGE / LIMIT** | Current memory / Maximum allowed |
| **MEM %** | Memory usage percentage |
| **NET I/O** | Network bytes sent/received |
| **BLOCK I/O** | Disk bytes read/written |
| **PIDS** | Number of processes/threads |

**Try it now**:
```powershell
# Monitor your containers for 10 seconds
docker stats --no-stream

# Watch in real-time (Ctrl+C to exit)
docker stats
```

### Analyzing Resource Usage

```powershell
# Find high CPU containers
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}" | Sort-Object -Property @{Expression={[double]($_.Split())[1].Replace('%',''))}} -Descending

# Find high memory containers
docker stats --no-stream --format "table {{.Name}}\t{{.MemPerc}}" | Sort-Object -Property @{Expression={[double]($_.Split())[1].Replace('%',''))}} -Descending

# Export stats to CSV
docker stats --no-stream --format "{{.Name}},{{.CPUPerc}},{{.MemPerc}}" | ConvertFrom-Csv -Header Name,CPU,Memory | Export-Csv stats.csv
```

## Container Process Information

### docker top

View processes running inside container:

```powershell
# Show processes
docker top <container>

# Custom format (ps syntax)
docker top <container> aux
docker top <container> -eo pid,cmd
```

**Try it now**:
```powershell
# See processes in your containers
docker top traefik
docker top openmemory
docker top calibre-web
```

**Output columns**:
- **UID**: User ID
- **PID**: Process ID on host
- **PPID**: Parent process ID
- **C**: CPU utilization
- **STIME**: Start time
- **TTY**: Terminal type
- **TIME**: Total CPU time
- **CMD**: Command

### Understanding PIDs

```powershell
# Container's main process PID on host
docker inspect --format='{{.State.Pid}}' traefik

# This PID exists in host process list
Get-Process -Id <pid>

# But inside container, it's PID 1
docker exec traefik ps aux  # Shows PID 1
```

## Port Mapping Inspection

### docker port

View port mappings:

```powershell
# Show all port mappings
docker port <container>

# Check specific port
docker port <container> 80

# Example with Traefik
docker port traefik
# Output:
# 80/tcp -> 192.168.12.210:80
# 443/tcp -> 192.168.12.210:443
# 8080/tcp -> 192.168.12.210:8080
```

### Port Mapping via Inspect

```powershell
# Get port mappings as JSON
docker inspect --format='{{json .NetworkSettings.Ports}}' traefik

# Extract specific port
docker inspect --format='{{(index (index .NetworkSettings.Ports "80/tcp") 0).HostPort}}' traefik

# List all exposed ports
docker inspect --format='{{range $p, $conf := .NetworkSettings.Ports}}{{$p}} {{end}}' traefik
```

## Health Checks

Some containers include health checks:

```powershell
# Check if container has health check
docker inspect --format='{{.State.Health.Status}}' <container>

# Possible values:
# - starting
# - healthy
# - unhealthy
# - none (no health check)

# View health check logs
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' <container>

# Health check configuration
docker inspect --format='{{json .Config.Healthcheck}}' <container>
```

## Practical Inspection Workflows

### Troubleshooting Container Issues

```powershell
# Step 1: Check if running
docker ps -a --filter "name=myapp"

# Step 2: Check status
docker inspect --format='{{.State.Status}}' myapp

# Step 3: If exited, check exit code
docker inspect --format='{{.State.ExitCode}}' myapp

# Step 4: View recent logs
docker logs --tail 50 myapp

# Step 5: Check error in logs
docker logs myapp 2>&1 | Select-String "error"

# Step 6: Check resource limits
docker inspect --format='Memory: {{.HostConfig.Memory}}' myapp
```

### Container Inventory Script

Create a PowerShell script to inventory all containers:

```powershell
# Save as Get-DockerInventory.ps1
$containers = docker ps -aq

foreach ($container in $containers) {
    $name = docker inspect --format='{{.Name}}' $container
    $status = docker inspect --format='{{.State.Status}}' $container
    $image = docker inspect --format='{{.Config.Image}}' $container
    $ip = docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $container
    
    [PSCustomObject]@{
        Name = $name.TrimStart('/')
        Status = $status
        Image = $image
        IP = $ip
    }
} | Format-Table -AutoSize
```

**Usage**:
```powershell
.\Get-DockerInventory.ps1
```

### Network Configuration Report

```powershell
# For each container, show network details
docker ps --format '{{.Names}}' | ForEach-Object {
    Write-Host "Container: $_"
    docker inspect --format='  IP: {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $_
    docker inspect --format='  Gateway: {{range .NetworkSettings.Networks}}{{.Gateway}}{{end}}' $_
    docker inspect --format='  Network: {{range $k, $v := .NetworkSettings.Networks}}{{$k}}{{end}}' $_
    docker port $_
    Write-Host ""
}
```

## Advanced Inspection Techniques

### Comparing Containers

```powershell
# Compare two containers' configurations
$config1 = docker inspect container1 | ConvertFrom-Json
$config2 = docker inspect container2 | ConvertFrom-Json

# Compare images
$config1.Image
$config2.Image

# Compare environment variables
Compare-Object $config1.Config.Env $config2.Config.Env
```

### Finding Containers by Criteria

```powershell
# Find containers using specific image
docker ps -a --filter "ancestor=node:20"

# Find containers with specific label
docker ps --filter "label=com.docker.compose.project=myapp"

# Find containers exposing specific port
docker ps --format '{{.Names}}' | Where-Object {
    (docker port $_ 2>$null) -match "8080"
}

# Find containers with high restart count
docker ps -q | ForEach-Object {
    $name = docker inspect --format='{{.Name}}' $_
    $restarts = docker inspect --format='{{.RestartCount}}' $_
    if ([int]$restarts -gt 5) {
        Write-Host "$name has restarted $restarts times"
    }
}
```

### Extract All Environment Variables

```powershell
# Format as name=value
docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' <container>

# Convert to PowerShell hashtable
$env = @{}
docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' traefik | ForEach-Object {
    $parts = $_ -split '=', 2
    $env[$parts[0]] = $parts[1]
}
$env
```

## Hands-On Exercises

### Exercise 1: Deep Inspection

Inspect your Traefik container:

```powershell
# 1. Get container ID, name, and status
docker ps --filter "name=traefik"

# 2. Get full JSON output
docker inspect traefik > traefik-inspect.json

# 3. Extract specific information
docker inspect --format='Status: {{.State.Status}}' traefik
docker inspect --format='Running: {{.State.Running}}' traefik
docker inspect --format='Started: {{.State.StartedAt}}' traefik
docker inspect --format='Image: {{.Config.Image}}' traefik

# 4. Network information
docker inspect --format='{{range .NetworkSettings.Networks}}IP: {{.IPAddress}}, Gateway: {{.Gateway}}{{end}}' traefik

# 5. Port mappings
docker port traefik

# 6. Environment variables
docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' traefik
```

### Exercise 2: Log Analysis

Analyze logs from all containers:

```powershell
# 1. View recent logs from each container
docker ps --format '{{.Names}}' | ForEach-Object {
    Write-Host "=== $_ ==="
    docker logs --tail 5 $_
    Write-Host ""
}

# 2. Search for errors
docker ps --format '{{.Names}}' | ForEach-Object {
    $errors = docker logs $_ 2>&1 | Select-String "error" -CaseSensitive:$false
    if ($errors) {
        Write-Host "$_ has errors:"
        $errors
    }
}

# 3. Check Traefik access logs
docker logs --tail 20 traefik

# 4. Follow logs in real-time
docker logs -f traefik
# (Press Ctrl+C to exit)
```

### Exercise 3: Resource Monitoring

Monitor resource usage:

```powershell
# 1. View stats snapshot
docker stats --no-stream

# 2. Monitor specific containers
docker stats --no-stream traefik calibre-web openmemory

# 3. Custom format
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# 4. Find highest CPU user
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}"

# 5. Real-time monitoring
docker stats
# Watch for 30 seconds, then Ctrl+C
```

### Exercise 4: Create Inspection Script

Create a comprehensive container inspection script:

```powershell
# Save as Inspect-Container.ps1
param(
    [Parameter(Mandatory=$true)]
    [string]$ContainerName
)

Write-Host "=== Container Information: $ContainerName ===" -ForegroundColor Cyan

# Basic Info
Write-Host "`n--- Basic Info ---" -ForegroundColor Yellow
docker inspect --format='ID: {{.Id}}' $ContainerName
docker inspect --format='Name: {{.Name}}' $ContainerName
docker inspect --format='Status: {{.State.Status}}' $ContainerName
docker inspect --format='Running: {{.State.Running}}' $ContainerName
docker inspect --format='Image: {{.Config.Image}}' $ContainerName

# State
Write-Host "`n--- State ---" -ForegroundColor Yellow
docker inspect --format='Started: {{.State.StartedAt}}' $ContainerName
docker inspect --format='PID: {{.State.Pid}}' $ContainerName
docker inspect --format='Exit Code: {{.State.ExitCode}}' $ContainerName
docker inspect --format='Restart Count: {{.RestartCount}}' $ContainerName

# Network
Write-Host "`n--- Network ---" -ForegroundColor Yellow
docker inspect --format='{{range $k, $v := .NetworkSettings.Networks}}Network: {{$k}}, IP: {{.IPAddress}}, Gateway: {{.Gateway}}{{end}}' $ContainerName
Write-Host "Ports:"
docker port $ContainerName

# Resources
Write-Host "`n--- Resources ---" -ForegroundColor Yellow
docker stats --no-stream --format "CPU: {{.CPUPerc}}, Memory: {{.MemUsage}}" $ContainerName

# Recent Logs
Write-Host "`n--- Recent Logs (last 10 lines) ---" -ForegroundColor Yellow
docker logs --tail 10 $ContainerName

Write-Host "`n=== End of Report ===" -ForegroundColor Cyan
```

**Usage**:
```powershell
.\Inspect-Container.ps1 -ContainerName traefik
```

## Key Takeaways

1. **`docker inspect`** provides comprehensive JSON data about containers and images
2. **Use `--format`** to extract specific fields without parsing full JSON
3. **`docker logs`** is essential for troubleshooting; use `-f` to follow in real-time
4. **`docker stats`** shows live resource usage; use `--no-stream` for snapshots
5. **`docker top`** reveals processes running inside containers
6. **`docker port`** quickly shows port mappings
7. **Combine with PowerShell** for powerful analysis and reporting
8. **Regular monitoring** helps catch issues before they become problems

## Common Inspection Patterns

```powershell
# Is container running?
docker inspect --format='{{.State.Running}}' <container>

# What's the IP?
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container>

# When did it start?
docker inspect --format='{{.State.StartedAt}}' <container>

# What ports are exposed?
docker port <container>

# What's using CPU?
docker stats --no-stream

# What are the recent errors?
docker logs --tail 50 <container> 2>&1 | Select-String "error"
```

## Next Module

You now know how to inspect and monitor containers. Next, learn about container lifecycle states:

**[04_Container_States.md](04_Container_States.md)** - Understanding container lifecycle

---

**Module Complete!** ✓

**Time to Complete**: 60-90 minutes  
**Next**: [Container States & Lifecycle](04_Container_States.md)  
**Phase Home**: [Phase 01 README](README.md)
