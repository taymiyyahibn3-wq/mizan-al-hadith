# DĀRAQUṬNĪ RELATIONAL ARCHITECTURE & ʿILAL DATA MODEL
## Structural Design for *al-ʿIlal al-Wāridah fī al-Aḥādīth al-Nabawiyyah* (4,136 Monographs)

---

### 1. Executive Summary & Non-Flattening Mandate
Imām al-Dāraquṭnī's masterpiece *al-ʿIlal al-Wāridah* (dictated to Abū Bakr al-Barqānī, ed. Dr. Maḥfūẓ al-Salafī, 15 vols.) is the foremost encyclopedia of transmission defects in Islamic scholarship.

**The Golden Principle (Part 4):**
> **DO NOT flatten al-Dāraquṭnī's ʿIlal into `hadith_id -> grade`.**  
> Flattening complex comparative transmission analyses into binary labels (*Ṣaḥīḥ* / *Ḍaʿīf*) destroys scholarly fidelity and violates the fundamental premise of classical *ʿIlal* methodology.

al-Dāraquṭnī does not stamp a hadith with a modern scalar grade. Rather, he decomposes the hadith into its competing transmission branches, diagnoses the point of divergence, isolates the narrator responsible for the error, and pronounces which variant is preserved (*al-Maḥfūẓ*) versus erroneous (*al-Khaṭaʾ*).

---

### 2. The Core ʿIlal Lifecycle Model
Every inquiry in *al-ʿIlal al-Wāridah* follows a rigorous forensic trajectory:

```
[ INQUIRY / QUESTION ]
(e.g., وسئل عن حديث عائشة في كذا وكذا)
         │
         ▼
[ COMPETING TRANSMISSION ROUTES (Wujūh al-Ikhtilāf) ]
   ├── Route A: Marfūʿ (Connected to Prophet) via Narrator X
   ├── Route B: Mawqūf (Halting at Companion) via Narrator Y
   └── Route C: Mursal (Discontinuous) via Narrator Z
         │
         ▼
[ DIVERGENCE & DEFECT IDENTIFICATION (al-ʿIllah / al-Wahm) ]
(e.g., والوهم فيه من فلان بن فلان حيث رفعه)
         │
         ▼
[ SCHOLARLY TARJĪḤ / PREFERRED ROUTE (al-Qawl al-Rājih) ]
(e.g., والصحيح هو الموقوف عن عائشة)
         │
         ▼
[ SOURCE CITATION & MANUSCRIPT ANCHOR ]
(Volume, Page, Question Number in Dār Ṭaybah edition)
```

---

### 3. Dedicated Relational Schema (DDL)

To capture this scholarship without flattening, Mīzān defines a dedicated multi-table relational schema:

```sql
-- 1. Main Inquiry Entry
CREATE TABLE daraqutni_inquiries (
    inquiry_id INTEGER PRIMARY KEY,           -- 1 to 4136
    companion_musnad TEXT NOT NULL,           -- e.g., 'مسند أبي هريرة', 'مسند عائشة'
    question_text_ar TEXT NOT NULL,           -- Verbatim inquiry: 'وسئل عن حديث...'
    topic_summary_en TEXT,                    -- English topic description
    volume_no INTEGER NOT NULL,               -- Volume in Dār Ṭaybah edition
    page_no INTEGER NOT NULL,                 -- Page number
    mizan_primary_hadith_id INTEGER,          -- FK to hadiths.id (Level C/B verified)
    mapping_status TEXT NOT NULL              -- 'UNMAPPED', 'PROBABLE', 'VERIFIED'
);

-- 2. Competing Transmission Routes
CREATE TABLE daraqutni_variant_routes (
    route_id INTEGER PRIMARY KEY AUTOINCREMENT,
    inquiry_id INTEGER NOT NULL REFERENCES daraqutni_inquiries(inquiry_id),
    route_label TEXT NOT NULL,                -- e.g., 'Route A', 'Route B'
    narrators_chain_ar TEXT NOT NULL,         -- e.g., 'مالك عن نافع عن ابن عمر'
    transmission_mode TEXT NOT NULL,          -- 'Marfu', 'Mawquf', 'Mursal', 'Munqati'
    key_transmitter TEXT NOT NULL,            -- Narrator where divergence occurs
    is_preferred INTEGER NOT NULL DEFAULT 0   -- 1 = Mahfūz / Rājih, 0 = Marjūh / Wahm
);

-- 3. Defect & Comparative Diagnosis
CREATE TABLE daraqutni_defects (
    defect_id INTEGER PRIMARY KEY AUTOINCREMENT,
    inquiry_id INTEGER NOT NULL REFERENCES daraqutni_inquiries(inquiry_id),
    defect_category TEXT NOT NULL,            -- 'Waqf_vs_Raf', 'Irsal_vs_Wasl', 'Idtirab', 'Tadlis'
    erring_narrator_ar TEXT,                  -- The transmitter who committed the error
    defect_explanation_ar TEXT NOT NULL       -- Verbatim explanation from al-Dāraquṭnī
);

-- 4. Final Scholarly Tarjīḥ (Verdict)
CREATE TABLE daraqutni_tarjih (
    tarjih_id INTEGER PRIMARY KEY AUTOINCREMENT,
    inquiry_id INTEGER NOT NULL REFERENCES daraqutni_inquiries(inquiry_id),
    verbatim_tarjih_ar TEXT NOT NULL,         -- e.g., 'والصحيح هو الموقوف'
    canonical_classification TEXT NOT NULL,   -- 'MAHFUZ_MAWQUF', 'MAHFUZ_MARFU', 'MUDTARIB'
    confidence_level TEXT NOT NULL            -- 'DEFINITIVE', 'PROBABLE', 'EQUIVOCAL'
);
```

---

### 4. Implementation Decision Gate
- **Status:** `DEFER_SPECIALIZED_MAPPING`.
- **Reasoning:**
  1. The 4,136 inquiries currently lack an open, machine-readable crosswalk to Sihah Sittah IDs.
  2. Forcing them into the scalar `classical_hadith_evaluations` table would violate the non-flattening mandate.
  3. When ingested in future specialized phases, al-Dāraquṭnī will be presented in a dedicated **Classical ʿIlal Analysis** UI component rendering the multi-route diagram.
