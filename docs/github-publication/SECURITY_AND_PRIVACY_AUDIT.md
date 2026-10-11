# MĪZĀN AL-ḤADĪTH — SECURITY, PRIVACY & PUBLICATION AUDIT

**Document Identifier:** `docs/github-publication/SECURITY_AND_PRIVACY_AUDIT.md`  
**Audit Standard:** Master Publication Directive · Phase B Compliance  
**Audit Date:** October 2026  
**Auditor:** Information Security Architect & Data Privacy Officer  
**Audit Outcome:** **PASS — SAFE FOR PUBLICATION UNDER DOCUMENTED POLICIES**  

---

## 1. Executive Summary

Before any public GitHub synchronization or repository release, a comprehensive forensic scan was conducted across all tracked and untracked directories of Mīzān al-Ḥadīth. The audit verified:
1. **Zero Secret Leakage:** No API keys, Discord bot tokens, provider credentials, personal access tokens, or private certificates exist in tracked or staged files.
2. **Environment File Protection:** All live `.env` and `.env.local` files are strictly excluded from source control by verified `.gitignore` rules.
3. **Canonical Scholarly Data Protection:** Canonical databases are strictly read-only, verified against SHA-256 integrity baselines, and protected from accidental mutation or direct commit.
4. **Researcher Workspace Isolation:** User-generated workspace annotations, claims, and notes are segregated in an isolated database file (`data/research_workspace.db`), preventing private research records from leaking into source control or canonical datasets.
5. **Compliant Dataset Distribution Policy:** A formal data distribution and acquisition policy is documented, replacing direct Git tracking of multi-gigabyte binary assets with reproducible hydration procedures.

---

## 2. Cryptographic Secret & Credential Scan

A ripgrep and regex-based forensic scan was executed targeting common token and credential patterns across all source, documentation, configuration, and script files.

| Secret Pattern Scanned | Regex Signature | Scan Scope | Detections Found | Remediation Status |
| :--- | :--- | :--- | :--- | :--- |
| **Google Cloud / Gemini API Keys** | `AIza[0-9A-Za-z-_]{35}` | All files (`*.py`, `*.ts`, `*.json`, `*.md`, etc.) | **0** | Verified Clean |
| **OpenAI Secret Keys** | `sk-[a-zA-Z0-9]{24,}` | All source & config files | **0** | Verified Clean |
| **GitHub Personal Access Tokens** | `ghp_[a-zA-Z0-9]{30,}` | All repositories and scripts | **0** | Verified Clean |
| **Discord Bot Tokens** | `[a-zA-Z0-9_-]{24}\.[a-zA-Z0-9_-]{6}\.[a-zA-Z0-9_-]{27}` | All bot and backend scripts | **0** | Verified Clean (Token isolated in untracked `.env`) |
| **Private Keys & Certificates** | `-----BEGIN (RSA\|EC\|OPENSSH)? PRIVATE KEY-----` | Workspace filesystem | **0** | Verified Clean |

### 2.1 Verification of Environment Files
- `.\.env` — Contains local development credentials (`DISCORD_TOKEN`, `GEMINI_API_KEY`). **Verified ignored by root `.gitignore` line 34.**
- `.\mizan-web\frontend\.env.local` — Contains `NEXT_PUBLIC_API_URL=http://127.0.0.1:8000/api`. **Verified ignored by Next.js `.gitignore`.**
- `.\.env.example` & `.\mizan-web\frontend\.env.example` — Sanitized templates containing dummy placeholders only (`your_discord_bot_token_here`). Safe for version control.

---

## 3. Canonical Database Safeguards & Read-Only Guarantees

### 3.1 Immutability of Canonical Assets
Canonical Hadith databases represent foundational scholarly heritage and cannot be modified under any runtime or publication scenario:
1. **Read-Only SQLite Connection Strings:** All backend database handles in `db_manager.py` connect via SQLite URI with strict `mode=ro` flags:
   ```python
   # db_manager.py enforce read-only handle
   sqlite3.connect(f"file:{resolved_path}?mode=ro", uri=True)
   ```
2. **Zero In-Place Migration:** Any schema updates or indices are created exclusively in separate additive tables or derived cache stores.
3. **Forensic Integrity Verification:** SHA-256 hashes of canonical database baselines are maintained in validation registries and verified by automated regression test suites (`scripts/test_scholarly_integrity.py`).

