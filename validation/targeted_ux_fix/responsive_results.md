# Responsive Design Validation (320px Mobile, Tablet, Desktop)

## Viewport Verification Matrix

### 1. Mobile (320px – 480px)
- **Search Bar Layout**:
  - Container width expands smoothly to `calc(100% - 12px)` at 360px and `calc(100% - 20px)` at 480px.
  - `.searchbox` switches to `flex-direction: column` with `padding: 10px` and `gap: 0.5rem`.
  - Input field takes `width: 100%` with clear placeholder text.
  - Submit button expands to `width: 100%` (`.searchbox .primary-btn`), centered directly beneath input without clipping or horizontal overflow.
  - Suggested inquiry chips wrap naturally with tight chip margins and zero overflow.
- **Narrator Biography**:
  - Biographical metrics cards stack gracefully into 2 columns on small screens, dropping to single column if required.
  - Onomastic components (Kunyah, Laqab, Nisbah) wrap cleanly.
  - Scholarly Statements research controls stack vertically (Search input -> Scholar select -> Group by toggle).
  - Arabic text maintains adequate line height (`line-height: 2.0`) and readable Naskh font size without horizontal clipping.
  - Transmission cards stack cleanly with 100% width button for the Isnād Network Visualizer link.

### 2. Tablet (768px – 1024px)
- **Search Bar Layout**:
  - Responsive container width `calc(100% - 32px)`.
  - Clean inline or stacked transitions at the 768px breakpoint.
  - Suggested inquiry chips center neatly beneath the form.
- **Narrator Biography**:
  - Biographical metrics grid renders in 4 columns.
  - Onomastic grid renders in 2–3 columns.
  - Scholarly Statements toolbar aligns horizontally.
  - Grouped scholar cards display scholar name and statement count side-by-side with death year badges.

### 3. Desktop (1280px – 1920px)
- **Search Bar Layout**:
  - Primary focal search form occupies `w-full max-w-5xl` (1040px max-width).
  - Generous height, centered icon, expansive input font size, and emerald/gold focus ring.
  - Language switch tabs and suggested query chips align with the form's golden balance geometry.
- **Narrator Biography**:
  - Full-width scholarly layout with rich typographic hierarchy.
  - Interactive research toolbar allows fast switching between Chronological List and Group by Scholar view.
  - Large statement lists load progressively without slowing DOM rendering.
