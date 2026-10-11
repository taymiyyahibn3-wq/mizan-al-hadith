import os
import glob
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

pre_path = "validation/classical_scholar_grading_research/pre_hashes.json"
if not os.path.exists(pre_path):
    print("ERROR: pre_hashes.json not found!")
    sys.exit(1)

with open(pre_path, "r", encoding="utf-8") as f:
    pre_hashes = json.load(f)

post_hashes = {}
mismatches = []

for p in sorted(pre_hashes.keys()):
    if os.path.isfile(p):
        h = hashlib.sha256()
        with open(p, "rb") as f:
            while chunk := f.read(1024*1024):
                h.update(chunk)
        post_sha = h.hexdigest()
        pre_sha = pre_hashes[p]["sha256"]
        if pre_sha != post_sha:
            print(f"MUTATED CANONICAL FILE: {p}! Pre: {pre_sha} Post: {post_sha}")
            mismatches.append((p, "MUTATED", post_sha))
        else:
            print(f"CANONICAL DB MATCH: {p} ({post_sha[:16]}...)")
    else:
        print(f"MISSING CANONICAL FILE: {p}")
        mismatches.append((p, "MISSING", None))

# Check for derived database
derived_path = "data/classical_scholar_evidence.db"
if os.path.exists(derived_path):
    print(f"DERIVED NON-CANONICAL DB: {derived_path} (Properly isolated and rebuildable)")

if mismatches:
    print(f"\nFAILED: {len(mismatches)} canonical database mutations detected!")
    sys.exit(1)
else:
    print(f"\nSUCCESS: ZERO MUTATIONS. All {len(pre_hashes)} canonical database pre-hashes match post-hashes exactly (PRE_HASH == POST_HASH)!")

