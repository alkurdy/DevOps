# Phase 05: Docker Compose

## Overview
Master Docker Compose for defining and running multi-container applications. Learn YAML syntax, service orchestration, and how to recreate your current stack as infrastructure-as-code.

## Learning Objectives

By the end of this phase, you will:
- Understand Docker Compose architecture and purpose
- Write docker-compose.yml files
- Define services, networks, and volumes in YAML
- Use environment variables and .env files
- Orchestrate multi-container applications
- Use Docker Compose CLI commands
- Implement service dependencies
- Scale services
- Override configurations for different environments
- Convert your current container setup to Compose

## Duration
**5-7 hours** (including exercises)

## Prerequisites
- Completed Phases 01-04
- Understanding of networking and volumes
- Basic YAML syntax knowledge (will be taught)

## Phase Structure

### Module 01: Docker Compose Fundamentals
**File**: [01_Compose_Fundamentals.md](01_Compose_Fundamentals.md)  
**Time**: 60 minutes

Topics:
- What is Docker Compose?
- Compose vs docker run
- docker-compose.yml structure
- Compose file versions (v3.x)
- Installing Compose (included with Docker Desktop)
- Basic Compose workflow
- Compose vs Kubernetes/Swarm
- When to use Compose

### Module 02: YAML Syntax & Structure
**File**: [02_YAML_Syntax.md](02_YAML_Syntax.md)  
**Time**: 45 minutes

Topics:
- YAML basics (indentation, data types)
- Key-value pairs
- Lists and nested structures
- Multi-line strings
- Comments
- Anchors and aliases
- YAML validation
- Common YAML mistakes

### Module 03: Defining Services
**File**: [03_Defining_Services.md](03_Defining_Services.md)  
**Time**: 90 minutes

Topics:
- Service definition structure
- Image vs build
- Container naming
- Port mapping in Compose
- Environment variables
- Command and entrypoint overrides
- Working directory
- User specification
- Labels and metadata
- Restart policies

### Module 04: Networks & Volumes in Compose
**File**: [04_Networks_Volumes.md](04_Networks_Volumes.md)  
**Time**: 90 minutes

Topics:
- Defining networks in Compose
- Network drivers in Compose
- Service networking and aliases
- Volume definitions
- Volume mounting
- Volume drivers
- External networks and volumes
- Network and volume configuration
- Custom network settings

### Module 05: Docker Compose CLI
**File**: [05_Compose_CLI.md](05_Compose_CLI.md)  
**Time**: 60 minutes

Topics:
- docker compose up/down
- docker compose start/stop/restart
- docker compose ps/logs
- docker compose exec/run
- docker compose build/pull
- docker compose config (validation)
- docker compose scale
- docker compose top/port
- Working with multiple Compose files
- Override files (docker-compose.override.yml)

### Module 06: Advanced Compose Features
**File**: [06_Advanced_Compose.md](06_Advanced_Compose.md)  
**Time**: 90 minutes

Topics:
- Service dependencies (depends_on)
- Health checks in Compose
- Resource limits
- Build arguments
- Multi-stage builds in Compose
- Extends and includes
- Profiles for different environments
- Variable substitution
- .env files and environment
- Secrets management basics

### Module 07: Production Patterns
**File**: [07_Production_Patterns.md](07_Production_Patterns.md)  
**Time**: 60 minutes

Topics:
- Development vs production configurations
- Environment-specific overrides
- Logging configuration
- Security considerations
- Using Compose in CI/CD
- Deployment strategies
- Monitoring and healthchecks
- Backup and recovery
- Migration strategies

## Key Commands Covered

