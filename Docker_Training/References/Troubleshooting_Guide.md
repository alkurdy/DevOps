# Docker Troubleshooting Guide

Quick reference for diagnosing and solving common Docker issues.

## Systematic Troubleshooting Approach

### Step-by-Step Process
1. **Identify the symptom** - What's not working?
2. **Check container status** - Is it running?
3. **Review logs** - What does the container say?
4. **Inspect configuration** - Is it configured correctly?
5. **Check resources** - Are limits reached?
6. **Test connectivity** - Can it reach what it needs?
7. **Verify permissions** - Access issues?

## Container Issues

### Container Won't Start

**Symptoms**: Container exits immediately, or won't start at all

**Diagnosis**:
```powershell
# Check if container exists
docker ps -a --filter "name=<container>"

# Check exit code
docker inspect --format='{{.State.ExitCode}}' <container>

# View logs
docker logs <container>

# View recent events
docker events --since 5m --filter 'container=<container>'
```

**Common Causes & Solutions**:

1. **Exit Code 1** - Application error
   ```powershell
   # Check logs for errors
   docker logs <container>
   # Fix application code or configuration
   ```

2. **Exit Code 127** - Command not found
   ```powershell
   # Check CMD/ENTRYPOINT in Dockerfile
   docker inspect --format='{{.Config.Cmd}}' <container>
   # Verify command exists in image
   docker run --rm <image> which <command>
   ```

3. **Exit Code 137** - Out of memory
   ```powershell
   # Check memory limit
   docker inspect --format='{{.HostConfig.Memory}}' <container>
   # Increase memory or optimize application
   docker run -m 1g <image>
   ```

4. **Exit Code 143** - Stopped (SIGTERM)
   ```powershell
   # Container was deliberately stopped
   # Check if it should have a restart policy
   docker update --restart unless-stopped <container>
   ```

### Container Keeps Restarting

**Symptoms**: Container constantly restarting, high restart count

**Diagnosis**:
```powershell
# Check restart count
docker inspect --format='{{.RestartCount}}' <container>

# Check restart policy
docker inspect --format='{{.HostConfig.RestartPolicy.Name}}' <container>

# Follow logs to see crash pattern
docker logs -f <container>

# Check for OOM kills
docker inspect --format='{{.State.OOMKilled}}' <container>
```

**Solutions**:
```powershell
# Temporarily remove restart policy to debug
docker update --restart no <container>

# Check resource usage
docker stats --no-stream <container>

# Fix application issue
# Then re-enable restart policy
docker update --restart unless-stopped <container>
```

### Container Runs but Application Doesn't Work

**Diagnosis**:
```powershell
# Check if process is running
docker top <container>

# Check port mappings
docker port <container>

# Get shell access
docker exec -it <container> sh

# Inside container:
# - Check processes: ps aux
# - Check listening ports: netstat -tlnp or ss -tlnp
# - Check files: ls -la
# - Test application: curl localhost:port
```

**Common Issues**:
- Application listening on localhost instead of 0.0.0.0
- Wrong port exposed
- Environment variables not set
- Missing dependencies

## Network Issues

### Cannot Connect to Container from Host

**Diagnosis**:
```powershell
# Check port mapping
docker port <container>

# Should show: 80/tcp -> 0.0.0.0:8080

# Test from host
curl http://localhost:8080

# Check if container is actually listening
docker exec <container> netstat -tlnp
# or
docker exec <container> ss -tlnp
```

**Solutions**:

1. **No port published**:
   ```powershell
   # Port not mapped
   docker run -p 8080:80 <image>
   ```

2. **Wrong port**:
   ```powershell
   # Check what port app listens on
   docker exec <container> netstat -tlnp
   # Map correct port
   docker run -p 8080:3000 <image>  # If app uses 3000
   ```

3. **Application listening on 127.0.0.1**:
   ```dockerfile
   # Application must listen on 0.0.0.0, not 127.0.0.1
   # In code: app.listen(3000, '0.0.0.0')
   ```

### Containers Cannot Communicate

**Diagnosis**:
```powershell
# Check networks
docker network ls

# Check which network containers are on
docker inspect --format='{{range $k, $v := .NetworkSettings.Networks}}{{$k}}{{end}}' <container1>
docker inspect --format='{{range $k, $v := .NetworkSettings.Networks}}{{$k}}{{end}}' <container2>

# From one container, try to reach another
docker exec <container1> ping <container2>
docker exec <container1> nslookup <container2>
docker exec <container1> curl http://<container2>:port
```

**Solutions**:

1. **On different networks**:
   ```powershell
   # Create custom network
   docker network create mynetwork
   
   # Connect both containers
   docker network connect mynetwork <container1>
   docker network connect mynetwork <container2>
   ```

2. **Using default bridge - no DNS**:
   ```powershell
   # Default bridge doesn't have DNS
   # Use custom bridge instead
   docker network create mynetwork
   docker run --network mynetwork <image>
   ```

3. **Firewall blocking**:
   ```powershell
   # Check Docker iptables rules
   # On Windows with WSL2, check Windows Firewall
   ```

