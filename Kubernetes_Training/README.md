# Kubernetes Training Path

Learn container orchestration with Kubernetes on Windows using Docker Desktop's built-in Kubernetes.

## Why Kubernetes?

Kubernetes (K8s) is the industry-standard container orchestration platform:
- **Scale automatically** - Handle increased load seamlessly
- **Self-healing** - Automatic restart, replacement, and rescheduling
- **Service discovery** - Built-in DNS and load balancing
- **Rolling updates** - Zero-downtime deployments
- **Declarative configuration** - Describe desired state, K8s maintains it

## Prerequisites

- **Docker Training** - Complete Phase 01-05 (especially Docker Compose)
- **Basic YAML** - Understanding of YAML syntax
- **Networking basics** - Understanding of ports, DNS, load balancing
- **Linux basics** - Basic container knowledge

## Lab Environment

You have multiple excellent options for Kubernetes learning:

### Single-Node Options
- **Docker Desktop Kubernetes** - Built-in, easiest to start (Windows)
- **Minikube** - Full-featured, works on Windows or Linux VM
- **K3s** - Lightweight K8s perfect for Linux VMs

### Multi-Node Options  
- **Kind** - Kubernetes in Docker (multi-node on single machine)
- **Multiple Linux VMs** - Most production-like setup
- **K3s cluster** - Lightweight multi-node on VMs

### Setup Options

#### Option 1: Docker Desktop K8s (Easiest Start)
```powershell
# On Windows
# 1. Open Docker Desktop
# 2. Settings → Kubernetes
# 3. Check "Enable Kubernetes"
# 4. Click "Apply & Restart"

# Install kubectl via Chocolatey
choco install kubernetes-cli
choco install k9s
choco install kubernetes-helm

# Verify
kubectl get nodes
# Should show: docker-desktop   Ready    control-plane   ...
```

#### Option 2: Minikube on Linux VM (Recommended for Learning)
```bash
# On Ubuntu VM
# Install Docker first, then:
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start cluster
minikube start --driver=docker --nodes=3  # Multi-node!

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Verify
kubectl get nodes
```

#### Option 3: K3s on Linux VM (Production-Like, Lightweight)
```bash
# On Ubuntu VM (Control Plane)
curl -sfL https://get.k3s.io | sh -

# Get node token for workers
sudo cat /var/lib/rancher/k3s/server/node-token

# On additional VMs (Workers) - optional
curl -sfL https://get.k3s.io | K3S_URL=https://<control-plane-ip>:6443 K3S_TOKEN=<token> sh -

# Kubectl included with K3s
sudo kubectl get nodes
```

#### Option 4: Kind (Multi-Node on Single Machine)
```bash
# On Windows (PowerShell) or Linux
# Install Kind
choco install kind  # Windows
# or
curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64  # Linux
chmod +x ./kind && sudo mv ./kind /usr/local/bin/kind

# Create multi-node cluster
kind create cluster --config=kind-config.yaml
# (See Kind documentation for config examples)
```

**Recommendation**: 
- **Start with**: Docker Desktop K8s (quickest to begin learning)
- **Progress to**: Minikube on Linux VM with 3 nodes (more realistic)
- **Advanced**: K3s cluster on multiple VMs (production-like)

## Training Structure

### Phase 01: Kubernetes Fundamentals (6-8 hours)
**Goal**: Understand K8s architecture and basic concepts

**Topics**:
- Kubernetes architecture
- Control plane components
- Node components
- Pods and containers
- kubectl basics
- Namespaces
- Labels and selectors
- Annotations

**Lab Environment**: Docker Desktop K8s (single-node)

**Hands-on**:
- Enable Kubernetes in Docker Desktop
- Deploy first pod
- Use kubectl commands
- Explore namespaces
- Work with labels

### Phase 02: Workload Resources (8-10 hours)
**Goal**: Deploy and manage applications in Kubernetes

**Topics**:
- Pods in detail
- ReplicaSets
- Deployments
- StatefulSets
- DaemonSets
- Jobs and CronJobs
- Init containers
- Multi-container pods

