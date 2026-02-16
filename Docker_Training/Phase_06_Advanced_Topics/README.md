# Phase 06: Advanced Topics & Best Practices

## Overview
Explore advanced Docker topics including security, optimization, monitoring, CI/CD integration, troubleshooting, and Windows-specific considerations.

## Learning Objectives

By the end of this phase, you will:
- Implement Docker security best practices
- Optimize images and containers for production
- Set up monitoring and logging solutions
- Integrate Docker into CI/CD pipelines
- Troubleshoot complex Docker issues
- Understand Windows containers vs Linux containers
- Implement backup and disaster recovery
- Apply DevOps best practices
- Work with Docker in production environments
- Plan scaling and orchestration strategies

## Duration
**6-8 hours** (including exercises)

## Prerequisites
- Completed Phases 01-05
- Understanding of all core Docker concepts
- Familiarity with Docker Compose

## Phase Structure

### Module 01: Security Best Practices
**File**: [01_Security.md](01_Security.md)  
**Time**: 90 minutes

Topics:
- Security principles for containers
- Running as non-root user
- Image vulnerability scanning
- Secrets management (not in ENV vars)
- Docker Content Trust
- Limiting container capabilities
- AppArmor and SELinux profiles
- Read-only filesystems
- Security scanning tools
- Network security

### Module 02: Image Optimization
**File**: [02_Image_Optimization.md](02_Image_Optimization.md)  
**Time**: 90 minutes

Topics:
- Advanced multi-stage builds
- Layer optimization techniques
- Choosing minimal base images
- Distroless images
- Scratch images for Go
- Cache optimization strategies
- BuildKit features
- Image signing and verification
- Automated optimization tools
- Analyzing with dive

### Module 03: Monitoring & Logging
**File**: [03_Monitoring_Logging.md](03_Monitoring_Logging.md)  
**Time**: 90 minutes

Topics:
- Container monitoring strategies
- Prometheus and Grafana integration
- ELK/EFK stack for logging
- Centralized logging
- Application performance monitoring
- Health checks and readiness probes
- Alerting and notifications
- Log aggregation
- Metrics collection
- Resource monitoring

### Module 04: Docker on Windows
**File**: [04_Docker_Windows.md](04_Docker_Windows.md)  
**Time**: 60 minutes

Topics:
- WSL2 architecture deep dive
- Linux containers on Windows
- Windows containers overview
- When to use Windows containers
- File system performance on Windows
- Path handling (Windows vs Linux)
- Docker Desktop configuration
- WSL2 resource management
- Troubleshooting Windows-specific issues
- Development on Windows

### Module 05: CI/CD Integration
**File**: [05_CICD_Integration.md](05_CICD_Integration.md)  
**Time**: 90 minutes

Topics:
- Docker in CI/CD pipelines
- Building images in CI
- Testing containers
- Automated security scanning
- Multi-arch builds
- Image tagging strategies
- Registry integration
- Deployment automation
- GitHub Actions with Docker
- GitLab CI/Docker

### Module 06: Troubleshooting & Debugging
**File**: [06_Troubleshooting.md](06_Troubleshooting.md)  
**Time**: 90 minutes

Topics:
- Systematic troubleshooting approach
- Common Docker errors and solutions
- Network troubleshooting
- Volume and storage issues
- Performance problems
- Memory leaks and resource exhaustion
- Build failures
- Debugging techniques
- Using docker debug
- System resources and limits

### Module 07: Backup & Disaster Recovery
**File**: [07_Backup_Recovery.md](07_Backup_Recovery.md)  
**Time**: 60 minutes

Topics:
- Volume backup strategies
- Container backup and restoration
- Database backup in containers
- Disaster recovery planning
- Automated backups
- Backup testing and validation
- Migration strategies
- Container state preservation
- Registry backup

### Module 08: Production Best Practices
**File**: [08_Production_Best_Practices.md](08_Production_Best_Practices.md)  
**Time**: 90 minutes

Topics:
- Production deployment checklist
- High availability patterns
- Rolling updates and rollbacks
- Zero-downtime deployments
- Resource allocation
- Scaling strategies
- Introduction to orchestration (Swarm, Kubernetes)
- When to use orchestration
- Monitoring and maintenance
- Documentation practices

## Key Topics Covered

