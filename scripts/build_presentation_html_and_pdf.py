"""
Generate MĪZĀN AL-ḤADĪTH 20-Slide Standalone HTML & Render PDF
Creates:
1. presentation/presentation_01/index.html (20-slide interactive standalone presentation)
2. presentation/presentation_01/presentation.css (with @media print 16:9 widescreen rules)
3. Mizan_al_Hadith_Introduction_Presentation.pdf (Rendered via Edge headless)
"""

import os
import sys
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

SLIDES_DATA = [
    {
        "id": 1,
        "tag": "SLIDE 01 · INSTITUTIONAL INTRODUCTION",
        "title": "Mīzān al-Ḥadīth: Institutional Introduction",
        "category": "Vision",
        "time": "1.5 min",
        "citation": "Phase 18 Certified Release Baseline · October 2026",
        "notes": "Good morning, Professor Syed and colleagues. Today, we are presenting Mīzān al-Ḥadīth. For centuries, Islamic scholars have engaged in some of the most rigorous historical-critical analysis in human civilization. Yet our modern digital tools have remained flat, fragmented, and disconnected. Mīzān was created to bring the full power of modern relational graphs and digital humanities to this sacred heritage—without compromising a single principle of classical methodology.",
        "html": """
        <div class="title-folio-wrap">
          <div class="title-folio-badge">● Academic Research Platform &amp; Institutional Overview</div>
          <div class="arabic-display-title" dir="rtl">مِيزَانُ الحَدِيث</div>
          <h1 class="main-display-title">MĪZĀN AL-ḤADĪTH</h1>
          <div class="title-divider"></div>
          <p class="title-desc">
            A Research Platform for Exploring Hadith, Narrators, Isnād, Commentaries, and Scholarly Evaluation
          </p>

          <div class="census-strip">
            <div class="census-card">
              <div class="census-label">Canonical Hadiths</div>
              <div class="census-val">715,790</div>
            </div>
            <div class="census-card">
              <div class="census-label">Collections &amp; Books</div>
              <div class="census-val">425</div>
            </div>
            <div class="census-card">
              <div class="census-label">Verified Narrators</div>
              <div class="census-val">49,844</div>
            </div>
            <div class="census-card">
              <div class="census-label">Transmission Chains</div>
              <div class="census-val">577,024</div>
            </div>
            <div class="census-card">
              <div class="census-label">Scholarly Evaluations</div>
              <div class="census-val">65,420</div>
            </div>
          </div>
        </div>
        """
    },
    {
        "id": 2,
        "tag": "SLIDE 02 · RESEARCH PROBLEM",
        "title": "The Problem: Rich Knowledge, Fragmented Access",
        "category": "Problem",
        "time": "1.5 min",
        "citation": "Academic Workflow Analysis · Hadith Studies Domain Research",
        "notes": "Hadith scholarship possesses one of the richest evidentiary traditions in history. But in contemporary research, accessing it requires consulting separate numbering systems, distinct narrator biographical dictionaries, separate commentary volumes, and divergent scholarly evaluations. Conventional digital tools merely dump raw text, leaving the burden of manual cross-referencing entirely on the researcher.",
        "html": """
        <div class="slide-header">
          <span class="slide-kicker">The Scholarly Dilemma</span>
          <h2 class="slide-title">Hadith knowledge is rich — but finding the connections is difficult.</h2>
          <p class="slide-subtitle">Researchers spend hours cross-referencing editions, tracing biographical dictionaries, and tracking commentary variations.</p>
        </div>
        <div class="grid-4" style="margin-top: 1.5rem;">
          <div class="card card-emerald">
            <div class="card-icon">🔢</div>
            <div class="card-title">Conflicting Editions</div>
            <div class="card-desc">Publishers in Cairo, Beirut, and Riyadh use contradictory numbering schemas for the exact same hadith.</div>
          </div>
          <div class="card card-gold">
            <div class="card-icon">⛓️</div>
            <div class="card-title">Opaque Chains</div>
            <div class="card-desc">Chains of narrators (isnāds) are printed as plain text strings, obscuring branch points and common transmitters.</div>
          </div>
          <div class="card card-emerald">
            <div class="card-icon">⚖️</div>
            <div class="card-title">Flattened Gradings</div>
            <div class="card-desc">Search engines reduce multi-century scholarly debates to a simplistic binary 'Authentic' or 'Weak' tag.</div>
          </div>
          <div class="card card-gold">
            <div class="card-icon">📖</div>
            <div class="card-title">Detached Commentaries</div>
            <div class="card-desc">Classical explanations from scholars like Ibn Ḥajar or al-Nawawī remain physically separated from the texts.</div>
          </div>
        </div>
        """
    },
    {
        "id": 3,
        "tag": "SLIDE 03 · THE CORE CONCEPT",
        "title": "The Basic Idea: A Connected Research Graph",
        "category": "Concept",
        "time": "1.5 min",
        "citation": "Relational Ontology Architecture · Mīzān Schema Design",
        "notes": "Mīzān fundamentally re-imagines how hadith data is organized. Instead of isolated text files or flat spreadsheets, Mīzān treats the entire hadith corpus as a connected, multidimensional knowledge graph where every text, edition, narrator, isnād, evaluation, and commentary note is explicitly linked.",
        "html": """
        <div class="slide-header">
          <span class="slide-kicker">Core Paradigm Shift</span>
          <h2 class="slide-title">What if hadith research could be explored as a connected system?</h2>
          <p class="slide-subtitle">Instead of isolated text entries, Mīzān connects texts, editions, narrators, isnāds, evaluations, and commentaries.</p>
        </div>
        <div class="card" style="padding: 1.75rem; margin-top: 1.5rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; text-align: center; gap: 0.5rem; flex-wrap: wrap;">
            <div style="background: var(--green-soft); color: var(--green-deep); padding: 0.75rem 1rem; border-radius: 0.5rem; font-weight: 600; border: 1px solid var(--green-primary);">Hadith Text</div>
            <div style="color: var(--gold-primary); font-size: 1.25rem;">➔</div>
            <div style="background: var(--gold-soft); color: var(--gold-dark); padding: 0.75rem 1rem; border-radius: 0.5rem; font-weight: 600; border: 1px solid var(--gold-border);">Collections &amp; Editions</div>
            <div style="color: var(--gold-primary); font-size: 1.25rem;">➔</div>
            <div style="background: var(--green-soft); color: var(--green-deep); padding: 0.75rem 1rem; border-radius: 0.5rem; font-weight: 600; border: 1px solid var(--green-primary);">Numbering Crosswalk</div>
            <div style="color: var(--gold-primary); font-size: 1.25rem;">➔</div>
            <div style="background: var(--gold-soft); color: var(--gold-dark); padding: 0.75rem 1rem; border-radius: 0.5rem; font-weight: 600; border: 1px solid var(--gold-border);">Narrators &amp; Tabaqāt</div>
            <div style="color: var(--gold-primary); font-size: 1.25rem;">➔</div>
            <div style="background: var(--green-soft); color: var(--green-deep); padding: 0.75rem 1rem; border-radius: 0.5rem; font-weight: 600; border: 1px solid var(--green-primary);">Transmission Chains</div>
            <div style="color: var(--gold-primary); font-size: 1.25rem;">➔</div>
            <div style="background: var(--gold-soft); color: var(--gold-dark); padding: 0.75rem 1rem; border-radius: 0.5rem; font-weight: 600; border: 1px solid var(--gold-border);">Scholarly Judgments</div>
            <div style="color: var(--gold-primary); font-size: 1.25rem;">➔</div>
            <div style="background: var(--green-soft); color: var(--green-deep); padding: 0.75rem 1rem; border-radius: 0.5rem; font-weight: 600; border: 1px solid var(--green-primary);">Commentaries</div>
          </div>
          <div style="margin-top: 1.5rem; padding: 1rem; background: var(--surface-cream); border-left: 4px solid var(--gold-primary); border-radius: 0.25rem;">
            <p style="font-size: 0.95rem; color: var(--ink-body);">
              <strong>Scholarly Benefit:</strong> A researcher examining a hadith can jump instantly to its narrator biographies, inspect its transmission branching across the Islamic world, compare its wording variants, and read its classical commentary—all within a single unified workspace.
            </p>
          </div>
        </div>
        """
    },
    {
        "id": 4,
        "tag": "SLIDE 04 · PLATFORM CAPABILITIES",
        "title": "What Mīzān Actually Is: Research Workbench",
        "category": "Overview",
        "time": "1.5 min",
        "citation": "System Feature Inventory · Mīzān Production Core",
        "notes": "Mīzān is not a generic consumer hadith app or a basic keyword search box. It is a purpose-built digital humanities platform engineered specifically for academic research. It provides four specialized primary modules: a Cross-Edition Reader, an Isnād Graph Explorer, a Multi-Scholar Evaluation Matrix, and a Relational Commentary Engine.",
        "html": """
        <div class="slide-header">
          <span class="slide-kicker">Architecture &amp; Features</span>
          <h2 class="slide-title">Mīzān is more than a hadith search box.</h2>
          <p class="slide-subtitle">Translating traditional hadith disciplines into structured research tools.</p>
        </div>
        <div class="grid-4" style="margin-top: 1.5rem;">
          <div class="card card-emerald">
            <div class="card-icon">📚</div>
            <div class="card-title">Cross-Edition Reader</div>
            <div class="card-desc">Compare texts across multiple major print publications side-by-side with full vocalization and variant indicators.</div>
          </div>
          <div class="card card-gold">
            <div class="card-icon">🕸️</div>
            <div class="card-title">Isnād Network Graph</div>
            <div class="card-desc">Explore generational transmission paths, identify common transmitters (madār), and view narrator biographies.</div>
          </div>
          <div class="card card-emerald">
            <div class="card-icon">⚖️</div>
            <div class="card-title">Multi-Scholar Matrix</div>
            <div class="card-desc">Inspect evaluations from 9 classical and modern hadith authorities side-by-side without flattening differences.</div>
          </div>
          <div class="card card-gold">
            <div class="card-icon">📑</div>
            <div class="card-title">Commentary Explorer</div>
            <div class="card-desc">Read classical explanations with exact relational scope linking to specific hadith paragraphs.</div>
          </div>
        </div>
        """
    },
    {
        "id": 5,
        "tag": "SLIDE 05 · DATA FOUNDATION",
        "title": "The Data Foundation: Interconnected Scale",
        "category": "Data",
        "time": "1.5 min",
        "citation": "Phase 18 Certified Database Census · Verified Cryptographic Baseline",
        "notes": "The foundation of Mīzān is not a mock or toy dataset. It contains 715,790 hadiths, 425 collections and books, nearly 50,000 verified narrators, over 577,000 transmission chains, 4.4 million transmission links, and 65,420 scholarly evaluations across 9 major critical authorities.",
        "html": """
        <div class="slide-header">
          <span class="slide-kicker">Empirical Scale</span>
          <h2 class="slide-title">Built on a large interconnected data layer</h2>
          <p class="slide-subtitle">Rigorous, multi-database architecture certified against corruption and data loss.</p>
        </div>
        <div class="grid-3" style="margin-top: 1.5rem;">
          <div class="card" style="text-align: center; padding: 1.5rem;">
            <div style="font-size: 2.25rem; font-weight: 700; color: var(--green-primary); font-family: var(--font-display);">715,790</div>
            <div style="font-weight: 600; color: var(--ink-primary); margin-top: 0.25rem;">Canonical Hadiths</div>
            <div style="font-size: 0.85rem; color: var(--ink-muted); margin-top: 0.25rem;">Covering 425 collections &amp; books</div>
          </div>
          <div class="card" style="text-align: center; padding: 1.5rem;">
            <div style="font-size: 2.25rem; font-weight: 700; color: var(--gold-primary); font-family: var(--font-display);">49,844</div>
            <div style="font-weight: 600; color: var(--ink-primary); margin-top: 0.25rem;">Verified Narrators</div>
            <div style="font-size: 0.85rem; color: var(--ink-muted); margin-top: 0.25rem;">Cross-referenced biographical registry</div>
          </div>
          <div class="card" style="text-align: center; padding: 1.5rem;">
            <div style="font-size: 2.25rem; font-weight: 700; color: var(--green-primary); font-family: var(--font-display);">577,024</div>
            <div style="font-weight: 600; color: var(--ink-primary); margin-top: 0.25rem;">Transmission Chains</div>
            <div style="font-size: 0.85rem; color: var(--ink-muted); margin-top: 0.25rem;">4,414,211 verified sequence steps</div>
          </div>
          <div class="card" style="text-align: center; padding: 1.5rem;">
            <div style="font-size: 2.25rem; font-weight: 700; color: var(--gold-primary); font-family: var(--font-display);">65,420</div>
            <div style="font-weight: 600; color: var(--ink-primary); margin-top: 0.25rem;">Scholarly Evaluations</div>
            <div style="font-size: 0.85rem; color: var(--ink-muted); margin-top: 0.25rem;">Preserved across 9 major critics</div>
          </div>
          <div class="card" style="text-align: center; padding: 1.5rem;">
            <div style="font-size: 2.25rem; font-weight: 700; color: var(--green-primary); font-family: var(--font-display);">127,863</div>
            <div style="font-weight: 600; color: var(--ink-primary); margin-top: 0.25rem;">Biographical Judgments</div>
            <div style="font-size: 0.85rem; color: var(--ink-muted); margin-top: 0.25rem;">Jarḥ wa Taʿdīl statements</div>
          </div>
          <div class="card" style="text-align: center; padding: 1.5rem;">
            <div style="font-size: 2.25rem; font-weight: 700; color: var(--gold-primary); font-family: var(--font-display);">1,015</div>
            <div style="font-weight: 600; color: var(--ink-primary); margin-top: 0.25rem;">Historical Critics</div>
            <div style="font-size: 0.85rem; color: var(--ink-muted); margin-top: 0.25rem;">Spanning 1,200 years of scholarship</div>
          </div>
        </div>
        """
    },
    {
        "id": 6,
        "tag": "SLIDE 06 · NUMBERING RECONCILIATION",
        "title": "Multiple Editions & Numbering Systems",
        "category": "Numbering",
        "time": "1.5 min",
        "citation": "Phase 13 Numbering Harmonization · hadith_numbering.db",
        "notes": "One of the greatest headaches for researchers is numbering divergence. In Ṣaḥīḥ al-Bukhārī, al-Bugha uses one numbering, Fatḥ al-Bārī another, and Dār al-Salām yet another. Mīzān harmonizes these editions under a unified canonical identifier while preserving every print edition's native numbering.",
        "html": """
        <div class="slide-header">
          <span class="slide-kicker">Cross-Edition Mapping</span>
          <h2 class="slide-title">One hadith can have different numbers.</h2>
          <p class="slide-subtitle">Mīzān connects varying print numbering systems without conflating or confusing them.</p>
        </div>
        <div class="grid-2" style="margin-top: 1.5rem;">
          <div class="card">
            <div class="card-title" style="color: var(--green-primary); font-size: 1.15rem; margin-bottom: 0.75rem;">The Numbering Problem in Practice</div>
            <p style="font-size: 0.95rem; color: var(--ink-body); line-height: 1.6;">
              When Professor Syed cites <em>Ṣaḥīḥ al-Bukhārī #1</em> ("Actions are by intentions"), different published editions assign distinct numbering references depending on chapter divisions, compiler comments, and edition formatting.
            </p>
            <div style="margin-top: 1rem; padding: 0.75rem; background: var(--surface-cream); border-radius: 0.5rem; border: 1px solid var(--line-soft);">
              <ul style="list-style: none; padding-left: 0; font-size: 0.9rem; line-height: 1.8;">
                <li>📖 <strong>Al-Bughā Edition:</strong> Hadith #1</li>
                <li>📖 <strong>Fatḥ al-Bārī / ʿAbd al-Bāqī:</strong> Hadith #1</li>
                <li>📖 <strong>Dār al-Salām / USC-MSA:</strong> Book 1, Hadith 1</li>
                <li>📖 <strong>In-Book Chapter Numbering:</strong> Kitāb Badʾ al-Waḥy, Bāb 1</li>
              </ul>
            </div>
          </div>
          <div class="card card-gold">
            <div class="card-title" style="color: var(--gold-dark); font-size: 1.15rem; margin-bottom: 0.75rem;">Mīzān's Canonical Resolution</div>
            <p style="font-size: 0.95rem; color: var(--ink-body); line-height: 1.6;">
              Mīzān assigns a single immutable Canonical Identifier (<code>bukhari:1</code>) and maps each published edition as an explicit alias.
            </p>
            <div style="margin-top: 1rem; display: flex; flex-direction: column; gap: 0.5rem;">
              <div style="display: flex; justify-content: space-between; padding: 0.5rem 0.75rem; background: #ffffff; border-radius: 0.25rem; font-size: 0.85rem; border: 1px solid var(--gold-border);">
                <span>Canonical Root</span>
                <strong style="color: var(--green-primary);">bukhari:1</strong>
              </div>
              <div style="display: flex; justify-content: space-between; padding: 0.5rem 0.75rem; background: #ffffff; border-radius: 0.25rem; font-size: 0.85rem; border: 1px solid var(--line-soft);">
                <span>Al-Bughā Alias</span>
                <code>bugha:1</code>
              </div>
              <div style="display: flex; justify-content: space-between; padding: 0.5rem 0.75rem; background: #ffffff; border-radius: 0.25rem; font-size: 0.85rem; border: 1px solid var(--line-soft);">
                <span>Dār al-Salām Alias</span>
                <code>darussalam:1</code>
              </div>
            </div>
          </div>
        </div>
        """
    },
    {
        "id": 7,
        "tag": "SLIDE 07 · SCHOLARLY NUANCE",
        "title": "Preserving Scholarly Disagreement",
        "category": "Gradings",
        "time": "1.5 min",
        "citation": "Multi-Scholar Evaluation Registry · Phase 11 & 14 Audits",
        "notes": "Different hadith scholars evaluate narrations using different methodological criteria. Al-Tirmidhī, al-Albānī, al-Arna'ūṭ, and Ibn Ḥajar frequently differ in their technical phrasing. Mīzān presents each authority's original wording side-by-side, preserving nuanced scholarly distinctions.",
        "html": """
        <div class="slide-header">
          <span class="slide-kicker">Multi-Scholar Evaluative Matrix</span>
          <h2 class="slide-title">Scholars do not always express a judgment in the same way.</h2>
          <p class="slide-subtitle">Mīzān preserves each authority's exact evaluation instead of flattening nuance into binary labels.</p>
        </div>
        <div class="grid-3" style="margin-top: 1.5rem;">
          <div class="card card-emerald">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span class="badge badge-emerald">Ṣaḥīḥ</span>
              <span style="font-size: 0.8rem; color: var(--ink-muted);">Al-Bukhārī / Muslim</span>
            </div>
            <div style="font-weight: 600; margin-top: 0.75rem; color: var(--green-deep);">Rigorous Authenticity</div>
            <p style="font-size: 0.85rem; color: var(--ink-body); margin-top: 0.5rem;">Continuous chain, righteous transmitters with precise retention, free of hidden defects and irregularities.</p>
          </div>
          <div class="card card-gold">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span class="badge badge-gold">Ṣaḥīḥ al-Isnād</span>
              <span style="font-size: 0.8rem; color: var(--ink-muted);">Al-Ḥākim / Al-Dhahabī</span>
            </div>
            <div style="font-weight: 600; margin-top: 0.75rem; color: var(--gold-dark);">Sound Chain Only</div>
            <p style="font-size: 0.85rem; color: var(--ink-body); margin-top: 0.5rem;">Validates chain transmitters without guaranteeing the matn text is free of subtle contradictions.</p>
          </div>
          <div class="card card-emerald">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span class="badge badge-emerald">Ḥasan li-Ghayrihī</span>
              <span style="font-size: 0.8rem; color: var(--ink-muted);">Ibn Ḥajar / Al-Albānī</span>
            </div>
            <div style="font-weight: 600; margin-top: 0.75rem; color: var(--green-deep);">Corroborated Good</div>
            <p style="font-size: 0.85rem; color: var(--ink-body); margin-top: 0.5rem;">Chain has mild weakness elevated to acceptability through independent corroborating paths.</p>
          </div>
          <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span class="badge" style="background: var(--surface-cream); color: var(--ink-primary); border: 1px solid var(--line-soft);">Mawqūf Ṣaḥīḥ</span>
              <span style="font-size: 0.8rem; color: var(--ink-muted);">Al-Bayhaqī</span>
            </div>
            <div style="font-weight: 600; margin-top: 0.75rem; color: var(--ink-primary);">Sound Companion Attribution</div>
            <p style="font-size: 0.85rem; color: var(--ink-body); margin-top: 0.5rem;">Authentic narration terminating at a Companion rather than attributed directly to the Prophet ﷺ.</p>
          </div>
          <div class="card card-gold">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span class="badge badge-gold">Ḥasan Ṣaḥīḥ</span>
              <span style="font-size: 0.8rem; color: var(--ink-muted);">Al-Tirmidhī</span>
            </div>
            <div style="font-weight: 600; margin-top: 0.75rem; color: var(--gold-dark);">Composite Classical Phrasing</div>
            <p style="font-size: 0.85rem; color: var(--ink-body); margin-top: 0.5rem;">Al-Tirmidhī's unique evaluative terminology denoting multiple supporting chains or internal qualities.</p>
          </div>
          <div class="card" style="border: 1px solid #fecdd3; background: #fff1f2;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span class="badge" style="background: #ffe4e6; color: #9f1239; border: 1px solid #fecdd3;">Ḍaʿīf</span>
              <span style="font-size: 0.8rem; color: #9f1239;">Al-Arna'ūṭ</span>
            </div>
            <div style="font-weight: 600; margin-top: 0.75rem; color: #9f1239;">Weak / Defective</div>
            <p style="font-size: 0.85rem; color: #881337; margin-top: 0.5rem;">Defect identified in chain continuity, narrator precision, or conflicting authentic transmissions.</p>
          </div>
        </div>
        """
    },
    {
        "id": 8,
        "tag": "SLIDE 08 · FORENSIC RIGOR",
        "title": "The Zero-Guess Principle: Scientific Quarantine",
        "category": "Integrity",
        "time": "1.5 min",
        "citation": "Phase 14 Zubayr Audit · 18,375 Records Inspected",
        "notes": "This is one of the most critical principles in Mīzān: when data is ambiguous, we do not guess. In Phase 14, out of 18,375 records from Zubayr's collection, 18,089 were certified with certainty. The remaining 286 records had disputed boundary markers. Rather than guessing, Mīzān isolated them in quarantine. Accuracy is never sacrificed for artificial coverage.",
        "html": """
        <div class="slide-header">
          <span class="slide-kicker">Data Integrity Mandate</span>
          <h2 class="slide-title">When the evidence is unclear, Mīzān does not guess.</h2>
          <p class="slide-subtitle">Coverage is never prioritized over scholarly precision. Ambiguity is quarantined, not invented.</p>
        </div>
        <div class="grid-2" style="margin-top: 1.5rem;">
          <div class="card card-emerald">
            <div style="font-size: 2rem; font-weight: 700; color: var(--green-primary); font-family: var(--font-display);">18,089 Records</div>
            <div style="font-weight: 600; color: var(--green-deep); margin-top: 0.5rem; font-size: 1.1rem;">Certified Core Corpus (98.4%)</div>
            <p style="font-size: 0.95rem; color: var(--ink-body); margin-top: 0.75rem; line-height: 1.6;">
              Demonstrated 100% deterministic textual fidelity, verified publisher cross-references, and unbroken chains of scholarly transmission.
            </p>
            <div style="margin-top: 1rem; display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem; color: var(--green-light);">
              <span>✔</span> Cryptographically verified against primary print editions.
            </div>
          </div>
          <div class="card" style="border: 2px solid #fecdd3; background: #fff5f5;">
            <div style="font-size: 2rem; font-weight: 700; color: #9f1239; font-family: var(--font-display);">286 Records</div>
            <div style="font-weight: 600; color: #9f1239; margin-top: 0.5rem; font-size: 1.1rem;">Strictly Quarantined (1.6%)</div>
            <p style="font-size: 0.95rem; color: #4c0519; margin-top: 0.75rem; line-height: 1.6;">
              Disputed editorial paragraph boundaries and ambiguous numbering were quarantined rather than forced into artificial canonical IDs.
            </p>
            <div style="margin-top: 1rem; display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem; color: #9f1239;">
              <span>⚠</span> Zero quarantine records leaked into the public query layer.
            </div>
          </div>
        </div>
        """
    },
    {
        "id": 9,
        "tag": "SLIDE 09 · NETWORK EXPLORATION",
        "title": "Isnād Visualization: Transmission Networks",
        "category": "Visualization",
        "time": "1.5 min",
        "citation": "Isnād Graph Engine · D3/Canvas Visualizer Component",
        "notes": "Instead of viewing an isnād as a lifeless list of names, Mīzān transforms it into a multi-generational transmission graph. Researchers can instantly identify the common link (madār), see branch points, explore co-transmitters (mutāba'āt), and inspect narrator reliability scores.",
        "html": """
        <div class="slide-header">
          <span class="slide-kicker">Interactive Network Architecture</span>
          <h2 class="slide-title">From a chain of names to a transmission network.</h2>
          <p class="slide-subtitle">Visualizing generational tabaqāt, co-transmitters, branch points, and narrator reliability.</p>
        </div>
        <div class="grid-3" style="margin-top: 1.5rem;">
          <div class="card card-emerald">
            <div class="card-icon">🌲</div>
            <div class="card-title">Generational Tabaqāt</div>
            <div class="card-desc">Vertically aligns narrators from the Prophet ﷺ through Companions, Successors, and compilers.</div>
          </div>
          <div class="card card-gold">
            <div class="card-icon">⚡</div>
            <div class="card-title">Common Link (Madār)</div>
            <div class="card-desc">Automatically highlights the central transmitter where multiple independent transmission paths converge.</div>
          </div>
          <div class="card card-emerald">
            <div class="card-icon">🔍</div>
            <div class="card-title">Defect Detection</div>
            <div class="card-desc">Flags missing chronological links (inqiṭāʿ), potential anachronisms, and tadlīs disclosures.</div>
          </div>
        </div>
        """
    },
    {
        "id": 10,
        "tag": "SLIDE 10 · HISTORICAL GEOGRAPHY",
        "title": "Geography & Transmission: Geographic Dispersion",
        "category": "Geography",
        "time": "1.5 min",
        "citation": "Historical Spatial Database · Regional Hadith Centers",
        "notes": "Hadith transmission was a physical, geographic journey across the classical Islamic world. Mīzān models the spatial movement of hadith—from Medina and Mecca through Kufa, Basra, Damascus, Baghdad, and into Khurasan and Central Asia.",
        "html": """
        <div class="slide-header">
          <span class="slide-kicker">Spatial Provenance</span>
          <h2 class="slide-title">Where did this transmission travel?</h2>
          <p class="slide-subtitle">Tracing the geographic movement of hadith across the major intellectual centers of Islam.</p>
        </div>
        <div class="card" style="padding: 1.5rem; margin-top: 1.5rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; text-align: center;">
            <div style="flex: 1; min-width: 140px; padding: 1rem; background: var(--green-soft); border-radius: 0.5rem;">
              <div style="font-weight: 700; color: var(--green-deep);">1. Medina / Mecca</div>
              <div style="font-size: 0.85rem; color: var(--green-light); margin-top: 0.25rem;">Prophetic Era &amp; Early Companions</div>
            </div>
            <div style="color: var(--gold-primary); font-size: 1.5rem;">➔</div>
            <div style="flex: 1; min-width: 140px; padding: 1rem; background: var(--gold-soft); border-radius: 0.5rem;">
              <div style="font-weight: 700; color: var(--gold-dark);">2. Kufa &amp; Basra</div>
              <div style="font-size: 0.85rem; color: var(--gold-primary); margin-top: 0.25rem;">Successors &amp; Regional Centers</div>
            </div>
            <div style="color: var(--gold-primary); font-size: 1.5rem;">➔</div>
            <div style="flex: 1; min-width: 140px; padding: 1rem; background: var(--green-soft); border-radius: 0.5rem;">
              <div style="font-weight: 700; color: var(--green-deep);">3. Baghdad</div>
              <div style="font-size: 0.85rem; color: var(--green-light); margin-top: 0.25rem;">Scholarly Synthesis &amp; Jurists</div>
            </div>
            <div style="color: var(--gold-primary); font-size: 1.5rem;">➔</div>
            <div style="flex: 1; min-width: 140px; padding: 1rem; background: var(--gold-soft); border-radius: 0.5rem;">
              <div style="font-weight: 700; color: var(--gold-dark);">4. Bukhara / Nishapur</div>
              <div style="font-size: 0.85rem; color: var(--gold-primary); margin-top: 0.25rem;">Canonical Compilation</div>
            </div>
          </div>
          <div style="margin-top: 1.25rem; font-size: 0.9rem; color: var(--ink-muted); text-align: center;">
            Spatial data is linked directly to narrator biographical records, allowing researchers to visualize geographical spread across generations.
          </div>
        </div>
        """
    },
    {
        "id": 11,
        "tag": "SLIDE 11 · TEXTUAL CRITICISM",
        "title": "Matn Comparison: Wording Variants",
        "category": "Matn",
        "time": "1.5 min",
        "citation": "Matn Difference Engine · Lexical Alignment Algorithm",
        "notes": "In hadith textual criticism, analyzing slight wording additions or omissions (ziyādāt al-thiqāt) is crucial for evaluating authenticity. Mīzān's Matn Comparison engine displays word-level differences side-by-side with color-coded additions, omissions, and lexical variants.",
        "html": """
        <div class="slide-header">
          <span class="slide-kicker">Textual Comparison</span>
          <h2 class="slide-title">Compare the wording — not just the translation.</h2>
          <p class="slide-subtitle">Highlighting shared wording, subtle additions, omissions, and lexical substitutions.</p>
        </div>
        <div class="grid-2" style="margin-top: 1.5rem;">
          <div class="card">
            <div class="card-title" style="color: var(--green-primary); font-size: 1.1rem; margin-bottom: 0.75rem;">Transmission A: Bukhari #1</div>
            <div style="background: var(--surface-cream); padding: 1rem; border-radius: 0.5rem; font-family: var(--font-serif); font-size: 1.2rem; line-height: 2; direction: rtl; text-align: right;">
              «إِنَّمَا الأَعْمَالُ <span style="background: #bbf7d0; padding: 0 4px; border-radius: 2px;">بِالنِّيَّاتِ</span>، وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى...»
            </div>
            <div style="font-size: 0.85rem; color: var(--ink-muted); margin-top: 0.75rem;">Standard plural form (بِالنِّيَّاتِ) found in Bukhari and Muslim.</div>
          </div>
          <div class="card card-gold">
            <div class="card-title" style="color: var(--gold-dark); font-size: 1.1rem; margin-bottom: 0.75rem;">Transmission B: Lexical Variant</div>
            <div style="background: #ffffff; padding: 1rem; border-radius: 0.5rem; font-family: var(--font-serif); font-size: 1.2rem; line-height: 2; direction: rtl; text-align: right; border: 1px solid var(--gold-border);">
              «إِنَّمَا الأَعْمَالُ <span style="background: #fed7aa; padding: 0 4px; border-radius: 2px;">بِالنِّيَّةِ</span>، وَإِنَّمَا لِامْرِئٍ مَا نَوَى...»
            </div>
            <div style="font-size: 0.85rem; color: var(--ink-muted); margin-top: 0.75rem;">Singular lexical variant (بِالنِّيَّةِ) documented in variant chains.</div>
          </div>
        </div>
        """
    },
    {
        "id": 12,
        "tag": "SLIDE 12 · EXPLANATORY CONTEXT",
        "title": "Commentary: Exact Relational Linking",
        "category": "Commentary",
        "time": "1.5 min",
        "citation": "Phase 12 Commentary Audit · hadith_commentaries.db",
        "notes": "Attaching classical commentaries to hadith is notoriously error-prone when done blindly. Mīzān's Phase 12 audit verified 1,202 commentary records across 1,203 links. As demonstrated in Record #428, commentary can link to Hadith 12427 as primary and 12428 as secondary, while rigorously excluding neighboring Hadith 12426.",
        "html": """
        <div class="slide-header">
          <span class="slide-kicker">Relational Sharḥ Integration</span>
          <h2 class="slide-title">Connect the hadith to its scholarly commentary.</h2>
          <p class="slide-subtitle">Precision linking ensures commentaries are attached only to the exact narrations they explain.</p>
        </div>
        <div class="grid-3" style="margin-top: 1.5rem;">
          <div class="card card-emerald">
            <div style="font-size: 2rem; font-weight: 700; color: var(--green-primary); font-family: var(--font-display);">1,202</div>
            <div style="font-weight: 600; color: var(--green-deep); margin-top: 0.25rem;">Commentary Records</div>
            <p style="font-size: 0.85rem; color: var(--ink-body); margin-top: 0.5rem;">Classical explanations with explicit boundary and author attributions.</p>
          </div>
          <div class="card card-gold">
            <div style="font-size: 2rem; font-weight: 700; color: var(--gold-primary); font-family: var(--font-display);">1,203</div>
            <div style="font-weight: 600; color: var(--gold-dark); margin-top: 0.25rem;">Explicit Links</div>
            <p style="font-size: 0.85rem; color: var(--ink-body); margin-top: 0.5rem;">Deterministic mappings between commentary units and canonical hadiths.</p>
          </div>
          <div class="card">
            <div style="font-size: 2rem; font-weight: 700; color: var(--green-primary); font-family: var(--font-display);">Record #428</div>
            <div style="font-weight: 600; color: var(--ink-primary); margin-top: 0.25rem;">Scope Verification</div>
            <p style="font-size: 0.85rem; color: var(--ink-body); margin-top: 0.5rem;">Hadith 12427 (Primary), 12428 (Secondary), 12426 (Zero link - protected).</p>
          </div>
        </div>
        """
    },
    {
        "id": 13,
        "tag": "SLIDE 13 · AI & RAG ARCHITECTURE",
        "title": "Ask Mīzān: Evidence-Grounded AI",
        "category": "AI/RAG",
        "time": "1.5 min",
        "citation": "Ask Mīzān RAG Architecture · Retrieval-Augmented Synthesis",
        "notes": "Ask Mīzān is not a free-form chatbot that hallucinates citations. It employs a strict Retrieval-Augmented Generation pipeline. When a user asks a research question, Mīzān retrieves verified records, constructs an evidence pack, and constrains the AI to answer solely from that evidence with clickable citations.",
        "html": """
        <div class="slide-header">
          <span class="slide-kicker">Grounded Synthesis</span>
          <h2 class="slide-title">AI that starts with evidence.</h2>
          <p class="slide-subtitle">The AI is not the source. The underlying verified evidence is.</p>
        </div>
        <div class="card" style="padding: 1.75rem; margin-top: 1.5rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem; text-align: center;">
            <div style="flex: 1; min-width: 140px; padding: 1rem; background: var(--green-soft); border-radius: 0.5rem;">
              <div style="font-weight: 700; color: var(--green-deep);">1. Research Query</div>
              <div style="font-size: 0.8rem; color: var(--green-light); margin-top: 0.25rem;">Academic prompt or hadith concept</div>
            </div>
            <div style="color: var(--gold-primary); font-size: 1.25rem;">➔</div>
            <div style="flex: 1; min-width: 140px; padding: 1rem; background: var(--gold-soft); border-radius: 0.5rem;">
              <div style="font-weight: 700; color: var(--gold-dark);">2. Hybrid Retrieval</div>
              <div style="font-size: 0.8rem; color: var(--gold-primary); margin-top: 0.25rem;">Canonical DB + semantic vector search</div>
            </div>
            <div style="color: var(--gold-primary); font-size: 1.25rem;">➔</div>
            <div style="flex: 1; min-width: 140px; padding: 1rem; background: var(--green-soft); border-radius: 0.5rem;">
              <div style="font-weight: 700; color: var(--green-deep);">3. Evidence Pack</div>
              <div style="font-size: 0.8rem; color: var(--green-light); margin-top: 0.25rem;">Cryptographically verified records</div>
            </div>
            <div style="color: var(--gold-primary); font-size: 1.25rem;">➔</div>
            <div style="flex: 1; min-width: 140px; padding: 1rem; background: var(--gold-soft); border-radius: 0.5rem;">
              <div style="font-weight: 700; color: var(--gold-dark);">4. Cited Synthesis</div>
              <div style="font-size: 0.8rem; color: var(--gold-primary); margin-top: 0.25rem;">Grounded response with source citations</div>
            </div>
          </div>
          <div style="margin-top: 1.5rem; padding: 1rem; background: var(--surface-cream); border-radius: 0.25rem; font-size: 0.9rem; color: var(--ink-body);">
            <strong>Anti-Hallucination Policy:</strong> If the retrieved evidence pack does not contain sufficient textual support to answer an inquiry, Ask Mīzān explicitly replies: <em>"The verified corpus does not contain sufficient textual evidence to confirm this claim."</em>
          </div>
        </div>
        """
    },
    {
        "id": 14,
        "tag": "SLIDE 14 · FORENSIC VALIDATION",
        "title": "Trust & Forensic Validation: 18 Audit Phases",
        "category": "Validation",
        "time": "1.5 min",
        "citation": "Validation Phases 01–18 Summary · Certified Machine Logs",
        "notes": "How do we know the system is reliable? Because it underwent 18 distinct audit phases. We verified that canonical databases cannot be mutated, cryptographic SHA-256 hashes match across environments, and fail-closed quarantine prevents invalid data from leaking.",
        "html": """
        <div class="slide-header">
          <span class="slide-kicker">Empirical Accountability</span>
          <h2 class="slide-title">How do we know the system is reliable?</h2>
          <p class="slide-subtitle">18 comprehensive validation phases testing integrity, boundaries, and adversarial conditions.</p>
        </div>
        <div class="grid-4" style="margin-top: 1.5rem;">
          <div class="card card-emerald">
            <div class="card-icon">🔒</div>
            <div class="card-title">Zero Mutations</div>
            <div class="card-desc">All canonical SQLite databases are read-only; zero records can be altered by user queries or frontend actions.</div>
          </div>
          <div class="card card-gold">
            <div class="card-icon">🔑</div>
            <div class="card-title">SHA-256 Hashes</div>
            <div class="card-desc">Every database file possesses cryptographic hashes verified automatically prior to test execution.</div>
          </div>
          <div class="card card-emerald">
            <div class="card-icon">🛑</div>
            <div class="card-title">Quarantine Defense</div>
            <div class="card-desc">Fail-closed mechanisms quarantine questionable records and verify zero quarantine leaks.</div>
          </div>
          <div class="card card-gold">
            <div class="card-icon">🛡️</div>
            <div class="card-title">Security Audited</div>
            <div class="card-desc">Hardened against SQL injections, prototype pollution, path traversals, and unauthorized API mutations.</div>
          </div>
        </div>
        """
    },
    {
        "id": 15,
        "tag": "SLIDE 15 · AUDIT CERTIFICATION",
        "title": "Zero-Trust Result: Phase 18 Final Audit",
        "category": "Audit",
        "time": "1.5 min",
        "citation": "Phase 18 Master Validation Audit · Unconditional Decision: GO",
        "notes": "In Phase 18, an adversarial zero-trust audit was executed across 35 machine acceptance gates. Across 5.96 million entities and relationships, exactly zero quarantine escapes occurred, and zero critical, high, medium, or low defects were found. The system received an unconditional GO.",
        "html": """
        <div class="slide-header">
          <span class="slide-kicker">Phase 18 Certification</span>
          <h2 class="slide-title">The system was tested as if it could fail.</h2>
          <p class="slide-subtitle">Adversarial audit completed with zero defects and zero quarantine escapes.</p>
        </div>
        <div class="grid-4" style="margin-top: 1.5rem;">
          <div class="card" style="text-align: center; padding: 1.5rem; border-top: 4px solid var(--green-primary);">
            <div style="font-size: 2.25rem; font-weight: 700; color: var(--green-primary); font-family: var(--font-display);">35 / 35</div>
            <div style="font-weight: 600; margin-top: 0.25rem;">Machine Gates Passed</div>
            <div style="font-size: 0.8rem; color: var(--ink-muted); margin-top: 0.25rem;">100% automated test compliance</div>
          </div>
          <div class="card" style="text-align: center; padding: 1.5rem; border-top: 4px solid var(--gold-primary);">
            <div style="font-size: 2.25rem; font-weight: 700; color: var(--gold-primary); font-family: var(--font-display);">5.96M+</div>
            <div style="font-weight: 600; margin-top: 0.25rem;">Entities &amp; Relations</div>
            <div style="font-size: 0.8rem; color: var(--ink-muted); margin-top: 0.25rem;">Total verified data volume</div>
          </div>
          <div class="card" style="text-align: center; padding: 1.5rem; border-top: 4px solid var(--green-primary);">
            <div style="font-size: 2.25rem; font-weight: 700; color: var(--green-primary); font-family: var(--font-display);">0</div>
            <div style="font-weight: 600; margin-top: 0.25rem;">Quarantine Escapes</div>
            <div style="font-size: 0.8rem; color: var(--ink-muted); margin-top: 0.25rem;">Strict quarantine boundary held</div>
          </div>
          <div class="card" style="text-align: center; padding: 1.5rem; border-top: 4px solid var(--gold-primary);">
            <div style="font-size: 2.25rem; font-weight: 700; color: var(--gold-primary); font-family: var(--font-display);">GO</div>
            <div style="font-weight: 600; margin-top: 0.25rem;">Final Audit Decision</div>
            <div style="font-size: 0.8rem; color: var(--ink-muted); margin-top: 0.25rem;">Unconditional production release</div>
          </div>
        </div>
        """
    },
    {
        "id": 16,
        "tag": "SLIDE 16 · WORKING SYSTEM",
        "title": "What Has Already Been Built: Functional Modules",
        "category": "Built",
        "time": "1.5 min",
        "citation": "Production Build Status · Frontend & Backend Implementation",
        "notes": "Mīzān is not just an idea or a slide deck. All core research capabilities have been implemented in functional software, including full-text search, hadith reader, isnād visualizer, multi-scholar grading matrix, relational commentary, and Ask Mīzān.",
        "html": """
        <div class="slide-header">
          <span class="slide-kicker">Concrete Reality</span>
          <h2 class="slide-title">This is not just a concept.</h2>
          <p class="slide-subtitle">A fully functional, high-performance research platform running on modern web architecture.</p>
        </div>
        <div class="grid-3" style="margin-top: 1.5rem;">
          <div class="card card-emerald">
            <div class="card-icon">⚡</div>
            <div class="card-title">Full-Text Search</div>
            <div class="card-desc">Sub-second Arabic root, stem, and fuzzy search across 715,790 hadiths and all collections.</div>
          </div>
          <div class="card card-gold">
            <div class="card-icon">📖</div>
            <div class="card-title">Canonical Reader</div>
            <div class="card-desc">Fully vocalized Arabic display with side-by-side English translations and cross-edition numbering.</div>
          </div>
          <div class="card card-emerald">
            <div class="card-icon">🕸️</div>
            <div class="card-title">Transmission Visualizer</div>
            <div class="card-desc">Interactive canvas and graph rendering of transmission networks with narrator biographical overlays.</div>
          </div>
          <div class="card card-gold">
            <div class="card-icon">⚖️</div>
            <div class="card-title">Grading Matrix</div>
            <div class="card-desc">Nine-scholar comparative evaluation display showing consensus, differences, and specific rulings.</div>
          </div>
          <div class="card card-emerald">
            <div class="card-icon">💬</div>
            <div class="card-title">Relational Sharḥ</div>
            <div class="card-desc">Commentary engine linking specific hadiths to classical explanations with verified boundary scopes.</div>
          </div>
          <div class="card card-gold">
            <div class="card-icon">🤖</div>
            <div class="card-title">Ask Mīzān (RAG)</div>
            <div class="card-desc">Evidence-grounded conversational research assistant powered by verified database context.</div>
          </div>
        </div>
        """
    },
    {
        "id": 17,
        "tag": "SLIDE 17 · TRANSPARENT ROADMAP",
        "title": "What is Still Growing: Current vs Next",
        "category": "Roadmap",
        "time": "1.5 min",
        "citation": "Development Roadmap · Strategic Milestone Planning",
        "notes": "We believe in complete scholarly transparency. Mīzān is functional and certified today, but hadith scholarship is vast. We clearly separate what is completed right now from what is slated for subsequent research phases.",
        "html": """
        <div class="slide-header">
          <span class="slide-kicker">Honest Growth Path</span>
          <h2 class="slide-title">Mīzān is already usable — but the work is not finished.</h2>
          <p class="slide-subtitle">Distinguishing current certified deliverables from ongoing expansion initiatives.</p>
        </div>
        <div class="grid-2" style="margin-top: 1.5rem;">
          <div class="card card-emerald">
            <div class="card-title" style="color: var(--green-primary); font-size: 1.15rem; margin-bottom: 0.75rem;">CURRENT (Built &amp; Certified)</div>
            <ul style="list-style: none; padding-left: 0; font-size: 0.9rem; line-height: 1.8;">
              <li>✔ Canonical Six Collections &amp; 425 secondary works fully indexed</li>
              <li>✔ 49,844 verified narrator biographical profiles</li>
              <li>✔ Cross-edition numbering harmonization across major printings</li>
              <li>✔ Nine-scholar evaluation registry with 65,420 judgments</li>
              <li>✔ Phase 12 relational commentary prototype (1,202 records)</li>
              <li>✔ Evidence-bounded Ask Mīzān RAG pipeline</li>
            </ul>
          </div>
          <div class="card card-gold">
            <div class="card-title" style="color: var(--gold-dark); font-size: 1.15rem; margin-bottom: 0.75rem;">NEXT (In Development &amp; Planned)</div>
            <ul style="list-style: none; padding-left: 0; font-size: 0.9rem; line-height: 1.8;">
              <li>⏳ Expanding commentary coverage across complete classical compendia</li>
              <li>⏳ High-resolution physical manuscript facsimile alignment</li>
              <li>⏳ Morphological Arabic NLP parsing and semantic relation tagging</li>
              <li>⏳ Direct integration with academic citation and export formats</li>
              <li>⏳ Expanded biographical coverage for obscure early transmitters</li>
              <li>⏳ Institutional multi-user collaborative workspace</li>
            </ul>
          </div>
        </div>
        """
    },
    {
        "id": 18,
        "tag": "SLIDE 18 · LONG-TERM VISION",
        "title": "The Long-Term Vision: Digital Research Infrastructure",
        "category": "Vision",
        "time": "1.5 min",
        "citation": "Digital Humanities Strategic Framework · Long-Term Vision",
        "notes": "Our long-term goal is to build an open, enduring research infrastructure for the entire discipline of Islamic Studies. By combining strict fidelity to classical principles with modern computational tools, Mīzān can serve as the foundational research workbench for scholars worldwide.",
        "html": """
        <div class="slide-header">
          <span class="slide-kicker">Disciplinary Transformation</span>
          <h2 class="slide-title">From a database to a research infrastructure.</h2>
          <p class="slide-subtitle">Preserving classical scholarly provenance while empowering the next century of digital humanities.</p>
        </div>
        <div class="grid-3" style="margin-top: 1.5rem;">
          <div class="card card-emerald">
            <div class="card-icon">🏛️</div>
            <div class="card-title">Scholarly Preservation</div>
            <div class="card-desc">Safeguards classical textual traditions and nuanced critical methodologies in standardized digital form.</div>
          </div>
          <div class="card card-gold">
            <div class="card-icon">🔬</div>
            <div class="card-title">Computational Research</div>
            <div class="card-desc">Enables macro-level analysis of transmission networks, lexical evolution, and geographical dissemination.</div>
          </div>
          <div class="card card-emerald">
            <div class="card-icon">🌐</div>
            <div class="card-title">Global Academic Access</div>
            <div class="card-desc">Democratizes access to primary sources, cross-edition references, and commentaries for scholars worldwide.</div>
          </div>
        </div>
        """
    },
    {
        "id": 19,
        "tag": "SLIDE 19 · ACADEMIC VALUE",
        "title": "Why This Matters: Impact on Islamic Studies",
        "category": "Impact",
        "time": "1.5 min",
        "citation": "Academic Value Assessment · Digital Humanities Methodologies",
        "notes": "Why does this matter for a university professor or funding institution? Because it transforms months of tedious manual cross-referencing into minutes of verified analysis, while creating an open foundation for collaborative research and pedagogical excellence.",
        "html": """
        <div class="slide-header">
          <span class="slide-kicker">Scholarly Value Proposition</span>
          <h2 class="slide-title">Why could this matter for Islamic Studies?</h2>
          <p class="slide-subtitle">Accelerating research, illuminating transmission networks, and setting a standard for digital humanities.</p>
        </div>
        <div class="grid-4" style="margin-top: 1.5rem;">
          <div class="card card-emerald">
            <div class="card-icon">⏱️</div>
            <div class="card-title">Accelerates Research</div>
            <div class="card-desc">Tasks requiring weeks in library stacks—tracing isnād variants or cross-referencing editions—take seconds.</div>
          </div>
          <div class="card card-gold">
            <div class="card-icon">📊</div>
            <div class="card-title">Novel Methodologies</div>
            <div class="card-desc">Enables network analysis, chronological mapping, and lexical variant tracking across millions of data points.</div>
          </div>
          <div class="card card-emerald">
            <div class="card-icon">🎓</div>
            <div class="card-title">Pedagogical Power</div>
            <div class="card-desc">Provides students with intuitive, visual mental models of complex hadith sciences and isnād structures.</div>
          </div>
          <div class="card card-gold">
            <div class="card-icon">🤝</div>
            <div class="card-title">Scholarly Transparency</div>
            <div class="card-desc">Every claim, grade, and text is traceable to physical print volumes with zero AI guesswork.</div>
          </div>
        </div>
        """
    },
    {
        "id": 20,
        "tag": "SLIDE 20 · CALL TO ACTION",
        "title": "Closing: Let's Build the Next Stage Together",
        "category": "Closing",
        "time": "1.5 min",
        "citation": "Mīzān al-Ḥadīth Project Initiative · Academic Partnership",
        "notes": "Professor Syed, colleagues, and supporters: Mīzān al-Ḥadīth was built to serve researchers like you. We have proved that computational digital humanities can be executed with absolute fidelity to classical Islamic scholarship. But to realize its full potential requires institutional partnership and sustained philanthropic support. We invite you to join us in establishing Mīzān as an enduring foundation for Islamic studies.",
        "html": """
        <div class="title-folio-wrap" style="text-align: center;">
          <div class="arabic-display-title" dir="rtl" style="font-size: 3rem;">مِيزَانُ الحَدِيث</div>
          <h1 class="main-display-title" style="font-size: 2.75rem;">MĪZĀN AL-ḤADĪTH</h1>
          <div class="title-divider" style="margin: 1rem auto;"></div>
          <p style="font-size: 1.15rem; color: var(--gold-dark); font-family: var(--font-serif); font-style: italic; max-width: 44rem; margin: 0 auto;">
            "Preserving the evidence. Connecting the scholarship. Making hadith research easier to explore."
          </p>

          <div class="grid-2" style="max-width: 46rem; margin: 1.75rem auto 1.25rem; text-align: left;">
            <div class="card card-emerald">
              <div style="font-weight: 700; color: var(--green-primary); font-size: 1rem; margin-bottom: 0.5rem;">Current Accomplishment</div>
              <p style="font-size: 0.85rem; color: var(--ink-body); line-height: 1.6;">
                Built, rigorously tested, and certified across 18 audit phases with 35 machine acceptance gates and zero critical defects.
              </p>
            </div>
            <div class="card card-gold">
              <div style="font-weight: 700; color: var(--gold-dark); font-size: 1rem; margin-bottom: 0.5rem;">Next Stage Collaboration</div>
              <p style="font-size: 0.85rem; color: var(--ink-body); line-height: 1.6;">
                Academic partnership, faculty advisory guidance, manuscript integration, and institutional endowment support.
              </p>
            </div>
          </div>

          <div style="margin-top: 1.5rem; font-size: 0.85rem; color: var(--ink-muted);">
            Repository / public release: not yet published &nbsp;·&nbsp; Prepared for Academic Review &nbsp;·&nbsp; October 2026
          </div>
        </div>
        """
    }
]

