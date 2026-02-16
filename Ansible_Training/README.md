# Ansible Training Path

Learn configuration management and automation using Ansible on Windows with WSL2.

## Why Ansible?

Ansible is an agentless automation tool that helps you:
- **Automate repetitive tasks** - Configure multiple systems with playbooks
- **Manage infrastructure** - Declarative configuration management
- **Orchestrate complex workflows** - Multi-step deployments and updates
- **Integrate with everything** - Docker, cloud providers, Windows, Linux

## Prerequisites

- **Docker Training** - Complete at least Phase 01-02
- **Basic YAML** - Understanding of YAML syntax
- **Linux basics** - Basic command line familiarity
- **WSL2** - Ansible runs in Linux environment

## Lab Environment

You can practice Ansible on your Windows machine using:
- **Linux VM** - Ubuntu/Rocky Linux VM (RECOMMENDED for production-like experience)
- **WSL2** - Ubuntu on WSL2 (convenient for quick testing)
- **Docker containers** - Use containers as managed hosts
- **Windows host** - Configure Windows using WinRM
- **Local files** - Practice with templates and file management

### Setup Options

#### Option 1: Linux VM (Recommended)
```bash
# On Ubuntu/Debian VM
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install -y ansible

# On RHEL/Rocky/CentOS
sudo dnf install -y epel-release
sudo dnf install -y ansible

# Verify installation
ansible --version
```

#### Option 2: WSL2 (Quick Start)
```bash
# In WSL2 Ubuntu
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install -y ansible

# Verify installation
ansible --version
```

**Why Linux VM over WSL2?**
- More like production environments
- Better for SSH key management
- Easier networking with other VMs
- Can snapshot/rollback
- No Windows filesystem performance issues

## Training Structure

### Phase 01: Ansible Fundamentals (4-6 hours)
**Goal**: Understand Ansible basics and run your first playbooks

**Topics**:
- Ansible architecture and concepts
- Inventory files (hosts and groups)
- Ad-hoc commands
- Modules and tasks
- Variables and facts
- Ansible configuration

**Lab Environment**: Use Docker containers as managed hosts

**Hands-on**:
- Install Ansible in WSL2
- Create inventory of Docker containers
- Run ad-hoc commands
- Gather facts from hosts

### Phase 02: Playbooks & Roles (6-8 hours)
**Goal**: Write playbooks to automate configuration tasks

**Topics**:
- Playbook structure and syntax
- Tasks, handlers, and notifications
- Conditionals and loops
- Templates (Jinja2)
- Roles and role structure
- Ansible Galaxy

**Lab Environment**: Multi-container Docker setup

**Hands-on**:
- Write playbooks to configure web servers
- Use templates for config files
- Create reusable roles
- Organize complex playbooks

### Phase 03: Managing Docker with Ansible (4-6 hours)
**Goal**: Automate Docker container and image management

**Topics**:
- Docker modules (docker_container, docker_image, etc.)
- Docker Compose module
- Managing container state
- Building images with Ansible
- Container orchestration
- Volume and network management

**Lab Environment**: Your existing Docker setup

**Hands-on**:
- Deploy containers using Ansible
- Manage your current container stack
- Create playbook for your lab environment
- Update and restart containers

### Phase 04: Advanced Automation (6-8 hours)
**Goal**: Create complex automation workflows

**Topics**:
- Vault for secrets management
- Dynamic inventory
- Error handling and rescue blocks
- Async tasks and polling
- Custom modules
- Ansible Tower/AWX concepts
- Integration with CI/CD

**Lab Environment**: Mixed Windows and Linux targets

**Hands-on**:
- Encrypt sensitive data with Vault
- Create dynamic inventory for Docker
- Write error-resilient playbooks
- Automate deployment pipeline

### Phase 05: Real-World Projects (8-10 hours)
**Goal**: Apply Ansible to practical scenarios

**Projects**:
1. **Infrastructure as Code**
   - Full environment deployment
   - Multi-tier application setup
   - Automated configuration management

2. **Container Stack Management**
   - Automated deployment of your Docker stack
   - Container updates and rollbacks
   - Health checks and monitoring setup

3. **Windows Management**
   - Configure Windows using WinRM
   - Manage Windows services and features
   - Deploy applications on Windows

4. **Hybrid Automation**
   - Manage both Windows and Linux
   - Docker containers and VMs
   - Multi-cloud deployments (Azure/AWS)

## Learning Path Integration

### Recommended Order
1. **Complete Docker Phase 01-03** first
2. Start with Ansible Phase 01-02
3. Parallel learning with Terraform basics
4. Ansible Phase 03 (Docker integration)
5. Continue with advanced topics

