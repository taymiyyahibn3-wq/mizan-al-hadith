"""
MĪZĀN AL-ḤADĪTH — Derived Vector Store Builder & Ingestion Engine (Phase 1)
Creates and manages the experimental derived database:
  data/derived_embeddinggemma2_768d.db

Features:
  - Strict schema definition for metadata and 768-D Float32 group embeddings.
  - Zero mutation of canonical hadith-kg.db or baseline derived_semantic_index.db.
  - Resumable ingestion with dynamic exclusion of already-committed group IDs.
  - Transactional chunking (every 500 records) ensuring atomic durability.
  - Local execution mode (via sentence-transformers if available, or ingestion from Colab artifacts).
  - Validation of vector dimensions (768), byte size (3072), and L2 normalization.
"""

from __future__ import annotations
import argparse
import hashlib
import json
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = REPO_ROOT / "data" / "derived_embeddinggemma2_768d.db"
DEFAULT_CORPUS_PATH = REPO_ROOT / "data" / "meaning_groups_export.jsonl"
CANONICAL_KG_PATH = REPO_ROOT / "data" / "hadith-kg.db"
BASELINE_SEMANTIC_PATH = REPO_ROOT / "data" / "derived_semantic_index.db"

MODEL_IDENTIFIER = "google/embeddinggemma-2"
MODEL_VARIANT = "text-only-270m"
DIMENSIONS = 768
EXPECTED_BLOB_SIZE = 768 * 4  # 3072 bytes (float32 little-endian)


def compute_file_sha256(path: Path) -> str:
    """Computes SHA-256 checksum of a file in 8MB chunks."""
    if not path.exists():
        return ""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024 * 8):
            h.update(chunk)
    return h.hexdigest()


def init_derived_database(db_path: Path, manifest_info: Optional[Dict[str, Any]] = None) -> None:
    """Initializes the isolated derived SQLite database schema."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    try:
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS group_embedding (
                group_id INTEGER PRIMARY KEY,
                model TEXT NOT NULL,
                dimensions INTEGER NOT NULL,
                vector BLOB NOT NULL,
                norm_l2 REAL NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_group_embedding_lookup 
            ON group_embedding(model, dimensions);
            """
        )

        # Record standard metadata manifest
        source_sha = compute_file_sha256(CANONICAL_KG_PATH)
        baseline_sha = compute_file_sha256(BASELINE_SEMANTIC_PATH)
        corpus_sha = compute_file_sha256(DEFAULT_CORPUS_PATH)

        default_metadata = {
            "model": MODEL_IDENTIFIER,
            "model_variant": MODEL_VARIANT,
            "dimensions": str(DIMENSIONS),
            "dtype": "float32_little_endian",
            "blob_bytes_per_vector": str(EXPECTED_BLOB_SIZE),
            "normalization": "L2 unit sphere",
            "corpus_type": "canonical_meaning_groups",
            "target_count": "20744",
            "source_database": "data/hadith-kg.db",
            "source_database_sha256": source_sha,
            "baseline_database": "data/derived_semantic_index.db",
            "baseline_database_sha256": baseline_sha,
            "corpus_sha256": corpus_sha,
            "embedding_provider": "embeddinggemma2",
            "baseline_provider": "gemini",
            "task_prompt_document": "Document",
            "task_prompt_query": "SearchQuery",
            "schema_version": "1.0.0",
            "initialized_at": datetime.now(timezone.utc).isoformat(),
        }

        if manifest_info:
            default_metadata.update(manifest_info)

        for k, v in default_metadata.items():
            conn.execute(
                "INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?);",
                (k, str(v)),
            )
        conn.commit()
    finally:
        conn.close()


def get_completed_group_ids(db_path: Path) -> Set[int]:
    """Returns the set of group_ids already present in the database."""
    if not db_path.exists():
        return set()
    conn = sqlite3.connect(f"file:{db_path.resolve()}?mode=ro", uri=True)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT group_id FROM group_embedding;")
        return {int(r[0]) for r in cursor.fetchall()}
    except sqlite3.OperationalError:
        return set()
    finally:
        conn.close()


