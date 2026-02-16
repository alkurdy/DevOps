# Exercise 01: Exploring Your Current Docker Environment

## Objective
Use inspection commands to analyze your existing Docker containers and gain hands-on experience with essential CLI tools.

## Duration
30-45 minutes

## Prerequisites
- Completed Modules 01-04
- Docker Desktop running
- Your existing containers (Traefik, Calibre-web, OpenMemory, etc.)

## Exercise Overview
You'll inspect and analyze the containers you already have running, learning practical skills you'll use daily.

## Part 1: Container Inventory (10 minutes)

### Task 1.1: List All Containers

```powershell
# List all running containers
docker ps

# List ALL containers (including stopped)
docker ps -a

# Count total containers
(docker ps -aq).Count
```

**Questions**:
1. How many containers do you have total?
2. How many are currently running?
3. Which container has been running the longest?

### Task 1.2: Custom Formatted Output

```powershell
# Create a clean inventory table
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"

# Get all container names
docker ps -a --format "{{.Names}}"

# Show containers with ports
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

**Challenge**: Create a custom format showing: Name, Status, and Image in a table format for ALL containers

<details>
<summary>Solution</summary>

```powershell
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"
```
</details>

## Part 2: Deep Inspection (15 minutes)

### Task 2.1: Analyze Traefik Container

```powershell
# 1. Get container ID
docker ps --filter "name=traefik" --format "{{.ID}}"

# 2. Check current status
docker inspect --format='Status: {{.State.Status}}' traefik

# 3. Is it actually running?
docker inspect --format='Running: {{.State.Running}}' traefik

# 4. When did it start?
docker inspect --format='Started: {{.State.StartedAt}}' traefik

# 5. What image is it using?
docker inspect --format='Image: {{.Config.Image}}' traefik

# 6. What's the container's hostname?
docker inspect --format='Hostname: {{.Config.Hostname}}' traefik
```

**Questions**:
1. What is Traefik's full container ID?
2. How long has Traefik been running?
3. What's the exact image name and tag?

### Task 2.2: Network Information

```powershell
# Get IP address
docker inspect --format='{{range .NetworkSettings.Networks}}IP: {{.IPAddress}}{{end}}' traefik

# Get Gateway
docker inspect --format='{{range .NetworkSettings.Networks}}Gateway: {{.Gateway}}{{end}}' traefik

# Get network name
docker inspect --format='{{range $k, $v := .NetworkSettings.Networks}}Network: {{$k}}{{end}}' traefik

# View port mappings
docker port traefik
```

**Record**:
- Traefik's IP address: _______________
- Gateway: _______________
- Network name: _______________
- Which ports are mapped to the host?

### Task 2.3: Environment Variables

```powershell
# List all environment variables
docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' traefik

