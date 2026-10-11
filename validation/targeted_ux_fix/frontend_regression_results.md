# Frontend Regression Results

Comprehensive testing was conducted on the running Next.js application across all core workflows.

## 1. Regression Checklist

| Test Target | Component / Route | Verification Detail | Status |
|---|---|---|---|
| **Homepage Search** | `/` | Desktop search bar widened to `max-w-5xl` (1040px max width). Form input and button stay centered and prominently positioned. | ✅ PASS |
| **Arabic Search** | `/` (`lang=ar`) | Searching classical terms (e.g., `إنما الأعمال بالنيات`) correctly triggers `/api/hadith/search` with RTL input alignment. | ✅ PASS |
| **English Search** | `/` (`lang=en`) | Searching English terms (e.g., `prayer`) queries `/api/hadith/search/en` via `english_translation_fts.db`, returning relevant hits with LTR layout. | ✅ PASS |
| **Hadith Detail Page** | `/hadith/1` | Bukhari 1 narration details, translations, Isnād chain, commentaries, and numbering load normally. Scholarly Statements tab correctly displays narrator statements (57 statements for narrators in chain). | ✅ PASS |
| **Chain Annotations Removed** | `/hadith/1` | "Chain Annotations" tab button, badge, and panel are completely absent from the DOM and tab bar. | ✅ PASS |
| **Narrator Biography Page** | `/narrator/3443` | Clean scholarly biography loaded: Name → Arabic Name → Basic Biographical Info → Scholarly Statements → Transmission/Isnād Network. | ✅ PASS |
| **Dossier Framing Absent** | `/narrator/3443` | "Canonical Narrator Dossier" framing, DNA icon, candidate scoring drawer, and duplicate record cards are completely removed. | ✅ PASS |
| **Add Research Notes Absent** | `/narrator/3443` | "Add Research Notes" form, textarea, button, and annotation modal are completely removed. | ✅ PASS |
| **Multiple Statements Transmitters** | `/narrator/2288`, `/narrator/3443`, `/narrator/4364` | Transmitters with 28–44 statements load full sets. Scholar grouping and search filter functions accurately without truncation. | ✅ PASS |
| **Zero Statements Transmitter** | `/narrator/581` | Displays the exact required copy: *“No scholarly statement is currently available in the verified source data.”* | ✅ PASS |
| **Collision Safety Rule** | `/narrator/4256` | Rawi 4256 correctly attaches critical attribution caveat to Yahya ibn Ma'in's tawthiq without breaking display. | ✅ PASS |
| **TypeScript Compilation** | `mizan-web/frontend` | `npx tsc --noEmit` exits with code 0 (zero errors, zero warnings). | ✅ PASS |