### Complementary Skills
- **With Docker**: Automate container deployment
- **With Terraform**: Configuration after infrastructure provisioning
- **With Kubernetes**: Initial cluster configuration
- **With CI/CD**: Deployment automation

## Lab Scenarios

### Beginner Labs
- Configure multiple Docker containers identically
- Deploy a web application across containers
- Manage configuration files with templates
- Install packages on multiple hosts

### Intermediate Labs
- Deploy your current Docker stack using Ansible
- Create roles for common configurations
- Use Ansible Vault for secrets
- Dynamic inventory from Docker

### Advanced Labs
- Full infrastructure automation
- Zero-downtime deployments
- Multi-environment management (dev/staging/prod)
- Custom module development

## Key Commands Reference

```bash
# Ad-hoc commands
ansible all -m ping
ansible webservers -m setup
ansible all -a "uptime"

# Playbook execution
ansible-playbook playbook.yml
ansible-playbook playbook.yml --check        # Dry run
ansible-playbook playbook.yml --limit host1  # Single host
ansible-playbook playbook.yml --tags "config"

# Inventory
ansible-inventory --list
ansible-inventory --graph

# Vault
ansible-vault create secrets.yml
ansible-vault encrypt file.yml
ansible-vault decrypt file.yml
ansible-playbook playbook.yml --ask-vault-pass

# Galaxy
ansible-galaxy init role_name
ansible-galaxy install username.role_name
ansible-galaxy list
```

## Practical Use Cases

### Your Current Environment
With your existing Docker setup, you can:
- Automate deployment of Traefik, Calibre-web, LazyLibrarian
- Update all containers with one command
- Manage environment variables centrally
- Deploy new services consistently
- Backup and restore configurations

### Future Applications
- **Azure/AWS**: Provision and configure cloud resources
- **EUC**: Manage user environments and applications
- **Lab Environment**: Automate lab setup and teardown
- **Development**: Consistent dev environment setup

## Resources

### Official Documentation
- [Ansible Documentation](https://docs.ansible.com/)
- [Ansible Galaxy](https://galaxy.ansible.com/)
- [Module Index](https://docs.ansible.com/ansible/latest/collections/index_module.html)

### Learning Resources
- [Ansible for DevOps](https://www.ansiblefordevops.com/) book
- [Ansible 101 on YouTube](https://www.youtube.com/playlist?list=PL2_OBreMn7FqZkvMYt6ATmgC0KAGGJNAN)
- [Learn Ansible](https://www.redhat.com/en/technologies/management/ansible/learning-path)

### Community
- [Ansible Subreddit](https://reddit.com/r/ansible)
- [Ansible Google Group](https://groups.google.com/g/ansible-project)
- [GitHub Issues](https://github.com/ansible/ansible)

## Best Practices

1. **Idempotency**: Playbooks should be safe to run multiple times
2. **Version Control**: Always keep playbooks in Git
3. **Testing**: Use --check mode before applying changes
4. **Documentation**: Comment complex tasks and playbooks
5. **Secrets**: Never commit passwords; use Vault
6. **Organization**: Use roles for reusability
7. **Simplicity**: Start simple; add complexity as needed

## Success Criteria

By the end of this training, you should be able to:
- ✅ Write and execute Ansible playbooks
- ✅ Manage Docker containers with Ansible
- ✅ Create reusable roles
- ✅ Use templates and variables effectively
- ✅ Secure sensitive data with Vault
- ✅ Automate your lab environment deployment
- ✅ Integrate Ansible into CI/CD workflows

## Estimated Time

- **Minimum**: 20-25 hours (basics and Docker integration)
- **Recommended**: 30-40 hours (including projects)
- **Mastery**: 50+ hours (advanced topics and real-world practice)

## Getting Started

1. Complete Docker Training Phase 01-02
2. Install Ansible in WSL2 (see Setup above)
3. Create first inventory file with Docker containers
4. Run your first ad-hoc command
5. Write a simple playbook

## Next Steps

After completing Ansible training:
- **Terraform**: Infrastructure provisioning (Ansible configures what Terraform builds)
- **Kubernetes**: Container orchestration at scale
- **CI/CD**: Integrate Ansible into automated pipelines
- **AWX/Tower**: Enterprise automation platform

---

**Note**: Ansible runs on Linux (not Windows natively). You have two great options:
1. **Linux VM** (Recommended) - Full Linux environment, production-like setup, better SSH handling
2. **WSL2** (Quick start) - Convenient but has some limitations with networking and SSH keys

Ansible can manage Windows hosts via WinRM regardless of where it runs.

Ready to automate all the things! 🚀
