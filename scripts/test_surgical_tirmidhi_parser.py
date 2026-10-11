import sqlite3
import re
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

def parse_tirmidhi_statement(stmt_text):
    """
    Surgically parses an authorial statement from Imam al-Tirmidhi.
    Distinguishes:
    1. EXPLICIT_HADITH_GRADE (Formula applied to the narration itself)
    2. HADITH_CRITICISM (Chain defects, comparisons, non-preserved variants, scholarly commentary)
    """
    clean = stmt_text.strip()
    
    # ---------------------------------------------------------
    # 1. Look for explicit negative grades on the hadith itself
    # ---------------------------------------------------------
    # "هذا حديث منكر" or "حديث ... منكر"
    m_munkar = re.search(r'(هذا حديث|هذا الحديث|حديث\s+\w+)\s+منكر', clean)
    if m_munkar:
        return {
            "evidence_type": "hadith_criticism",
            "canonical_term": "Munkar",
            "verbatim": m_munkar.group(0),
            "category": "Hadith Criticism / Defect"
        }

    # "ليس إسناده بصحيح" or "ليس إسناده بذاك" or "ليس إسناده بالقوي"
    m_laysa = re.search(r'ليس\s+إسناده\s+(?:بـ?|ب)(صحيح|ذاك|القوي|بذلك)', clean)
    if m_laysa:
        matched_phrase = clean[m_laysa.start():m_laysa.start()+40].split('،')[0].split('.')[0].strip()
        term = "Laysa Isnāduhu bi-Ṣaḥīḥ" if "صحيح" in m_laysa.group(1) else "Laysa Isnāduhu bi-Dhāk"
        return {
            "evidence_type": "hadith_criticism",
            "canonical_term": term,
            "verbatim": matched_phrase,
            "category": "Hadith Criticism / Chain Defect"
        }

    # "غير محفوظ"
    if "غير محفوظ" in clean:
        m_ghayr = re.search(r'(هذا حديث\s+غير محفوظ|حديث\s+غير محفوظ)', clean)
        vb = m_ghayr.group(0) if m_ghayr else "هذا حديث غير محفوظ"
        return {
            "evidence_type": "hadith_criticism",
            "canonical_term": "Ghayr Maḥfūẓ",
            "verbatim": vb,
            "category": "Hadith Criticism / Anomaly"
        }

    # ---------------------------------------------------------
    # 2. Look for standard positive/descriptive explicit grades
    # Formulas:
    # "هذا حديث حسن صحيح غريب"
    # "هذا حديث حسن صحيح"
    # "هذا حديث حسن غريب"
    # "هذا حديث صحيح غريب"
    # "هذا حديث حسن"
    # "هذا حديث صحيح"
    # "هذا حديث غريب"
    # "هذا حديث ضعيف" (applied to hadith)
    # Also: "حديث فلان حسن صحيح", etc.
    # ---------------------------------------------------------
    
    # Pattern matching grading formulas strictly:
    # Anchor to 'هذا حديث' or 'حديث فلان' or 'وكلا الحديثين'
    grade_regex = re.compile(
        r'(?:قال أبو عيسى\s+)?((?:هذا حديث|هذا الحديث|حديث\s+[^\n،\.]+?|وكلا الحديثين(?:[^\n،\.]+?)?)\s+'
        r'(حسنٌ?\s+صحيحٌ?\s+غريبٌ?|حسنٌ?\s+صحيحٌ?|حسنٌ?\s+غريبٌ?|صحيحٌ?\s+غريبٌ?|حسنٌ?|صحيحٌ?|غريبٌ?|ضعيفٌ?))'
        r'(?:(?=\s+(?:لا نعرفه|من هذا|وقد روي|وفي الباب|سمعت|حدثنا|والعمل|وروي|\.|\n|،|$)))'
    )
    
    m_grade = grade_regex.search(clean)
    if m_grade:
        full_match = m_grade.group(1).strip()
        grade_part = m_grade.group(2).strip()
        
        # Normalize canonical term
        if "حسن" in grade_part and "صحيح" in grade_part and "غريب" in grade_part:
            canonical_term = "Ḥasan Ṣaḥīḥ Gharīb"
        elif "حسن" in grade_part and "صحيح" in grade_part:
            canonical_term = "Ḥasan Ṣaḥīḥ"
        elif "حسن" in grade_part and "غريب" in grade_part:
            canonical_term = "Ḥasan Gharīb"
        elif "صحيح" in grade_part and "غريب" in grade_part:
            canonical_term = "Ṣaḥīḥ Gharīb"
        elif "صحيح" in grade_part:
            canonical_term = "Ṣaḥīḥ"
        elif "حسن" in grade_part:
            canonical_term = "Ḥasan"
        elif "غريب" in grade_part:
            canonical_term = "Gharīb"
        elif "ضعيف" in grade_part:
            canonical_term = "Ḍaʿīf"
        else:
            canonical_term = "Qawl Abī ʿĪsā (Scholarly Remark)"
            
        return {
            "evidence_type": "explicit_hadith_grade",
            "canonical_term": canonical_term,
            "verbatim": full_match,
            "category": "Explicit Hadith Grade"
        }

    # "أصح شيء في هذا الباب"
    if "أصح شيء في هذا الباب" in clean or "أصح شيء" in clean:
        m_asah = re.search(r'(هذا الحديث\s+أصح شيء[^\n،\.]+?|أصح شيء في هذا الباب[^\n،\.]+?)', clean)
        vb = m_asah.group(1).strip() if m_asah else "هذا الحديث أصح شيء في هذا الباب"
        return {
            "evidence_type": "hadith_criticism",
            "canonical_term": "Aṣaḥḥu Shayʾin fī al-Bāb",
            "verbatim": vb,
            "category": "Hadith Criticism / Comparative Tarjīḥ"
        }

    # "والصحيح ما روي عن..." (Chain preference)
    if "والصحيح ما رو" in clean:
        m_sah = re.search(r'(والصحيح ما رو[^\n،\.]+)', clean)
        vb = m_sah.group(1).strip() if m_sah else "والصحيح ما روي"
        return {
            "evidence_type": "hadith_criticism",
            "canonical_term": "Tarjīḥ al-Wajh al-Ṣaḥīḥ",
            "verbatim": vb,
            "category": "Hadith Criticism / Variant Preference"
        }

    # ---------------------------------------------------------
    # 3. Everything else is classical hadith criticism / commentary
    # ---------------------------------------------------------
    # First sentence of Qawl Abi Isa
    first_phrase = clean.split('.')[0].split('،')[0][:120].strip()
    return {
        "evidence_type": "hadith_criticism",
        "canonical_term": "Qawl Abī ʿĪsā (Scholarly Remark)",
        "verbatim": first_phrase,
        "category": "Hadith Criticism / Remarks"
    }

