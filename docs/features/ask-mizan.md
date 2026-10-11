# FEATURE — ASK MĪZĀN (GROUNDED AI RESEARCH ASSISTANT)

**Document Identifier:** `docs/features/ask-mizan.md`  
**Frontend Route:** `/ask`  
**Backend Endpoints:** `/api/ask`, `/api/ask/stream`, `/api/ask/conversations/{id}`, `/api/ask/feedback`  

---

## 1. Overview & Scholarly Objective

Ask Mīzān ("اسأل ميزان") is an evidence-grounded AI research assistant designed specifically for Islamic studies scholars.

Unlike generic conversational models that freely hallucinate narrations or fabricate biographical judgments, Ask Mīzān operates under a **Strict Grounding Protocol**:
- Every response is constructed exclusively from canonical hadith records, verified commentary excerpts, and biographical dictionaries retrieved for that specific query.
- If the canonical corpus contains insufficient evidence, the system refuses to answer rather than speculating.
- Citations are validated deterministically after generation.

---

## 2. Supported Inquiries & Interaction Modes

1. **Exact Narration Inquiries:**
   - *"Show me hadith 1 of Sahih al-Bukhari."*
   - *"What is hadith 1986 in Sunan Ibn Majah?"*
2. **Biographical Narrator Inquiries:**
   - *"Tell me about the narrator Sufyan al-Thawri."*
   - *"What are the classical opinions on Abdur Rahman al-Musalli?"*
3. **Classical Commentary & Thematic Inquiries:**
   - *"What did Ibn Hajar say in Fath al-Bari regarding the intention hadith?"*
   - *"Explain the rulings mentioned by Imam al-Tirmidhi in chapter 1."*
4. **Textual Variant & Cross-Collection Comparisons:**
   - *"How does the matn of Bukhari 1 compare to Muslim 1907?"*

---

## 3. The Grounding Architecture & Citation Guard

```
               [ User Natural Language Query ]
                              |
                              v
                 [ Intent & Entity Parser ]
                              |
                              v
                [ Multi-Tier Evidence Pack ]
                 - Canonical Matn & Sanad
                 - Jarh wa Ta'dil Judgments
                 - Classical Commentary Links
                              |
                              v
               [ Sufficient Evidence Check ]
                 /                         \
           YES  /                           \  NO
               v                             v
   [ Prompt Assembly & LLM ]          [ Structured Refusal ]
               |
               v
  [ Citation Anti-Hallucination Guard ]
   - Validate citations against Pack
   - Strip ungrounded references
               |
               v
  [ Verified Answer with Citation Chips ]
```

---

## 4. Grounding Evaluation & Benchmarks

In automated evaluations conducted across stratified benchmark queries (`scripts/test_ask_mizan_suite.py` and `scripts/test_critical_fixes_sprint.py`):
- **Intent Routing Accuracy:** `100%` (Exact references, narrator queries, and intentions variants routed to dedicated handlers).
- **Hallucinated Citation Admissions:** `0%` (Zero hallucinated citations admitted into final answers).
- **Collision Guard Triggering:** `100%` (Yahya ibn Ma'in statement for Abdur Rahman al-Musalli correctly flagged as `father_son_collision`).
- **Insufficient Evidence Handling:** Clean structured refusal issued without leaking prompt template markers.
