# MĪZĀN AL-ḤADĪTH — ISNĀD VISUALIZATION MASTER SPECIFICATION
**Document Identifier:** `05_ISNAD_VISUALIZATION_SPEC.md`  
**Certified System Baseline:** Phase 18 Certified Relational Graph  
**Version:** 2.0.0  
**Author:** Lead Data Visualization Engineer & Scholarly Digital Humanities Architect  

---

## 1. Research Objectives & Design Tenets

The Isnād (chain of transmission) is the foundational forensic instrument of classical hadith criticism (*Naqd al-Ḥadīth*). Visualizing an isnād network must avoid decorative graph bloat; it must serve as an analytical research instrument capable of revealing:
1. **Chain Convergence & Divergence:** Identifying common link scholars (*Madār al-Isnād*) where multiple transmission branches originate or unite.
2. **Generational Progression (*Tabaqāt*):** Clear visual separation between the Prophet ﷺ, the Companions (*Ṣaḥābah*), the Followers (*Tābiʿīn*), the Successors (*Atbāʿ al-Tābiʿīn*), and subsequent compiler generations.
3. **Temporal Fidelity:** Representing verified death years (*Wafayāt*) without fabricating missing chronology; undated transmitters must remain explicitly distinguishable.
4. **Geographic Grounding:** Mapping real centers of transmission (Madīnah, Makkah, Kūfah, Baṣrah, Damascus, Cairo, Nishāpūr, etc.) without drawing speculative routes.
5. **Multi-View Coordination:** Unifying Network, Timeline, Map, Atlas, and 3D views around a shared selected narrator context.

---

## 2. Coordinated Multi-View Architecture

```
                               ISNĀD VISUALIZATION ENGINE
                               
 ┌─────────────────────────────────────────────────────────────────────────┐
 │               Global State & Narrator Context (Selected / Hovered)       │
 └──────┬──────────────┬──────────────┬──────────────┬──────────────┬──────┘
        │              │              │              │              │
        ▼              ▼              ▼              ▼              ▼
 ┌─────────────┐┌─────────────┐┌─────────────┐┌─────────────┐┌─────────────┐
 │ 1. Network  ││ 2. Timeline ││ 3. Map View ││ 4. Atlas    ││ 5. 3D Space │
 │ Direct      ││ Chronology  ││ Regional    ││ Spatio-     ││ Generational│
 │ Directed    ││ & Branching ││ Clustering  ││ Temporal    ││ Volumetric  │
 │ Multigraph  ││ Divergence  ││ & Centers   ││ Flow Arc    ││ Projection  │
 └─────────────┘└─────────────┘└─────────────┘└─────────────┘└─────────────┘
        │              │              │              │              │
        └──────────────┴──────────────┼──────────────┴──────────────┘
                                      ▼
               ┌──────────────────────────────────────────────┐
               │    Narrator Research Drawer & Rijāl Panel     │
               │  • Biographical card & Classical evaluations │
               │  • Direct teachers & Verified students       │
               │  • Tabaqah, Death AH, Geographic Center      │
               └──────────────────────────────────────────────┘
```

---

## 3. Data Invariants & Zero-Fabrication Rules

1. **No Date Invention:** If `death_year` is `null` or `0`, the transmitter is rendered with a distinct dashed visual perimeter and segregated into an "Undated Transmitters" scholarly drawer.
2. **No Speculative Geography:** A transmission edge between two geographical locations is drawn *if and only if* the database records an authentic student-to-teacher reception relationship between narrators associated with those centers.
3. **Canonical Identity Preservation:** When `resolve_identity=true` is toggled, transmitter nodes highlight verified cross-collection identity clusters (*canonical_rawi_id*) with confidence indicators (`CONFIRMED`, `HIGH_CONFIDENCE`).
4. **Accessible Matrix Fallback:** Every visualization provides an expandable semantic table listing all nodes, relationships, and metrics for screen readers and text-only research workflows.
