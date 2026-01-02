# DevOps Project – Shimi Lieberman  
End-to-end DevOps mini-platform including Docker, Kubernetes, Helm, Git workflows, and CI/CD preparation.

---

## Overview

This repository demonstrates a complete DevOps workflow implemented across three major phases:

### **Phase 1 – Application & Dockerization**
- Developed a Flask-based Python application (`app.py`)
- Built and tested the Docker image using a `Dockerfile`
- Ran the application locally in Docker

### **Phase 2 – Kubernetes Deployment**
- Wrote Deployment & Service manifests
- Deployed application into **Minikube**
- Added `/healthz` endpoint for Kubernetes probes
- Verified pod logs, liveness, readiness, and service behavior

### **Phase 3 – Automation (Helm + Git Workflows)**
- Packaged the application as a **Helm chart**
- Deployed via Helm (`helm upgrade --install devops-demo`)
- Fixed service selectors & validated Service → Pod connectivity
- Implemented a real multi-branch Git workflow:
  - `main`, `develop`, and `feature/*`
  - Pull Request simulation
  - Merge conflict creation & resolution

---

## 🏗 Project Structure

project-Devops/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
│
├── helm/
│ └── devops-demo/
│ ├── Chart.yaml
│ ├── values.yaml
│ └── templates/
│ ├── deployment.yaml
│ ├── service.yaml
│ └── _helpers.tpl
│
└── README.md


---

# Phase 1 – Docker Build

Build Docker image inside Minikube’s Docker daemon:

```bash
eval $(minikube docker-env)
docker build -t shimi/devops-demo-app:latest .
Run locally (optional):

bash
Copy code
docker run -p 5000:5000 shimi/devops-demo-app:latest
☸ Phase 2 – Kubernetes Deployment
Deploy manually (early phase):

bash
Copy code
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
View resources:

bash
Copy code
kubectl get pods,svc
kubectl logs <pod>
kubectl describe pod <pod>

Phase 3 – Helm Deployment
Install or upgrade the Helm release:

bash
Copy code
helm upgrade --install devops-demo ./helm/devops-demo
Check everything is running:

bash
Copy code
kubectl get deploy,po,svc
kubectl get endpoints devops-demo
Access the application:

bash
Copy code
kubectl port-forward svc/devops-demo 8081:80
Test:

bash
Copy code
curl http://localhost:8081/
curl http://localhost:8081/healthz
Expected:

csharp
Copy code
Hello, World! Phase3 is online.
{"status":"ok"}

Git Workflow Demonstration (Task 2)
Branching Strategy
css
Copy code
main      → production-ready code  
develop   → integration branch  
feature/* → isolated development  

Commands Used
Initial Setup
bash
Copy code
git init
git add .
git commit -m "Initial commit – Phase 1–3"
git branch -M main
git remote add origin <repo-url>
git push -u origin main
Create develop branch
bash
Copy code
git checkout -b develop
git push -u origin develop
Create a feature branch (example)
bash
Copy code
git checkout -b feature/add-version-endpoint
# edit app.py
git add app.py
git commit -m "Add /version endpoint"
git push -u origin feature/add-version-endpoint
Open a Pull Request → Merge into develop.

Demonstrate Merge Conflict
Feature branch:
bash
Copy code
git checkout -b feature/change-message

# edit app.py
git commit -m "Change greeting"
git push
Conflicting change in develop:
bash
Copy code
git checkout develop

# edit same line differently
git commit -m "Different greeting update"
git push
Trigger conflict:
bash
Copy code
git checkout feature/change-message
git merge develop

Resolve the conflict:
bash
Copy code
git add app.py
git commit -m "Resolve merge conflict"
git push

Validation Commands
bash
Copy code
kubectl get deploy
kubectl get endpoints devops-demo
kubectl logs devops-demo-<pod>
kubectl describe svc devops-demo

Next Phase (Phase 4 – CI/CD with Jenkins)
Prepared tasks include:

Jenkinsfile creation

Docker build stage

Unit test stage

Helm deployment stage

Smoke test stage (curl /healthz)

Author
Shimi Lieberman
Senior Network & Cloud Engineer | DevOps Practitioner

