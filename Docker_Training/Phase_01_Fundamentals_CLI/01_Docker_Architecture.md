# Module 01: Docker Architecture & Concepts

## Introduction

Understanding Docker's architecture is essential for effective container management. This module covers the foundational concepts that underpin all Docker operations.

## What is Docker?

Docker is an open-source platform that automates the deployment of applications inside lightweight, portable containers. It packages an application and its dependencies into a standardized unit called a container.

### Key Benefits
- **Consistency**: "Works on my machine" becomes "works everywhere"
- **Isolation**: Applications run independently without conflicts
- **Efficiency**: Containers share the OS kernel, using fewer resources than VMs
- **Portability**: Run anywhere Docker is installed
- **Speed**: Start in seconds, not minutes
- **Scalability**: Easy to scale up or down

## Containers vs Virtual Machines

### Virtual Machines
```
┌─────────────────────────────────────────┐
│          Application A                  │
│  ┌──────────────────────────────────┐  │
│  │  App Dependencies & Libraries    │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │      Guest OS (Full OS)          │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│          Hypervisor                     │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│          Host OS                        │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│          Physical Hardware              │
└─────────────────────────────────────────┘
```

### Docker Containers
```
┌────────┬────────┬────────┐
│ App A  │ App B  │ App C  │
├────────┼────────┼────────┤
│ Libs   │ Libs   │ Libs   │
└────────┴────────┴────────┘
┌─────────────────────────┐
│   Docker Engine         │
└─────────────────────────┘
┌─────────────────────────┐
│   Host OS               │
└─────────────────────────┘
┌─────────────────────────┐
│   Physical Hardware     │
└─────────────────────────┘
```

### Comparison

| Aspect | Virtual Machine | Container |
|--------|----------------|-----------|
| **OS** | Full guest OS per VM | Shares host OS kernel |
| **Size** | Gigabytes | Megabytes |
| **Startup** | Minutes | Seconds |
| **Resource Usage** | Heavy | Lightweight |
| **Isolation** | Complete | Process-level |
| **Performance** | Slower (overhead) | Near-native |
| **Portability** | Less portable | Highly portable |

### When to Use Each

**Use VMs when:**
- You need complete OS-level isolation
- Running different operating systems
- Strong security boundaries required
- Legacy application requirements

**Use Containers when:**
- Running microservices
- CI/CD pipelines
- Rapid scaling needed
- Development environments
- Resource efficiency is priority

## Docker Architecture

Docker uses a **client-server architecture**:

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Client (CLI)                  │
│                      docker commands                    │
└────────────┬────────────────────────────────────────────┘
             │ REST API
             ▼
┌─────────────────────────────────────────────────────────┐
│              Docker Daemon (dockerd)                    │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Container Management                            │  │
│  │  Image Management                                │  │
│  │  Network Management                              │  │
│  │  Volume Management                               │  │
│  └──────────────────────────────────────────────────┘  │
└────────────┬────────────────────────────────────────────┘
             │
    ┌────────┴─────────┬──────────┐
    ▼                  ▼          ▼
┌─────────┐      ┌─────────┐  ┌─────────┐
│Container│      │Container│  │Container│
└─────────┘      └─────────┘  └─────────┘
```

### Components

#### 1. Docker Client
- The command-line tool you interact with
- Sends commands to Docker daemon via REST API
- Can communicate with local or remote daemons
- Examples: `docker ps`, `docker run`, `docker build`

#### 2. Docker Daemon (dockerd)
- Runs as a background service
- Manages all Docker objects (containers, images, networks, volumes)
- Listens for API requests
- Handles container lifecycle
- Communicates with other daemons for distributed features

#### 3. Docker Registry
- Stores Docker images
- **Docker Hub**: Public registry (default)
- **Private registries**: Self-hosted or cloud-based
- Where `docker pull` downloads from
- Where `docker push` uploads to

#### 4. Docker Objects

**Images**:
- Read-only templates
- Blueprint for containers
- Contain application code and dependencies
- Built from Dockerfile
- Stored in layers (more on this in Phase 02)

**Containers**:
- Runnable instances of images
- Isolated processes
- Can be created, started, stopped, deleted
- Have their own filesystem, networking, process space
- Ephemeral by default

**Networks**:
- Enable container communication
- Multiple network drivers (bridge, host, overlay, etc.)
    - bridge: Default for standalone containers, isolated network, NATed.
    - host: Containers share host network stack, no isolation.
    - overlay: For multi-host communication in swarm mode.
    - macvlan: Assigns MAC addresses to containers, making them appear as physical devices on the network.
    - ipvlan: Similar to macvlan but uses IP addresses for isolation.
    - container: Connects containers directly to each other without a network driver.
- Containers can join multiple networks, allowing for complex communication patterns.

E.g., a web app container can be on both a frontend network (for client access) and a backend network (for database access).

**Volumes**:
- Persistent data storage
- Survive container deletion
- Can be shared between containers
- Managed by Docker

## Docker on Windows: WSL2 Backend

Your Docker Desktop uses the **WSL2 (Windows Subsystem for Linux)** backend:

```
┌─────────────────────────────────────────┐
│         Windows 10/11                   │
│  ┌────────────────────────────────────┐ │
│  │    Docker Desktop                  │ │
│  │    (GUI & Management)              │ │
│  └──────────────┬─────────────────────┘ │
│                 │                        │
│  ┌──────────────▼─────────────────────┐ │
│  │         WSL2 VM                    │ │
│  │  ┌──────────────────────────────┐ │ │
│  │  │  Docker Engine (Linux)       │ │ │
│  │  │  Containers run here         │ │ │
│  │  └──────────────────────────────┘ │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Why WSL2?