def test_on_all():
    conn = sqlite3.connect("file:data/hadith-kg.db?mode=ro", uri=True)
    rows = conn.execute("""
        SELECT id, no_inbook, taraf_nass
        FROM hadiths
        WHERE book_id = 3
        ORDER BY no_inbook
    """).fetchall()
    
    results = []
    grade_count = 0
    crit_count = 0
    term_counts = {}
    
    for hid, no, taraf in rows:
        if not taraf:
            continue
        idx = taraf.find("قال أبو عيسى")
        if idx == -1:
            continue
            
        stmt = taraf[idx:].strip()
        parsed = parse_tirmidhi_statement(stmt)
        results.append((hid, no, parsed, stmt))
        
        ev = parsed["evidence_type"]
        ct = parsed["canonical_term"]
        if ev == "explicit_hadith_grade":
            grade_count += 1
        else:
            crit_count += 1
        term_counts[ct] = term_counts.get(ct, 0) + 1
        
    conn.close()
    
    print(f"Total Tirmidhi Authorial Statements Parsed: {len(results)}")
    print(f"Explicit Hadith Grades: {grade_count}")
    print(f"Classical Hadith Criticism: {crit_count}")
    print(f"Sum: {grade_count + crit_count}")
    print("\nBreakdown of Canonical Terms:")
    for ct, cnt in sorted(term_counts.items(), key=lambda x: -x[1]):
        print(f"  {ct}: {cnt}")

if __name__ == "__main__":
    test_on_all()
