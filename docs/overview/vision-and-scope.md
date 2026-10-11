# MĪZĀN AL-ḤADĪTH — VISION & RESEARCH SCOPE

**Document Identifier:** `docs/overview/vision-and-scope.md`  
**System Baseline:** Production Relational Graph & Hybrid Retrieval v2  

---

## 1. The Scholarly Challenge

For over fourteen centuries, the science of Hadith (*ʿIlm al-Ḥadīth*) has preserved the oral and textual transmissions of Prophet Muhammad ﷺ through rigorous biographical critique (*ʿIlm al-Rijāl*), chain evaluation (*Taḥqīq al-Asānīd*), and comparative textual analysis (*Muʿāraḍat al-Mutūn*).

However, modern digital Hadith tools frequently suffer from major methodological failures:
1. **Unmoored Large Language Models:** Generic AI models fabricate hadith texts, invent non-existent transmission chains, or present weak fabricated narrations as authentic without classical citations.
2. **Concordance Fragmentation:** A hadith numbered #1986 in the international Darussalam English edition often corresponds to #1976 in the classical Fu'ad 'Abd al-Baqi edition, or #493 in classical Bulaq printings. Researchers waste countless hours reconciling references across printed volumes.
3. **Loss of Isnād Topology:** Traditional websites present isnāds as flat text strings, obscuring complex transmission networks, common transmitters (*Madār al-Ḥadīth*), and regional transmission hubs (Madinah, Kufa, Basra, Baghdad).
4. **Conflation of Editorial Views with Primary Evidence:** Modern editorial judgments (e.g., modern gradings by al-Albani or Zubair Ali Zai) are frequently conflated with classical consensus or author evaluations (e.g., Imam al-Tirmidhi's *al-Jāmiʿ*).

---

## 2. The Mīzān Vision (ميزان الحديث)

**Mīzān al-Ḥadīth** ("The Scale of Hadith") bridges classical Islamic scholarship with state-of-the-art computational humanities.

```
       +-------------------------------------------------------------+
       |               CANONICAL HERITAGE PRESERVATION               |
       |  Immutable Primary Texts · Classical Jarḥ wa Taʿdīl (127k)  |
       +------------------------------+------------------------------+
                                      |
                                      v
       +-------------------------------------------------------------+
       |              DETERMINISTIC RELATIONAL GRAPH                 |
       |  Isnād Network (298k Edges) · 18 Numbering Crosswalks (95k)  |
       +------------------------------+------------------------------+
                                      |
                                      v
       +-------------------------------------------------------------+
       |             VERIFIABLE HYBRID RETRIEVAL ENGINE              |
       |   FTS5 Lexical Search + Embedding Vector Rerank + Routing   |
       +------------------------------+------------------------------+
                                      |
                                      v
       +-------------------------------------------------------------+
       |               SCHOLARLY RESEARCH WORKSPACE                  |
       | Isolated Projects · Claim-Evidence Matrix · Dossier Exports |
       +-------------------------------------------------------------+
```

### Core Invariants:
1. **Canonical Immutability:** Primary classical texts (`hadith-kg.db`) are strictly read-only. No machine learning model or researcher can mutate historical transmission records.
2. **Strict Grounding:** Every statement produced by the AI research assistant ("Ask Mīzān") must cite specific canonical hadith IDs or biographical records verified in the evidence pack. Hallucinated tokens are automatically purged.
3. **Demarcation of Scholarly Tiers:**
   - **Tier 1 (Canonical Source):** Primary matn and isnād from historical manuscripts and recognized printings.
   - **Tier 2 (Classical Commentary):** Historical scholarly remarks (*Fatḥ al-Bārī*, *Sharḥ Ṣaḥīḥ Muslim*, etc.).
   - **Tier 3 (Modern Editorial / Analytical):** Modern crosswalk mappings, editorial gradings, and computational topological metrics.
   - **Tier 4 (Researcher Workspace):** Private notes, hypotheses, and draft claim matrices authored by the researcher.

---

## 3. Scope & Target Audience

### Target Users:
- **Academic Researchers & Digital Humanists:** Analyzing transmission dynamics, lexical evolution, and geographical diffusion of traditions across the Islamic world.
- **Traditional Islamic Scholars & Students of Knowledge (*Ṭullāb al-ʿIlm*):** Cross-referencing complex hadith numbering across international print editions, accessing classical commentaries, and verifying narrator biographies.
- **Developers & Data Scientists:** Utilizing the 95 REST API endpoints to build reproducible Islamic studies tools, citation visualizers, and academic corpora.

### Explicit Limitations (What Mīzān Does Not Claim):
- Mīzān is **not a mufti or automated fatwa issuer**. It does not perform legal derivation (*Ijtihād*) or issue legal rulings (*Aḥkām Fiqhiyyah*).
- Lexical similarity scores between texts are **analytical aids**, not proof of identical transmission or authentic provenance.
- A topological transmission link indicates that narrator A narrated to narrator B in a documented isnād; it is not an endorsement of personal reliability or continuity without considering *tadlīs* or *inqiṭāʿ*.
