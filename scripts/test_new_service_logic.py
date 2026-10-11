import sqlite3
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HADITH_KG_PATH = os.path.join(REPO_ROOT, "data", "hadith-kg.db")
HADITH_NUMBERING_PATH = os.path.join(REPO_ROOT, "data", "hadith_numbering.db")

sys.path.insert(0, os.path.join(REPO_ROOT, "mizan-web", "backend"))
from scholarly_service import transliterate_scholar, translate_scholarly_statement

COLLECTION_DARUSSALAM_SCHEMES = {
    4: ("abudawud", 12),
    6: ("ibnmajah", 18),
    5: ("nasai", 15),
    3: ("tirmidhi", 9),
}

def get_canonical_hadith_grades(hadith_id: int):
    kg_conn = sqlite3.connect(f"file:{HADITH_KG_PATH}?mode=ro", uri=True)
    kg_conn.row_factory = sqlite3.Row
    num_conn = sqlite3.connect(f"file:{HADITH_NUMBERING_PATH}?mode=ro", uri=True)
    num_conn.row_factory = sqlite3.Row

    try:
        h = kg_conn.execute("SELECT id, book_id, no_inbook, taraf_nass FROM hadiths WHERE id = ?", (hadith_id,)).fetchone()
        if not h:
            return []

        book_id = h['book_id']
        grades = []

        if book_id in COLLECTION_DARUSSALAM_SCHEMES:
            collection_name, scheme_id = COLLECTION_DARUSSALAM_SCHEMES[book_id]
            num_row = num_conn.execute(
                "SELECT primary_number FROM hadith_numbers WHERE hadith_id = ? AND scheme_id = ?",
                (hadith_id, scheme_id)
            ).fetchone()

            if num_row and str(num_row['primary_number']).isdigit():
                d_num = int(num_row['primary_number'])
                hp_row = kg_conn.execute(
                    "SELECT reference_book, reference_hadith FROM hadith_pro_hadiths WHERE collection = ? AND hadith_number = ?",
                    (collection_name, d_num)
                ).fetchone()

                if hp_row:
                    ref_book = hp_row['reference_book']
                    ref_hadith = hp_row['reference_hadith']

                    rows = kg_conn.execute("""
                        SELECT hg.id, ? as hadith_id, hg.source, hg.scholar, hg.grade, hg.reference_book, hg.reference_hadith
                        FROM hadith_grades hg
                        JOIN hadiths h ON h.id = hg.hadith_id
                        WHERE h.book_id = ? AND hg.reference_book = ? AND hg.reference_hadith = ?
                        ORDER BY hg.id
                    """, (hadith_id, book_id, ref_book, ref_hadith)).fetchall()

                    for r in rows:
                        g = dict(r)
                        sch_raw = g.get("scholar")
                        grd_raw = g.get("grade")
                        s_en, s_ar = transliterate_scholar(sch_raw)
                        st_en, st_ar, is_v = translate_scholarly_statement(grd_raw)
                        
                        # Arabic scholar name fix if raw is English
                        if "albani" in str(sch_raw).lower():
                            s_ar = "الألباني"
                        elif "abd al-baqi" in str(sch_raw).lower():
                            s_ar = "محمد فؤاد عبد الباقي"
                        elif "arnaut" in str(sch_raw).lower():
                            s_ar = "شعيب الأرنؤوط"
                        elif "zubair" in str(sch_raw).lower():
                            s_ar = "زبير علي زئي"

                        g["scholar_en"] = s_en
                        g["scholar_ar"] = s_ar
                        g["statement_en"] = st_en
                        g["statement_ar"] = st_ar
                        g["grade_en"] = st_en
                        g["grade_ar"] = st_ar
                        g["is_verified"] = is_v
                        g["reference_formatted"] = f"Book {ref_book}, Hadith {ref_hadith}"
                        g["provenance"] = f"Hadith Pro / Darussalam Edition #{d_num} (Book {ref_book} #{ref_hadith})"
                        grades.append(g)
                    return grades

        # Fallback to direct query if not in Darussalam scheme or not matched
        rows = kg_conn.execute("""
            SELECT id, hadith_id, source, scholar, grade, reference_book, reference_hadith
            FROM hadith_grades
            WHERE hadith_id = ?
            ORDER BY id
        """, (hadith_id,)).fetchall()
        for r in rows:
            g = dict(r)
            s_en, s_ar = transliterate_scholar(g.get("scholar"))
            st_en, st_ar, is_v = translate_scholarly_statement(g.get("grade"))
            g["scholar_en"] = s_en
            g["scholar_ar"] = s_ar
            g["statement_en"] = st_en
            g["statement_ar"] = st_ar
            g["grade_en"] = st_en
            g["grade_ar"] = st_ar
            g["is_verified"] = is_v
            grades.append(g)
        return grades
    finally:
        kg_conn.close()
        num_conn.close()


