# NCAP — Native Cloud API Platform

Self-hosted, cloud-native API management platform built end-to-end — FastAPI microservices, Kong gateway, Kubernetes, GitOps CI/CD, full observability stack.

## Architecture

Monorepository of microservices behind a Kong gateway, and deployed on Kubernetes via GitOps

| Phase | Scope | Status |
|-------|-------|--------|
| 1. Foundations | FastAPI service, tests, Dockerfile, docker-compose | In progress |
| 2. Kubernetes | kind cluster, Helm chart, probes, HPA | Not started |
| 3. Gateway | Kong on Kubernetes, routing, auth & rate-limiting plugins | Not started |
| 4. CI/CD | GitLab CI pipeline: lint, tests, build, Trivy scan, registry push | Not started |
| 5. GitOps | Argo CD, app-of-apps structure, automated sync | Not started |
| 6. Security & secrets | Vault, OAuth2 on the gateway, end-to-end TLS | Not started |
| 7. Observability | Prometheus, Grafana dashboards, alerting | Not started |
| 8. Bonus | Terraform provisioning to AKS, chaos testing | Not started |

## Quick start

Requires Docker Desktop.

    git clone https://github.com/Teakt/ncap.git
    cd ncap
    docker compose up --build

The API is available at http://localhost:8000/health.
Interactive OpenAPI docs: http://localhost:8000/docs.

## Tech Stack

- Python - FastAPI, backend
- Docker - containers, for creating prod image
- Kubernetes - Docker containers orchestration
- Kong - For the API gateway
- Argo CD - for the GitOps application and deployment
- Helm - packaging
- GitLab CI - for build, tests, push, versioning
- HashiCorp Vault - secrets
- Prometheus + Grafana - Metrics and monitoring
- OAuth2/OIDC - Auth method 