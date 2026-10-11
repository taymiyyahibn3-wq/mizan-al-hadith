from pathlib import Path
import json
import sqlite3
import re
import unicodedata
import urllib.error
import urllib.request

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="MÄ«zÄn al-HadÄ«th API",
    description="Hadith Research & Verification API",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DATABASE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = (
    BASE_DIR
    / ".."
    / ".."
    / "data"
    / "hadith-kg.db"
).resolve()


def get_db():
    """
    Open Hadith database in read-only mode.

    The API never modifies the source database.
    """

    if not DB_PATH.exists():
        raise RuntimeError(
            f"Hadith database not found: {DB_PATH}"
        )

    db_uri = f"file:{DB_PATH}?mode=ro"

    db = sqlite3.connect(
        db_uri,
        uri=True,
        timeout=30,
    )

    # Allows:
    # row["id"]
    # row["name"]
    # etc.
    db.row_factory = sqlite3.Row

    return db


# ============================================================
# HEALTH
# ============================================================

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "MÄ«zÄn al-HadÄ«th API",
    }


# ============================================================
# STATS
# ============================================================

@app.get("/api/stats")
def stats():
    db = get_db()

    try:
        hadiths = db.execute(
            "SELECT COUNT(*) FROM hadiths"
        ).fetchone()[0]

        books = db.execute(
            "SELECT COUNT(*) FROM books"
        ).fetchone()[0]

        narrators = db.execute(
            "SELECT COUNT(*) FROM rawis"
        ).fetchone()[0]

        sanads = db.execute(
            "SELECT COUNT(*) FROM sanads"
        ).fetchone()[0]

        return {
            "hadiths": hadiths,
            "books": books,
            "narrators": narrators,
            "sanads": sanads,
        }

    finally:
        db.close()


# ============================================================
# BOOKS
# ============================================================

@app.get("/api/books")
def get_books():
    db = get_db()

    try:
        rows = db.execute(
            """
            SELECT
                id,
                name,
                author_no,
                author_name,
                author_death_year,
                city,
                dar,
                tabaa,
                tasnif_no,
                tasnif,
                hadith_qty
            FROM books
            ORDER BY id
            """
        ).fetchall()

        return {
            "count": len(rows),
            "books": [dict(row) for row in rows],
        }

    finally:
        db.close()


# ============================================================
# BOOK HADITHS
#
# Returns hadiths belonging to one specific book.
#
# IMPORTANT:
# This route is placed before the generic:
# /api/hadith/{hadith_id}
# route so it cannot be mistaken for a hadith ID.
# ============================================================

