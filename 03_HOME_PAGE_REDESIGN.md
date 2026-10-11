# MĪZĀN AL-ḤADĪTH — HOMEPAGE REDESIGN SPECIFICATION
**Document Identifier:** `03_HOME_PAGE_REDESIGN.md`  
**Certified System Baseline:** Phase 18 Certified Relational Graph  
**Version:** 2.0.0  
**Author:** Lead Frontend Architect & Visual Design Director  

---

## 1. Core Mission & Information Architecture

The redesigned homepage communicates two fundamental answers within the first three seconds of user interaction:
1. **"What is MĪZĀN AL-ḤADĪTH?"**  
   An authoritative computational research platform for the classical Arabic hadith corpus, providing primary-text normalization, verified English translations, biographical transmitter graphs (*rijāl*), and certified scholarly grading chains.
2. **"What can I research here?"**  
   Six dedicated research pillars immediately visible above the fold and in primary navigation:
   - **Hadith Textual Search:** Instant Arabic full-text search (with diacritic stripping and alef/ya unification) and verified English translations.
   - **Isnād Transmission Explorer:** Multi-view chain analysis (Timeline, Map, Atlas, and 3D spatial layers).
   - **Matn Textual Variant Explorer:** Radial similarity graphs and phrase-level comparative diffing.
   - **Biographical Narrator Database (*Rijāl*):** 49,844 transmitter profiles with classical evaluations (*Jarḥ wa Taʿdīl*).
   - **Scholarly Authenticity & Grades:** Certified rulings from nine classical and contemporary authorities with transparent absence documentation.
   - **Classical Commentaries (*Shurūḥ*):** Verse-by-verse and hadith-by-hadith commentary synthesis (*Fatḥ al-Bārī*, *Sharḥ al-Nawawī*, *Tuḥfat al-Aḥwadhī*).

---

## 2. Structural Wireframe & Page Sections

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. SCHOLARLY HERO & DUAL-CORPUS SEARCH                                      │
│    • Eyebrow: "THE SCHOLARLY HADITH RESEARCH PLATFORM"                     │
│    • Title: "Read the Tradition. Trace the Chain."                         │
│    • Arabic / English Language Pill Switcher                                │
│    • Primary Search Box with real-time submit + quick query pills           │
│    • In-line Search Results Card Grid (rendered on search submit)           │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. REAL-TIME CORPUS TELEMETRY (Backend Stats Bar)                          │
│    • Hadiths Indexed: 715,790 | Collections: 425                            │
│    • Narrators (Rijāl): 49,844 | Verified Sanads: 300,000+                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. PRIMARY RESEARCH ENTRY POINTS (Six Coordinated Modules)                  │
│    [1. Hadith Search]     [2. Isnād Explorer]     [3. Matn Visualizer]      │
│    [4. Narrator Database] [5. Scholarly Grades]   [6. Classical Sharḥ]      │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. SIHAH SITTAH DIGITAL BOOKSHELF (Verified Sourced Editions)               │
│    • Interactive 3D Perspective Books with authentic sourced covers:         │
│      1. Ṣaḥīḥ al-Bukhārī   (Būlāq 1311 AH / Sultanic Title Page)             │
│      2. Ṣaḥīḥ Muslim       (Al-Amīrah Imperial Binding, 1334 AH)            │
│      3. Jāmiʿ al-Tirmidhī  (Halabi 1st Edition, 1356 AH / 1937 CE)          │
│      4. Sunan Abī Dāwūd    (Classical Moroccan Leather Binding)             │
│      5. Sunan al-Nasāʾī    (Documented Reference Edition)                   │
│      6. Sunan Ibn Mājah    (Documented Reference Edition)                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 5. METHODOLOGY & DATA INTEGRITY GUARANTEE BANNER                           │
│    • Phase 18 Forensic Grounding certification callout                      │
│    • Zero-Contamination policy statement & link to Data Provenance Registry │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Motion Design & Interaction Tokens

- **Subtle Entrance:** Elements reveal using a gentle stagger (`animation: fadeIn 0.4s var(--ease-scholarly)`).
- **Reduced-Motion Compliance:** In accordance with `prefers-reduced-motion: reduce`, all 3D rotations, perspective tilts, and continuous glows are immediately replaced by crisp static geometry.
- **Visual Calm:** Avoid constant bouncing or floating badges. Interactive state transitions (hover, focus-visible) use smooth 180ms ease transitions.