**Lab Environment**: Docker Desktop K8s

**Hands-on**:
- Create deployments
- Scale applications
- Rolling updates and rollbacks
- Run background jobs
- Deploy your Docker apps to K8s

### Phase 03: Services & Networking (6-8 hours)
**Goal**: Expose applications and configure networking

**Topics**:
- Service types (ClusterIP, NodePort, LoadBalancer)
- Service discovery and DNS
- Endpoints
- Ingress controllers
- Ingress rules and routing
- Network policies
- CoreDNS
- Port forwarding

**Lab Environment**: Docker Desktop K8s with Ingress

**Hands-on**:
- Create services
- Set up ingress controller
- Configure ingress rules
- Implement service mesh basics
- Expose your applications

### Phase 04: Configuration & Secrets (5-7 hours)
**Goal**: Manage application configuration securely

**Topics**:
- ConfigMaps
- Secrets
- Environment variables
- Volume mounts for config
- Secret management best practices
- External secret stores
- Immutable ConfigMaps/Secrets

**Lab Environment**: Docker Desktop K8s

**Hands-on**:
- Create ConfigMaps
- Manage secrets securely
- Inject configuration
- Update configs without restart
- Migrate Docker Compose env vars

### Phase 05: Storage & Persistence (6-8 hours)
**Goal**: Handle persistent data in Kubernetes

**Topics**:
- Volumes
- PersistentVolumes (PV)
- PersistentVolumeClaims (PVC)
- StorageClasses
- Dynamic provisioning
- StatefulSets with storage
- Volume types
- Backup and restore

**Lab Environment**: Docker Desktop K8s with local storage

**Hands-on**:
- Create persistent volumes
- Use storage classes
- Deploy stateful applications
- Migrate Docker volumes to K8s
- Handle data persistence

### Phase 06: Application Management (8-10 hours)
**Goal**: Package and deploy complex applications

**Topics**:
- Helm fundamentals
- Charts and repositories
- Values and templating
- Installing charts
- Creating custom charts
- Chart dependencies
- Helm vs kubectl
- Kustomize basics

**Lab Environment**: Docker Desktop K8s

**Hands-on**:
- Install apps with Helm
- Create custom Helm charts
- Manage releases
- Package your applications
- Convert Docker Compose to Helm

### Phase 07: Observability & Debugging (6-8 hours)
**Goal**: Monitor, log, and troubleshoot applications

**Topics**:
- Container logs
- kubectl debugging commands
- Resource metrics
- Liveness and readiness probes
- Startup probes
- Events
- Monitoring with Prometheus
- Logging with ELK/Loki
- Distributed tracing

**Lab Environment**: Docker Desktop K8s with monitoring stack

**Hands-on**:
- View and stream logs
- Debug failing pods
- Set up health checks
- Install Prometheus/Grafana
- Troubleshoot common issues

### Phase 08: Security & RBAC (6-8 hours)
**Goal**: Secure Kubernetes clusters and workloads

**Topics**:
- Authentication and authorization
- RBAC (Role-Based Access Control)
- ServiceAccounts
- Security contexts
- Pod security standards
- Network policies
- Secrets encryption
- Image security

**Lab Environment**: Docker Desktop K8s

**Hands-on**:
- Configure RBAC
- Create service accounts
- Implement pod security
- Restrict network access
- Scan images for vulnerabilities

### Phase 09: Advanced Topics (8-10 hours)
**Goal**: Master advanced Kubernetes features

**Topics**:
- Resource management (requests/limits)
- Autoscaling (HPA, VPA, Cluster Autoscaler)
- Affinity and anti-affinity
- Taints and tolerations
- Custom Resource Definitions (CRDs)
- Operators
- Admission controllers
- Service mesh (Istio/Linkerd)

**Lab Environment**: Multi-node with Kind (optional)

**Hands-on**:
- Configure autoscaling
- Use advanced scheduling
- Create custom resources
- Deploy service mesh
- Optimize resource usage

### Phase 10: Real-World Projects (15-20 hours)
**Goal**: Deploy production-grade applications

