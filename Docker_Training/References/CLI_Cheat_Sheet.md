# Docker CLI Cheat Sheet

Quick reference for essential Docker commands. For detailed explanations, see the training phases.

## Container Management

### Listing Containers
```powershell
docker ps                              # List running containers
docker ps -a                           # List all containers
docker ps -q                           # List container IDs only
docker ps --filter "status=exited"     # Filter by status
docker ps --format "table {{.Names}}\t{{.Status}}" # Custom format
```

### Running Containers
```powershell
# Basic
docker run <image>                     # Run container
docker run -d <image>                  # Detached mode
docker run -it <image> bash            # Interactive with terminal
docker run --rm <image>                # Remove after exit

# Naming & Networking
docker run --name <name> <image>       # Named container
docker run -p 8080:80 <image>          # Port mapping
docker run -P <image>                  # Publish all exposed ports
docker run --network <net> <image>     # Specific network

# Environment & Configuration
docker run -e VAR=value <image>        # Environment variable
docker run --env-file .env <image>     # Environment file
docker run -v vol:/path <image>        # Named volume
docker run -v /host:/cont <image>      # Bind mount
docker run -w /app <image>             # Working directory

# Resources
docker run -m 512m <image>             # Memory limit
docker run --cpus 2 <image>            # CPU limit
docker run --restart unless-stopped <image> # Restart policy

# Complete Example
docker run -d \
  --name myapp \
  -p 8080:80 \
  -e ENV=production \
  -v mydata:/data \
  -m 512m \
  --restart unless-stopped \
  nginx:alpine
```

### Starting/Stopping Containers
```powershell
docker start <container>               # Start stopped container
docker stop <container>                # Graceful stop (SIGTERM)
docker stop -t 30 <container>          # Custom timeout
docker restart <container>             # Restart container
docker kill <container>                # Force stop (SIGKILL)
docker pause <container>               # Pause processes
docker unpause <container>             # Resume processes
```

### Removing Containers
```powershell
docker rm <container>                  # Remove stopped container
docker rm -f <container>               # Force remove (stop + remove)
docker rm $(docker ps -aq)             # Remove all containers
docker container prune                 # Remove all stopped containers
docker container prune -f              # Force, no confirmation
```

## Inspection & Monitoring

### Logs
```powershell
docker logs <container>                # Show logs
docker logs -f <container>             # Follow logs (tail -f)
docker logs --tail 50 <container>      # Last 50 lines
docker logs --since 10m <container>    # Last 10 minutes
docker logs -t <container>             # Show timestamps
docker logs <container> 2>&1 | Select-String "error" # Search logs
```

### Inspection
```powershell
docker inspect <container>             # Full JSON details
docker inspect --format='{{.State.Status}}' <container> # Specific field
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container>
docker top <container>                 # Running processes
docker port <container>                # Port mappings
docker stats                           # Live resource usage
docker stats --no-stream               # Single snapshot
```

### Execution
```powershell
docker exec <container> <command>      # Execute command
docker exec -it <container> bash       # Interactive shell
docker exec -u root <container> cmd    # Run as root
docker exec -w /app <container> ls     # Set working directory
docker attach <container>              # Attach to main process
```

### File Operations
```powershell
docker cp <container>:/path/file .     # Copy from container
docker cp file <container>:/path/      # Copy to container
docker cp <container>:/app/logs ./logs # Copy directory
```

## Image Management

### Listing & Searching
```powershell
docker images                          # List images
docker images -a                       # Include intermediate
docker images -q                       # Image IDs only
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
docker search nginx                    # Search Docker Hub
docker search --filter "is-official=true" nginx
```

### Pulling & Pushing
```powershell
docker pull <image>                    # Pull latest
docker pull <image>:tag                # Specific version
docker pull ubuntu:22.04               # Example
docker login                           # Login to registry
docker logout                          # Logout
docker push <image>:tag                # Push to registry
docker tag <image> <new-name>:tag      # Tag image
```

