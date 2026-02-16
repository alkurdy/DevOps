# Phase 01: Docker Fundamentals & CLI Basics

## Overview
Master the foundational concepts and essential CLI commands needed for all Docker operations.

## Learning Objectives

By the end of this phase, you will:
- Understand Docker architecture and core concepts
- Navigate the Docker CLI confidently
- Inspect and analyze running containers
- Understand container states and lifecycle
- Use essential Docker commands for daily operations
- Analyze your existing container environment

## Duration
**3-5 hours** (including exercises)

## Prerequisites
- Docker Desktop installed and running
- Completed [QUICK_START.md](../QUICK_START.md)
- Basic command-line knowledge

## Phase Structure

### Module 01: Docker Architecture & Concepts
**File**: [01_Docker_Architecture.md](01_Docker_Architecture.md)  
**Time**: 45-60 minutes

Topics:
- What is Docker and containerization?
- Docker vs Virtual Machines
- Docker architecture (Client-Server model)
- Docker Engine, daemon, and CLI
- Images vs Containers
- Docker Desktop on Windows (WSL2 backend)

### Module 02: Essential CLI Commands
**File**: [02_Essential_Commands.md](02_Essential_Commands.md)  
**Time**: 60-90 minutes

Topics:
- Docker CLI structure and syntax
- Help system (`--help` flag)
- Container commands (`ps`, `start`, `stop`, `restart`)
- Image commands (`images`, `pull`, `rmi`)
- System commands (`info`, `version`, `system df`)
- Formatting output (`--format` flag)
- Filtering and searching

### Module 03: Inspecting Containers
**File**: [03_Inspecting_Containers.md](03_Inspecting_Containers.md)  
**Time**: 60-90 minutes

Topics:
- Understanding `docker inspect`
- Reading JSON output
- Extracting specific information with templates
- Viewing container logs (`docker logs`)
- Real-time monitoring (`docker stats`)
- Checking running processes (`docker top`)
- Analyzing your current containers

### Module 04: Container States & Lifecycle
**File**: [04_Container_States.md](04_Container_States.md)  
**Time**: 45-60 minutes

Topics:
- Container lifecycle stages
- Created vs Running vs Stopped vs Paused
- Exit codes and what they mean
- Auto-restart policies
- Graceful shutdown vs forced kill
- Removing containers safely

## Hands-On Exercises

### Exercise 1: Explore Your Current Environment
**File**: [Exercises/Exercise_01_Current_Environment.md](Exercises/Exercise_01_Current_Environment.md)

Analyze your existing containers (Traefik, Calibre-web, etc.) using inspection commands.

### Exercise 2: CLI Command Practice
**File**: [Exercises/Exercise_02_CLI_Practice.md](Exercises/Exercise_02_CLI_Practice.md)

Practice essential commands with test containers.

### Exercise 3: Container Lifecycle Management
**File**: [Exercises/Exercise_03_Lifecycle.md](Exercises/Exercise_03_Lifecycle.md)

Start, stop, restart, and remove test containers while monitoring states.

### Exercise 4: Log Analysis Challenge
**File**: [Exercises/Exercise_04_Logs.md](Exercises/Exercise_04_Logs.md)

Practice log viewing and filtering techniques.

## Key Commands Covered

```powershell
# Container Management
docker ps                          # List running containers
docker ps -a                       # List all containers
docker start <container>           # Start container
docker stop <container>            # Stop container
docker restart <container>         # Restart container
docker rm <container>              # Remove container
docker pause <container>           # Pause container
docker unpause <container>         # Unpause container

# Inspection & Monitoring
docker inspect <container>         # Detailed container info
docker logs <container>            # View logs
docker logs -f <container>         # Follow logs
docker stats                       # Resource usage
docker top <container>             # Container processes
docker port <container>            # Port mappings

# Image Management
docker images                      # List images
docker image ls                    # List images (alternate)
docker pull <image>                # Download image
docker rmi <image>                 # Remove image
docker image inspect <image>       # Image details

# System Information
docker info                        # System-wide information
docker version                     # Version details
docker system df                   # Disk usage
docker system events               # Real-time events
```

## Practice Environment Setup

Create a dedicated practice directory:

```powershell
cd C:\Users\alkur\OneDrive\Documents\DevOps\Docker_Training\Phase_01_Fundamentals_CLI
mkdir Exercises
mkdir Notes
```

## Learning Tips

### For Windows Users
- Docker Desktop uses WSL2 backend - commands work identically to Linux
- Use PowerShell or Windows Terminal for best experience
- Path separators in containers use forward slashes even on Windows

### CLI Best Practices
1. Always read the help: `docker <command> --help`
2. Use tab completion in PowerShell
3. Use `--format` for clean, parseable output
4. Name your containers for easier management
5. Use `--rm` for temporary test containers

### Common Pitfalls to Avoid
- ❌ Confusing images with containers
- ❌ Forgetting containers are still running in background
- ❌ Not reading error messages fully
- ❌ Using `docker system prune` without understanding scope

## Assessment Checklist

Before moving to Phase 02, ensure you can:

### Conceptual Understanding
- [ ] Explain the difference between an image and a container
- [ ] Describe the Docker client-server architecture
- [ ] Understand what happens when you run `docker run`
- [ ] Explain container lifecycle states

### Practical Skills
- [ ] List all containers (running and stopped)
- [ ] Inspect any container and extract specific information
- [ ] View and filter container logs
- [ ] Monitor container resource usage
- [ ] Start, stop, and restart containers
- [ ] Remove containers safely
- [ ] List and inspect images

### Applied Knowledge
- [ ] Analyze your Traefik container configuration
- [ ] Identify why a container stopped
- [ ] Find port mappings for running containers
- [ ] Determine disk space used by Docker

## Real-World Scenarios

This phase prepares you for:
- Troubleshooting container issues
- Daily container operations
- Monitoring container health
- Managing development environments
- Understanding existing Docker setups

## Reference Materials

### Official Documentation
- [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/cli/)
- [Docker Architecture](https://docs.docker.com/get-started/overview/)
- [Container Lifecycle](https://docs.docker.com/engine/reference/run/)

### Quick References
- [CLI Cheat Sheet](../References/CLI_Cheat_Sheet.md)
- [Container States Diagram](../References/Container_States.png)

## Next Steps

After completing Phase 01:
1. Complete all exercises
2. Review the assessment checklist
3. Take notes on any challenging concepts
4. Proceed to [Phase 02: Images & Registries](../Phase_02_Images_Registries/README.md)

## Navigation

- **Previous**: [Quick Start Guide](../QUICK_START.md)
- **Next**: [Phase 02: Images & Registries](../Phase_02_Images_Registries/README.md)
- **Home**: [Training Path Home](../README.md)

---

**Ready to begin?** Start with [01_Docker_Architecture.md](01_Docker_Architecture.md)

**Last Updated**: February 16, 2026