```powershell
# Project Management
docker compose up                      # Start all services
docker compose up -d                   # Start in detached mode
docker compose down                    # Stop and remove containers
docker compose down -v                 # Also remove volumes
docker compose restart                 # Restart services

# Service Management
docker compose start                   # Start stopped services
docker compose stop                    # Stop services
docker compose pause                   # Pause services
docker compose unpause                 # Unpause services
docker compose kill                    # Kill services

# Viewing & Monitoring
docker compose ps                      # List containers
docker compose logs                    # View logs
docker compose logs -f                 # Follow logs
docker compose logs <service>          # Logs for specific service
docker compose top                     # View processes
docker compose events                  # View events

# Execution
docker compose exec <service> <cmd>    # Execute in running service
docker compose run <service> <cmd>     # Run one-off command
docker compose run --rm <service>      # Run and remove

# Building & Images
docker compose build                   # Build/rebuild services
docker compose build --no-cache        # Build without cache
docker compose pull                    # Pull service images
docker compose push                    # Push service images

# Utilities
docker compose config                  # Validate and view config
docker compose config --services       # List services
docker compose config --volumes        # List volumes
docker compose version                 # Show version
docker compose port <service> <port>   # Show public port

# Scaling
docker compose up -d --scale web=3     # Scale service to 3 instances
```

## Hands-On Exercises

### Exercise 1: First Compose File
**File**: [Exercises/Exercise_01_First_Compose.md](Exercises/Exercise_01_First_Compose.md)

Create your first docker-compose.yml with a simple web application.

### Exercise 2: Multi-Service Application
**File**: [Exercises/Exercise_02_Multi_Service.md](Exercises/Exercise_02_Multi_Service.md)

Build a frontend + backend + database stack.

### Exercise 3: Recreate Your Current Stack
**File**: [Exercises/Exercise_03_Current_Stack.md](Exercises/Exercise_03_Current_Stack.md)

Convert your Traefik, Calibre-web, and other containers to Compose.

### Exercise 4: Environment Management
**File**: [Exercises/Exercise_04_Environments.md](Exercises/Exercise_04_Environments.md)

Implement dev, staging, and production configurations.

### Exercise 5: Service Dependencies
**File**: [Exercises/Exercise_05_Dependencies.md](Exercises/Exercise_05_Dependencies.md)

Implement proper service startup ordering and health checks.

## Real-World Projects

### Project 1: WordPress Stack
Complete WordPress deployment:
```yaml
services:
  wordpress:
    image: wordpress:latest
    depends_on:
      - db
    # ... configuration
  db:
    image: mysql:8
    # ... configuration
```

### Project 2: Your Current Infrastructure
Recreate your complete setup as Compose:
- Traefik reverse proxy
- LazyLibrarian
- Calibre-web
- OpenMemory (Node.js)
- AdGuard Home
- All networks and volumes

### Project 3: Development Environment
Full development stack:
- Web application with hot-reload
- Database
- Redis cache
- Development tools

## Sample docker-compose.yml

### Basic Example
```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html
    restart: unless-stopped

  app:
    build: ./app
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    networks:
      - backend

  db:
    image: postgres:15
    volumes:
      - db-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=secretpassword
    networks:
      - backend

networks:
  backend:
    driver: bridge

volumes:
  db-data:
```

### Your Stack Template
```yaml
version: '3.8'

services:
  traefik:
    image: traefik:v3.2
    ports:
      - "192.168.12.210:80:80"
      - "192.168.12.210:443:443"
      - "192.168.12.210:8080:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - traefik-config:/etc/traefik
    restart: unless-stopped

  calibre-web:
    image: lscr.io/linuxserver/calibre-web:latest
    depends_on:
      - traefik
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/New_York
    volumes:
      - calibre-config:/config
      - calibre-books:/books
    restart: unless-stopped

  # ... more services

volumes:
  traefik-config:
  calibre-config:
  calibre-books:
```

## Assessment Checklist

Before moving to Phase 06, ensure you can:

### Conceptual Understanding
- [ ] Explain Docker Compose purpose and benefits
- [ ] Understand Compose file structure
- [ ] Know when to use Compose vs docker run
- [ ] Understand service dependencies
- [ ] Know environment variable precedence

