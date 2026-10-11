# MĪZĀN AL-ḤADĪTH — ISNĀD GEOGRAPHY & HISTORICAL CENTERS SPECIFICATION
**Document Identifier:** `07_ISNAD_GEOGRAPHY_SPEC.md`  
**Certified System Baseline:** Phase 18 Certified Relational Graph  
**Version:** 2.0.0  
**Author:** Lead Data Visualization Engineer & Scholarly Digital Humanities Architect  

---

## 1. Geographic Research Foundations

The geographic dispersion of hadith transmission (*Riḥlah fī Ṭalab al-Ḥadīth*) is mapped strictly from biographical and demographic evidence recorded in the canonical database:
- **Historical Transmission Centers:**
  1. **Madīnah al-Munawwarah:** The prophetic origin hub, seat of the Seven Jurists (*Fuqahāʾ al-Sabʿah*) and Imam Mālik.
  2. **Makkah al-Mukarramah:** Center of Ibn ʿAbbās, ʿAmr ibn Dīnār, and Sufyān ibn ʿUyaynah.
  3. **Al-Kūfah:** Epicenter of ʿAlī, Ibn Masʿūd, Ibrāhīm al-Nakhaʿī, and Sufyān al-Thawrī.
  4. **Al-Baṣrah:** Hub of Anas ibn Mālik, al-Ḥasan al-Baṣrī, Muḥammad ibn Sīrīn, and Shuʿbah ibn al-Ḥajjāj.
  5. **Baghdād:** Abbasid scholarly capital, home to Imam Aḥmad ibn Ḥanbal and Yaḥyā ibn Maʿīn.
  6. **Dimashq (Damascus):** Center of al-Awzāʿī and the Syrian school.
  7. **Al-Fusṭāṭ / Al-Qāhirah (Cairo):** Seat of Imam al-Layth ibn Saʿd and Imam al-Shāfiʿī.
  8. **Nīshāpūr (Khurāsān):** Major eastern hub for Imam Muslim and Imam al-Ḥākim.
  9. **Bukhārā & Samarqand (Transoxiana):** Origin of Imam al-Bukhārī.
  10. **Al-Rayy:** Hub of Abū Ḥātim al-Rāzī and Abū Zurʿah al-Rāzī.
  11. **Sanʿāʾ (Yemen):** Center of ʿAbd al-Razzāq al-Ṣanʿānī and Maʿmar ibn Rāshid.
  12. **Al-Qayrawān & Cordoba (Maghrib / Andalus):** Western transmission hubs.

---

## 2. Interactive Map Capabilities

- **Location Clustering:** Aggregates narrators by city with radius proportional to transmitter density.
- **Narrator Detail Drawer:** Clicking a center reveals all affiliated scholars grouped by generation (*Ṣaḥābah*, *Tābiʿīn*, *Atbāʿ*).
- **Zero-Speculation Edge Constraint:** Edges between cities are drawn *only* when an authenticated transmission relationship connects a scholar in City A to a scholar in City B.
- **Filtering by Generation & Collection:** Filter active regional displays by book (e.g. Sahih al-Bukhari only) or era (1st, 2nd, 3rd Century AH).
