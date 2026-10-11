# MĪZĀN AL-ḤADĪTH — Phase 0 Read-Only Forensic Re-Verification Report
**Status**: Certified Complete  
**Date**: 2026-10-05  
**Auditor**: Lead Product Engineer, Senior Frontend Architect & Scholarly Systems Auditor  
**Mode**: Zero-Trust / Evidence-First

---

## 1. Executive Summary of Re-Verification
Before modifying a single line of production code, every P0 and P1 finding identified in the Master Product Audit (`validation/product_audit/`) was independently investigated and verified against the actual source code, database schemas, and data census of MĪZĀN AL-ḤADĪTH.

All 5 canonical databases were checked and their pre-implementation SHA-256 hashes recorded:
- `data/hadith-kg.db`: `08c3a43d78f510828ab870a23203ef67d8ded7be81f74fdb1b9378996c65dfdd`
- `data/isnad_network.db`: `d141026b306388b4ad30ee6c5c51fca7bf5a2bf90f2698e6089198ff80fb1f6d`
- `data/hadith_numbering.db`: `ecfe3079dba318bde09f544eaf84764a9095a1ec12e0bd3446acf5f6428a66cb`
- `data/citation_enrichment.db`: `8e3a1d03ee6d3668314448acfbb227476cfd85c88b5fb8e57cb92abf5c6d4c37`
- `data/hadith_commentaries.db`: `2fcd9ae4deeb006de25d6db23719abd2ecdaf9779a14f29f81e0cf3a9acebed1`

All scholarly invariants remain intact:
- Rawis: 49,844
- Sanads: 577,024
- Sanad sequences: 4,414,211
- Aqwāl: 127,863
- Critics: 1,015
- Evaluations: 65,420
- Quarantined Zubayr records: 286 (`QUARANTINE_ESCAPE_COUNT = 0`)
- Certified Zubayr records: 18,089
- Commentary #428: Hadith 12427 = PRIMARY, Hadith 12428 = SECONDARY, Hadith 12426 = 0 links.

---

## 2. Forensic Code Verification of Priority Issues

### P0-1: 3D Isnād Chronological Distortion (`ThreeDView.tsx`)
- **Inspection Target**: `mizan-web/frontend/src/app/isnad/ThreeDView.tsx` lines 157-175.
- **Code Observation**:
  ```typescript
  const norm = (val: number | null | undefined, min: number, max: number) => {
    if (val == null) return 0;
    const span = max - min || 1;
    return ((val - min) / span - 0.5) * 2;
  };
  ```
  When `dimX === "death_year"`, any node where `node.death_year == null` yields `norm = 0`.
- **Database Census**: 35,460 out of 49,844 narrators (71.1%) have `death_year IS NULL`.
- **Verification Verdict**: **VERIFIED DEFECT**. 71.1% of narrators are mapped to the geometric center (approx 150 AH), creating an artificial vertical wall of narrators. This constitutes fabricated chronological precision.
- **Remediation Specification**: Replace with explicit partitioning between:
  1. `KNOWN_DATE`: exact death year mapped to temporal axis.
  2. `ESTIMATED_DATE`: generation-derived interval (Ṭabaqah lane) with clear visual bounds.
  3. `UNKNOWN_DATE`: separate uncertainty lane/band with explicit tooltip declaring unknown chronology.

---

### P1-1: Matn Diff Bag-of-Words Limitation (`MatnDiffViewer.tsx`)
- **Inspection Target**: `mizan-web/frontend/src/app/components/MatnDiffViewer.tsx` lines 58-85.
- **Code Observation**:
  ```typescript
  const vNormSet = new Set(vNorm);
  const cNormSet = new Set(cNorm);
  // cTokens mapped via vNormSet.has(norm) -> 'exact' : 'variant'
  // vTokens mapped via cNormSet.has(norm) -> 'exact' : 'addition'
  ```
- **Verification Verdict**: **VERIFIED DEFECT**. Naive set membership checks destroy word order, ignore phrase syntax, cannot distinguish transposition/inversion from matching, and fail to differentiate orthographic normalization from textual additions (*ziyādāt*) or omissions (*nuqṣān*).
- **Remediation Specification**: Implement an Arabic-aware sequence alignment diff algorithm (Longest Common Subsequence / Myers diff) distinguishing:
  - `EXACT_MATCH`: identical letters and diacritics in aligned position.
  - `NORMALIZATION_MATCH`: matched under orthographic normalization (e.g. alif wasla, hamza forms).
  - `DIACRITIC_DIFF`: identical rasm but different harakat.
  - `ADDITION` (*Ziyādah*): text present only in variant.
  - `OMISSION` (*Nuqṣān*): text present in central but omitted in variant.
  - `SUBSTITUTION`: aligned word replacement.
  - `WORD_ORDER_CHANGE`: token present but transposed.

---

### P1-2: Matn 3D Pseudo-Clustering (`MatnThreeDView.tsx`)
- **Inspection Target**: `mizan-web/frontend/src/app/hadith-visualizer/MatnThreeDView.tsx` lines 123-134.
- **Code Observation**:
  ```typescript
  const angle = (idx / (nodes.length - 1)) * 2 * Math.PI;
  const dist = (1 - score) * 280 + 100;
  ```
- **Verification Verdict**: **VERIFIED DEFECT**. Cylindrical angle is strictly a function of arbitrary array index `idx`. Adjacent items appear proximate without any textual, transmission, or thematic relationship.
- **Remediation Specification**: Decommission the misleading cylindrical rotation. Replace with a strictly labeled, data-grounded 2D/3D Variant Lineage or Textual Metric Explorer where spatial dimensions represent verified values:
  - X: Lexical similarity score (Levenshtein / Jaccard / Cosine embedding).
  - Y: Canonical Book hierarchy (Bukhari, Muslim, Tirmidhi...).
  - Z (if 3D maintained): Word count delta or transmission generation, with a mandatory persistent Legend explaining every axis.

---

### P1-3: Isnād Timeline Chain Discontinuity (`TimelineView.tsx`)
- **Inspection Target**: `mizan-web/frontend/src/app/isnad/TimelineView.tsx` lines 52-66.
- **Code Observation**: Nodes lacking death years are partitioned into `undatedNodes` and excluded from the main SVG canvas, relegated to a collapsible drawer.
- **Verification Verdict**: **VERIFIED DEFECT**. Transmission chains spanning dated and undated narrators are broken into disconnected fragments on the canvas.
- **Remediation Specification**: Introduce a hybrid 12-generation Ṭabaqāt timeline. Because `tabaka` is 100% complete across all 49,844 narrators, all narrators can be rendered in continuous sequence within their generation bands. Narrators with verified death years display exact milestone ticks; narrators with unknown death years display dotted/dashed uncertainty contours within their Ṭabaqah lane.

---

## 3. Conclusion & Authorization
Phase 0 Read-Only Forensic Re-Verification is complete. All architectural prerequisites and risk mitigations are formalized. The implementation plan is authorized for execution under zero-mutation rules for canonical databases.
