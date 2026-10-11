# MĪZĀN AL-ḤADĪTH — MATN TEXTUAL RESEARCH & COMPARATIVE VISUALIZATION SPECIFICATION
**Document Identifier:** `10_MATN_VISUALIZATION_SPEC.md`  
**Certified System Baseline:** Phase 18 Certified Relational Graph  
**Version:** 2.0.0  
**Author:** Lead Data Visualization Engineer & Scholarly Digital Humanities Architect  

---

## 1. Textual Research Objectives

The Matn (hadith text) visualization interface is designed as an analytical workbench for textual criticism (*Naqd al-Matn*) and variant synthesis across primary collections:
1. **Phrase-Level Variant Highlighting:** Comparing two or more textual witnesses to visually distinguish:
   - **Identical Phrases (Green/Gold background):** Verbatim matching word sequences across witnesses.
   - **Variant Wording (Amber background):** Synonymous expressions, grammatical alternations, or lexical substitutions (e.g. *akhbaranā* vs *ḥaddathanā*).
   - **Additions / Omissions (Blue/Purple or Strikethrough):** Words present in one witness but absent in another (e.g. *Ziyādāt al-Thiqāt*).
2. **Synchronized Dual-Pane Scrolling:** Scrolling the primary central hadith scrolls candidate variant witnesses proportionally according to aligned token indices.
3. **RTL Correctness & Arabic Calligraphic Typography:** Classical Naskh rendering with proper letter-shaping, full diacritic preservation, and high-contrast ink legibility.
4. **Relationship Tier Transparency:** Explicit distinction between:
   - `exact_normalized_matn`: 100% token sequence identity after normalization.
   - `matn_contained`: Subsequence containment (one narration contains the full text of another plus additions).
   - `near_matn`: High token overlap with minor lexical variants.
5. **Zero Speculative Attribution:** Algorithmic similarity percentages represent mathematical token overlaps and must never be falsely labeled as direct literary borrowing or historical dependence unless supported by explicit takhrij citations in the database.
