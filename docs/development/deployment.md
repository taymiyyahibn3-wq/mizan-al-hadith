# MĪZĀN AL-ḤADĪTH — DEPLOYMENT & PRODUCTION TOPOLOGIES

**Document Identifier:** `docs/development/deployment.md`  

---

## 1. Deployment Topologies

Mīzān al-Ḥadīth supports three production deployment architectures:

```
TOPOLOGY A: Unified Virtual Machine / Dedicated Host (Nginx Reverse Proxy)
[ Clients ] ---> [ Nginx Proxy ] ---> [ Next.js :3000 ]
                                  ---> [ Uvicorn :8000 ] ---> [ Local SQLite /data ]

TOPOLOGY B: Decoupled Cloud Hosting (Vercel + Cloud Run / Docker)
[ Clients ] ---> [ Vercel (Next.js) ] ---> [ Cloud Run (FastAPI + GCS/Volume) ]

TOPOLOGY C: Static Documentation & Interactive Visualizers (GitHub Pages)
[ Clients ] ---> [ GitHub Pages (https://<user>.github.io/<repo>/) ]
```

---

## 2. Docker Containerization

The backend repository includes a production Dockerfile (`mizan-web/backend/Dockerfile`):

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

To run with data mounted:
```bash
docker build -t mizan-backend mizan-web/backend
docker run -d -p 8000:8000 -v /path/to/data:/data mizan-backend
```

---

## 3. GitHub Pages Deployment for Documentation

The static documentation portal and interactive visualization engine in `docs/` can be deployed directly to GitHub Pages:
1. In repository settings: **Settings → Pages**.
2. Source: **Deploy from a branch**.
3. Branch: `main` or `master`, Folder: `/docs`.
4. The interactive documentation website is immediately live without external database dependencies.
