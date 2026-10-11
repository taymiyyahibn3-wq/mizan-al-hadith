#!/usr/bin/env python3
"""
Mizan al-Hadith — safely add English book/author metadata.

Usage inside the backend/container environment:
    python apply_books_english_metadata.py /data/hadith-kg.db books_425_english_metadata.csv

This script:
- refuses to continue unless the CSV contains exactly 425 unique IDs (1..425)
- creates a SQLite backup with VACUUM INTO before changing the live DB
- adds english_name and english_author columns if missing
- updates by book ID only
- verifies all 425 rows after the update
- never changes the existing Arabic fields
"""

from __future__ import annotations
import csv
import os
import sqlite3
import sys
from datetime import datetime, timezone

EXPECTED_IDS = set(range(1, 426))

def die(msg: str) -> None:
    raise SystemExit(f"ERROR: {msg}")

if len(sys.argv) != 3:
    die("Usage: python apply_books_english_metadata.py DB_PATH CSV_PATH")

db_path, csv_path = sys.argv[1], sys.argv[2]

if not os.path.isfile(db_path):
    die(f"Database not found: {db_path}")
if not os.path.isfile(csv_path):
    die(f"CSV not found: {csv_path}")

rows = []
with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    required = {"id", "english_name", "english_author"}
    missing = required - set(reader.fieldnames or [])
    if missing:
        die(f"CSV missing columns: {sorted(missing)}")
    for row in reader:
        try:
            row_id = int(row["id"])
        except Exception:
            die(f"Invalid book id: {row['id']!r}")
        name = (row["english_name"] or "").strip()
        author = (row["english_author"] or "").strip()
        if not name or not author:
            die(f"Empty English metadata for book {row_id}")
        rows.append((row_id, name, author))

ids = {r[0] for r in rows}
if len(rows) != 425 or ids != EXPECTED_IDS:
    die(f"CSV must contain exactly IDs 1..425; got {len(rows)} rows")

db = sqlite3.connect(db_path)
db.row_factory = sqlite3.Row

try:
    # Basic source validation.
    count = db.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    if count != 425:
        die(f"Expected 425 books in DB, found {count}")

    cols = {r["name"] for r in db.execute("PRAGMA table_info(books)").fetchall()}
    for col in ("english_name", "english_author"):
        if col not in cols:
            db.execute(f"ALTER TABLE books ADD COLUMN {col} TEXT")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = f"{db_path}.before_english_metadata_{stamp}.sqlite"
    db.execute("VACUUM INTO ?", (backup,))
    print(f"Backup: {backup}")

    db.execute("BEGIN")
    db.executemany(
        "UPDATE books SET english_name=?, english_author=? WHERE id=?",
        [(name, author, row_id) for row_id, name, author in rows],
    )
    db.commit()

    # Verify every ID and ensure no empty values.
    bad = db.execute("""
        SELECT id, english_name, english_author
        FROM books
        WHERE english_name IS NULL OR TRIM(english_name) = ''
           OR english_author IS NULL OR TRIM(english_author) = ''
        ORDER BY id
    """).fetchall()
    if bad:
        die(f"Verification failed; empty English metadata remains for {len(bad)} rows")

    verified = db.execute("""
        SELECT COUNT(*) FROM books
        WHERE english_name IS NOT NULL AND TRIM(english_name) <> ''
          AND english_author IS NOT NULL AND TRIM(english_author) <> ''
    """).fetchone()[0]

    print(f"Verified English metadata rows: {verified}/425")
    print("Migration complete. Arabic name/author fields were not modified.")

finally:
    db.close()
