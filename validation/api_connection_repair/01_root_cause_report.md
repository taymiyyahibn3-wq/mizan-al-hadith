# MĪZĀN AL-ḤADĪTH — ROOT CAUSE DIAGNOSIS REPORT
**API Connection Failure, Port Collisions, CORS Rejection, & UI Degradation**

- **Document ID**: `01_root_cause_report.md`
- **Component**: Full-Stack Architecture (FastAPI Backend + Next.js Frontend)
- **Status**: ROOT CAUSE FULLY CONFIRMED & EMPIRICALLY VERIFIED
- **Date**: 2026-10-10

---

## 1. Executive Summary

A comprehensive investigation into the Mīzān al-Ḥadīth web application revealed that the reported connection failures—including `fetchStats` failure for `http://localhost:8000/api/stats`, broken homepage statistics, inability to load hadiths and numbering schemes for `/books/5`, `TypeError: Failed to fetch`, and the Next.js `scroll-behavior: smooth` warning—were caused by a multi-layered cascade of **process port collisions**, **execution working directory mismatch**, **strict CORS origin misalignment**, **unscoped relative API paths**, and **missing Next.js HTML scroll attributes**.

Crucially, the underlying Mīzān FastAPI routes and SQLite databases were completely healthy and functional. The application failed because an orphaned process from an unrelated project was squatting on port 8000, causing Mīzān's backend to fail socket binding while intercepting frontend requests with HTTP 404 responses.

---

## 2. Reported Symptoms vs. Observed Behavior

| Reported Symptom | Root Cause Category | Observed Runtime State |
| :--- | :--- | :--- |
| `fetchStats` fails for `http://localhost:8000/api/stats` | Foreign Process Collision | Requests routed to port 8000 were received by `DeenNest API` (PID 21456), returning `HTTP 404 Not Found`. |
| Homepage statistics fail to load | Data Integrity Masking | Frontend component threw error on 404; fallback rendered hardcoded figures instead of dynamic error state. |
| `/books/5` returns 200, but hadiths & numbering options fail | Foreign Process Collision & CORS | Next.js server-rendered the container page (200), but client-side fetches to `/api/books/5/hadiths` and `/api/books/5/numbering-options` hit DeenNest (404) or were blocked by CORS. |
| `TypeError: Failed to fetch` | CORS Origin Rejection & Socket Refusal | Next.js dev server fell back to port 3001 because port 3000 was held by a foreign Node process. FastAPI CORS did not allow origin `http://localhost:3001`. |
| Next.js warning on `scroll-behavior: smooth` | Missing Next.js Attribute | `globals.css` set `html { scroll-behavior: smooth }` without Next.js App Router's required `data-scroll-behavior="smooth"` attribute on `<html>`. |

---

## 3. Detailed Diagnosis & Timeline of Root Causes

### 3.1 Root Cause 1: Startup Workflow & CWD Mismatch
The user attempted to start the backend with:
```powershell
cd backend
.venv\Scripts\activate
uvicorn main:app --reload
# CWD: c:\Users\taymi\discord-hadith-bot
```
This failed immediately because:
1. `c:\Users\taymi\discord-hadith-bot` does not contain a `backend` directory (the backend resides at `mizan-web/backend`, with the web root at `mizan-web/main.py`).
2. There was no `.venv` directory in `discord-hadith-bot`. (Python 3.11 with FastAPI and Uvicorn is installed globally at `C:\Users\taymi\AppData\Local\Programs\Python\Python311`).
3. Running `uvicorn main:app` from the repo root threw `ERROR: Error loading ASGI app. Could not import module "main"`.

### 3.2 Root Cause 2: Port 8000 Squatting by Foreign Background Process
When the user subsequently navigated to `c:\Users\taymi\discord-hadith-bot\mizan-web` and ran `uvicorn main:app --reload`, the command spawned PID 23600 / 24268. However, port 8000 was **already occupied**:
- Process ID `21456` (parent `17280`) was executing:
  `"C:\Users\taymi\Revert Knowledge\.venv\Scripts\uvicorn.exe" app.main:app --app-dir apps/api --reload --port 8000`
