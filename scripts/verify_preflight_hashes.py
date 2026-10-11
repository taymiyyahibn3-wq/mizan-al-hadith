import hashlib
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

files = {
    "data/hadith-kg.db": "08c3a43d78f510828ab870a23203ef67d8ded7be81f74fdb1b9378996c65dfdd",
    "data/derived_semantic_index.db": "0867383f9b29bd9c31fcd197aa1ac4fa923f1114df5e20ca7c4feca1185be875",
    "data/meaning_groups_export.jsonl": "bc15a337b6eb0dddfb294fe6ce7ada063b5a4879ad7eec80f98ddbb17d6a9cbf",
}

print("=== VERIFYING PREFLIGHT HASHES ===")
all_match = True
for f_path, expected_sha in files.items():
    if not os.path.exists(f_path):
        print(f"[ERROR] Missing file: {f_path}")
        all_match = False
        continue
    h = hashlib.sha256()
    with open(f_path, "rb") as f:
        while chunk := f.read(1024 * 1024 * 8):
            h.update(chunk)
    actual_sha = h.hexdigest()
    match = (actual_sha == expected_sha)
    print(f"{f_path}:")
    print(f"  Expected: {expected_sha}")
    print(f"  Actual:   {actual_sha}")
    print(f"  Match:    {match}")
    if not match:
        all_match = False

print(f"\nAll hashes match: {all_match}")

# Check Gemini API Key
api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or ""
print(f"GEMINI_API_KEY present in os.environ: {bool(api_key.strip())}")

# Also check .env file if present
env_file = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(env_file):
    print(".env file exists.")
    for line in open(env_file, "r", encoding="utf-8"):
        if "GEMINI_API_KEY" in line or "GOOGLE_API_KEY" in line:
            parts = line.strip().split("=", 1)
            if len(parts) == 2 and parts[1].strip():
                print(f"Found {parts[0].strip()} in .env: True (length {len(parts[1].strip())})")
else:
    print(".env file does not exist.")

# Check mizan-web backend .env
backend_env = os.path.join(os.path.dirname(__file__), "..", "mizan-web", "backend", ".env")
if os.path.exists(backend_env):
    print("mizan-web/backend/.env file exists.")
    for line in open(backend_env, "r", encoding="utf-8"):
        if "GEMINI_API_KEY" in line or "GOOGLE_API_KEY" in line:
            parts = line.strip().split("=", 1)
            if len(parts) == 2 and parts[1].strip():
                print(f"Found {parts[0].strip()} in backend .env: True (length {len(parts[1].strip())})")
