# HADITH MAPPING AUDIT & METHODOLOGY

---

## 1. Controlled Mapping Tiers

| Mapping Level | Definition | Allowed in Production UI? |
|---|---|---|
| **LEVEL A — DETERMINISTIC** | Exact row-level database foreign key join (e.g. `hadiths.id == hid` in same table row). Zero guessing. | **YES (Fully Certified)** |
| **LEVEL B — MULTI-KEY DETERMINISTIC** | Deterministic match verified by 4+ invariant identifiers: Book ID + Chapter + In-Book Hadith # + Matn exact substring. | **YES (Audited Only)** |
| **LEVEL C — MANUAL VERIFIED** | Human hadith scholar audited with cited page/volume proof. | **YES (Documented in Register)** |
| **LEVEL D — PROBABLE** | Approximate matching based on question title or narrator chain similarity without unique number crosswalk. | **NO (Blocked from UI)** |
| **LEVEL E — AMBIGUOUS** | Speculative or automated heuristic guess. | **NO (Strictly Prohibited)** |

---

## 2. Scholar Mapping Assessment

| Scholar | Mapping Strategy | Current Mapping Level | Mīzān Mapping Status |
|---|---|---|---|
| **al-Tirmidhī** | Direct row-level join in Book 3 `taraf_nass` | **LEVEL A** | **DETERMINISTIC (2,726 / 2,726)** |
| **Abū Dāwūd** | Direct row-level join in Book 4 `taraf_nass` | **LEVEL A** | **DETERMINISTIC (585 / 585)** |
| **al-Nasāʾī** | Direct row-level join in Book 5 `taraf_nass` | **LEVEL A** | **DETERMINISTIC (151 / 151)** |
| **Aḥmad ibn Ḥanbal** | Question # to Hadith ID crosswalk | **LEVEL D** | **UNMAPPED (Crosswalk unbuilt)** |
| **al-Dāraquṭnī** | Monograph # to Hadith ID crosswalk | **LEVEL D** | **UNMAPPED (Crosswalk unbuilt)** |
| **al-Bukhārī** | Oral statement to Tirmidhī Hadith ID | **LEVEL C** | **UNMAPPED (Requires extraction project)** |
| **Ibn Ḥajar** | *Bulūgh* Hadith # to Sihah Sittah ID | **LEVEL B** | **UNMAPPED (Takhrīj crosswalk unbuilt)** |
| **ʿAlī ibn al-Madīnī** | Biographical notice mapping | **LEVEL E** | **UNMAPPED (Narrator-only)** |
| **Yaḥyā ibn Maʿīn** | Biographical entry mapping | **LEVEL E** | **UNMAPPED (Narrator-only)** |

---

## 3. Mapping Gate Rule
Only scholars with **LEVEL A, LEVEL B, or LEVEL C** mappings may be exposed in the verified production user interface. All candidates with LEVEL D or LEVEL E are strictly deferred.