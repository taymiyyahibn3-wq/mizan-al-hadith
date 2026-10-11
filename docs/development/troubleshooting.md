# MĪZĀN AL-ḤADĪTH — TROUBLESHOOTING & COMMON ISSUES

**Document Identifier:** `docs/development/troubleshooting.md`  

---

## 1. Database Connection & File Missing Errors

### Symptom: `sqlite3.OperationalError: unable to open database file`
- **Cause:** Database file not found at expected location.
- **Resolution:** Verify that `data/` directory exists and contains `hadith-kg.db`, `hadith_numbering.db`, and related databases. In `db_manager.py`, database paths resolve relative to `REPO_ROOT` or Docker `/data/`.

### Symptom: `sqlite3.OperationalError: attempt to write a readonly database`
- **Cause:** Code attempted an `INSERT` or `UPDATE` on a canonical database.
- **Resolution:** By design, canonical databases are strictly read-only. User-created data must be saved to `data/ask_mizan.db` or `data/research_workspace.db`.

---

## 2. API & Network Issues

### Symptom: Frontend Displays Network Error / "Cannot connect to server"
- **Cause:** Backend FastAPI server is not running, or listening on a different port.
- **Resolution:**
  1. Ensure FastAPI is running on `http://127.0.0.1:8000`.
  2. Verify that `mizan-web/frontend/.env.local` contains `NEXT_PUBLIC_API_URL=http://127.0.0.1:8000/api`.

### Symptom: Ask Mīzān Returns "Service Degraded" or Refusal
- **Cause:** Missing or invalid API key (`GEMINI_API_KEY`).
- **Resolution:** Check `.env` to verify your key is populated. If running offline, set `ASK_MIZAN_PROVIDER=ollama`.

---

## 3. Node.js & Memory Issues

### Symptom: `JavaScript heap out of memory` during build
- **Resolution:** Run Next.js with expanded memory:
  ```bash
  NODE_OPTIONS="--max-old-space-size=4096" npm run build
  ```
