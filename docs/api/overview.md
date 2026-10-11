# MĪZĀN AL-ḤADĪTH — REST API OVERVIEW

**Document Identifier:** `docs/api/overview.md`  
**Base URL:** `http://127.0.0.1:8000/api` (or environment-configured `NEXT_PUBLIC_API_URL`)  
**Specification Standard:** OpenAPI 3.1.0  
**Endpoint Total:** 95 Verified Registered REST Endpoints  

---

## 1. API Architecture & Standards

The Mīzān al-Ḥadīth backend exposes a high-performance, asynchronous REST API powered by FastAPI.
- **Protocol:** HTTP/1.1 and HTTP/2 supported via ASGI.
- **Data Exchange:** Strict JSON for request bodies and response payloads.
- **Encoding:** UTF-8 mandatory for all textual endpoints to support full Arabic script and diacritics.
- **Idempotency:** All `GET`, `PUT`, and `DELETE` endpoints follow standard HTTP idempotent semantics.
- **Read-Only Guarantees:** Public corpus query endpoints never mutate server state.

---

## 2. Interactive API Documentation

When the backend server is running locally:
- **Interactive Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc Interactive Reference:** `http://127.0.0.1:8000/redoc`
- **Raw OpenAPI 3.1 Schema:** `http://127.0.0.1:8000/openapi.json`

---

## 3. High-Level Endpoint Categories

```
+-----------------------------------------------------------------------------------+
|                        MĪZĀN API SUBSYSTEM CATEGORIES                             |
+-----------------------------------------------------------------------------------+
|  1. System Health & Telemetry          GET  /api/health                           |
|                                        GET  /api/stats                            |
|                                                                                   |
|  2. Canonical Hadith Library           GET  /api/books                            |
|                                        GET  /api/books/{id}                       |
|                                        GET  /api/hadith/{id}                      |
|                                        GET  /api/hadith/{id}/grades               |
|                                        GET  /api/hadith/{id}/commentaries         |
|                                        GET  /api/hadith/{id}/translations         |
|                                                                                   |
|  3. Multi-Modal Search & Concordance   GET  /api/search                           |
|                                        GET  /api/numbering/resolve                |
|                                        GET  /api/hadith/{id}/crosswalk            |
|                                                                                   |
|  4. Biographical Narrators (Rijāl)     GET  /api/narrators                        |
|                                        GET  /api/narrator/{id}                    |
|                                        GET  /api/narrator/{id}/aqwal              |
|                                        GET  /api/narrator/{id}/network            |
|                                                                                   |
|  5. Isnād Topology Graphs              GET  /api/isnad/{id}                       |
|                                        GET  /api/isnad/stats                      |
|                                                                                   |
|  6. Ask Mīzān Assistant                POST /api/ask                              |
|                                        POST /api/ask/stream                       |
|                                        GET  /api/ask/conversations/{id}           |
|                                        POST /api/ask/feedback                     |
|                                                                                   |
|  7. Scholarly Research Workspace       25 Endpoints under /api/workspace/*        |
+-----------------------------------------------------------------------------------+
```
