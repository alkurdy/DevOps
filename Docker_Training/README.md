# Docker & Containers Training Path

## Overview
This training path provides a structured, hands-on approach to mastering Docker and containerization on Windows, with a focus on CLI proficiency for cross-platform use.

## Training Philosophy
- **CLI-First Approach**: All exercises focus on command-line operations for maximum portability
- **Hands-On Learning**: Practical exercises using real-world scenarios
- **Progressive Complexity**: Each phase builds on previous knowledge
- **Windows Integration**: Specific guidance for Docker on Windows while maintaining cross-platform skills

## Your Current Docker Environment
Based on your running containers, you're already working with:
- **Reverse Proxy**: Traefik v3.2
- **DNS/Ad Blocking**: AdGuard Home
- **Media Management**: Calibre-web, LazyLibrarian
- **Development**: Node.js 20
- **Database**: SQLite3

This training will help you understand, manage, and expand these services confidently.

## Training Phases

### [Phase 01: Docker Fundamentals & CLI Basics](Phase_01_Fundamentals_CLI/README.md)
**Duration**: 3-5 hours
- Docker architecture and concepts
- Essential CLI commands
- Inspecting your current containers
- Container states and lifecycle
- Working with running and stopped containers

### [Phase 02: Images & Registries](Phase_02_Images_Registries/README.md)
**Duration**: 4-6 hours
- Understanding Docker images
- Image layers and caching
- Working with Docker Hub and other registries
- Pulling, tagging, and managing images
- Creating custom images with Dockerfile
- Multi-stage builds

### [Phase 03: Container Lifecycle Management](Phase_03_Container_Lifecycle/README.md)
**Duration**: 4-6 hours
- Starting and stopping containers
- Container logs and debugging
- Executing commands in running containers
- Resource limits and constraints
- Environment variables and configuration
- Container restart policies

### [Phase 04: Networking & Storage](Phase_04_Networking_Storage/README.md)
**Duration**: 5-7 hours
- Docker networking modes
- Creating and managing networks
- Port mapping and exposure
- Container communication
- Volumes vs bind mounts
- Volume management and backup
- Persistent data strategies

### [Phase 05: Docker Compose](Phase_05_Docker_Compose/README.md)
**Duration**: 5-7 hours
- Docker Compose fundamentals
- YAML syntax and structure
- Multi-container applications
- Service orchestration
- Recreating your current stack with Compose
- Environment management
- Compose CLI commands

### [Phase 06: Advanced Topics & Best Practices](Phase_06_Advanced_Topics/README.md)
**Duration**: 6-8 hours
- Security best practices
- Image optimization techniques
- Health checks and monitoring
- Logging strategies
- Backup and disaster recovery
- Docker on Windows specifics (WSL2, Windows containers)
- CI/CD integration basics
- Troubleshooting common issues

## Getting Started

1. **Start Here**: Read the [QUICK_START.md](QUICK_START.md) guide
2. **Begin Training**: Start with Phase 01
3. **Track Progress**: Use the checklist in each phase
4. **Practice**: Complete all exercises before moving to next phase

## Prerequisites

### Required
- Docker Desktop for Windows installed and running
- Basic PowerShell/command-line knowledge
- Text editor (VS Code recommended)
- Internet connection for pulling images

### Recommended
- WSL2 enabled (for better performance)
- 16GB+ RAM
- 50GB+ free disk space

## Learning Resources

### Official Documentation
- [Docker Documentation](https://docs.docker.com/)
- [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/cli/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)

### Additional Materials
- Docker Cheat Sheet (see References folder)
- Common patterns and examples
- Troubleshooting guides

## Project Structure

```
Docker_Training/
├── README.md (this file)
├── QUICK_START.md
├── copilot-instructions.md
├── Phase_01_Fundamentals_CLI/
│   ├── README.md
│   ├── 01_Docker_Architecture.md
│   ├── 02_Essential_Commands.md
│   ├── 03_Inspecting_Containers.md
│   └── Exercises/
├── Phase_02_Images_Registries/
├── Phase_03_Container_Lifecycle/
├── Phase_04_Networking_Storage/
├── Phase_05_Docker_Compose/
├── Phase_06_Advanced_Topics/
└── References/
    ├── CLI_Cheat_Sheet.md
    ├── Dockerfile_Best_Practices.md
    └── Troubleshooting_Guide.md
```

## Estimated Total Time
**30-40 hours** of structured learning, plus additional practice time

## Completion Goals

By the end of this training path, you will:
- ✅ Confidently use Docker CLI on any platform
- ✅ Build, manage, and troubleshoot containers
- ✅ Create optimized Docker images
- ✅ Design multi-container applications
- ✅ Implement networking and persistent storage
- ✅ Use Docker Compose for orchestration
- ✅ Apply security and optimization best practices
- ✅ Deploy and maintain production-ready containers

## Next Steps

1. Review [QUICK_START.md](QUICK_START.md)
2. Begin with [Phase 01: Fundamentals & CLI](Phase_01_Fundamentals_CLI/README.md)
3. Complete each phase sequentially
4. Practice with your existing containers

---

**Note**: This training path is designed to be completed at your own pace. Each phase includes checkpoints and exercises to reinforce learning.

**Last Updated**: February 16, 2026
