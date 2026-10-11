import os
import sys
import json
import csv

sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PHASE2_DIR = os.path.join(REPO_ROOT, "validation", "classical_external_grading_research", "phase2")
os.makedirs(PHASE2_DIR, exist_ok=True)

print("=== GENERATING PHASE 2 CLASSICAL SCHOLAR RESEARCH ARTIFACTS ===")

# Matrix Data
matrix_rows = [
    {
        "scholar": "al-Tirmidhī",
        "death_ah": 279,
        "work": "al-Jāmiʿ al-Kabīr (Sunan al-Tirmidhī)",
        "evidence_type": "EXPLICIT_HADITH_GRADE & HADITH_CRITICISM",
        "actual_hadith_level_evidence": "YES (1,918 explicit grades + 808 criticisms)",
        "record_count": 2726,
        "primary_source": "al-Jāmiʿ al-Kabīr, Book 3 taraf_nass",
        "digital_source": "Shamela / OpenITI / Mīzān hadith-kg.db",
        "mapping_level": "LEVEL A — DETERMINISTIC",
        "mapping_status": "DETERMINISTIC (100% row-level join in Book 3)",
        "attribution_status": "VERIFIED (Directly attributed authorial text)",
        "license_status": "GREEN (Public Domain, Author d. 279 AH)",
        "implementation_status": "IMPLEMENT",
        "reason": "Certified and forensically verified baseline in classical_scholar_evidence.db.",
        "notes": "1,918 explicit grades and 808 criticisms strictly separated."
    },
    {
        "scholar": "Abū Dāwūd al-Sijistānī",
        "death_ah": 275,
        "work": "al-Sunan",
        "evidence_type": "HADITH_CRITICISM & ISNAD_DEFECT",
        "actual_hadith_level_evidence": "YES (585 authorial remarks in Book 4 taraf_nass)",
        "record_count": 585,
        "primary_source": "Sunan Abī Dāwūd, Book 4 taraf_nass",
        "digital_source": "Shamela / Mīzān hadith-kg.db",
        "mapping_level": "LEVEL A — DETERMINISTIC",
        "mapping_status": "DETERMINISTIC (Row-level join in Book 4)",
        "attribution_status": "VERIFIED (Authorial remarks: Qawl Abī Dāwūd)",
        "license_status": "GREEN (Public Domain, Author d. 275 AH)",
        "implementation_status": "DEFER_MANUAL_VERIFICATION",
        "reason": "Remarks are predominantly criticism, defect remarks, and transmitter notes; silence cannot be converted to Sahih. Requires dedicated categorization audit before UI ingestion.",
        "notes": "Strong candidate for Phase 3 Hadith Criticism pass."
    },
    {
        "scholar": "al-Nasāʾī",
        "death_ah": 303,
        "work": "al-Sunan al-Ṣughrā (al-Mujtabā)",
        "evidence_type": "HADITH_CRITICISM & VARIANT_PREFERENCE",
        "actual_hadith_level_evidence": "YES (151 authorial remarks in Book 5 taraf_nass)",
        "record_count": 151,
        "primary_source": "Sunan al-Nasāʾī, Book 5 taraf_nass",
        "digital_source": "Shamela / Mīzān hadith-kg.db",
        "mapping_level": "LEVEL A — DETERMINISTIC",
        "mapping_status": "DETERMINISTIC (Row-level join in Book 5)",
        "attribution_status": "VERIFIED (Authorial remarks: Qawl Abī ʿAbd al-Raḥmān)",
        "license_status": "GREEN (Public Domain, Author d. 303 AH)",
        "implementation_status": "DEFER_MANUAL_VERIFICATION",
        "reason": "Exclusively variant preference (Ashbahu bi-al-Sawab, Khata'), defects, and comparisons. Zero modern binary grades.",
        "notes": "Candidate for Phase 3 Hadith Criticism pass."
    },
    {
        "scholar": "Aḥmad ibn Ḥanbal",
        "death_ah": 241,
        "work": "al-ʿIlal wa-Maʿrifat al-Rijāl / Masāʾil",
        "evidence_type": "HADITH_CRITICISM & NARRATOR_JARH",
        "actual_hadith_level_evidence": "YES (~600 hadith-level defect statements in al-ʿIlal)",
        "record_count": 4115,
        "primary_source": "al-ʿIlal (transmission of ʿAbd Allāh, ed. Wasiyyullah Abbas)",
        "digital_source": "Shamela / Waqfeya / OpenITI",
        "mapping_level": "LEVEL D — PROBABLE",
        "mapping_status": "UNMAPPED (Identified only by question number 1–4115)",
        "attribution_status": "VERIFIED (Transmitted by ʿAbd Allāh ibn Aḥmad)",
        "license_status": "GREEN (Public Domain classical text)",
        "implementation_status": "DEFER_SPECIALIZED_MAPPING",
        "reason": "Question numbers in al-ʿIlal are unmapped to standard Sihah Sittah hadith IDs. Requires dedicated takhrij crosswalk project.",
        "notes": "Narrator Jarh wa Ta'dil (1,963 statements) already exposed in Mizan aqwal layer."
    },
    {
        "scholar": "al-Dāraquṭnī",
        "death_ah": 385,
        "work": "al-ʿIlal al-Wāridah fī al-Aḥādīth al-Nabawiyyah",
        "evidence_type": "ILLAL_ANALYSIS & VARIANT_PREFERENCE",
        "actual_hadith_level_evidence": "YES (4,136 detailed variant monographs)",
        "record_count": 4136,
        "primary_source": "al-ʿIlal (ed. Mahfuzur Rahman al-Salafi, 15 vols)",
        "digital_source": "Shamela / OpenITI",
        "mapping_level": "LEVEL D — PROBABLE",
        "mapping_status": "UNMAPPED (Monograph questions unmapped to Mīzān IDs)",
        "attribution_status": "VERIFIED (Reported by al-Barqānī)",
        "license_status": "GREEN (Public Domain classical text)",
        "implementation_status": "DEFER_SPECIALIZED_MAPPING",
        "reason": "Complex multi-branch isnad variant analysis cannot be flattened into scalar hadith grade. Requires dedicated relational variant data model.",
        "notes": "Highest priority for specialized ʿIlal subsystem in future roadmap."
    },
    {
        "scholar": "al-Bukhārī",
        "death_ah": 256,
        "work": "al-Tārīkh al-Kabīr / al-ʿIlal via Tirmidhī",
        "evidence_type": "HADITH_CRITICISM & COLLECTION_METADATA",
        "actual_hadith_level_evidence": "YES (~450 oral statements in Tirmidhī + 67 in Sahih)",
        "record_count": 517,
        "primary_source": "al-Tārīkh al-Kabīr / oral questions quoted in Jāmiʿ al-Tirmidhī",
        "digital_source": "Shamela / Mīzān hadith-kg.db",
        "mapping_level": "LEVEL C — MANUAL VERIFIED",
        "mapping_status": "UNMAPPED (Oral statements in Tirmidhi require extraction)",
        "attribution_status": "VERIFIED (Quoted with explicit attribution)",
        "license_status": "GREEN (Public Domain)",
        "implementation_status": "DEFER_SPECIALIZED_MAPPING",
        "reason": "Collection inclusion in Sahih is collection metadata, not individual grading. Oral rulings inside Tirmidhi require secondary compiler attribution model.",
        "notes": "Narrator evaluations (4,783 statements) already exposed in Mizan aqwal layer."
    },
    {
        "scholar": "Ibn Ḥajar al-ʿAsqalānī",
        "death_ah": 852,
        "work": "Bulūgh al-Marām min Adillat al-Aḥkām",
        "evidence_type": "EXPLICIT_HADITH_GRADE & TAKHRIJ",
        "actual_hadith_level_evidence": "YES (~1,500 concise judgments and takhrij statements)",
        "record_count": 1596,
        "primary_source": "Bulūgh al-Marām",
        "digital_source": "Shamela / OpenITI / Al-Maktaba",
        "mapping_level": "LEVEL B — MULTI-KEY DETERMINISTIC",
        "mapping_status": "UNMAPPED (Bulugh hadith numbers 1–1596 unaligned to Mīzān IDs)",
        "attribution_status": "MULTI-LAYER (Quotes earlier critics in ~70% of cases)",
        "license_status": "GREEN (Public Domain classical text)",
        "implementation_status": "DEFER_SPECIALIZED_MAPPING",
        "reason": "Requires algorithmic takhrij parser to separate Ibn Hajar's own rulings from his quotations of Tirmidhi, Ibn Hibban, Daraqutni, etc., plus crosswalk alignment.",
        "notes": "Prime candidate for post-Sittah secondary takhrij integration."
    },
    {
        "scholar": "ʿAlī ibn al-Madīnī",
        "death_ah": 234,
        "work": "Kitāb al-ʿIlal",
        "evidence_type": "NARRATOR_JARH & ISNAD_DEFECT",
        "actual_hadith_level_evidence": "NO (Predominantly transmitter notices and Madar al-Isnad)",
        "record_count": 0,
        "primary_source": "Kitāb al-ʿIlal (ed. Qal'aji)",
        "digital_source": "Shamela",
        "mapping_level": "LEVEL E — AMBIGUOUS",
        "mapping_status": "UNMAPPED",
        "attribution_status": "VERIFIED (Transmitted fragments)",
        "license_status": "GREEN (Public Domain)",
        "implementation_status": "DO_NOT_IMPLEMENT_NO_DATA",
        "reason": "No discrete machine-actionable hadith-level grading records exist. Evidence is narrator-level and already indexed in Mizan aqwal layer.",
        "notes": "720+ statements present in Mizan aqwal."
    },
    {
        "scholar": "Yaḥyā ibn Maʿīn",
        "death_ah": 233,
        "work": "Tārīkh Ibn Maʿīn (riwāyat al-Dūrī / Ibn Muḥriz)",
        "evidence_type": "NARRATOR_JARH & NARRATOR_TADIL",
        "actual_hadith_level_evidence": "NO (Transmitter evaluation only)",
        "record_count": 0,
        "primary_source": "al-Tārīkh (ed. Ahmad Muhammad Nur Sayf, 4 vols)",
        "digital_source": "Shamela",
        "mapping_level": "LEVEL E — AMBIGUOUS",
        "mapping_status": "UNMAPPED",
        "attribution_status": "VERIFIED (al-Dūrī transmission)",
        "license_status": "GREEN (Public Domain)",
        "implementation_status": "DO_NOT_IMPLEMENT_NO_DATA",
        "reason": "Ibn Ma'in's expertise is predominantly transmitter criticism (Jarh wa Ta'dil). Converting narrator tawthiq to hadith Sahih violates Rule 1.",
        "notes": "3,293 statements present in Mizan aqwal."
    },
    {
        "scholar": "Abū Ḥātim al-Rāzī & Abū Zurʿah al-Rāzī",
        "death_ah": 277,
        "work": "ʿIlal al-Ḥadīth (Ibn Abī Ḥātim)",
        "evidence_type": "ILLAL_ANALYSIS & HADITH_CRITICISM",
        "actual_hadith_level_evidence": "YES (2,840 question entries in ʿIlal Ibn Abī Ḥātim)",
        "record_count": 2840,
        "primary_source": "ʿIlal al-Ḥadīth (ed. Sa'd al-Humayyid, 7 vols)",
        "digital_source": "Shamela / Waqfeya",
        "mapping_level": "LEVEL D — PROBABLE",
        "mapping_status": "UNMAPPED (Numbered entries 1–2840 unmapped to Mīzān)",
        "attribution_status": "VERIFIED (Ibn Abī Ḥātim reporting from his father and Abū Zurʿah)",
        "license_status": "GREEN (Public Domain)",
        "implementation_status": "DEFER_SPECIALIZED_MAPPING",
        "reason": "Requires question-to-hadith crosswalk alignment and attribution separation between Abū Ḥātim and Abū Zurʿah.",
        "notes": "4,100+ narrator statements in Mizan aqwal."
    }
]

