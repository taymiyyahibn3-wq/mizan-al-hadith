import sys
import os
import sqlite3

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.abspath("mizan-web/backend"))
sys.path.insert(0, os.path.abspath("."))

from sanad_aligner import align_hadith_sanad_narrators

db = sqlite3.connect("data/hadith-kg.db")
db.row_factory = sqlite3.Row

# Hadith 1
h1 = db.execute("SELECT id, nass, taraf_nass, matn, matn_start FROM hadiths WHERE id = 1").fetchone()
nass1 = h1["nass"] or h1["taraf_nass"]
spans1 = align_hadith_sanad_narrators(db, 1, nass1, h1["matn_start"])
print(f"Hadith 1: found {len(spans1)} spans in text (len={len(nass1)}):")
for s in spans1:
    print(f"   • rawi_id={s['rawi_id']}, span=[{s['start']}:{s['end']}], text='{s['display_text']}', name='{s['name']}'")

# Hadith 20918 (Nasa'i #4)
h20918 = db.execute("SELECT id, nass, taraf_nass, matn, matn_start FROM hadiths WHERE id = 20918").fetchone()
nass20918 = h20918["nass"] or h20918["taraf_nass"]
spans20918 = align_hadith_sanad_narrators(db, 20918, nass20918, h20918["matn_start"])
print(f"\nHadith 20918 (Nasa'i #4): found {len(spans20918)} spans in text (len={len(nass20918)}):")
for s in spans20918:
    print(f"   • rawi_id={s['rawi_id']}, span=[{s['start']}:{s['end']}], text='{s['display_text']}', name='{s['name']}'")
