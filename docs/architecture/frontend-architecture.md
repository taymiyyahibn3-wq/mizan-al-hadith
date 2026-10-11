# MĪZĀN AL-ḤADĪTH — FRONTEND ARCHITECTURE

**Document Identifier:** `docs/architecture/frontend-architecture.md`  
**Subsystem Directory:** `mizan-web/frontend`  
**Framework:** Next.js 16.3.6 (App Router) · React 19.2.8 · Tailwind CSS 4.0  

---

## 1. Architectural Philosophy & Design Principles

The Mīzān frontend is engineered to fulfill the aesthetic, scholarly, and computational demands of serious Islamic digital humanities:
1. **Restrained Scholarly Identity:** Deep heritage green (`#0d3826`), warm parchment/stone surfaces (`#fcfbf7` to `#f7f5ed`), subtle gold accents (`#c5a059`), and crisp typographic hierarchy.
2. **Native Arabic Typography:** Optimized rendering of Arabic script using modern typography (`Amiri`, `Scheherazade New`, and traditional Naskh fallbacks) with proper diacritical mark positioning and bidirectional text (`dir="rtl"`) handling.
3. **Zero Heavy Bloat:** No massive monolithic UI component libraries (such as MUI or Ant Design). All components are bespoke, lightweight React components styled via Tailwind CSS utilities.
4. **Resilient API Layer:** The API client in `src/lib/api.ts` provides typed, fault-tolerant fetching with automatic timeout handling and informative error fallbacks.

---

## 2. Route Hierarchy & Page Component Inventory

```
mizan-web/frontend/src/app/
├── layout.tsx                                 # Root layout with HTML/body, font declarations & SiteChrome
├── page.tsx                                   # Homepage / Landing portal
├── globals.css                                # Design tokens, CSS custom properties & base resets
│
├── books/                                     # Canonical Hadith Library
│   ├── page.tsx                               # Sihah Sittah catalog showcase & volume statistics
│   └── [id]/page.tsx                          # Book detail, chapter navigation & hadith pagination
│
├── hadith/                                    # Deep Hadith Detail Reader
│   └── [id]/page.tsx                          # Arabic matn, English translation, isnād breakdown,
│                                              # commentary drawer, grading matrix & bookmarking
│
├── narrators/                                 # Biographical Narrator Catalog
│   ├── page.tsx                               # Narrator search, rank filters & alphabetical index
│   └── [id]/page.tsx                          # Detailed narrator profile, jarḥ wa taʿdīl statements,
│                                              # transmission span & teacher/student connections
│
├── search/                                    # Unified Multi-Modal Search Interface
│   └── page.tsx                               # Instant search across Arabic, English, Rawis & Concordances
│
├── ask/                                       # Ask Mīzān Grounded AI Research Assistant
│   └── page.tsx                               # Multi-turn conversation, streaming, citation chips & feedback
│
├── isnad/                                     # Isnād Topology Explorer
│   ├── page.tsx                               # View selector (2D Graph, Timeline, Map, Atlas, 3D Spatial)
│   ├── GraphView.tsx                          # SVG directed transmission graph
│   ├── TimelineView.tsx                       # Generational chronology (1 AH to 300 AH)
│   ├── MapView.tsx                            # 2D Islamic transmission geography
│   ├── AtlasView.tsx                          # Historical regional centers (Madinah, Kufa, Basra, etc.)
│   ├── SpatialView.tsx                        # 3D spatial transmission visualization
│   ├── NarratorResearchPanel.tsx              # Deep biographical inspection slide-over
│   └── geoData.ts                             # Verified coordinates for 12 canonical transmission hubs
│
├── hadith-visualizer/                         # Matn Variant & Diff Visualizer
│   └── page.tsx                               # Side-by-side textual diffing with token-level highlights
│
├── workspace/                                 # Scholarly Research Workspace
│   ├── page.tsx                               # Workspace dashboard, project cards & activity stats
│   └── [projectId]/page.tsx                   # Project editor: Evidence library, notes, claim-evidence matrix,
│                                              # side-by-side comparison & dossier export
│
├── info/                                      # System Information & Methodological Safeguards
│   └── page.tsx                               # Technical overview, provenance register & limitations
│
└── contact/                                   # Contact & Institutional Information
    └── page.tsx                               # Academic contact and collaboration details
```

---

## 3. Specialized Reusable Components (`src/app/components/`)

| Component | File Path | Role & Capabilities |
| :--- | :--- | :--- |
| **SiteChrome** | `src/app/components/SiteChrome.tsx` | Global top navigation bar, active route highlighting, mobile drawer, and footer. |
| **BookShowcase** | `src/app/components/BookShowcase.tsx` | Interactive cover cards for the Six Canonical Books with verified cover art and record counts. |
| **AnimatedStatCounter** | `src/app/components/AnimatedStatCounter.tsx` | Smooth counter animating verified platform figures (715k ahadith, 49k rawis, 298k edges). |
| **MatnDiffViewer** | `src/app/components/MatnDiffViewer.tsx` | Word-by-word token diffing highlighting additions (green), deletions (rose), and matching stems. |
| **ScholarlyStatementCard**| `src/app/components/ScholarlyStatementCard.tsx`| Renders classical scholar verdicts with verified badges, provenance references, and collision alerts. |
| **ScholarlyAnnotationPanel**| `src/app/components/ScholarlyAnnotationPanel.tsx`| Displays classical author remarks (e.g. Abu 'Isa al-Tirmidhi's *hukum*) alongside the text. |
| **HadithCommentarySection**| `src/app/components/HadithCommentarySection.tsx`| Collapsible drawer presenting classical commentary excerpts (*Fatḥ al-Bārī*, etc.) with volume/page tags. |
| **CitationChip** | `src/app/components/CitationChip.tsx` | Clickable citation badge linking Ask Mīzān answers directly to canonical hadith records. |
| **SaveToWorkspaceModal** | `src/app/components/SaveToWorkspaceModal.tsx` | Modal dialogue allowing researchers to bookmark hadiths directly into private workspace projects. |
| **HadithWorkspaceBookmarkButton** | `src/app/components/HadithWorkspaceBookmarkButton.tsx` | Quick-save button integrated into the Hadith Detail reader. |
| **HeroCalligraphy** | `src/app/components/HeroCalligraphy.tsx` | Verified SVG calligraphy rendering «ميزان الحديث». |
| **MizanBalanceMotif** | `src/app/components/MizanBalanceMotif.tsx` | Geometric scales-of-justice visual motif representing balance (*Mīzān*). |
| **HeroBackgroundGeometry** | `src/app/components/HeroBackgroundGeometry.tsx` | Subtle Islamic geometric background lattice rendered in pure CSS/SVG. |

---

## 4. Client-Side API Integration (`src/lib/api.ts`)

The frontend interacts with backend endpoints via typed wrapper functions in `src/lib/api.ts`:
- Automatic JSON header inclusion and query string serialization.
- Dynamic detection of `X-Researcher-Id` from local storage for workspace sessions.
- Graceful error boundary support: API failures return structured error messages instead of crashing client components.
