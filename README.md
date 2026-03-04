# Multi-Container Application with CI/CD Pipeline

A production-style multi-container Flask application with Nginx reverse proxy,
PostgreSQL database, automated CI/CD pipeline, and security scanning.

## 🏗 Architecture
Browser → Nginx (port 80) → Flask + Gunicorn (port 5000) → PostgreSQL

## 🔧 Tech Stack
- **Backend:** Python Flask + Gunicorn (WSGI)
- **Database:** PostgreSQL
- **Reverse Proxy:** Nginx
- **Containerization:** Docker + Docker Compose
- **CI/CD:** Jenkins
- **Security Scanning:** Trivy
- **Authentication:** JWT
- **Secret Management:** Environment variables (.env)

## 🚀 CI/CD Pipeline Stages
1. ✅ Checkout — Pull latest code from GitHub
2. ✅ File Scan — Trivy filesystem vulnerability scan
3. ✅ Build Image — Docker image build
4. ✅ Image Scan — Trivy image vulnerability scan
5. ✅ Deploy — Docker Compose deployment (3 containers)

## 🏃 Run Locally
git clone https://github.com/abdullahK888/Multi-Container-Application
cd Multi-Container-Application
cp .env.example .env  # Add your values
docker compose up -d --build

## 🔐 Environment Variables
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=
SECRET_KEY=
ADMIN_PASSWORD=

## 📡 API Endpoints
- GET  /        → App status
- GET  /health  → Health check
- GET  /ready   → Readiness probe
- POST /login   → User authentication (JWT)

## 🚧 Coming Soon
- SonarQube code quality analysis
- Kubernetes deployment (Minikube)
- Prometheus + Grafana monitoring
