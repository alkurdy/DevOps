# Module 02: Essential CLI Commands

## Introduction

The Docker CLI is your primary interface for container management. Mastering these commands enables you to work with Docker on any platform - Windows, Linux, or macOS.

## CLI Structure & Syntax

### Command Format

```
docker [management-command] [sub-command] [options] [arguments]
```

**Examples**:
```powershell
docker container ls              # Management command style
docker ps                        # Legacy style (still works)
docker container run nginx       # Management command
docker run nginx                 # Legacy equivalent
```

### Modern vs Legacy Commands

Docker has two command styles:

| Legacy | Modern | Purpose |
|--------|--------|---------|
| `docker ps` | `docker container ls` | List containers |
| `docker images` | `docker image ls` | List images |
| `docker rm` | `docker container rm` | Remove container |
| `docker rmi` | `docker image rm` | Remove image |

**Recommendation**: Learn both! Legacy commands are shorter; modern commands are more explicit.

## The Help System

**Most important command**:
```powershell
docker --help            # Main help
docker run --help        # Command-specific help
docker container --help  # Management group help
```

### Help Navigation

```powershell
# Top-level commands
docker --help

# Management commands
docker container --help
docker image --help
docker network --help
docker volume --help

# Specific command help
docker run --help
docker exec --help
```

**Practice**: Always read `--help` before using an unfamiliar command!

## Container Management Commands

### Listing Containers

```powershell
# List running containers
docker ps
docker container ls

# List all containers (including stopped)
docker ps -a
docker container ls -a

# List only container IDs
docker ps -q

# List with custom format
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

**Try it now**:
```powershell
# See your running containers
docker ps

# See all containers including stopped
docker ps -a
```

#### Useful Filters

```powershell
# Show only running containers
docker ps --filter "status=running"

# Show containers with specific name
docker ps --filter "name=traefik"

# Show containers based on specific image
docker ps --filter "ancestor=node:20"

# Combine filters
docker ps -a --filter "status=exited" --filter "ancestor=ubuntu"
```

### Starting & Stopping Containers

```powershell
# Start a stopped container
docker start <container-name-or-id>
docker start traefik

# Stop a running container (graceful, SIGTERM)
docker stop <container-name-or-id>
docker stop traefik

# Restart a container
docker restart <container-name-or-id>
docker restart traefik

# Start multiple containers
docker start container1 container2 container3

# Stop all running containers
docker stop $(docker ps -q)
```

**Important**: 
- `docker start` resumes an existing container
- `docker run` creates a NEW container from an image

### Creating Containers (docker run)

The `docker run` command creates and starts a container:

```powershell
# Basic syntax
docker run [options] <image> [command]

# Simple example
docker run hello-world

# Interactive terminal
docker run -it ubuntu bash
# -i: interactive (keep STDIN open)
# -t: allocate a TTY (terminal)

# Detached mode (background)
docker run -d nginx
# -d: detached mode

# Named container
docker run --name my-nginx nginx
# --name: assign a specific name

# Auto-remove after exit
docker run --rm ubuntu echo "Hello"
# --rm: remove container when it exits

# Port mapping
docker run -p 8080:80 nginx
# -p HOST_PORT:CONTAINER_PORT

# Environment variables
docker run -e "VAR=value" nginx
# -e: set environment variable

# Full example
docker run -d \
  --name web-server \
  -p 8080:80 \
  -e "ENV=production" \
  --rm \
  nginx
```

### Pausing Containers

```powershell
# Pause container (freeze processes)
docker pause <container>

# Unpause container
docker unpause <container>

# Example
docker pause traefik
docker ps  # Status shows "Paused"
docker unpause traefik
```

**Use case**: Temporarily freeze resource-intensive container.

### Removing Containers

```powershell
# Remove stopped container
docker rm <container>

# Force remove running container
docker rm -f <container>

# Remove multiple containers
docker rm container1 container2

# Remove all stopped containers
docker container prune

# Remove all containers (stopped and running)
docker rm -f $(docker ps -aq)
```

⚠️ **Warning**: `docker rm` is permanent! Ensure you don't need the container.

## Image Management Commands

### Listing Images

```powershell
# List all images
docker images
docker image ls

