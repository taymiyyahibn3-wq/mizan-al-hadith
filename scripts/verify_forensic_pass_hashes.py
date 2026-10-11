import os
import glob
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PRE_HASH_PATH = os.path.join(REPO_ROOT, "validation", "classical_external_grading_research", "forensic_pass_pre_hashes.json")

if not os.path.exists(PRE_HASH_PATH):
    print("ERROR: forensic_pass_pre_hashes.json not found!")
    sys.exit(1)

with open(PRE_HASH_PATH, "r", encoding="utf-8") as f:
    pre_hashes = json.load(f)

mismatches = []
matches = []

for rel_path, pre_sha in sorted(pre_hashes.items()):
    full_path = os.path.join(REPO_ROOT, rel_path)
    if os.path.isfile(full_path):
        h = hashlib.sha256()
        with open(full_path, "rb") as f:
            while chunk := f.read(1024*1024):
                h.update(chunk)
        post_sha = h.hexdigest()
        if pre_sha != post_sha:
            print(f"MUTATED CANONICAL FILE: {rel_path}! Pre: {pre_sha} Post: {post_sha}")
            mismatches.append((rel_path, pre_sha, post_sha))
        else:
            matches.append(rel_path)
            print(f"CANONICAL DB MATCH: {rel_path} ({post_sha[:16]}...)")
    else:
        print(f"MISSING CANONICAL FILE: {rel_path}")
        mismatches.append((rel_path, pre_sha, "MISSING"))

print(f"\nAudit complete: {len(matches)} matches, {len(mismatches)} mismatches.")

if mismatches:
    print(f"FAILED: {len(mismatches)} canonical database mutations detected!")
    sys.exit(1)
else:
    print(f"SUCCESS: ZERO MUTATIONS. All {len(matches)} canonical databases verified bit-for-bit identical (PRE_HASH == POST_HASH)!")
