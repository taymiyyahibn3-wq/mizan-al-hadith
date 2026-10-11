# ATTRIBUTION MODEL AUDIT: MULTI-LAYER CITATIONS

---

## 1. Principles of Scholarly Attribution

A major failure mode in digital hadith systems is the flattening of multi-layered transmission chains into a single pseudo-author.

### The Problem
When a 9th-century commentator (such as Ibn Ḥajar in *Bulūgh al-Marām*) writes:
> "رَوَاهُ الْخَمْسَةُ، وَصَحَّحَهُ التِّرْمِذِيُّ"  
A naive system attributes this as:
> `Scholar: Ibn Ḥajar` | `Grade: Ṣaḥīḥ`

This is a **gross scholarly error**:
1. Ibn Ḥajar did not grade the hadith Ṣaḥīḥ; he reported that **Imām al-Tirmidhī** graded it.
2. If al-Tirmidhī's actual verdict was *Ḥasan Ṣaḥīḥ*, flattening it through Ibn Ḥajar misquotes both scholars.

---

## 2. Controlled Attribution Schema

Mīzān enforces a 5-role attribution structure for every record:

```json
{
  "original_authority": "al-Imām al-Tirmidhī",
  "transmitting_compiler": "al-Ḥāfiẓ Ibn Ḥajar al-ʿAsqalānī",
  "source_work": "Bulūgh al-Marām min Adillat al-Aḥkām",
  "attribution_chain": "Ibn Ḥajar -> quoting al-Tirmidhī -> from al-Jāmiʿ al-Kabīr",
  "attribution_category": "QUOTED_CLASSICAL_VERDICT"
}
```

### Attribution Categories
1. `DIRECT_AUTHORIAL_EVALUATION`: The author personally issues the judgment in their own work (e.g. al-Tirmidhī in *al-Jāmiʿ*, Abū Dāwūd in *al-Sunan*).
2. `QUOTED_CLASSICAL_VERDICT`: The author quotes an earlier classical critic (e.g. Ibn Ḥajar quoting Ibn Ḥibbān or al-Tirmidhī).
3. `ORAL_TRANSMISSION`: The author reports verbal criticism heard directly from their master (e.g. al-Tirmidhī reporting from al-Bukhārī; ʿAbd Allāh reporting from Aḥmad).
4. `TRANSMITTER_ADDITION (Ziyādat al-Rāwī)`: The transmitter of the book adds an isnād or remark (e.g. Abū al-Ḥasan al-Qaṭṭān in *Sunan Ibn Mājah*).