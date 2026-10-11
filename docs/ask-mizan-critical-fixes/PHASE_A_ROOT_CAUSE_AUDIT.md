# PHASE A — ROOT CAUSE AUDIT & INCIDENT REPRODUCTION REPORT
**Project:** Mīzān al-Ḥadīth (ميزان الحديث)  
**Target System:** Ask Mīzān Backend, Retrieval Pipeline, Entity Resolution & Frontend UI  
**Execution Timestamp:** 2026-10-11T13:30:00Z  
**Audit Author:** Senior AI Retrieval Architect & Adversarial QA Specialist  
**Status:** All 4 Incidents Empirically Reproduced & Root Causes Isolated  

---

## 1. PRE-IMPLEMENTATION CRYPTOGRAPHIC DATABASE AUDIT

Prior to initiating any investigation or code modifications, a full cryptographic verification was executed across all 34 canonical and reference SQLite databases in `data/` against the authoritative baseline hashes recorded in `validation/baseline_db_hashes.json`.

- **Total Canonical & Reference Databases:** 34
- **Verified Bit-for-Bit Matches:** 34 / 34 (100.0%)
- **Mismatches:** 0
- **Integrity Verdict:** **100% CRYPTOGRAPHICALLY IDENTICAL AND UNTOUCHED**

```
Database Verification Status:
- data/hadith-kg.db: MATCH
- data/isnad_network.db: MATCH
- data/hadith_translations.db: MATCH
- data/hadith_numbering.db: MATCH
- data/hadith_commentaries.db: MATCH
- data/classical_scholar_evidence.db: MATCH
- data/citation_enrichment.db: MATCH
- data/english_enrichment.db: MATCH
- data/english_translation_fts.db: MATCH
- data/hadith-search-index.db: MATCH
... (all 34 databases verified)
```

---

## 2. INCIDENT 1: SUFYĀN AL-THAWRĪ MISRESOLVED TO SUFYĀN IBN ḤAMZAH AL-ASLAMĪ

### 2.1 Incident Description & Reproduction
- **User Query:** `Tell me about Sufyan al-Thawri`
- **Observed Bug:** The system returned a narrator dossier for **Sufyān ibn Ḥamzah al-Aslamī** (`CANON-RAW-003432`, Rawi ID 3432), a minor narrator with 41 narrations, rather than the intended celebrated master scholar **Sufyān al-Thawrī** (`CANON-RAW-003436`, Rawi ID 3436, 2,917 narrations).
- **Reproduction Command:**
  ```bash
  python scratch/trace_sufyan_resolution.py
  ```
- **Observed Payload:**
  ```json
  {
    "canonical_id": "CANON-RAW-003432",
    "anchor_rawi_id": 3432,
    "canonical_arabic_name": "سفيان بن حمزة بن سفيان بن فروة",
    "preferred_english_name": "Sufyān ibn Ḥamzah al-Aslamī",
    "matched_by": {
      "matched_alias": "سفيان الثوري",
      "alias_type": "full_name",
      "matched_query": "Sufyan al-Thawri",
      "is_exact_alias": true
    }
  }
  ```

