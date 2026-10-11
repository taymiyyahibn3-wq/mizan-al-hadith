# MĪZĀN AL-ḤADĪTH — ISNĀD ATLAS (SPATIO-TEMPORAL TRANSMISSION) SPECIFICATION
**Document Identifier:** `08_ISNAD_ATLAS_SPEC.md`  
**Certified System Baseline:** Phase 18 Certified Relational Graph  
**Version:** 2.0.0  
**Author:** Lead Data Visualization Engineer & Scholarly Digital Humanities Architect  

---

## 1. Integrated Concept: Geography + Time + Transmission

The Isnād Atlas is a synthesis mode unifying geographic location, chronological progression, and relational transmission vectors into a single interactive research interface:
- **Directional Transmission Flow Arcs:** Quadratic Bézier curves connect teacher centers to student centers (Teacher City &rarr; Student City), indicating the historical direction of narration propagation.
- **Century & Era Scrubbing:** Researchers can filter flows by century:
  - 1st Century AH (Prophetic era through late Companions: Madinah &rarr; Kufah, Basra, Damascus, Egypt)
  - 2nd Century AH (The era of great regional compilation: Madinah/Makkah &rarr; Iraq, Yemen, Syria)
  - 3rd Century AH (The era of the canonical Sihah Sittah: Khurasan, Transoxiana, Baghdad, Hijaz)
- **Multi-Chain Route Inspection:** Clicking any transmission arc displays the exact transmitter pairs and associated collection records that traveled along that regional path.
- **Internal vs External Regional Toggles:** Option to isolate long-distance journeys (*Riḥlah*) from internal city transmissions (e.g. Kufah &rarr; Kufah).
