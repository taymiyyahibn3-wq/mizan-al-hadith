# MĪZĀN AL-ḤADĪTH — API AUTHENTICATION & ERROR HANDLING

**Document Identifier:** `docs/api/authentication-and-errors.md`  
**Specification Standard:** RFC 7807 (Problem Details for HTTP APIs)  

---

## 1. Authentication & Identity Models

### 1.1 Public Corpus Queries
All public read endpoints (Hadith text, isnāds, narrators, commentaries, crosswalks, translations, search) are **unauthenticated and open for academic research**:
- No API keys or tokens required for read access.
- Read operations connect via SQLite URI `mode=ro` (read-only).

### 1.2 Scholarly Research Workspace Identity (`/api/workspace/*`)
The Research Workspace supports isolated multi-researcher sessions using header-driven identity:
- **Header:** `X-Researcher-Id` (e.g., `X-Researcher-Id: researcher_fatima`)
- **Default Fallback:** If omitted in local development, defaults safely to `default_researcher`.
- **Sanitization:** Alphanumeric, underscores, and hyphens only (`[a-zA-Z0-9_\-]`).
- **Isolation:** Row-level authorization enforces that researchers can only inspect, mutate, or export their own projects.

### 1.3 LLM Provider Authentication (Ask Mīzān Engine)
The backend service securely reads upstream LLM keys from environment variables (never exposed to frontend clients):
- `GEMINI_API_KEY` or `GOOGLE_API_KEY` (Google Gemini)
- `OPENAI_API_KEY` (OpenAI GPT-4o-mini)
- `ANTHROPIC_API_KEY` (Anthropic Claude)
- `OLLAMA_BASE_URL` (Local Ollama instances, e.g. `http://localhost:11434`)

---

## 2. Standard Error Format (RFC 7807)

All error responses return standard JSON structures with descriptive fields:

```json
{
  "detail": "Canonical Hadith #999999 could not be resolved in the protected KG."
}
```

For validation errors (`422 Unprocessable Entity`):
```json
{
  "detail": [
    {
      "loc": ["body", "query"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## 3. Standard HTTP Status Codes

| Status Code | Reason | Subsystem Context |
| :--- | :--- | :--- |
| **`200 OK`** | Successful retrieval | Normal query response |
| **`201 Created`** | Successful resource creation | New workspace project, note, or claim created |
| **`400 Bad Request`** | Malformed parameters | Invalid filter options or malformed identifiers |
| **`404 Not Found`** | Resource missing | Hadith ID or Narrator ID not in database |
| **`409 Conflict`** | Duplicate resource blocked | Attempting to bookmark an already bookmarked hadith in evidence library |
| **`422 Unprocessable`** | Schema validation failed | Missing required Pydantic body fields or type mismatch |
| **`429 Too Many Req`**| Rate limit exceeded | Exceeding 30 requests/minute on `/api/ask` |
| **`500 Internal Error`**| Unhandled server exception | Database handle failure or unexpected exception |
