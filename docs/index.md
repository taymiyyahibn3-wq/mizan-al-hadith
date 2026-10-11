# MĪZĀN AL-ḤADĪTH (ميزان الحديث) — DOCUMENTATION PORTAL

Welcome to the official technical documentation for **Mīzān al-Ḥadīth** (ميزان الحديث), a computational research platform and digital humanities system designed for rigorous, verifiable exploration of classical Islamic Hadith literature.

---

## 📚 Documentation Sitemap

```
docs/
├── index.md                                   # This portal entry point
│
├── overview/                                  # High-level vision, catalog & scope
│   ├── vision-and-scope.md                    # Research rationale and architectural principles
│   ├── feature-catalog.md                     # Comprehensive verified feature matrix
│   └── system-capabilities.md                 # Computational capabilities and benchmarks
│
├── architecture/                              # Structural design and subsystem contracts
│   ├── system-overview.md                     # End-to-end full-stack topology
│   ├── frontend-architecture.md               # Next.js 16 App Router & component hierarchy
│   ├── backend-architecture.md                # FastAPI 0.141 services and connection lifecycle
│   ├── data-architecture.md                   # SQLite relational graph, FTS5 & schemas
│   ├── retrieval-and-rag.md                   # Hybrid retrieval v2 & Ask Mīzān pipeline
│   ├── request-lifecycle.md                   # Deterministic request-to-render lifecycle
│   └── security-and-integrity.md              # Read-only guarantees & scholarly safety guards
│
├── features/                                  # Deep-dive documentation for each feature
│   ├── hadith-library.md                      # Canonical Six Books collection browser
│   ├── search-and-retrieval.md                # Multi-modal search (Arabic, English, rawis, editions)
│   ├── ask-mizan.md                           # Evidence-grounded AI research assistant
│   ├── narrator-research.md                   # Jarḥ wa Taʿdīl & biographical resolution
│   ├── isnad-explorer.md                      # 2D graph, timeline, geographical atlas & 3D space
│   ├── matn-analysis.md                       # Variant comparison & token-level diff viewer
│   ├── knowledge-visualizer.md                # Interactive graph and relation visualizer
│   ├── scholarly-evidence.md                  # Classical master evaluations & modern takhrij
│   ├── commentary-system.md                   # Classical commentary corpus (Fatḥ al-Bārī, etc.)
│   ├── numbering-and-crosswalks.md            # Multi-edition concordancing & alias resolution
│   ├── research-workspace.md                  # Isolated scholarly workspace, projects & claims
│   └── citation-and-export.md                 # Chicago/Arabic academic citation & dossier exports
│
├── api/                                       # Developer interface and OpenAPI reference
│   ├── overview.md                            # REST API overview, conventions & health checks
│   ├── endpoint-reference.md                  # 95 verified API endpoints with schemas & examples
│   └── authentication-and-errors.md           # Researcher identity, rate limits & HTTP error codes
│
├── data/                                      # Datasets, schemas, provenance & licensing
│   ├── dataset-inventory.md                   # Forensic inventory of all databases & records
│   ├── schemas-and-relationships.md           # DDL definitions, primary keys & foreign keys
│   ├── provenance-and-attribution.md          # Upstream source registry & classical attributions
│   ├── translations.md                        # English translation corpus & FTS alignment
│   └── licensing-and-redistribution.md        # Asset licenses, redistribution rules & fair use
│
├── development/                               # Engineering guides and reproducibility
│   ├── prerequisites.md                       # Required runtimes (Node 20+, Python 3.11+, SQLite)
│   ├── local-setup.md                         # Step-by-step installation and startup commands
│   ├── environment-configuration.md           # Configuration variables and .env template
│   ├── testing.md                             # Test suites execution and validation protocols
│   ├── troubleshooting.md                     # Common operational issues and solutions
│   ├── deployment.md                          # Containerization (Docker) and deployment topologies
│   └── contribution-guide.md                  # Guidelines for scholarly and engineering contributions
│
├── diagrams/                                  # Source-controlled Mermaid architectural diagrams
│   ├── system-architecture.mmd                # High-level full-stack architecture diagram
│   ├── request-flow.mmd                       # Query execution & data resolution sequence
│   ├── data-lineage.mmd                       # Source-to-feature data lineage graph
│   ├── ask-mizan-pipeline.mmd                 # Multi-tier Ask Mīzān retrieval & synthesis
│   └── research-workspace.mmd                 # Workspace data model & entity relationships
│
└── github-publication/                        # Release audits & publication reports
    ├── REPOSITORY_AUDIT.md                    # Forensic inventory of real codebase & assets
    ├── SECURITY_AND_PRIVACY_AUDIT.md          # Cryptographic secret scan & privacy certification
    └── PUBLICATION_REPORT.md                  # Final GitHub publication status & checklist
```

---

## 🧭 Key Principles of Mīzān Documentation

1. **Evidence-Based & Verified:** Every statement reflects the real codebase. No hypothetical features or mockups are represented as functional software.
2. **Scholarly Transparency:** Primary Islamic texts and classical judgments are preserved immutably. Researcher notes and AI synthesis are explicitly demarcated and cannot masquerade as canonical gradings.
3. **Reproducibility:** All setup instructions, benchmarks, and tests are verified against live runtime environments.
