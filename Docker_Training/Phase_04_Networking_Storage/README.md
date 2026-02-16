# Phase 04: Networking & Storage

## Overview
Master Docker networking modes, create custom networks, understand container communication, and implement persistent storage with volumes and bind mounts.

## Learning Objectives

By the end of this phase, you will:
- Understand Docker networking architecture
- Work with different network drivers (bridge, host, overlay)
- Create and manage custom networks
- Configure container-to-container communication
- Implement port mapping and exposure
- Work with Docker volumes for persistent storage
- Use bind mounts effectively
- Backup and restore volume data
- Understand storage drivers
- Implement data persistence strategies

## Duration
**5-7 hours** (including exercises)

## Prerequisites
- Completed Phases 01-03
- Understanding of container lifecycle
- Basic networking concepts (IP, ports, DNS)

## Phase Structure

### Module 01: Docker Networking Fundamentals
**File**: [01_Networking_Fundamentals.md](01_Networking_Fundamentals.md)  
**Time**: 90 minutes

Topics:
- Docker networking architecture
- Network drivers overview (bridge, host, none, overlay)
- Default bridge network
- DNS and service discovery
- Network namespaces and isolation
- Container Network Interface (CNI)
- IPv4 and IPv6 support
- Network inspection

### Module 02: Network Types & Configuration
**File**: [02_Network_Types.md](02_Network_Types.md)  
**Time**: 90 minutes

Topics:
- Bridge networks (default and custom)
- Host networking mode
- None network (network isolation)
- Overlay networks (Swarm)
- Macvlan networks
- Creating custom networks
- Network configuration options
- Network aliases
- Connecting containers to multiple networks

### Module 03: Port Mapping & Exposure
**File**: [03_Ports_Exposure.md](03_Ports_Exposure.md)  
**Time**: 60 minutes

Topics:
- EXPOSE instruction vs -p flag
- Publishing ports (-p, --publish)
- Publishing all ports (-P)
- Port mapping syntax
- Binding to specific IP addresses
- Port conflicts and resolution
- Dynamic port allocation
- Understanding your Traefik setup

### Module 04: Container Communication
**File**: [04_Container_Communication.md](04_Container_Communication.md)  
**Time**: 90 minutes

Topics:
- Container-to-container communication
- Service discovery with DNS
- Network aliases and link aliasing
- Legacy links (deprecated)
- Communication across networks
- Network security and isolation
- Connecting to host services
- External network access

### Module 05: Storage Fundamentals
**File**: [05_Storage_Fundamentals.md](05_Storage_Fundamentals.md)  
**Time**: 60 minutes

Topics:
- Container filesystem layers
- Writable layer
- Storage drivers
- Data persistence challenges
- Volumes vs bind mounts vs tmpfs
- Volume drivers and plugins
- Storage on Windows vs Linux
- Performance considerations

### Module 06: Working with Volumes
**File**: [06_Volumes.md](06_Volumes.md)  
**Time**: 90 minutes

Topics:
- Creating and managing volumes
- Named volumes vs anonymous volumes
- Sharing volumes between containers
- Volume mounting options
- Volume drivers
- Volume backups and restoration
- Volume migration
- Inspecting volume data
- Cleaning up unused volumes

### Module 07: Bind Mounts & tmpfs
**File**: [07_BindMounts_tmpfs.md](07_BindMounts_tmpfs.md)  
**Time**: 60 minutes

Topics:
- Bind mount use cases
- Bind mount syntax
- Read-only bind mounts
- Bind mount limitations
- tmpfs mounts for sensitive data
- Performance comparisons
- Development vs production usage
- Windows path considerations

## Key Commands Covered

```powershell
# Network Management
docker network ls                      # List networks
docker network create <name>           # Create network
docker network inspect <network>       # Inspect network
docker network connect <net> <cont>    # Connect container
docker network disconnect <net> <cont> # Disconnect container
docker network rm <network>            # Remove network
docker network prune                   # Remove unused networks

# Running with Networks
docker run --network <network> <image> # Use specific network
docker run --network host <image>      # Use host networking
docker run --network none <image>      # No networking
docker run --add-host name:ip <image>  # Add custom host entry

# Port Mapping
docker run -p 8080:80 <image>          # Map host:container port
docker run -p 127.0.0.1:8080:80 <img>  # Bind to specific IP
docker run -P <image>                  # Publish all exposed ports
docker port <container>                # Show port mappings

# Volume Management
docker volume ls                       # List volumes
docker volume create <name>            # Create volume
docker volume inspect <volume>         # Inspect volume
docker volume rm <volume>              # Remove volume
docker volume prune                    # Remove unused volumes

# Running with Volumes
docker run -v <volume>:/path <image>   # Named volume
docker run -v /host:/container <image> # Bind mount
docker run --mount type=volume,src=vol,dst=/path <image>
docker run --mount type=bind,src=/host,dst=/cont <image>
docker run --tmpfs /path <image>       # tmpfs mount
docker run -v /path:ro <image>         # Read-only

# Backup & Restore
docker run --rm -v vol:/data -v $(pwd):/backup ubuntu tar -czf /backup/backup.tar.gz /data
docker run --rm -v vol:/data -v $(pwd):/backup ubuntu tar -xzf /backup/backup.tar.gz -C /
```

## Hands-On Exercises

### Exercise 1: Network Exploration
**File**: [Exercises/Exercise_01_Networks.md](Exercises/Exercise_01_Networks.md)

Analyze your current network setup (Traefik, etc.).

