# MĪZĀN AL-ḤADĪTH — TESTING & REGRESSION VERIFICATION

**Document Identifier:** `docs/development/testing.md`  

---

## 1. Automated Test Suite Overview

Mīzān al-Ḥadīth maintains a comprehensive test suite guaranteeing scholarly integrity, API schema correctness, frontend type safety, and identity resolution.

```
       +--------------------------------------------------------------+
       |               AUTOMATED TEST SUITE MATRIX                    |
       +--------------------------------------------------------------+
       |  1. Workspace Backend Suite      15 / 15 Tests Passed (100%) |
       |  2. Scholarly Integrity Suite    10 / 10 Tests Passed (100%) |
       |  3. Ask Mīzān End-to-End Suite   18 / 18 Tests Passed (100%) |
       |  4. Critical Fixes Sprint Suite  11 / 11 Tests Passed (100%) |
       |  5. Frontend TypeScript Check     0 Errors (Clean Compile)   |
       +--------------------------------------------------------------+
```

---

## 2. Running Backend Test Suites

All tests are located in `scripts/` and can be executed via Python:

### 2.1 Research Workspace Backend Suite (15 Tests)
Validates project lifecycle, evidence library, duplicate guard, Arabic text bit-for-bit preservation, claim formulations, and dossier export.
```bash
python scripts/test_workspace_backend.py
```

### 2.2 Scholarly Integrity & Collision Guard (10 Tests)
Asserts numbering concordance stability (e.g. Ibn Majah 1986 -> canonical #28581), Al-Albani Da'if verification, and Yahya ibn Ma'in father/son collision protection.
```bash
python scripts/test_scholarly_integrity.py
```

### 2.3 Ask Mīzān End-to-End Suite (18 Tests)
Asserts health checks, intent classification, exact lookup, commentary extraction, anti-hallucination citation validation, and canonical DB immutability.
```bash
python scripts/test_ask_mizan_suite.py
```

### 2.4 Critical Fixes Sprint Suite (11 Tests)
Asserts narrator alias resolution (Sufyan al-Thawri vs Sufyan ibn 'Uyaynah vs Sufyan ibn Hamzah), intention variant routing, and translation availability handling.
```bash
python scripts/test_critical_fixes_sprint.py
```

---

## 3. Running Frontend Tests & Type Checking

From the `mizan-web/frontend` directory:

```bash
# TypeScript Typecheck (Zero emit)
npx tsc --noEmit

# Production Build Validation
npm run build
```
