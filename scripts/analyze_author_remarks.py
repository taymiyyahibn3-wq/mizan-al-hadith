import sqlite3
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('data/hadith-kg.db')
c = conn.cursor()

def analyze_author_remarks(book_id, marker, scholar_name):
    c.execute(f"SELECT id, no_inbook, taraf_nass FROM hadiths WHERE book_id = ? AND taraf_nass LIKE ?", (book_id, f'%{marker}%'))
    rows = c.fetchall()
    print(f"\n==========================================")
    print(f"{scholar_name} (Book {book_id}): Total matching rows: {len(rows)}")
    
    multi_count = 0
    lengths = []
    
    for r in rows:
        hid, no_inbook, taraf = r
        matches = list(re.finditer(re.escape(marker), taraf))
        if len(matches) > 1:
            multi_count += 1
            
        # extract the text starting from marker
        first_idx = matches[0].start()
        extracted = taraf[first_idx:].strip()
        lengths.append(len(extracted))
        
    print(f"Rows with multiple markers: {multi_count}")
    print(f"Min length: {min(lengths)}, Max length: {max(lengths)}, Avg length: {sum(lengths)/len(lengths):.1f}")

analyze_author_remarks(4, "قال أبو داود", "Abu Dawud")
analyze_author_remarks(5, "قال أبو عبد الرحمن", "Al-Nasai")
