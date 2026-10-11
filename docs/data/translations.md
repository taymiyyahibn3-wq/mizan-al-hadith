# MĪZĀN AL-ḤADĪTH — ENGLISH TRANSLATION CORPUS

**Document Identifier:** `docs/data/translations.md`  
**Database Files:** `data/hadith_translations.db` & `data/english_translation_fts.db`  
**Record Count:** 31,488 Verified English Translations  

---

## 1. Corpus Overview & Translation Edition Alignment

To provide accessible study for global researchers, Mīzān indexes **31,488 verified English translations** spanning the Six Canonical Books:
- **Ṣaḥīḥ al-Bukhārī:** Translated by Dr. Muḥammad Muḥsin Khān.
- **Ṣaḥīḥ Muslim:** Translated by ʿAbdul Ḥamīd Ṣiddīqī.
- **Sunan Abī Dāwūd:** Translated by Prof. Aḥmad Ḥasan.
- **Jāmiʿ al-Tirmidhī:** Translated by Abū Khalīl (Darussalam edition).
- **Sunan al-Nasāʾī:** Translated by Nāṣiruddīn al-Khaṭṭāb.
- **Sunan Ibn Mājah:** Translated by Nāṣiruddīn al-Khaṭṭāb.

---

## 2. Text Normalization & Search Indexing

1. **Prefix Separation:** Common English opening phrases (e.g. `Narrated 'Aisha:`, `It was narrated that Abu Hurairah said:`) are indexed while allowing the search engine to prioritize the substantive content of the narration.
2. **FTS5 Porter Stemming:** English text is indexed via SQLite FTS5 using the Porter stemmer tokenizer, enabling queries like `praying`, `prayed`, and `prayer` to match the same root occurrences.
3. **Canonical Alignment:** Every translation record is mapped directly to `canonical_hadith_id` via `data/hadith_translations.db`.
