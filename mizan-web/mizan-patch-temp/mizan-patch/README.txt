MIZAN AL-HADITH — UI PATCH

Changes:
- Reworked global navigation with desktop links + accessible mobile drawer.
- Removed visible mojibake from the homepage copy.
- Refined emerald/parchment/brass visual system without changing the research architecture.
- Improved homepage search/error/loading presentation.
- Improved Six Books showcase and reusable cover fallback.
- Added reliable cover fallback to the catalogue cards too.
- Improved library catalogue loading/error/empty states.
- Preserved existing backend search endpoints and their behavior.
- Backend main.py change is intentionally limited to user-facing mojibake strings.

Validation performed here:
- backend_main.py passes Python syntax compilation.
- TSX files passed basic source checks; full Next.js build must be run in the user's local project because node_modules/project config are not part of this patch runtime.

Apply with PowerShell:
  Set-ExecutionPolicy -Scope Process Bypass
  .\apply-mizan-patch.ps1

The script automatically creates a timestamped backup before replacing files.
