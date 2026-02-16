# Terraform Training Path

Learn Infrastructure as Code (IaC) using Terraform on Windows to manage Docker, Azure, and AWS resources.

## Why Terraform?

Terraform lets you define infrastructure using code:
- **Declarative syntax** - Describe what you want, not how to build it
- **Multi-cloud** - One tool for Docker, Azure, AWS, and more
- **Version control** - Treat infrastructure like application code
- **Plan before apply** - Preview changes before making them
- **State management** - Track infrastructure state automatically

## Prerequisites

- **Docker Training** - Complete at least Phase 01-03
- **Basic understanding of cloud resources** (from your Azure/AWS folders)
- **PowerShell** - Basic command familiarity
- **Git** - Version control basics

## Lab Environment

You can practice Terraform on your Windows machine with:
- **Docker provider** - Manage your existing containers
- **Azure** - Free tier resources
- **AWS** - Free tier resources  
- **Local resources** - Files, null resources for testing

### Setup Options

#### Option 1: Windows (PowerShell) - Works Great!
```powershell
# Install Terraform via Chocolatey
choco install terraform

# Or download from https://www.terraform.io/downloads
# Add to PATH

# Verify installation
terraform version

# Enable tab completion (PowerShell)
terraform -install-autocomplete
```

#### Option 2: Linux VM (Optional)
```bash
# On Ubuntu/Debian
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform

# Verify
terraform version
```

**Note**: Terraform works equally well on Windows and Linux. Use Windows/PowerShell for convenience, or Linux VM if you prefer working in Linux environments.

## Training Structure

### Phase 01: Terraform Fundamentals (5-7 hours)
**Goal**: Understand Terraform basics and deploy your first resources

**Topics**:
- Infrastructure as Code concepts
- Terraform workflow (init, plan, apply, destroy)
- HCL syntax (HashiCorp Configuration Language)
- Providers and resources
- State files and state management
- Terraform CLI commands

**Lab Environment**: Docker provider (manage your containers)

**Hands-on**:
- Install Terraform on Windows
- Write first configuration
- Deploy Docker container with Terraform
- Understand state files
- Destroy and recreate resources

### Phase 02: Language & Configuration (6-8 hours)
**Goal**: Master HCL and resource configuration

**Topics**:
- Variables and input validation
- Output values
- Data sources
- Locals and expressions
- Functions and built-ins
- Type constraints
- String interpolation
- Conditionals and loops

**Lab Environment**: Multi-container Docker setup

**Hands-on**:
- Create reusable configurations
- Use variables for flexibility
- Output resource information
- Query existing resources
- Complex variable structures

### Phase 03: Managing Docker Infrastructure (4-6 hours)
**Goal**: Manage complete Docker environment with Terraform

**Topics**:
- Docker provider deep dive
- Container resources
- Image management
- Networks and volumes
- Dependencies between resources
- Docker Compose vs Terraform
- Managing existing containers

**Lab Environment**: Your current Docker stack

**Hands-on**:
- Recreate your Docker stack in Terraform
- Manage Traefik configuration
- Create network topology
- Handle persistent volumes
- Import existing containers

### Phase 04: State & Remote Backends (4-6 hours)
**Goal**: Understand state management and collaboration

**Topics**:
- State file deep dive
- Remote state storage
- State locking
- State manipulation commands
- Workspaces
- Sensitive data in state
- State migration

**Lab Environment**: Azure Storage or local backend

**Hands-on**:
- Set up remote state storage
- Use workspaces for environments
- Safely manipulate state
- Recover from state issues
- Import existing resources

### Phase 05: Modules & Organization (6-8 hours)
**Goal**: Create reusable, maintainable Terraform code

**Topics**:
- Module structure and design
- Module inputs and outputs
- Module versioning
- Public module registry
- Local vs remote modules
- Module composition
- Testing modules

**Lab Environment**: Multi-provider setup

**Hands-on**:
- Create custom modules
- Use public registry modules
- Organize complex infrastructure
- Version and publish modules
- Build module library

