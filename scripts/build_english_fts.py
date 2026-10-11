"""
Build the English Translation FTS5 search index for Mīzān al-Hadīth.

Sources: hadith_translations.db (verified, correctly mapped translations)
Output:  english_translation_fts.db

This creates an FTS5-indexed database for fast English translation search,
using ONLY verified translation records from hadith_translations.db that
correctly map to the main hadith-kg.db by hadith_id and book_id.
"""
import sqlite3
import os
import sys
import re
import time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
TRANS_DB_PATH = os.path.join(DATA_DIR, "hadith_translations.db")
MAIN_DB_PATH = os.path.join(DATA_DIR, "hadith-kg.db")
OUTPUT_DB_PATH = os.path.join(DATA_DIR, "english_translation_fts.db")

print("=" * 70)
print("BUILDING ENGLISH TRANSLATION FTS5 INDEX")
print("=" * 70)

if not os.path.exists(TRANS_DB_PATH):
    print(f"ERROR: Translation DB not found: {TRANS_DB_PATH}")
    sys.exit(1)

if not os.path.exists(MAIN_DB_PATH):
    print(f"ERROR: Main hadith DB not found: {MAIN_DB_PATH}")
    sys.exit(1)

# Remove old output if exists
if os.path.exists(OUTPUT_DB_PATH):
    os.remove(OUTPUT_DB_PATH)
    print(f"Removed existing: {OUTPUT_DB_PATH}")

# Open source databases
trans_db = sqlite3.connect(TRANS_DB_PATH)
trans_db.row_factory = sqlite3.Row

main_db = sqlite3.connect(MAIN_DB_PATH)
main_db.row_factory = sqlite3.Row

# Create output database
out_db = sqlite3.connect(OUTPUT_DB_PATH)
out_db.execute("PRAGMA journal_mode=WAL")
out_db.execute("PRAGMA synchronous=NORMAL")

# Create main table to hold searchable English translation records
out_db.execute("""
    CREATE TABLE english_translations (
        id INTEGER PRIMARY KEY,
        hadith_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        hadith_number INTEGER,
        translation_text TEXT NOT NULL,
        narrator TEXT,
        translator TEXT,
        edition TEXT,
        source_name TEXT,
        alignment_score REAL,
        verified INTEGER DEFAULT 0,
        book_name TEXT,
        book_english_name TEXT,
        book_transliteration TEXT,
        author_name TEXT,
        english_author TEXT
    )
""")

# Create the FTS5 virtual table
# content-table approach: FTS references the main table by rowid
out_db.execute("""
    CREATE VIRTUAL TABLE english_fts USING fts5(
        translation_text,
        narrator,
        content='english_translations',
        content_rowid='id'
    )
""")

# Load book metadata from main DB
books = {}
for row in main_db.execute("""
    SELECT id, name, english_name, transliteration, author_name, english_author
    FROM books
""").fetchall():
    books[row['id']] = dict(row)

# Load all English translations
print("\nLoading translations from hadith_translations.db...")
start = time.time()

translations = trans_db.execute("""
    SELECT id, hadith_id, book_id, hadith_number, translation_text,
           narrator, translator, edition, source_name, alignment_score,
           verified
    FROM hadith_translations
    WHERE language = 'en'
    ORDER BY book_id, hadith_id
""").fetchall()

print(f"Loaded {len(translations)} English translation records in {time.time()-start:.2f}s")

# Insert into output DB
print("Inserting into FTS-indexed database...")
start = time.time()
inserted = 0
skipped = 0

