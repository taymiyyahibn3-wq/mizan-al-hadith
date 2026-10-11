# MĪZĀN AL-ḤADĪTH — ENVIRONMENT CONFIGURATION

**Document Identifier:** `docs/development/environment-configuration.md`  

---

## 1. Environment Files Summary

Mīzān al-Ḥadīth utilizes two decoupled configuration files:
1. `/.env` — Backend and AI provider credentials (server-side only, never bundled in client code).
2. `/mizan-web/frontend/.env.local` — Frontend configuration variables.

---

## 2. Server Configuration Variables (`/.env`)

| Variable Name | Required | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `ENVIRONMENT` | No | `development` | Environment mode (`development`, `staging`, `production`). |
| `HOST` | No | `127.0.0.1` | ASGI server listening host. |
| `PORT` | No | `8000` | ASGI server listening port. |
| `GEMINI_API_KEY` | Optional | `""` | Google Gemini API key for Ask Mīzān online synthesis. |
| `OPENAI_API_KEY` | Optional | `""` | OpenAI API key for alternative LLM synthesis. |
| `ANTHROPIC_API_KEY` | Optional | `""` | Anthropic Claude API key for alternative LLM synthesis. |
| `OLLAMA_BASE_URL` | Optional | `http://localhost:11434` | Endpoint for local offline Ollama models. |
| `ASK_MIZAN_PROVIDER` | No | `gemini` | Active LLM adapter (`gemini`, `openai`, `anthropic`, `ollama`). |
| `ASK_MIZAN_TEMPERATURE`| No | `0.1` | Sampling temperature (low temperature enforces factual grounding). |
| `ASK_MIZAN_MAX_TOKENS` | No | `2048` | Maximum response tokens generated. |
| `SEMANTIC_EMBEDDING_PROVIDER`| No | `gemini` | Embedding vector provider (`gemini`, `embeddinggemma`). |

---

## 3. Frontend Configuration Variables (`/mizan-web/frontend/.env.local`)

| Variable Name | Required | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | Yes | `http://127.0.0.1:8000/api` | Public base URL for the FastAPI backend service. In production, set to your domain or reverse proxy. |
