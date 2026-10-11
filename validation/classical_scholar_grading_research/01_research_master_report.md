# MĪZĀN AL-ḤADĪTH — CLASSICAL SCHOLAR GRADING RESEARCH MASTER REPORT
**Audit Date:** 2026-10-06  
**Auditor:** Anti Gravity Senior Hadith Database Architect & Security Auditor  
**Status:** COMPLETE & CERTIFIED  

---

## 1. Executive Summary

This investigation was conducted under strict zero-trust parameters to evaluate whether classical hadith scholars' evaluations (e.g. Imam al-Bukhari, Imam Ahmad ibn Hanbal, Yahya ibn Ma'in, Ibn Hajar al-Asqalani, al-Daraqutni, al-Dhahabi, Abu Hatim, Abu Zur'ah, etc.) exist in Mīzān's existing database corpus, source repositories, or external legally usable materials.

### Core Discoveries:
1. **Existing Hadith Grades (`hadith_grades`):**
   The project's `hadith_grades` table contains **65,420 entries**, all originating from 20th/21st-century critical editions and muhaddithin:
   - Shaykh Zubayr 'Ali Za'i (18,375 entries)
   - Shaykh Muhammad Nasir al-Din al-Albani (18,301 entries)
   - Shaykh Shu'ayb al-Arna'ut (6,374 entries)
   - Shaykh 'Abd al-Fattah Abu Ghuddah (5,627 entries)
   - Shaykh Muhammad Muhyi al-Din 'Abd al-Hamid (4,503 entries)
   - Shaykh Muhammad Fu'ad 'Abd al-Baqi (4,313 entries)
   - Shaykh Ahmad Muhammad Shakir (3,698 entries)
   - Dr. Bashar 'Awwad Ma'ruf (2,406 entries)
   - Shaykh Salim al-Hilali (1,823 entries)
   **Zero classical scholars exist in `hadith_grades`.**

2. **Existing Narrator Evaluations (`alems` & `aqwal`):**
   All 15 candidate classical scholars **are already present** in `hadith-kg.db` in the `alems` table with **over 63,000 verified narrator critical statements** (`aqwal al-rijāl`):
   - Ibn Hibban: 12,250 aqwal
   - al-Dhahabi: 11,501 aqwal
   - Ibn Hajar al-Asqalani: 10,377 aqwal
   - Abu Hatim al-Razi: 5,227 aqwal
   - al-Bukhari: 4,783 aqwal
   - Ibn Abi Hatim: 3,845 aqwal
   - Yahya ibn Ma'in: 3,293 aqwal
   - al-Daraqutni: 2,984 aqwal
   - al-Nasa'i: 2,735 aqwal
   - Ahmad ibn Hanbal: 1,963 aqwal
   - Abu Zur'ah al-Razi: 1,703 aqwal
   - Abu Dawud: 1,206 aqwal
   - Ali ibn al-Madini: 861 aqwal
   - al-Tirmidhi: 238 aqwal
   - Malik ibn Anas: 76 aqwal

3. **Critical Scholarly Integrity Principle:**
   As mandated by scholarly methodology and prompt Section 5, **Narrator Evaluation (Rijāl criticism: Thiqah, Da'if, Saduq)** must NEVER be converted into **Hadith Grading (Sahih, Hasan, Da'if)** unless the scholar explicitly stated that verdict for that specific narration. Converting "Ahmad evaluated rawi as Thiqah" into "Ahmad: Sahih" would be a catastrophic scholarly falsification.

---

## 2. Forensic Candidate Scholar Matrix