def insert_embedding_chunk(
    db_path: Path,
    records: List[Tuple[int, str, int, bytes, float, str]],
) -> None:
    """Inserts a batch of embedding records in a single atomic transaction."""
    if not records:
        return
    conn = sqlite3.connect(str(db_path), timeout=60.0)
    try:
        conn.execute("BEGIN TRANSACTION;")
        conn.executemany(
            """
            INSERT OR REPLACE INTO group_embedding 
            (group_id, model, dimensions, vector, norm_l2, created_at)
            VALUES (?, ?, ?, ?, ?, ?);
            """,
            records,
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def validate_vector_array(arr: np.ndarray) -> Tuple[bool, str, float]:
    """Validates vector dimensions, finite numbers, and computes L2 norm."""
    if arr.ndim != 1 or arr.shape[0] != DIMENSIONS:
        return False, f"Expected shape ({DIMENSIONS},), got {arr.shape}", 0.0
    if not np.all(np.isfinite(arr)):
        return False, "Vector contains NaN or Inf values", 0.0
    norm = float(np.linalg.norm(arr))
    if norm < 1e-6:
        return False, "Vector norm is near zero", norm
    return True, "", norm


def build_from_checkpoint_archive(
    checkpoint_jsonl_path: Path,
    output_db_path: Path = DEFAULT_DB_PATH,
    chunk_size: int = 500,
) -> int:
    """Imports precomputed vectors from a JSONL checkpoint archive into the derived SQLite database."""
    init_derived_database(output_db_path)
    completed_ids = get_completed_group_ids(output_db_path)
    print(f"[INFO] Existing records in {output_db_path.name}: {len(completed_ids)}")

    if not checkpoint_jsonl_path.exists():
        raise FileNotFoundError(f"Checkpoint archive not found: {checkpoint_jsonl_path}")

    now_iso = datetime.now(timezone.utc).isoformat()
    buffer: List[Tuple[int, str, int, bytes, float, str]] = []
    total_inserted = 0

    with open(checkpoint_jsonl_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue
            data = json.loads(line)
            gid = int(data["group_id"])
            if gid in completed_ids:
                continue

            # Supports either base64/hex bytes or float list
            if "vector" in data and isinstance(data["vector"], list):
                arr = np.array(data["vector"], dtype=np.float32)
            elif "vector_b64" in data:
                import base64
                raw_bytes = base64.b64decode(data["vector_b64"])
                arr = np.frombuffer(raw_bytes, dtype=np.float32)
            else:
                raise ValueError(f"Line {line_num}: Unrecognized vector format")

            valid, err, norm = validate_vector_array(arr)
            if not valid:
                print(f"[ERROR] Group {gid} validation failed: {err}")
                continue

            # Unit normalize
            norm_arr = (arr / norm).astype(np.float32)
            blob = norm_arr.tobytes()
            buffer.append((gid, MODEL_IDENTIFIER, DIMENSIONS, blob, norm, now_iso))
            completed_ids.add(gid)

            if len(buffer) >= chunk_size:
                insert_embedding_chunk(output_db_path, buffer)
                total_inserted += len(buffer)
                print(f"[PROGRESS] Inserted {total_inserted} records (total {len(completed_ids)})...")
                buffer.clear()

    if buffer:
        insert_embedding_chunk(output_db_path, buffer)
        total_inserted += len(buffer)
        buffer.clear()

    print(f"[DONE] Ingestion complete. Total records in DB: {len(completed_ids)}")
    return total_inserted


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mīzān EmbeddingGemma 2 Derived DB Manager")
    parser.add_argument("--init", action="store_true", help="Initialize schema and metadata")
    parser.add_argument("--db", type=str, default=str(DEFAULT_DB_PATH), help="Target SQLite DB path")
    parser.add_argument("--import-jsonl", type=str, help="Import precomputed vectors from JSONL archive")
    args = parser.parse_args()

    db_p = Path(args.db)
    if args.init:
        init_derived_database(db_p)
        print(f"[SUCCESS] Initialized derived database schema at {db_p}")
    elif args.import_jsonl:
        build_from_checkpoint_archive(Path(args.import_jsonl), output_db_path=db_p)
    else:
        init_derived_database(db_p)
        print(f"[INFO] Initialized {db_p}. Current count: {len(get_completed_group_ids(db_p))}")