### Phase 06: Multi-Cloud & Advanced (8-10 hours)
**Goal**: Work with Azure, AWS, and advanced patterns

**Topics**:
- Azure provider
- AWS provider
- Provider configuration
- Provider versioning
- Multi-provider dependencies
- Provisioners (when necessary)
- Dynamic blocks
- Advanced functions

**Lab Environment**: Azure free tier + AWS free tier

**Hands-on**:
- Deploy Azure resources (Storage, Virtual Networks)
- Deploy AWS resources (S3, EC2)
- Mix Docker + Cloud resources
- Use provisioners sparingly
- Advanced configurations

### Phase 07: Best Practices & Production (6-8 hours)
**Goal**: Production-ready Terraform workflows

**Topics**:
- Directory structure
- Code organization patterns
- Naming conventions
- Security best practices
- CI/CD integration
- Automated testing
- Policy as Code (Sentinel/OPA)
- Drift detection

**Lab Environment**: Full multi-environment setup

**Hands-on**:
- Set up dev/staging/prod
- Implement security controls
- Automate with CI/CD
- Test infrastructure code
- Handle secrets properly

### Phase 08: Real-World Projects (10-15 hours)
**Goal**: Apply Terraform to complete infrastructure scenarios

**Projects**:
1. **Complete Lab Environment**
   - Docker containers
   - Networking and storage
   - Traefik reverse proxy
   - Monitoring stack

2. **Azure Infrastructure**
   - Resource groups
   - Storage accounts
   - Virtual networks
   - VMs or App Services

3. **AWS Infrastructure**
   - VPC and networking
   - EC2 instances
   - S3 buckets
   - IAM roles

4. **Hybrid Deployment**
   - Local Docker services
   - Cloud backing services
   - Multi-cloud redundancy
   - Complete application stack

## Learning Path Integration

### Recommended Order
1. **Docker Phase 01-04** first
2. Terraform Phase 01-02 (basics and HCL)
3. Terraform Phase 03 (Docker provider)
4. **Parallel with Ansible**: Terraform provisions, Ansible configures
5. Terraform Phase 04-07 (advanced topics)
6. Kubernetes Training (Terraform can provision K8s clusters)

### Complementary Skills
- **With Docker**: Codify container infrastructure
- **With Ansible**: Terraform provisions, Ansible configures
- **With Kubernetes**: Provision and manage K8s clusters
- **With Azure/AWS**: Full cloud automation

## Lab Scenarios

### Beginner Labs
- Deploy single Docker container
- Create Docker network
- Manage Docker volumes
- Simple variable usage

### Intermediate Labs
- Full Docker stack (your current setup)
- Multi-environment configurations
- Remote state storage
- Custom modules

### Advanced Labs
- Multi-cloud deployment
- Complex module composition
- CI/CD integration
- Complete infrastructure platform

## Key Commands Reference

```powershell
# Initialize Terraform
terraform init

# Format code
terraform fmt
terraform fmt -check -recursive

# Validate configuration
terraform validate

# Plan changes
terraform plan
terraform plan -out=plan.tfplan

# Apply changes
terraform apply
terraform apply plan.tfplan
terraform apply -auto-approve

# Destroy resources
terraform destroy
terraform destroy -auto-approve

# State management
terraform state list
terraform state show <resource>
terraform state mv <source> <dest>
terraform state rm <resource>
terraform state pull
terraform state push

# Import existing resources
terraform import <resource_type>.<name> <id>

# Workspaces
terraform workspace list
terraform workspace new <name>
terraform workspace select <name>

# Output values
terraform output
terraform output <name>

# Show current state
terraform show

# Refresh state
terraform refresh

# Graph visualization
terraform graph | Out-File graph.dot
# View with GraphViz
```

## Example: Your Docker Stack in Terraform

