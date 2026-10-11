# MĪZĀN AL-ḤADĪTH — ENVIRONMENT CONFIGURATION GUIDE
**Development & Production Architecture Specification**

- **Document ID**: `04_environment_configuration.md`
- **Scope**: Frontend Environment Variables, Backend CORS Configuration, Production Deployment
- **Status**: APPROVED
- **Date**: 2026-10-10

---

## 1. Environment Variable Architecture

Mīzān al-Ḥadīth uses standard Next.js environment configuration conventions:

- **Client-Exposed Variables**: Prefixed with `NEXT_PUBLIC_`. Inlined into client JavaScript bundles at build time.
- **Backend Environment Variables**: Read at runtime by FastAPI via standard `os.getenv()`.
- **Secret Hygiene**: No database credentials, API keys, or JWT secrets are exposed through `NEXT_PUBLIC_*` variables.

---

## 2. Frontend Configuration (`.env.local` / `.env.production`)

### 2.1 Local Development Configuration
File: `mizan-web/frontend/.env.local`
```bash
# Point to local FastAPI instance
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000/api
```

> [!IMPORTANT]
> **API Prefix Requirement**: The value of `NEXT_PUBLIC_API_URL` MUST end with `/api`.
> All backend routes in FastAPI are declared with the `/api` prefix (e.g. `/api/stats`, `/api/books`, `/api/hadith/*`).
> The frontend client (`src/lib/api.ts`) strips any trailing slashes and constructs endpoints as `${baseUrl}/stats` -> `http://127.0.0.1:8000/api/stats`.

### 2.2 Production Deployment Configuration
File: `mizan-web/frontend/.env.production`
```bash
# Production API endpoint (must use HTTPS, never localhost)
NEXT_PUBLIC_API_URL=https://api.mizan.islamicstudies.org/api
```

---

## 3. Backend CORS Configuration (`backend/main.py`)

The FastAPI application enforces strict origin validation with credential support:

```python
cors_env = os.getenv("CORS_ALLOWED_ORIGINS")
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]
if cors_env:
    for o in cors_env.split(","):
        clean_origin = o.strip()
        if clean_origin and clean_origin not in allowed_origins:
            allowed_origins.append(clean_origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3.1 Production Environment Variables for Backend
Set in production container or system environment:
```bash
# Comma-separated list of trusted production frontend origins
CORS_ALLOWED_ORIGINS="https://mizan.islamicstudies.org,https://www.mizan.islamicstudies.org"
```

> [!WARNING]
> Never set `allow_origins=["*"]` when `allow_credentials=True` is enabled, as browsers will reject credentialed CORS responses with wildcards.

---

## 4. Hostname Alignment in `src/lib/api.ts`

To guarantee seamless operation across loopback interfaces (`localhost` vs `127.0.0.1`):
1. In the browser (`typeof window !== 'undefined'`), `getApiBaseUrl()` inspects `window.location.hostname`.
2. If accessing via `http://localhost:3000`, the hostname is dynamically aligned to `http://localhost:8000/api`.
3. If accessing via `http://127.0.0.1:3000`, the hostname is aligned to `http://127.0.0.1:8000/api`.
4. Both origins are explicitly registered in the backend CORS whitelist.
5. In Node.js SSR environments, the explicit `NEXT_PUBLIC_API_URL` value is preserved.

---

## 5. Multi-Project Port Conflict Prevention

When running multiple local applications concurrently (e.g. DeenNest and Mīzān):
- Default Mīzān ports: **Frontend = 3000, Backend = 8000**.
- Default DeenNest ports: **Frontend = 3000, Backend = 8000**.
- **Rule**: If developing on another project simultaneously, assign distinct ports to prevent socket collisions:
  ```powershell
  # Example running Mīzān on port 8080:
  python -m uvicorn main:app --host 127.0.0.1 --port 8080 --reload
  # With corresponding frontend config:
  # NEXT_PUBLIC_API_URL=http://127.0.0.1:8080/api
  ```
