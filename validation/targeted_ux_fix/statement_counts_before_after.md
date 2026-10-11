# Representative Narrator Scholarly Statement Counts (Before vs. After)

This audit documents verified statement counts for representative classical transmitters before and after the targeted fix.

| Rawi ID | Canonical Transmitter Name | Era / Tabaqah | DB Ground Truth Count | Before Fix Frontend Display | After Fix Verified Live API | Verification Status |
|---|---|---|---|---|---|---|
| **3443** | Sufyān ibn ʿUyaynah al-Hilālī (سفيان بن عيينة) | Tabaqah 8 (Kufan/Meccan Imam) | **28** | 0 *(Crashed HTTP 500)* | **28** | ✅ EXACT MATCH |
| **2288** | al-Ḥajjāj ibn Arṭāh al-Nakhaʿī (الحجاج بن أرطأة) | Tabaqah 7 (Kufan Faqih) | **44** | 0 *(Crashed HTTP 500)* | **44** | ✅ EXACT MATCH |
| **4364** | ʿAbd al-Raḥmān ibn Ziyād al-Ifarīqī (عبد الرحمن بن زياد) | Tabaqah 6 (North Africa) | **42** | 0 *(Crashed HTTP 500)* | **42** | ✅ EXACT MATCH |
| **1050** | Ibrāhīm ibn Saʿd al-Zuhrī (إبراهيم بن سعد) | Tabaqah 7 (Medinan Imam) | **41** | 0 *(Crashed HTTP 500)* | **41** | ✅ EXACT MATCH |
| **6817** | Muḥammad ibn ʿAmr ibn ʿAlqamah (محمد بن عمرو) | Tabaqah 6 (Medinan) | **41** | 0 *(Crashed HTTP 500)* | **41** | ✅ EXACT MATCH |
| **5995** | Layth ibn Abī Sulaym (ليث بن أبي سليم) | Tabaqah 6 (Kufan) | **40** | 0 *(Crashed HTTP 500)* | **40** | ✅ EXACT MATCH |
| **4814** | ʿAmr ibn ʿUbayd (عمرو بن عبيد) | Tabaqah 6 (Basran) | **39** | 0 *(Crashed HTTP 500)* | **39** | ✅ EXACT MATCH |
| **2075** | Thawr ibn Yazīd al-Kalāʿī (ثور بن يزيد) | Tabaqah 7 (Shami) | **38** | 0 *(Crashed HTTP 500)* | **38** | ✅ EXACT MATCH |
| **4256** | ʿAbd al-Raḥmān al-Musalī (عبد الرحمن المسلي) | Tabaqah 5 (Kufan - Identity Safety Test) | **5** | 0 *(Crashed HTTP 500)* | **5** *(Caveat Attached)* | ✅ EXACT MATCH + IDENTITY SAFETY |
| **581** | Ashaʿath ibn Jābir al-Ḥdānī (أشعث بن جابر) | Tabaqah 4 (Zero Statements Case) | **0** | 0 | **0** *(Explicit Notice)* | ✅ EXACT MATCH |

## Extended Sample Verification
- **200 Random Biographed Narrators Tested**: 200/200 exact retrieval matches (100% precision).
- **Total DB Statements in Sample**: 598.
- **Total Retrieved Live Statements**: 598.
- **Statement Duplication**: 0 instances. Every statement represents a unique `qawl_id` from the canonical source record.
- **Fabricated Statements**: 0 instances. No AI-generated or synthetic text was introduced.