```hcl
# main.tf
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {
  host = "npipe:////./pipe/docker_engine"
}

# Traefik network
resource "docker_network" "traefik" {
  name = "traefik"
}

# Traefik reverse proxy
resource "docker_container" "traefik" {
  name  = "traefik"
  image = "traefik:v3.2"
  
  networks_advanced {
    name = docker_network.traefik.name
  }

  ports {
    internal = 80
    external = 80
  }

  ports {
    internal = 443
    external = 443
  }

  volumes {
    host_path      = "/var/run/docker.sock"
    container_path = "/var/run/docker.sock"
    read_only      = true
  }
}

# Calibre-web
resource "docker_container" "calibre" {
  name  = "calibre-web"
  image = "linuxserver/calibre-web:latest"
  
  networks_advanced {
    name = docker_network.traefik.name
  }
  
  env = [
    "PUID=1000",
    "PGID=1000",
    "TZ=America/Chicago"
  ]
  
  volumes {
    volume_name    = "calibre_config"
    container_path = "/config"
  }

  volumes {
    host_path      = "/path/to/books"
    container_path = "/books"
  }
}
```

## Integration with Your Learning

### Azure Connection
Apply Terraform to your Azure studies:
- Automate resource group creation
- Deploy VNets and subnets
- Create storage accounts
- Build lab environments for AZ-104

### AWS Connection
Support your AWS training:
- Provision VPCs
- Deploy EC2 instances
- Manage S3 buckets
- Practice for certifications

### Lab Environment
Codify your entire lab:
- Docker containers
- Network configuration
- Storage management
- Repeatable deployments

## Resources

### Official Documentation
- [Terraform Documentation](https://www.terraform.io/docs)
- [Terraform Registry](https://registry.terraform.io/)
- [Provider Documentation](https://registry.terraform.io/browse/providers)
- [Docker Provider](https://registry.terraform.io/providers/kreuzwerker/docker/latest/docs)

### Learning Resources
- [HashiCorp Learn](https://learn.hashicorp.com/terraform)
- [Terraform: Up & Running](https://www.terraformupandrunning.com/) book
- [Terraform Best Practices](https://www.terraform-best-practices.com/)

### Community
- [Terraform Subreddit](https://reddit.com/r/terraform)
- [HashiCorp Discuss](https://discuss.hashicorp.com/c/terraform-core)
- [GitHub Issues](https://github.com/hashicorp/terraform)

## Best Practices

1. **Version Control**: Always use Git for Terraform code
2. **State Security**: Use remote state with encryption
3. **Least Privilege**: Use minimal permissions for providers
4. **Formatting**: Run `terraform fmt` regularly
5. **Validation**: Always run `terraform validate`
6. **Planning**: Review plans before applying
7. **Modules**: Reuse code through modules
8. **Documentation**: Comment complex logic
9. **Secrets**: Never commit secrets; use variables
10. **Testing**: Test changes in dev/staging first

## Success Criteria

By the end of this training, you should be able to:
- ✅ Write Terraform configurations in HCL
- ✅ Manage Docker infrastructure with Terraform
- ✅ Deploy Azure and AWS resources
- ✅ Use modules for code reusability
- ✅ Manage state files properly
- ✅ Implement multi-environment strategies
- ✅ Integrate Terraform into CI/CD
- ✅ Follow production best practices

## Estimated Time

- **Minimum**: 30-35 hours (basics through Docker management)
- **Recommended**: 45-60 hours (including cloud providers)
- **Mastery**: 80+ hours (advanced patterns and projects)

## Getting Started

1. Install Terraform (see Setup above)
2. Complete Docker Training Phase 01-03
3. Write your first Terraform configuration
4. Deploy a Docker container
5. Explore the state file
6. Plan and apply changes

## Next Steps

After completing Terraform training:
- **Integrate with Ansible**: Terraform + Ansible = Complete automation
- **Kubernetes**: Use Terraform to provision K8s clusters
- **Cloud Certifications**: Azure/AWS with IaC focus
- **Terraform Cloud/Enterprise**: Team collaboration platform

---

**Note**: Terraform is a powerful tool for managing infrastructure declaratively. Start with Docker provider to learn concepts, then expand to cloud providers.

Infrastructure as Code = Version-controlled, repeatable, testable infrastructure! 🏗️
