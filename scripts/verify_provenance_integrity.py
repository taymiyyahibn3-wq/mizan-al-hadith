import os
import sqlite3
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

def test_databases_and_tables():
    print("--- 1. Testing Local Databases & Tables ---")
    db_checks = [
        ("data/hadith-kg.db", ["books", "hadiths", "sanads", "rawis", "sanad_rawis", "hadith_grades", "hadith_pro_hadiths", "meaning_groups", "tarafs"]),
        ("data/hadith_numbering.db", ["numbering_editions", "numbering_authorities", "hadith_numbers", "numbering_provenance"]),
        ("data/hadith_commentaries.db", ["commentary_sources", "hadith_commentaries", "commentary_hadith_links"]),
        ("data/hadith_translations.db", ["hadith_translations"]),
        ("data/citation_enrichment.db", ["zubair_grade_references_v3"]),
        ("data/classical_scholar_evidence.db", ["classical_scholars", "classical_hadith_evaluations"]),
        ("data/english_enrichment.db", ["narrator_names", "narrator_name_variants", "narrator_grades", "narrator_sources"]),
        ("data/isnad_network.db", ["narrator_nodes", "narrator_edges", "network_meta"]),
        ("data/derived_semantic_index.db", ["semantic_vectors", "index_metadata"]),
        ("data/derived_embeddinggemma2_768d.db", ["metadata", "group_embedding"]),
        ("data/ask_mizan.db", ["conversations", "messages", "citations", "feedback"]),
        ("data/hadith-search-index.db", ["hadith_fts"]),
        ("data/english_translation_fts.db", ["english_fts", "english_translations", "coverage_summary"])
    ]
    
    passed = 0
    total = len(db_checks)
    for db_path, tables in db_checks:
        if not os.path.exists(db_path):
            print(f"FAIL: Database missing: {db_path}")
            continue
        try:
            conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = set(r[0] for r in c.fetchall())
            conn.close()
            
            missing = [t for t in tables if t not in existing_tables]
            if missing:
                print(f"FAIL: {db_path} missing tables: {missing}. Existing tables: {existing_tables}")
            else:
                print(f"PASS: {db_path} verified with {len(tables)} target tables.")
                passed += 1
        except Exception as e:
            print(f"FAIL: Error reading {db_path}: {e}")
            
    print(f"Result: {passed}/{total} databases passed.\n")
    return passed == total

def test_urls():
    print("--- 2. Testing Upstream URLs in Documentation ---")
    url_pattern = re.compile(r'https?://[^\s\)\]\>]+')
    doc_files = [
        "docs/data/dataset-inventory.md",
        "docs/data/provenance-and-attribution.md",
        "docs/data/external-services.md",
        "docs/data/licensing-and-redistribution.md",
        "README.md",
        "docs/index.html"
    ]
    
    all_urls = set()
    for doc in doc_files:
        if os.path.exists(doc):
            with open(doc, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = url_pattern.findall(content)
                for u in matches:
                    all_urls.add(u.rstrip('.,;`"\''))
                    
    print(f"Extracted {len(all_urls)} unique external URLs across documentation.")
    # Check expected core URLs
    expected_urls = [
        "https://huggingface.co/datasets/emadjumaah/hadith-kg",
        "https://github.com/emadjumaah/hadith",
        "https://github.com/unkn4wn/hadith-pro",
        "https://github.com/r3genesi5/Itqan",
        "https://doi.org/10.5281/zenodo.19453612",
        "https://github.com/mhashim6/Open-Hadith-Data",
        "https://shamela.ws/book/8302",
        "https://shamela.ws/book/10578",
        "https://sunnah.com",
        "https://huggingface.co/google/embeddinggemma-2"
    ]
    missing_urls = [u for u in expected_urls if u not in all_urls]
    if missing_urls:
        print(f"FAIL: Missing expected URLs: {missing_urls}")
        return False
    else:
        print("PASS: All core upstream URLs are present and documented.")
        return True

def main():
    ok1 = test_databases_and_tables()
    ok2 = test_urls()
    if ok1 and ok2:
        print("ALL PROVENANCE INTEGRITY VERIFICATIONS PASSED!")
        sys.exit(0)
    else:
        print("SOME VERIFICATIONS FAILED!")
        sys.exit(1)

if __name__ == '__main__':
    main()
