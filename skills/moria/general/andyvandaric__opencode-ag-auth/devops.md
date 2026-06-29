## 🐳 DevOps & Infrastructure Rules

### Docker Best Practices

#### Dockerfile Conventions
```dockerfile
# ✅ Use specific base image tags (not :latest)
FROM node:20-alpine

# ✅ Use multi-stage builds for smaller images
FROM node:20 AS builder
WORKDIR /app
COPY package*.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile
COPY . .
RUN pnpm build

FROM node:20-alpine AS production
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY package*.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile --prod
EXPOSE 3000
CMD ["node", "dist/main.js"]

# ✅ Combine RUN commands to reduce layers
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# ✅ Use .dockerignore to exclude unnecessary files
# node_modules, .git, *.log, etc.
```

#### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: 
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

---

### Terraform Best Practices

#### File Structure
```
terraform/
├── main.tf           # Main resources
├── variables.tf      # Input variables
├── outputs.tf        # Output values
├── providers.tf      # Provider configurations
├── backend.tf        # State backend config
├── terraform.tfvars  # Variable values (git-ignored)
└── modules/          # Reusable modules
    └── vpc/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

#### Conventions
```hcl
# ✅ Use snake_case for resource names
resource "aws_instance" "web_server" {
  ami           = var.ami_id
  instance_type = var.instance_type
  
  tags = {
    Name        = "web-server-${var.environment}"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

# ✅ ALWAYS use variables for configurable values
variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

# ✅ Use locals for computed values
locals {
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}
```

#### Commands
```bash
terraform init      # Initialize providers
terraform plan      # Preview changes
terraform apply     # Apply changes
terraform destroy   # Destroy infrastructure
terraform fmt       # Format code
terraform validate  # Validate configuration
```

---

### Ansible Best Practices

#### Directory Structure
```
ansible/
├── inventory/
│   ├── production
│   └── staging
├── group_vars/
│   └── all.yml
├── host_vars/
├── roles/
│   └── webserver/
│       ├── tasks/main.yml
│       ├── handlers/main.yml
│       ├── templates/
│       └── defaults/main.yml
└── playbooks/
    └── deploy.yml
```

#### Conventions
```yaml
# ✅ Use YAML-style syntax, not key=value
- name: Install packages
  apt:
    name: "{{ item }}"
    state: present
  loop:
    - nginx
    - curl

# ✅ Always name tasks
- name: Copy configuration file  # ✅ GOOD
  copy:
    src: nginx.conf
    dest: /etc/nginx/nginx.conf

# ✅ Use handlers for service restarts
handlers:
  - name: Restart nginx
    service:
      name: nginx
      state: restarted
```

---

### Kubernetes Best Practices

#### Resource Naming
```yaml
# ✅ Use kebab-case for resource names
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: production
  labels:
    app: web-app
    environment: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
```

#### Essential Configs
```yaml
# ✅ ALWAYS set resource limits
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "500m"

# ✅ Use liveness and readiness probes
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

#### kubectl Commands
```bash
kubectl get pods -n namespace
kubectl describe pod pod-name
kubectl logs pod-name -f
kubectl apply -f manifest.yaml
kubectl delete -f manifest.yaml
kubectl rollout status deployment/name
kubectl rollout undo deployment/name
```

---

### CI/CD (GitHub Actions)

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
        with:
          version: 9
      - name: Run tests
        run: pnpm test
        
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
        with:
          version: 9
      - name: Build
        run: pnpm build
```
