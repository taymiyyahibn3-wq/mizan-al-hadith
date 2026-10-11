# MĪZĀN AL-ḤADĪTH — PREREQUISITES & ENVIRONMENT REQUIREMENTS

**Document Identifier:** `docs/development/prerequisites.md`  

---

## 1. System Requirements

To run Mīzān al-Ḥadīth locally or in a server environment, ensure the host machine meets the following specifications:

| Component | Minimum Specification | Recommended Specification | Notes |
| :--- | :--- | :--- | :--- |
| **Operating System** | Windows 10/11, macOS 12+, Ubuntu 22.04+ | Linux (Ubuntu/Debian) or macOS | Tested on Windows 11 & Linux x86_64 |
| **CPU Architecture** | 4-Core x86_64 or Apple Silicon (M1+) | 8-Core CPU | Multi-core beneficial for FTS and graph queries |
| **RAM** | 8 GB RAM | 16 GB+ RAM | Recommended for caching SQLite B-trees in memory |
| **Storage** | 10 GB Free Storage | 25 GB SSD (NVMe preferred) | Canonical databases total ~2.1 GB uncompressed |

---

## 2. Software Runtimes

1. **Python:** Version `3.11+` (tested with Python 3.11.9)
   - Ensure `pip` is installed and updated (`python -m pip install --upgrade pip`).
2. **Node.js:** Version `20.x` or `22.x LTS` (tested with Node 20+)
   - Includes `npm` (version 10+).
3. **SQLite3:** Version `3.45+` with FTS5 support (included by default in Python 3.11+).
4. **Git:** Version `2.40+`