# Show all images including intermediate
docker images -a

# Show only image IDs
docker images -q

# Custom format
docker images --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}"
```

**Try it now**:
```powershell
# See your images
docker images

# See sizes
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

### Pulling Images

```powershell
# Pull latest version
docker pull ubuntu

# Pull specific version
docker pull ubuntu:22.04

# Pull from specific registry
docker pull mcr.microsoft.com/dotnet/sdk:7.0

# View available tags
# Visit: https://hub.docker.com
```

**Image naming**:
```
[registry/][username/]repository[:tag]

Examples:
ubuntu                          # Docker Hub official image
ubuntu:22.04                    # Specific version
nginx:alpine                    # Alpine variant
myregistry.com/app:v1.2        # Private registry
```

### Inspecting Images

```powershell
# Detailed image information
docker image inspect ubuntu

# View image layers
docker image history ubuntu

# Check image size
docker images ubuntu
```

### Removing Images

```powershell
# Remove image
docker rmi <image>
docker image rm <image>

# Remove multiple images
docker rmi image1 image2 image3

# Remove unused images
docker image prune

# Remove all images
docker rmi $(docker images -q)

# Force remove (even if containers exist)
docker rmi -f <image>
```

## Inspection & Monitoring Commands

### docker inspect

Get detailed information in JSON format:

```powershell
# Inspect container
docker inspect traefik

# Inspect image
docker inspect nginx

# Extract specific field with --format
docker inspect --format='{{.State.Status}}' traefik
docker inspect --format='{{.NetworkSettings.IPAddress}}' traefik
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' traefik
```

**Useful fields**:
- `.State.Status` - Current state
- `.State.Running` - Boolean, is running?
- `.NetworkSettings.IPAddress` - Container IP
- `.Config.Env` - Environment variables
- `.Mounts` - Volume mounts
- `.RestartPolicy` - Restart configuration

### docker logs

View container output:

```powershell
# Show all logs
docker logs <container>

# Follow logs (like tail -f)
docker logs -f <container>

# Show last N lines
docker logs --tail 50 <container>

# Show logs since timestamp
docker logs --since 2024-01-01T00:00:00 <container>

# Show logs from last N minutes
docker logs --since 10m <container>

# Show timestamps
docker logs -t <container>

# Combination
docker logs -f --tail 100 -t traefik
```

**Try it now**:
```powershell
# View Traefik logs
docker logs --tail 20 traefik

# Follow live logs (Ctrl+C to exit)
docker logs -f traefik
```

### docker stats

Real-time resource usage:

```powershell
# Monitor all running containers
docker stats

# Monitor specific containers
docker stats traefik calibre-web

# Show once, don't stream
docker stats --no-stream

# Custom format
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

**Metrics shown**:
- CPU % - CPU usage percentage
- MEM USAGE / LIMIT - Memory consumption
- MEM % - Memory percentage
- NET I/O - Network traffic
- BLOCK I/O - Disk I/O
- PIDS - Number of processes

### docker top

View processes running in container:

```powershell
# Show processes
docker top <container>

# Example
docker top traefik
```

### docker port

View port mappings:

```powershell
# Show all port mappings
docker port <container>

# Show specific port mapping
docker port traefik 80

# Example output:
# 80/tcp -> 192.168.12.210:80
```

## System Information Commands

### docker info

System-wide information:

```powershell
docker info
```

**Shows**:
- Containers (running, stopped, paused)
- Images count
- Server version
- Storage driver
- OS/Arch
- CPUs
- Memory
- Docker Root Dir

### docker version

Version information:

```powershell
docker version        # Detailed format
docker --version      # Short format
```

### docker system df

Disk usage:

```powershell
# Disk usage summary
docker system df

# Verbose output
docker system df -v
```

**Shows**:
- Images space
- Containers space
- Volumes space
- Build cache

### docker events

Real-time Docker events:

```powershell
# Stream all events
docker events

# Filter events
docker events --filter 'type=container'
docker events --filter 'event=start'
docker events --filter 'container=traefik'

