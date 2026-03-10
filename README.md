# Multi-Container Application with CI/CD Pipeline

A production-style multi-container Flask application with Nginx reverse proxy, PostgreSQL database, automated CI/CD pipeline, security scanning, static code analysis, Kubernetes orchestration, and full observability with Prometheus & Grafana.

## 🏗 Architecture

```
Browser → Nginx (port 80) → Flask + Gunicorn (port 5000) → PostgreSQL
```

All containerized and deployed to Kubernetes, with the full pipeline triggered automatically on every GitHub push via Jenkins. Metrics are collected by Prometheus and visualized in Grafana dashboards.

## 🔧 Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python Flask + Gunicorn (WSGI) |
| **Database** | PostgreSQL |
| **Reverse Proxy** | Nginx |
| **Containerization** | Docker + Docker Compose |
| **Orchestration** | Kubernetes (Minikube) |
| **CI/CD** | Jenkins |
| **Security Scanning** | Trivy (filesystem + image) |
| **Code Quality** | SonarQube + Quality Gate |
| **Monitoring** | Prometheus + Grafana (via Helm) |
| **Authentication** | JWT |
| **Secret Management** | Environment variables (.env) |
| **Cloud Environment** | GitHub Codespaces (powered by Microsoft Azure) |

## 🚀 CI/CD Pipeline Stages

```
Checkout → File Scan → Build Image → Image Scan → SonarQube → Quality Gate → Deploy to Kubernetes
```

| Stage | Tool | Description |
|-------|------|-------------|
| 1. Checkout | Git | Pull latest code from GitHub |
| 2. File Scan | Trivy | Filesystem vulnerability scan on source code |
| 3. Build Image | Docker | Build and tag image with build number |
| 4. Image Scan | Trivy | Container image vulnerability scan |
| 5. SonarQube Analysis | SonarQube | Static code analysis on backend source |
| 6. Quality Gate | SonarQube | Pipeline aborts if code quality standards not met |
| 7. Deploy to Kubernetes | kubectl | Rolling update via ConfigMap, Deployment, Service |

## ⚙️ Kubernetes Setup

Manifests are located in the `k8s/` directory:

```
k8s/
├── configmap.yaml      # Environment config for the app
├── deployment.yaml     # Backend deployment (imagePullPolicy: Never)
└── service.yaml        # NodePort service exposing the backend
```

The pipeline applies all manifests on every run and performs a rolling update with `kubectl rollout status` to verify the deployment succeeded.

> **Note:** `imagePullPolicy: Never` is set because Jenkins and Minikube run separate Docker daemons. Images are built in Jenkins' daemon and must be loaded into Minikube manually via `minikube image load`.

## 📊 Monitoring Stack

Prometheus and Grafana are deployed inside the Kubernetes cluster via Helm:

```bash
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

This installs the full observability stack:

- **Prometheus** — scrapes metrics from all pods every 15 seconds
- **Grafana** — visualizes metrics with pre-built Kubernetes dashboards
- **Alertmanager** — handles alerts and notifications

### Accessing Grafana

```bash
export POD_NAME=$(kubectl --namespace monitoring get pod \
  -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=monitoring" -oname)
kubectl --namespace monitoring port-forward $POD_NAME 3000
```

Open port **3000** and login with:
- Username: `admin`
- Password: `kubectl get secret --namespace monitoring monitoring-grafana -o jsonpath="{.data.admin-password}" | base64 --decode`

### Available Dashboards

- **Kubernetes / Compute Resources / Cluster** — cluster-wide CPU & memory
- **Kubernetes / Compute Resources / Pod** — per-pod metrics
- **Kubernetes / Nodes** — node-level metrics

## 🏃 Run Locally with Docker

```bash
git clone https://github.com/abdullahK888/Multi-Container-Application
cd Multi-Container-Application
cp .env.example .env  # Add your values
docker compose up -d --build
```

## 🔐 Environment Variables

```
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=
DB_PORT=
APP_PORT=
SECRET_KEY=
ADMIN_PASSWORD=
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | App status |
| GET | /health | Health check |
| GET | /ready | Readiness probe |
| POST | /login | User authentication (JWT) |

## ☁️ Cloud & Next Steps

This entire project was built and run on **GitHub Codespaces** — a cloud-based development environment powered by **Microsoft Azure**. This means the project already runs in the cloud!

The natural next step is deploying to **Azure Kubernetes Service (AKS)** for a fully managed production cluster — the same Kubernetes manifests and Jenkins pipeline work with zero changes, just pointed at a cloud cluster instead of Minikube.

## 📁 Project Structure

```
Multi-Container-Application/
├── backend_project/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container
├── nginx_project/
│   └── nginx.conf          # Nginx reverse proxy config
├── k8s/
│   ├── configmap.yaml      # Kubernetes ConfigMap
│   ├── deployment.yaml     # Kubernetes Deployment
│   └── service.yaml        # Kubernetes Service
├── docker-compose.yml      # Local development orchestration
├── Jenkinsfile             # CI/CD pipeline definition
└── README.md
```
