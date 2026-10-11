# FEATURE — MATN VARIANT ANALYSIS & DIFF VIEWER

**Document Identifier:** `docs/features/matn-analysis.md`  
**Frontend Route:** `/hadith-visualizer`  
**Backend Endpoints:** `/api/matn/diff`, `/api/hadith/compare`  

---

## 1. Overview & Scholarly Objective

In classical Hadith criticism, analyzing textual variations across transmission chains (*Muʿāraḍat al-Mutūn*) is essential for detecting transmission additions (*Ziyādat al-Thiqah*), anomalies (*Shudhūdh*), and hidden defects (*ʿIlal*).

The Matn Variant Analysis module provides digital side-by-side textual diffing and lexical alignment between different narrations of the same tradition.

---

## 2. Capabilities & Layout

1. **Dual Narration Selection:** Researchers can enter two canonical hadith IDs (e.g. Bukhari #1 and Muslim #1907) or select from suggested parallel transmissions.
2. **Word-by-Word Alignment:** Computes token-level differences using longest common subsequence algorithms adapted for Arabic morphology.
3. **Color-Coded Visual Diff:**
   - **Green Highlight:** Unique tokens present in Text A.
   - **Rose Highlight:** Unique tokens present in Text B.
   - **Neutral Parchment:** Shared matching tokens.
4. **Lexical Overlap Score:** Quantifies lexical similarity as a ratio from 0.00 to 1.00.
5. **Scholarly Integrity Caveat:** The interface explicitly reminds users:
   > *"Lexical similarity is an analytical computational aid, not proof of identical transmission or authentic provenance."*

---

## 3. Technical Implementation

- **Frontend Component:** `src/app/hadith-visualizer/page.tsx` and `src/app/components/MatnDiffViewer.tsx`.
- **Backend Endpoints:**
  - `POST /api/hadith/compare` (Request: `{ hadith_id_1: int, hadith_id_2: int }`)
  - Response contains: `hadith_1`, `hadith_2`, `lexical_overlap`, `exact_match`, `normalized_match`, `alignment_tokens`.
- **Normalization Engine:** Strips diacritics and unifies orthographic variants prior to diff calculation while rendering original diacritics in the visual display.
