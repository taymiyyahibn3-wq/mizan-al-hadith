# MĪZĀN AL-ḤADĪTH — FRONTEND ARCHITECTURE & DESIGN SYSTEM SPECIFICATION
**Document Identifier:** `02_FRONTEND_ARCHITECTURE.md`  
**Certified System Baseline:** Phase 18 Certified Relational Graph  
**Version:** 2.0.0  
**Author:** Lead Frontend Architect & Scholarly Digital Humanities Engineer  

---

## 1. Architectural Philosophy & Guiding Principles

Mīzān al-Ḥadīth is an academic research platform designed for scholarly hadith exploration, biographical analysis (*rijāl*), isnād transmission modeling, and cross-collection textual variant synthesis. The frontend architecture is governed by five inviolable design principles:

1. **Scholarly Rigor Over Visual Gimmicks:**  
   Every node, link, score, and visualization must represent authentic, verified underlying database entities. No artistic embellishment or artificial clustering may be presented without strict relational grounding.
2. **Calm, Distraction-Free Visual Atmosphere:**  
   Inspired by classical Islamic manuscript aesthetics (warm ivory parchment, deep emerald, burnished gold, and charcoal ink), the interface prioritizes readability, typographic harmony, and long-session intellectual focus.
3. **Deterministic, Zero-Contamination Integrity:**  
   The frontend is strictly read-only with respect to canonical databases. It preserves 100% of Phase 18 certified baselines, quarantine boundaries (Zubayr quarantine), scholar grading attributions, and Record #428 scope.
4. **Lightweight, Native Performance:**  
   Avoid multi-megabyte visualization runtimes. Utilize hardware-accelerated SVG and pure HTML5 Canvas with sub-100ms render targets, responsive layout isolation, and minimal memory footprints.
5. **Universal Accessibility & Multilingual Parity:**  
   Equal scholarly usability across classical Arabic typography (with diacritics and correct RTL flow) and Latin transliteration, paired with keyboard accessibility and semantic fallbacks for all graphical data.

---

## 2. Technology Stack & Component Structure

```
                           MĪZĀN CLIENT ARCHITECTURE
                           
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Next.js 16 (App Router)                           │
│  ┌──────────────────────┬──────────────────────┬─────────────────────────┐  │
│  │   Research Views     │   Visualization      │    Scholarly Registry   │  │
│  │  • Homepage (/)      │  • Isnād Timeline    │  • 425-Book Catalog     │  │
│  │  • Hadith View ([id])│  • Isnād Map         │  • Biographical Rijāl   │  │
│  │  • Search (/search)  │  • Isnād Atlas       │  • Data Provenance      │  │
│  │  • Ask Mizan (/ask)  │  • Isnād 3D Spatial  │  • Cover Registry       │  │
│  │                      │  • Matn Diff & 3D    │  • License Registry     │  │
│  └──────────────────────┴──────────────────────┴─────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                     Shared Component Subsystem                        │  │
│  │  • SiteChrome (Header, Footer, Navigation, Breadcrumbs)               │  │
│  │  • SihahSittahCollectionGrid & ClassicalBookCover                     │  │
│  │  • ScholarlyStatementCard & CitationChip                              │  │
│  │  • TextDiffViewer (Synchronized Arabic variant alignment)            │  │
│  │  • NarratorResearchDrawer & LegendDrawer                              │  │
│  │  • AccessibleDataFallbackTable (Screen-reader visualization matrix)   │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                       Design Tokens & Styling                         │  │
│  │  • Tailwind CSS v4 + Semantic CSS Custom Properties                   │  │
│  │  • Classical Typography: Amiri, Scheherazade New, Cinzel, Inter      │  │
│  │  • Motion Engine: CSS cubic-bezier transitions + Reduced-Motion Gate  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ HTTP / JSON (Read-Only)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FastAPI Backend Layer (:8000)                        │
│  ┌──────────────────────┬──────────────────────┬─────────────────────────┐  │
│  │   /api/stats         │   /api/isnad/*       │   /api/hadith/*         │  │
│  │   /api/books/*       │   /api/narrator/*    │   /api/hadith-visualizer│  │
│  │   /api/commentary/*  │   /api/grades/*      │   /api/ask/*            │  │
│  └──────────────────────┴──────────────────────┴─────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                       Canonical Databases (SQLite)                    │  │
│  │  • hadith-kg.db (Core Mutūn, Books, Rawis, Sanads)                    │  │
│  │  • hadith_numbering.db (Authoritative & Concordance Numbering)        │  │
│  │  • citation_enrichment.db (Takhrij & Scholarly Crosswalks)            │  │
│  │  • hadith_commentaries.db (Classical Sharh & Hashiyah)                │  │
│  │  • isnad_network.db & english-search.db & hadith-search-index.db      │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Design System Tokens & Color Palette

All colors adhere to WCAG 2.1 AA contrast requirements against their respective backgrounds (minimum 4.5:1 for body copy, 3:1 for large headers).

```css
:root {
  /* Surface Layers (Parchment & Warm Ivory) */
  --bg-parchment: #f5f1e8;
  --bg-ivory: #fdfbf7;
  --bg-cream: #f7f2e6;
  --bg-elevated: #ffffff;
  --bg-card-hover: #fcf9f2;

  /* Primary Scholarly Identity (Deep Forest Emerald) */
  --emerald-950: #0a2921;
  --emerald-900: #123d32;
  --emerald-800: #195143; /* Primary Brand Color */
  --emerald-700: #226b58;
  --emerald-100: #e2ede8;
  --emerald-50:  #f0f6f3;

  /* Antique Illumination Accents (Burnished Manuscript Gold) */
  --gold-900: #573f18;
  --gold-800: #6e5020;
  --gold-600: #a77c38; /* Primary Accent */
  --gold-500: #c99b4f;
  --gold-200: #dcc8a4;
  --gold-100: #f4ebd6;
  --gold-50:  #fcf8f0;

  /* Typographic Ink Colors */
  --ink-primary:   #181c1a; /* 16.2:1 contrast against --bg-parchment */
  --ink-secondary: #333a36; /* 9.8:1 contrast */
  --ink-muted:     #626b66; /* 4.9:1 contrast */
  --ink-faint:     #8f9893;

  /* Borders & Dividers */
  --border-strong: #cfc5b4;
  --border-subtle: #e3dcce;
  --border-faint:  #eee7db;

  /* Shadows */
  --shadow-sm: 0 1px 3px rgba(24, 28, 26, 0.05);
  --shadow-md: 0 4px 14px rgba(24, 28, 26, 0.07);
  --shadow-lg: 0 12px 32px rgba(24, 28, 26, 0.09);
  --shadow-book: 0 18px 40px rgba(18, 28, 24, 0.18);
}
```

---

## 4. Typography Hierarchy & Font Loading Strategy

### Font Stacks
1. **Classical Arabic:** `"Amiri", "Scheherazade New", "Traditional Arabic", serif`
   - Optimal for vowelled and unvowelled mutūn, honoring classical calligraphic proportions.
   - Text rendering: `font-feature-settings: "cv01" on, "ss01" on; -webkit-font-smoothing: antialiased;`
2. **Scholarly Latin Serif:** `"Cinzel", "Playfair Display", Georgia, serif`
   - Applied to book titles, Latin transliterations, author names, and chapter headers.
3. **Functional UI Sans-Serif:** `"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`
   - Clean, highly legible at small sizes (11px–14px) for telemetry badges, tabular metadata, and navigational controls.

