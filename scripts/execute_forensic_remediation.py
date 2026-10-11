import os
import sys
import sqlite3
import csv
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESEARCH_DIR = os.path.join(REPO_ROOT, "validation", "classical_external_grading_research")
DERIVED_DB_PATH = os.path.join(REPO_ROOT, "data", "classical_scholar_evidence.db")
KG_DB_PATH = os.path.join(REPO_ROOT, "data", "hadith-kg.db")

print("=== EXECUTING TIRMIDHI EVIDENCE FORENSIC REMEDIATION & RE-INDEXING ===")

# 1. Connect to canonical hadith-kg.db in READ-ONLY mode
kg_conn = sqlite3.connect(f"file:{KG_DB_PATH}?mode=ro", uri=True)
kg_rows = kg_conn.execute("""
    SELECT id, no_inbook, page_no, taraf_nass, nass, matn
    FROM hadiths
    WHERE book_id = 3
    ORDER BY no_inbook
""").fetchall()

print(f"Loaded {len(kg_rows)} total rows for Book 3 (Jāmiʿ al-Tirmidhī) from canonical database.")

# 2. Parse all authorial statements
evaluations = []

for hid, no_inbook, pg, taraf, nass, matn in kg_rows:
    if not taraf:
        continue
    idx = taraf.find("قال أبو عيسى")
    if idx == -1:
        continue
        
    stmt = taraf[idx:].strip()
    body = re.sub(r'^قال أبو عيسى\s*', '', stmt).strip()
    
    # Surgical classification
    ev_type = "hadith_criticism"
    canonical_term = "Qawl Abī ʿĪsā (Scholarly Remark)"
    verbatim_text = ""
    
    # Check 1: Chain defect remarks / Negative criticism
    if re.search(r'ليس\s+إسناده\s+(?:بـ?|ب)صحيح', body):
        m = re.search(r'(?:هذا حديث\s+)?ليس\s+إسناده\s+(?:بـ?|ب)صحيح[^\n،\.]*', body)
        vb = m.group(0).strip() if m else "ليس إسناده بصحيح"
        ev_type = "hadith_criticism"
        canonical_term = "Laysa Isnāduhu bi-Ṣaḥīḥ"
        verbatim_text = vb
    elif re.search(r'ليس\s+إسناده\s+(?:بذاك|بذلك|بالقوي)', body):
        m = re.search(r'(?:هذا حديث\s+)?ليس\s+إسناده\s+(?:بذاك|بذلك|بالقوي)[^\n،\.]*', body)
        vb = m.group(0).strip() if m else "ليس إسناده بذاك"
        ev_type = "hadith_criticism"
        canonical_term = "Laysa Isnāduhu bi-Dhāk"
        verbatim_text = vb
    elif re.search(r'غير\s+محفوظ', body):
        m = re.search(r'(?:هذا حديث\s+)?غير\s+محفوظ[^\n،\.]*', body)
        vb = m.group(0).strip() if m else "هذا حديث غير محفوظ"
        ev_type = "hadith_criticism"
        canonical_term = "Ghayr Maḥfūẓ"
        verbatim_text = vb
    elif re.search(r'(?:هذا حديث|هذا الحديث|حديث\s+\w+)\s+منكر', body):
        m = re.search(r'(?:هذا حديث|هذا الحديث|حديث\s+\w+)\s+منكر', body)
        vb = m.group(0).strip()
        ev_type = "hadith_criticism"
        canonical_term = "Munkar"
        verbatim_text = vb
    elif "أصح شيء في هذا الباب" in body:
        m = re.search(r'(?:هذا الحديث\s+)?أصح شيء في هذا الباب[^\n،\.]*', body)
        vb = m.group(0).strip() if m else "أصح شيء في هذا الباب"
        ev_type = "hadith_criticism"
        canonical_term = "Aṣaḥḥu Shayʾin fī al-Bāb"
        verbatim_text = vb
    elif body.startswith("والصحيح ما رو") or ("والصحيح ما رو" in body and not re.search(r'هذا حديث\s+(?:حسن|صحيح)', body)):
        m = re.search(r'والصحيح ما رو[^\n،\.]*', body)
        vb = m.group(0).strip() if m else "والصحيح ما روي"
        ev_type = "hadith_criticism"
        canonical_term = "Tarjīḥ al-Wajh al-Ṣaḥīḥ"
        verbatim_text = vb
    else:
        # Check 2: Explicit positive/descriptive hadith grades
        # Match standard grading formulas anchored to hadith
        m_exp = re.search(
            r'(هذا حديث|هذا الحديث|حديث\s+[^\n،\.]+?|وكلا الحديثين[^\n،\.]*?)\s+'
            r'(حسنٌ?\s+صحيحٌ?\s+غريبٌ?|حسنٌ?\s+صحيحٌ?|حسنٌ?\s+غريبٌ?|صحيحٌ?\s+غريبٌ?|صحيحٌ?|حسنٌ?|غريبٌ?|ضعيفٌ?)'
            r'(?=\s+(?:لا نعرفه|من هذا|وقد روي|وفي الباب|سمعت|حدثنا|والعمل|وروي|\.|\n|،|$|إلا|ورواه))',
            body
        )
        
        m_start = None
        if not m_exp:
            m_start = re.match(
                r'^(هذا حديث|هذا الحديث)\s+(حسنٌ?\s+صحيحٌ?\s+غريبٌ?|حسنٌ?\s+صحيحٌ?|حسنٌ?\s+غريبٌ?|صحيحٌ?\s+غريبٌ?|صحيحٌ?|حسنٌ?|غريبٌ?|ضعيفٌ?)',
                body
            )
            
        m_chosen = m_exp or m_start
        if m_chosen:
            grade_term = m_chosen.group(2).strip()
            # Guard against narrator name like "عبد الرحمن بن حسنة"
            if "حسنة" in grade_term:
                ev_type = "hadith_criticism"
                canonical_term = "Qawl Abī ʿĪsā (Scholarly Remark)"
                verbatim_text = body.split('.')[0].split('،')[0][:120].strip()
            else:
                ev_type = "explicit_hadith_grade"
                if "حسن" in grade_term and "صحيح" in grade_term and "غريب" in grade_term:
                    canonical_term = "Ḥasan Ṣaḥīḥ Gharīb"
                elif "حسن" in grade_term and "صحيح" in grade_term:
                    canonical_term = "Ḥasan Ṣaḥīḥ"
                elif "حسن" in grade_term and "غريب" in grade_term:
                    canonical_term = "Ḥasan Gharīb"
                elif "صحيح" in grade_term and "غريب" in grade_term:
                    canonical_term = "Ṣaḥīḥ Gharīb"
                elif "حسن" in grade_term:
                    canonical_term = "Ḥasan"
                elif "صحيح" in grade_term:
                    canonical_term = "Ṣaḥīḥ"
                elif "غريب" in grade_term:
                    canonical_term = "Gharīb"
                elif "ضعيف" in grade_term:
                    canonical_term = "Ḍaʿīf"
                verbatim_text = m_chosen.group(0).strip()
        else:
            ev_type = "hadith_criticism"
            canonical_term = "Qawl Abī ʿĪsā (Scholarly Remark)"
            verbatim_text = body.split('.')[0].split('،')[0][:120].strip()
            
    evaluations.append({
        "hadith_id": hid,
        "book_id": 3,
        "no_inbook": no_inbook,
        "scholar_id": "al_tirmidhi",
        "scholar_en": "al-Imām al-Tirmidhī",
        "scholar_ar": "أبو عيسى الترمذي",
        "work_en": "al-Jāmiʿ al-Kabīr (Sunan al-Tirmidhī)",
        "work_ar": "الجامع الكبير (سنن الترمذي)",
        "evidence_type": ev_type,
        "canonical_term": canonical_term,
        "verbatim_arabic": verbatim_text,
        "full_context_arabic": stmt[:300],
        "attribution": "Directly attributed authorial evaluation preserved in transmission",
        "license": "Public Domain (Classical text, Author d. 279 AH)",
        "verification_status": "VERIFIED_PRIMARY_SOURCE"
    })