@app.get("/api/books/{book_id}/hadiths")
def get_book_hadiths(
    book_id: int,
    limit: int = Query(30, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    db = get_db()

    try:
        # ----------------------------------------------------
        # Verify book
        # ----------------------------------------------------

        book = db.execute(
            """
            SELECT
                id,
                name,
                author_no,
                author_name,
                author_death_year,
                city,
                dar,
                tabaa,
                tasnif_no,
                tasnif,
                hadith_qty
            FROM books
            WHERE id = ?
            """,
            (book_id,),
        ).fetchone()

        if book is None:
            raise HTTPException(
                status_code=404,
                detail="Book not found",
            )

        # ----------------------------------------------------
        # Total hadith count
        # ----------------------------------------------------

        total = db.execute(
            """
            SELECT COUNT(*)
            FROM hadiths
            WHERE book_id = ?
            """,
            (book_id,),
        ).fetchone()[0]

        # ----------------------------------------------------
        # Hadiths
        # ----------------------------------------------------

        rows = db.execute(
            """
            SELECT
                h.id,
                h.book_id,
                h.no_inbook,
                h.page_no,
                h.type_no,
                h.type,
                h.matn_no,
                h.matn,
                h.group_id,
                h.takhrij,
                h.taraf_nass,
                h.nass
            FROM hadiths h
            WHERE h.book_id = ?
            ORDER BY
                h.no_inbook,
                h.id
            LIMIT ?
            OFFSET ?
            """,
            (
                book_id,
                limit,
                offset,
            ),
        ).fetchall()

        return {
            "book": dict(book),
            "total": total,
            "limit": limit,
            "offset": offset,
            "results": [
                dict(row)
                for row in rows
            ],
        }

    finally:
        db.close()


# ============================================================
# ARABIC TEXT NORMALIZATION & HADITH SEARCH SYSTEM
# ============================================================

ARABIC_STOPWORDS = {
    "من", "في", "ما", "عن", "على", "ان", "أن", "إن", "او", "أو", "لا", "ثم", "مع", "كل", "هو", "هي", "قد", "كان", "كانت"
}


def strip_tashkeel(value: str) -> str:
    """Remove diacritics/tashkeel and tatweel while preserving letter identities."""
    value = unicodedata.normalize("NFKC", str(value or ""))
    return re.sub(r"[\u064B-\u065F\u0670\u06D6-\u06ED\u0610-\u061A\u0640]", "", value)


def normalize_arabic(value: str) -> str:
    """
    Module-level reusable function to normalize Arabic text.
    - Unicode NFKC normalize
    - remove tashkeel/U+064B-U+065F, U+0670, U+06D6-U+06ED, U+0610-U+061A
    - remove tatweel
    - normalize إ أ ٱ آ -> ا
    - normalize ى -> ي
    - normalize ئ -> ي
    - normalize ؤ -> و
    - normalize ة -> ه
    - replace punctuation/non-Arabic separators with spaces
    - collapse whitespace
    """
    value = unicodedata.normalize("NFKC", str(value or ""))
    value = re.sub(r"[\u064B-\u065F\u0670\u06D6-\u06ED\u0610-\u061A]", "", value)
    value = value.replace("\u0640", "")
    value = re.sub(r"[إأٱآ]", "ا", value)
    value = value.replace("ى", "ي").replace("ئ", "ي").replace("ؤ", "و").replace("ة", "ه")
    value = re.sub(r"[^\w\s]+|_", " ", value, flags=re.UNICODE)
    return " ".join(value.split()).strip()


def perform_hadith_search(
    db: sqlite3.Connection,
    q: str,
    limit: int = 20,
    offset: int = 0,
    book_id: int | None = None,
) -> dict:
    """
    Search hadith text with strict candidate retrieval + normalized ranking.

    Important design rule:
    - Candidate retrieval is AND across several query tokens, not OR.
      OR across every token was the cause of huge irrelevant result sets.
    - Each token itself allows spelling/diacritic variants.
    - Long quotations are additionally required to have strong token coverage
      before they are returned.
    """
    raw_query = " ".join(str(q).split()).strip()
    nq = normalize_arabic(raw_query)

    empty_res = {
        "query": raw_query,
        "limit": limit,
        "offset": offset,
        "count": 0,
        "results": [],
        "search_mode": "empty",
    }
    if book_id is not None:
        empty_res["book_id"] = book_id

    if not nq:
        return empty_res

    q_tokens = [t for t in nq.split() if t]
    q_set = set(q_tokens)
    raw_tokens = re.findall(r"[\u0621-\u065F\u0670-\u06ED\w]+", raw_query)

    # Keep the query's actual order. For a quotation, the opening words are
    # extremely useful anchors. Then add distinctive longer words.
    selected = []
    seen_norm = set()

    for raw_token in raw_tokens:
        norm = normalize_arabic(raw_token)
        if not norm or len(norm) < 2 or norm in seen_norm:
            continue
        seen_norm.add(norm)
        selected.append((raw_token, norm))

    if not selected:
        selected = [(raw_query, nq)]

    # Prefer first words plus distinctive content words. Do not make "الله"
    # or generic sanad words the only anchors for a long quotation.
    first = selected[:3]
    rest = selected[3:]
    rest.sort(
        key=lambda x: (
            x[1] not in ARABIC_STOPWORDS,
            len(x[1]),
        ),
        reverse=True,
    )

    if len(q_tokens) >= 8:
        chosen = first + rest[:5]
    elif len(q_tokens) >= 3:
        chosen = first + rest[:2]
    else:
        chosen = selected[:3]

    # De-duplicate normalized tokens.
    anchors = []
    seen = set()
    for raw_token, norm_token in chosen:
        if norm_token not in seen:
            seen.add(norm_token)
            anchors.append((raw_token, norm_token))

    def variants(raw_token: str, norm_token: str) -> list[str]:
        values = []
        for value in (
            strip_tashkeel(raw_token),
            raw_token,
            norm_token,
        ):
            value = str(value or "").strip()
            if value and value not in values:
                values.append(value)
        return values

    # Candidate retrieval:
    # AND between query-token groups, OR between spelling variants and fields.
    # This prevents a query for one specific hadith from returning every hadith
    # that merely contains one common word such as "الله".
    token_groups = []
    params: list[object] = []

    for raw_token, norm_token in anchors:
        variants_for_token = variants(raw_token, norm_token)
        variant_clauses = []
        for term in variants_for_token:
            like = f"%{term}%"
            variant_clauses.append(
                "(h.nass LIKE ? OR h.taraf_nass LIKE ? OR h.matn LIKE ?)"
            )
            params.extend((like, like, like))
        token_groups.append("(" + " OR ".join(variant_clauses) + ")")

    where_parts = []
    if token_groups:
        where_parts.append("(" + " AND ".join(token_groups) + ")")

    if book_id is not None:
        where_parts.append("h.book_id = ?")
        params.append(book_id)

    where_sql = " AND ".join(where_parts) or "1=0"

    rows = db.execute(
        f"""
        SELECT h.id, h.book_id, h.no_inbook, h.matn_no, h.matn,
               h.nass, h.taraf_nass, h.group_id,
               b.name AS book_name, b.author_name
        FROM hadiths h
        LEFT JOIN books b ON b.id = h.book_id
        WHERE {where_sql}
        LIMIT 10000
        """,
        params,
    ).fetchall()

    # If the strict multi-token candidate query found nothing, progressively
    # relax it. This is useful for short/fuzzy searches, but only after the
    # strict path has had a chance to find the exact quotation.
    if not rows and len(anchors) > 1:
        fallback_groups = []
        fallback_params: list[object] = []

        # Use the first two query tokens as mandatory anchors.
        for raw_token, norm_token in anchors[:2]:
            variant_clauses = []
            for term in variants(raw_token, norm_token):
                like = f"%{term}%"
                variant_clauses.append(
                    "(h.nass LIKE ? OR h.taraf_nass LIKE ? OR h.matn LIKE ?)"
                )
                fallback_params.extend((like, like, like))
            fallback_groups.append("(" + " OR ".join(variant_clauses) + ")")

        fallback_where = "(" + " AND ".join(fallback_groups) + ")"
        if book_id is not None:
            fallback_where += " AND h.book_id = ?"
            fallback_params.append(book_id)

        rows = db.execute(
            f"""
            SELECT h.id, h.book_id, h.no_inbook, h.matn_no, h.matn,
                   h.nass, h.taraf_nass, h.group_id,
                   b.name AS book_name, b.author_name
            FROM hadiths h
            LEFT JOIN books b ON b.id = h.book_id
            WHERE {fallback_where}
            LIMIT 10000
            """,
            fallback_params,
        ).fetchall()

    total_q_tokens = max(1, len(q_tokens))
    long_query = len(q_tokens) >= 6 or len(raw_query) >= 40

    def score_field(field_text: str | None):
        if not field_text:
            return 0, 0.0, 0.0, 0.0, "none"

        nf = normalize_arabic(field_text)
        if not nf:
            return 0, 0.0, 0.0, 0.0, "none"

        ft = nf.split()
        f_set = set(ft)

        # Exact normalized phrase match is strongest.
        is_exact = 1 if nq in nf else 0

        # Also support a compact phrase where punctuation/spacing differs.
        if not is_exact and len(nq.replace(" ", "")) >= 10:
            if nq.replace(" ", "") in nf.replace(" ", ""):
                is_exact = 1

        coverage = len(q_set & f_set) / total_q_tokens

        # True ordered consecutive run, not merely "all words exist".
        longest = 0
        current = 0
        for token in q_tokens:
            if token in f_set:
                current += 1
                longest = max(longest, current)
            else:
                current = 0

        ordered = longest / total_q_tokens

        if is_exact:
            score = 1.0
            match_type = "exact_phrase"
        else:
            score = round((0.60 * coverage) + (0.40 * ordered), 4)
            match_type = "normalized"

        return is_exact, coverage, ordered, score, match_type

    scored = []

    for row in rows:
        best = (0, 0.0, 0.0, 0.0, "none", "nass")

        for field_name, field_value in (
            ("nass", row["nass"]),
            ("taraf_nass", row["taraf_nass"]),
            ("matn", row["matn"]),
        ):
            exact_flag, coverage, ordered, score, match_type = score_field(
                field_value
            )
            candidate = (
                exact_flag,
                coverage,
                ordered,
                score,
                match_type,
                field_name,
            )
            if candidate[:4] > best[:4]:
                best = candidate

        best_exact, coverage, ordered, score, match_type, field_name = best

        # Strictness is the important fix:
        # long quotations must have very high coverage and ordered evidence.
        if long_query:
            accepted = (
                best_exact == 1
                or (
                    coverage >= 0.80
                    and ordered >= 0.50
                )
            )
        else:
            # Short queries remain useful as ordinary word searches.
            accepted = coverage > 0

        if accepted:
            item = dict(row)
            item["score"] = round(score, 4)
            item["match_type"] = match_type
            item["matched_field"] = field_name
            item["_exact"] = best_exact
            item["_coverage"] = coverage
            item["_ordered"] = ordered
            scored.append(item)

    # Exact phrase > complete token coverage > ordered sequence > id.
    scored.sort(
        key=lambda x: (
            -x["_exact"],
            -x["_coverage"],
            -x["_ordered"],
            x["id"],
        )
    )

    for item in scored:
        item.pop("_exact", None)
        item.pop("_coverage", None)
        item.pop("_ordered", None)

    response = {
        "query": raw_query,
        "limit": limit,
        "offset": offset,
        "count": len(scored),
        "results": scored[offset:offset + limit],
        "search_mode": "strict_normalized_ranked",
    }

    if book_id is not None:
        response["book_id"] = book_id

    return response


# ============================================================
# BOOK HADITH NUMBER LOOKUP
#
# "Hadith #N" means the book-local number (no_inbook), not the
# global database primary key (id).
# ============================================================

@app.get("/api/books/{book_id}/hadith/{hadith_number}")
def get_book_hadith_by_number(
    book_id: int,
    hadith_number: int,
):
    db = get_db()
    try:
        row = db.execute(
            """
            SELECT
                h.id,
                h.book_id,
                h.no_inbook,
                h.page_no,
                h.type_no,
                h.type,
                h.matn_no,
                h.matn,
                h.group_id,
                h.takhrij,
                h.taraf_nass,
                h.nass,
                h.matn_start,
                h.matn_end,
                b.name AS book_name,
                b.author_name,
                b.author_death_year,
                b.tasnif
            FROM hadiths h
            LEFT JOIN books b
                ON b.id = h.book_id
            WHERE h.book_id = ?
              AND h.no_inbook = ?
            ORDER BY h.id
            LIMIT 1
            """,
            (book_id, hadith_number),
        ).fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail=f"Hadith {hadith_number} not found in book {book_id}",
            )

        return dict(row)
    finally:
        db.close()


# ============================================================
# BOOK HADITH SEARCH
# ============================================================

@app.get("/api/books/{book_id}/hadiths/search")
@app.get("/api/books/{book_id}/search")
def search_book_hadiths(
    book_id: int,
    q: str = Query(..., min_length=1),
    limit: int = Query(30, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Search Arabic hadith text within a specific book collection."""
    db = get_db()
    try:
        book = db.execute(
            "SELECT id, name FROM books WHERE id = ?",
            (book_id,),
        ).fetchone()
        if book is None:
            raise HTTPException(
                status_code=404,
                detail="Book not found",
            )
        return perform_hadith_search(db, q, limit, offset, book_id=book_id)
    finally:
        db.close()


# ============================================================
# HADITH SEARCH
#
# IMPORTANT:
# This route MUST remain before:
# /api/hadith/{hadith_id}
# ============================================================

@app.get("/api/hadith/search")
def search_hadith(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Search Arabic hadith text robustly across nass, taraf_nass and matn."""
    db = get_db()
    try:
        return perform_hadith_search(db, q, limit, offset, book_id=None)
    finally:
        db.close()



@app.get("/api/hadith/{hadith_id}/group")
def get_hadith_group(hadith_id: int):
    db = get_db()

    try:
        # ----------------------------------------------------
        # Current Hadith
        # ----------------------------------------------------

        hadith = db.execute(
            """
            SELECT
                h.id,
                h.book_id,
                h.no_inbook,
                h.page_no,
                h.type_no,
                h.type,
                h.matn_no,
                h.group_id,
                h.takhrij,
                h.taraf_nass,

                b.name AS book_name,
                b.author_name,
                b.author_death_year

            FROM hadiths h

            LEFT JOIN books b
                ON b.id = h.book_id

            WHERE h.id = ?
            """,
            (hadith_id,),
        ).fetchone()

        if hadith is None:
            raise HTTPException(
                status_code=404,
                detail="Hadith not found",
            )

        hadith_data = dict(hadith)
        group_id = hadith_data["group_id"]

        # ----------------------------------------------------
        # No Group
        # ----------------------------------------------------

        if group_id is None:
            return {
                "hadith_id": hadith_id,
                "group_id": None,
                "count": 0,
                "meaning_group": None,
                "taraf": None,
                "hadiths": [],
            }

        # ----------------------------------------------------
        # Meaning Group
        # ----------------------------------------------------

        meaning_group = db.execute(
            """
            SELECT
                id,
                taraf_id,
                is_qudsi,
                matn_no,
                sahaba_qty,
                repeat_qty,
                nass

            FROM meaning_groups

            WHERE id = ?
            """,
            (group_id,),
        ).fetchone()

        meaning_group_data = (
            dict(meaning_group)
            if meaning_group is not None
            else None
        )

        # ----------------------------------------------------
        # Taraf
        # ----------------------------------------------------

        taraf = db.execute(
            """
            SELECT
                id,
                nass,
                matn_no,
                matn,
                is_qudsi,
                group_id

            FROM tarafs

            WHERE group_id = ?

            ORDER BY id

            LIMIT 1
            """,
            (group_id,),
        ).fetchone()

        taraf_data = (
            dict(taraf)
            if taraf is not None
            else None
        )

        # ----------------------------------------------------
        # All Hadiths In Group
        # ----------------------------------------------------

        rows = db.execute(
            """
            SELECT
                h.id,
                h.book_id,
                h.no_inbook,
                h.page_no,
                h.type_no,
                h.type,
                h.matn_no,
                h.group_id,
                h.takhrij,
                h.taraf_nass,

                b.name AS book_name,
                b.author_name,
                b.author_death_year

            FROM hadiths h

            LEFT JOIN books b
                ON b.id = h.book_id

            WHERE h.group_id = ?

            ORDER BY
                h.book_id,
                h.no_inbook,
                h.id
            """,
            (group_id,),
        ).fetchall()

        grouped_hadiths = [
            dict(row)
            for row in rows
        ]

        return {
            "hadith_id": hadith_id,
            "group_id": group_id,
            "count": len(grouped_hadiths),
            "meaning_group": meaning_group_data,
            "taraf": taraf_data,
            "hadiths": grouped_hadiths,
        }

    finally:
        db.close()


# ============================================================
# HADITH SANAD
# ============================================================

@app.get("/api/hadith/{hadith_id}/sanad")
def get_hadith_sanad(hadith_id: int):
    db = get_db()

    try:
        # ----------------------------------------------------
        # Verify Hadith
        # ----------------------------------------------------

        hadith = db.execute(
            """
            SELECT id
            FROM hadiths
            WHERE id = ?
            """,
            (hadith_id,),
        ).fetchone()

        if hadith is None:
            raise HTTPException(
                status_code=404,
                detail="Hadith not found",
            )

        # ----------------------------------------------------
        # Sanads
        # ----------------------------------------------------

        sanad_rows = db.execute(
            """
            SELECT
                id,
                hadith_id,
                matn_no,
                matn,
                hukum,
                group_id,
                takhrij,
                max_rank,
                length

            FROM sanads

            WHERE hadith_id = ?

            ORDER BY id
            """,
            (hadith_id,),
        ).fetchall()

        sanads = []

        for sanad_row in sanad_rows:
            sanad = dict(sanad_row)

            # ------------------------------------------------
            # Rawis
            # ------------------------------------------------

            rawi_rows = db.execute(
                """
                SELECT
                    sr.pos,
                    sr.rawi_id,

                    r.name,
                    r.nickname,
                    r.rank_no,
                    r.rank,
                    r.tabaka,

                    r.is_bukhari,
                    r.is_muslim,

                    r.has_ikhtilat,
                    r.has_tadlis,

                    r.riwaya_qty,

                    r.birth_year,
                    r.birth_year_raw,

                    r.death_year,
                    r.death_year_raw,

                    r.age_raw,

                    r.profession,
                    r.nasab,
                    r.iqama,
                    r.death_place,

                    r.is_stub

                FROM sanad_rawis sr

                LEFT JOIN rawis r
                    ON r.id = sr.rawi_id

                WHERE sr.sanad_id = ?

                ORDER BY sr.pos
                """,
                (sanad["id"],),
            ).fetchall()

            sanad["rawis"] = [
                dict(row)
                for row in rawi_rows
            ]

            sanads.append(sanad)

        return {
            "hadith_id": hadith_id,
            "sanad_count": len(sanads),
            "sanads": sanads,
        }

    finally:
        db.close()


# ============================================================
# ENGLISH HADITH TRANSLATION
# ============================================================

TRANSLATION_EDITIONS = {
    # Verified English editions present in the project's Hadith Pro assets
    # and also available through the Hadith API dataset.
    1: ("eng-bukhari", "Sahih al-Bukhari"),
    2: ("eng-muslim", "Sahih Muslim"),
    3: ("eng-tirmidhi", "Jami` at-Tirmidhi"),
    4: ("eng-abudawud", "Sunan Abi Dawud"),
    5: ("eng-nasai", "Sunan an-Nasa'i"),
    6: ("eng-ibnmajah", "Sunan Ibn Majah"),
    8: ("eng-malik", "Muwatta Malik"),
}


def _translation_fetch(edition: str, number: int):
    url = f"https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/{edition}/{number}.json"
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mizan-al-Hadith/1.0"},
    )
    with urllib.request.urlopen(request, timeout=8) as response:
        payload = json.loads(response.read().decode("utf-8"))

    hadiths = payload.get("hadiths") or []
    if not hadiths:
        return None, url
    item = hadiths[0] or {}
    text = item.get("text") or item.get("translation")
    if isinstance(text, dict):
        text = text.get("text")
    return ({
        "text": str(text).strip() if text else None,
        "narrator": item.get("narrator"),
        "reference": item.get("reference"),
    } if text else None), url


@app.get("/api/translation-coverage")
def translation_coverage():
    db = get_db()
    try:
        rows = db.execute(
            "SELECT id, name, hadith_qty FROM books ORDER BY id"
        ).fetchall()
        result = []
        for row in rows:
            mapped = row["id"] in TRANSLATION_EDITIONS
            edition = TRANSLATION_EDITIONS.get(row["id"])
            result.append({
                "book_id": row["id"],
                "book_name": row["name"],
                "hadith_qty": row["hadith_qty"],
                "translation_available": mapped,
                "edition": edition[0] if edition else None,
                "edition_name": edition[1] if edition else None,
            })
        return {
            "total_books": len(result),
            "books_with_verified_english_source": sum(1 for x in result if x["translation_available"]),
            "books": result,
        }
    finally:
        db.close()


@app.get("/api/hadith/{hadith_id}/translation")
def get_hadith_translation(hadith_id: int):
    db = get_db()
    try:
        row = db.execute(
            """SELECT h.id, h.book_id, h.no_inbook, b.name AS book_name
               FROM hadiths h LEFT JOIN books b ON b.id = h.book_id
               WHERE h.id = ?""",
            (hadith_id,),
        ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Hadith not found")

        edition_info = TRANSLATION_EDITIONS.get(row["book_id"])
        number = row["no_inbook"]
        if not edition_info or number is None:
            return {
                "available": False,
                "message": "No verified English translation source is mapped for this collection.",
                "book_id": row["book_id"],
                "book_name": row["book_name"],
                "hadith_number": number,
            }

        edition, edition_name = edition_info
        try:
            item, url = _translation_fetch(edition, int(number))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            return {
                "available": False,
                "message": "The English translation source is temporarily unavailable. Arabic remains available.",
                "book_id": row["book_id"],
                "book_name": row["book_name"],
                "hadith_number": number,
                "edition": edition,
                "source_url": url if 'url' in locals() else None,
            }

        if not item:
            return {
                "available": False,
                "message": "No English translation was found for this collection number.",
                "book_id": row["book_id"],
                "book_name": row["book_name"],
                "hadith_number": number,
                "edition": edition,
                "source_url": url,
            }

        reference = item.get("reference")
        if isinstance(reference, dict):
            reference = reference.get("book") or reference.get("hadith") or reference.get("number")

        return {
            "available": True,
            "text": item["text"],
            "narrator": item.get("narrator"),
            "reference": reference,
            "source": "Hadith API dataset",
            "source_url": url,
            "edition": edition,
            "edition_name": edition_name,
            "book_id": row["book_id"],
            "book_name": row["book_name"],
            "hadith_number": number,
        }
    finally:
        db.close()


# ============================================================
# HADITH GRADES
# ============================================================

@app.get("/api/hadith/{hadith_id}/grades")
def get_hadith_grades(hadith_id: int):
    db = get_db()

    try:
        # ----------------------------------------------------
        # Verify Hadith
        # ----------------------------------------------------

        hadith = db.execute(
            """
            SELECT id
            FROM hadiths
            WHERE id = ?
            """,
            (hadith_id,),
        ).fetchone()

        if hadith is None:
            raise HTTPException(
                status_code=404,
                detail="Hadith not found",
            )

        # ----------------------------------------------------
        # Grades
        # ----------------------------------------------------

        rows = db.execute(
            """
            SELECT
                id,
                hadith_id,
                source,
                scholar,
                grade,
                reference_book,
                reference_hadith

            FROM hadith_grades

            WHERE hadith_id = ?

            ORDER BY id
            """,
            (hadith_id,),
        ).fetchall()

        grades = [
            dict(row)
            for row in rows
        ]

        return {
            "hadith_id": hadith_id,
            "count": len(grades),
            "grades": grades,
        }

    finally:
        db.close()


# ============================================================
# HADITH TOPICS
# ============================================================

@app.get("/api/hadith/{hadith_id}/topics")
def get_hadith_topics(hadith_id: int):
    db = get_db()

    try:
        # ----------------------------------------------------
        # Get Hadith Group
        # ----------------------------------------------------

        hadith = db.execute(
            """
            SELECT
                id,
                group_id

            FROM hadiths

            WHERE id = ?
            """,
            (hadith_id,),
        ).fetchone()

        if hadith is None:
            raise HTTPException(
                status_code=404,
                detail="Hadith not found",
            )

        group_id = hadith["group_id"]

        # ----------------------------------------------------
        # No Group
        # ----------------------------------------------------

        if group_id is None:
            return {
                "hadith_id": hadith_id,
                "group_id": None,
                "count": 0,
                "topics": [],
            }

        # ----------------------------------------------------
        # Topics
        # ----------------------------------------------------

        topics = db.execute(
            """
            SELECT
                id,
                name,
                parent_id,
                level,
                lft,
                rgt,
                tree_id,
                group_id

            FROM topics

            WHERE group_id = ?

            ORDER BY
                level,
                lft,
                id
            """,
            (group_id,),
        ).fetchall()

        result = []

        for topic_row in topics:
            topic = dict(topic_row)

            parent = None

            if topic["parent_id"] is not None:
                parent_row = db.execute(
                    """
                    SELECT
                        id,
                        name,
                        parent_id,
                        level

                    FROM topics

                    WHERE id = ?
                    """,
                    (topic["parent_id"],),
                ).fetchone()

                if parent_row is not None:
                    parent = dict(parent_row)

            topic["parent"] = parent

            result.append(topic)

        return {
            "hadith_id": hadith_id,
            "group_id": group_id,
            "count": len(result),
            "topics": result,
        }

    finally:
        db.close()


# ============================================================
# HADITH FULL RECORD
#
# IMPORTANT:
# This MUST remain AFTER all:
# /api/hadith/{hadith_id}/...
# routes.
# ============================================================

@app.get("/api/hadith/{hadith_id}")
def get_hadith(hadith_id: int):
    db = get_db()

    try:
        row = db.execute(
            """
            SELECT
                h.id,
                h.book_id,
                h.no_inbook,
                h.page_no,
                h.type_no,
                h.type,
                h.matn_no,
                h.matn,
                h.group_id,
                h.takhrij,
                h.taraf_nass,
                h.nass,
                h.matn_start,
                h.matn_end,

                b.name AS book_name,
                b.author_name,
                b.author_death_year,
                b.tasnif

            FROM hadiths h

            LEFT JOIN books b
                ON b.id = h.book_id

            WHERE h.id = ?
            """,
            (hadith_id,),
        ).fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Hadith not found",
            )

        return dict(row)

    finally:
        db.close()


# ============================================================
# ============================================================
# NARRATORS LIST / SEARCH
# ============================================================

@app.get("/api/narrators")
def list_narrators(q: str = Query(""), limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0)):
    db = get_db()
    try:
        term = q.strip()
        where = ""
        params: list[object] = []
        if term:
            like = f"%{term}%"
            where = "WHERE name LIKE ? OR nickname LIKE ? OR rank LIKE ?"
            params = [like, like, like]
        count = db.execute(f"SELECT COUNT(*) FROM rawis {where}", params).fetchone()[0]
        rows = db.execute(f"""SELECT id, name, nickname, rank, tabaka, riwaya_qty FROM rawis {where} ORDER BY name COLLATE NOCASE, id LIMIT ? OFFSET ?""", params + [limit, offset]).fetchall()
        return {"count": count, "limit": limit, "offset": offset, "narrators": [dict(row) for row in rows]}
    finally:
        db.close()


# NARRATOR AQWAL
#
# IMPORTANT:
# This MUST remain BEFORE:
# /api/narrator/{rawi_id}
# ============================================================

@app.get("/api/narrator/{rawi_id}/aqwal")
def get_narrator_aqwal(rawi_id: int):
    db = get_db()

    try:
        # ----------------------------------------------------
        # Verify Narrator
        # ----------------------------------------------------

        narrator = db.execute(
            """
            SELECT id
            FROM rawis
            WHERE id = ?
            """,
            (rawi_id,),
        ).fetchone()

        if narrator is None:
            raise HTTPException(
                status_code=404,
                detail="Narrator not found",
            )

        # ----------------------------------------------------
        # Scholarly Statements
        # ----------------------------------------------------

        rows = db.execute(
            """
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

            LEFT JOIN alems e
                ON e.id = a.alem_id

            WHERE a.rawi_id = ?

            ORDER BY
                e.death_year,
                a.id
            """,
            (rawi_id,),
        ).fetchall()

        aqwal = [
            dict(row)
            for row in rows
        ]

        return {
            "rawi_id": rawi_id,
            "count": len(aqwal),
            "aqwal": aqwal,
        }

    finally:
        db.close()


# ============================================================
# NARRATOR PROFILE
# ============================================================

@app.get("/api/narrator/{rawi_id}")
def get_narrator(rawi_id: int):
    db = get_db()

    try:
        row = db.execute(
            """
            SELECT
                id,
                name,
                nickname,

                rank_no,
                rank,
                tabaka,

                is_bukhari,
                is_muslim,

                has_ikhtilat,
                has_tadlis,

                riwaya_qty,

                birth_year,
                birth_year_raw,

                death_year,
                death_year_raw,

                age_raw,

                profession,
                nasab,
                iqama,
                death_place,

                is_stub

            FROM rawis

            WHERE id = ?
            """,
            (rawi_id,),
        ).fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Narrator not found",
            )

        return dict(row)

    finally:
        db.close()


# ============================================================
# STARTUP INFORMATION
# ============================================================

@app.on_event("startup")
def startup_check():
    """
    Verify database availability when the API starts.
    """

    if not DB_PATH.exists():
        raise RuntimeError(
            f"Database not found at: {DB_PATH}"
        )

    print("=" * 70)
    print("MÄªZÄ€N AL-HADÄªTH API")
    print("=" * 70)
    print(f"Database: {DB_PATH}")
    print("CORS: localhost:3000 + 127.0.0.1:3000")
    print("Status: READY")
    print("=" * 70)
