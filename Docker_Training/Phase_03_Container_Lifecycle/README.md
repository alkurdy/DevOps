# Phase 03: Container Lifecycle Management

## Overview
Master advanced container lifecycle operations including running containers interactively, managing logs, configuring environment variables, setting resource limits, and implementing proper restart strategies.

## Learning Objectives

By the end of this phase, you will:
- Run containers in interactive and detached modes
- Manage container logs effectively
- Execute commands in running containers
- Configure environment variables and secrets
- Set CPU and memory resource limits
- Implement health checks
- Configure restart policies for reliability
- Handle container dependencies
- Debug running containers

## Duration
**4-6 hours** (including exercises)

## Prerequisites
- Completed Phase 01 & 02
- Understanding of Docker images and containers
- Ability to create basic Dockerfiles

## Phase Structure

### Module 01: Running Containers
**File**: [01_Running_Containers.md](01_Running_Containers.md)  
**Time**: 60 minutes

Topics:
- Interactive vs detached mode
- Foreground vs background execution
- Container naming strategies
- Temporary containers with `--rm`
- stdin, stdout, stderr handling
- TTY allocation (`-it` flags)
- Attaching and detaching from containers

### Module 02: Environment Configuration
**File**: [02_Environment_Configuration.md](02_Environment_Configuration.md)  
**Time**: 60 minutes

Topics:
- Setting environment variables (`-e`, `--env`)
- Environment files (`--env-file`)
- Configuration management patterns
- Secrets management (NOT in environment vars)
- Runtime vs build-time configuration
- Overriding Dockerfile ENV
- Twelve-factor app methodology

### Module 03: Logging & Debugging
**File**: [03_Logging_Debugging.md](03_Logging_Debugging.md)  
**Time**: 90 minutes

Topics:
- Accessing container logs
- Log drivers and configuration
- Structured logging
- Log rotation and retention
- Debugging techniques with `docker exec`
- Copying files to/from containers
- Troubleshooting common issues
- Using `docker attach`
- Debugging crashed containers

### Module 04: Resource Management
**File**: [04_Resource_Management.md](04_Resource_Management.md)  
**Time**: 90 minutes

Topics:
- CPU constraints and shares
- Memory limits and reservations
- OOM (Out of Memory) handling
- Block I/O limits
- Device access
- PID limits
- Resource monitoring
- Container metrics
- Performance tuning

### Module 05: Container Dependencies & Health
**File**: [05_Dependencies_Health.md](05_Dependencies_Health.md)  
**Time**: 60 minutes

Topics:
- Dependency management
- Wait strategies
- Health checks (HEALTHCHECK)
- Readiness vs liveness
- Graceful shutdown handling
- Init processes and zombie reaping
- Using tini or dumb-init
- Signal handling

## Key Commands Covered

```powershell
# Running Containers
docker run -d <image>                  # Detached mode
docker run -it <image> bash            # Interactive
docker run --rm <image>                # Auto-remove
docker run --name <name> <image>       # Named container
docker run -e VAR=value <image>        # Environment variable
docker run --env-file .env <image>     # Environment file

# Resource Limits
docker run -m 512m <image>             # Memory limit
docker run --memory-reservation 256m   # Memory soft limit
docker run --cpus 1.5 <image>          # CPU limit
docker run --cpu-shares 512            # CPU shares
docker run --pids-limit 100            # PID limit

# Executing Commands
docker exec <container> <command>      # Execute command
docker exec -it <container> bash       # Interactive shell
docker exec -u root <container> cmd    # As different user
docker exec -w /app <container> ls     # With working directory

# Debugging
docker logs <container>                # View logs
docker logs -f <container>             # Follow logs
docker attach <container>              # Attach to container
docker cp <container>:/path .          # Copy from container
docker cp file <container>:/path       # Copy to container

# Monitoring
docker stats                           # Resource usage
docker top <container>                 # Container processes
docker port <container>                # Port mappings
docker inspect <container>             # Full details
```

## Hands-On Exercises

### Exercise 1: Interactive Container Management
**File**: [Exercises/Exercise_01_Interactive.md](Exercises/Exercise_01_Interactive.md)

Practice running containers in different modes.

### Exercise 2: Environment Configuration
**File**: [Exercises/Exercise_02_Environment.md](Exercises/Exercise_02_Environment.md)

Configure applications using environment variables and files.