### Security Hardening
```dockerfile
# Non-root user
FROM node:20-alpine
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
USER nodejs

# Read-only root filesystem
docker run --read-only --tmpfs /tmp myapp

# Drop capabilities
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE myapp

# Security scanning
docker scout cves myapp:latest
```

### Advanced Build Techniques
```dockerfile
# Multi-stage with BuildKit
# syntax=docker/dockerfile:1
FROM --platform=$BUILDPLATFORM golang:1.21 AS builder
ARG TARGETOS TARGETARCH
RUN GOOS=$TARGETOS GOARCH=$TARGETARCH go build -o app

FROM gcr.io/distroless/base
COPY --from=builder /app /
CMD ["/app"]
```

### Health Monitoring
```yaml
services:
  app:
    image: myapp
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## Hands-On Exercises

### Exercise 1: Security Audit
**File**: [Exercises/Exercise_01_Security_Audit.md](Exercises/Exercise_01_Security_Audit.md)

Audit your containers for security issues and fix them.

### Exercise 2: Image Optimization Challenge
**File**: [Exercises/Exercise_02_Optimization.md](Exercises/Exercise_02_Optimization.md)

Reduce an image from 500MB to under 50MB.

### Exercise 3: Monitoring Stack
**File**: [Exercises/Exercise_03_Monitoring.md](Exercises/Exercise_03_Monitoring.md)

Set up Prometheus + Grafana for container monitoring.

### Exercise 4: CI/CD Pipeline
**File**: [Exercises/Exercise_04_CICD.md](Exercises/Exercise_04_CICD.md)

Create a GitHub Actions workflow for Docker builds.

### Exercise 5: Troubleshooting Scenarios
**File**: [Exercises/Exercise_05_Troubleshooting.md](Exercises/Exercise_05_Troubleshooting.md)

Debug various broken container scenarios.

### Exercise 6: Backup & Restore
**File**: [Exercises/Exercise_06_Backup.md](Exercises/Exercise_06_Backup.md)

Implement automated backup solution.

## Real-World Projects

### Project 1: Production-Ready Application
Take an application through:
- Security hardening
- Image optimization
- Monitoring setup
- Automated backups
- CI/CD pipeline
- Documentation

### Project 2: Your Infrastructure Hardening
Apply best practices to your current stack:
- Security audit
- Resource optimization
- Monitoring implementation
- Backup automation
- Documentation

### Project 3: Complete DevOps Pipeline
Build end-to-end:
- Code commit triggers build
- Automated testing in containers
- Security scanning
- Image deployment
- Health monitoring
- Automated rollback

## Assessment Checklist

Before completing the training, ensure you can:

### Security
- [ ] Run containers as non-root
- [ ] Scan images for vulnerabilities
- [ ] Implement secrets management
- [ ] Apply security best practices
- [ ] Understand security implications

### Optimization
- [ ] Build minimal images
- [ ] Use multi-stage builds effectively
- [ ] Optimize layer caching
- [ ] Analyze image layers
- [ ] Choose appropriate base images

### Operations
- [ ] Set up monitoring and alerting
- [ ] Implement centralized logging
- [ ] Create backup strategies
- [ ] Troubleshoot systematically
- [ ] Document configurations

### DevOps
- [ ] Integrate Docker in CI/CD
- [ ] Automate builds and deployments
- [ ] Implement testing strategies
- [ ] Tag and version properly
- [ ] Manage environments

### Production Readiness
- [ ] Deploy production-ready containers
- [ ] Implement health checks
- [ ] Set appropriate resource limits
- [ ] Plan for high availability
- [ ] Create disaster recovery plans

## Tools & Resources

### Security Tools
- **Docker Scout**: Vulnerability scanning
- **Trivy**: Container security scanner
- **Snyk**: Security and license scanning
- **Clair**: Static analysis

### Monitoring Tools
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **cAdvisor**: Container advisor
- **Portainer**: Container management UI

### Build Tools
- **BuildKit**: Advanced build engine
- **dive**: Image layer analysis
- **hadolint**: Dockerfile linter
- **docker-slim**: Image optimization

### Official Documentation
- [Docker Security](https://docs.docker.com/engine/security/)
- [Production Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Docker BuildKit](https://docs.docker.com/build/buildkit/)

### Quick References
- [Security Checklist](../References/Security_Checklist.md)
- [Optimization Guide](../References/Optimization_Guide.md)
- [Troubleshooting Guide](../References/Troubleshooting_Guide.md)
- [Production Checklist](../References/Production_Checklist.md)

## Windows-Specific Considerations

### WSL2 Configuration
```powershell
# Configure WSL2 resources
# Create/edit: C:\Users\<username>\.wslconfig
[wsl2]
memory=8GB
processors=4
swap=2GB
```

### Path Handling
```powershell
# Windows paths in Compose
volumes:
  - C:\Users\alkur\data:/data        # Absolute path
  - ./data:/data                      # Relative path (recommended)