### DNS Resolution Not Working

**Diagnosis**:
```powershell
# Test DNS from container
docker exec <container> nslookup google.com
docker exec <container> ping google.com

# Check container's DNS servers
docker exec <container> cat /etc/resolv.conf

# Check Docker's DNS
docker inspect --format='{{.HostConfig.DNS}}' <container>
```

**Solutions**:
```powershell
# Set custom DNS
docker run --dns 8.8.8.8 --dns 8.8.4.4 <image>

# Or in daemon.json (C:\ProgramData\Docker\config\daemon.json)
{
  "dns": ["8.8.8.8", "8.8.4.4"]
}
```

## Volume & Storage Issues

### Permission Denied Errors

**Symptoms**: Cannot write to mounted volume

**Diagnosis**:
```powershell
# Check volume mount
docker inspect --format='{{json .Mounts}}' <container>

# Check user container runs as
docker inspect --format='{{.Config.User}}' <container>

# Inside container, check permissions
docker exec <container> ls -la /mounted/path
```

**Solutions**:

1. **Wrong permissions on bind mount**:
   ```powershell
   # On Windows, ensure file sharing is enabled
   # Docker Desktop -> Settings -> Resources -> File Sharing
   
   # Check folder permissions in Windows
   ```

2. **Container runs as non-root**:
   ```powershell
   # Option 1: Run as root (not recommended)
   docker run -u root <image>
   
   # Option 2: Change ownership (recommended)
   docker run -v vol:/data <image>
   docker exec -u root <container> chown -R user:group /data
   
   # Option 3: Use named volume instead of bind mount
   docker volume create mydata
   docker run -v mydata:/data <image>
   ```

### Data Not Persisting

**Diagnosis**:
```powershell
# Check if volume is mounted
docker inspect --format='{{json .Mounts}}' <container>

# Check volume
docker volume inspect <volume>

# Verify data location
docker volume inspect <volume> --format='{{.Mountpoint}}'
```

**Solutions**:

1. **No volume mounted**:
   ```powershell
   # Create and mount volume
   docker volume create mydata
   docker run -v mydata:/app/data <image>
   ```

2. **Wrong path in container**:
   ```powershell
   # Check where app writes data
   docker exec <container> find / -name "*.db" 2>/dev/null
   # Mount to correct path
   docker run -v mydata:/correct/path <image>
   ```

3. **Using anonymous volume**:
   ```powershell
   # Anonymous volumes are hard to manage
   # Use named volumes instead
   docker volume create mydata
   docker run -v mydata:/data <image>
   ```

### Out of Disk Space

**Diagnosis**:
```powershell
# Check Docker disk usage
docker system df
docker system df -v

# Check for large images
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | Sort-Object

# Check for many stopped containers
docker ps -a
```

**Solutions**:
```powershell
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune
docker image prune -a  # Remove ALL unused images

# Remove unused volumes
docker volume prune

# Full cleanup
docker system prune -a --volumes

# On Windows, reset disk image
# Docker Desktop -> Settings -> Resources -> Advanced -> Disk image size
# Or: Troubleshoot -> Clean / Purge data
```

## Build Issues

### Build Fails with "No Such File or Directory"

**Diagnosis**:
```powershell
# Check build context
cd <directory-with-dockerfile>
ls

# Check what Docker sees
docker build -t test .
```

**Solutions**:

1. **File not in build context**:
   ```dockerfile
   # Files must be in build context (Dockerfile's directory or subdirectories)
   # Cannot COPY files from parent directory
   
   # Wrong:
   COPY ../file.txt /app/
   
   # Right:
   COPY file.txt /app/
   ```

2. **Check .dockerignore**:
   ```powershell
   # .dockerignore might be excluding files
   cat .dockerignore
   ```

### Build is Very Slow

**Diagnosis**:
```powershell
# Check build context size
docker build -t test . --no-cache
# If "Sending build context" takes long, context is too large
```

**Solutions**:

1. **Create .dockerignore**:
   ```
   node_modules/
   .git/
   *.log
   tmp/
   .vscode/
   ```

2. **Use multi-stage builds**:
   ```dockerfile
   FROM node:20 AS builder
   COPY package*.json ./
   RUN npm install
   COPY . .
   RUN npm run build
   
   FROM node:20-alpine
   COPY --from=builder /app/dist ./dist
   ```

### Image Too Large

**Solutions**:
```dockerfile
# Use smaller base image
FROM node:20-alpine  # Instead of node:20

# Combine RUN commands
RUN apt-get update && \
    apt-get install -y package && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Use multi-stage build
FROM node:20 AS builder
RUN npm install
# ... build

FROM node:20-alpine
COPY --from=builder /app/dist ./
```

## Docker Desktop Issues (Windows)

### Docker Desktop Won't Start

**Solutions**:
```powershell
# 1. Restart Docker Desktop
# Right-click system tray icon -> Restart

# 2. Check WSL2
wsl --status
wsl --list --verbose

# 3. Restart WSL
wsl --shutdown
# Then start Docker Desktop

# 4. Check Hyper-V (if using Hyper-V backend)
Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V

# 5. Reset Docker Desktop
# Settings -> Troubleshoot -> Reset to factory defaults
```