def build_index_html():
    slides_html_list = []
    for s in SLIDES_DATA:
        active_cls = " active" if s["id"] == 1 else ""
        slide_block = f"""
    <!-- SLIDE {s["id"]:02d}: {s["title"].upper()} -->
    <section class="slide{active_cls}" id="slide-{s["id"]}"
      data-title="{s["title"]}"
      data-tag="{s["tag"]}"
      data-category="{s["category"]}"
      data-time="{s["time"]}"
      data-citation="{s["citation"]}"
      data-notes="{s["notes"]}">
      {s["html"]}
    </section>"""
        slides_html_list.append(slide_block)

    full_slides_content = "\n".join(slides_html_list)

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MĪZĀN AL-ḤADĪTH — Presentation 01 (Academic &amp; Institutional Overview)</title>
  <link rel="stylesheet" href="presentation.css">
</head>
<body>
  <!-- Ambient Background Canvas -->
  <div class="ambient-bg"></div>

  <!-- DECK TOP HEADER -->
  <header class="deck-header">
    <div class="brand-badge">
      <div class="brand-icon">م</div>
      <span class="brand-title">MĪZĀN AL-ḤADĪTH</span>
      <span class="slide-tag" id="slideTag">SLIDE 01 · INSTITUTIONAL INTRODUCTION</span>
    </div>

    <!-- Center Progress Dots -->
    <div class="progress-dots" id="progressDots"></div>

    <!-- Controls -->
    <div class="deck-controls">
      <div class="timer-pill" title="Click to pause/resume timer">
        <span class="timer-dot"></span>
        <span id="timerDisplay">00:00</span>
      </div>
      <button class="btn-ctrl" id="btnNotes" title="Speaker Notes [N]">Notes</button>
      <button class="btn-ctrl" id="btnOverview" title="Slide Overview [O]">Grid</button>
      <button class="btn-ctrl" id="btnFullscreen" title="Toggle Fullscreen [F]">⤢</button>
    </div>
  </header>

  <!-- PRESENTATION STAGE -->
  <main class="stage" id="slideStage">
{full_slides_content}
  </main>

  <!-- DECK BOTTOM FOOTER -->
  <footer class="deck-footer">
    <div class="footer-citation" id="footerCitation">Source: Phase 18 Certified Release Baseline · October 2026</div>
    <div class="footer-nav">
      <button class="btn-nav" id="btnPrev" title="Previous Slide [Left Arrow]" disabled>← Prev</button>
      <span class="slide-counter" id="slideCounter">01 / 20</span>
      <button class="btn-nav" id="btnNext" title="Next Slide [Right Arrow, Space]">Next →</button>
    </div>
  </footer>

  <!-- SPEAKER NOTES DRAWER -->
  <aside class="speaker-notes-drawer" id="notesDrawer">
    <div class="notes-header">
      <div class="notes-title">SPEAKER SCRIPT &amp; ACADEMIC RATIONALE</div>
      <div class="notes-time" id="notesTime">Est: 1.5 min</div>
    </div>
    <div class="notes-content" id="notesContent">
      "Good morning, Professor Syed and colleagues. Today, we are presenting Mīzān al-Ḥadīth. For centuries, Islamic scholars have engaged in some of the most rigorous historical-critical analysis in human civilization..."
    </div>
  </aside>

  <!-- SLIDE OVERVIEW MODAL -->
  <div class="overview-modal" id="overviewModal">
    <div class="overview-panel">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--line-soft); padding-bottom: 0.75rem;">
        <h3 style="font-family: var(--font-display); font-size: 1.125rem; color: var(--green-deep);">Slide Directory (20 Folios)</h3>
        <span style="font-size: 0.8rem; color: var(--ink-muted);">Press [ESC] or [O] to Close</span>
      </div>
      <div class="overview-grid" id="overviewGrid"></div>
    </div>
  </div>

  <script src="presentation.js"></script>
