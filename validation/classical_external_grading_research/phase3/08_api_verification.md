# BACKEND API VERIFICATION

## 1. Endpoint Audited
- `GET /api/hadith/{hadith_id}/grades`

## 2. Response Structure
The endpoint response was enhanced to explicitly partition classical grades and classical criticism while preserving 100% backward compatibility:
```json
{
  "hadith_id": 16340,
  "status_grade": null,
  "narration_type": "حديث",
  "count": 0,
  "grades": [],
  "contemporary_grades": [],
  "classical_evaluations": [
    {
      "id": 2731,
      "hadith_id": 16340,
      "book_id": 4,
      "no_inbook": 18,
      "scholar_id": "abu_dawud",
      "scholar_en": "al-Imām Abū Dāwūd",
      "scholar_ar": "أبو داود السجستاني",
      "work_en": "Sunan Abī Dāwūd",
      "work_ar": "سنن أبي داود",
      "evidence_type": "hadith_criticism",
      "canonical_term": "Munkar (Hadith Criticism)",
      "verbatim_arabic": "قال أبو داود هذا حديث منكر وإنما يعرف عن ابن جريج...",
      "full_context_arabic": "قال أبو داود هذا حديث منكر...",
      "attribution": "Direct authorial remark preserved in transmitted text of Sunan Abī Dāwūd",
      "license": "Public Domain (Classical Work, d. 275 AH)",
      "verification_status": "verified"
    }
  ],
  "classical_evaluations_count": 1,
  "classical_hadith_grades": [],
  "classical_hadith_criticism": [ ... ],
  "narrator_statements": [],
  "narrator_statements_count": 0
}
```
