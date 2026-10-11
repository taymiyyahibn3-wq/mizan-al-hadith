import re
import json

with open("presentation_02.html", "r", encoding="utf-8") as f:
    html = f.read()

print("File size:", len(html), "bytes")

# Check slide count
slides = re.findall(r'<section class="slide[^"]*" id="slide-(\d+)"', html)
print(f"Total slides found: {len(slides)} (IDs: {slides[0]} to {slides[-1]})")
assert len(slides) == 22, f"Expected 22 slides, found {len(slides)}"

# Check critical content tokens
critical_tokens = [
    "<!DOCTYPE html>",
    "MĪZĀN AL-ḤADĪTH",
    "₹165,000",
    "₹130,000",
    "₹18,518",
    "43,493",
    "49,844",
    "4,414,211",
    "65,420",
    "1,202",
    "1,203",
    "Numbering Schemes",
    "Phase 18",
    "AWS Lightsail",
    "Hetzner",
    "Gemini 1.5 Flash",
    "Cloudflare R2",
    "Tesseract",
    "sources-drawer",
    "bgCanvas",
    "progress-fill",
    "current-slide-num"
]

for token in critical_tokens:
    assert token in html, f"Missing token: {token}"

print("All 22 critical tokens verified successfully!")

# Validate validation json
with open("validation/presentation_02_validation.json", "r", encoding="utf-8") as f:
    val = json.load(f)

print("Validation JSON final_status:", val.get("final_status"))
assert val.get("final_status") == "READY_FOR_MEETING"
assert val.get("financial_total_18mo_inr") == 165000.0
assert val.get("financial_total_12mo_inr") == 130000.0
assert val.get("slide_count") == 22

print("ALL QUALITY, FINANCIAL & STRUCTURAL AUDITS PASSED CLEANLY!")
