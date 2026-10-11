import sqlite3
import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('file:data/hadith-kg.db?mode=ro', uri=True)
c = conn.cursor()

# Query all hadiths in Book 3
rows = c.execute("""
    SELECT id, no_inbook, page_no, taraf_nass, nass 
    FROM hadiths 
    WHERE book_id = 3 
    ORDER BY no_inbook
""").fetchall()

print(f"Total Hadiths in Book 3: {len(rows)}")

extracted = []
unparsed_qala = []

# Regular expressions for Tirmidhi statements
# Commonly: "قال أبو عيسى هذا حديث [GRADE]" or "قال أبو عيسى حديث [NARRATOR] حديث [GRADE]"
pattern_direct = re.compile(r'قال أبو عيسى\s+(?:هذا\s+)?حديث\s+([^،\.\n]+?)(?:وقد|وروي|وفي|وهذا|والعمل|وقد روي|سمعت|حدثنا|$)')
pattern_general = re.compile(r'قال أبو عيسى\s+([^،\.\n]+)')

grade_counts = {}

for r in rows:
    hid, no_inbook, pg, taraf, nass = r
    if not taraf:
        continue
    
    idx = taraf.find("قال أبو عيسى")
    if idx != -1:
        stmt = taraf[idx:].strip()
        # Clean up trailing text
        m = re.search(r'قال أبو عيسى\s+(هذا حديث [^،\.\n]+?)(?:\s+وفي الباب|\s+وقد روي|\s+وهذا حديث|\s+سمعت|\s+حدثنا|\s+والعمل|\.|$)', stmt)
        if not m:
            m = re.search(r'قال أبو عيسى\s+(حديث [^،\.\n]+? حديث [^،\.\n]+?)(?:\s+وفي الباب|\s+وقد روي|\s+وهذا حديث|\s+سمعت|\s+حدثنا|\s+والعمل|\.|$)', stmt)
        if not m:
            m = re.search(r'قال أبو عيسى\s+(هذا الحديث [^،\.\n]+?)(?:\s+وفي الباب|\s+وقد روي|\s+وهذا حديث|\s+سمعت|\s+حدثنا|\s+والعمل|\.|$)', stmt)
        
        extracted_text = m.group(1).strip() if m else stmt[:80]
        
        # Categorize
        is_grade = False
        grade_term = None
        for term in ["حسن صحيح غريب", "حسن صحيح", "حسن غريب", "صحيح غريب", "حسن", "صحيح", "غريب", "ليس إسناده بذاك", "ضعيف", "منكر", "أصح شيء"]:
            if term in extracted_text:
                is_grade = True
                grade_term = term
                break
        
        item = {
            "hadith_id": hid,
            "no_inbook": no_inbook,
            "raw_statement": stmt[:150],
            "extracted_text": extracted_text,
            "grade_term": grade_term,
            "is_grade": is_grade
        }
        extracted.append(item)
        if grade_term:
            grade_counts[grade_term] = grade_counts.get(grade_term, 0) + 1

print(f"\nExtracted statements: {len(extracted):,}")
print("Grade terminology breakdown in Jami' al-Tirmidhi:")
for k, v in sorted(grade_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {k}: {v:,}")

conn.close()
