# Quick Start Guide

## Welcome to Docker Training!

This guide will help you verify your setup and start your Docker learning journey.

## Step 1: Verify Docker Installation

Open PowerShell and run:

```powershell
docker --version
docker compose version
```

Expected output:
```
Docker version 24.x.x or later
Docker Compose version v2.x.x or later
```

## Step 2: Check Docker Status

```powershell
docker info
```

This should show your Docker system information without errors.

## Step 3: Explore Your Current Containers

Let's examine what you already have running:

```powershell
# List all containers (running and stopped)
docker ps -a

# List only running containers
docker ps

# See resource usage
docker stats --no-stream
```

### Your Current Stack Analysis

You have **6 containers** in your environment:

1. **traefik** - Reverse proxy (Running)
2. **lazylibrarian** - Media management (Running)
3. **calibre-web** - Ebook library (Running)
4. **openmemory** - Node.js app (Running)
5. **romantic_murdock** - SQLite (Stopped)
6. **adguardhome** - DNS/Ad blocker (Recently stopped)

## Step 4: Your First Docker Commands

Try these commands to start exploring:

```powershell
# Inspect a running container (Traefik)
docker inspect traefik

# View logs from a container
docker logs traefik --tail 20

# Check container processes
docker top traefik

# View detailed stats for specific container
docker stats traefik --no-stream
```

## Step 5: List Your Images

```powershell
# Show all images
docker images

# Show image sizes
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

You currently have **8 images** consuming approximately **8.6GB** of disk space.

## Step 6: Understanding Your Setup

### Network Configuration
Your containers use various networking modes:
- **Traefik**: Binds to ports 80, 443, 8080 on 192.168.12.210
- **OpenMemory**: Exposed on 0.0.0.0:8081 (all interfaces)
- **LazyLibrarian**: Port 5299 on host network

### Container Naming Patterns
You'll notice two naming patterns:
- **Named containers**: traefik, calibre-web, lazylibrarian (explicitly named)
- **Auto-generated names**: romantic_murdock (Docker assigns random names)

**Best Practice**: Always use `--name` flag for production containers!

## Step 7: Set Up Your Training Environment

Create a sandbox directory for practice:

```powershell
# Create training workspace
mkdir C:\Users\alkur\OneDrive\Documents\DevOps\Docker_Training\Sandbox
cd C:\Users\alkur\OneDrive\Documents\DevOps\Docker_Training\Sandbox

# Create directories for exercises
mkdir exercises
mkdir compose-examples
mkdir dockerfiles
```

## Step 8: Run Your First Test Container

```powershell
# Pull and run a simple test container
docker run --name hello-docker --rm hello-world

# Run an interactive container
docker run -it --name my-ubuntu --rm ubuntu:latest bash
# Inside the container, type: cat /etc/os-release
# Type 'exit' to leave
```

## Step 9: Begin Phase 01

You're ready to start! Open:
```
Phase_01_Fundamentals_CLI/README.md
```

## Common Commands Reference

### Container Management
```powershell
docker ps                    # List running containers
docker ps -a                 # List all containers
docker start <name>          # Start stopped container
docker stop <name>           # Stop running container
docker restart <name>        # Restart container
docker rm <name>             # Remove stopped container
docker logs <name>           # View container logs
docker exec -it <name> bash  # Access container shell
```

### Image Management
```powershell
docker images                # List images
docker pull <image>          # Download image
docker rmi <image>           # Remove image
docker image prune           # Remove unused images
```

### System Information
```powershell
docker info                  # Docker system info
docker version               # Version details
docker stats                 # Live resource usage
docker system df             # Disk usage
```

## Safety Tips for Learning

### DO's ✅
- Use `--rm` flag for temporary test containers
- Name your containers with `--name` for easy reference
- Stop containers before removing them
- Practice in the Sandbox directory
- Read command help: `docker <command> --help`

### DON'Ts ❌
- Don't remove your production containers (traefik, calibre-web, etc.) while learning
- Don't use `docker system prune -a` without understanding the impact
- Don't expose containers to the internet during testing
- Don't run containers as root unless necessary

## Troubleshooting Quick Checks

### Docker Desktop Not Running
```powershell
# Check if Docker Desktop is running
Get-Process "Docker Desktop" -ErrorAction SilentlyContinue
```

### WSL2 Issues (Windows)
```powershell
# Check WSL status
wsl --status

# Restart WSL if needed
wsl --shutdown
# Then restart Docker Desktop
```

### Container Won't Start
```powershell
# Check detailed error logs
docker logs <container-name>

# Inspect container configuration
docker inspect <container-name>
```

## Learning Path Navigation

- **Current Location**: Quick Start
- **Next**: [Phase 01: Fundamentals & CLI](Phase_01_Fundamentals_CLI/README.md)
- **Main Menu**: [Return to README](README.md)

## Time Estimate

**Quick Start Setup**: 15-20 minutes

## Checklist

Before moving to Phase 01, verify:

- [ ] Docker Desktop is running
- [ ] `docker --version` works
- [ ] `docker ps` shows your containers
- [ ] `docker images` shows your images
- [ ] You can run `docker run --rm hello-world`
- [ ] Sandbox directory created
- [ ] You understand the basic commands above

## Ready to Learn?

Once you've completed this checklist, you're ready to dive into **Phase 01**!

---

**Need help?** Check the [Troubleshooting Guide](References/Troubleshooting_Guide.md) or Docker's official documentation.

**Last Updated**: February 16, 2026
