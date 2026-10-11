import sys, sqlite3
sys.stdout.reconfigure(encoding='utf-8')

def search_rawis_tokenized(query_str: str, kg_db: sqlite3.Connection, ee_db: sqlite3.Connection):
    # Common transliteration mappings
    q = query_str.lower()
    # Normalize common transliteration variants
    q = q.replace("abdur ", "abd al-").replace("abdurrahman", "abd al-rahman")
    q = q.replace("musalli", "musli").replace("mussali", "musli")
    
    # 1. Search ee_db narrator_names with individual key tokens
    tokens = [t.strip("-'") for t in q.split() if len(t) > 2 and t not in ("the", "bin", "ibn", "al")]
    print("Tokens:", tokens)
    
    # 2. Check if Arabic equivalent can be searched directly in rawis
    ar_q = query_str
    # Convert obvious transliterations
    ar_name = ""
    if "abdur rahman" in q or "abd al-rahman" in q:
        ar_name = "عبد الرحمن"
    if "musli" in q or "musalli" in q:
        ar_nisba = "المسلي"
    else:
        ar_nisba = ""
    
    print(f"Arabic guess: {ar_name} {ar_nisba}")
    if ar_name and ar_nisba:
        rows = kg_db.execute("SELECT id, name, nickname FROM rawis WHERE nickname LIKE ? OR (name LIKE ? AND nickname LIKE ?)",
                            (f"%{ar_name}%{ar_nisba}%", f"%{ar_name}%", f"%{ar_nisba}%")).fetchall()
        print("Direct rawis match:", rows)

kg_db = sqlite3.connect('data/hadith-kg.db')
ee_db = sqlite3.connect('data/english_enrichment.db')
search_rawis_tokenized("Abdur Rahman al-Musalli", kg_db, ee_db)
kg_db.close()
ee_db.close()
