import os
import glob
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
pre_path = os.path.join(repo_root, "validation", "research_workspace_pre_hashes.json")

if not os.path.exists(pre_path):
    print("ERROR: validation/research_workspace_pre_hashes.json not found!")
    sys.exit(1)

with open(pre_path, "r", encoding="utf-8") as f:
    pre_hashes = json.load(f)

mismatches = []
matches = []

for rel_path, meta in sorted(pre_hashes.items()):
    full_path = os.path.join(repo_root, rel_path)
    expected_sha = meta["sha256"]
    if os.path.isfile(full_path):
        h = hashlib.sha256()
        with open(full_path, "rb") as f:
            while chunk := f.read(4 * 1024 * 1024):
                h.update(chunk)
        post_sha = h.hexdigest()
        if expected_sha != post_sha:
            print(f"MUTATED FILE: {rel_path}! Pre: {expected_sha} Post: {post_sha}")
            mismatches.append((rel_path, expected_sha, post_sha))
        else:
            matches.append(rel_path)
            print(f"CANONICAL DB MATCH: {rel_path} ({post_sha[:16]}...)")
    else:
        print(f"MISSING FILE: {rel_path}")
        mismatches.append((rel_path, expected_sha, "MISSING"))

print(f"\nAudit complete: {len(matches)} matches, {len(mismatches)} mismatches.")
if mismatches:
    print(f"FAILED: {len(mismatches)} database mutations detected!")
    sys.exit(1)
else:
    print(f"SUCCESS: ZERO MUTATIONS across all {len(matches)} canonical and reference databases (PRE_HASH == POST_HASH)!")
