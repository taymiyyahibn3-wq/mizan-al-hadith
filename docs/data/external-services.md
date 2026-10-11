# MĪZĀN AL-ḤADĪTH — EXTERNAL API & SERVICE REGISTER

**Document Identifier:** `docs/data/external-services.md`  
**System Baseline:** Complete Runtime Codebase & Ingestion Pipeline Audit  
**Security Standard:** Strict Zero-Secret Exposure Policy  

---

## 1. Register Overview

Mīzān al-Ḥadīth is architected to operate primarily as an offline, sovereign, and self-contained research system using local SQLite databases (`data/*.db`). However, certain advanced capabilities—specifically semantic embedding computation, generative answer synthesis in Ask Mīzān, and evaluation benchmarking—can interface with external hosted AI APIs or local offline model servers.

This document inventories every external API, hosted cloud service, and local model runtime integrated into the codebase.

```
                    +--------------------------------------------------------------+
                    |                      USER RESEARCH QUERY                     |
                    +--------------------------------------------------------------+
                                                   |
                                                   v
                    +--------------------------------------------------------------+
                    |            MĪZĀN LOCAL BACKEND (FastAPI / SQLite)            |
                    |    Deterministic Parsing -> Local Read-Only DB Retrieval    |
                    +--------------------------------------------------------------+
                                                   |
                                                   v
                    +--------------------------------------------------------------+
                    |            EXTERNAL API / MODEL PROVIDER SWITCH              |
                    |  - Google Gemini (Default Cloud Provider)                    |
                    |  - OpenAI GPT (Opt-in Provider)                              |
                    |  - Anthropic Claude (Opt-in Provider)                        |
                    |  - Ollama (100% Local Sovereign Offline LLM)                 |
                    +--------------------------------------------------------------+
```

---

## 2. External Services Inventory Table

| Service ID | Provider & Documentation | Model / Service Identifier | Configuration Path | Data Payload Sent | Credentials Required | Runtime vs. Offline | Rate Limits & Cost | Privacy & Retention Considerations |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `srv-gemini-synth` | **Google Cloud / AI Studio**<br>[ai.google.dev](https://ai.google.dev) | `gemini-1.5-flash`<br>`gemini-1.5-pro` | `mizan-web/backend/ask_mizan/config.py`<br>`mizan-web/backend/ask_mizan/providers/gemini.py` | Sanitized user question + assembled evidence pack (hadith matn, isnad, grading, commentary). | `GEMINI_API_KEY` or `GOOGLE_API_KEY` | Runtime (Optional) | Free tier: 15 RPM / 1M TPM. Paid tier: standard Google pricing. | No customer data used to train models on paid tier. Zero IP addresses or user accounts transmitted. |
| `srv-gemini-embed` | **Google Cloud / AI Studio**<br>[ai.google.dev](https://ai.google.dev) | `gemini-embedding-001`<br>`text-embedding-004` | `mizan-web/backend/ask_mizan/semantic.py` | Hadith matn strings and semantic meaning group definitions. | `GEMINI_API_KEY` | Offline Data Preparation & Runtime Hybrid Search | Paid / Free API tier depending on key tier. | Used offline to generate 20,744 768d vectors stored in `data/derived_semantic_index.db`. |
| `srv-openai-synth` | **OpenAI**<br>[platform.openai.com](https://platform.openai.com) | `gpt-4o`<br>`gpt-4o-mini` | `mizan-web/backend/ask_mizan/config.py`<br>`mizan-web/backend/ask_mizan/providers/openai.py` | Sanitized research question + assembled evidence pack. | `OPENAI_API_KEY` | Runtime (Opt-in via `ASK_MIZAN_PROVIDER=openai`) | Standard OpenAI API pay-per-token rates. | Subject to OpenAI enterprise API terms (zero data retention for training). |
| `srv-anthropic-synth` | **Anthropic**<br>[docs.anthropic.com](https://docs.anthropic.com) | `claude-3-5-sonnet-20241022`<br>`claude-3-haiku` | `mizan-web/backend/ask_mizan/config.py`<br>`mizan-web/backend/ask_mizan/providers/anthropic.py` | Sanitized research question + assembled evidence pack. | `ANTHROPIC_API_KEY` | Runtime (Opt-in via `ASK_MIZAN_PROVIDER=anthropic`) | Standard Anthropic API pay-per-token rates. | Commercial API data is not retained for training. |
| `srv-ollama-local` | **Ollama Local Runtime**<br>[ollama.com](https://ollama.com) | `qwen2.5:7b`<br>`llama3.1:8b`<br>`mistral` | `mizan-web/backend/ask_mizan/config.py`<br>`mizan-web/backend/ask_mizan/providers/ollama.py` | Formatted prompt via HTTP POST to `http://localhost:11434/api/generate`. | **None** (100% Local) | Runtime (Opt-in via `ASK_MIZAN_PROVIDER=ollama`) | Unlimited local compute (Hardware dependent). Zero financial cost. | **Maximum Sovereignty:** Zero data leaves the local computer or local network. |
| `srv-huggingface-hub` | **Hugging Face**<br>[huggingface.co](https://huggingface.co) | Model weight hub (`google/embeddinggemma-2`) | `mizan-web/backend/ask_mizan/embeddinggemma_store.py` | Model weight downloads during build/setup. | Optional `HF_TOKEN` | Setup / Offline evaluation | Free community download bandwidth. | Public model weights download only. |

---

## 3. Configuration & Security Protocols

### 3.1 Strict Zero-Secret Principle
- No API keys, passwords, or personal credentials are hardcoded in any file tracked by Git.
- Credentials must be supplied via local environment variables or `.env` files (which are strictly excluded by `.gitignore`).
- The test suites automatically mock external API calls or skip external network invocations if keys are absent.

### 3.2 Offline Graceful Fallback
- If no external API key is configured and Ollama is not active, the Mīzān platform continues to operate all core functionality:
  - Canonical library browsing across 715k hadiths.
  - Isnād topological graph generation across 49.8k scholars.
  - Arabic and English full-text search (FTS5).
  - Multi-edition numbering concordance lookups.
  - Research workspace bookmarking, notes, and matrix exports.
  - Classical scholar evaluations and commentary readings.
- The Ask Mīzān engine informs the user when external generative synthesis is unconfigured, allowing deterministic evidence retrieval without external model invocation.