</body>
</html>"""

    html_path = os.path.abspath("presentation/presentation_01/index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"Standalone HTML presentation updated: {html_path}")
    return html_path

def update_css_for_print():
    css_path = os.path.abspath("presentation/presentation_01/presentation.css")
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()

    # Strip existing @media print block if present
    if "/* PRINT & PDF EXPORT STYLES" in css:
        css = css.split("/* PRINT & PDF EXPORT STYLES")[0].rstrip()
    elif "@media print" in css:
        css = css.split("@media print")[0].rstrip()

    print_rules = """

/* PRINT & PDF EXPORT STYLES (16:9 Widescreen Landscape) */
@media print {
  @page {
    size: 16in 9in;
    margin: 0;
  }
  
  *, *:before, *:after {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
  
  html, body {
    width: 16in !important;
    height: auto !important;
    background: #f8f4ec !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: visible !important;
    font-size: 16px !important;
  }
  
  .ambient-bg,
  .deck-header,
  .deck-footer,
  .speaker-notes-drawer,
  .overview-modal,
  .deck-controls {
    display: none !important;
  }
  
  .stage {
    display: block !important;
    width: 16in !important;
    height: auto !important;
    padding: 0 !important;
    margin: 0 !important;
    overflow: visible !important;
  }
  
  .slide {
    display: flex !important;
    opacity: 1 !important;
    visibility: visible !important;
    transform: none !important;
    flex-direction: column !important;
    justify-content: center !important;
    width: 16in !important;
    height: 8.98in !important;
    max-height: 8.98in !important;
    box-sizing: border-box !important;
    padding: 0.5in 0.8in !important;
    background: #f8f4ec !important;
    page-break-after: always !important;
    break-after: page !important;
    overflow: hidden !important;
    position: relative !important;
  }
  
  .slide:last-child,
  .slide:last-of-type,
  #slide-20 {
    page-break-after: avoid !important;
    break-after: avoid !important;
  }
  
  .slide-title {
    font-size: 2.25rem !important;
  }
  
  .main-display-title {
    font-size: 3.5rem !important;
  }
  
  .arabic-display-title {
    font-size: 4rem !important;
  }
  
  .card {
    box-shadow: none !important;
    border: 1px solid #dcc8a4 !important;
  }
}
"""
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css + "\n" + print_rules)
    print("Cleanly updated presentation.css with print media rules.")

def generate_pdf(html_path):
    edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge_exe):
        edge_exe = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    
    if not os.path.exists(edge_exe):
        print(f"Edge executable not found at standard locations.")
        return None

    pdf_out = os.path.abspath("Mizan_al_Hadith_Introduction_Presentation.pdf")
    html_url = f"file:///{html_path.replace(os.sep, '/')}"
    
    cmd = [
        edge_exe,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={pdf_out}",
        html_url
    ]
    
    print(f"Generating PDF via Edge headless: {pdf_out}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(pdf_out):
        size_kb = os.path.getsize(pdf_out) / 1024
        print(f"PDF Successfully Generated: {pdf_out} ({size_kb:.1f} KB)")
        return pdf_out
    else:
        print(f"Failed to generate PDF: {res.stderr}")
        return None

if __name__ == "__main__":
    html_path = build_index_html()
    update_css_for_print()
    generate_pdf(html_path)