# Since timestamp
docker events --since '2024-01-01T00:00:00'
```

## Executing Commands in Containers

### docker exec

Run commands inside running containers:

```powershell
# Execute single command
docker exec <container> <command>
docker exec traefik ls /etc

# Interactive shell
docker exec -it <container> bash
docker exec -it traefik /bin/sh

# Run as specific user
docker exec -u root <container> whoami

# Set working directory
docker exec -w /app <container> ls

# Full example
docker exec -it traefik /bin/sh
```

**Try it now**:
```powershell
# Get shell in your Node container
docker exec -it openmemory bash

# Inside container:
node --version
npm --version
pwd
ls
exit
```

**Common uses**:
- Debugging
- Running maintenance tasks
- Checking configurations
- Installing tools temporarily

## Copying Files

### docker cp

Copy files between host and container:

```powershell
# Copy from container to host
docker cp <container>:/path/in/container /path/on/host
docker cp traefik:/etc/traefik/traefik.yml ./traefik-config.yml

# Copy from host to container
docker cp /path/on/host <container>:/path/in/container
docker cp ./config.yml traefik:/etc/traefik/config.yml

# Copy directory
docker cp <container>:/app/logs ./logs
```

## Output Formatting

### Format Templates

Use Go templates for custom output:

```powershell
# Basic format
docker ps --format "{{.Names}}"

# Table format
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# JSON format
docker ps --format "{{json .}}"

# Multiple fields
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

**Available placeholders**:

For `docker ps`:
- `{{.ID}}` - Container ID
- `{{.Names}}` - Container name
- `{{.Image}}` - Image name
- `{{.Status}}` - Status
- `{{.Ports}}` - Port mappings
- `{{.CreatedAt}}` - Creation time

For `docker images`:
- `{{.Repository}}` - Image name
- `{{.Tag}}` - Image tag
- `{{.ID}}` - Image ID
- `{{.Size}}` - Image size
- `{{.CreatedAt}}` - Creation time

### Filtering

```powershell
# Filter by status
docker ps --filter "status=running"
docker ps --filter "status=exited"

# Filter by name
docker ps --filter "name=traefik"

# Filter by label
docker ps --filter "label=com.docker.compose.project"

# Filter by image
docker ps --filter "ancestor=nginx"

# Multiple filters (AND logic)
docker ps --filter "status=running" --filter "name=web"
```

## Cleanup Commands

### Prune Commands

Remove unused resources:

```powershell
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune

# Remove everything unused
docker system prune

# Remove everything INCLUDING volumes
docker system prune --volumes

# Force (no confirmation)
docker system prune -f
```

⚠️ **Warning**: Prune commands are destructive! Review what will be removed.

## Practical Command Combinations

### Common Workflows

```powershell
# Stop and remove container
docker stop myapp && docker rm myapp

# Remove container and image
docker rm -f myapp && docker rmi myapp-image

# Get container IP address
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' traefik

# Follow logs with patterns
docker logs -f traefik 2>&1 | Select-String "error"

# List containers with specific ports
docker ps --format "table {{.Names}}\t{{.Ports}}" | Select-String "8080"

# Check container health
docker inspect --format='{{.State.Health.Status}}' myapp

# Get environment variables
docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' traefik
```

### Quick Reference Scripts

Create PowerShell functions for common tasks:

```powershell
# Add to your PowerShell profile

# Stop all containers
function Stop-AllContainers {
    docker stop $(docker ps -q)
}

# Remove all stopped containers
function Remove-StoppedContainers {
    docker container prune -f
}

# Show container IPs
function Get-ContainerIPs {
    docker ps -q | ForEach-Object {
        $name = docker inspect --format='{{.Name}}' $_
        $ip = docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $_
        Write-Host "$name : $ip"
    }
}
```

## Hands-On Practice

### Exercise 1: Basic Commands

```powershell
# List all your current containers
docker ps -a

# List all images
docker images

# Check Docker disk usage
docker system df

# View system info
docker info
```

### Exercise 2: Container Operations