**Projects**:
1. **Migrate Your Docker Stack**
   - Convert docker-compose.yml to K8s manifests
   - Deploy Traefik as Ingress
   - Migrate all services (Calibre, LazyLibrarian, etc.)
   - Implement persistent storage
   - Set up monitoring

2. **Multi-Tier Application**
   - Frontend (React/Vue)
   - Backend API (Node.js/Python)
   - Database (PostgreSQL/MySQL)
   - Redis cache
   - Complete CI/CD pipeline

3. **Microservices Platform**
   - Multiple services
   - Service mesh
   - Distributed tracing
   - Centralized logging
   - Auto-scaling

4. **GitOps Workflow**
   - ArgoCD or Flux
   - Git as source of truth
   - Automated deployments
   - Multi-environment management

## Learning Path Integration

### Natural Progression
1. **Docker Training** (Complete Phase 01-05)
2. **Kubernetes Phase 01-03** (Core concepts)
3. **Terraform** (Provision K8s clusters in cloud)
4. **Kubernetes Phase 04-07** (Application management)
5. **Ansible** (Initial cluster configuration)
6. **Kubernetes Phase 08-10** (Advanced and production)

### Why This Order?
- **Docker first**: K8s orchestrates containers; must understand containers
- **Docker Compose**: Similar concepts to K8s manifests
- **Terraform**: Infrastructure provisioning for real clusters
- **Ansible**: Configuration management complements K8s

## Lab Scenarios

### Beginner Labs
- Deploy nginx pod
- Create deployment with replicas
- Expose service with NodePort
- View logs and exec into pods

### Intermediate Labs
- Multi-tier web application
- Ingress with multiple routes
- StatefulSet for database
- ConfigMaps and Secrets

### Advanced Labs
- Complete microservices platform
- Service mesh implementation
- Autoscaling configuration
- Multi-cluster federation

## Key Commands Reference

```powershell
# Cluster info
kubectl cluster-info
kubectl get nodes
kubectl version

# Working with resources
kubectl get pods
kubectl get pods -A                    # All namespaces
kubectl get pods -o wide               # More details
kubectl get pods -w                    # Watch mode
kubectl describe pod <name>
kubectl logs <pod>
kubectl logs -f <pod>                  # Follow logs
kubectl logs <pod> -c <container>      # Specific container
kubectl exec -it <pod> -- /bin/sh      # Shell access
kubectl port-forward <pod> 8080:80     # Port forward

# Deployments
kubectl create deployment nginx --image=nginx
kubectl get deployments
kubectl describe deployment <name>
kubectl scale deployment <name> --replicas=3
kubectl set image deployment/<name> nginx=nginx:1.21
kubectl rollout status deployment/<name>
kubectl rollout undo deployment/<name>
kubectl rollout history deployment/<name>

# Services
kubectl expose deployment <name> --port=80 --type=NodePort
kubectl get services
kubectl get endpoints

# ConfigMaps and Secrets
kubectl create configmap <name> --from-file=config.txt
kubectl create secret generic <name> --from-literal=password=secret
kubectl get configmaps
kubectl get secrets

# Apply/Delete resources
kubectl apply -f manifest.yaml
kubectl apply -f ./directory/
kubectl delete -f manifest.yaml
kubectl delete pod <name>
kubectl delete deployment <name>

# Namespaces
kubectl get namespaces
kubectl create namespace <name>
kubectl config set-context --current --namespace=<name>

# Debugging
kubectl describe pod <name>
kubectl logs <pod>
kubectl exec -it <pod> -- /bin/sh
kubectl top nodes
kubectl top pods

# Helm
helm repo add stable https://charts.helm.sh/stable
helm repo update
helm search repo <chart>
helm install <release> <chart>
helm list
helm upgrade <release> <chart>
helm uninstall <release>

# Context switching (for multiple clusters)
kubectl config get-contexts
kubectl config use-context <context>
```

## Example: Docker Compose to Kubernetes

**Your docker-compose.yml**:
```yaml
version: '3.8'
services:
  web:
    image: nginx
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html
```

