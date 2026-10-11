from pathlib import Path

main_path = Path("backend/main.py")
patch_path = Path("backend_hadith_visualizer_patch.py")

main = main_path.read_text(encoding="utf-8")
patch = patch_path.read_text(encoding="utf-8")

marker = '@app.get("/api/hadith/{hadith_id}")'

if "HADITH_PRO_COLLECTION_TO_BOOK_ID" in main:
    print("Hadith Visualizer backend patch already appears to be installed.")
    raise SystemExit(0)

if marker not in main:
    raise SystemExit(
        "ERROR: Could not find the insertion marker: "
        '@app.get("/api/hadith/{hadith_id}")'
    )

# Remove patch-file header comments that say it is not a replacement.
lines = patch.splitlines()

while lines and (
    lines[0].startswith("#")
    or not lines[0].strip()
):
    lines.pop(0)

patch_clean = "\n".join(lines).rstrip() + "\n\n"

new_main = main.replace(
    marker,
    patch_clean + marker,
    1,
)

main_path.write_text(new_main, encoding="utf-8")

print("SUCCESS: Hadith Visualizer backend patch inserted.")
print("main.py size:", main_path.stat().st_size)
