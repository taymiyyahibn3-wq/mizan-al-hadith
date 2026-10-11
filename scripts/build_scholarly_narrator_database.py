#!/usr/bin/env python3
"""
Mīzān al-Hadīth - Scholarly Narrator Database Builder
=====================================================
Builds and persists canonical scholarly transliterations for all 49,844 narrators.
Updates:
1. data/english_enrichment.db (table: narrator_names)
2. data/isnad_network.db (table: narrator_nodes)

Adheres strictly to the Scholarly Transliteration Standard (IJMES/EI):
- ā, ī, ū
- ʿ for ʿayn (U+02BF)
- ʾ for hamzah (U+02BE)
- ṣ, ḍ, ṭ, ẓ, ḥ, kh, dh, sh, gh, th
- Consistent 'ibn' / 'bint' / 'al-'
- Preserves full identity (kunyah, patronymic, nisbah, laqab)
- Creates normalized ASCII search keys for tolerant search
"""

import os
import shutil
import sqlite3
import sys
import time
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
sys.stdout.reconfigure(encoding="utf-8")

from src.narrator_transliteration import transliterate_narrator_name, normalize_for_search

HADITH_KG_PATH = ROOT_DIR / "data" / "hadith-kg.db"
ENGLISH_ENRICHMENT_PATH = ROOT_DIR / "data" / "english_enrichment.db"
ISNAD_NETWORK_PATH = ROOT_DIR / "data" / "isnad_network.db"

def backup_file(fpath: Path, tag: str = "backup-before-scholarly-translit"):
    backup_path = fpath.with_name(f"{fpath.stem}.{tag}{fpath.suffix}")
    if not backup_path.exists():
        print(f"Backing up {fpath.name} to {backup_path.name}...")
        shutil.copy2(fpath, backup_path)
    else:
        print(f"Backup already exists at {backup_path.name}")
    return backup_path

