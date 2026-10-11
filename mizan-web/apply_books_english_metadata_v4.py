#!/usr/bin/env python3
import csv, os, sqlite3, sys
from datetime import datetime, timezone
EXPECTED=set(range(1,426))
if len(sys.argv)!=3: raise SystemExit('Usage: python apply_books_english_metadata_v3.py DB_PATH CSV_PATH')
db_path,csv_path=sys.argv[1:]
if not os.path.isfile(db_path): raise SystemExit(f'ERROR: DB not found: {db_path}')
if not os.path.isfile(csv_path): raise SystemExit(f'ERROR: CSV not found: {csv_path}')
rows=[]
with open(csv_path,encoding='utf-8-sig',newline='') as f:
 r=csv.DictReader(f)
 if set(r.fieldnames or []) != {'id','english_name','english_author'}: raise SystemExit('ERROR: CSV columns must be id,english_name,english_author')
 for x in r:
  i=int(x['id']); n=x['english_name'].strip(); a=x['english_author'].strip()
  if i not in EXPECTED or not n or not a: raise SystemExit(f'ERROR: invalid row {x}')
  rows.append((i,n,a))
if len(rows)!=425 or {x[0] for x in rows}!=EXPECTED: raise SystemExit('ERROR: CSV must contain exactly IDs 1..425')
db=sqlite3.connect(db_path)
try:
 if db.execute('SELECT COUNT(*) FROM books').fetchone()[0]!=425: raise SystemExit('ERROR: DB books count is not 425')
 cols={r[1] for r in db.execute('PRAGMA table_info(books)')}
 for c in ('english_name','english_author'):
  if c not in cols: db.execute(f'ALTER TABLE books ADD COLUMN {c} TEXT')
 stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
 backup=f'{db_path}.before_english_metadata_v3_{stamp}.sqlite'
 db.execute('VACUUM INTO ?', (backup,)); print('Backup:',backup)
 db.execute('BEGIN')
 db.executemany('UPDATE books SET english_name=?, english_author=? WHERE id=?',[(n,a,i) for i,n,a in rows])
 db.commit()
 bad=db.execute("SELECT COUNT(*) FROM books WHERE english_name IS NULL OR TRIM(english_name)='' OR english_author IS NULL OR TRIM(english_author)=''").fetchone()[0]
 if bad: raise SystemExit(f'ERROR: verification failed: {bad} empty rows')
 print('Verified:',db.execute("SELECT COUNT(*) FROM books WHERE english_name IS NOT NULL AND TRIM(english_name)<>'' AND english_author IS NOT NULL AND TRIM(english_author)<>''").fetchone()[0],'/425')
 print('Arabic fields untouched. Migration complete.')
finally: db.close()
