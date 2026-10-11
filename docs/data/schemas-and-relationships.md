# MĪZĀN AL-ḤADĪTH — SCHEMAS & RELATIONSHIPS

**Document Identifier:** `docs/data/schemas-and-relationships.md`  
**Specification Standard:** SQLite DDL Schema Specifications  

---

## 1. Core Knowledge Graph DDL (`hadith-kg.db`)

### 1.1 `books` Table
```sql
CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    title_ar TEXT,
    author TEXT,
    author_ar TEXT,
    death_year_ah INTEGER,
    hadith_count INTEGER DEFAULT 0
);
```

### 1.2 `hadiths` Table
```sql
CREATE TABLE hadiths (
    id INTEGER PRIMARY KEY,
    book_id INTEGER NOT NULL REFERENCES books(id),
    chapter_id INTEGER,
    matn_ar TEXT NOT NULL,
    matn_normalized TEXT,
    grade_canonical TEXT
);
CREATE INDEX idx_hadiths_book ON hadiths(book_id);
CREATE INDEX idx_hadiths_norm ON hadiths(matn_normalized);
```

### 1.3 `rawis` (Transmitters) Table
```sql
CREATE TABLE rawis (
    id INTEGER PRIMARY KEY,
    name_ar TEXT NOT NULL,
    nasab_ar TEXT,
    rank_ar TEXT,
    death_year_ah INTEGER,
    generation_tier INTEGER,
    canonical_center TEXT
);
CREATE INDEX idx_rawis_name ON rawis(name_ar);
CREATE INDEX idx_rawis_death ON rawis(death_year_ah);
```

### 1.4 `sanads` & `sanad_rawis` Tables
```sql
CREATE TABLE sanads (
    id INTEGER PRIMARY KEY,
    hadith_id INTEGER NOT NULL REFERENCES hadiths(id),
    sanad_text_ar TEXT
);

CREATE TABLE sanad_rawis (
    id INTEGER PRIMARY KEY,
    sanad_id INTEGER NOT NULL REFERENCES sanads(id),
    rawi_id INTEGER NOT NULL REFERENCES rawis(id),
    sequence_order INTEGER NOT NULL
);
CREATE INDEX idx_sr_sanad ON sanad_rawis(sanad_id);
CREATE INDEX idx_sr_rawi ON sanad_rawis(rawi_id);
```

---

## 2. Numbering Concordance DDL (`hadith_numbering.db`)

```sql
CREATE TABLE numbering_editions (
    edition_id INTEGER PRIMARY KEY,
    edition_code TEXT UNIQUE NOT NULL,
    authority_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE hadith_numbers (
    id INTEGER PRIMARY KEY,
    canonical_hadith_id INTEGER NOT NULL,
    edition_id INTEGER NOT NULL REFERENCES numbering_editions(edition_id),
    in_book_number TEXT NOT NULL,
    volume_number INTEGER,
    page_number INTEGER,
    normalized_lookup_key TEXT NOT NULL
);
CREATE INDEX idx_hn_key ON hadith_numbers(normalized_lookup_key);
CREATE INDEX idx_hn_hadith ON hadith_numbers(canonical_hadith_id);
```

---

## 3. Isnād Topology Graph DDL (`isnad_network.db`)

```sql
CREATE TABLE narrator_nodes (
    node_id INTEGER PRIMARY KEY,
    name_ar TEXT NOT NULL,
    name_translit TEXT,
    death_year_ah INTEGER,
    in_degree INTEGER DEFAULT 0,
    out_degree INTEGER DEFAULT 0,
    generation_tier INTEGER,
    canonical_center TEXT
);

CREATE TABLE narrator_edges (
    source_id INTEGER NOT NULL REFERENCES narrator_nodes(node_id),
    target_id INTEGER NOT NULL REFERENCES narrator_nodes(node_id),
    weight INTEGER DEFAULT 1,
    book_mask INTEGER DEFAULT 0,
    PRIMARY KEY (source_id, target_id)
);
CREATE INDEX idx_edges_source ON narrator_edges(source_id);
CREATE INDEX idx_edges_target ON narrator_edges(target_id);
```
