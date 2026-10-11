# EVIDENCE TAXONOMY AUDIT

## 1. Generalized Evidence Model
Mīzān al-Ḥadīth rejects binary flattening of classical hadith criticism. The evidence architecture strictly separates:

1. **`explicit_hadith_grade`**: Direct scholarly verdicts using unequivocal grading vocabulary (*Ṣaḥīḥ*, *Ḥasan*, *Ḥasan Ṣaḥīḥ*).
2. **`hadith_criticism`**: Technical ʿilal analysis, defect identification, isnād analysis, and variant evaluations.

## 2. Controlled Vocabulary for `canonical_term`
- `Ṣaḥīḥ (Explicit)`
- `Ḥasan (Explicit)`
- `Munkar (Hadith Criticism)`
- `Laysa bi-Ṣaḥīḥ (Criticism)`
- `Transmitter Defect / Ḍaʿīf`
- `Mursal (Isnād Defect)`
- `Inqitāʿ / Disconnection (Isnād Defect)`
- `Transmission Error / Wahm`
- `Comparative Tarjīḥ / Variant Preference`
- `Comparative Tarjīḥ (Ashbah bi-al-Ṣawāb)`
- `Khaṭaʾ (Transmission Defect)`
- `Tafarrud / Solitary Route (Isnād Analysis)`
- `Tafarrud / Lack of Corroboration`
- `Waqf / Rafʿ Distinction`
- `Laysa bi-Qawī (Criticism)`
- `Classical Transmission Remark`

## 3. Storage Hierarchy
- **`verbatim_arabic`**: The core operative evaluation phrase.
- **`full_context_arabic`**: The complete text of the scholar's comment as recorded in `taraf_nass`.
- **`attribution`**: Direct attribution to the classical critic as recorded in the primary transmitted text.
