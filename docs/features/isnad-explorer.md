# FEATURE — ISNĀD TOPOLOGY EXPLORER

**Document Identifier:** `docs/features/isnad-explorer.md`  
**Frontend Route:** `/isnad`  
**Backend Endpoints:** `/api/isnad/{id}`, `/api/isnad/stats`, `/api/isnad/path`  

---

## 1. Overview & Capabilities

The Isnād Topology Explorer transforms complex textual chains of transmission into intuitive, interactive mathematical graphs. It enables scholars to inspect transmission bottlenecks, identify common transmitters (*Madār al-Ḥadīth*), and trace the geographic migration of traditions.

---

## 2. Four Interactive Visualization Perspectives

The `/isnad` interface provides four coordinated visualization modes:

### 2.1 2D Transmission Graph (`GraphView.tsx`)
- Directed acyclic graph (DAG) showing transmission flow from Prophet Muhammad ﷺ and the Companions through successive generations down to the classical author.
- Node sizing proportional to in-degree / out-degree centrality.
- Color-coded by reliability rank (*Thiqah* = Emerald, *Saduq* = Teal, *Da'if* = Amber/Rose).
- Edge weights indicating the frequency of direct transmission across the Six Books.

### 2.2 Generational Chronological Timeline (`TimelineView.tsx`)
- Arranges transmitters across a chronological timeline from 1 AH to 300 AH.
- Groups transmitters by scholarly generation tier (Companions, Senior Tabi'in, Younger Tabi'in, Successors).
- Visualizes teacher-student transmission spans to highlight temporal overlap.

### 2.3 Historical Geographical Atlas (`AtlasView.tsx` & `MapView.tsx`)
- Maps transmission centers onto historical Islamic geography.
- Features **12 canonical transmission hubs**: Madinah, Makkah, Kufa, Basra, Baghdad, Damascus, Cairo, Nishapur, Rayy, San'a, Bukhara, and Balkh.
- Visualizes the geographic migration of narrations from the Hijaz across Iraq, the Levant, and Khurasan.

### 2.4 3D Spatial Transmission Space (`SpatialView.tsx`)
- Renders the transmission network in three-dimensional interactive space.
- Allows rotational orbit and spatial exploration of high-density transmission clusters.

---

## 3. Data Model & Graph Engine

- **Precomputed Topology:** Stored in `data/isnad_network.db` containing **49,844 narrator nodes** and **298,655 directed transmission edges**.
- **On-the-Fly Isnād Extraction:** For individual hadiths, `/api/isnad/{id}` traverses the canonical `sanads` and `sanad_rawis` tables to construct the specific sub-network for that narration.