### Practical Skills
- [ ] Write valid docker-compose.yml files
- [ ] Define services, networks, and volumes
- [ ] Use docker compose up/down
- [ ] View and follow logs
- [ ] Execute commands in services
- [ ] Build images with Compose
- [ ] Use environment files
- [ ] Validate Compose files

### Applied Knowledge
- [ ] Design multi-container applications
- [ ] Implement service dependencies
- [ ] Create environment-specific configs
- [ ] Convert docker run to Compose
- [ ] Manage application lifecycle
- [ ] Troubleshoot Compose issues

## Benefits of Converting to Compose

Your current setup uses individual `docker run` commands. Converting to Compose provides:

✅ **Infrastructure as Code**: Everything defined in version-controlled files  
✅ **Repeatability**: Recreate entire stack with one command  
✅ **Team Collaboration**: Share configurations easily  
✅ **Environment Management**: Dev/staging/prod configurations  
✅ **Service Dependencies**: Automatic startup ordering  
✅ **Network Management**: Automatic network creation  
✅ **Volume Management**: Centralized volume definitions  
✅ **Documentation**: Self-documenting infrastructure  

## Compose File Best Practices

1. **Use version 3.8 or later**
2. **Name your project** (directory name or -p flag)
3. **Use named volumes** instead of anonymous
4. **Specify restart policies**
5. **Use .env for sensitive data**
6. **Don't commit .env** (use .env.example)
7. **Use healthchecks** for dependencies
8. **Organize by concern** (frontend/backend/data)
9. **Comment complex configurations**
10. **Validate before deploying** (`docker compose config`)

## Common Patterns

### Pattern 1: Web App + Database
```yaml
services:
  app:
    build: .
    depends_on:
      - db
  db:
    image: postgres
    volumes:
      - db-data:/var/lib/postgresql/data
```

### Pattern 2: Reverse Proxy + Services
```yaml
services:
  proxy:
    image: traefik
    ports:
      - "80:80"
  app1:
    image: myapp1
  app2:
    image: myapp2
```

### Pattern 3: Development with Overrides
```yaml
# docker-compose.yml (base)
services:
  app:
    image: myapp

# docker-compose.override.yml (dev)
services:
  app:
    build: .
    volumes:
      - ./src:/app/src
```

## Tools & Resources

### Tools You'll Use
- **docker compose**: Main CLI tool
- **yamllint**: YAML validation
- **docker-compose-viz**: Visualize configs
- **dive**: Image inspection

### Official Documentation
- [Compose Specification](https://docs.docker.com/compose/compose-file/)
- [Compose CLI](https://docs.docker.com/compose/reference/)
- [Environment Variables](https://docs.docker.com/compose/environment-variables/)
- [Networking in Compose](https://docs.docker.com/compose/networking/)

### Quick References
- [Compose File Reference](../References/Compose_File_Reference.md)
- [Compose CLI Cheatsheet](../References/Compose_CLI_Cheatsheet.md)
- [Environment Variables Guide](../References/Compose_Environment.md)

## Migration Strategy

### From docker run to Compose:

1. **Document current setup**: `docker ps`, `docker inspect`
2. **Create docker-compose.yml**: Define services
3. **Test in parallel**: Don't remove old containers yet
4. **Validate**: `docker compose config`
5. **Deploy**: `docker compose up -d`
6. **Verify**: `docker compose ps`, check logs
7. **Clean up**: Remove old containers

## Next Steps

After completing Phase 05:
1. Complete all exercises
2. Create Compose file for your infrastructure
3. Test and validate configurations
4. Proceed to [Phase 06: Advanced Topics](../Phase_06_Advanced_Topics/README.md)

## Navigation

- **Previous**: [Phase 04: Networking & Storage](../Phase_04_Networking_Storage/README.md)
- **Next**: [Phase 06: Advanced Topics](../Phase_06_Advanced_Topics/README.md)
- **Home**: [Training Path Home](../README.md)

---

**Ready to begin?** Start with [01_Compose_Fundamentals.md](01_Compose_Fundamentals.md)

**Last Updated**: February 16, 2026