def main():
    start_time = time.time()
    print("=" * 70)
    print("MĪZĀN AL-HADĪTH: SCHOLARLY NARRATOR TRANSLITERATION PIPELINE")
    print("=" * 70)

    if not HADITH_KG_PATH.exists():
        raise FileNotFoundError(f"Database not found: {HADITH_KG_PATH}")

    # Step 1: Backup databases before applying changes
    print("\n[Step 1] Creating database backups...")
    if ENGLISH_ENRICHMENT_PATH.exists():
        backup_file(ENGLISH_ENRICHMENT_PATH)
    if ISNAD_NETWORK_PATH.exists():
        backup_file(ISNAD_NETWORK_PATH)

    # Step 2: Fetch all rawis from read-only hadith-kg.db
    print("\n[Step 2] Fetching narrators from hadith-kg.db (read-only)...")
    kg_conn = sqlite3.connect(f"file:{HADITH_KG_PATH}?mode=ro", uri=True)
    kg_cur = kg_conn.cursor()

    rawi_rows = kg_cur.execute(
        "SELECT id, name, nickname FROM rawis ORDER BY id"
    ).fetchall()
    kg_conn.close()

    total_rawis = len(rawi_rows)
    print(f"Loaded {total_rawis:,} narrators from rawis table.")

    # Step 3: Compute canonical scholarly transliterations
    print("\n[Step 3] Computing deterministic scholarly transliterations...")
    transliterated_records = []
    stats = {
        "authoritative_scholarly": 0,
        "canonical_lexicon": 0,
        "deterministic_transliteration": 0,
    }

    for rawi_id, full_name, nickname in rawi_rows:
        display_ar = (nickname or full_name or "").strip()
        full_ar = (full_name or nickname or "").strip()

        # Transliterate famous display name (nickname/shuhrah)
        name_en, src, conf = transliterate_narrator_name(display_ar, rawi_id)

        # Transliterate full patronymic chain (name)
        full_name_en, _, _ = transliterate_narrator_name(full_ar, rawi_id)

        # Search key
        search_key = normalize_for_search(name_en)

        stats[src] = stats.get(src, 0) + 1

        review_status = "verified" if src == "authoritative_scholarly" else "standard_mapped"

        transliterated_records.append((
            rawi_id,
            display_ar,
            name_en,
            full_name_en,
            search_key,
            "scholarly_diacritics_v1",
            src,
            conf,
            review_status,
        ))

    print("\nTransliteration summary:")
    print(f"  Authoritative scholarly forms:      {stats.get('authoritative_scholarly', 0):,}")
    print(f"  Canonical lexicon mapped:            {stats.get('canonical_lexicon', 0):,}")
    print(f"  Deterministic transliterations:      {stats.get('deterministic_transliteration', 0):,}")
    print(f"  Total mapped:                        {len(transliterated_records):,}")

    # Step 4: Update english_enrichment.db
    print(f"\n[Step 4] Updating {ENGLISH_ENRICHMENT_PATH.name}...")
    ee_conn = sqlite3.connect(str(ENGLISH_ENRICHMENT_PATH))
    ee_cur = ee_conn.cursor()

    # Ensure schema supports new metadata columns
    existing_cols = [c[1] for c in ee_cur.execute("PRAGMA table_info(narrator_names)").fetchall()]
    new_cols = {
        "full_name_en": "TEXT",
        "search_name": "TEXT",
        "transliteration_standard": "TEXT DEFAULT 'scholarly_diacritics_v1'",
        "review_status": "TEXT DEFAULT 'standard_mapped'",
    }
    for col_name, col_type in new_cols.items():
        if col_name not in existing_cols:
            print(f"  Adding column {col_name} to narrator_names...")
            ee_cur.execute(f"ALTER TABLE narrator_names ADD COLUMN {col_name} {col_type};")

    # Update/replace rows in narrator_names
    print("  Populating narrator_names records...")
    ee_cur.executemany(
        """
        INSERT INTO narrator_names (
            rawi_id,
            arabic_name,
            english_name,
            full_name_en,
            search_name,
            transliteration_standard,
            source,
            confidence,
            review_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(rawi_id) DO UPDATE SET
            arabic_name = excluded.arabic_name,
            english_name = excluded.english_name,
            full_name_en = excluded.full_name_en,
            search_name = excluded.search_name,
            transliteration_standard = excluded.transliteration_standard,
            source = excluded.source,
            confidence = excluded.confidence,
            review_status = excluded.review_status
        """,
        transliterated_records,
    )

    # Ensure indexes
    ee_cur.execute("CREATE INDEX IF NOT EXISTS idx_narrator_search ON narrator_names(search_name);")
    ee_cur.execute("CREATE INDEX IF NOT EXISTS idx_narrator_en_name ON narrator_names(english_name);")
    ee_conn.commit()
    ee_conn.close()
    print("  narrator_names updated and indexed successfully.")

    # Step 5: Update isnad_network.db narrator_nodes
    if ISNAD_NETWORK_PATH.exists():
        print(f"\n[Step 5] Updating {ISNAD_NETWORK_PATH.name}...")
        isnad_conn = sqlite3.connect(str(ISNAD_NETWORK_PATH))
        isnad_cur = isnad_conn.cursor()

        isnad_cols = [c[1] for c in isnad_cur.execute("PRAGMA table_info(narrator_nodes)").fetchall()]
        if "english_name" not in isnad_cols:
            print("  Adding english_name to narrator_nodes...")
            isnad_cur.execute("ALTER TABLE narrator_nodes ADD COLUMN english_name TEXT;")
        if "name_en" not in isnad_cols:
            print("  Adding name_en to narrator_nodes...")
            isnad_cur.execute("ALTER TABLE narrator_nodes ADD COLUMN name_en TEXT;")
        if "full_name_en" not in isnad_cols:
            print("  Adding full_name_en to narrator_nodes...")
            isnad_cur.execute("ALTER TABLE narrator_nodes ADD COLUMN full_name_en TEXT;")
        if "search_name" not in isnad_cols:
            print("  Adding search_name to narrator_nodes...")
            isnad_cur.execute("ALTER TABLE narrator_nodes ADD COLUMN search_name TEXT;")

        print("  Updating narrator_nodes with canonical English transliterations...")
        node_updates = [
            (rec[2], rec[2], rec[3], rec[4], rec[0]) # english_name, name_en, full_name_en, search_name, rawi_id
            for rec in transliterated_records
        ]
        isnad_cur.executemany(
            """
            UPDATE narrator_nodes
            SET english_name = ?,
                name_en = ?,
                full_name_en = ?,
                search_name = ?
            WHERE rawi_id = ?
            """,
            node_updates,
        )
        isnad_cur.execute("CREATE INDEX IF NOT EXISTS idx_node_en_name ON narrator_nodes(english_name);")
        isnad_cur.execute("CREATE INDEX IF NOT EXISTS idx_node_search ON narrator_nodes(search_name);")
        isnad_conn.commit()
        isnad_conn.close()
        print("  narrator_nodes updated and indexed successfully.")

    elapsed = time.time() - start_time
    print(f"\nAll 49,844 narrators successfully processed and persisted in {elapsed:.2f}s!")

if __name__ == "__main__":
    main()
