import os
import glob
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
output_path = os.path.join(repo_root, "validation", "research_workspace_pre_hashes.json")

print("Calculating SHA-256 for all databases in data/...")
db_files = sorted(glob.glob(os.path.join(repo_root, "data", "*.db")))
hashes = {}

for db_path in db_files:
    rel_path = os.path.relpath(db_path, repo_root)
    h = hashlib.sha256()
    with open(db_path, "rb") as f:
        while chunk := f.read(4 * 1024 * 1024):
            h.update(chunk)
    file_sha = h.hexdigest()
    file_size = os.path.getsize(db_path)
    hashes[rel_path] = {
        "sha256": file_sha,
        "size": file_size
    }
    print(f"  {rel_path}: {file_sha[:16]}... ({file_size:,} bytes)")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(hashes, f, indent=2)

print(f"\nSuccessfully stored baseline pre-hashes for {len(hashes)} databases to {output_path}")
