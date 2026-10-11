# MĪZĀN AL-ḤADĪTH — BACKEND ARCHITECTURE

**Document Identifier:** `docs/architecture/backend-architecture.md`  
**Subsystem Directory:** `mizan-web/backend`  
**Framework:** FastAPI 0.141.1 · Uvicorn 0.53.0 · Pydantic 2.13.5  

---

## 1. Application Architecture & Entry Point

The Mīzān backend is an asynchronous Python application rooted in `mizan-web/backend/main.py`. It integrates domain-specific routers, centralized database handle management, identity resolution, hybrid retrieval, and AI synthesis.

```
mizan-web/backend/
├── main.py                                    # FastAPI application factory, middleware & route registration
├── db_manager.py                              # Centralized connection lifecycle manager (ConnectionTracker, mode=ro)
├── identity_resolution.py                     # Deterministic alias & scholar disambiguation
├── reference_resolver.py                      # Multi-edition hadith reference & concordance parser
├── scholarly_service.py                       # Canonical grading, takhrij & commentary retrieval
├── scholarly_annotations.py                   # Author remarks & historical evaluation extraction
├── sanad_aligner.py                           # Isnād sequence alignment and narrator link matching
├── build_isnad_network.py                     # Topological graph compilation scripts
├── research_workspace.py                      # Scholarly Research Workspace router & persistence engine
│
└── ask_mizan/                                 # Ask Mīzān Subsystem
    ├── router.py                              # /api/ask, /api/ask/stream, /api/ask/feedback routes
    ├── engine.py                              # Multi-turn query coordinator & evidence pack builder
    ├── parser.py                              # Intent classification & query parsing
    ├── hybrid_service.py                      # Hybrid retrieval orchestrator
    ├── hybrid_retrieval.py                    # Lexical BM25 + Exact match + Semantic fusion
    ├── validator.py                           # Anti-hallucination citation verification engine
    ├── tools.py                               # Canonical lookup tools for evidence retrieval
    ├── db.py                                  # Additive persistence handle for ask_mizan.db
    └── config.py                              # Subsystem environment configuration
```

---

## 2. Centralized Database Handle Lifecycle (`db_manager.py`)

To eliminate resource leaks and enforce absolute read-only guarantees on canonical assets, database connections are managed exclusively through `db_manager.py`:

### 2.1 Connection Tracking & Leak Telemetry
```python
class ConnectionTracker:
    def register(self, conn: sqlite3.Connection, db_name: str) -> None: ...
    def unregister(self, conn: sqlite3.Connection) -> None: ...
    def active_count(self) -> int: ...
    def stats(self) -> Dict[str, Any]: ...
```
- Every opened connection is registered in a thread-safe registry with its calling descriptor.
- When closed, the connection is deregistered.
- Any active handle count discrepancies are immediately detectable via the `/api/health` diagnostic endpoint.

### 2.2 Strict Read-Only URI Mode
All canonical database connections are opened with immutable SQLite URI flags:
```python
def open_readonly_connection(db_path: Path) -> ManagedConnection:
    conn = sqlite3.connect(f"file:{db_path.resolve()}?mode=ro", uri=True)
    return ManagedConnection(conn, db_path.name)
```
Any accidental runtime attempt to run `INSERT`, `UPDATE`, `DELETE`, or `DROP` on a canonical asset raises an immediate `sqlite3.OperationalError: attempt to write a readonly database`.

---

## 3. Router Modularization & 95 API Endpoints

The API surface is organized into clear domain routers:
1. **Books & Canonical Hadiths:** `/api/books`, `/api/books/{id}`, `/api/hadith/{id}`, `/api/hadith/{id}/grades`, `/api/hadith/{id}/commentaries`.
2. **Biographical Narrators:** `/api/narrators`, `/api/narrator/{id}`, `/api/narrator/{id}/aqwal`, `/api/narrator/{id}/network`.
3. **Isnād Network Topology:** `/api/isnad/{id}`, `/api/isnad/stats`, `/api/isnad/path`.
4. **Search & Crosswalk Concordance:** `/api/search`, `/api/numbering/resolve`, `/api/hadith/{id}/crosswalk`.
5. **Ask Mīzān Assistant:** `/api/ask/health`, `/api/ask`, `/api/ask/stream`, `/api/ask/conversations/{id}`, `/api/ask/feedback`.
6. **Scholarly Research Workspace:** 25 endpoints under `/api/workspace/*` covering project CRUD, evidence libraries, notes, claims, claim-evidence matrices, and exports.