### Building
```powershell
docker build -t <name>:tag .           # Build from Dockerfile
docker build -t <name>:tag -f <file> . # Custom Dockerfile
docker build --no-cache -t <name> .    # Build without cache
docker build --build-arg VAR=val .     # Build argument
docker build --target stage -t name .  # Multi-stage to specific stage
```

### Inspection & Analysis
```powershell
docker image inspect <image>           # Detailed info
docker history <image>                 # Show layers
docker image ls --digests              # Show digests
docker save <image> -o file.tar        # Export image
docker load -i file.tar                # Import image
```

### Removing
```powershell
docker rmi <image>                     # Remove image
docker rmi -f <image>                  # Force remove
docker image prune                     # Remove unused images
docker image prune -a                  # Remove all unused images
docker rmi $(docker images -q)         # Remove all images
```

## Network Management

### Listing & Inspection
```powershell
docker network ls                      # List networks
docker network inspect <network>       # Network details
docker network inspect bridge          # Inspect default bridge
```

### Creating & Managing
```powershell
docker network create <name>           # Create bridge network
docker network create -d bridge <name> # Specify driver
docker network create --subnet 172.20.0.0/16 <name> # Custom subnet
docker network connect <net> <cont>    # Connect container
docker network disconnect <net> <cont> # Disconnect container
docker network rm <network>            # Remove network
docker network prune                   # Remove unused networks
```

## Volume Management

### Listing & Inspection
```powershell
docker volume ls                       # List volumes
docker volume inspect <volume>         # Volume details
docker volume inspect <volume> --format='{{.Mountpoint}}' # Mount point
```

### Creating & Managing
```powershell
docker volume create <name>            # Create named volume
docker volume rm <volume>              # Remove volume
docker volume prune                    # Remove unused volumes
docker volume prune -f                 # Force, no confirmation
```

### Backup & Restore
```powershell
# Backup volume to tar.gz
docker run --rm -v <volume>:/data -v ${PWD}:/backup alpine tar -czf /backup/backup.tar.gz /data

# Restore from tar.gz
docker run --rm -v <volume>:/data -v ${PWD}:/backup alpine tar -xzf /backup/backup.tar.gz -C /
```

## Docker Compose

### Project Management
```powershell
docker compose up                      # Start services
docker compose up -d                   # Detached mode
docker compose up --build              # Rebuild images
docker compose down                    # Stop and remove
docker compose down -v                 # Also remove volumes
docker compose restart                 # Restart services
docker compose stop                    # Stop services
docker compose start                   # Start services
```

### Service Management
```powershell
docker compose ps                      # List containers
docker compose logs                    # View logs
docker compose logs -f                 # Follow logs
docker compose logs <service>          # Service-specific logs
docker compose exec <service> <cmd>    # Execute in service
docker compose exec <service> bash     # Interactive shell
docker compose run <service> <cmd>     # Run one-off command
docker compose run --rm <service> cmd  # Run and remove
```

### Building & Images
```powershell
docker compose build                   # Build services
docker compose build --no-cache        # Build without cache
docker compose pull                    # Pull service images
docker compose push                    # Push service images
```

### Utilities
```powershell
docker compose config                  # Validate and view config
docker compose config --services       # List services
docker compose config --volumes        # List volumes
docker compose top                     # Running processes
docker compose port <service> <port>   # Show public port
docker compose version                 # Show version
```

### Scaling
```powershell
docker compose up -d --scale web=3     # Scale to 3 instances
docker compose up -d --scale api=5     # Scale API service
```

## System Commands

### System Information
```powershell
docker info                            # System-wide information
docker version                         # Version details
docker --version                       # Short version
docker system df                       # Disk usage
docker system df -v                    # Verbose disk usage
docker system events                   # Real-time events
docker system events --since 10m       # Events from last 10 min
```

### Cleanup
```powershell
docker system prune                    # Remove unused data
docker system prune -a                 # Remove all unused images
docker system prune --volumes          # Include volumes
docker system prune -af --volumes      # Aggressive cleanup
docker container prune                 # Remove stopped containers
docker image prune                     # Remove unused images
docker volume prune                    # Remove unused volumes
docker network prune                   # Remove unused networks
```

