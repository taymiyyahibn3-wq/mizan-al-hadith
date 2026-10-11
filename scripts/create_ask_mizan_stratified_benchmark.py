"""
Constructs the stratified, 12-category Ask Mīzān benchmark dataset:
Categories A through L, 120 total test queries, evenly split into:
- 60 Development queries (DEV)
- 60 Held-out Evaluation queries (TEST)

Verified against canonical databases (hadith-kg.db, hadith_numbering.db, isnad_network.db,
citation_enrichment.db, classical_scholar_evidence.db, hadith_commentaries.db).
"""

import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = REPO_ROOT / "data" / "benchmarks" / "ask_mizan_stratified_benchmark_v1.jsonl"

BENCHMARK_ITEMS = [
    # =========================================================================
    # CATEGORY A: Exact Hadith References
    # =========================================================================
    {
        "id": "CAT_A_001",
        "split": "dev",
        "category": "Category A — Exact Hadith references",
        "query": "Sahih al-Bukhari 1",
        "language": "en",
        "expected_intent": "HADITH_LOOKUP",
        "expected_hadith_ids": [1],
        "expected_primary_id": 1,
        "notes": "Canonical Bukhari hadith #1, intention"
    },
    {
        "id": "CAT_A_002",
        "split": "dev",
        "category": "Category A — Exact Hadith references",
        "query": "Sahih Muslim 1907",
        "language": "en",
        "expected_intent": "HADITH_LOOKUP",
        "expected_hadith_ids": [8938],
        "expected_primary_id": 8938,
        "notes": "Canonical Muslim hadith #1907, parallel to Bukhari 1"
    },
    {
        "id": "CAT_A_003",
        "split": "dev",
        "category": "Category A — Exact Hadith references",
        "query": "Sunan an-Nasa'i Darussalam 348",
        "language": "en",
        "expected_intent": "NUMBERING",
        "expected_hadith_ids": [21260],
        "expected_primary_id": 21260,
        "notes": "Nasa'i Darussalam edition #348"
    },
    {
        "id": "CAT_A_004",
        "split": "dev",
        "category": "Category A — Exact Hadith references",
        "query": "Sunan Ibn Majah Darussalam 1986",
        "language": "en",
        "expected_intent": "NUMBERING",
        "expected_hadith_ids": [28581],
        "expected_primary_id": 28581,
        "notes": "Ibn Majah Darussalam edition #1986"
    },
    {
        "id": "CAT_A_005",
        "split": "dev",
        "category": "Category A — Exact Hadith references",
        "query": "صحيح البخاري رقم 8",
        "language": "ar",
        "expected_intent": "HADITH_LOOKUP",
        "expected_hadith_ids": [7],
        "expected_primary_id": 7,
        "notes": "Bukhari in-book #8 (Buni al-Islam)"
    },
    {
        "id": "CAT_A_006",
        "split": "test",
        "category": "Category A — Exact Hadith references",
        "query": "Jami at-Tirmidhi 1",
        "language": "en",
        "expected_intent": "HADITH_LOOKUP",
        "expected_hadith_ids": [12399],
        "expected_primary_id": 12399,
        "notes": "Tirmidhi hadith #1 (Taharah)"
    },
    {
        "id": "CAT_A_007",
        "split": "test",
        "category": "Category A — Exact Hadith references",
        "query": "Sunan Abi Dawud 1",
        "language": "en",
        "expected_intent": "HADITH_LOOKUP",
        "expected_hadith_ids": [16333],
        "expected_primary_id": 16333,
        "notes": "Abu Dawud hadith #1"
    },
    {
        "id": "CAT_A_008",
        "split": "test",
        "category": "Category A — Exact Hadith references",
        "query": "Muwatta Malik 1",
        "language": "en",
        "expected_intent": "HADITH_LOOKUP",
        "expected_hadith_ids": [32971],
        "expected_primary_id": 32971,
        "notes": "Muwatta Malik #1 (Prayer times)"
    },
    {
        "id": "CAT_A_009",
        "split": "test",
        "category": "Category A — Exact Hadith references",
        "query": "صحيح مسلم 1",
        "language": "ar",
        "expected_intent": "HADITH_LOOKUP",
        "expected_hadith_ids": [7032],
        "expected_primary_id": 7032,
        "notes": "Muslim hadith #1 (Muqaddimah / Iman)"
    },
    {
        "id": "CAT_A_010",
        "split": "test",
        "category": "Category A — Exact Hadith references",
        "query": "Sunan Ibn Majah 1",
        "language": "en",
        "expected_intent": "HADITH_LOOKUP",
        "expected_hadith_ids": [26600],
        "expected_primary_id": 26600,
        "notes": "Ibn Majah hadith #1 (Sunnah)"
    },

    # =========================================================================
    # CATEGORY B: Arabic Queries
    # =========================================================================
    {
        "id": "CAT_B_001",
        "split": "dev",
        "category": "Category B — Arabic queries",
        "query": "إِنَّمَا الْأَعْمَالُ بِالنِّيَّاتِ",
        "language": "ar",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [1],
        "expected_primary_id": 1,
        "notes": "Arabic query with full diacritics / tashkeel"
    },
    {
        "id": "CAT_B_002",
        "split": "dev",
        "category": "Category B — Arabic queries",
        "query": "طلب العلم فريضة على كل مسلم",
        "language": "ar",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [26823],
        "expected_primary_id": 26823,
        "notes": "Famous prophetic hadith on seeking knowledge"
    },
    {
        "id": "CAT_B_003",
        "split": "dev",
        "category": "Category B — Arabic queries",
        "query": "المسلم من سلم المسلمون من لسانه ويده",
        "language": "ar",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [9],
        "expected_primary_id": 9,
        "notes": "Bukhari #10 definition of Muslim"
    },
    {
        "id": "CAT_B_004",
        "split": "dev",
        "category": "Category B — Arabic queries",
        "query": "لا ضرر ولا ضرار في الإسلام",
        "language": "ar",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [28938],
        "expected_primary_id": 28938,
        "notes": "Legal maxim of harm"
    },
    {
        "id": "CAT_B_005",
        "split": "dev",
        "category": "Category B — Arabic queries",
        "query": "بني الاسلام علي خمس",
        "language": "ar",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [7],
        "expected_primary_id": 7,
        "notes": "Arabic with hamza/alif variations (علي vs على)"
    },
    {
        "id": "CAT_B_006",
        "split": "test",
        "category": "Category B — Arabic queries",
        "query": "الدين النصيحة قلنا لمن قال لله ولكتابه",
        "language": "ar",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [7116],
        "expected_primary_id": 7116,
        "notes": "Hadith of sincerity"
    },
    {
        "id": "CAT_B_007",
        "split": "test",
        "category": "Category B — Arabic queries",
        "query": "الحلال بين والحرام بين وبينهما مشبهات",
        "language": "ar",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [51],
        "expected_primary_id": 51,
        "notes": "Hadith of doubtful matters"
    },
    {
        "id": "CAT_B_008",
        "split": "test",
        "category": "Category B — Arabic queries",
        "query": "من غشنا فليس منا",
        "language": "ar",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [7180],
        "expected_primary_id": 7180,
        "notes": "Prohibition of cheating"
    },
    {
        "id": "CAT_B_009",
        "split": "test",
        "category": "Category B — Arabic queries",
        "query": "لا يؤمن أحدكم حتى يحب لأخيه ما يحب لنفسه",
        "language": "ar",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [12],
        "expected_primary_id": 12,
        "notes": "Brotherhood and love for believers"
    },
    {
        "id": "CAT_B_010",
        "split": "test",
        "category": "Category B — Arabic queries",
        "query": "كلمتان خفيفتان على اللسان ثقيلتان في الميزان",
        "language": "ar",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [6037],
        "expected_primary_id": 6037,
        "notes": "Virtue of Tasbih (Subhan Allah wa bihamdihi)"
    },

    # =========================================================================
    # CATEGORY C: Urdu Queries
    # =========================================================================
    {
        "id": "CAT_C_001",
        "split": "dev",
        "category": "Category C — Urdu queries",
        "query": "صحیح بخاری حدیث نمبر 1 کا متن اور ترجمہ",
        "language": "ur",
        "expected_intent": "HADITH_LOOKUP",
        "expected_hadith_ids": [1],
        "expected_primary_id": 1,
        "notes": "Urdu query referencing Bukhari hadith 1"
    },
    {
        "id": "CAT_C_002",
        "split": "dev",
        "category": "Category C — Urdu queries",
        "query": "اعمال کا دارومدار نیتوں پر ہے",
        "language": "ur",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [1],
        "expected_primary_id": 1,
        "notes": "Urdu famous paraphrase of Innamal A'mal"
    },
    {
        "id": "CAT_C_003",
        "split": "dev",
        "category": "Category C — Urdu queries",
        "query": "راوی ابو ہریرہ کے بارے میں بتائیں",
        "language": "ur",
        "expected_intent": "NARRATOR_LOOKUP",
        "expected_rawi_ids": [4396],
        "expected_primary_id": 4396,
        "notes": "Urdu query on narrator Abu Hurayrah"
    },
    {
        "id": "CAT_C_004",
        "split": "dev",
        "category": "Category C — Urdu queries",
        "query": "کیا حدیث انما الاعمال بالنیات صحیح ہے؟",
        "language": "ur",
        "expected_intent": "HADITH_GRADING",
        "expected_hadith_ids": [1],
        "expected_primary_id": 1,
        "notes": "Urdu grading question on Bukhari 1"
    },
    {
        "id": "CAT_C_005",
        "split": "dev",
        "category": "Category C — Urdu queries",
        "query": "سنن ابوداؤد حدیث 1",
        "language": "ur",
        "expected_intent": "HADITH_LOOKUP",
        "expected_hadith_ids": [16333],
        "expected_primary_id": 16333,
        "notes": "Urdu compound collection name Sunan Abu Dawud"
    },
    {
        "id": "CAT_C_006",
        "split": "test",
        "category": "Category C — Urdu queries",
        "query": "نماز کے اوقات کے متعلق احادیث",
        "language": "ur",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [499],
        "expected_primary_id": 499,
        "notes": "Urdu thematic question on prayer times"
    },
    {
        "id": "CAT_C_007",
        "split": "test",
        "category": "Category C — Urdu queries",
        "query": "حافظ زبیر علی زئی کی سنن نسائی پر تحقیق",
        "language": "ur",
        "expected_intent": "HADITH_GRADING",
        "expected_hadith_ids": [21260],
        "expected_primary_id": 21260,
        "notes": "Urdu question about Zubair Ali Zai tahqiq"
    },
    {
        "id": "CAT_C_008",
        "split": "test",
        "category": "Category C — Urdu queries",
        "query": "راوی عبدالرحمن المسلی کون ہیں؟",
        "language": "ur",
        "expected_intent": "NARRATOR_LOOKUP",
        "expected_rawi_ids": [4256],
        "expected_primary_id": 4256,
        "notes": "Urdu query on Abdur Rahman al-Musalli"
    },
    {
        "id": "CAT_C_009",
        "split": "test",
        "category": "Category C — Urdu queries",
        "query": "صحیح مسلم حدیث ۱۹۰۷",
        "language": "ur",
        "expected_intent": "HADITH_LOOKUP",
        "expected_hadith_ids": [8938],
        "expected_primary_id": 8938,
        "notes": "Urdu query with Urdu numerals (۱۹۰۷)"
    },
    {
        "id": "CAT_C_010",
        "split": "test",
        "category": "Category C — Urdu queries",
        "query": "والدین کی اطاعت اور حسن سلوک کے بارے میں حدیث",
        "language": "ur",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [5567],
        "expected_primary_id": 5567,
        "notes": "Urdu thematic on dutifulness to parents"
    },

    # =========================================================================
    # CATEGORY D: English Queries
    # =========================================================================
    {
        "id": "CAT_D_001",
        "split": "dev",
        "category": "Category D — English queries",
        "query": "Actions are judged by motives and intentions",
        "language": "en",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [1],
        "expected_primary_id": 1,
        "notes": "Conceptual paraphrase of intention hadith"
    },
    {
        "id": "CAT_D_002",
        "split": "dev",
        "category": "Category D — English queries",
        "query": "Show me the hadith about five pillars of Islam",
        "language": "en",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [7],
        "expected_primary_id": 7,
        "notes": "Five pillars in English"
    },
    {
        "id": "CAT_D_003",
        "split": "dev",
        "category": "Category D — English queries",
        "query": "Seeking knowledge is an obligation upon every Muslim",
        "language": "en",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [26823],
        "expected_primary_id": 26823,
        "notes": "Seeking knowledge hadith in Ibn Majah"
    },
    {
        "id": "CAT_D_004",
        "split": "dev",
        "category": "Category D — English queries",
        "query": "What is the ruling and hadith text of Bukhari 1?",
        "language": "en",
        "expected_intent": "HADITH_LOOKUP",
        "expected_hadith_ids": [1],
        "expected_primary_id": 1,
        "notes": "Direct reference lookup with text inquiry"
    },
    {
        "id": "CAT_D_005",
        "split": "dev",
        "category": "Category D — English queries",
        "query": "Hadiths concerning the virtues of patience during adversity",
        "language": "en",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [1400],
        "expected_primary_id": 1400,
        "notes": "Thematic on patience (Sabr)"
    },
    {
        "id": "CAT_D_006",
        "split": "test",
        "category": "Category D — English queries",
        "query": "The Muslim is the one from whose tongue and hand others are safe",
        "language": "en",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [9],
        "expected_primary_id": 9,
        "notes": "Quotation in English"
    },
    {
        "id": "CAT_D_007",
        "split": "test",
        "category": "Category D — English queries",
        "query": "Prophetic statements prohibiting harm and reciprocating harm",
        "language": "en",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [28938],
        "expected_primary_id": 28938,
        "notes": "Maxim of harm in English"
    },
    {
        "id": "CAT_D_008",
        "split": "test",
        "category": "Category D — English queries",
        "query": "Narrations where the Prophet describes the signs of a hypocrite",
        "language": "en",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [32],
        "expected_primary_id": 32,
        "notes": "Signs of a hypocrite (Ayat al-Munafiq)"
    },
    {
        "id": "CAT_D_009",
        "split": "test",
        "category": "Category D — English queries",
        "query": "None of you truly believes until he loves for his brother what he loves for himself",
        "language": "en",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [12],
        "expected_primary_id": 12,
        "notes": "Quotation of brotherhood hadith"
    },
    {
        "id": "CAT_D_010",
        "split": "test",
        "category": "Category D — English queries",
        "query": "Two words that are light on the tongue but heavy on the scale",
        "language": "en",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [6037],
        "expected_primary_id": 6037,
        "notes": "Bukhari closing hadith on Kalimatan"
    },

    # =========================================================================
    # CATEGORY E: Narrator Research
    # =========================================================================
    {
        "id": "CAT_E_001",
        "split": "dev",
        "category": "Category E — Narrator research",
        "query": "Tell me about the narrator Abu Hurayrah",
        "language": "en",
        "expected_intent": "NARRATOR_LOOKUP",
        "expected_rawi_ids": [4396],
        "expected_primary_id": 4396,
        "notes": "Abu Hurayrah (rawi_id 4396)"
    },
    {
        "id": "CAT_E_002",
        "split": "dev",
        "category": "Category E — Narrator research",
        "query": "Who is Abdur Rahman al-Musalli?",
        "language": "en",
        "expected_intent": "NARRATOR_LOOKUP",
        "expected_rawi_ids": [4256],
        "expected_primary_id": 4256,
        "notes": "Abdur Rahman al-Musli (rawi_id 4256, father of Wabarah)"
    },
    {
        "id": "CAT_E_003",
        "split": "dev",
        "category": "Category E — Narrator research",
        "query": "Teachers and students of Sufyan al-Thawri",
        "language": "en",
        "expected_intent": "TEACHERS_STUDENTS",
        "expected_rawi_ids": [3382],
        "expected_primary_id": 3382,
        "notes": "Sufyan al-Thawri transmission network"
    },
    {
        "id": "CAT_E_004",
        "split": "dev",
        "category": "Category E — Narrator research",
        "query": "What did scholars say about narrator Hammad ibn Salamah?",
        "language": "en",
        "expected_intent": "SCHOLARLY_STATEMENTS",
        "expected_rawi_ids": [2019],
        "expected_primary_id": 2019,
        "notes": "Hammad ibn Salamah rijal evaluations"
    },
    {
        "id": "CAT_E_005",
        "split": "dev",
        "category": "Category E — Narrator research",
        "query": "من هو الراوي نافع مولى ابن عمر",
        "language": "ar",
        "expected_intent": "NARRATOR_LOOKUP",
        "expected_rawi_ids": [7841],
        "expected_primary_id": 7841,
        "notes": "Nafi' mawla Ibn Umar (rawi_id 7841)"
    },
    {
        "id": "CAT_E_006",
        "split": "test",
        "category": "Category E — Narrator research",
        "query": "Who is Al-Zuhri Muhammad ibn Muslim?",
        "language": "en",
        "expected_intent": "NARRATOR_LOOKUP",
        "expected_rawi_ids": [6931],
        "expected_primary_id": 6931,
        "notes": "Ibn Shihab al-Zuhri (rawi_id 6931)"
    },
    {
        "id": "CAT_E_007",
        "split": "test",
        "category": "Category E — Narrator research",
        "query": "Jarh wa ta'dil evaluations of narrator Ikrimah mawla Ibn Abbas",
        "language": "en",
        "expected_intent": "JARH_TADIL",
        "expected_rawi_ids": [5387],
        "expected_primary_id": 5387,
        "notes": "Ikrimah mawla Ibn Abbas"
    },
    {
        "id": "CAT_E_008",
        "split": "test",
        "category": "Category E — Narrator research",
        "query": "Biography of narrator Malik ibn Anas",
        "language": "en",
        "expected_intent": "NARRATOR_BIOGRAPHY",
        "expected_rawi_ids": [6769],
        "expected_primary_id": 6769,
        "notes": "Imam Malik (rawi_id 6769)"
    },
    {
        "id": "CAT_E_009",
        "split": "test",
        "category": "Category E — Narrator research",
        "query": "أقوال العلماء في الراوي شعبة بن الحجاج",
        "language": "ar",
        "expected_intent": "SCHOLARLY_STATEMENTS",
        "expected_rawi_ids": [3426],
        "expected_primary_id": 3426,
        "notes": "Shu'bah ibn al-Hajjaj rijal statements"
    },
    {
        "id": "CAT_E_010",
        "split": "test",
        "category": "Category E — Narrator research",
        "query": "Who narrated from Yahya ibn Said al-Ansari?",
        "language": "en",
        "expected_intent": "TEACHERS_STUDENTS",
        "expected_rawi_ids": [8077],
        "expected_primary_id": 8077,
        "notes": "Yahya ibn Sa'id al-Ansari students"
    },

    # =========================================================================
    # CATEGORY F: Scholarly Grading and Criticism
    # =========================================================================
    {
        "id": "CAT_F_001",
        "split": "dev",
        "category": "Category F — Scholarly grading and criticism",
        "query": "What is the grading of Sunan Ibn Majah 1986 by Al-Albani?",
        "language": "en",
        "expected_intent": "HADITH_GRADING",
        "expected_hadith_ids": [28581],
        "expected_primary_id": 28581,
        "notes": "Al-Albani graded Ibn Majah 1986 as Da'if"
    },
    {
        "id": "CAT_F_002",
        "split": "dev",
        "category": "Category F — Scholarly grading and criticism",
        "query": "What did Imam al-Tirmidhi say about Jami at-Tirmidhi 1?",
        "language": "en",
        "expected_intent": "HADITH_GRADING",
        "expected_hadith_ids": [12399],
        "expected_primary_id": 12399,
        "notes": "Al-Tirmidhi classical verdict in classical_scholar_evidence.db"
    },
    {
        "id": "CAT_F_003",
        "split": "dev",
        "category": "Category F — Scholarly grading and criticism",
        "query": "Is the grading of hadith 28581 narrator-level or hadith-level?",
        "language": "en",
        "expected_intent": "HADITH_GRADING",
        "expected_hadith_ids": [28581],
        "expected_primary_id": 28581,
        "notes": "Preserves distinction between narrator judgment and hadith grade"
    },
    {
        "id": "CAT_F_004",
        "split": "dev",
        "category": "Category F — Scholarly grading and criticism",
        "query": "What is the verdict of Hafiz Zubair Ali Zai on Jami at-Tirmidhi 2?",
        "language": "en",
        "expected_intent": "HADITH_GRADING",
        "expected_hadith_ids": [12400],
        "expected_primary_id": 12400,
        "notes": "Zubair Ali Zai in citation_enrichment.db: Sahih Muslim"
    },
    {
        "id": "CAT_F_005",
        "split": "dev",
        "category": "Category F — Scholarly grading and criticism",
        "query": "درجة حديث سنن أبي داود 1 عند الألباني",
        "language": "ar",
        "expected_intent": "HADITH_GRADING",
        "expected_hadith_ids": [16333],
        "expected_primary_id": 16333,
        "notes": "Albani evaluation of Abu Dawud #1"
    },
    {
        "id": "CAT_F_006",
        "split": "test",
        "category": "Category F — Scholarly grading and criticism",
        "query": "What did Abu Dawud say about Sunan Abi Dawud 1?",
        "language": "en",
        "expected_intent": "HADITH_GRADING",
        "expected_hadith_ids": [16333],
        "expected_primary_id": 16333,
        "notes": "Abu Dawud author verdict in classical_scholar_evidence.db"
    },
    {
        "id": "CAT_F_007",
        "split": "test",
        "category": "Category F — Scholarly grading and criticism",
        "query": "What is the authenticity of hadith Bukhari 1?",
        "language": "en",
        "expected_intent": "HADITH_GRADING",
        "expected_hadith_ids": [1],
        "expected_primary_id": 1,
        "notes": "Bukhari #1 is unanimously Sahih"
    },
    {
        "id": "CAT_F_008",
        "split": "test",
        "category": "Category F — Scholarly grading and criticism",
        "query": "حكم حديث طلب العلم فريضة",
        "language": "ar",
        "expected_intent": "HADITH_GRADING",
        "expected_hadith_ids": [26823],
        "expected_primary_id": 26823,
        "notes": "Scholarly disagreements on Talab al-Ilm hadith"
    },
    {
        "id": "CAT_F_009",
        "split": "test",
        "category": "Category F — Scholarly grading and criticism",
        "query": "What is the grade of Sunan an-Nasa'i 348 according to scholars?",
        "language": "en",
        "expected_intent": "HADITH_GRADING",
        "expected_hadith_ids": [21260],
        "expected_primary_id": 21260,
        "notes": "Nasai #348 authenticity"
    },
    {
        "id": "CAT_F_010",
        "split": "test",
        "category": "Category F — Scholarly grading and criticism",
        "query": "What is Yahya ibn Ma'in's statement on Abdur Rahman al-Musalli?",
        "language": "en",
        "expected_intent": "SCHOLARLY_STATEMENTS",
        "expected_rawi_ids": [4256],
        "expected_primary_id": 4256,
        "notes": "Father/son collision check (Ibn Ma'in spoke of son Wabarah)"
    },

    # =========================================================================
    # CATEGORY G: Commentary Retrieval
    # =========================================================================
    {
        "id": "CAT_G_001",
        "split": "dev",
        "category": "Category G — Commentary retrieval",
        "query": "What does the commentary say about Bukhari 1?",
        "language": "en",
        "expected_intent": "COMMENTARY",
        "expected_hadith_ids": [1],
        "expected_primary_id": 1,
        "notes": "Fath al-Bari / Umdat al-Qari on Bukhari 1"
    },
    {
        "id": "CAT_G_002",
        "split": "dev",
        "category": "Category G — Commentary retrieval",
        "query": "Show Fath al-Bari commentary on Sahih al-Bukhari 1",
        "language": "en",
        "expected_intent": "COMMENTARY",
        "expected_hadith_ids": [1],
        "expected_primary_id": 1,
        "notes": "Specific Fath al-Bari request"
    },
    {
        "id": "CAT_G_003",
        "split": "dev",
        "category": "Category G — Commentary retrieval",
        "query": "شرح حديث إنما الأعمال بالنيات في فتح الباري",
        "language": "ar",
        "expected_intent": "COMMENTARY",
        "expected_hadith_ids": [1],
        "expected_primary_id": 1,
        "notes": "Arabic Sharh request"
    },
    {
        "id": "CAT_G_004",
        "split": "dev",
        "category": "Category G — Commentary retrieval",
        "query": "What does Ibn Hajar explain in the commentary of hadith 1?",
        "language": "en",
        "expected_intent": "COMMENTARY",
        "expected_hadith_ids": [1],
        "expected_primary_id": 1,
        "notes": "Ibn Hajar commentary"
    },
    {
        "id": "CAT_G_005",
        "split": "dev",
        "category": "Category G — Commentary retrieval",
        "query": "What does Umdat al-Qari say about Bukhari 1?",
        "language": "en",
        "expected_intent": "COMMENTARY",
        "expected_hadith_ids": [1],
        "expected_primary_id": 1,
        "notes": "Al-Ayni's Umdat al-Qari"
    },
    {
        "id": "CAT_G_006",
        "split": "test",
        "category": "Category G — Commentary retrieval",
        "query": "Classical sharh for Bukhari hadith 8 on five pillars",
        "language": "en",
        "expected_intent": "COMMENTARY",
        "expected_hadith_ids": [7],
        "expected_primary_id": 7,
        "notes": "Commentary on five pillars"
    },
    {
        "id": "CAT_G_007",
        "split": "test",
        "category": "Category G — Commentary retrieval",
        "query": "ماذا قال ابن حجر في شرح حديث بني الإسلام على خمس",
        "language": "ar",
        "expected_intent": "COMMENTARY",
        "expected_hadith_ids": [7],
        "expected_primary_id": 7,
        "notes": "Arabic commentary query"
    },
    {
        "id": "CAT_G_008",
        "split": "test",
        "category": "Category G — Commentary retrieval",
        "query": "Commentary explanation of Bukhari hadith 9 on true Muslim",
        "language": "en",
        "expected_intent": "COMMENTARY",
        "expected_hadith_ids": [9],
        "expected_primary_id": 9,
        "notes": "Fath al-Bari on hadith 9"
    },
    {
        "id": "CAT_G_009",
        "split": "test",
        "category": "Category G — Commentary retrieval",
        "query": "Sharh of Bukhari hadith 12 about loving for your brother",
        "language": "en",
        "expected_intent": "COMMENTARY",
        "expected_hadith_ids": [12],
        "expected_primary_id": 12,
        "notes": "Commentary on loving for one's brother"
    },
    {
        "id": "CAT_G_010",
        "split": "test",
        "category": "Category G — Commentary retrieval",
        "query": "عمدة القاري شرح صحيح البخاري حديث 1",
        "language": "ar",
        "expected_intent": "COMMENTARY",
        "expected_hadith_ids": [1],
        "expected_primary_id": 1,
        "notes": "Umdat al-Qari in Arabic"
    },

    # =========================================================================
    # CATEGORY H: Isnad and Transmission Evidence
    # =========================================================================
    {
        "id": "CAT_H_001",
        "split": "dev",
        "category": "Category H — Isnad and transmission evidence",
        "query": "Show the isnad chain for Sahih al-Bukhari 1",
        "language": "en",
        "expected_intent": "ISNAD_ANALYSIS",
        "expected_hadith_ids": [1],
        "expected_primary_id": 1,
        "notes": "Isnad of Bukhari 1: Humaydi -> Sufyan -> Yahya ibn Said -> Muhammad ibn Ibrahim -> Alqamah -> Umar"
    },
    {
        "id": "CAT_H_002",
        "split": "dev",
        "category": "Category H — Isnad and transmission evidence",
        "query": "What is the sanad of Sahih Muslim 1907?",
        "language": "en",
        "expected_intent": "ISNAD_ANALYSIS",
        "expected_hadith_ids": [8938],
        "expected_primary_id": 8938,
        "notes": "Sanad of Muslim 1907"
    },
    {
        "id": "CAT_H_003",
        "split": "dev",
        "category": "Category H — Isnad and transmission evidence",
        "query": "سند حديث إنما الأعمال بالنيات في صحيح البخاري",
        "language": "ar",
        "expected_intent": "ISNAD_ANALYSIS",
        "expected_hadith_ids": [1],
        "expected_primary_id": 1,
        "notes": "Arabic sanad request"
    },
    {
        "id": "CAT_H_004",
        "split": "dev",
        "category": "Category H — Isnad and transmission evidence",
        "query": "Sanad chain of Sunan Ibn Majah 1986",
        "language": "en",
        "expected_intent": "ISNAD_ANALYSIS",
        "expected_hadith_ids": [28581],
        "expected_primary_id": 28581,
        "notes": "Contains Abdur Rahman al-Musalli in sanad"
    },
    {
        "id": "CAT_H_005",
        "split": "dev",
        "category": "Category H — Isnad and transmission evidence",
        "query": "Who is the companion in the chain of Bukhari 1?",
        "language": "en",
        "expected_intent": "ISNAD_ANALYSIS",
        "expected_hadith_ids": [1],
        "expected_primary_id": 1,
        "notes": "Umar ibn al-Khattab"
    },
    {
        "id": "CAT_H_006",
        "split": "test",
        "category": "Category H — Isnad and transmission evidence",
        "query": "Chain of narrators for Jami at-Tirmidhi 1",
        "language": "en",
        "expected_intent": "ISNAD_ANALYSIS",
        "expected_hadith_ids": [12399],
        "expected_primary_id": 12399,
        "notes": "Tirmidhi #1 chain"
    },
    {
        "id": "CAT_H_007",
        "split": "test",
        "category": "Category H — Isnad and transmission evidence",
        "query": "Isnad of Sunan Abi Dawud 1",
        "language": "en",
        "expected_intent": "ISNAD_ANALYSIS",
        "expected_hadith_ids": [16333],
        "expected_primary_id": 16333,
        "notes": "Abu Dawud #1 chain"
    },
    {
        "id": "CAT_H_008",
        "split": "test",
        "category": "Category H — Isnad and transmission evidence",
        "query": "سند حديث لا ضرر ولا ضرار في سنن ابن ماجه",
        "language": "ar",
        "expected_intent": "ISNAD_ANALYSIS",
        "expected_hadith_ids": [28938],
        "expected_primary_id": 28938,
        "notes": "Chain of La Darar wa la Dirar"
    },
    {
        "id": "CAT_H_009",
        "split": "test",
        "category": "Category H — Isnad and transmission evidence",
        "query": "Isnad of Sunan an-Nasa'i 348",
        "language": "en",
        "expected_intent": "ISNAD_ANALYSIS",
        "expected_hadith_ids": [21260],
        "expected_primary_id": 21260,
        "notes": "Chain of Nasai 348"
    },
    {
        "id": "CAT_H_010",
        "split": "test",
        "category": "Category H — Isnad and transmission evidence",
        "query": "Transmission chain of Muwatta Malik 1",
        "language": "en",
        "expected_intent": "ISNAD_ANALYSIS",
        "expected_hadith_ids": [32971],
        "expected_primary_id": 32971,
        "notes": "Chain of Muwatta #1"
    },

    # =========================================================================
    # CATEGORY I: Cross-reference and Numbering
    # =========================================================================
    {
        "id": "CAT_I_001",
        "split": "dev",
        "category": "Category I — Cross-reference and numbering",
        "query": "Sunan Ibn Majah Darussalam 1986 crosswalk",
        "language": "en",
        "expected_intent": "NUMBERING",
        "expected_hadith_ids": [28581],
        "expected_primary_id": 28581,
        "notes": "Resolves to canonical 28581 (In-book 1976)"
    },
    {
        "id": "CAT_I_002",
        "split": "dev",
        "category": "Category I — Cross-reference and numbering",
        "query": "Sunan an-Nasa'i Darussalam 348 numbering schemes",
        "language": "en",
        "expected_intent": "NUMBERING",
        "expected_hadith_ids": [21260],
        "expected_primary_id": 21260,
        "notes": "Multi-scheme resolution (Darussalam vs Shamela)"
    },
    {
        "id": "CAT_I_003",
        "split": "dev",
        "category": "Category I — Cross-reference and numbering",
        "query": "What is the Darussalam number for Bukhari 1?",
        "language": "en",
        "expected_intent": "NUMBERING",
        "expected_hadith_ids": [1],
        "expected_primary_id": 1,
        "notes": "Bukhari 1 is #1 in Darussalam"
    },
    {
        "id": "CAT_I_004",
        "split": "dev",
        "category": "Category I — Cross-reference and numbering",
        "query": "ترقيم دار السلام لسنن ابن ماجه 1986",
        "language": "ar",
        "expected_intent": "NUMBERING",
        "expected_hadith_ids": [28581],
        "expected_primary_id": 28581,
        "notes": "Arabic numbering crosswalk query"
    },
    {
        "id": "CAT_I_005",
        "split": "dev",
        "category": "Category I — Cross-reference and numbering",
        "query": "Sahih Muslim 1907 numbering across editions",
        "language": "en",
        "expected_intent": "NUMBERING",
        "expected_hadith_ids": [8938],
        "expected_primary_id": 8938,
        "notes": "Abd al-Baqi vs inbook numbering"
    },
    {
        "id": "CAT_I_006",
        "split": "test",
        "category": "Category I — Cross-reference and numbering",
        "query": "What is Shamela number for Sunan Ibn Majah Darussalam 1986?",
        "language": "en",
        "expected_intent": "NUMBERING",
        "expected_hadith_ids": [28581],
        "expected_primary_id": 28581,
        "notes": "Resolves Shamela 1976"
    },
    {
        "id": "CAT_I_007",
        "split": "test",
        "category": "Category I — Cross-reference and numbering",
        "query": "Sunan Abi Dawud Darussalam 1 numbering",
        "language": "en",
        "expected_intent": "NUMBERING",
        "expected_hadith_ids": [16333],
        "expected_primary_id": 16333,
        "notes": "Abu Dawud #1"
    },
    {
        "id": "CAT_I_008",
        "split": "test",
        "category": "Category I — Cross-reference and numbering",
        "query": "Jami at-Tirmidhi Darussalam 1 numbering crosswalk",
        "language": "en",
        "expected_intent": "NUMBERING",
        "expected_hadith_ids": [12399],
        "expected_primary_id": 12399,
        "notes": "Tirmidhi #1"
    },
    {
        "id": "CAT_I_009",
        "split": "test",
        "category": "Category I — Cross-reference and numbering",
        "query": "ترقيم صحيح البخاري في الشاملة ودار السلام لحديث 1",
        "language": "ar",
        "expected_intent": "NUMBERING",
        "expected_hadith_ids": [1],
        "expected_primary_id": 1,
        "notes": "Arabic cross-edition numbering"
    },
    {
        "id": "CAT_I_010",
        "split": "test",
        "category": "Category I — Cross-reference and numbering",
        "query": "Sunan an-Nasa'i 1 numbering crosswalk",
        "language": "en",
        "expected_intent": "NUMBERING",
        "expected_hadith_ids": [20913],
        "expected_primary_id": 20913,
        "notes": "Nasai #1 crosswalk"
    },

    # =========================================================================
    # CATEGORY J: Ambiguous and Unanswerable Questions (Abstention)
    # =========================================================================
    {
        "id": "CAT_J_001",
        "split": "dev",
        "category": "Category J — Ambiguous and unanswerable questions",
        "query": "Sahih al-Bukhari 999999",
        "language": "en",
        "expected_intent": "HADITH_LOOKUP",
        "expected_refusal": True,
        "notes": "Non-existent hadith identifier; must refuse safely"
    },
    {
        "id": "CAT_J_002",
        "split": "dev",
        "category": "Category J — Ambiguous and unanswerable questions",
        "query": "Who is the narrator Zayd?",
        "language": "en",
        "expected_intent": "NARRATOR_LOOKUP",
        "expected_ambiguous": True,
        "notes": "Ambiguous single name without kunya, father, or nisbah"
    },
    {
        "id": "CAT_J_003",
        "split": "dev",
        "category": "Category J — Ambiguous and unanswerable questions",
        "query": "Sunan Abu Dawud 88888",
        "language": "en",
        "expected_intent": "HADITH_LOOKUP",
        "expected_refusal": True,
        "notes": "Out of range number"
    },
    {
        "id": "CAT_J_004",
        "split": "dev",
        "category": "Category J — Ambiguous and unanswerable questions",
        "query": "What did Imam al-Bukhari write about quantum physics?",
        "language": "en",
        "expected_intent": "GENERAL_RESEARCH",
        "expected_refusal": True,
        "notes": "Anachronistic / unanswerable from Hadith corpus"
    },
    {
        "id": "CAT_J_005",
        "split": "dev",
        "category": "Category J — Ambiguous and unanswerable questions",
        "query": "صحيح مسلم 555555",
        "language": "ar",
        "expected_intent": "HADITH_LOOKUP",
        "expected_refusal": True,
        "notes": "Arabic non-existent hadith reference"
    },
    {
        "id": "CAT_J_006",
        "split": "test",
        "category": "Category J — Ambiguous and unanswerable questions",
        "query": "Jami at-Tirmidhi 77777",
        "language": "en",
        "expected_intent": "HADITH_LOOKUP",
        "expected_refusal": True,
        "notes": "Non-existent Tirmidhi hadith"
    },
    {
        "id": "CAT_J_007",
        "split": "test",
        "category": "Category J — Ambiguous and unanswerable questions",
        "query": "Who is narrator Muhammad?",
        "language": "en",
        "expected_intent": "NARRATOR_LOOKUP",
        "expected_ambiguous": True,
        "notes": "Severely ambiguous narrator query"
    },
    {
        "id": "CAT_J_008",
        "split": "test",
        "category": "Category J — Ambiguous and unanswerable questions",
        "query": "Sunan Ibn Majah 99999",
        "language": "en",
        "expected_intent": "HADITH_LOOKUP",
        "expected_refusal": True,
        "notes": "Non-existent Ibn Majah reference"
    },
    {
        "id": "CAT_J_009",
        "split": "test",
        "category": "Category J — Ambiguous and unanswerable questions",
        "query": "ما هو حديث صحيح البخاري 999999",
        "language": "ar",
        "expected_intent": "HADITH_LOOKUP",
        "expected_refusal": True,
        "notes": "Arabic inquiry for non-existent hadith"
    },
    {
        "id": "CAT_J_010",
        "split": "test",
        "category": "Category J — Ambiguous and unanswerable questions",
        "query": "Tell me the hadith about bitcoin investment in Bukhari",
        "language": "en",
        "expected_intent": "GENERAL_RESEARCH",
        "expected_refusal": True,
        "notes": "Anachronistic / corpus has no answer"
    },

    # =========================================================================
    # CATEGORY K: Cross-Lingual Retrieval
    # =========================================================================
    {
        "id": "CAT_K_001",
        "split": "dev",
        "category": "Category K — Cross-lingual retrieval",
        "query": "انما الاعمال بالنیات کا مفہوم اور ماخذ",
        "language": "ur",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [1],
        "expected_primary_id": 1,
        "notes": "Urdu query seeking classical Arabic source Bukhari 1"
    },
    {
        "id": "CAT_K_002",
        "split": "dev",
        "category": "Category K — Cross-lingual retrieval",
        "query": "Hadith on actions being judged by intentions",
        "language": "en",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [1],
        "expected_primary_id": 1,
        "notes": "English query seeking Arabic hadith #1"
    },
    {
        "id": "CAT_K_003",
        "split": "dev",
        "category": "Category K — Cross-lingual retrieval",
        "query": "اسلام کی بنیاد پانچ چیزوں پر ہے",
        "language": "ur",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [7],
        "expected_primary_id": 7,
        "notes": "Urdu phrasing seeking Bukhari 8 (Buni al-Islam)"
    },
    {
        "id": "CAT_K_004",
        "split": "dev",
        "category": "Category K — Cross-lingual retrieval",
        "query": "English hadith on the cleanliness is half of faith",
        "language": "en",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [7364],
        "expected_primary_id": 7364,
        "notes": "English query seeking Sahih Muslim 223 (al-Tahuru shatr al-Iman)"
    },
    {
        "id": "CAT_K_005",
        "split": "dev",
        "category": "Category K — Cross-lingual retrieval",
        "query": "کسی مسلمان کو گالی دینا فسق اور قتل کرنا کفر ہے",
        "language": "ur",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [46],
        "expected_primary_id": 46,
        "notes": "Urdu translation seeking Sibab al-Muslim fusuq (Bukhari 48)"
    },
    {
        "id": "CAT_K_006",
        "split": "test",
        "category": "Category K — Cross-lingual retrieval",
        "query": "Reviling a Muslim is an act of wickedness and fighting him is disbelief",
        "language": "en",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [46],
        "expected_primary_id": 46,
        "notes": "English seeking Arabic Sibab al-Muslim"
    },
    {
        "id": "CAT_K_007",
        "split": "test",
        "category": "Category K — Cross-lingual retrieval",
        "query": "جس نے دھوکہ دیا وہ ہم میں سے نہیں ہے",
        "language": "ur",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [7180],
        "expected_primary_id": 7180,
        "notes": "Urdu translation seeking Man ghashana fa-laysa minna"
    },
    {
        "id": "CAT_K_008",
        "split": "test",
        "category": "Category K — Cross-lingual retrieval",
        "query": "The religion is sincerity to Allah, His Book, and His Messenger",
        "language": "en",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [7116],
        "expected_primary_id": 7116,
        "notes": "English seeking al-Dinu al-Nasihah"
    },
    {
        "id": "CAT_K_009",
        "split": "test",
        "category": "Category K — Cross-lingual retrieval",
        "query": "علم حاصل کرنا ہر مسلمان پر فرض ہے",
        "language": "ur",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [26823],
        "expected_primary_id": 26823,
        "notes": "Urdu seeking Talab al-Ilm faridah"
    },
    {
        "id": "CAT_K_010",
        "split": "test",
        "category": "Category K — Cross-lingual retrieval",
        "query": "There should be neither harming nor reciprocating harm in Islam",
        "language": "en",
        "expected_intent": "THEMATIC",
        "expected_hadith_ids": [28938],
        "expected_primary_id": 28938,
        "notes": "English seeking La Darara wa la Dirar"
    },

    # =========================================================================
    # CATEGORY L: Multi-Part Research Questions
    # =========================================================================
    {
        "id": "CAT_L_001",
        "split": "dev",
        "category": "Category L — Multi-part research questions",
        "query": "Compare Bukhari 1 and Muslim 1907",
        "language": "en",
        "expected_intent": "HADITH_COMPARISON",
        "expected_hadith_ids": [1, 8938],
        "notes": "Side-by-side matn and isnad comparison"
    },
    {
        "id": "CAT_L_002",
        "split": "dev",
        "category": "Category L — Multi-part research questions",
        "query": "Explain Sahih al-Bukhari 1 with its sanad and classical commentary",
        "language": "en",
        "expected_intent": "COMMENTARY",
        "expected_hadith_ids": [1],
        "expected_primary_id": 1,
        "notes": "Requires Hadith text + Isnad + Commentary"
    },
    {
        "id": "CAT_L_003",
        "split": "dev",
        "category": "Category L — Multi-part research questions",
        "query": "Compare the wording and isnad of Bukhari 8 and Muslim 16",
        "language": "en",
        "expected_intent": "SOURCE_COMPARISON",
        "expected_hadith_ids": [7, 7053],
        "notes": "Source comparison across Bukhari and Muslim on 5 pillars"
    },
    {
        "id": "CAT_L_004",
        "split": "dev",
        "category": "Category L — Multi-part research questions",
        "query": "Who is Abdur Rahman al-Musalli and what hadiths did he narrate in Ibn Majah?",
        "language": "en",
        "expected_intent": "NARRATOR_LOOKUP",
        "expected_rawi_ids": [4256],
        "expected_hadith_ids": [28581],
        "notes": "Combines narrator biography + hadith transmission link"
    },
    {
        "id": "CAT_L_005",
        "split": "dev",
        "category": "Category L — Multi-part research questions",
        "query": "مقارنة بين حديث البخاري 1 وحديث مسلم 1907 في السند والمتن",
        "language": "ar",
        "expected_intent": "HADITH_COMPARISON",
        "expected_hadith_ids": [1, 8938],
        "notes": "Arabic multi-part comparison"
    },
    {
        "id": "CAT_L_006",
        "split": "test",
        "category": "Category L — Multi-part research questions",
        "query": "Explain Sunan Ibn Majah 1986 with its grading by Al-Albani and narrator evaluation",
        "language": "en",
        "expected_intent": "HADITH_GRADING",
        "expected_hadith_ids": [28581],
        "expected_rawi_ids": [4256],
        "notes": "Multi-part grading and rijal evaluation"
    },
    {
        "id": "CAT_L_007",
        "split": "test",
        "category": "Category L — Multi-part research questions",
        "query": "Show Bukhari 1, its parallel narrations, and its opening commentary by Ibn Hajar",
        "language": "en",
        "expected_intent": "COMMENTARY",
        "expected_hadith_ids": [1],
        "notes": "Requires parallel narrations + commentary"
    },
    {
        "id": "CAT_L_008",
        "split": "test",
        "category": "Category L — Multi-part research questions",
        "query": "What are the common narrators between Bukhari 1 and Muslim 1907?",
        "language": "en",
        "expected_intent": "HADITH_COMPARISON",
        "expected_hadith_ids": [1, 8938],
        "notes": "Common narrator extraction across two chains"
    },
    {
        "id": "CAT_L_009",
        "split": "test",
        "category": "Category L — Multi-part research questions",
        "query": "صحیح بخاری 1 اور صحیح مسلم 1907 کا موازنہ اور اسناد",
        "language": "ur",
        "expected_intent": "HADITH_COMPARISON",
        "expected_hadith_ids": [1, 8938],
        "notes": "Urdu multi-part comparison"
    },
    {
        "id": "CAT_L_010",
        "split": "test",
        "category": "Category L — Multi-part research questions",
        "query": "Explain the hadith on five pillars with its grading and commentary in Bukhari",
        "language": "en",
        "expected_intent": "COMMENTARY",
        "expected_hadith_ids": [7],
        "notes": "Multi-part: Bukhari 8 text + grade + commentary"
    },
]

def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for item in BENCHMARK_ITEMS:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"Successfully generated {len(BENCHMARK_ITEMS)} stratified benchmark items at {OUTPUT_FILE}")
    dev_count = sum(1 for i in BENCHMARK_ITEMS if i["split"] == "dev")
    test_count = sum(1 for i in BENCHMARK_ITEMS if i["split"] == "test")
    print(f"Splits: DEV = {dev_count}, TEST = {test_count}")

if __name__ == "__main__":
    main()