def get_verified_narrator_aqwal(rawi_id: int):
    kg_conn = sqlite3.connect(f"file:{HADITH_KG_PATH}?mode=ro", uri=True)
    kg_conn.row_factory = sqlite3.Row

    try:
        rawi = kg_conn.execute("SELECT id, name, nickname, rank, tabaka, profession, nasab FROM rawis WHERE id = ?", (rawi_id,)).fetchone()
        if not rawi:
            return []

        rows = kg_conn.execute("""
            SELECT
                a.id AS qawl_id,
                a.alem_id,
                a.rawi_id,
                a.qawl,
                e.name AS scholar_name,
                e.nickname AS scholar_nickname,
                e.shuhra AS scholar_shuhra,
                e.laqab AS scholar_laqab,
                e.tabaka AS scholar_tabaka,
                e.death_year AS scholar_death_year,
                e.rank_no AS scholar_rank_no,
                e.rank AS scholar_rank
            FROM aqwal a
            LEFT JOIN alems e ON e.id = a.alem_id
            WHERE a.rawi_id = ?
            ORDER BY e.death_year, a.id
        """, (rawi_id,)).fetchall()

        aqwal = []
        for r in rows:
            q = dict(r)
            s_en, s_ar = transliterate_scholar(q.get("scholar_name"), q.get("scholar_shuhra"))
            st_en, st_ar, is_v = translate_scholarly_statement(q.get("qawl"))

            q["scholar_en"] = s_en
            q["scholar_ar"] = s_ar
            q["statement_en"] = st_en
            q["statement_ar"] = st_ar
            q["is_verified"] = is_v
            q["attribution_status"] = "verified"
            q["provenance_caveat"] = None

            # ----------------------------------------------------
            # IDENTITY SAFETY RULE: Father/Son Collision on Rawi 4256
            # ----------------------------------------------------
            if rawi_id == 4256 and q.get("alem_id") == 2821:
                # Yahya ibn Ma'in tawthiq collision: belongs to son Wabarah (Rawi #8145)
                q["attribution_status"] = "father_son_collision"
                q["is_verified"] = False
                q["provenance_caveat"] = (
                    "Identity Attribution Unresolved: In classical rijal authorities (al-Mizzi's Tahdhib al-Kamal 17/413, "
                    "al-Dhahabi's Mizan al-I'tidal 2/591, Ibn Hajar's Tahdhib al-Tahdhib 6/262), Yahya ibn Ma'in's tawthiq "
                    "was explicitly declared regarding his son Wabarah ibn Abdur Rahman al-Musli (Rawi #8145, Tarikh Ibn Ma'in #1511). "
                    "Abdur Rahman himself has no verified direct tawthiq from Ibn Ma'in and is evaluated as Maqbul / Majhul."
                )
                q["statement_en"] = "Identity attribution unresolved (Belongs to son Wabarah; no direct tawthiq for Abdur Rahman)"

            aqwal.append(q)

        return aqwal
    finally:
        kg_conn.close()

# TEST 1: Ibn Majah 1986 grades
print("=== GRADES FOR HADITH 28581 (Ibn Majah Darussalam 1986) ===")
for g in get_canonical_hadith_grades(28581):
    print(f"  Scholar: {g['scholar_en']} | Grade: {g['grade_en']} ({g['grade_ar']}) | Ref: {g.get('reference_formatted')}")

# TEST 2: Narrator 4256 aqwal
print("\n=== AQWAL FOR RAWI 4256 (Abdur Rahman al-Musli) ===")
for a in get_verified_narrator_aqwal(4256):
    print(f"  Scholar: {a['scholar_en']} | Status: {a['attribution_status']} | Verified: {a['is_verified']} | Stmt: {a['statement_en']}")