| Scholar | Exists in DB? | Narrator Aqwal | Hadith Grades | Source Work | Attribution | Usability Verdict |
| :--- | :---: | :---: | :---: | :--- | :--- | :--- |
| **al-Bukhārī** (d. 256) | YES | 4,783 | 0 | al-Tārīkh al-Kabīr | Direct | Narrator: IMPLEMENT / Hadith Grade: DEFER |
| **Aḥmad ibn Ḥanbal** (d. 241) | YES | 1,963 | 0 | al-ʿIlal wa-Maʿrifat al-Rijāl | Direct ('Abdullah) | Narrator: IMPLEMENT / Hadith Grade: DO NOT IMPLEMENT |
| **Yaḥyā ibn Maʿīn** (d. 233) | YES | 3,293 | 0 | Tārīkh Ibn Maʿīn | Direct (al-Duri) | Narrator: IMPLEMENT / Hadith Grade: DO NOT IMPLEMENT |
| **Ibn Ḥajar al-ʿAsqalānī** (d. 852) | YES | 10,377 | 0 | Taqrīb & Tahdhīb al-Tahdhīb | Authoritative | Narrator: IMPLEMENT / Hadith Grade: DEFER |
| **ʿAlī ibn al-Madīnī** (d. 234) | YES | 861 | 0 | Kitāb al-ʿIlal | Direct | Narrator: IMPLEMENT / Hadith Grade: DO NOT IMPLEMENT |
| **Abū Zurʿah al-Rāzī** (d. 264) | YES | 1,703 | 0 | al-Jarḥ wa-al-Taʿdīl | Direct | Narrator: IMPLEMENT / Hadith Grade: DO NOT IMPLEMENT |
| **Abū Ḥātim al-Rāzī** (d. 277) | YES | 5,227 | 0 | al-Jarḥ wa-al-Taʿdīl | Direct | Narrator: IMPLEMENT / Hadith Grade: DO NOT IMPLEMENT |
| **al-Dāraquṭnī** (d. 385) | YES | 2,984 | 0 | Sunan & al-ʿIlal | Direct | Narrator: IMPLEMENT / Hadith Grade: DO NOT IMPLEMENT |
| **al-Dhahabī** (d. 748) | YES | 11,501 | 0 | Mīzān al-Iʿtidāl | Authoritative | Narrator: IMPLEMENT / Hadith Grade: DEFER |
| **Ibn Abī Ḥātim** (d. 327) | YES | 3,845 | 0 | al-Jarḥ wa-al-Taʿdīl | Direct | Narrator: IMPLEMENT / Hadith Grade: DO NOT IMPLEMENT |
| **Ibn Ḥibbān** (d. 354) | YES | 12,250 | 0 | al-Thiqāt & al-Majrūḥīn | Direct | Narrator: IMPLEMENT / Hadith Grade: DO NOT IMPLEMENT |
| **al-Tirmidhī** (d. 279) | YES | 238 | 0 | al-Jāmiʿ al-Kabīr | Direct | Narrator: IMPLEMENT / Hadith Grade: DEFER |
| **Abū Dāwūd** (d. 275) | YES | 1,206 | 0 | Su'ālāt al-Ājurrī | Direct | Narrator: IMPLEMENT / Hadith Grade: DO NOT IMPLEMENT |
| **al-Nasāʾī** (d. 303) | YES | 2,735 | 0 | al-Ḍuʿafāʾ wa-al-Matrūkūn | Direct | Narrator: IMPLEMENT / Hadith Grade: DO NOT IMPLEMENT |
| **Mālik ibn Anas** (d. 179) | YES | 76 | 0 | al-Muwaṭṭaʾ | Direct | Narrator: IMPLEMENT / Hadith Grade: DO NOT IMPLEMENT |

---

## 3. UI/UX Architecture & Acceptance

Rather than creating artificial "consensus" grades or fabricating classical hadith grades, Mīzān implements a truthful, scholarly presentation:

1. **Clear Division of Scholarly Evidence:**
   - **Contemporary / Modern Critical Editions:** Exact hadith authenticity verdicts from 20th/21st-century research editions (Zubayr Ali Zai, Al-Albani, Shu'ayb al-Arna'ut, Fu'ad Abd al-Baqi, Ahmad Shakir, etc.) with publisher, edition, and exact terminology.
   - **Classical Scholarly Evidence (Aqwāl al-ʿUlamāʾ):** Direct narrator and isnād evaluations from classical imams of Jarḥ wa-Taʿdīl (Ahmad ibn Hanbal, Yahya ibn Ma'in, al-Bukhari, Ibn Hajar, Abu Hatim, Abu Zur'ah, etc.) displaying the exact Arabic statement, English translation, and specific target transmitter.

2. **Interactive Filtering:**
   - Filter by Type: `All Evidence`, `Contemporary Hadith Grades`, `Classical Narrator Critics`.
   - Filter by Scholar: Dynamically populated ONLY with scholars who have verified evidence for this narration.

3. **Zero Algorithmic Consensus Rule:**
   - No majority voting ("3 out of 4 scholars say Sahih").
   - No synthetic confidence percentages ("92% Authentic").
   - Evidence is presented side-by-side with full provenance.

---

## 4. Zero-Trust Database Certification
- Canonical database `data/hadith-kg.db` was accessed in read-only mode (`mode=ro`).
- SHA-256 Pre-Hash: `08c3a43d78f51082...`
- SHA-256 Post-Hash: `08c3a43d78f51082...` (PRE_HASH == POST_HASH).
- Canonical database mutation: **NONE**.