### 2.2 Root Cause Analysis
1. **Primary Root Cause — Hardcoded ID Transposition in Alias Table:**
   In [`mizan-web/backend/identity_resolution.py:731-734`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/identity_resolution.py#L731-L734):
   ```python
   FAMOUS_CLASSICAL_ALIASES: Dict[int, List[Dict[str, str]]] = {
       ...
       3432: [  # Sufyan al-Thawri (INCORRECT ID: 3432 instead of 3436)
           {"arabic": "الثوري", "english": "al-Thawrī", "type": "nisbah"},
           {"arabic": "سفيان الثوري", "english": "Sufyān al-Thawrī", "type": "full_name"},
       ],
   }
   ```
   In the canonical database `data/hadith-kg.db`:
   - Rawi **3432** is `سفيان بن حمزة بن سفيان بن فروة` (Sufyān ibn Ḥamzah al-Aslamī, riwaya_qty: 41).
   - Rawi **3436** is `سفيان بن سعيد بن مسروق بن حمزة بن حبيب بن موهبة بن نصر بن ثعلبة بن ملكان بن ثور` (`سفيان الثوري`, riwaya_qty: 2,917).
2. **Secondary Discrepancies in `FAMOUS_CLASSICAL_ALIASES`:**
   - Key `4698` was mapped to `Sufyan ibn Uyaynah`. In `hadith-kg.db`, Rawi 4698 is `الحميدي عبد الله بن الزبير` (al-Humaydī), whereas `سفيان بن عيينة` is Rawi **3443** (riwaya_qty: 2,299).
   - Key `4049` was mapped to `Malik ibn Anas`. In `hadith-kg.db`, Rawi 4049 is `عائشة بنت أبي بكر` (Aisha bint Abi Bakr), whereas `مالك بن أنس الأصبحي` is Rawi **6659** (riwaya_qty: 1,341).
3. **Flawed Alias Search Substring Matching:**
   In `identity_resolution.py:773`:
   ```python
   if al_ar == norm_q or al_en == norm_en or norm_q in al_ar or norm_en in al_en:
       matched_rawis[rid] = { ... "is_exact_alias": True }
   ```
   Even partial substring containment set `"is_exact_alias": True`, prioritizing partial substring matches over database lexical matches.

---

## 3. INCIDENT 2: HADITH OF INTENTIONS FAILS TO RETRIEVE APPROPRIATE HADITH

### 3.1 Incident Description & Reproduction
- **User Query:** `Tell me about hadith of intentions`
- **Observed Bug:** Failed to retrieve Sahih al-Bukhari 1; displayed an insufficient-evidence message: `"No biographical record or Jarḥ wa Taʿdīl statements were found in Mīzān for the requested narrator."`
- **Reproduction Command:**
  ```bash
  python scratch/test_intentions_routing.py
  ```
- **Observed Output:**
  ```
  QUERY: Tell me about hadith of intentions
  PARSER INTENT: QueryIntent.NARRATOR_LOOKUP (Confidence: 0.98)
  PARSER ENTITIES: {'narrator_name': 'hadith of intentions'}
  EXEC INTENT: QueryIntent.NARRATOR_LOOKUP
  INSUFFICIENT: True (HADITHS COUNT: 0)
  ANSWER: > [!IMPORTANT]
  > **Insufficient Mīzān Evidence**
  > No biographical record or Jarḥ wa Taʿdīl statements were found in Mīzān for the requested narrator.
  ```

### 3.2 Root Cause Analysis
1. **Aggressive Catch-All Narrator Regex:**
   In [`mizan-web/backend/ask_mizan/parser.py:116-121`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/parser.py#L116-L121):
   ```python
   # Pattern 6: "tell\s+me\s+about\s+(?:the\s+narrator\s+)?<Name>"
   m = re.search(r"(?:tell\s+me\s+about|about\s+the\s+narrator|عن\s+الراوي|کے\s+بارے\s+میں\s+بتائیں)\s+(.+)$", clean, re.I)
   ```
   The regex captured whatever text followed `"tell me about"`. For `"Tell me about hadith of intentions"`, it extracted `hadith of intentions`.
2. **Inadequate Stopword/Filter Guards:**
   `clean_target_name()` only checked if the whole extracted string was exactly `"hadith"`, but did not reject strings starting with `hadith of`, `the hadith about`, `hadith`, `narration`, or phrases referencing Hadith subjects.
3. **Inversion of Intent Priority in `parse_query`:**
   In `parser.py:238-242`, Section 1 ("Narrator Entity First Extraction") was executed before Hadith reference resolution and thematic keyword search. Any query matching `"tell me about <topic>"` was forced into `QueryIntent.NARRATOR_LOOKUP` with 0.98 confidence, bypassing Hadith text retrieval.

---

## 4. INCIDENT 3: BUKHARI 1 PAGE REPORTS ENGLISH TRANSLATION UNAVAILABLE

### 4.1 Incident Description & Reproduction
- **Observed Bug:** Navigating to `/hadith/1` (Sahih al-Bukhari 1) renders Arabic matn, but the English Translation panel shows:
  *"English translation is not currently available for this narration. Mīzān al-Hadīth only displays verified scholarly translations with provenance."*
- **Observed Network Call:**
  `GET /api/hadith/1/translations` returned:
  ```json
  {
    "hadith_id": 1,
    "available": false,
    "count": 0,
    "primary": null,
    "translations": [],
    "message": "English translation not currently available for this narration."
  }
  ```

### 4.2 Root Cause Analysis
1. **Canonical Database File Path Misconfiguration:**
   In [`mizan-web/backend/db_manager.py:35`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/db_manager.py#L35):
   ```python
   TRANSLATIONS_PATH = resolve_db_path("/data/translations.db", "data/translations.db")
   ```
   The actual verified database file in the repository is [`data/hadith_translations.db`](file:///c:/Users/taymi/discord-hadith-bot/data/hadith_translations.db) (24.05 MB, containing 31,488 verified English translations).
   The path `data/translations.db` **does not exist** (`Path('data/translations.db').exists() == False`).
2. **Silent Failure in Endpoint Handler:**
   In `db_manager.py:287-288`:
   ```python
   def get_translations_db() -> Optional[sqlite3.Connection]:
       return open_readonly_connection(TRANSLATIONS_PATH, "translations")
   ```
   Because `TRANSLATIONS_PATH` pointed to a non-existent file, `get_translations_db()` returned `None`.
   In [`mizan-web/backend/main.py:2012-2024`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/main.py#L2012-L2024):
   ```python
   trans_db = get_translations_db()
   if trans_db is None:
       return {
           "available": False,
           "message": "English translation not currently available for this narration.",
           ...
       }
   ```
   The backend unconditionally returned `available: False` for every single Hadith in the application, despite 31,488 verified scholarly translations (including Dr. Muhammad Muhsin Khan's translation for Bukhari 1) existing in `data/hadith_translations.db`.

---

## 5. INCIDENT 4: RAW MARKDOWN MARKERS IN INSUFFICIENT-EVIDENCE NOTICE

### 5.1 Incident Description & Reproduction
- **Observed Bug:** The insufficient-evidence callout box rendered raw Markdown markers:
  `> [!IMPORTANT] > **Insufficient Mīzān Evidence** > ...`
- **Reproduction Payload:**
  `response.answer_markdown`:
  ```markdown
  > [!IMPORTANT]
  > **Insufficient Mīzān Evidence**
  >
  > No biographical record or Jarḥ wa Taʿdīl statements were found in Mīzān for the requested narrator.
  ```

### 5.2 Root Cause Analysis
1. **Backend Construction:**
   In [`mizan-web/backend/ask_mizan/engine.py:306`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/backend/ask_mizan/engine.py#L306):
   ```python
   answer_markdown=f"> [!IMPORTANT]\n> **Insufficient Mīzān Evidence**\n>\n> {refusal_reason}"
   ```
   The backend formatted the refusal reason as GitHub Flavored Markdown alert blockquotes (`> [!IMPORTANT]`, `> **...**`).
2. **Frontend Unparsed Rendering:**
   In [`mizan-web/frontend/src/app/ask/page.tsx:497-499`](file:///c:/Users/taymi/discord-hadith-bot/mizan-web/frontend/src/app/ask/page.tsx#L497-L499):
   ```tsx
   <div className="text-sm text-[#3b321e] leading-relaxed">
     {response.answer_markdown}
   </div>
   ```
   React rendered `{response.answer_markdown}` as raw text inside a `<div>`, without parsing Markdown via `<FormattedAnswer>` or stripping alert blockquote prefixes for plain-text presentation.

---

## 6. PHASE REPAIR ROADMAP

| Phase | Target Component | Corrective Action |
| :--- | :--- | :--- |
| **Phase B** | `identity_resolution.py` | Correct `FAMOUS_CLASSICAL_ALIASES` IDs: Sufyān al-Thawrī $\rightarrow$ 3436, Sufyān ibn ʿUyaynah $\rightarrow$ 3443, Mālik ibn Anas $\rightarrow$ 6659. Restrict `is_exact_alias` strictly to exact normalized string equality. |
| **Phase C** | `parser.py` & `engine.py` | Add guards in `extract_narrator_name_from_query` rejecting `hadith of ...`, `the hadith about ...`, and non-person terms. Route Hadith of intentions to Hadith retrieval. |
| **Phase D** | `db_manager.py` | Correct `TRANSLATIONS_PATH` to point to `/data/hadith_translations.db` (and `SEARCH_INDEX_PATH` to `/data/hadith-search-index.db`). |
| **Phase E** | `engine.py` & `page.tsx` | Sanitize/render insufficient-evidence messages properly: clean alert markers and render formatted text without raw `>` or `**` artifacts. |
| **Phase F & G** | Frontend & Automated Tests | End-to-end regression testing and unit test suite expansion. |
| **Phase H** | Verification & Certification | Recompute all 34 database hashes to certify 100% read-only data preservation. |