for t in translations:
    book_info = books.get(t['book_id'], {})
    
    # Skip empty translations
    text = (t['translation_text'] or '').strip()
    if not text:
        skipped += 1
        continue
    
    out_db.execute("""
        INSERT INTO english_translations
        (id, hadith_id, book_id, hadith_number, translation_text,
         narrator, translator, edition, source_name, alignment_score,
         verified, book_name, book_english_name, book_transliteration,
         author_name, english_author)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        t['id'],
        t['hadith_id'],
        t['book_id'],
        t['hadith_number'],
        text,
        t['narrator'],
        t['translator'],
        t['edition'],
        t['source_name'],
        t['alignment_score'],
        t['verified'],
        book_info.get('name'),
        book_info.get('english_name'),
        book_info.get('transliteration'),
        book_info.get('author_name'),
        book_info.get('english_author'),
    ))
    inserted += 1

print(f"Inserted {inserted} records, skipped {skipped} empty records")
print(f"Insert took {time.time()-start:.2f}s")

# Populate FTS index
print("\nPopulating FTS5 index...")
start = time.time()
out_db.execute("""
    INSERT INTO english_fts(english_fts) VALUES('rebuild')
""")
print(f"FTS rebuild took {time.time()-start:.2f}s")

# Create indexes for fast lookup
print("Creating indexes...")
out_db.execute("CREATE INDEX idx_et_hadith_id ON english_translations(hadith_id)")
out_db.execute("CREATE INDEX idx_et_book_id ON english_translations(book_id)")
out_db.execute("CREATE INDEX idx_et_book_hadith ON english_translations(book_id, hadith_number)")

# Create coverage summary table
out_db.execute("""
    CREATE TABLE coverage_summary (
        book_id INTEGER PRIMARY KEY,
        book_name TEXT,
        book_english_name TEXT,
        book_transliteration TEXT,
        total_hadiths_in_book INTEGER,
        translated_count INTEGER,
        translator TEXT,
        edition TEXT,
        source_name TEXT,
        coverage_percent REAL
    )
""")

# Populate coverage summary
for book_id, book_info in sorted(books.items()):
    count = out_db.execute(
        "SELECT COUNT(*) FROM english_translations WHERE book_id=?", (book_id,)
    ).fetchone()[0]
    
    if count == 0:
        continue
    
    total_in_book = main_db.execute(
        "SELECT hadith_qty FROM books WHERE id=?", (book_id,)
    ).fetchone()
    total = total_in_book[0] if total_in_book else 0
    
    meta = out_db.execute("""
        SELECT translator, edition, source_name
        FROM english_translations
        WHERE book_id = ?
        LIMIT 1
    """, (book_id,)).fetchone()
    
    coverage = (count / total * 100) if total > 0 else 0
    
    out_db.execute("""
        INSERT INTO coverage_summary
        (book_id, book_name, book_english_name, book_transliteration,
         total_hadiths_in_book, translated_count, translator, edition,
         source_name, coverage_percent)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        book_id,
        book_info.get('name'),
        book_info.get('english_name'),
        book_info.get('transliteration'),
        total,
        count,
        meta[0] if meta else None,
        meta[1] if meta else None,
        meta[2] if meta else None,
        round(coverage, 2),
    ))

out_db.commit()

# Verify
print("\n" + "=" * 70)
print("VERIFICATION")
print("=" * 70)

total = out_db.execute("SELECT COUNT(*) FROM english_translations").fetchone()[0]
print(f"Total indexed translations: {total}")

fts_count = out_db.execute("SELECT COUNT(*) FROM english_fts").fetchone()[0]
print(f"FTS index entries: {fts_count}")

coverage = out_db.execute("SELECT * FROM coverage_summary ORDER BY book_id").fetchall()
print(f"\nCoverage across {len(coverage)} collections:")
for c in coverage:
    print(f"  Book {c[0]}: {c[2]} - {c[5]}/{c[4]} ({c[9]:.1f}%) - {c[6]}")

# Test searches
print("\n--- Search Test: 'intentions' ---")
results = out_db.execute("""
    SELECT et.hadith_id, et.book_id, et.hadith_number, et.book_english_name,
           et.translator, rank,
           SUBSTR(et.translation_text, 1, 120) as snippet
    FROM english_fts fts
    JOIN english_translations et ON et.id = fts.rowid
    WHERE english_fts MATCH 'intentions'
    ORDER BY rank
    LIMIT 5
""").fetchall()
for r in results:
    print(f"  hadith_id={r[0]}, book={r[3]}, #{r[2]}, rank={r[5]:.4f}")
    print(f"    {r[6]}...")

print("\n--- Search Test: 'mercy knowledge' ---")
results = out_db.execute("""
    SELECT et.hadith_id, et.book_id, et.hadith_number, et.book_english_name,
           rank, SUBSTR(et.translation_text, 1, 120) as snippet
    FROM english_fts fts
    JOIN english_translations et ON et.id = fts.rowid
    WHERE english_fts MATCH 'mercy knowledge'
    ORDER BY rank
    LIMIT 5
""").fetchall()
for r in results:
    print(f"  hadith_id={r[0]}, book={r[3]}, #{r[2]}, rank={r[4]:.4f}")
    print(f"    {r[5]}...")

# File size
out_db.close()
size_mb = os.path.getsize(OUTPUT_DB_PATH) / (1024 * 1024)
print(f"\nOutput file: {OUTPUT_DB_PATH}")
print(f"File size: {size_mb:.1f} MB")
print("\nDONE — English Translation FTS5 index built successfully!")

trans_db.close()
main_db.close()