```powershell
# Run a test container
docker run -d --name test-nginx nginx

# Check it's running
docker ps | Select-String "test-nginx"

# View logs
docker logs test-nginx

# Stop it
docker stop test-nginx

# Start it again
docker start test-nginx

# Remove it
docker stop test-nginx
docker rm test-nginx
```

### Exercise 3: Inspection

```powershell
# Get Traefik's IP address
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' traefik

# View Traefik's environment variables
docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' traefik

# Check resource usage
docker stats --no-stream traefik

# View port mappings
docker port traefik
```

### Exercise 4: Working with Images

```powershell
# Pull Alpine Linux (small image)
docker pull alpine

# Check the size
docker images alpine

# Run interactive shell
docker run -it --rm alpine sh
# Inside: apk add --no-cache curl
# Inside: curl --version
# Inside: exit

# Image is removed automatically (--rm flag)
docker ps -a | Select-String "alpine"  # Not found
```

## PowerShell-Specific Tips

### Using PowerShell Features

```powershell
# Select-String for filtering
docker ps | Select-String "traefik"

# Export to CSV
docker ps --format "{{.Names}},{{.Status}},{{.Image}}" | ConvertFrom-Csv -Header Name,Status,Image | Export-Csv containers.csv

# Count running containers
(docker ps -q).Count

# Format as table
docker ps --format "table {{.Names}}\t{{.Status}}" | Format-Table
```

### Aliases

```powershell
# Create aliases in PowerShell profile
Set-Alias -Name dps -Value 'docker ps'
Set-Alias -Name di -Value 'docker images'
Set-Alias -Name dex -Value 'docker exec -it'
```

## Common Pitfalls & Solutions

### Issue 1: Container Name Conflicts

```powershell
# Error: name already in use
docker run --name myapp nginx
# Error!

# Solution: Remove existing container first
docker rm myapp
# Or use different name
docker run --name myapp2 nginx
```

### Issue 2: Port Already in Use

```powershell
# Error: port is already allocated
docker run -p 8080:80 nginx
# Error!

# Solution: Find what's using the port
docker ps --filter "publish=8080"
# Or use different port
docker run -p 8081:80 nginx
```

### Issue 3: Cannot Remove Running Container

```powershell
# Error: container is running
docker rm myapp
# Error!

# Solution: Stop first, or force
docker stop myapp && docker rm myapp
# Or force remove
docker rm -f myapp
```

## Key Takeaways

1. **Two command styles exist**: Legacy (shorter) and Management (clearer)
2. **Use `--help` extensively**: Your best learning tool
3. **`docker ps`**: Most frequently used command
4. **`docker logs -f`**: Essential for debugging
5. **`docker exec -it`**: Access running containers
6. **Format output**: Use `--format` for clean, parseable data
7. **Filter results**: Use `--filter` to narrow down output
8. **Cleanup regularly**: Use `prune` commands to free space

## Command Reference Table

| Task | Command |
|------|---------|
| List running containers | `docker ps` |
| List all containers | `docker ps -a` |
| Start container | `docker start <name>` |
| Stop container | `docker stop <name>` |
| Restart container | `docker restart <name>` |
| Remove container | `docker rm <name>` |
| View logs | `docker logs <name>` |
| Follow logs | `docker logs -f <name>` |
| View stats | `docker stats` |
| Execute command | `docker exec <name> <cmd>` |
| Interactive shell | `docker exec -it <name> bash` |
| List images | `docker images` |
| Pull image | `docker pull <image>` |
| Remove image | `docker rmi <image>` |
| Inspect object | `docker inspect <object>` |
| System info | `docker info` |
| Disk usage | `docker system df` |
| Cleanup | `docker system prune` |

## Next Module

You now have a solid foundation in Docker CLI commands. Next, you'll learn how to deeply inspect containers:

**[03_Inspecting_Containers.md](03_Inspecting_Containers.md)** - Deep dive into container analysis

---

**Module Complete!** ✓

**Time to Complete**: 60-90 minutes  
**Next**: [Inspecting Containers](03_Inspecting_Containers.md)  
**Phase Home**: [Phase 01 README](README.md)