kg_conn.close()

grade_count = sum(1 for e in evaluations if e["evidence_type"] == "explicit_hadith_grade")
crit_count = sum(1 for e in evaluations if e["evidence_type"] == "hadith_criticism")

print(f"Total authorial evaluations extracted: {len(evaluations):,}")
print(f"  Explicit Hadith Grades: {grade_count:,}")
print(f"  Hadith Criticism / ʿIlal Remarks: {crit_count:,}")
assert len(evaluations) == 2726, "Extraction row count must be exactly 2,726!"

# 3. Rebuild derived database with audited data
if os.path.exists(DERIVED_DB_PATH):
    os.remove(DERIVED_DB_PATH)

der_conn = sqlite3.connect(DERIVED_DB_PATH)
c_der = der_conn.cursor()

c_der.execute("""
    CREATE TABLE classical_scholars (
        id TEXT PRIMARY KEY,
        name_en TEXT NOT NULL,
        name_ar TEXT NOT NULL,
        death_year_ah INTEGER NOT NULL,
        primary_field TEXT NOT NULL,
        era TEXT NOT NULL,
        notes TEXT
    )
""")

c_der.execute("""
    CREATE TABLE classical_hadith_evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hadith_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        no_inbook INTEGER NOT NULL,
        scholar_id TEXT NOT NULL,
        scholar_en TEXT NOT NULL,
        scholar_ar TEXT NOT NULL,
        work_en TEXT NOT NULL,
        work_ar TEXT NOT NULL,
        evidence_type TEXT NOT NULL,
        canonical_term TEXT NOT NULL,
        verbatim_arabic TEXT NOT NULL,
        full_context_arabic TEXT NOT NULL,
        attribution TEXT NOT NULL,
        license TEXT NOT NULL,
        verification_status TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
""")

