# MĪZĀN AL-ḤADĪTH — SECURITY & SCHOLARLY INTEGRITY

**Document Identifier:** `docs/architecture/security-and-integrity.md`  
**System Baseline:** Phase 18 Forensic Integrity Architecture  

---

## 1. The Principle of Scholarly Integrity

In Islamic digital humanities, software bugs or algorithmic hallucinations do not merely degrade user experience—they risk corrupting religious texts, misattributing scholarly statements, or introducing doctrinal distortions.

Mīzān al-Ḥadīth implements **four computational safety invariants** to protect scholarly integrity:

---

## 2. Invariant 1: Canonical Read-Only Access

Canonical databases (`hadith-kg.db`, `classical_scholar_evidence.db`, etc.) are completely immutable at runtime:
1. **URI Mode Flags:** Connections are opened strictly with `?mode=ro`.
2. **Prohibited Write Operations:** Any runtime query containing `INSERT`, `UPDATE`, `DELETE`, `ALTER`, or `DROP` directed toward a canonical database raises an immediate fatal exception.
3. **Additive Caches:** All user-generated content, conversation histories, and bookmarks reside in external databases (`ask_mizan.db`, `research_workspace.db`).

---

## 3. Invariant 2: Father/Son & Similar-Name Collision Guards

A frequent error in automatic narrator linking is confusing transmitters who share names or parentage.

### Case Study: Abdur Rahman al-Musalli vs. Wabarah
In biographical literature, **Abdur Rahman al-Musalli (Rawi #4256)** was graded by some critics, while his son **Wabarah ibn Abdur Rahman (Rawi #8145)** received praise (*tawthīq*) from Yahya ibn Ma'in. Unrefined search algorithms erroneously attributed Yahya ibn Ma'in's judgment to the father.

### Technical Remediation (`identity_resolution.py`):
```python
# Guarding father/son collision in narrator verdicts
if rawi_id == 4256 and alem_id == YAHYA_IBN_MAIN_ID:
    return {
        "is_verified": False,
        "attribution_status": "father_son_collision",
        "caveat": "Identity Attribution Unresolved: In classical rijal authorities (al-Mizzi 17/413), Yahya ibn Ma'in's tawthiq refers to the son Wabarah (#8145), not Abdur Rahman (#4256)."
    }
```
When this condition is met:
- The API explicitly returns `is_verified: false`.
- The frontend renders an amber alert badge (`ScholarlyStatementCard.tsx`) explaining the historical ambiguity.
- Automated tests (`scripts/test_scholarly_integrity.py`) assert that this guard triggers 100% of the time.

---

## 4. Invariant 3: Famous Alias Disambiguation

Transmitters frequently share patronymics (*Kunyah*) or tribal nicknames (*Nisbah*). For example:
- **Sufyan al-Thawri (Rawi #3436)** is an authoritative master (*Amīr al-Muʾminīn fī al-Ḥadīth*).
- **Sufyan ibn 'Uyaynah (Rawi #3443)** is an independent contemporary master.
- **Sufyan ibn Hamzah (Rawi #3432)** is an obscure regional transmitter.

The identity resolution engine (`identity_resolution.py`) enforces strict canonical resolution to prevent cross-contamination of biographical profiles or isnād graphs.

---

## 5. Invariant 4: Separation of Editorial Opinions from Primary Evidence

1. **Independent Columns:** In database schemas, classical primary evaluations (e.g. Imam al-Tirmidhi's *hukum*) are stored separately from modern editorial gradings (e.g. Shaykh al-Albani or Zubair Ali Zai).
2. **Explicit Labeling:** The UI explicitly denotes whether a grade is from the classical author himself or a 20th-century researcher.
3. **Workspace Isolation:** Research notes authored in `/workspace` carry `source_tier = "RESEARCHER_WORKSPACE"` and `is_canonical = false`, ensuring private hypothesis formulation cannot be confused with historical transmission facts.
