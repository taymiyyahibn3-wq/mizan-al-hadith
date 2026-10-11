import os
import shutil
import hashlib
import json
import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DERIVED_DB_PATH = os.path.join(REPO_ROOT, "data", "classical_scholar_evidence.db")
BACKUP_DERIVED_PATH = os.path.join(REPO_ROOT, "data", "classical_scholar_evidence.backup_before_phase3.db")

# 1. Backup derived DB
shutil.copy2(DERIVED_DB_PATH, BACKUP_DERIVED_PATH)
print(f"Backed up {DERIVED_DB_PATH} to {BACKUP_DERIVED_PATH}")

# 2. Hash pre-state of derived DB
h = hashlib.sha256()
with open(DERIVED_DB_PATH, "rb") as f:
    while chunk := f.read(1024*1024):
        h.update(chunk)
derived_pre_sha = h.hexdigest()
print(f"Derived DB pre-hash: {derived_pre_sha}")

# 3. Check existing rows in derived DB
conn = sqlite3.connect(DERIVED_DB_PATH)
c = conn.cursor()
tirmidhi_grades = c.execute("SELECT count(*) FROM classical_hadith_evaluations WHERE scholar_id='al_tirmidhi' AND evidence_type='explicit_hadith_grade'").fetchone()[0]
tirmidhi_crit = c.execute("SELECT count(*) FROM classical_hadith_evaluations WHERE scholar_id='al_tirmidhi' AND evidence_type='hadith_criticism'").fetchone()[0]
total_tirmidhi = c.execute("SELECT count(*) FROM classical_hadith_evaluations WHERE scholar_id='al_tirmidhi'").fetchone()[0]
conn.close()

print(f"Tirmidhi Explicit Grades: {tirmidhi_grades}")
print(f"Tirmidhi Criticism: {tirmidhi_crit}")
print(f"Total Tirmidhi: {total_tirmidhi}")

if total_tirmidhi != 2726 or tirmidhi_grades != 1918 or tirmidhi_crit != 808:
    print("FATAL: Tirmidhi baseline verification failed!")
    sys.exit(1)
else:
    print("SUCCESS: Tirmidhi baseline verified (2,726 records).")
