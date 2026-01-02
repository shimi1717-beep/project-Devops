# QuakeWatch — Minimal Flask + Docker

A tiny Python Flask app that returns **"Hello, World! QuakeWatch is online."** at `/` and a `/healthz` endpoint.

---

## 1) Prerequisites
- Docker Engine + Docker Compose plugin
- Docker Hub account (to push the image)

Verify:
```bash
docker --version
docker compose version
```

---

## 2) Run locally with Docker Compose (recommended)
From the project root:
```bash
# Optionally export your Docker Hub username for the compose image tag
export DOCKERHUB_USER=<your-dockerhub-username>

docker compose up --build -d
docker compose ps
```
Open: http://localhost:5000

Stop & clean up:
```bash
docker compose down
```

---

## 3) Build, tag, and push with plain Docker
```bash
# Build
docker build -t quakewatch:local .

# Tag for Docker Hub
docker tag quakewatch:local <your-dockerhub-username>/quakewatch:latest

# Login & push
docker login
docker push <your-dockerhub-username>/quakewatch:latest
```

### Run the pushed image
```bash
docker run -d --name quakewatch -p 5000:5000 <your-dockerhub-username>/quakewatch:latest
# Test:
curl http://localhost:5000/
curl http://localhost:5000/healthz
```

---

## 4) Using Docker volumes (persistent storage)
The app doesn't need persistence, but here's an example for logs/data.
Add a volume to `docker-compose.yml` under the service:
```yaml
services:
  quakewatch:
    # ...
    volumes:
      - qw_logs:/var/log/quakewatch
volumes:
  qw_logs:
```

Or with `docker run`:
```bash
docker run -d --name quakewatch -p 5000:5000           -v qw_logs:/var/log/quakewatch           <your-dockerhub-username>/quakewatch:latest
```

---

## 5) Troubleshooting
```bash
docker compose logs -f
docker logs quakewatch
docker ps
docker images
```

---

## 6) Project Structure
```
.
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
└── README.md
```
