# FEATURE — HADITH LIBRARY & COLLECTION BROWSING

**Document Identifier:** `docs/features/hadith-library.md`  
**Frontend Routes:** `/books`, `/books/[id]`, `/hadith/[id]`  
**Backend Endpoints:** `/api/books`, `/api/books/{id}`, `/api/hadith/{id}`  

---

## 1. Overview & Scholarly Objective

The Hadith Library provides a digital reading environment for exploring the canonical Hadith collections. It addresses the challenge of reading classical texts in digital formats without losing manuscript context, chapter boundaries, or critical apparatus.

---

## 2. Supported Canonical Collections (*al-Kutub al-Sittah*)

The library catalog provides verified editions for the Six Canonical Books:

| Collection Title | Arabic Name | Author / Compiler | Death Year | Hadith Count (Verified) | Verified Book ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Ṣaḥīḥ al-Bukhārī** | صحيح البخاري | Muḥammad ibn Ismāʿīl al-Bukhārī | 256 AH | 7,563 | `1` |
| **Ṣaḥīḥ Muslim** | صحيح مسلم | Muslim ibn al-Ḥajjāj al-Naysābūrī | 261 AH | 7,500 | `2` |
| **Sunan Abī Dāwūd** | سنن أبي داود | Abū Dāwūd Sulaymān ibn al-Ashʿath | 275 AH | 5,274 | `3` |
| **Jāmiʿ al-Tirmidhī** | جامع الترمذي | Muḥammad ibn ʿĪsā al-Tirmidhī | 279 AH | 3,956 | `4` |
| **Sunan al-Nasāʾī** | سنن النسائي | Aḥmad ibn Shuʿayb al-Nasāʾī | 303 AH | 5,758 | `5` |
| **Sunan Ibn Mājah** | سنن ابن ماجه | Muḥammad ibn Yazīd Ibn Mājah | 273 AH | 4,341 | `6` |

---

## 3. User Capabilities & Layout

### 3.1 Collection Catalog (`/books`)
- Displays cover art and publication history for each compilation.
- Provides total narration counts, chapter breakdowns, and author biographical summaries.

### 3.2 Book Chapter & Pagination View (`/books/[id]`)
- Interactive chapter sidebar (*Kitāb* / *Bāb*).
- Clean pagination controls supporting jump-to-page and jump-to-hadith.
- Dual-display mode: Arabic matn with toggleable English translation previews.

### 3.3 Deep Hadith Detail Reader (`/hadith/[id]`)
- **Full Arabic Matn:** Rendered in large, high-legibility Arabic typography with diacritics.
- **English Translation:** High-fidelity translation aligned with canonical text ID.
- **Isnād Chain Breakdown:** Segmented transmission chain showing each transmitter name as an interactive biographical link.
- **Scholarly Commentary Drawer:** Direct excerpts from classical commentaries (*Fatḥ al-Bārī*, etc.).
- **Grading & Evidence Matrix:** Badges indicating classical author evaluations and modern academic gradings.
- **Workspace Bookmark Button:** One-click saving to active research projects.

---

## 4. Technical Implementation

- **Frontend Components:**
  - `src/app/books/page.tsx`
  - `src/app/books/[id]/page.tsx`
  - `src/app/hadith/[id]/page.tsx`
  - `src/app/components/BookShowcase.tsx`
  - `src/app/components/HadithCommentarySection.tsx`
  - `src/app/components/ScholarlyAnnotationPanel.tsx`
- **Backend Handlers:**
  - `mizan-web/backend/main.py`: `get_books()`, `get_book(id)`, `get_hadith(id)`, `get_hadith_grades(id)`, `get_hadith_translations(id)`
- **Data Dependencies:** `data/hadith-kg.db` (`books`, `hadiths`, `sanads`, `sanad_rawis`, `rawis`).