## Useful Formatting Templates

### Container Information
```powershell
# Table format
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"

# JSON output
docker ps --format "{{json .}}"

# Specific fields
docker ps --format "{{.Names}}: {{.Status}}"

# With PowerShell
docker ps --format '{{.Names}}' | ForEach-Object {
    $ip = docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $_
    Write-Host "$_ : $ip"
}
```

### Image Information
```powershell
# Size-focused
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# With creation date
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.CreatedAt}}"
```

## PowerShell-Specific Tips

### Variable Usage
```powershell
# Current directory
docker run -v ${PWD}:/app myapp

# Getting values
$containerId = docker ps -q --filter "name=myapp"
docker logs $containerId

# Iterating containers
docker ps --format '{{.Names}}' | ForEach-Object {
    docker inspect $_
}
```

### Output Filtering
```powershell
# Search output
docker logs myapp 2>&1 | Select-String "error"

# Count occurrences
(docker ps -a).Count

# Export to CSV
docker stats --no-stream --format "{{.Name}},{{.CPUPerc}},{{.MemPerc}}" | 
    ConvertFrom-Csv -Header Name,CPU,Memory | 
    Export-Csv stats.csv
```

## Common Flag Combinations

### Development Container
```powershell
docker run -it --rm \
  --name dev \
  -v ${PWD}:/app \
  -p 3000:3000 \
  -e NODE_ENV=development \
  node:20-alpine \
  sh
```

### Production Container
```powershell
docker run -d \
  --name prod-app \
  -p 80:80 \
  -e NODE_ENV=production \
  -v app-data:/data \
  -m 512m \
  --cpus 1 \
  --restart unless-stopped \
  --health-cmd="curl -f http://localhost/health || exit 1" \
  --health-interval=30s \
  myapp:latest
```

### Database Container
```powershell
docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=secretpassword \
  -e POSTGRES_DB=mydb \
  -v postgres-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --restart unless-stopped \
  postgres:15
```

## Quick Troubleshooting Commands

```powershell
# Why did container exit?
docker inspect --format='{{.State.ExitCode}}' <container>
docker logs --tail 50 <container>

# Container not starting?
docker logs <container>
docker inspect <container>
docker events --filter 'container=<name>'

# Network issues?
docker network inspect <network>
docker exec <container> ping <other-container>
docker exec <container> nslookup <other-container>

# Resource issues?
docker stats --no-stream
docker inspect --format='{{.HostConfig.Memory}}' <container>

# Volume issues?
docker volume inspect <volume>
docker inspect --format='{{json .Mounts}}' <container>
```

## Getting Help

```powershell
docker --help                          # Main help
docker <command> --help                # Command-specific help
docker run --help                      # Run command help
docker compose --help                  # Compose help
```

## Environment Variables

```powershell
# Set Docker context
$env:DOCKER_HOST="tcp://192.168.1.100:2375"

# Set default buildkit
$env:DOCKER_BUILDKIT=1

# Compose file
$env:COMPOSE_FILE="docker-compose.yml"
$env:COMPOSE_PROJECT_NAME="myproject"
```

---

## Legend

- `<container>`: Container name or ID
- `<image>`: Image name or ID
- `<network>`: Network name
- `<volume>`: Volume name
- `<command>`: Command to execute
- `<name>`: Custom name
- `<tag>`: Image tag

## See Also

- [Phase 01: Essential Commands](../Phase_01_Fundamentals_CLI/02_Essential_Commands.md)
- [Phase 02: Image Management](../Phase_02_Images_Registries/README.md)
- [Phase 04: Networking & Storage](../Phase_04_Networking_Storage/README.md)
- [Phase 05: Docker Compose](../Phase_05_Docker_Compose/README.md)

---

**Pro Tip**: Use `docker <command> --help` to see all available flags and examples for any command!
