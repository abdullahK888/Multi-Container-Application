# Multi-Container Application with CI/CD Pipeline

A production-style multi-container Flask application with Nginx reverse proxy,
PostgreSQL database, automated CI/CD pipeline, security scanning, static code
analysis, and Kubernetes orchestration.

## 🏗 Architecture

```
Browser → Nginx (port 80) → Flask + Gunicorn (port 5000) → PostgreSQL
```

All containerized and deployed to Kubernetes, with the full pipeline triggered
automatically on every GitHub push via Jenkins.

## 🔧 Tech Stack

- **Backend:** Python Flask + Gunicorn (WSGI)
- **Database:** PostgreSQL
- **Reverse Proxy:** Nginx
- **Containerization:** Docker
- **Orchestration:** Kubernetes (Minikube)
- **CI/CD:** Jenkins
- **Security Scanning:** Trivy (filesystem + image)
- **Code Quality:** SonarQube + Quality Gate
- **Authentication:** JWT
- **Secret Management:** Environment variables (.env)

## 🚀 CI/CD Pipeline Stages

1. ✅ Checkout — Pull latest code from GitHub
2. ✅ File Scan — Trivy filesystem vulnerability scan on source code
3. ✅ Build Image — Docker image build (tagged with build number)
4. ✅ Image Scan — Trivy image vulnerability scan on built container
5. ✅ SonarQube Analysis — Static code analysis on backend source
6. ✅ Quality Gate — Pipeline aborts if code quality standards not met
7. ✅ Deploy to Kubernetes — Rolling update via kubectl (ConfigMap, Deployment, Service)

## ⚙️ Kubernetes Setup

Manifests are located in the `k8s/` directory:

```
k8s/
├── configmap.yaml      # Environment config for the app
├── deployment.yaml     # Backend deployment (imagePullPolicy: Never)
└── service.yaml        # Service exposing the backend
```

The pipeline applies all manifests on every run and performs a rolling update
with `kubectl rollout status` to verify the deployment succeeded. On failure,
diagnostics are automatically collected (pod status, describe, logs).

> **Note:** `imagePullPolicy: Never` is set because Jenkins and Minikube run
> separate Docker daemons. Images are built in Jenkins' daemon and do not exist
> in a remote registry — Kubernetes must use the locally available image only.

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
SECRET_KEY=
ADMIN_PASSWORD=
```

## 📡 API Endpoints

| Method | Endpoint  | Description                  |
|--------|-----------|------------------------------|
| GET    | /         | App status                   |
| GET    | /health   | Health check                 |
| GET    | /ready    | Readiness probe              |
| POST   | /login    | User authentication (JWT)    |

## 🚧 Coming Soon

- Prometheus metrics collection
- Grafana dashboards and alerting
- Full observability on the running Kubernetes cluster
