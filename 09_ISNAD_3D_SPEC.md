# MĪZĀN AL-ḤADĪTH — ISNĀD 3D SPATIAL PROJECTION SPECIFICATION
**Document Identifier:** `09_ISNAD_3D_SPEC.md`  
**Certified System Baseline:** Phase 18 Certified Relational Graph  
**Version:** 2.0.0  
**Author:** Lead Data Visualization Engineer & Scholarly Digital Humanities Architect  

---

## 1. 3D Spatial Research Model

The Isnād 3D Spatial Explorer projects multi-dimensional hadith transmission networks onto a volumetric stage without relying on heavy external WebGL frameworks (built using pure HTML5 Canvas and custom matrix projection mathematics):
- **Spatial Axes Mapping:**
  - **X-Axis:** Chronology (Verified Death Year *Hijri*, 10–310 AH) or Geographic Longitude.
  - **Y-Axis:** Generational Stratum (*Tabaqah*, Rank 1 to 12) or Geographic Latitude.
  - **Z-Axis:** Network Centrality / Degree (Total Riwayah Volume & Citation Count).
- **Depth Cueing & Layering:**
  - Nodes further back along the Z-axis undergo smooth atmospheric fading and scale reduction.
  - Generational planes are rendered as subtle translucent guide grids.
- **Interactive Orbit Controls:**
  - Left-Click + Drag: 360° Pitch and Yaw orbit rotation with inertial damping.
  - Right-Click + Drag: Smooth stage panning.
  - Scroll Wheel: Exponential zoom (0.4x to 3.0x).
- **Path Highlighting & Focus:**
  - Selecting a narrator isolates their entire ascending chain (teachers leading to the Prophet ﷺ) and descending branches (students leading to book compilers).
- **Hardware & Accessibility Safeguards:**
  - **Lazy-Loaded Engine:** The 3D canvas is loaded on demand when the user toggles into the 3D tab.
  - **Reduced-Motion Gate:** If `prefers-reduced-motion: reduce` is active, auto-rotation is disabled, transitions become instantaneous, and camera rotation is bounded.
  - **Automatic 2D Fallback:** On mobile viewports (<640px) or low-spec devices (FPS < 30), a prominent button enables an instant switch to the high-performance 2D Network or Timeline view.
