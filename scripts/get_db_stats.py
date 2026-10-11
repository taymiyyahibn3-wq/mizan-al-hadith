import sqlite3
import os
import json

dbs = {
    'hadith-kg.db': 'data/hadith-kg.db',
    'hadith_numbering.db': 'data/hadith_numbering.db',
    'hadith_commentaries.db': 'data/hadith_commentaries.db',
    'hadith_translations.db': 'data/hadith_translations.db',
    'isnad_network.db': 'data/isnad_network.db',
    'citation_enrichment.db': 'data/citation_enrichment.db',
    'classical_scholar_evidence.db': 'data/classical_scholar_evidence.db',
    'ask_mizan.db': 'data/ask_mizan.db'
}

stats = {}
for name, rel_path in dbs.items():
    if not os.path.exists(rel_path):
        continue
    try:
        conn = sqlite3.connect(f'file:{rel_path}?mode=ro', uri=True)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = [r[0] for r in cursor.fetchall()]
        table_counts = {}
        for t in tables:
            try:
                cursor.execute(f'SELECT COUNT(*) FROM "{t}"')
                table_counts[t] = cursor.fetchone()[0]
            except Exception as e:
                table_counts[t] = str(e)
        stats[name] = {
            'file_size_bytes': os.path.getsize(rel_path),
            'tables': table_counts
        }
        conn.close()
    except Exception as e:
        stats[name] = {'error': str(e)}

with open('db_stats.json', 'w', encoding='utf-8') as f:
    json.dump(stats, f, indent=2, ensure_ascii=False)
print("Saved db_stats.json successfully")
