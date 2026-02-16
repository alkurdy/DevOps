# Phase 02: Images & Registries

## Overview
Deep dive into Docker images - understanding layers, creating custom images with Dockerfiles, optimizing image sizes, and working with container registries.

## Learning Objectives

By the end of this phase, you will:
- Understand Docker image architecture and layers
- Create custom images using Dockerfiles
- Optimize images for size and performance
- Work with Docker Hub and other registries
- Implement multi-stage builds
- Tag and version images effectively
- Push and pull images from registries

## Duration
**4-6 hours** (including exercises)

## Prerequisites
- Completed Phase 01
- Understanding of container basics
- Familiarity with basic command-line operations

## Phase Structure

### Module 01: Understanding Docker Images
**File**: [01_Image_Architecture.md](01_Image_Architecture.md)  
**Time**: 60 minutes

Topics:
- What are Docker images?
- Image layers and the Union File System
- Layer caching and reuse
- Image manifests and metadata
- Image IDs vs Image tags
- Parent-child relationships
- Inspecting image layers with `docker history`

### Module 02: Introduction to Dockerfile
**File**: [02_Dockerfile_Basics.md](02_Dockerfile_Basics.md)  
**Time**: 90 minutes

Topics:
- Dockerfile syntax and structure
- Essential instructions: FROM, RUN, COPY, ADD, CMD, ENTRYPOINT
- WORKDIR, ENV, EXPOSE, USER
- Build context and .dockerignore
- Building images with `docker build`
- Tagging images
- Best practices for layer organization

### Module 03: Advanced Dockerfile Techniques
**File**: [03_Advanced_Dockerfile.md](03_Advanced_Dockerfile.md)  
**Time**: 90 minutes

Topics:
- Multi-stage builds
- Build arguments (ARG)
- Environment variables at build vs runtime
- HEALTHCHECK instruction
- LABEL for metadata
- VOLUME declaration
- ONBUILD instruction
- Shell vs Exec form
- Minimizing layer count

### Module 04: Image Optimization
**File**: [04_Image_Optimization.md](04_Image_Optimization.md)  
**Time**: 60 minutes

Topics:
- Reducing image size
- Choosing the right base image
- Alpine vs Debian vs Ubuntu
- Removing build dependencies
- Combining RUN commands
- .dockerignore best practices
- Analyzing image size with dive
- Security considerations

### Module 05: Working with Registries
**File**: [05_Registries.md](05_Registries.md)  
**Time**: 60 minutes

Topics:
- Docker Hub overview
- Pulling images from registries
- Pushing images to Docker Hub
- Image naming and tagging conventions
- Private registries (Azure ACR, AWS ECR, etc.)
- Authentication and credentials
- Docker Hub organizations and teams
- Setting up a local registry
- Registry best practices

## Key Commands Covered

```powershell
# Image Management
docker images                          # List images
docker image ls                        # List images (modern)
docker image inspect <image>           # Inspect image
docker history <image>                 # Show image layers
docker image rm <image>                # Remove image
docker image prune                     # Remove unused images

# Building Images
docker build -t <name:tag> .           # Build from Dockerfile
docker build -t <name:tag> -f <file> . # Build with custom Dockerfile
docker build --no-cache -t <name:tag> .# Build without cache
docker build --build-arg VAR=value .   # Pass build arguments
docker tag <image> <new-name:tag>      # Tag image

# Registry Operations
docker login                           # Login to Docker Hub
docker logout                          # Logout
docker pull <image:tag>                # Pull from registry
docker push <image:tag>                # Push to registry
docker search <term>                   # Search Docker Hub

# Image Analysis
docker history <image>                 # Layer history
docker image inspect <image>           # Detailed info
docker save <image> -o file.tar        # Export image
docker load -i file.tar                # Import image
```

## Hands-On Exercises

### Exercise 1: Create Your First Dockerfile
**File**: [Exercises/Exercise_01_First_Dockerfile.md](Exercises/Exercise_01_First_Dockerfile.md)

Create a simple web application image using a Dockerfile.

