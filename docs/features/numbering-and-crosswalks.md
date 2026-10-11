# FEATURE — NUMBERING SCHEMES & CONCORDANCE CROSSWALKS

**Document Identifier:** `docs/features/numbering-and-crosswalks.md`  
**Frontend Route:** Integrated in `/hadith/[id]` & `/search`  
**Backend Endpoints:** `/api/numbering/resolve`, `/api/hadith/{id}/crosswalk`  

---

## 1. Overview & Scholarly Problem

Hadith numbering is not historically standardized. Classical manuscripts were organized by *Kitāb* (Book) and *Bāb* (Chapter), not sequential integers. In the 20th century, multiple independent scholars and publishers assigned sequential numbers, creating severe concordancing discrepancies:
- **Fu'ad ʿAbd al-Bāqī Edition:** Used extensively in Egyptian and Arabic scholarship.
- **Darussalam Edition:** Used internationally in English and Urdu translations.
- **A.J. Wensinck Concordance:** Used in Western orientalist scholarship (*Concordance et Indices de la Tradition Musulmane*).

A researcher searching for "Sunan Ibn Majah #1986" in an English work will fail to find it in an Arabic database that numbers it #1976.

---

## 2. Concordance Resolution Engine

Mīzān's concordance crosswalk (`hadith_numbering.db`) contains **95,598 mappings across 18 numbering editions**:

```
[ User Input: "Ibn Majah 1986" ]
              |
              v
[ Normalized Key: "ibnmajah_darussalam_en:1986" ]
              |
              v
[ hadith_numbers table lookup ]
              |
              v
[ Canonical Hadith ID: 28581 ]
              |
    +---------+---------+
    |                   |
    v                   v
[ Arabic Matn ]     [ Concordance Crosswalk Table ]
                    - Darussalam English: #1986
                    - Fu'ad 'Abd al-Baqi: #1976
                    - Classical Print Page: p. 493
```

---

## 3. Supported Editions Matrix

1. `bukhari_darussalam_en` / `bukhari_abdul_baqi`
2. `muslim_darussalam_en` / `muslim_abdul_baqi`
3. `abudawud_darussalam_en` / `abudawud_muhyi_al_din`
4. `tirmidhi_darussalam_en` / `tirmidhi_ahmad_shakir`
5. `nasai_darussalam_en` / `nasai_abu_ghuddah`
6. `ibnmajah_darussalam_en` / `ibnmajah_abdul_baqi`

All crosswalk resolutions are verified in automated test suites (`scripts/test_scholarly_integrity.py`).
