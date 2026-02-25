# Multi-Container Application

A production-ready multi-container Flask application with Nginx reverse proxy, 
PostgreSQL database, and Docker Compose orchestration.

## Tech Stack
- **Backend:** Python Flask + Gunicorn
- **Database:** PostgreSQL
- **Reverse Proxy:** Nginx
- **Containerization:** Docker + Docker Compose
- **CI/CD:** Jenkins (coming soon)
- **Monitoring:** Grafana + Prometheus (coming soon)

## Architecture
Browser → Nginx (port 80) → Flask App (port 5000) → PostgreSQL

## How To Run Locally
git clone https://github.com/abdullahK888/Multi-Container-Application
cd Multi-Container-Application
docker compose up --build

## API Endpoints
- GET /          → App status
- GET /health    → Health check
- POST /login    → User authentication

## Pipeline (Coming Soon)
- Jenkins CI/CD pipeline
- Trivy security scanning
- SonarQube code quality
- Kubernetes deployment via Minikube
- Grafana monitoring dashboard
