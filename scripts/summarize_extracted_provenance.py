import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def main():
    with open('scratch/provenance_deep_details.json', 'r', encoding='utf-8') as f:
        d = json.load(f)

    print('=== 1. COMMENTARY SOURCES in data/hadith_commentaries.db ===')
    for cs in d['commentary_sources']:
        print(f"Slug: {cs.get('slug')}")
        print(f"  Name: {cs.get('name_en')} ({cs.get('name_ar')})")
        print(f"  Author: {cs.get('author_en')} (d. {cs.get('author_death_year')} AH)")
        print(f"  Target Collection: {cs.get('collection_name_en')}")
        print(f"  Edition/Publisher: {cs.get('edition')} / {cs.get('publisher')}")
        print(f"  Source URL: {cs.get('source_url')}")
        print(f"  License: {cs.get('license')} | Redistribution: {cs.get('redistribution_allowed')}")
        print(f"  Notes: {cs.get('provenance_notes')}\n")

    print('=== 2. CLASSICAL SCHOLARS in data/classical_scholar_evidence.db ===')
    for s in d['classical_scholars']:
        print(f"Scholar ID: {s.get('id')} - {s.get('name_en')} ({s.get('name_ar')}) d. {s.get('death_year_ah')} AH")
        print(f"  Field: {s.get('primary_field')} | Era: {s.get('era')} | Notes: {s.get('notes')}")

    print('\n=== 3. NUMBERING AUTHORITIES in data/hadith_numbering.db ===')
    for a in d['numbering_authorities']:
        print(f"Authority ID {a.get('id')} [{a.get('slug')}]: {a.get('name_en')} ({a.get('name_ar')}) | Type: {a.get('authority_type')}")

    print('\n=== 4. NUMBERING EDITIONS (All 18) in data/hadith_numbering.db ===')
    for e in d['numbering_editions']:
        print(f"- Edition {e.get('id')}: '{e.get('title_en')}' (Book {e.get('book_id')}, Auth {e.get('authority_id')}, Pub: {e.get('publisher')}, Style: {e.get('numbering_style')})")

    print('\n=== 5. HADITH-KG GRADES SCHOLARS & COUNTS in data/hadith-kg.db ===')
    for k, v in d['hadith_kg_grades_scholars'].items():
        print(f"  {k}: {v:,} grades")

    print('\n=== 6. HADITH-KG GRADES SOURCE COLUMN ===')
    for k, v in d['hadith_kg_grades_sources'].items():
        print(f"  Source '{k}': {v:,} rows")

    print('\n=== 7. TRANSLATION DETAILS ===')
    print("Columns in hadith_translations.db:")
    print(d['hadith_translations_columns'])
    print("Sample translation record:")
    print(json.dumps(d['hadith_translations_sample'][0] if d['hadith_translations_sample'] else {}, indent=2))

if __name__ == '__main__':
    main()
