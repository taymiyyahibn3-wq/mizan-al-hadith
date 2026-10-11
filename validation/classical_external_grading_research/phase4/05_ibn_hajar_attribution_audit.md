# IBN ḤAJAR ATTRIBUTION AUDIT: MULTI-LAYER ENGINE

## 1. Forensic Attribution Analysis
In *Bulūgh al-Marām*, over **70% of evaluations are citations of earlier classical authorities**:
- *"رَوَاهُ الْخَمْسَةُ، وَصَحَّحَهُ التِّرْمِذِيُّ"* $ightarrow$ Evaluator: **al-Tirmidhī**.
- *"رَوَاهُ ابْنُ مَاجَهْ، وَصَحَّحَهُ ابْنُ حِبَّانَ"* $ightarrow$ Evaluator: **Ibn Ḥibbān**.
- *"رَوَاهُ الْأَرْبَعَةُ، وَصَحَّحَهُ ابْنُ خُزَيْمَةَ"* $ightarrow$ Evaluator: **Ibn Khuzaymah**.

Direct rulings by Ibn Ḥajar (*"وَإِسْنَادُهُ صَحِيحٌ"*, *"قُلْتُ: وَفِيهِ عِلَّةٌ"*) represent <30% of entries.

## 2. Attribution Safety Rule
Attributing *"وَصَحَّحَهُ التِّرْمِذِيُّ"* as `Scholar: Ibn Ḥajar` violates scholarly attribution principles.
The multi-layer attribution regex parser designed in Phase 3 successfully classifies entries into:
- `DIRECT_AUTHOR_RULING`
- `QUOTED_CLASSICAL_CRITIC`
- `COMPILER_CITATION_ONLY`

Implementation is deferred until both attribution parsing and crosswalk alignment are combined.
