import sqlite3
import json

def inspect_details():
    out = {}
    
    # 1. hadith_commentaries
    conn = sqlite3.connect('file:data/hadith_commentaries.db?mode=ro', uri=True)
    c = conn.cursor()
    c.execute("SELECT * FROM commentary_sources")
    cols = [col[0] for col in c.description]
    rows = c.fetchall()
    out['commentary_sources'] = [dict(zip(cols, r)) for r in rows]
    c.execute("PRAGMA table_info(hadith_commentaries)")
    out['hadith_commentaries_columns'] = [col[1] for col in c.fetchall()]
    c.execute("SELECT * FROM hadith_commentaries LIMIT 3")
    cols_com = [col[0] for col in c.description]
    out['hadith_commentaries_sample'] = [dict(zip(cols_com, r)) for r in c.fetchall()]
    conn.close()

    # 2. classical_scholar_evidence
    conn = sqlite3.connect('file:data/classical_scholar_evidence.db?mode=ro', uri=True)
    c = conn.cursor()
    c.execute("SELECT * FROM classical_scholars")
    cols = [col[0] for col in c.description]
    out['classical_scholars'] = [dict(zip(cols, r)) for r in c.fetchall()]
    c.execute("PRAGMA table_info(classical_hadith_evaluations)")
    out['evaluations_columns'] = [col[1] for col in c.fetchall()]
    c.execute("SELECT * FROM classical_hadith_evaluations LIMIT 3")
    cols_ev = [col[0] for col in c.description]
    out['evaluations_sample'] = [dict(zip(cols_ev, r)) for r in c.fetchall()]
    conn.close()

    # 3. hadith_numbering
    conn = sqlite3.connect('file:data/hadith_numbering.db?mode=ro', uri=True)
    c = conn.cursor()
    c.execute("SELECT * FROM numbering_authorities")
    cols = [col[0] for col in c.description]
    out['numbering_authorities'] = [dict(zip(cols, r)) for r in c.fetchall()]
    c.execute("SELECT * FROM numbering_editions")
    cols = [col[0] for col in c.description]
    out['numbering_editions'] = [dict(zip(cols, r)) for r in c.fetchall()]
    c.execute("SELECT * FROM numbering_schemes")
    cols = [col[0] for col in c.description]
    out['numbering_schemes'] = [dict(zip(cols, r)) for r in c.fetchall()]
    c.execute("SELECT * FROM subsystem_metadata")
    cols = [col[0] for col in c.description]
    out['numbering_subsystem_metadata'] = [dict(zip(cols, r)) for r in c.fetchall()]
    conn.close()

    # 4. hadith_translations
    conn = sqlite3.connect('file:data/hadith_translations.db?mode=ro', uri=True)
    c = conn.cursor()
    c.execute("PRAGMA table_info(hadith_translations)")
    out['hadith_translations_columns'] = [col[1] for col in c.fetchall()]
    c.execute("SELECT * FROM hadith_translations LIMIT 3")
    cols = [col[0] for col in c.description]
    out['hadith_translations_sample'] = [dict(zip(cols, r)) for r in c.fetchall()]
    conn.close()

    # 5. hadith-kg scholars in hadith_grades
    conn = sqlite3.connect('file:data/hadith-kg.db?mode=ro', uri=True)
    c = conn.cursor()
    c.execute("SELECT scholar, COUNT(*) FROM hadith_grades GROUP BY scholar")
    out['hadith_kg_grades_scholars'] = dict(c.fetchall())
    c.execute("SELECT source, COUNT(*) FROM hadith_grades GROUP BY source")
    out['hadith_kg_grades_sources'] = dict(c.fetchall())
    conn.close()

    with open('scratch/provenance_deep_details.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("Saved scratch/provenance_deep_details.json successfully")

inspect_details()
