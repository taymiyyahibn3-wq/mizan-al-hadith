# FRONTEND VERIFICATION & REACT HOOK AUDIT

## 1. Tab 5: Scholarly Evidence UI
The frontend renders classical evidence across two strictly separated sections:
1. **Classical Hadith Grading (Ahkam al-Hadith):** Shows only `explicit_hadith_grade` (verifiable positive scalar rulings).
2. **Classical Hadith Criticism & ʿIlal (Naqd al-Hadith):** Shows `hadith_criticism` (Abū Dāwūd, al-Nasāʾī, and Tirmidhī ʿilal remarks).

## 2. Dynamic Scholar Filters
- The `availableScholars` selector dynamically gathers scholars present for the active hadith.
- When opening an Abū Dāwūd hadith with authorial comments, "al-Imām Abū Dāwūd" appears in the filter dropdown.
- When opening an al-Nasāʾī hadith with authorial comments, "al-Imām al-Nasāʾī" appears in the filter dropdown.
- Zero empty filters: scholars without remarks on a hadith are never shown in that hadith's dropdown.

## 3. React Hook Ordering Invariant
- **Total Hooks in `HadithDetailPage`:** Exactly 36 hooks.
- **Hook Invariance:** All hooks execute unconditionally at top level. Zero hooks inside conditional branches.
- **Turbopack Build:** Next.js 16.3.6 production build compiled with 0 errors across all 12 routes.
