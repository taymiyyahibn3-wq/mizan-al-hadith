"""
MĪZĀN AL-ḤADĪTH — Phase 6C Unseen Reference Dataset Generator
Generates ~250–300 completely unseen reference/citation queries from canonical hadith-kg.db.
Categories:
  A. English citations (e.g. Bukhari 52, Muslim 45, Tirmidhi 150)
  B. Arabic citations (e.g. البخاري 52, مسلم 45)
  C. Alternate citation forms (e.g. Sahih Bukhari #52, Bukhari hadith 52, Sunan Abu Dawud 120)
  D. Arabic numeral variants (e.g. البخاري ٥٢, مسلم ٤٥)
  E. Mixed citation + topic queries (e.g. Bukhari 52 about belief, Muslim 45 prayer)
  F. Urdu citation-style queries (e.g. صحیح بخاری 52, صحیح مسلم حدیث 45)
  G. Malformed/ambiguous citations (e.g. Bukhari 999999, Muslim abc, Bukhari alone)

Invariants:
  - Canonical hadiths table is strictly READ-ONLY.
  - Zero overlap with the numbers in the existing 50 benchmark reference queries.
  - Real canonical group_id used as ground truth for valid references; empty [] for malformed.
"""

from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Set

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
KG_DB_PATH = REPO_ROOT / "data" / "hadith-kg.db"
BENCHMARK_PATH = REPO_ROOT / "data" / "benchmarks" / "embeddinggemma2_benchmark_v1.jsonl"
OUTPUT_PATH = REPO_ROOT / "data" / "benchmarks" / "phase6c" / "phase6c_unseen_reference_queries.jsonl"

EASTERN_ARABIC_DIGITS = {"0": "٠", "1": "١", "2": "٢", "3": "٣", "4": "٤", "5": "٥", "6": "٦", "7": "٧", "8": "٨", "9": "٩"}

def to_arabic_numerals(num_str: str) -> str:
    return "".join(EASTERN_ARABIC_DIGITS.get(ch, ch) for ch in num_str)