### Slow Performance on Windows

**Solutions**:
```powershell
# 1. Use WSL2 file system, not Windows filesystem
# Store code in: \\wsl$\docker-desktop\
# Not in: C:\Users\...

# 2. Configure WSL2 resources
# Create/edit: C:\Users\<user>\.wslconfig
[wsl2]
memory=8GB
processors=4
swap=2GB

# 3. Restart WSL
wsl --shutdown
# Restart Docker Desktop

# 4. Disable unused features
# Docker Desktop -> Settings -> General
# Uncheck features you don't use
```

### File Sharing Not Working

**Solutions**:
```powershell
# 1. Check file sharing settings
# Docker Desktop -> Settings -> Resources -> File Sharing
# Add the directory

# 2. Use WSL2 path
docker run -v /mnt/c/Users/alkur/project:/app <image>

# 3. Use PowerShell $PWD
docker run -v ${PWD}:/app <image>
```

## Docker Compose Issues

### Compose File Invalid

**Diagnosis**:
```powershell
# Validate compose file
docker compose config

# Check specific service
docker compose config --services
docker compose config --volumes
```

**Common Errors**:

1. **Indentation error**:
   ```yaml
   # Wrong - mixing spaces and tabs
   services:
   	web:  # Tab here
     image: nginx  # Spaces here
   
   # Right - consistent spaces
   services:
     web:
       image: nginx
   ```

2. **Version mismatch**:
   ```yaml
   # Use recent version
   version: '3.8'
   ```

### Service Dependencies Not Working

**Solutions**:
```yaml
services:
  web:
    depends_on:
      db:
        condition: service_healthy  # Wait for health check
  db:
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
```

### Environment Variables Not Working

**Diagnosis**:
```powershell
# Check what variables are set
docker compose config
docker compose exec <service> env
```

**Solutions**:
```yaml
# Use .env file
# Create .env in same directory as docker-compose.yml
DB_PASSWORD=secret

# In docker-compose.yml
services:
  db:
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    # Or
    env_file:
      - .env
```

## Logging & Debugging Tips

### Enable Debug Logging

```powershell
# Docker daemon debug mode
# Edit: C:\ProgramData\Docker\config\daemon.json
{
  "debug": true,
  "log-level": "debug"
}
# Restart Docker Desktop

# Docker CLI debug
$env:DOCKER_DEBUG = "1"
docker info
```

### Capture Full Diagnostic

```powershell
# Get all container info
docker inspect <container> > container-info.json

# Get all logs
docker logs <container> > container-logs.txt 2>&1

# Get system info
docker info > docker-info.txt
docker version > docker-version.txt
docker system df > docker-disk.txt

# WSL info (Windows)
wsl --status > wsl-status.txt
wsl --list --verbose > wsl-list.txt
```

## Quick Diagnostic Commands

```powershell
# Container health check
function Test-ContainerHealth {
    param($container)
    
    Write-Host "=== $container ===" -ForegroundColor Cyan
    docker inspect --format='Status: {{.State.Status}}' $container
    docker inspect --format='Running: {{.State.Running}}' $container
    docker inspect --format='Exit Code: {{.State.ExitCode}}' $container
    docker inspect --format='Restarts: {{.RestartCount}}' $container
    Write-Host "Recent logs:"
    docker logs --tail 5 $container
}

# Network diagnostic
function Test-Network {
    param($container, $target)
    
    Write-Host "Testing network from $container to $target"
    docker exec $container ping -c 3 $target
    docker exec $container nslookup $target
}

# Volume check
function Test-Volume {
    param($container)
    
    $mounts = docker inspect --format='{{json .Mounts}}' $container | ConvertFrom-Json
    $mounts | ForEach-Object {
        Write-Host "Type: $($_.Type), Source: $($_.Source), Dest: $($_.Destination)"
    }
}
```

## Getting Help

When stuck:

1. **Read the logs**
   ```powershell
   docker logs <container>
   ```

2. **Check configuration**
   ```powershell
   docker inspect <container>
   ```

3. **Search error message**
   - Google the exact error
   - Check Docker forums
   - Search GitHub issues

4. **Reproduce in isolation**
   - Test with minimal example
   - Remove complexity

5. **Ask for help**
   - Provide `docker version`
   - Provide `docker info`
   - Share Dockerfile/compose file
   - Include exact error messages
   - Show what you've tried

## See Also

- [Phase 01: Container States](../Phase_01_Fundamentals_CLI/04_Container_States.md)
- [Phase 04: Networking](../Phase_04_Networking_Storage/01_Networking_Fundamentals.md)
- [Phase 06: Advanced Troubleshooting](../Phase_06_Advanced_Topics/06_Troubleshooting.md)
- [Docker Documentation](https://docs.docker.com/)

---

**Remember**: Always start with logs and work systematically through the diagnostic steps!
