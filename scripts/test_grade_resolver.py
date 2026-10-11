import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')

kg_conn = sqlite3.connect('data/hadith-kg.db')
kg_conn.row_factory = sqlite3.Row
num_conn = sqlite3.connect('data/hadith_numbering.db')
num_conn.row_factory = sqlite3.Row

COLLECTION_MAP = {
    4: ('abudawud', 12),
    6: ('ibnmajah', 18),
    5: ('nasai', 15),
    3: ('tirmidhi', 9),
}

def resolve_grades_for_canonical_hadith(hadith_id: int):
    """
    Deterministically resolves authentic scholarly grades for a canonical hadith.
    Does NOT rely on faulty import-time assumptions (where Darussalam number was treated as no_inbook).
    Uses canonical hadiths.id -> Darussalam scheme in hadith_numbering.db -> hadith_pro_hadiths -> verified grades.
    """
    # 1. Get hadith info
    h = kg_conn.execute("SELECT id, book_id, no_inbook, taraf_nass FROM hadiths WHERE id = ?", (hadith_id,)).fetchone()
    if not h:
        return []

    book_id = h['book_id']
    if book_id not in COLLECTION_MAP:
        # Standard query for books without Darussalam cross-numbering issues
        return kg_conn.execute("SELECT * FROM hadith_grades WHERE hadith_id = ? ORDER BY id", (hadith_id,)).fetchall()

    collection_name, scheme_id = COLLECTION_MAP[book_id]

    # 2. Look up the verified Darussalam primary number for this canonical hadith
    num_row = num_conn.execute(
        "SELECT primary_number FROM hadith_numbers WHERE hadith_id = ? AND scheme_id = ?",
        (hadith_id, scheme_id)
    ).fetchone()

    if not num_row:
        # Fallback to direct hadith_grades if no scheme mapping exists
        return kg_conn.execute("SELECT * FROM hadith_grades WHERE hadith_id = ? ORDER BY id", (hadith_id,)).fetchall()

    darussalam_number = int(num_row['primary_number'])

    # 3. Look up the Hadith Pro reference from hadith_pro_hadiths
    hp_row = kg_conn.execute(
        "SELECT reference_book, reference_hadith FROM hadith_pro_hadiths WHERE collection = ? AND hadith_number = ?",
        (collection_name, darussalam_number)
    ).fetchone()

    if not hp_row:
        return kg_conn.execute("SELECT * FROM hadith_grades WHERE hadith_id = ? ORDER BY id", (hadith_id,)).fetchall()

    ref_book = hp_row['reference_book']
    ref_hadith = hp_row['reference_hadith']

    # 4. Find the grade records belonging to this exact collection and reference
    # Note: To avoid cross-collection collision in reference_book/reference_hadith,
    # we filter by hadith_id that belongs to the same book_id
    verified_grades = kg_conn.execute("""
        SELECT hg.id, ? as hadith_id, hg.source, hg.scholar, hg.grade, hg.reference_book, hg.reference_hadith
        FROM hadith_grades hg
        JOIN hadiths h ON h.id = hg.hadith_id
        WHERE h.book_id = ? AND hg.reference_book = ? AND hg.reference_hadith = ?
        ORDER BY hg.id
    """, (hadith_id, book_id, ref_book, ref_hadith)).fetchall()

    return verified_grades

# Test on 28581 (Darussalam 1986)
print("=== TESTING CANONICAL HADITH 28581 (Ibn Majah Darussalam 1986) ===")
grades_28581 = resolve_grades_for_canonical_hadith(28581)
for g in grades_28581:
    print(f"id={g['id']} hadith_id={g['hadith_id']} scholar={g['scholar']} grade={g['grade']} ref_book={g['reference_book']} ref_hadith={g['reference_hadith']}")

# Test on 28571 (Ibn Majah Darussalam 1976 - Usamah)
print("\n=== TESTING CANONICAL HADITH 28571 (Ibn Majah Darussalam 1976 - Usamah) ===")
grades_28571 = resolve_grades_for_canonical_hadith(28571)
for g in grades_28571:
    print(f"id={g['id']} hadith_id={g['hadith_id']} scholar={g['scholar']} grade={g['grade']} ref_book={g['reference_book']} ref_hadith={g['reference_hadith']}")

# Test on 28591 (Ibn Majah Darussalam 1996 - Jealousy)
print("\n=== TESTING CANONICAL HADITH 28591 (Ibn Majah Darussalam 1996 - Jealousy) ===")
grades_28591 = resolve_grades_for_canonical_hadith(28591)
for g in grades_28591:
    print(f"id={g['id']} hadith_id={g['hadith_id']} scholar={g['scholar']} grade={g['grade']} ref_book={g['reference_book']} ref_hadith={g['reference_hadith']}")