def main() -> None:
    print("[INFO] Loading existing benchmark references to ensure zero overlap...")
    existing_bench = [json.loads(l) for l in open(BENCHMARK_PATH, encoding="utf-8") if l.strip()]
    existing_nums: Set[int] = set()
    for q in existing_bench:
        if q["category"] in ("reference_lookup", "edge_case"):
            m = re.search(r"\b(\d+)\b", q["query"])
            if m:
                existing_nums.add(int(m.group(1)))

    print(f"[INFO] Found {len(existing_nums)} existing citation numbers to exclude: {sorted(list(existing_nums))[:10]}...")

    conn = sqlite3.connect(f"file:{KG_DB_PATH}?mode=ro", uri=True)
    conn.execute("PRAGMA query_only = ON;")

    # Sample canonical hadiths from major books with group_id > 0
    # Books: 1 (Bukhari), 2 (Muslim), 3 (Tirmidhi), 4 (Abu Dawud), 5 (Nasa'i), 6 (Ibn Majah), 8 (Malik), 9 (Ahmad)
    book_meta = {
        1: {"en_short": "Bukhari", "en_full": "Sahih al-Bukhari", "ar": "البخاري", "ar_full": "صحيح البخاري", "ur": "صحیح بخاری"},
        2: {"en_short": "Muslim", "en_full": "Sahih Muslim", "ar": "مسلم", "ar_full": "صحيح مسلم", "ur": "صحیح مسلم"},
        3: {"en_short": "Tirmidhi", "en_full": "Jami at-Tirmidhi", "ar": "الترمذي", "ar_full": "جامع الترمذي", "ur": "جامع ترمذی"},
        4: {"en_short": "Abu Dawud", "en_full": "Sunan Abi Dawud", "ar": "أبو داود", "ar_full": "سنن أبي داود", "ur": "سنن ابوداؤد"},
        5: {"en_short": "Nasa'i", "en_full": "Sunan an-Nasa'i", "ar": "النسائي", "ar_full": "سنن النسائي", "ur": "سنن نسائی"},
        6: {"en_short": "Ibn Majah", "en_full": "Sunan Ibn Majah", "ar": "ابن ماجه", "ar_full": "سنن ابن ماجه", "ur": "سنن ابن ماجہ"},
        8: {"en_short": "Muwatta", "en_full": "Muwatta Malik", "ar": "موطأ مالك", "ar_full": "موطأ مالك", "ur": "موطا امام مالک"},
        9: {"en_short": "Musnad Ahmad", "en_full": "Musnad Ahmad", "ar": "مسند أحمد", "ar_full": "مسند أحمد", "ur": "مسند احمد"},
    }

    # Query diverse hadiths for each book
    new_queries: List[Dict[str, Any]] = []
    idx = 1

    for book_id, meta in book_meta.items():
        # Fetch rows with numeric no_inbook that are NOT in existing_nums
        rows = conn.execute(
            """
            SELECT id, no_inbook, group_id, taraf_nass, matn
            FROM hadiths
            WHERE book_id = ? AND group_id > 0
            ORDER BY id ASC;
            """,
            (book_id,),
        ).fetchall()

        # Filter valid numeric hadiths
        valid_rows = []
        for r in rows:
            num_str = str(r[1]).strip()
            if num_str.isdigit() and int(num_str) not in existing_nums:
                valid_rows.append((r[0], int(num_str), r[2], r[3], r[4]))

        # Take a balanced slice (e.g. 25-30 per book)
        step = max(1, len(valid_rows) // 30)
        selected_rows = valid_rows[::step][:30]

        for hid, num, gid, taraf, matn in selected_rows:
            num_str = str(num)
            ar_num = to_arabic_numerals(num_str)

            # Category A: English citation
            new_queries.append({
                "query_id": f"UNSEEN_REF_{idx:04d}",
                "query": f"{meta['en_short']} {num_str}",
                "gold_group_ids": [gid],
                "book_id": book_id,
                "hadith_number": num_str,
                "category": "unseen_english_citation",
                "language": "en",
            })
            idx += 1

            # Category B: Arabic citation
            new_queries.append({
                "query_id": f"UNSEEN_REF_{idx:04d}",
                "query": f"{meta['ar']} {num_str}",
                "gold_group_ids": [gid],
                "book_id": book_id,
                "hadith_number": num_str,
                "category": "unseen_arabic_citation",
                "language": "ar",
            })
            idx += 1

            # Category C: Alternate citation form (every 2nd item)
            if idx % 2 == 0:
                alt_formats = [
                    f"{meta['en_full']} {num_str}",
                    f"{meta['en_short']} #{num_str}",
                    f"{meta['en_short']} hadith {num_str}",
                    f"{meta['ar_full']} {num_str}",
                ]
                new_queries.append({
                    "query_id": f"UNSEEN_REF_{idx:04d}",
                    "query": alt_formats[idx % len(alt_formats)],
                    "gold_group_ids": [gid],
                    "book_id": book_id,
                    "hadith_number": num_str,
                    "category": "unseen_alternate_citation",
                    "language": "mixed",
                })
                idx += 1

            # Category D: Arabic numerals (every 3rd item)
            if idx % 3 == 0:
                new_queries.append({
                    "query_id": f"UNSEEN_REF_{idx:04d}",
                    "query": f"{meta['ar']} {ar_num}",
                    "gold_group_ids": [gid],
                    "book_id": book_id,
                    "hadith_number": num_str,
                    "category": "unseen_arabic_numerals",
                    "language": "ar",
                })
                idx += 1

            # Category E: Mixed citation + topic (every 4th item)
            if idx % 4 == 0:
                topic_words = ["prayer", "charity", "fasting", "faith", "intentions", "manners", "knowledge"]
                chosen_topic = topic_words[idx % len(topic_words)]
                new_queries.append({
                    "query_id": f"UNSEEN_REF_{idx:04d}",
                    "query": f"{meta['en_short']} {num_str} about {chosen_topic}",
                    "gold_group_ids": [gid],
                    "book_id": book_id,
                    "hadith_number": num_str,
                    "category": "unseen_mixed_citation_topic",
                    "language": "en",
                })
                idx += 1

            # Category F: Urdu citation (every 5th item)
            if idx % 5 == 0:
                new_queries.append({
                    "query_id": f"UNSEEN_REF_{idx:04d}",
                    "query": f"{meta['ur']} {num_str}",
                    "gold_group_ids": [gid],
                    "book_id": book_id,
                    "hadith_number": num_str,
                    "category": "unseen_urdu_citation",
                    "language": "ur",
                })
                idx += 1

    conn.close()

    # Category G: Malformed / Out-of-bounds citations (adversarial negative tests)
    malformed_queries = [
        ("Bukhari", "unseen_malformed_no_number"),
        ("Muslim", "unseen_malformed_no_number"),
        ("Tirmidhi", "unseen_malformed_no_number"),
        ("Bukhari 999999", "unseen_out_of_bounds"),
        ("Muslim 888888", "unseen_out_of_bounds"),
        ("Tirmidhi 777777", "unseen_out_of_bounds"),
        ("Abu Dawud 999999", "unseen_out_of_bounds"),
        ("Nasa'i 999999", "unseen_out_of_bounds"),
        ("Ibn Majah 999999", "unseen_out_of_bounds"),
        ("Muwatta 999999", "unseen_out_of_bounds"),
        ("Bukhari abc", "unseen_alphabetic_noise"),
        ("Muslim xyz", "unseen_alphabetic_noise"),
        ("hadith invalid_number", "unseen_alphabetic_noise"),
        ("صحيح البخاري 999999", "unseen_out_of_bounds_ar"),
        ("مسلم 999999", "unseen_out_of_bounds_ar"),
    ]

    for q_text, cat in malformed_queries:
        new_queries.append({
            "query_id": f"UNSEEN_REF_{idx:04d}",
            "query": q_text,
            "gold_group_ids": [],  # Gold is strictly EMPTY: system must NOT invent a hit
            "book_id": None,
            "hadith_number": None,
            "category": cat,
            "language": "ar" if any("\u0600" <= c <= "\u06FF" for c in q_text) else "en",
        })
        idx += 1

    # Write output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for q in new_queries:
            f.write(json.dumps(q, ensure_ascii=False) + "\n")

    print(f"\n[SUCCESS] Generated {len(new_queries)} unseen reference validation queries.")
    print(f"[SUCCESS] Saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
