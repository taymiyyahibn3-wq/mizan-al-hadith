"""
MĪZĀN AL-ḤADĪTH — Deterministic Corpus Extraction for EmbeddingGemma 2 (Phase 1)
Extracts exactly 20,744 active meaning groups from canonical hadith-kg.db.
GUARANTEES:
  - Strict read-only SQLite URI (file:...mode=ro) + PRAGMA query_only = ON.
  - Zero modification to canonical data/hadith-kg.db.
  - Excludes placeholder meaning group id=0 ('غير منشور').
  - Deterministic sort order (ORDER BY id ASC).
  - Emits JSONL records and cryptographic SHA-256 verification digest.
"""

from __future__ import annotations
import hashlib
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

# Ensure UTF-8 output across platforms
sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = REPO_ROOT / "data" / "hadith-kg.db"
OUTPUT_CORPUS_PATH = REPO_ROOT / "data" / "meaning_groups_export.jsonl"
OUTPUT_SHA_PATH = REPO_ROOT / "data" / "meaning_groups_export.jsonl.sha256"
OUTPUT_MANIFEST_PATH = REPO_ROOT / "data" / "embedding_manifest.json"
BASELINE_SEMANTIC_PATH = REPO_ROOT / "data" / "derived_semantic_index.db"

EXPECTED_COUNT = 20744


def compute_sha256(path: Path) -> str:
    """Computes SHA-256 digest of a file in 8MB chunks."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024 * 8):
            h.update(chunk)
    return h.hexdigest()


def extract_corpus(
    db_path: Path = DB_PATH,
    output_path: Path = OUTPUT_CORPUS_PATH,
) -> int:
    """Deterministically extracts active meaning groups from canonical hadith-kg.db."""
    if not db_path.exists():
        raise FileNotFoundError(f"Canonical database not found: {db_path}")

    print(f"[INFO] Connecting to canonical database: {db_path}")
    source_sha256 = compute_sha256(db_path)
    print(f"[INFO] Source hadith-kg.db SHA-256: {source_sha256}")

    # Read-only URI with query_only pragma
    uri = f"file:{db_path.resolve()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA query_only = ON;")

    try:
        cursor = conn.cursor()
        # Strictly active meaning groups: exclude group 0 and empty nass
        cursor.execute(
            """
            SELECT id, nass, sahaba_qty, repeat_qty
            FROM meaning_groups
            WHERE id > 0 AND LENGTH(TRIM(nass)) > 0
            ORDER BY id ASC
            """
        )

        rows = cursor.fetchall()
        count = len(rows)
        print(f"[INFO] Active meaning groups retrieved: {count}")

        if count != EXPECTED_COUNT:
            print(f"[WARNING] Extracted count ({count}) differs from expected ({EXPECTED_COUNT})!")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        hasher = hashlib.sha256()

        with open(output_path, "w", encoding="utf-8", newline="\n") as f:
            for row in rows:
                record = {
                    "group_id": int(row["id"]),
                    "text": str(row["nass"]).strip(),
                    "sahaba_qty": int(row["sahaba_qty"]),
                    "repeat_qty": int(row["repeat_qty"]),
                }
                # Deterministic JSON serialization (no whitespace variance, UTF-8 preserved)
                line = json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"
                f.write(line)
                hasher.update(line.encode("utf-8"))

        corpus_sha256 = hasher.hexdigest()
        print(f"[INFO] Corpus written to: {output_path}")
        print(f"[INFO] Corpus SHA-256: {corpus_sha256}")

        # Write .sha256 companion file
        with open(OUTPUT_SHA_PATH, "w", encoding="utf-8") as f:
            f.write(f"{corpus_sha256}  {output_path.name}\n")

        # Verify baseline semantic DB exists and record its SHA-256
        baseline_sha256 = ""
        if BASELINE_SEMANTIC_PATH.exists():
            baseline_sha256 = compute_sha256(BASELINE_SEMANTIC_PATH)
            print(f"[INFO] Baseline derived_semantic_index.db SHA-256: {baseline_sha256}")

        # Write comprehensive audit manifest
        manifest = {
            "schema_version": "1.0.0",
            "generation_timestamp": datetime.now(timezone.utc).isoformat(),
            "generator": "scripts/export_embeddinggemma2_corpus.py",
            "canonical_source": {
                "path": str(db_path.name),
                "sha256": source_sha256,
                "table": "meaning_groups",
                "filter": "id > 0 AND LENGTH(TRIM(nass)) > 0",
                "ordering": "id ASC",
            },
            "baseline_semantic_store": {
                "path": str(BASELINE_SEMANTIC_PATH.name),
                "sha256": baseline_sha256,
                "model": "gemini-embedding-001",
                "dimensions": 768,
            },
            "exported_corpus": {
                "path": str(output_path.name),
                "sha256": corpus_sha256,
                "record_count": count,
                "min_group_id": int(rows[0]["id"]) if rows else None,
                "max_group_id": int(rows[-1]["id"]) if rows else None,
            },
            "target_model": {
                "model_identifier": "google/embeddinggemma-2",
                "model_variant": "text-only-270m",
                "dimensions": 768,
                "dtype": "float32",
                "normalization": "L2 unit sphere",
                "task_prompt_document": "Document",
                "task_prompt_query": "SearchQuery",
            },
        }

        with open(OUTPUT_MANIFEST_PATH, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        print(f"[INFO] Manifest written to: {OUTPUT_MANIFEST_PATH}")

        # Post-check: ensure canonical DB hash has not changed
        post_source_sha256 = compute_sha256(db_path)
        assert post_source_sha256 == source_sha256, "CRITICAL ERROR: canonical hadith-kg.db changed during extraction!"
        print("[SUCCESS] Canonical database integrity verified (unchanged).")

        return count

    finally:
        conn.close()


if __name__ == "__main__":
    count = extract_corpus()
    print(f"[DONE] Successfully extracted {count} records.")
