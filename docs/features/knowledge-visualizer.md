# FEATURE — KNOWLEDGE GRAPH & RELATION VISUALIZER

**Document Identifier:** `docs/features/knowledge-visualizer.md`  
**Frontend Routes:** Integrated across `/hadith/[id]`, `/isnad`, `/hadith-visualizer`  
**Backend Endpoints:** `/api/isnad/{id}`, `/api/narrator/{id}/network`  

---

## 1. Overview & Capabilities

The Knowledge Graph Visualizer exposes the multi-dimensional relationships linking Hadiths, Narrators, Scholarly Evaluations, and Canonical Books.

### Key Visualizations:
1. **Narration Transmission Clusters:** Visualizing how multiple chains converge on a common narrator (*Madār*), such as al-Zuhri, Yahya ibn Sa'id al-Ansari, or Qatadah.
2. **Book-Aware Subnetworks:** Filtering transmission edges to display only asānīd recorded by specific authors (e.g. Sahih al-Bukhari vs Sahih Muslim).
3. **Interactive Node Inspector:** Clicking any transmitter node in the graph opens a biographical drawer (`NarratorResearchPanel.tsx`) showing exact death year, rank, and teachers without leaving the visualizer.

---

## 2. Technical Implementation

- **Graph Model:** Directed Multigraph loaded from `data/isnad_network.db`.
- **Centrality Metrics:** In-degree and out-degree metrics calculated pre-run to ensure instant layout rendering.
- **Accessibility:** Textual equivalent lists provided alongside graphical canvases for keyboard navigation and screen readers.