### 3.2 Canonical Data Protection Rules
- **No Direct Git Tracking:** Multi-gigabyte SQLite databases (`hadith-kg.db` at 1.64 GB, `hadith-search-index.db` at 237 MB, etc.) exceed GitHub recommended file limits (100 MB max per file). They are strictly excluded by `*.db`, `*.sqlite`, and `data/` rules in `.gitignore`.
- **Preservation of Attribution:** Classical texts remain attributed to their historical compilers (Imam al-Bukhari, Imam Muslim, Imam Abu Dawud, Imam al-Tirmidhi, Imam al-Nasa'i, Imam Ibn Majah).
- **Prohibited Alterations:** Normalization, diacritics stripping, or entity linking is performed via external index tables or query-time normalization; the underlying canonical matn is preserved bit-for-bit.

---

## 4. Scholarly Research Workspace Privacy & Isolation

The Mīzān platform includes an isolated Scholarly Research Workspace (`/workspace`) allowing researchers to formulate private hypotheses, create claim-evidence matrices, and write draft notes.

### 4.1 Privacy Architecture
1. **Separate Storage:** All workspace data is persisted strictly in `data/research_workspace.db`. It never writes to `hadith-kg.db` or any canonical database.
2. **Metadata Attribution:** Every workspace entity (claim, note, evidence link) explicitly carries:
   ```json
   {
     "source_tier": "RESEARCHER_WORKSPACE",
     "is_canonical": false
   }
   ```
3. **Multi-User Isolation:** Endpoints in `mizan-web/backend/research_workspace.py` require the `X-Researcher-Id` header and enforce row-level access control. A researcher cannot inspect or mutate another researcher's projects or notes.
4. **Git Exclusion:** `data/research_workspace.db` is strictly ignored by `.gitignore` and is never committed to GitHub.

---

## 5. Dataset Distribution & Acquisition Policy

Because primary database files exceed Git storage limits and carry distinct upstream licenses, Mīzān employs a **Hydration & Provenance Policy**:

```
+-----------------------------------------------------------------------------------+
|                        MĪZĀN DATASET DISTRIBUTION POLICY                          |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ GitHub Repository ]                                                            |
|       |                                                                           |
|       +--> Source Code (FastAPI backend + Next.js frontend)                       |
|       +--> Documentation & Interactive Visualizers                                |
|       +--> Schemas, DDLs, and Ingestion Scripts (`scripts/`)                      |
|       +--> Synthetic & Acceptance Test Fixtures                                   |
|                                                                                   |
|  [ External Dataset Distribution Mirrors ]                                        |
|       |                                                                           |
|       +--> Canonical `hadith-kg.db` (1.64 GB)      --> Zenodo / Hugging Face      |
|       +--> `hadith_numbering.db` (35 MB)           --> Release Asset Mirror       |
|       +--> `isnad_network.db` (52 MB)              --> Release Asset Mirror       |
|       +--> `hadith_translations.db` (24 MB)        --> Release Asset Mirror       |
|       +--> `hadith_commentaries.db` (9 MB)         --> Release Asset Mirror       |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

### 5.1 Hydration Instructions for Developers
1. Clone the repository without large binaries.
2. Run `python scripts/download_canonical_datasets.py` or manually place verified database snapshots into `data/`.
3. Verify SHA-256 checksums using `python scripts/verify_preflight_hashes.py`.
4. Initialize the derived search indices via `python scripts/build_english_fts.py`.

---

## 6. Updated `.gitignore` Specification

The root `.gitignore` has been updated and audited to guarantee zero unauthorized tracking:
- **Python:** `venv/`, `.venv/`, `__pycache__/`, `*.py[cod]`
- **Node.js:** `node_modules/`, `.next/`, `out/`, `build/`, `dist/`
- **Databases:** `data/`, `database/`, `*.db`, `*.sqlite`, `*.sqlite3`, `*.db-shm`, `*.db-wal`, `*.parquet`, `*.npy`
- **Secrets:** `.env`, `.env.*`, `.env.local`, `*.pem`, `*.key` (allowing only `!.env.example`)
- **Logs & Dumps:** `*.log`, `*.zip`, `*.tar.gz`, `scratch/`, `tmp/`, intermediate audit text files
- **Backups:** `*.backup*`, `*.mojibake-backup`, `*.visualizer-backup*`

---

## 7. Audit Certification

This security and privacy audit certifies that the Mīzān al-Ḥadīth codebase is **fully sanitized, architecturally safeguarded, and safe for public GitHub repository publication**.
