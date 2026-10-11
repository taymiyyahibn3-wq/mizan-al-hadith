import sqlite3
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect("file:data/hadith-kg.db?mode=ro", uri=True)
rows = conn.execute("SELECT no_inbook, taraf_nass FROM hadiths WHERE book_id = 3").fetchall()

patterns = [
    ("هذا حديث حسن صحيح غريب", r'هذا حديث حسن صحيح غريب'),
    ("هذا حديث حسن صحيح", r'هذا حديث حسن صحيح(?! غريب)'),
    ("هذا حديث حسن غريب", r'هذا حديث حسن غريب'),
    ("هذا حديث صحيح غريب", r'هذا حديث صحيح غريب'),
    ("هذا حديث حسن", r'هذا حديث حسن(?! صحيح| غريب)'),
    ("هذا حديث صحيح", r'هذا حديث صحيح(?! غريب)'),
    ("هذا حديث غريب", r'هذا حديث غريب(?! لا نعرفه)'),
    ("هذا حديث ضعيف", r'هذا حديث ضعيف'),
    ("حديث ... حسن صحيح", r'حديث (?:[^\n،\.]+?) حسن صحيح'),
    ("حديث ... حسن غريب", r'حديث (?:[^\n،\.]+?) حسن غريب'),
    ("حديث ... غريب", r'حديث (?:[^\n،\.]+?) غريب'),
    ("حديث ... حسن", r'حديث (?:[^\n،\.]+?) حسن(?! صحيح| غريب)'),
    ("حديث ... صحيح", r'حديث (?:[^\n،\.]+?) صحيح(?! غريب)'),
]

total_set = set()
for name, pat in patterns:
    matches = [r[0] for r in rows if r[1] and re.search(pat, r[1])]
    print(f"{name}: {len(matches)}")
    total_set.update(matches)

print(f"\nTotal unique hadiths with genuine explicit grade formulas: {len(total_set)}")

conn.close()