### Zero-CLS Font Loading
Replace render-blocking `@import` statements in `globals.css` with `<link rel="preconnect">` and `<link rel="stylesheet">` with `display=swap`, or standard font-family fallbacks with matching cap-height/x-height metrics to eliminate layout shift during initialization.

---

## 5. Unified API Service Layer (`src/lib/api.ts`)

All frontend components communicate with the backend through a hardened, typed API client featuring:
- Standardized request timeout (10 seconds)
- Automated request deduplication for idempotent GET endpoints
- Consistent error formatting with human-readable scholarly fallbacks
- Origin auto-detection (handling `localhost` vs `127.0.0.1` port mismatches)

```typescript
export interface ApiResponse<T> {
  data: T | null;
  error: string | null;
  loading: boolean;
}
```

---

## 6. Visualization Subsystem Architecture

The visualization subsystem is partitioned into coordinated specialized views:

| Module | Location | Primary Technology | Analytical Focus |
| :--- | :--- | :--- | :--- |
| **Isnād Timeline** | `src/app/isnad/TimelineView.tsx` | SVG + Canvas | Temporal succession, generational layers (*Tabaqāt*), branching, and divergence. |
| **Isnād Geography** | `src/app/isnad/MapView.tsx` | Projected Vector Map (SVG) | Spatial distribution of narrators across 12 historical Islamic scholarship centers. |
| **Isnād Atlas** | `src/app/isnad/AtlasView.tsx` | Coordinated SVG Vector Flow | Dynamic transmission routes connecting teacher and student regional hubs. |
| **Isnād 3D Spatial** | `src/app/isnad/ThreeDView.tsx` | Pure HTML5 Canvas 3D Engine | Multi-dimensional projection (X: Time, Y: Tabaqah, Z: Degree/Riwayah). |
| **Matn Visualizer** | `src/app/hadith-visualizer/page.tsx` | Radial Variant Graph (SVG) | Cross-collection textual similarity percentages and variant relationships. |
| **Matn Comparative Diff**| `src/app/components/MatnDiffViewer.tsx`| Side-by-Side Dual Pane (HTML/CSS)| Phrase-level token diffing, highlighting identical, variant, and omitted wording. |
| **Matn 3D Cluster** | `src/app/hadith-visualizer/MatnThreeDView.tsx`| HTML5 Canvas 3D Space | Spatial cluster mapping of textual witnesses based on token overlap. |

---

## 7. Reduced-Motion & Hardware Compatibility Gates

Every visualization incorporates an explicit performance and accessibility gate:
1. If `window.matchMedia('(prefers-reduced-motion: reduce)').matches` is `true`, all continuous particle flows, orbital rotations, and pulse animations are immediately suspended.
2. If canvas frame rate drops below 30 FPS or the client is detected as a low-memory mobile device, the system automatically falls back to static 2D vector rendering.
3. Every graphical visualization is accompanied by an accessible tabular matrix displaying the same relational data in semantic HTML.
