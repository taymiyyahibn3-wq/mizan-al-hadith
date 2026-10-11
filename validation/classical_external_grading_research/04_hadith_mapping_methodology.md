# 04 — HADITH MAPPING METHODOLOGY & DETERMINISTIC ATTACHMENT RULES

## The Danger of Heuristic Mapping
Mapping classical evaluations based on fuzzy title matching, naive keyword overlap, or approximate number offsets leads to severe errors:
1. Two different narrations sharing the same first words (*ṭaraf*) getting cross-contaminated.
2. An evaluation of a specific isnād variant being falsely attached to a different isnād.
3. Attributing a defect (*ʿillah*) found in Sunan Ibn Mājah to an authentic parallel in Ṣaḥīḥ Muslim.

## Mīzān Deterministic Mapping Protocol
Every candidate evaluation MUST pass through a multi-tier identity pipeline before attachment:
```
External Classical Record
          ↓
[1] Collection Identifier (e.g. Jāmiʿ al-Tirmidhī / Book 3)
          ↓
[2] Canonical Hadith Number (no_inbook)
          ↓
[3] Matn Hash & Taraf Verification (Verifying identical opening text)
          ↓
[4] Sanad Transmitter Verification (Verifying transmitter chain matches query)
          ↓
[5] Edition Scheme Resolution (hadith_numbering.db authority)
          ↓
Attached to Mīzān Hadith ID with Certified Provenance
```

For al-Tirmidhi's evaluations, mapping is **100% deterministic** because:
- The text is embedded directly within the book's canonical entry in `hadith-kg.db` (`book_id = 3`, `hadith_id`).
- There is zero external numbering divergence or misaligned lookup table.