# Write CSV Matrix
csv_path = os.path.join(PHASE2_DIR, "16_scholar_expansion_matrix.csv")
root_csv_path = os.path.join(PHASE2_DIR, "scholar_expansion_matrix.csv")

fieldnames = [
    "scholar", "death_ah", "work", "evidence_type", "actual_hadith_level_evidence",
    "record_count", "primary_source", "digital_source", "mapping_level",
    "mapping_status", "attribution_status", "license_status",
    "implementation_status", "reason", "notes"
]

for p in [csv_path, root_csv_path]:
    with open(p, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in matrix_rows:
            writer.writerow(r)

print(f"Wrote {csv_path} and {root_csv_path}.")

# Write Implementation Candidates JSON
impl_candidates = [r for r in matrix_rows if r["implementation_status"] in ("IMPLEMENT", "IMPLEMENT_LIMITED")]
impl_json_path = os.path.join(PHASE2_DIR, "14_implementation_candidates.json")
with open(impl_json_path, "w", encoding="utf-8") as f:
    json.dump(impl_candidates, f, indent=2, ensure_ascii=False)
print(f"Wrote {impl_json_path} ({len(impl_candidates)} candidate).")

# Write Deferred Candidates JSON
deferred_candidates = [r for r in matrix_rows if "DEFER" in r["implementation_status"] or "DO_NOT_IMPLEMENT" in r["implementation_status"]]
deferred_json_path = os.path.join(PHASE2_DIR, "15_deferred_candidates.json")
with open(deferred_json_path, "w", encoding="utf-8") as f:
    json.dump(deferred_candidates, f, indent=2, ensure_ascii=False)
print(f"Wrote {deferred_json_path} ({len(deferred_candidates)} candidates).")

print("Generated structured matrix and candidate JSONs.")