**Advantages**:
- Full Linux kernel compatibility
- Better performance than Hyper-V
- Lower resource usage
- Faster file I/O
- Native Linux tools available

### Windows vs Linux Containers

**Linux Containers** (default):
- Run on WSL2
- Most common use case
- Same images work everywhere
- Your current setup uses these

**Windows Containers** (optional):
- Native Windows processes
- For Windows Server apps
- Less common
- Require explicit switching

## Core Concepts

### Images vs Containers

**Image = Class**  
**Container = Instance**

```powershell
# Pull an image (like downloading a class definition)
docker pull ubuntu:latest

# Run containers (like creating instances)
docker run --name instance1 ubuntu
docker run --name instance2 ubuntu
# Both containers based on same image, but independent
```

**Image Characteristics**:
- Immutable (read-only)
- Versioned with tags
- Layered architecture
- Shareable and reusable

**Container Characteristics**:
- Mutable (writeable)
- Has state (running, stopped, etc.)
- Isolated from other containers
- Disposable and recreatable

### Container Isolation

Containers provide isolation through Linux namespaces:

1. **PID Namespace**: Process isolation
2. **NET Namespace**: Network isolation
3. **MNT Namespace**: Filesystem isolation
4. **UTS Namespace**: Hostname isolation
5. **IPC Namespace**: Inter-process communication isolation
6. **USER Namespace**: User ID isolation

```powershell
# Each container thinks it's the only one running
docker run -it ubuntu bash
# Inside: ps aux
# You'll only see processes inside THIS container
```

### Container Lifecycle (Simplified)

```
      docker run
          │
          ▼
    ┌─────────┐
    │ Created │
    └────┬────┘
         │
         ▼
    ┌─────────┐   docker stop    ┌─────────┐
    │ Running │ ─────────────────▶│ Stopped │
    └────┬────┘                   └────┬────┘
         │                             │
         │ docker restart              │
         │◀────────────────────────────┘
         │
         │ exit/crash
         ▼
    ┌─────────┐   docker rm     [Deleted]
    │ Exited  │ ───────────────▶
    └─────────┘
```

## Hands-On Examples

### Example 1: Verify Architecture

```powershell
# Check Docker version and architecture
docker version

# Output shows:
# Client: Windows (your CLI)
# Server: Linux (WSL2 backend)
```

### Example 2: Understanding Client-Server

```powershell
# Client sends command
docker info

# Daemon responds with system information
# Look for "OSType: linux" - confirms WSL2 backend
```

### Example 3: Images vs Containers

```powershell
# List images (blueprints)
docker images

# You should see: node:20, traefik:v3.2, etc.

# List containers (instances)
docker ps -a

# You should see: traefik, calibre-web, etc.
# Notice: Multiple containers can use the same image!
```

### Example 4: Container Isolation

```powershell
# Run two separate Ubuntu containers
docker run -it --name ubuntu1 --rm ubuntu bash
# Inside: touch /test-file-1.txt && ls /
# Exit: exit

docker run -it --name ubuntu2 --rm ubuntu bash
# Inside: ls /
# Notice: /test-file-1.txt doesn't exist!
# Each container has isolated filesystem
```

## Understanding Your Current Setup

Let's analyze your existing containers through the architecture lens:

```powershell
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"
```

**Traefik Container**:
- **Image**: traefik:v3.2 (blueprint)
- **Container**: traefik (running instance)
- **Purpose**: Reverse proxy
- **Isolation**: Has its own network stack, sees only its processes

**Node Container (openmemory)**:
- **Image**: node:20
- **Container**: openmemory
- **Purpose**: JavaScript runtime environment
- **Isolation**: Independent from other containers

Each container:
- Based on an immutable image
- Has its own writable layer
- Isolated process space
- Independent network namespace

## Key Takeaways

1. **Docker is a containerization platform** that packages apps and dependencies together
2. **Containers are lightweight** - share host OS kernel, unlike VMs
3. **Client-Server architecture** - CLI talks to daemon via API
4. **Images are templates** - Containers are running instances
5. **WSL2 backend on Windows** - Provides native Linux compatibility
6. **Isolation without overhead** - Process-level, not hardware-level

## Knowledge Check

Answer these questions to test your understanding:

1. What's the main difference between a container and a VM?
2. What are the three main components of Docker architecture?
3. What is the relationship between an image and a container?
4. Why does Docker Desktop on Windows use WSL2?
5. Name three things that are isolated in a container.

**Answers**:
1. Containers share the host OS kernel; VMs run a full guest OS
2. Docker Client (CLI), Docker Daemon (dockerd), Docker Registry
3. Image is a template/blueprint; container is a running instance
4. WSL2 provides full Linux kernel, better performance, and compatibility
5. Process space, filesystem, network, hostname, users (any 3)

## Further Exploration

Try these commands to explore architecture:

```powershell
# See client and server details
docker version

# See system-wide information
docker info

# See what containers are using resources
docker stats --no-stream

# See Docker disk usage
docker system df
```

## Next Module

Now that you understand Docker's architecture, proceed to:
**[02_Essential_Commands.md](02_Essential_Commands.md)** - Master the CLI tools

---

**Module Complete!** ✓

**Time to Complete**: 45-60 minutes  
**Next**: [Essential CLI Commands](02_Essential_Commands.md)  
**Phase Home**: [Phase 01 README](README.md)