**Kubernetes equivalent**:
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 1
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
        volumeMounts:
        - name: html
          mountPath: /usr/share/nginx/html
      volumes:
      - name: html
        hostPath:
          path: /path/to/html
---
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  type: NodePort
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080
```

## Migration Path: Your Docker Stack → Kubernetes

You'll learn to migrate:
1. **Traefik** → Nginx Ingress Controller or Traefik Ingress
2. **Calibre-web** → Deployment + PVC + Service + Ingress
3. **LazyLibrarian** → Deployment + PVC + Service + Ingress
4. **OpenMemory** → Deployment + ConfigMap + Service + Ingress
5. **AdGuard Home** → StatefulSet + Service
6. **Networks** → Network Policies and Services
7. **Volumes** → PersistentVolumes and Claims

## Resources

### Official Documentation
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes API Reference](https://kubernetes.io/docs/reference/kubernetes-api/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

### Learning Resources
- [Kubernetes the Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way)
- [Kubernetes Up & Running](https://www.oreilly.com/library/view/kubernetes-up-and/9781492046523/) book
- [CNCF Kubernetes Training](https://www.cncf.io/certification/training/)

### Tools
- [k9s](https://k9scli.io/) - Terminal UI
- [Lens](https://k8slens.dev/) - Kubernetes IDE
- [Helm](https://helm.sh/) - Package manager
- [Kind](https://kind.sigs.k8s.io/) - K8s in Docker

### Community
- [Kubernetes Slack](https://slack.k8s.io/)
- [Kubernetes Subreddit](https://reddit.com/r/kubernetes)
- [CNCF](https://www.cncf.io/)

## Best Practices

1. **Declarative Configuration**: Use YAML manifests, not imperative commands
2. **Version Control**: All manifests in Git
3. **Namespaces**: Organize resources logically
4. **Resource Limits**: Always set requests and limits
5. **Health Checks**: Implement liveness and readiness probes
6. **Labels**: Use meaningful, consistent labels
7. **Secrets Management**: Never commit secrets to Git
8. **Rolling Updates**: Use deployment strategies for zero downtime
9. **Monitoring**: Implement observability from day one
10. **Documentation**: Comment complex configurations

## Success Criteria

By the end of this training, you should be able to:
- ✅ Deploy applications to Kubernetes
- ✅ Expose services with Ingress
- ✅ Manage configuration and secrets
- ✅ Handle persistent storage
- ✅ Monitor and debug applications
- ✅ Scale applications automatically
- ✅ Implement security best practices
- ✅ Migrate Docker Compose apps to K8s
- ✅ Use Helm for package management
- ✅ Understand K8s architecture deeply

## Estimated Time

- **Minimum**: 40-50 hours (basics through application management)
- **Recommended**: 70-90 hours (including advanced topics)
- **Mastery**: 120+ hours (production mastery and projects)

## Getting Started

1. Enable Kubernetes in Docker Desktop
2. Install kubectl and verify connection
3. Complete Docker Training Phase 01-05
4. Deploy your first pod
5. Explore with kubectl
6. Try k9s for better visibility

## Next Steps

After completing Kubernetes training:
- **CKA Certification** - Certified Kubernetes Administrator
- **CKAD Certification** - Certified Kubernetes Application Developer
- **Service Mesh**: Istio or Linkerd
- **GitOps**: ArgoCD or Flux
- **Multi-Cloud**: EKS (AWS), AKS (Azure), GKE (Google)

## Why Docker Desktop K8s?

Perfect for learning:
- ✅ Pre-installed with Docker Desktop
- ✅ Single-node simplicity
- ✅ No cloud costs
- ✅ Fast iteration
- ✅ Same kubectl/YAML as production
- ✅ Easy reset (disable/enable)

Later, expand to:
- **Kind**: Multi-node clusters on your machine
- **AKS**: Azure Kubernetes Service (from your Azure training)
- **EKS**: Amazon EKS (from your AWS training)

---

**Note**: Kubernetes is complex but incredibly powerful. Start with Docker Desktop's built-in K8s, master the concepts locally, then scale to cloud providers.

Welcome to the world of container orchestration! ☸️
