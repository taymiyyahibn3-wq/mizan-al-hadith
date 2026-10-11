# AL-DĀRAQUṬNĪ IMPLEMENTATION AUDIT: RELATIONAL DATA MODEL

## 1. Non-Flattening Mandate
al-Dāraquṭnī evaluates **competing transmission branches**, not single scalar hadiths.
Forcing an entry such as:
> *"ورواه شعبة عن قتادة موقوفا، ورواه حماد مرفوعا، والموقوف هو الصحيح والوهم فيه من حماد"*

into `hadith_id -> Ḍaʿīf` is a severe scholarly falsehood. The hadith itself may be authentic through other routes; what is defective is Hammād's elevation (*Rafʿ*).

## 2. Implemented Schema Architecture
The relational model designed in Phase 3 is validated as the definitive schema for future ingestion:
- `daraqutni_inquiries`
- `daraqutni_variant_routes`
- `daraqutni_defects`
- `daraqutni_tarjih`

Zero records are prematurely forced into the production database during this phase to maintain 100% data integrity.