### Exercise 2: Multi-Stage Build
**File**: [Exercises/Exercise_02_MultiStage.md](Exercises/Exercise_02_MultiStage.md)

Build an optimized image using multi-stage builds.

### Exercise 3: Image Optimization Challenge
**File**: [Exercises/Exercise_03_Optimization.md](Exercises/Exercise_03_Optimization.md)

Reduce an image from 1GB to under 100MB.

### Exercise 4: Docker Hub Workflow
**File**: [Exercises/Exercise_04_Registry.md](Exercises/Exercise_04_Registry.md)

Push and pull images from Docker Hub.

### Exercise 5: Custom Base Images
**File**: [Exercises/Exercise_05_Custom_Base.md](Exercises/Exercise_05_Custom_Base.md)

Create reusable base images for your organization.

## Real-World Projects

### Project 1: Containerize Your Node.js App
Containerize the OpenMemory app (Node.js) with an optimized Dockerfile.

### Project 2: Python Application with Dependencies
Create an optimized Python image with proper dependency management.

### Project 3: Static Website Serving
Build a minimal NGINX image serving a static website.

## Assessment Checklist

Before moving to Phase 03, ensure you can:

### Conceptual Understanding
- [ ] Explain Docker image layers and caching
- [ ] Describe the difference between CMD and ENTRYPOINT
- [ ] Understand multi-stage builds benefits
- [ ] Know when to use different base images

### Practical Skills
- [ ] Write a Dockerfile from scratch
- [ ] Build images with `docker build`
- [ ] Tag images properly (name:version)
- [ ] Push images to Docker Hub
- [ ] Pull images from registries
- [ ] Inspect image layers
- [ ] Optimize image size

### Applied Knowledge
- [ ] Create multi-stage builds
- [ ] Use .dockerignore effectively
- [ ] Apply image optimization techniques
- [ ] Understand security implications
- [ ] Version images semantically

## Example Dockerfiles Included

This phase includes sample Dockerfiles for:
- Node.js applications
- Python applications
- Go applications
- Static websites (NGINX)
- Java applications
- .NET applications

## Tools & Resources

### Tools You'll Use
- **Dockerfile**: Image build instructions
- **docker build**: Build images
- **docker history**: Inspect layers
- **dive**: Analyze image layers (optional)

### Official Documentation
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Build Reference](https://docs.docker.com/engine/reference/commandline/build/)
- [Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)

### Quick References
- [Dockerfile Best Practices](../References/Dockerfile_Best_Practices.md)
- [Base Image Selection Guide](../References/Base_Image_Guide.md)
- [Common Dockerfile Patterns](../References/Dockerfile_Patterns.md)

## Image Naming Conventions

Learn and apply proper naming:

```
[registry/][username/]repository[:tag]

Examples:
myapp:latest                          # Local image
myapp:1.0.0                          # Version tag
myapp:dev                            # Environment tag
username/myapp:latest                # Docker Hub public
registry.example.com/myapp:1.0.0     # Private registry
```

## Common Pitfalls to Avoid

- ❌ Not using .dockerignore (bloated images)
- ❌ Running containers as root
- ❌ Installing unnecessary packages
- ❌ Not combining RUN commands
- ❌ Using `latest` tag in production
- ❌ Hardcoding secrets in images
- ❌ Not cleaning up in the same layer
- ❌ Copying entire build context

## Next Steps

After completing Phase 02:
1. Complete all exercises
2. Review the assessment checklist  
3. Create custom images for your projects
4. Proceed to [Phase 03: Container Lifecycle Management](../Phase_03_Container_Lifecycle/README.md)

## Navigation

- **Previous**: [Phase 01: Fundamentals & CLI](../Phase_01_Fundamentals_CLI/README.md)
- **Next**: [Phase 03: Container Lifecycle Management](../Phase_03_Container_Lifecycle/README.md)
- **Home**: [Training Path Home](../README.md)

---

**Ready to begin?** Start with [01_Image_Architecture.md](01_Image_Architecture.md)

**Last Updated**: February 16, 2026