### Exercise 3: Resource Limits Testing
**File**: [Exercises/Exercise_03_Resources.md](Exercises/Exercise_03_Resources.md)

Set and test memory and CPU limits.

### Exercise 4: Log Management
**File**: [Exercises/Exercise_04_Logging.md](Exercises/Exercise_04_Logging.md)

Configure different log drivers and analyze logs.

### Exercise 5: Health Checks Implementation
**File**: [Exercises/Exercise_05_HealthChecks.md](Exercises/Exercise_05_HealthChecks.md)

Implement and test container health checks.

## Real-World Scenarios

### Scenario 1: Database Container
Configure and run a PostgreSQL container with:
- Persistent storage
- Environment-based configuration
- Memory limits
- Health checks
- Proper restart policy

### Scenario 2: Web Application
Run a web application with:
- Environment variables
- Log management
- Resource constraints
- Health endpoints
- Graceful shutdown

### Scenario 3: Batch Processing
Run a data processing container:
- One-time execution
- Auto-removal
- Resource limits
- Output capture
- Error handling

## Assessment Checklist

Before moving to Phase 04, ensure you can:

### Conceptual Understanding
- [ ] Explain interactive vs detached mode
- [ ] Understand environment variable precedence
- [ ] Describe resource constraint mechanisms
- [ ] Know when to use health checks
- [ ] Understand graceful shutdown

### Practical Skills
- [ ] Run containers in various modes
- [ ] Configure environment variables
- [ ] Set resource limits
- [ ] Access and analyze logs
- [ ] Execute commands in running containers
- [ ] Copy files to/from containers
- [ ] Implement health checks
- [ ] Debug container issues

### Applied Knowledge
- [ ] Configure production containers properly
- [ ] Implement proper logging strategies
- [ ] Set appropriate resource limits
- [ ] Handle container dependencies
- [ ] Troubleshoot common issues

## Common Patterns

### Pattern 1: Configuration Management
```powershell
# Use environment files for configuration
docker run --env-file config.env myapp
```

### Pattern 2: Resource-Constrained Services
```powershell
# Limit resources for specific workloads
docker run -m 512m --cpus 1 myapp
```

### Pattern 3: One-Shot Tasks
```powershell
# Run and auto-remove
docker run --rm myapp process-data
```

### Pattern 4: Debugging Running Containers
```powershell
# Access shell in running container
docker exec -it myapp bash
```

## Tools & Resources

### Tools You'll Use
- **docker run**: Start containers
- **docker exec**: Execute in containers
- **docker logs**: View logs
- **docker stats**: Monitor resources
- **docker inspect**: Detailed information

### Official Documentation
- [Docker Run Reference](https://docs.docker.com/engine/reference/run/)
- [Environment Variables](https://docs.docker.com/engine/reference/commandline/run/#env)
- [Resource Constraints](https://docs.docker.com/config/containers/resource_constraints/)
- [Logging Drivers](https://docs.docker.com/config/containers/logging/)

### Quick References
- [Run Flags Cheat Sheet](../References/Run_Flags_Cheatsheet.md)
- [Environment Variables Guide](../References/Environment_Variables_Guide.md)
- [Resource Limits Guide](../References/Resource_Limits_Guide.md)

## Common Issues & Solutions

### Issue 1: Container Exits Immediately
**Problem**: Container starts then exits  
**Solution**: Check if process runs in foreground, check logs

### Issue 2: Out of Memory
**Problem**: Container killed due to OOM  
**Solution**: Increase memory limit or optimize application

### Issue 3: Configuration Not Applied
**Problem**: Environment variables not working  
**Solution**: Check variable names, precedence, and format

### Issue 4: Cannot Access Logs
**Problem**: Logs not visible  
**Solution**: Check log driver configuration, ensure app logs to stdout/stderr

## Next Steps

After completing Phase 03:
1. Complete all exercises
2. Review the assessment checklist
3. Practice with your existing containers
4. Proceed to [Phase 04: Networking & Storage](../Phase_04_Networking_Storage/README.md)

## Navigation

- **Previous**: [Phase 02: Images & Registries](../Phase_02_Images_Registries/README.md)
- **Next**: [Phase 04: Networking & Storage](../Phase_04_Networking_Storage/README.md)
- **Home**: [Training Path Home](../README.md)

---

**Ready to begin?** Start with [01_Running_Containers.md](01_Running_Containers.md)

**Last Updated**: February 16, 2026