# Count environment variables
(docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' traefik).Count
```

**Challenge**: Find the PATH variable value

<details>
<summary>Solution</summary>

```powershell
docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' traefik | Select-String "^PATH="
```
</details>

## Part 3: Working with Logs (10 minutes)

### Task 3.1: View Container Logs

```powershell
# View last 20 lines of Traefik logs
docker logs --tail 20 traefik

# View logs with timestamps
docker logs -t --tail 20 traefik

# Follow logs in real-time (Ctrl+C to exit)
docker logs -f traefik
```

### Task 3.2: Search Logs

```powershell
# Search for "error" in logs (case-insensitive)
docker logs traefik 2>&1 | Select-String "error" -CaseSensitive:$false

# Count error occurrences
(docker logs traefik 2>&1 | Select-String "error" -CaseSensitive:$false).Count

# Show errors with 2 lines of context
docker logs traefik 2>&1 | Select-String "error" -Context 2,2
```

**Questions**:
1. How many errors appear in Traefik's logs?
2. What types of log messages do you see?

### Task 3.3: Compare Logs Across Containers

```powershell
# Check last 5 log lines for each container
docker ps --format '{{.Names}}' | ForEach-Object {
    Write-Host "=== $_ ==="
    docker logs --tail 5 $_
    Write-Host ""
}
```

## Part 4: Resource Monitoring (10 minutes)

### Task 4.1: View Resource Usage

```powershell
# Single snapshot of all containers
docker stats --no-stream

# Watch specific containers
docker stats --no-stream traefik calibre-web openmemory

# Custom format
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

**Record**:
- Which container uses the most CPU? _______________
- Which container uses the most memory? _______________
- Total number of PIDs across all containers? _______________

### Task 4.2: Process Inspection

```powershell
# View processes in Traefik
docker top traefik

# View processes in OpenMemory (Node.js)
docker top openmemory

# View processes in Calibre-web
docker top calibre-web
```

**Questions**:
1. How many processes are running in OpenMemory?
2. What's the main process (PID 1) in each container?

## Part 5: Container States & Exit Codes (10 minutes)

### Task 5.1: Check Exit Codes

```powershell
# Find stopped containers
docker ps -a --filter "status=exited"

# Check exit code for romantic_murdock (your stopped SQLite container)
docker inspect --format='Exit Code: {{.State.ExitCode}}' romantic_murdock

# When did it finish?
docker inspect --format='Finished: {{.State.FinishedAt}}' romantic_murdock

# View last logs before exit
docker logs --tail 20 romantic_murdock
```

**Questions**:
1. What exit code does romantic_murdock have?
2. What does that exit code mean?
3. When did it stop?

### Task 5.2: Check Restart Policies

```powershell
# Check restart policy for each running container
docker ps --format '{{.Names}}' | ForEach-Object {
    $policy = docker inspect --format='{{.HostConfig.RestartPolicy.Name}}' $_
    Write-Host "$_ : $policy"
}
```

**Questions**:
1. Which containers have restart policies set?
2. What are the policies?
3. Why might some containers not have restart policies?

### Task 5.3: Test Restart Policy

```powershell
# Create a test container with restart policy
docker run -d --name restart-test --restart unless-stopped alpine sleep 300

# Verify it's running
docker ps --filter "name=restart-test"

# Check the policy
docker inspect --format='{{.HostConfig.RestartPolicy.Name}}' restart-test

# Stop it
docker stop restart-test

# Try to restart it
docker start restart-test

# Clean up
docker rm -f restart-test
```

## Part 6: Practical Container Management (15 minutes)

### Task 6.1: Create Inspection Script

Create a script to inspect any container:

```powershell
# Save as Inspect-MyContainer.ps1
param([string]$ContainerName)

Write-Host "=== Inspecting: $ContainerName ===" -ForegroundColor Cyan

# Basic Info
Write-Host "`nBasic Information:" -ForegroundColor Yellow
docker inspect --format='  Status: {{.State.Status}}' $ContainerName
docker inspect --format='  Running: {{.State.Running}}' $ContainerName
docker inspect --format='  Image: {{.Config.Image}}' $ContainerName
docker inspect --format='  Created: {{.Created}}' $ContainerName

# Network
Write-Host "`nNetwork Information:" -ForegroundColor Yellow
docker inspect --format='  {{range $k, $v := .NetworkSettings.Networks}}Network: {{$k}}, IP: {{.IPAddress}}{{end}}' $ContainerName
Write-Host "  Ports:"
docker port $ContainerName | ForEach-Object { Write-Host "    $_" }

# State
Write-Host "`nState Information:" -ForegroundColor Yellow
docker inspect --format='  Started: {{.State.StartedAt}}' $ContainerName
docker inspect --format='  Restart Count: {{.RestartCount}}' $ContainerName
docker inspect --format='  Exit Code: {{.State.ExitCode}}' $ContainerName

# Resources
Write-Host "`nResource Usage:" -ForegroundColor Yellow
docker stats --no-stream --format "  CPU: {{.CPUPerc}}, Memory: {{.MemUsage}}, PIDs: {{.PIDs}}" $ContainerName

# Recent Logs
Write-Host "`nRecent Logs (last 5 lines):" -ForegroundColor Yellow
docker logs --tail 5 $ContainerName | ForEach-Object { Write-Host "  $_" }
```

**Test the script**:
```powershell
.\Inspect-MyContainer.ps1 traefik
.\Inspect-MyContainer.ps1 openmemory
.\Inspect-MyContainer.ps1 calibre-web
```

### Task 6.2: Container Health Report

Create a health report for all containers:

```powershell
# Create health report
$report = docker ps --format '{{.Names}}' | ForEach-Object {
    $name = $_
    $status = docker inspect --format='{{.State.Status}}' $_
    $running = docker inspect --format='{{.State.Running}}' $_
    $restarts = docker inspect --format='{{.RestartCount}}' $_
    $cpu = docker stats --no-stream --format "{{.CPUPerc}}" $_
    $mem = docker stats --no-stream --format "{{.MemPerc}}" $_
    
    [PSCustomObject]@{
        Container = $name
        Status = $status
        Running = $running
        Restarts = $restarts
        CPU = $cpu
        Memory = $mem
    }
}

$report | Format-Table -AutoSize

# Export to CSV
$report | Export-Csv -Path "docker-health-report.csv" -NoTypeInformation
Write-Host "Report saved to docker-health-report.csv"
```

### Task 6.3: Port Mapping Overview

Create a port mapping table:

```powershell
# Port mapping report
Write-Host "=== Port Mappings ===" -ForegroundColor Cyan
docker ps --format '{{.Names}}' | ForEach-Object {
    Write-Host "`n$_:" -ForegroundColor Yellow
    $ports = docker port $_
    if ($ports) {
        $ports | ForEach-Object { Write-Host "  $_" }
    } else {
        Write-Host "  No ports exposed" -ForegroundColor Gray
    }
}
```

## Bonus Challenges

### Challenge 1: Find All Images Used

Create a list of unique images used by your containers:

```powershell
# Your solution here
```

<details>
<summary>Solution</summary>

```powershell
docker ps -a --format '{{.Image}}' | Sort-Object -Unique
```
</details>

### Challenge 2: Calculate Total Memory Usage

Calculate total memory used by all running containers:

```powershell
# Your solution here
```

<details>
<summary>Solution</summary>

```powershell
# This is complex due to memory format parsing
docker stats --no-stream --format "{{.MemUsage}}" | ForEach-Object {
    # Parse memory usage (e.g., "123.4MiB / 7.765GiB")
    $usage = ($_ -split ' / ')[0]
    Write-Host $usage
}
# Note: Summing requires unit conversion - advanced PowerShell
```
</details>

### Challenge 3: Automated Container Monitoring

Create a script that monitors containers and alerts if any are stopped:

```powershell
# Save as Monitor-Containers.ps1
while ($true) {
    Clear-Host
    Write-Host "=== Container Monitor ===" -ForegroundColor Cyan
    Write-Host "Time: $(Get-Date)" -ForegroundColor Gray
    
    $containers = docker ps -a --format '{{.Names}}'
    foreach ($container in $containers) {
        $status = docker inspect --format='{{.State.Status}}' $container
        if ($status -eq "running") {
            Write-Host "✓ $container - Running" -ForegroundColor Green
        } else {
            Write-Host "✗ $container - $status" -ForegroundColor Red
        }
    }
    
    Write-Host "`nPress Ctrl+C to exit"
    Start-Sleep -Seconds 5
}
```

## Exercise Completion Checklist

Before moving on, ensure you can:

- [ ] List all containers with custom formatting
- [ ] Inspect container state and configuration
- [ ] Extract specific information using `--format`
- [ ] View and search container logs
- [ ] Monitor resource usage with `docker stats`
- [ ] Check container processes with `docker top`
- [ ] Understand exit codes
- [ ] View port mappings
- [ ] Check and modify restart policies
- [ ] Create inspection scripts for automation

## Review Questions

1. What's the difference between `docker ps` and `docker ps -a`?
2. How do you extract just the IP address from a container?
3. What does exit code 137 mean?
4. How do you follow logs in real-time?
5. What's the recommended restart policy for production services?
6. How can you check if a stopped container exited successfully?
7. What command shows processes inside a container?
8. How do you view port mappings?

## Next Steps

Proceed to Exercise 02 or move to Phase 02:

- **Exercise 02**: [CLI Command Practice](Exercise_02_CLI_Practice.md)
- **Phase 02**: [Images & Registries](../../Phase_02_Images_Registries/README.md)

---

**Exercise Complete!** ✓

**Time**: 30-45 minutes  
**Skills Practiced**: Inspection, Logging, Monitoring, State Management  
**Next**: [Exercise 02](Exercise_02_CLI_Practice.md) or [Phase 02](../../Phase_02_Images_Registries/README.md)