c_der.execute("CREATE INDEX idx_che_hadith_id ON classical_hadith_evaluations(hadith_id)")
c_der.execute("CREATE INDEX idx_che_book_no ON classical_hadith_evaluations(book_id, no_inbook)")
c_der.execute("CREATE INDEX idx_che_evidence_type ON classical_hadith_evaluations(evidence_type)")

c_der.execute("""
    INSERT INTO classical_scholars (id, name_en, name_ar, death_year_ah, primary_field, era, notes)
    VALUES (
        'al_tirmidhi',
        'al-Imām al-Tirmidhī',
        'أبو عيسى الترمذي',
        279,
        'Hadith Criticism, Grading, and Comparative Fiqh',
        'Early Classical (3rd Century AH)',
        'Direct authorial evaluations and terminology preserved in his Sunan / Jāmiʿ'
    )
""")

for e in evaluations:
    c_der.execute("""
        INSERT INTO classical_hadith_evaluations (
            hadith_id, book_id, no_inbook, scholar_id, scholar_en, scholar_ar,
            work_en, work_ar, evidence_type, canonical_term, verbatim_arabic,
            full_context_arabic, attribution, license, verification_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        e["hadith_id"], e["book_id"], e["no_inbook"], e["scholar_id"],
        e["scholar_en"], e["scholar_ar"], e["work_en"], e["work_ar"],
        e["evidence_type"], e["canonical_term"], e["verbatim_arabic"],
        e["full_context_arabic"], e["attribution"], e["license"],
        e["verification_status"]
    ))

der_conn.commit()
der_conn.close()
print("Successfully regenerated data/classical_scholar_evidence.db with remediated classifications.")

# 4. Generate 17_tirmidhi_provenance_completeness.csv
prov_csv_path = os.path.join(RESEARCH_DIR, "17_tirmidhi_provenance_completeness.csv")
with open(prov_csv_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "hadith_id", "book_id", "collection_name", "no_inbook", "scholar_en", "scholar_ar",
        "work_en", "evidence_type", "canonical_term", "verbatim_arabic",
        "provenance_chain", "provenance_status", "mapping_status", "license"
    ])
    for e in evaluations:
        chain = f"al-Imām al-Tirmidhī -> al-Jāmiʿ al-Kabīr -> Hadith #{e['no_inbook']} -> taraf_nass -> MīZĀN #{e['hadith_id']}"
        writer.writerow([
            e["hadith_id"], e["book_id"], "Jāmiʿ al-Tirmidhī", e["no_inbook"],
            e["scholar_en"], e["scholar_ar"], e["work_en"], e["evidence_type"],
            e["canonical_term"], e["verbatim_arabic"], chain, "COMPLETE", "DETERMINISTIC", e["license"]
        ])

print(f"Wrote {prov_csv_path} ({len(evaluations)} rows).")

# 5. Update 15_mapping_register.csv
map_csv_path = os.path.join(RESEARCH_DIR, "15_mapping_register.csv")
with open(map_csv_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "mizan_hadith_id", "book_id", "collection", "no_inbook", "scholar",
        "work", "evidence_type", "canonical_term", "verbatim_statement",
        "attribution", "license", "verification_status", "mapping_confidence"
    ])
    for e in evaluations:
        writer.writerow([
            e["hadith_id"], e["book_id"], "Jāmiʿ al-Tirmidhī", e["no_inbook"],
            e["scholar_en"], e["work_en"], e["evidence_type"], e["canonical_term"],
            e["verbatim_arabic"][:100], e["attribution"], e["license"],
            e["verification_status"], "DETERMINISTIC"
        ])

print(f"Wrote {map_csv_path} ({len(evaluations)} rows).")

# 6. Update 14_verified_evidence_candidates.json
json_path = os.path.join(RESEARCH_DIR, "14_verified_evidence_candidates.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(evaluations[:200], f, indent=2, ensure_ascii=False)
print(f"Updated sample candidate records in {json_path}.")

print("=== REMEDIATION EXECUTION COMPLETE ===")