# PowerShell variables
docker run -v ${PWD}/data:/data myapp
```

### Performance Optimization
```powershell
# Keep files in WSL2 filesystem for best performance
cd \\wsl$\docker-desktop\
# Not in /mnt/c/ (Windows filesystem)
```

## Production Deployment Checklist

Before deploying to production:

### Configuration
- [ ] Environment variables configured
- [ ] Secrets properly managed
- [ ] Resource limits set
- [ ] Health checks implemented
- [ ] Restart policies configured

### Security
- [ ] Running as non-root
- [ ] Images scanned for vulnerabilities
- [ ] Minimal attack surface
- [ ] Network policies configured
- [ ] Logging enabled

### Reliability
- [ ] High availability considered
- [ ] Backup strategy implemented
- [ ] Monitoring and alerting configured
- [ ] Disaster recovery tested
- [ ] Documentation complete

### Performance
- [ ] Images optimized
- [ ] Caching configured
- [ ] Resource allocation tuned
- [ ] Networking optimized
- [ ] Storage performance validated

## Beyond Docker: Next Steps

After mastering Docker, consider:

### Container Orchestration
- **Docker Swarm**: Simple orchestration
- **Kubernetes**: Enterprise orchestration
- **Amazon ECS/EKS**: AWS container services
- **Azure Container Instances/AKS**: Azure solutions

### Service Mesh
- **Istio**: Traffic management
- **Linkerd**: Simple service mesh
- **Consul**: Service discovery and mesh

### Advanced Topics
- **GitOps**: Git-based operations
- **Policy as Code**: OPA, Kyverno
- **Infrastructure as Code**: Terraform, Pulumi
- **Observability**: OpenTelemetry, Jaeger

## Final Project: Complete Infrastructure

Create a production-ready multi-service application:

**Requirements**:
- Multi-container application
- Custom networks
- Persistent storage
- Security hardening
- Monitoring and logging
- Automated backups
- CI/CD pipeline
- Complete documentation
- Disaster recovery plan

**Your Stack Transformation**:
Transform your current containers into:
- Secure, hardened containers
- Optimized images
- Monitored services
- Automated backups
- Documented infrastructure
- CI/CD enabled

## Course Completion

### You've Learned:
✅ Docker fundamentals and architecture  
✅ Container and image management  
✅ Networking and storage  
✅ Docker Compose orchestration  
✅ Security best practices  
✅ Production deployment  
✅ Monitoring and troubleshooting  
✅ CI/CD integration  

### You Can Now:
✅ Containerize any application  
✅ Deploy production workloads  
✅ Troubleshoot Docker issues  
✅ Optimize containers for performance  
✅ Implement security measures  
✅ Automate container workflows  
✅ Work with Docker anywhere (Windows, Linux, macOS)  

## Certificate of Completion

Congratulations on completing the Docker & Containers Training Path!

**Skills Acquired**:
- Docker CLI mastery
- Container lifecycle management
- Image creation and optimization
- Networking and storage
- Docker Compose
- Security and best practices
- Production deployment
- CI/CD integration

**Next Steps**:
1. Apply knowledge to real projects
2. Contribute to open source
3. Explore orchestration (Kubernetes)
4. Continue learning DevOps practices

## Community & Support

### Continue Learning
- [Docker Community Forums](https://forums.docker.com/)
- [Docker Blog](https://www.docker.com/blog/)
- [Awesome Docker](https://github.com/veggiemonk/awesome-docker)
- [Play with Docker](https://labs.play-with-docker.com/)

### Practice Environments
- Docker Playground
- Katacoda scenarios
- Your own projects!

## Navigation

- **Previous**: [Phase 05: Docker Compose](../Phase_05_Docker_Compose/README.md)
- **Home**: [Training Path Home](../README.md)

---

**Ready to begin?** Start with [01_Security.md](01_Security.md)

**Last Updated**: February 16, 2026
