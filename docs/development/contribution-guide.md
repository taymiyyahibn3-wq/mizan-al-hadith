# MĪZĀN AL-ḤADĪTH — CONTRIBUTION GUIDE

**Document Identifier:** `docs/development/contribution-guide.md`  

---

## 1. Welcoming Contributions

We welcome scholarly, engineering, and digital humanities contributions to Mīzān al-Ḥadīth. Because Mīzān handles primary religious texts, contributions are held to both rigorous software engineering standards and traditional scholarly integrity requirements.

---

## 2. Contribution Code of Ethics

1. **Textual Immutability:** Never modify or edit canonical Hadith texts or biographical statements directly. Any corrections to typos in published editions must be submitted with manuscript citations and processed via additive errata tables.
2. **Attribution Integrity:** Never remove or alter historical scholar attributions.
3. **No Unmoored Hallucinations:** Any modifications to the retrieval or AI pipelines must undergo evaluation against `scripts/test_ask_mizan_suite.py` to ensure zero hallucinated citations.

---

## 3. Development Workflow

1. Fork the repository and create a feature branch (`git checkout -b feature/narrator-timeline-zoom`).
2. Make your modifications adhering to TypeScript and Python style guides.
3. Run the automated test suites:
   ```bash
   python scripts/test_workspace_backend.py
   python scripts/test_scholarly_integrity.py
   python scripts/test_ask_mizan_suite.py
   npx tsc --noEmit (in mizan-web/frontend)
   ```
4. Commit your changes with clear, descriptive commit messages.
5. Push to your branch and open a Pull Request.
