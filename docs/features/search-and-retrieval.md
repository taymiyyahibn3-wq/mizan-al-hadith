# FEATURE — MULTI-MODAL SEARCH & RETRIEVAL

**Document Identifier:** `docs/features/search-and-retrieval.md`  
**Frontend Route:** `/search`  
**Backend Endpoints:** `/api/search`, `/api/numbering/resolve`  

---

## 1. Overview & Capabilities

Traditional Hadith search engines often restrict users to either exact Arabic substrings or English keyword queries. Mīzān al-Ḥadīth implements a **Multi-Modal Search Architecture** capable of simultaneous resolution across four distinct query modalities:

1. **Exact Bibliographical Citations:** e.g., `Sahih al-Bukhari 1`, `Sunan Ibn Majah 1986`, `Bukhari 303`.
2. **Arabic Text & Root Search:** Sub-millisecond FTS5 search with automatic Arabic orthographic normalization (unifying forms of *Alif*, *Yāʾ*, *Tāʾ Marbūṭah*, and stripping diacritics).
3. **English Translation Search:** Full-text semantic and lexical search over 31,488 verified English translations.
4. **Biographical Narrator Lookup:** Searching by scholar or transmitter name in Arabic or English transliteration (e.g. `Abu Hurayrah`, `Sufyan al-Thawri`, `أبو هريرة`).

---

## 2. Arabic Orthographic Normalization

To ensure that differences in spelling or manuscript vocalization do not prevent matching, the search subsystem normalizes queries and index tokens:
- Diacritical marks (*Tashkīl*: fatḥah, ḍammah, kasrah, sukūn, shaddah) are stripped for indexing.
- *Hamzah* variants (`أ`, `إ`, `آ`, `ء`, `ئ`, `ؤ`) normalize to canonical forms.
- *Alif Maqṣūrah* (`ى`) and *Yāʾ* (`ي`) are unified for matching.
- *Tāʾ Marbūṭah* (`ة`) unifies with *Hāʾ* (`ه`).

---

## 3. Request Flow & Execution

```
[ User Search Input ]
         |
         v
+-------------------------------+
|  Query Intent Classification  |
+---------------+---------------+
                |
    +-----------+-----------+--------------------+
    |                       |                    |
    v                       v                    v
[ Citation Matcher ]   [ Arabic FTS5 ]   [ English FTS5 ]
    |                       |                    |
    +-----------+-----------+--------------------+
                |
                v
    [ Score Fusion & Deduplication ]
                |
                v
    [ JSON Response / Top Matches ]
```

---

## 4. Technical Implementation

- **Frontend Component:** `src/app/search/page.tsx`
  - Real-time debounced query submission.
  - Modality filtering tabs: All, Arabic Matn, English Translation, Narrators, Citations.
  - Direct navigation to Hadith reader or Narrator profile.
- **Backend Endpoints:**
  - `GET /api/search?q={query}&book_id={optional}&limit=50`
  - `GET /api/numbering/resolve?query={query}`
- **Databases:** `data/hadith-search-index.db` (FTS5), `data/english_translation_fts.db` (FTS5), `data/hadith_numbering.db`.