### Exercise 2: Custom Network Creation
**File**: [Exercises/Exercise_02_Custom_Networks.md](Exercises/Exercise_02_Custom_Networks.md)

Create custom networks and connect containers.

### Exercise 3: Multi-Container Communication
**File**: [Exercises/Exercise_03_Communication.md](Exercises/Exercise_03_Communication.md)

Set up frontend-backend container communication.

### Exercise 4: Volume Management
**File**: [Exercises/Exercise_04_Volumes.md](Exercises/Exercise_04_Volumes.md)

Create and manage persistent volumes.

### Exercise 5: Database with Persistent Storage
**File**: [Exercises/Exercise_05_Database.md](Exercises/Exercise_05_Database.md)

Run PostgreSQL with persistent data.

### Exercise 6: Volume Backup & Restore
**File**: [Exercises/Exercise_06_Backup.md](Exercises/Exercise_06_Backup.md)

Backup and restore volume data.

## Real-World Projects

### Project 1: Multi-Tier Application
Deploy a three-tier application:
- Frontend (NGINX)
- Backend (Node.js/Python)
- Database (PostgreSQL/MySQL)
All connected via custom network with persistent storage.

### Project 2: Reverse Proxy Setup
Replicate your Traefik setup:
- Custom network
- Multiple backend services
- Port mapping
- Service discovery

### Project 3: Development Environment
Create a development environment with:
- Bind mounts for live code reloading
- Volume for dependencies
- Custom network for services
- Database with persistence

## Analysis of Your Current Setup

### Your Network Configuration
```powershell
# Analyze your Traefik network setup
docker network ls
docker network inspect bridge
docker inspect --format='{{range $k, $v := .NetworkSettings.Networks}}{{$k}}: {{.IPAddress}}{{end}}' traefik
```

### Your Volume Usage
```powershell
# Check which containers use volumes
docker ps --format '{{.Names}}' | ForEach-Object {
    Write-Host "$_:"
    docker inspect --format='{{range .Mounts}}  {{.Type}}: {{.Source}} -> {{.Destination}}{{end}}' $_
}
```

## Assessment Checklist

Before moving to Phase 05, ensure you can:

### Conceptual Understanding
- [ ] Explain Docker network drivers
- [ ] Understand container DNS resolution
- [ ] Describe volumes vs bind mounts
- [ ] Know when to use each storage type
- [ ] Understand network isolation

### Practical Skills
- [ ] Create custom networks
- [ ] Connect containers to networks
- [ ] Configure port mappings
- [ ] Create and manage volumes
- [ ] Use bind mounts for development
- [ ] Backup and restore volumes
- [ ] Inspect network configurations
- [ ] Troubleshoot connectivity issues

### Applied Knowledge
- [ ] Design multi-container network topologies
- [ ] Implement service discovery
- [ ] Choose appropriate storage solutions
- [ ] Secure container communications
- [ ] Optimize storage performance

## Common Networking Patterns

### Pattern 1: Frontend-Backend Isolation
```powershell
# Create networks for different tiers
docker network create frontend
docker network create backend

# Frontend connects to both
docker run --network frontend nginx
docker run --network frontend --network backend api
docker run --network backend postgres
```

### Pattern 2: Shared Database
```powershell
# Create data network
docker network create data-network

# All services connect to it
docker run --network data-network app1
docker run --network data-network app2
docker run --network data-network postgres
```

## Common Storage Patterns

### Pattern 1: Named Volumes for Databases
```powershell
docker volume create postgres-data
docker run -v postgres-data:/var/lib/postgresql/data postgres
```

### Pattern 2: Bind Mounts for Development
```powershell
docker run -v ${PWD}/src:/app/src nodejs-app
```

### Pattern 3: Anonymous Volumes for Cache
```powershell
docker run -v /app/node_modules nodejs-app
```

## Tools & Resources

### Tools You'll Use
- **docker network**: Network management
- **docker volume**: Volume management
- **docker inspect**: Detailed configuration
- **tcpdump**: Network traffic analysis
- **nc (netcat)**: Connection testing

### Official Documentation
- [Docker Networking](https://docs.docker.com/network/)
- [Docker Volumes](https://docs.docker.com/storage/volumes/)
- [Bind Mounts](https://docs.docker.com/storage/bind-mounts/)
- [Storage Drivers](https://docs.docker.com/storage/storagedriver/)

### Quick References
- [Network Drivers Comparison](../References/Network_Drivers.md)
- [Storage Options Comparison](../References/Storage_Options.md)
- [Port Mapping Guide](../References/Port_Mapping_Guide.md)

## Troubleshooting Guide

### Network Issues
- Cannot connect between containers
- DNS resolution failures
- Port conflicts
- Network not found

### Storage Issues
- Permission denied
- Volume not persisting
- Disk space issues
- Slow I/O performance

## Next Steps

After completing Phase 04:
1. Complete all exercises
2. Review the assessment checklist
3. Analyze your current containers' networking and storage
4. Proceed to [Phase 05: Docker Compose](../Phase_05_Docker_Compose/README.md)

## Navigation

- **Previous**: [Phase 03: Container Lifecycle](../Phase_03_Container_Lifecycle/README.md)
- **Next**: [Phase 05: Docker Compose](../Phase_05_Docker_Compose/README.md)
- **Home**: [Training Path Home](../README.md)

---

**Ready to begin?** Start with [01_Networking_Fundamentals.md](01_Networking_Fundamentals.md)

**Last Updated**: February 16, 2026