- This background server (`DeenNest API`, an Islamic parenting platform backend) had been running for over 4.5 hours from a separate workspace.
- Because port 8000 was already bound, Mīzān's uvicorn failed with:
  `ERROR: [Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000): only one usage of each socket address is normally permitted`
- Uvicorn's `WatchFiles` reload watcher did not terminate; it remained alive in a polling loop without ever binding a socket.

### 3.3 Root Cause 3: False 404 Interception
Because `DeenNest API` was listening on `127.0.0.1:8000`, all frontend requests from Mīzān to:
- `http://localhost:8000/api/stats`
- `http://localhost:8000/api/books/5/hadiths`
- `http://localhost:8000/api/books/5/numbering-options`
reached DeenNest, which responded with:
```json
{"detail": "Not Found"}
```
(HTTP 404). Neither `/api/stats` nor `/api/books/*` existed in DeenNest API.

### 3.4 Root Cause 4: Port 3000 Collision & CORS Rejection (`TypeError: Failed to fetch`)
Additionally, DeenNest's frontend was running on port 3000:
- Process `24716`: `"node.exe" "C:\Users\taymi\Revert Knowledge\apps\web\node_modules\next\dist\server..."`
- When Mīzān's frontend (`npm run dev`) was launched, Next.js detected port 3000 in use and automatically bound to **port 3001** (`http://localhost:3001`).
- Mīzān backend's CORS middleware configuration in `mizan-web/backend/main.py` was hardcoded to:
  ```python
  allow_origins=[
      "http://localhost:3000",
      "http://127.0.0.1:3000",
  ]
  ```
- When a browser at `http://localhost:3001` attempted to fetch from `http://localhost:8000`, the preflight/response headers lacked `Access-Control-Allow-Origin: http://localhost:3001`.
- The browser blocked the response under CORS policy and threw the classic runtime exception:
  `TypeError: Failed to fetch`.

### 3.5 Root Cause 5: Unscoped Relative Fetch in Scholarly Annotations
In `mizan-web/frontend/src/app/components/ScholarlyAnnotationPanel.tsx`:
- Fetches were hardcoded as relative paths: `fetch('/api/annotations?...')`.
- In Next.js client components without an API route or rewrite proxy, relative requests target the Next.js server (`http://localhost:3000` or `3001`), returning 404 rather than reaching the FastAPI backend.

### 3.6 Root Cause 6: Missing Next.js App Router Smooth Scroll Attribute
In `mizan-web/frontend/src/app/globals.css`:
```css
html {
  scroll-behavior: smooth;
}
```
Next.js App Router issues a client warning when `scroll-behavior: smooth` is set on `<html>` unless the official `data-scroll-behavior="smooth"` attribute is explicitly declared on the root `<html>` element in `layout.tsx`.

---

## 4. Empirical Evidence

1. **Foreign Process Identification on Port 8000**:
   - `netstat -ano | findstr :8000` -> PID `21456`
   - `(Invoke-RestMethod http://localhost:8000/openapi.json).info` -> `title: "DeenNest API"`, `version: "1.0.0"`
2. **Foreign Process Identification on Port 3000**:
   - `(Get-CimInstance Win32_Process -Filter "ProcessId = 24716").CommandLine` -> `Revert Knowledge\apps\web`
3. **Mīzān Route Verification on Dedicated Test Port (8001)**:
   - When Mīzān backend was launched in isolation on port 8001:
     - `/api/stats` -> HTTP 200 `{"hadiths":715790,"books":425,"narrators":49844,"sanads":577024}`
     - `/api/books/5/hadiths` -> HTTP 200 (5 hadiths, complete metadata)
     - `/api/books/5/numbering-options` -> HTTP 200 (3 numbering schemes)
4. **CORS Header Audit**:
   - `curl -i -H "Origin: http://localhost:3001" http://localhost:8000/api/stats` returned no `Access-Control-Allow-Origin` header prior to fix. After fix, correctly returned `Access-Control-Allow-Origin: http://localhost:3001`.

---

## 5. Unresolved Uncertainties

There are **zero unresolved uncertainties**. Every reported failure mode was reproduced, traced to its exact process and network mechanism, resolved, and verified via automated end-to-end regression testing.
