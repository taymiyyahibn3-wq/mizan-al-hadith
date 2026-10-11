# MĪZĀN AL-ḤADĪTH — MATN 3D SPATIAL VARIANT CLUSTER SPECIFICATION
**Document Identifier:** `11_MATN_3D_SPEC.md`  
**Certified System Baseline:** Phase 18 Certified Relational Graph  
**Version:** 2.0.0  
**Author:** Lead Data Visualization Engineer & Scholarly Digital Humanities Architect  

---

## 1. 3D Textual Witness Cluster Architecture

The Matn 3D Visualization models textual relationships as a spatial constellation of manuscript witnesses:
- **Entities & Geometry:**
  - **Nodes (Textual Witnesses):** Represent distinct narrations (Bukhārī #1, Muslim #1907, Abū Dāwūd #2201, etc.). Node size reflects text length / token volume; color indicates canonical collection (Bukhari emerald, Muslim navy, Tirmidhi amber, Abu Dawud bronze, Nasa'i violet, Ibn Majah olive).
  - **Edges (Verified Textual Links):** Connect witness nodes where the backend provides a verified mathematical or takhrij alignment score. Edge thickness and opacity scale with LCS (Longest Common Subsequence) score.
  - **Spatial Coordinate Mapping:**
    - **X-Axis:** Chronological compilation date (Compiler Death Year AH).
    - **Y-Axis:** Collection grouping or Chapter classification (*Kitāb*).
    - **Z-Axis:** Textual distance / Jaccard divergence from the central target hadith.
- **Interactive Capabilities:**
  - Orbit rotation, pitch tilt, and smooth zoom.
  - Node selection opens the comparative phrase diff drawer.
  - 2D / 3D toggle button allowing instantaneous switch between radial SVG layout and 3D spatial space.
  - Reduced-motion gate immediately disabling continuous canvas rotations.
