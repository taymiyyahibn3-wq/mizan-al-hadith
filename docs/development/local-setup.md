# MĪZĀN AL-ḤADĪTH — LOCAL SETUP & QUICKSTART GUIDE

**Document Identifier:** `docs/development/local-setup.md`  
**Execution Environment:** Reproducible Developer Environment  

---

## 1. Quickstart Overview

Setting up Mīzān al-Ḥadīth consists of four primary steps:
1. Cloning the repository.
2. Installing backend dependencies and booting FastAPI.
3. Installing frontend dependencies and booting Next.js.
4. Verifying system health.

---

## 2. Step-by-Step Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/<owner>/mizan-al-hadith.git
cd mizan-al-hadith
```

### Step 2: Configure Environment Variables
Copy the template configuration files:
```bash
# Root environment (backend and bot)
cp .env.example .env

# Frontend environment
cp mizan-web/frontend/.env.example mizan-web/frontend/.env.local
```

### Step 3: Backend Setup & Startup
Navigate to the backend directory, initialize a Python virtual environment, install requirements, and start the Uvicorn ASGI server:

```bash
# Windows (PowerShell):
cd mizan-web/backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# macOS / Linux (bash/zsh):
cd mizan-web/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
The backend API will be available at: `http://127.0.0.1:8000`  
Interactive Swagger docs: `http://127.0.0.1:8000/docs`

### Step 4: Frontend Setup & Startup
In a separate terminal window, navigate to the frontend directory, install dependencies, and start the Next.js development server:

```bash
cd mizan-web/frontend
npm install
npm run dev
```
The web application will be accessible at: `http://localhost:3000`

---

## 3. Verification & Health Check

Open a terminal and verify that both subsystems are operating properly:

```bash
# Check backend health
curl http://127.0.0.1:8000/api/ask/health

# Expected response:
# {"status":"healthy","databases":{"hadith_kg":true,"numbering":true,"commentaries":true,"translations":true}}
```
Navigate to `http://localhost:3000` in your web browser. You should see the Mīzān al-Ḥadīth home page with the animated statistics counter and Sihah Sittah showcase.
