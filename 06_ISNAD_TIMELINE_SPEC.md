# MĪZĀN AL-ḤADĪTH — ISNĀD TIMELINE & CHRONOLOGY SPECIFICATION
**Document Identifier:** `06_ISNAD_TIMELINE_SPEC.md`  
**Certified System Baseline:** Phase 18 Certified Relational Graph  
**Version:** 2.0.0  
**Author:** Lead Data Visualization Engineer & Scholarly Digital Humanities Architect  

---

## 1. Analytical Purpose & Research Features

The Isnād Timeline transforms abstract transmitter graphs into a rigorous chronological sequence showing how narrations passed across centuries:
- **Generational Progression (*Tabaqāt*):** Transmitters are mapped along the horizontal axis by their verified death year (*Hijri*), with vertical banding indicating classical generational strata:
  - Stratum 1: *Al-Ṣaḥābah* (Companions, 1–110 AH)
  - Stratum 2: *Kibār al-Tābiʿīn* (Senior Followers, 60–150 AH)
  - Stratum 3: *Wusṭā al-Tābiʿīn* (Intermediate Followers, 100–180 AH)
  - Stratum 4: *Atbāʿ al-Tābiʿīn* (Successors, 140–220 AH)
  - Stratum 5: *Aṣḥāb al-Kutub* (Great Compilers, 200–310 AH)
- **Branching & Divergence Highlighting:** Tracing where a single teacher's students transmit into multiple independent chains, or where multiple independent chains converge on a common link (*Madār*).
- **Undated Transmitters Handling:** Transmitters whose historical death year is unrecorded in biographical dictionaries are not assigned speculative dates. They are explicitly distinguished with a dotted border and listed in an expandable "Undated Scholarly Roster" with their generational rank (*tabaqah*).
- **Interactive Temporal Scrubbing:** A playback scrubber allows researchers to step year-by-year from 10 AH to 300 AH, watching the living chain of narrators illuminate as transmission occurred.
- **Node Selection & Chain Focus:** Clicking any narrator highlights all incoming edges (teachers) and outgoing edges (students), dimming unrelated branches.
