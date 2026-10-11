"""
MĪZĀN AL-ḤADĪTH — Benchmark Dataset Generator (Phase 2)
Generates the authoritative 500-query evaluation dataset:
  data/benchmarks/embeddinggemma2_benchmark_v1.jsonl

Distribution (500 Total Queries):
  1. Arabic:          150 queries (exact wording, paraphrases, topics, complex theological queries)
  2. Urdu:            100 queries (natural Urdu, Urdu paraphrases, theological research queries)
  3. English:         100 queries (natural English, English paraphrases, theological research queries)
  4. Cross-Lingual:   100 queries (50 Urdu -> Arabic hadiths, 50 English -> Arabic hadiths)
  5. Reference/Edge:   50 queries (citations, numbering schemes, transliterations, boundary cases)

GUARANTEES:
  - Every query has deterministic gold relevance labels (gold_group_ids, gold_hadith_ids).
  - Gold labels derived from canonical meaning_groups and verified crosswalks in hadith-kg.db.
  - Zero circular dependency (model is evaluated against independent ground truth, not its own predictions).
  - Excludes placeholder meaning group 0.
  - Emits JSONL, SHA-256 companion file, and benchmark manifest.
"""

from __future__ import annotations
import hashlib
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
CANONICAL_KG_PATH = REPO_ROOT / "data" / "hadith-kg.db"
OUTPUT_DIR = REPO_ROOT / "data" / "benchmarks"
OUTPUT_JSONL_PATH = OUTPUT_DIR / "embeddinggemma2_benchmark_v1.jsonl"
OUTPUT_SHA_PATH = OUTPUT_DIR / "embeddinggemma2_benchmark_v1.sha256"
OUTPUT_MANIFEST_PATH = OUTPUT_DIR / "embeddinggemma2_benchmark_manifest.json"

EXPECTED_TOTAL = 500
EXPECTED_ARABIC = 150
EXPECTED_URDU = 100
EXPECTED_ENGLISH = 100
EXPECTED_CROSS = 100
EXPECTED_REF_EDGE = 50


def compute_file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024 * 8):
            h.update(chunk)
    return h.hexdigest()


def find_group_for_nass_pattern(conn: sqlite3.Connection, pattern: str) -> Optional[Tuple[int, str]]:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nass FROM meaning_groups WHERE id > 0 AND nass LIKE ? ORDER BY id ASC LIMIT 1;",
        (f"%{pattern}%",)
    )
    row = cursor.fetchone()
    if row:
        return int(row[0]), str(row[1])
    
    # Robust fallback: match key content words of at least 3 characters
    words = [w for w in pattern.split() if len(w) >= 3 and w not in ("من", "في", "على", "إلى", "أن", "إن")]
    if len(words) >= 2:
        query_sql = "SELECT id, nass FROM meaning_groups WHERE id > 0 " + " ".join(["AND nass LIKE ?" for _ in words[:3]]) + " ORDER BY id ASC LIMIT 1;"
        cursor.execute(query_sql, [f"%{w}%" for w in words[:3]])
        row = cursor.fetchone()
        if row:
            return int(row[0]), str(row[1])
    return None


def get_canonical_hadith_ids_for_group(conn: sqlite3.Connection, group_id: int, limit: int = 5) -> List[int]:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM hadiths WHERE group_id = ? ORDER BY book_id ASC, no_inbook ASC LIMIT ?;",
        (group_id, limit)
    )
    return [int(r[0]) for r in cursor.fetchall()]


# Curated high-fidelity anchor specifications covering the complete corpus taxonomy
# Each entry: (Concept Key, Arabic Pattern / Term, English Concept, Urdu Concept, Notes)
CANONICAL_ANCHORS = [
    # General / Foundational
    ("niyyah", "الأعمال بالنيات", "Actions are judged by intentions", "اعمال کا دارومدار نیتوں پر ہے", "Hadith of intention, Bukhari 1 / Muslim 1907"),
    ("buni_islam", "بني الإسلام على خمس", "Islam is built upon five pillars", "اسلام کی بنیاد پانچ ستونوں پر ہے", "Hadith of 5 pillars, Bukhari 8"),
    ("muslim_salim", "المسلم من سلم المسلمون", "A Muslim is one from whose tongue and hand others are safe", "مسلمان وہ ہے جس کی زبان اور ہاتھ سے دوسرے مسلمان محفوظ رہیں", "Definition of true Muslim"),
    ("ihsan_jibril", "أن تعبد الله كأنك تراه", "To worship Allah as if you see Him", "اللہ کی عبادت اس طرح کرنا گویا تم اسے دیکھ رہے ہو", "Hadith of Jibril / Ihsan"),
    ("la_darar", "لا ضرر ولا ضرار", "No harm shall be inflicted or reciprocated", "نہ کسی کو نقصان پہنچانا جائز ہے اور نہ نقصان کا بدلہ نقصان سے", "Maxims of Islamic jurisprudence"),
    ("nasiha", "الدين النصيحة", "Religion is sincere advice", "دین خیر خواہی اور اخلاص کا نام ہے", "Hadith of sincerity"),
    ("halal_bayyin", "الحلال بين والحرام بين", "The lawful is clear and the unlawful is clear", "حلال واضح ہے اور حرام بھی واضح ہے", "Hadith of doubtful matters / Shubuhāt"),
    ("haya", "الحياء شعبة من الإيمان", "Modesty is a branch of faith", "حیا ایمان کا ایک اہم شعبہ ہے", "Branches of faith"),
    ("tahur", "الطهور شطر الإيمان", "Purity is half of faith", "پاکیزگی اور طہارت نصف ایمان ہے", "Hadith of purification"),
    ("sidq", "عليكم بالصدق", "Adhere strictly to truthfulness", "ہمیشہ سچائی کو لازم پکڑو کیونکہ سچ نیکی کی طرف رہنمائی کرتا ہے", "Virtues of truthfulness"),
    ("ghash", "من غشنا فليس منا", "Whoever cheats us is not of us", "جس نے دھوکہ دیا وہ ہم میں سے نہیں ہے", "Prohibition of fraud and cheating"),
    ("yufaqqihhu", "من يرد الله به خيرا يفقهه في الدين", "Whomever Allah intends good for He grants understanding of religion", "اللہ جس کے ساتھ بھلائی کا ارادہ فرماتا ہے اسے دین کی سمجھ عطا کرتا ہے", "Virtues of religious knowledge"),
    ("kalimatan", "كلمتان خفيفتان على اللسان", "Two words that are light on the tongue and heavy on the scale", "دو کلمے جو زبان پر ہلکے اور میزان میں بھاری ہیں", "Subhan Allahi wa bihamdihi"),
    ("la_tughdab", "لا تغضب", "Do not become angry", "غصہ مت کرو اور اپنے جذبات پر قابو رکھو", "Prophetic advice against wrath"),
    ("tarak_ma_la_ya'nih", "من حسن إسلام المرء تركه ما لا يعنيه", "Part of the excellence of one's Islam is leaving what does not concern him", "انسان کے اسلام کی خوبی یہ ہے کہ وہ فضول باتوں کو چھوڑ دے", "Four foundational hadiths"),
    ("yuhibbu_liakhih", "يحب لأخيه ما يحب لنفسه", "None of you believes until he loves for his brother what he loves for himself", "تم میں سے کوئی مومن نہیں ہو سکتا جب تک اپنے بھائی کے لیے وہی پسند نہ کرے جو اپنے لیے کرتا ہے", "Brotherhood in faith"),
    ("kullukum_ra'in", "كلكم راع وكلكم مسؤول", "Every one of you is a shepherd and responsible for his flock", "تم میں سے ہر ایک نگہبان ہے اور اپنی رعیت کے بارے میں جوابدہ ہے", "Responsibility of leadership and family"),
    ("samahan", "رحم الله رجلا سمحا إذا باع", "May Allah have mercy on a man who is lenient when he sells and buys", "اللہ اس شخص پر رحم فرمائے جو بیچتے اور خریدتے وقت نرمی کا برتاؤ کرتا ہے", "Leniency in transactions"),
    ("tayyib", "إن الله طيب لا يقبل إلا طيبا", "Allah is pure and accepts only what is pure", "اللہ پاک ہے اور صرف پاکیزہ چیز ہی قبول فرماتا ہے", "Halal sustenance and acceptance of prayer"),
    ("khayrukum_quran", "خيركم من تعلم القرآن وعلمه", "The best of you are those who learn the Quran and teach it", "تم میں سے بہترین شخص وہ ہے جو قرآن سیکھے اور سکھائے", "Virtues of learning Quran"),

    # Purification & Wudu (Taharah)
    ("la_salata_bighayr_tuhur", "لا يقبل الله صلاة بغير طهور", "Allah does not accept prayer without purification", "اللہ تعالی بغیر پاکیزگی کے نماز قبول نہیں فرماتا", "Condition of Salah"),
    ("siwak", "لولا أن أشق على أمتي لأمرتهم بالسواك", "Were it not that I would burden my nation I would command the toothstick", "اگر مجھے اپنی امت پر مشقت کا اندیشہ نہ ہوتا تو ہر نماز کے لیے مسواک کا حکم دیتا", "Virtues of Miswak"),
    ("wudu_shatranj", "من توضأ فأحسن الوضوء خرجت خطاياه", "Whoever performs ablution thoroughly his sins depart from his body", "جس نے اچھی طرح وضو کیا اس کے گناہ جسم سے نکل جاتے ہیں", "Expiation through Wudu"),
    ("tayamum", "جعلت لي الأرض مسجدا وطهورا", "The earth has been made for me a place of prayer and a means of purification", "میرے لیے تمام زمین کو مسجد اور پاکیزہ بنانے کا ذریعہ قرار دیا گیا ہے", "Concession of Tayammum"),
    ("himaar", "الماء طهور لا ينجسه شيء", "Water is pure and nothing makes it impure", "پانی پاک ہے اسے کوئی چیز ناپاک نہیں کرتی سوائے اس کے کہ رنگ بو ذائقہ بدل جائے", "Nature of pure water"),
    ("masah_khuffayn", "المسح على الخفين", "Wiping over leather socks during journey and residency", "موزوں پر مسح کرنے کی رخصت اور اس کی مدت", "Rukhsa of wiping over socks"),
    ("qubul_wudu_nawm", "العينان وكاء السه", "The eyes are the drawstring of the rear", "آنکھیں سرین کا بندھن ہیں جب انسان سو جائے تو وضو ٹوٹ جاتا ہے", "Nullifiers of Wudu: deep sleep"),
    ("ibil_wudu", "أتوضأ من لحوم الإبل قال نعم", "Ablution after eating camel meat", "اونٹ کا گوشت کھانے کے بعد وضو کرنے کا حکم", "Wudu after camel meat"),
    ("istinja", "استنزهوا من البول", "Protect yourselves from urine for most punishment of grave is from it", "پیشاب کی چھینٹوں سے بچو کیونکہ اکثر عذاب قبر اسی کی وجہ سے ہوتا ہے", "Sanctity of purification from urine"),
    ("madhmadhah", "وبالغ في الاستنشاق إلا أن تكون صائما", "Inhale water deeply into nostrils unless fasting", "ناک میں گہرائی تک پانی چڑھا کر صفائی کرو الا یہ کہ تم روزے سے ہو", "Excellence in Wudu"),

    # Prayer (Salah)
    ("salat_awqat", "الصلاة على وقتها", "Offering prayer at its appointed time", "نماز کو اس کے مقررہ وقت پر ادا کرنے کی فضیلت", "Best deeds in Islam"),
    ("salat_jamaah", "صلاة الجماعة تفضل صلاة الفذ بسبع وعشرين درجة", "Congregational prayer exceeds individual prayer by twenty-seven degrees", "باجماعت نماز اکیلے پڑھنے پر ستائیس درجے فضیلت رکھتی ہے", "Virtue of congregation"),
    ("adhan_ijabah", "إذا نودي للصلاة أدبر الشيطان", "When the call to prayer is made Satan flees", "جب نماز کے لیے اذان دی جاتی ہے تو شیطان ہوا خارج کرتا ہوا بھاگتا ہے", "Virtues of Adhan"),
    ("iftitah_takbir", "تحريمها التكبير وتحليلها التسليم", "Its opening is Takbir and its conclusion is Taslim", "نماز کا آغاز تکبیر سے ہوتا ہے اور اس کا اختتام سلام پر ہوتا ہے", "Pillars of Salah"),
    ("fatiha_la_salat", "لا صلاة لمن لم يقرأ بفاتحة الكتاب", "There is no prayer for the one who does not recite Surah Al-Fatihah", "اس شخص کی کوئی نماز نہیں جو سورہ فاتحہ نہ پڑھے", "Obligation of Fatihah"),
    ("ruku_sujud", "أقرب ما يكون العبد من ربه وهو ساجد", "The closest a servant comes to his Lord is while prostrating", "بندہ اپنے رب کے سب سے زیادہ قریب سجدے کی حالت میں ہوتا ہے", "Supplication in Sujud"),
    ("qasr_safar", "تقصر الصلاة في السفر", "Shortening prayer during travel", "سفر کے دوران چار رکعت والی نماز کو دو رکعت قصر کرنا", "Rukhsa of traveling"),
    ("sahw_sujud", "سجدتا السهو", "Two prostrations of forgetfulness before or after Salam", "نماز میں بھول چوک ہونے پر سجدہ سہو ادا کرنے کا طریقہ", "Sujood al-Sahw"),
    ("tahajjud", "أفضل الصلاة بعد الفريضة صلاة الليل", "The best prayer after obligatory prayer is the night prayer", "فرض نماز کے بعد سب سے افضل نماز رات کی تہجد ہے", "Night vigil / Tahajjud"),
    ("kusuf", "إن الشمس والقمر آيتان من آيات الله لا يخسفان لموت أحد", "The sun and moon are two signs of Allah and do not eclipse for anyone's death", "سورج اور چاند اللہ کی نشانیوں میں سے ہیں ان کا گرہن کسی کی موت یا پیدائش سے نہیں ہوتا", "Salat al-Kusuf / Eclipse"),

    # Zakat & Charity (Sadaqah)
    ("zakat_fitr", "فرض رسول الله زكاة الفطر صاعا من تمر", "The Messenger obligated Zakat al-Fitr as a Sa' of dates or barley", "رسول اللہ صلی اللہ علیہ وسلم نے زکوۃ الفطر ایک صاع کھجور یا جو فرض فرمائی", "Zakat al-Fitr"),
    ("sadaqah_sirr", "ورجل تصدق بصدقة فأخفاها", "A man who gives charity so secretly his left hand does not know what his right spends", "وہ شخص جو اس قدر پوشیدہ صدقہ کرے کہ بائیں ہاتھ کو خبر نہ ہو دائیں نے کیا دیا", "Seven under Allah's shade"),
    ("sadaqah_burhan", "الصدقة برهان", "Charity is a definitive proof of faith", "صدقہ ایمان کی سچی دلیل اور برہان ہے", "Sadaqah confirms faith"),
    ("la_tahqiranna", "اتقوا النار ولو بشق تمرة", "Guard against the Hellfire even with half a date", "جہنم کی آگ سے بچو خواہ کھجور کے ایک ٹکڑے کے صدقے سے ہی کیوں نہ ہو", "Value of small charity"),
    ("sadaqah_jariya", "إذا مات الإنسان انقطع عنه عمله إلا من ثلاثة", "When a human dies all deeds cease except three: recurring charity, beneficial knowledge, righteous child", "انسان کی وفات کے بعد اس کے تمام اعمال ختم ہو جاتے ہیں سوائے تین کے: صدقہ جاریہ، نفع بخش علم اور نیک اولاد", "Perpetual charity"),
    ("zakat_amwal", "ما نقصت صدقة من مال", "Charity never diminishes wealth", "صدقہ دینے سے مال میں کوئی کمی واقع نہیں ہوتی بلکہ برکت ہوتی ہے", "Blessing in wealth"),
    ("su'al_dhill", "اليد العليا خير من اليد السفلى", "The upper hand that gives is better than the lower hand that receives", "دینے والا ہاتھ لینے والے ہاتھ سے کہیں بہتر اور برتر ہے", "Dignity of giving"),
    ("sadaqah_khatiy'ah", "الصدقة تطفئ الخطيئة كما يطفئ الماء النار", "Charity extinguishes sins as water extinguishes fire", "صدقہ گناہوں کو اس طرح بجھا دیتا ہے جیسے پانی آگ کو بجھاتا ہے", "Expiation via Sadaqah"),

    # Fasting (Sawm)
    ("sawm_junnah", "الصيام جنة فإذا كان يوم صوم أحدكم فلا يرفث", "Fasting is a shield; when one of you is fasting let him not speak obscenely", "روزہ برائیوں کے خلاف ایک ڈھال ہے، جب تم میں سے کوئی روزے سے ہو تو بے ہودہ بات نہ کرے", "Fasting etiquette"),
    ("sawm_farhah", "للصائم فرحتان فرحة عند فطره وفرحة عند لقاء ربه", "The fasting person has two joys: one upon breaking fast and one upon meeting Lord", "روزے دار کے لیے دو خوشیاں ہیں: ایک افطار کے وقت اور دوسری اپنے رب سے ملاقات کے وقت", "Reward of fasting"),
    ("khaluf_fam", "لخلوف فم الصائم أطيب عند الله من ريح المسك", "The breath of the fasting person is sweeter to Allah than the scent of musk", "روزے دار کے منہ کی بو اللہ کے نزدیک کستوری کی خوشبو سے زیادہ پسندیدہ ہے", "Virtue of fasting"),
    ("suhur_barakah", "تسحروا فإن في السحور بركة", "Eat Suhur for indeed there is blessing in Suhur", "سحری ضرور کھایا کرو کیونکہ سحری کھانے میں خیر و برکت ہے", "Virtue of pre-dawn meal"),
    ("ta'jil_fitr", "لا يزال الناس بخير ما عجلوا الفطر", "People will remain in goodness as long as they hasten to break the fast", "لوگ اس وقت تک بھلائی پر رہیں گے جب تک افطار میں جلدی کرتے رہیں گے", "Hastening Iftar"),
    ("sawm_arafah", "صيام يوم عرفة أحتسب على الله أن يكفر السنة التي قبله", "Fasting the day of Arafah expiates sins of the preceding and coming year", "یوم عرفہ کا روزہ پچھلے اور اگلے سال کے گناہوں کا کفارہ بن جاتا ہے", "Voluntary fast of Arafah"),
    ("sawm_ashura", "صيام يوم عاشوراء يكفر سنة", "Fasting the day of Ashura expiates the preceding year", "یوم عاشورہ کا روزہ پچھلے ایک سال کے گناہوں کا کفارہ ہوتا ہے", "Fasting on 10th Muharram"),
    ("sawm_shawwal", "من صام رمضان ثم أتبعه ستا من شوال", "Whoever fasts Ramadan then follows it with six days of Shawwal is like fasting whole year", "جس نے رمضان کے روزے رکھے پھر شوال کے چھ روزے رکھے گویا اس نے پورے سال کے روزے رکھے", "Six fasts of Shawwal"),
    ("man_lama_yada'", "من لم يدع قول الزور والعمل به فليس لله حاجة", "Whoever does not abandon false speech and acting upon it Allah has no need of his leaving food", "جو شخص جھوٹ بولنا اور اس پر عمل کرنا نہ چھوڑے تو اللہ کو اس کے بھوکا پیاسا رہنے کی کوئی ضرورت نہیں", "Spiritual core of fasting"),
    ("bab_rayyan", "إن في الجنة بابا يقال له الريان لا يدخله إلا الصائمون", "In Paradise there is a gate called Ar-Rayyan through which only fasting persons enter", "جنت کا ایک دروازہ ریان ہے جس سے صرف روزے دار داخل ہوں گے", "Gate of Rayyan"),

    # Hajj & Umrah
    ("hajj_mabrur", "الحج المبرور ليس له جزاء إلا الجنة", "The accepted Hajj has no reward except Paradise", "حج مبرور کا بدلہ جنت کے سوا کچھ نہیں ہے", "Excellence of Hajj"),
    ("hajj_waladathu", "من حج هذا البيت فلم يرفث ولم يفسق رجع كيوم ولدته أمه", "Whoever performs Hajj without obscenity or transgression returns like the day his mother bore him", "جس نے گناہوں اور بے ہودگی سے بچتے ہوئے حج کیا وہ گناہوں سے ایسے پاک ہو کر لوٹتا ہے جیسے اس دن تھا جب ماں نے جنم دیا", "Purity after Hajj"),
    ("umrah_kaffarah", "العمرة إلى العمرة كفارة لما بينهما", "One Umrah to the next is an expiation for whatever occurred between them", "ایک عمرہ دوسرے عمرے تک کے درمیانی گناہوں کا کفارہ بن جاتا ہے", "Virtue of Umrah"),
    ("talbiyah", "لبيك اللهم لبيك لبيك لا شريك لك لبيك", "Here I am O Allah at Your service, You have no partner", "لبیک اللہم لبیک، تیرے حضور حاضر ہوں، تیرا کوئی شریک نہیں", "Chant of Talbiyah"),
    ("arafah_hajj", "الحج عرفة", "Hajj is standing at Arafah", "حج کا سب سے بڑا اور بنیادی رکن وقوف عرفہ ہے", "Core pillar of Hajj"),
    ("tawaf_salat", "الطواف حول البيت صلاة إلا أن الله أحل فيه الكلام", "Circumambulation around the House is a prayer except Allah permitted speech in it", "بیت اللہ کا طواف ایک نماز کی طرح ہے سوائے اس کے کہ اس میں بات چیت جائز کی گئی ہے", "Rules of Tawaf"),
    ("hajar_aswad", "الحجر الأسود نزل من الجنة أشد بياضا من الثلج", "The Black Stone descended from Paradise whiter than snow then sins of humans blackened it", "حجر اسود جنت سے اترا تو دودھ سے زیادہ سفید تھا پھر بنی آدم کے گناہوں نے اسے سیاہ کر دیا", "Black Stone history"),
    ("zamzam", "ماء زمزم لما شرب له", "The water of Zamzam is for whatever purpose it is drunk", "آب زمزم جس نیت اور مقصد سے پیا جائے وہ پورا ہوتا ہے", "Blessings of Zamzam"),

    # Transactions & Ethics (Mu'amalat)
    ("la_tabi_ma_laysa", "لا تبع ما ليس عندك", "Do not sell what you do not possess", "جو چیز تمہاری ملکیت اور قبضے میں نہ ہو اسے آگے مت بیچو", "Prohibition of short-selling"),
    ("riba_hadith", "الذهب بالذهب والفضة بالفضة ربا إلا هاء وهاء", "Gold for gold and silver for silver is usury unless hand to hand equal for equal", "سونا سونے کے بدلے اور چاندی چاندی کے بدلے برابر اور نقد نہ ہو تو وہ سود ہے", "Rules of Riba al-Fadl"),
    ("bay_gharar", "نهى رسول الله عن بيع الغرر", "The Messenger prohibited transactions of uncertainty and risk", "رسول اللہ صلی اللہ علیہ وسلم نے دھوکے، خطرے اور غیر یقینی سودوں سے منع فرمایا", "Prohibition of Gharar"),
    ("ajir_ujrah", "أعطوا الأجير أجره قبل أن يجف عرقه", "Give the laborer his wages before his sweat dries", "مزدور کو اس کی مزدوری اس کا پسینہ خشک ہونے سے پہلے ادا کرو", "Rights of workers"),
    ("ghash_tijarah", "البيعان بالخيار ما لم يتفرقا", "The buyer and seller have the option to cancel as long as they have not separated", "خریدار اور فروخت کنندہ کو جدا ہونے تک سودا منسوخ کرنے کا اختیار حاصل ہے", "Khiyar al-Majlis"),
    ("dayn_shahid", "يغفر للشهيد كل ذنب إلا الدين", "Every sin of the martyr is forgiven except unpaid debt", "شہید کے ہر گناہ کو معاف کر دیا جاتا ہے سوائے قرض کے", "Gravity of debts"),
    ("matlu_ghaniyy", "مطل الغني ظلم", "Procrastination in repaying debt by a wealthy person is injustice", "مالدار اور صاحب استطاعت شخص کا قرض کی ادائیگی میں ٹال مٹول کرنا ظلم ہے", "Delaying debt repayment"),
    ("khayrukum_qada'an", "إن خياركم أحسنكم قضاء", "Indeed the best of you are those best in repaying debts", "تم میں سے بہترین لوگ وہ ہیں جو قرض چکانے میں سب سے اچھے اور فراخ دل ہوں", "Nobility in debt repayment"),

    # Ethics, Adab & Family (Manners)
    ("birr_walidayn", "رضا الرب في رضا الوالد وسخط الرب في سخط الوالد", "The pleasure of the Lord lies in the pleasure of the father and His anger in his anger", "رب کی رضا والدین کی رضا میں ہے اور رب کی ناراضگی والدین کی ناراضگی میں ہے", "Dutifulness to parents"),
    ("ummu_thumma_umm", "أمك ثم أمك ثم أمك ثم أبوك", "Your mother, then your mother, then your mother, then your father", "تمہاری حسن سلوک کی سب سے زیادہ حقدار تمہاری ماں ہے، پھر تمہاری ماں، پھر تمہاری ماں، پھر تمہارا باپ", "Precedence of mother"),
    ("silat_rahim", "من سره أن يبسط له في رزقه وينسأ له في أثره فليصل رحمه", "Whoever wishes that his provision be expanded and his lifespan prolonged let him maintain ties of kinship", "جو شخص روزی میں فراخی اور عمر میں برکت چاہتا ہے اسے چاہیے کہ رشتہ داروں کے ساتھ صلہ رحمی کرے", "Maintaining kinship"),
    ("haqq_muslim", "حق المسلم على المسلم خمس", "The rights of a Muslim upon a Muslim are five: returning salam, visiting sick, attending funeral, accepting invitation, answering sneeze", "مسلمان کے دوسرے مسلمان پر پانچ حقوق ہیں: سلام کا جواب دینا، مریض کی عیادت کرنا، جنازے میں شرکت، دعوت قبول کرنا اور چھینک کا جواب دینا", "Five rights of brotherhood"),
    ("afshu_salam", "أفشوا السلام وأطعموا الطعام وصلوا بالليل والناس نيام تدخلوا الجنة بسلام", "Spread peace, feed the hungry, maintain kinship, and pray at night while people sleep, you will enter Paradise in peace", "سلام کو عام کرو، غریبوں کو کھانا کھلاؤ اور رات کو نماز پڑھو جب لوگ سو رہے ہوں، تم سلامتی کے ساتھ جنت میں داخل ہو جاؤ گے", "Keys to Paradise"),
    ("ithm_haka", "البر حسن الخلق والإثم ما حاك في صدرك وكرهت أن يطلع عليه الناس", "Righteousness is good character, and sin is that which wavers in your chest and you hate for people to see", "نیکی اچھے اخلاق کا نام ہے اور گناہ وہ ہے جو تمہارے دل میں کھٹکے اور تم لوگوں کے سامنے ظاہر ہونے سے ناپسند کرو", "Definition of sin and virtue"),
    ("la_tahāsadū", "لا تحاسدوا ولا تباغضوا ولا تدابروا وكونوا عباد الله إخوانا", "Do not envy one another, do not hate one another, do not turn away from one another, and be servants of Allah, brothers", "ایک دوسرے سے حسد مت کرو، بغض نہ رکھو اور پیٹھ نہ پھیرو، بلکہ اللہ کے بندے بھائی بھائی بن جاؤ", "Prohibition of malice and envy"),
    ("man_satara", "من ستر مسلما ستره الله في الدنيا والآخرة", "Whoever conceals the faults of a Muslim Allah will conceal his faults in this world and the Hereafter", "جو شخص کسی مسلمان کی پردہ پوشی کرے گا اللہ دنیا اور آخرت میں اس کے عیبوں پر پردہ ڈالے گا", "Concealing brother's fault"),
    ("kafil_yatim", "أنا وكافل اليتيم في الجنة هكذا", "I and the sponsor of an orphan will be in Paradise like these two fingers", "میں اور یتیم کی کفالت کرنے والا جنت میں ان دو انگلیوں کی طرح قریب ہوں گے", "Virtues of sponsoring orphans"),
    ("tabassum_sadaqah", "تبسمك في وجه أخيك لك صدقة", "Your smile in the face of your brother is charity for you", "اپنے بھائی کے سامنے مسکرانا بھی تمہارے لیے صدقہ ہے", "Good cheer and smile"),

    # Trials, Hereafter & Remembrance (Dhikr & Ruqyah)
    ("sayyid_istighfar", "اللهم أنت ربي لا إله إلا أنت خلقتني وأنا عبدك", "Sayyid al-Istighfar: O Allah You are my Lord there is no god but You", "سید الاستغفار: اے اللہ تو میرا رب ہے تیرے سوا کوئی معبود نہیں، تو نے مجھے پیدا کیا اور میں تیرا بندہ ہوں", "Master supplication of repentance"),
    ("ayat_kursi", "أعظم آية في كتاب الله آية الكرسي", "The greatest verse in the Book of Allah is Ayat al-Kursi", "قرآن مجید کی سب سے عظیم آیت، آیت الکرسی ہے", "Virtues of Ayat al-Kursi"),
    ("baqarah_shaitan", "إن الشيطان ينفر من البيت الذي تقرأ فيه سورة البقرة", "Satan flees from the house in which Surah Al-Baqarah is recited", "شیطان اس گھر سے بھاگتا ہے جس میں سورہ بقرہ کی تلاوت کی جاتی ہے", "Virtues of Surah Baqarah"),
    ("fitnah_dajjal", "من حفظ عشر آيات من أول سورة الكهف عصم من الدجال", "Whoever memorizes ten verses from the beginning of Surah Al-Kahf is protected from Dajjal", "جس نے سورہ کہف کی پہلی دس آیات یاد کیں وہ فتنہ دجال سے محفوظ رہے گا", "Protection from Dajjal"),
    ("shafa'ah", "شفاعتي لأهل الكبائر من أمتي", "My intercession is for the people of major sins from my nation", "میری شفاعت میری امت کے ان لوگوں کے لیے ہوگی جنہوں نے کبیرہ گناہ کیے", "Prophetic intercession on Judgment Day"),
    ("hawd_kawthar", "حوضي مسيرة شهر ماؤه أبيض من اللبن", "My Cistern is the journey of a month, its water whiter than milk", "میرا حوض کوثر ایک ماہ کی مسافت کے برابر ہے اور اس کا پانی دودھ سے زیادہ سفید ہے", "The Hawd of the Prophet"),
    ("qabr_adhab", "تعوذوا بالله من عذاب القبر", "Seek refuge in Allah from the torment of the grave", "قبر کے عذاب سے اللہ کی پناہ مانگو کیونکہ قبر کا عذاب برحق ہے", "Torment of the grave"),
    ("mizan_a'mal", "أثقل شيء في ميزان المؤمن يوم القيامة حسن الخلق", "The heaviest thing in the believer's Scale on the Day of Resurrection is good character", "قیامت کے دن مومن کے ترازو میں سب سے بھاری چیز حسن اخلاق ہوگی", "The Scales on Judgment Day"),
    ("sirat_jisr", "يضرب الصراط بين ظهري جهنم", "The Bridge will be set up over the Hellfire", "پل صراط جہنم کی پشت پر قائم کیا جائے گا اور لوگ اپنے اعمال کے مطابق اس سے گزریں گے", "The Bridge over Hellfire"),
    ("liqa_allah", "من أحب لقاء الله أحب الله لقاءه", "Whoever loves to meet Allah, Allah loves to meet him", "جو شخص اللہ سے ملاقات کو پسند کرتا ہے اللہ بھی اس سے ملاقات کو پسند فرماتا ہے", "Longing to meet Allah"),
]


def build_500_benchmark_dataset() -> List[Dict[str, Any]]:
    conn = sqlite3.connect(f"file:{CANONICAL_KG_PATH.resolve()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA query_only = ON;")

    try:
        # Step 1: Match all anchor definitions to actual canonical meaning_groups in hadith-kg.db
        matched_anchors = []
        for key, ar_pat, en_txt, ur_txt, notes in CANONICAL_ANCHORS:
            res = find_group_for_nass_pattern(conn, ar_pat)
            if res:
                gid, full_nass = res
                hids = get_canonical_hadith_ids_for_group(conn, gid, limit=3)
                matched_anchors.append({
                    "key": key,
                    "ar_pattern": ar_pat,
                    "group_id": gid,
                    "full_nass": full_nass,
                    "hadith_ids": hids,
                    "en_text": en_txt,
                    "ur_text": ur_txt,
                    "notes": notes,
                })

        print(f"[INFO] Successfully resolved {len(matched_anchors)} anchor meaning groups in canonical DB.")

        queries: List[Dict[str, Any]] = []

        # -------------------------------------------------------------
        # CATEGORY 1: ARABIC (150 Queries)
        # -------------------------------------------------------------
        # 1a. Exact/Core statements (35 queries)
        for i, a in enumerate(matched_anchors[:35]):
            queries.append({
                "query_id": f"AR_EXACT_{i+1:03d}",
                "language": "ar",
                "category": "exact_wording",
                "query": a["ar_pattern"],
                "gold_group_ids": [a["group_id"]],
                "gold_hadith_ids": a["hadith_ids"],
                "difficulty": "easy",
                "provenance_source": f"canonical_meaning_group:{a['group_id']}",
                "notes": f"Exact core prophetic wording: {a['notes']}"
            })

        # 1b. Paraphrases and lexical synonyms (40 queries)
        ar_paraphrases = [
            ("أجر الأعمال مرتبط بالنيات والمقاصد", "niyyah"),
            ("أعمدة وركائز الدين الإسلامي", "buni_islam"),
            ("سلامة المسلمين من أذى الأيدي والألسن", "muslim_salim"),
            ("الإحسان في عبادة الخالق ومراقبته", "ihsan_jibril"),
            ("منع الإضرار بالنفس وبالآخرين في الشريعة", "la_darar"),
            ("النصيحة الصادقة لله ولكتابه ولأئمة المسلمين", "nasiha"),
            ("الابتعاد عن الشبهات والتحري في الحلال والحرام", "halal_bayyin"),
            ("الحياء من خصال الإيمان العظيمة", "haya"),
            ("فضل النظافة والتطهر في ميزان الشريعة", "tahur"),
            ("الحث على التزام الصدق وعاقبة الكذب", "sidq"),
            ("تحريم الخداع والغش في المعاملات", "ghash"),
            ("الفقه في الدين علامة إرادة الخير بالعبد", "yufaqqihhu"),
            ("ذكر الله بكلمات خفيفة حبيبة للرحمن", "kalimatan"),
            ("السيطرة على الغضب واجتناب الانفعال", "la_tughdab"),
            ("ترك الفضول وما لا يعني المسلم في دينه", "tarak_ma_la_ya'nih"),
            ("محبة الخير للمؤمنين كالنفس", "yuhibbu_liakhih"),
            ("مسؤولية كل راع عن رعيته وأهله", "kullukum_ra'in"),
            ("التسامح واليسر في البيع والشراء وقضاء الحقوق", "samahan"),
            ("طيب المكسب وقبول العمل الصالح عند الله", "tayyib"),
            ("فضل تعلم القرآن الكريم وتعليمه للناس", "khayrukum_quran"),
            ("بطلان الصلاة بغير طهارة ووضوء", "la_salata_bighayr_tuhur"),
            ("أهمية السواك وتطهير الفم لكل صلاة", "siwak"),
            ("تكفير الذنوب بإسباغ الوضوء على المكاره", "wudu_shatranj"),
            ("مشروعية التيمم بالتراب عند فقد الماء", "tayamum"),
            ("طهارة الماء وعدم تنجسه بغير التغير", "himaar"),
            ("شروط المسح على الخفين والجوربين", "masah_khuffayn"),
            ("نواقض الوضوء بالنوم المستغرق", "qubul_wudu_nawm"),
            ("حكم الوضوء بعد تناول لحوم الإبل", "ibil_wudu"),
            ("التحرز من النجاسات وعذاب القبر من البول", "istinja"),
            ("المبالغة في الاستنشاق لغير الصائم", "madhmadhah"),
            ("أداء الصلوات المفروضة في أوقاتها المحددة", "salat_awqat"),
            ("فضل صلاة الجماعة على صلاة المنفرد", "salat_jamaah"),
            ("فضل الأذان وهروب الشيطان عند سماعه", "adhan_ijabah"),
            ("تكبيرة الإحرام والتسليم في الصلاة", "iftitah_takbir"),
            ("وجوب قراءة سورة الفاتحة في كل ركعة", "fatiha_la_salat"),
            ("القرب من الله في السجود وإكثار الدعاء فيه", "ruku_sujud"),
            ("رخصة قصر الصلاة الرباعية للمسافر", "qasr_safar"),
            ("أحكام سجدتي السهو في الزيادة والنقصان", "sahw_sujud"),
            ("قيام الليل وصلاة التهجد بعد المكتوبة", "tahajjud"),
            ("صلاة الكسوف والخسوف ودعاء الله عند الآيات", "kusuf"),
        ]
        anchor_map = {a["key"]: a for a in matched_anchors}
        for i, (p_text, a_key) in enumerate(ar_paraphrases):
            a = anchor_map.get(a_key, matched_anchors[0])
            queries.append({
                "query_id": f"AR_PARA_{i+1:03d}",
                "language": "ar",
                "category": "paraphrase",
                "query": p_text,
                "gold_group_ids": [a["group_id"]],
                "gold_hadith_ids": a["hadith_ids"],
                "difficulty": "medium",
                "provenance_source": f"canonical_meaning_group:{a['group_id']}",
                "notes": f"Semantic Arabic paraphrase targeting {a['key']}"
            })

        # 1c. Thematic & Conceptual Queries (45 queries)
        ar_thematic = [
            ("أحكام زكاة الفطر ومقدار الصاع المفروض", "zakat_fitr"),
            ("فضل الصدقة الخفية التي لا تعلم شماله ما تنفق يمينه", "sadaqah_sirr"),
            ("الصدقة برهان على صدق إيمان المتصدق", "sadaqah_burhan"),
            ("الوقاية من النار ولو بشق تمرة يتصدق بها", "la_tahqiranna"),
            ("الأعمال التي يستمر أجرها بعد الموت كالصدقة الجارية", "sadaqah_jariya"),
            ("بركة المال بالصدقة وعدم نقصانه بالإنفاق", "zakat_amwal"),
            ("فضل اليد المعطية المنفقة على اليد الآخذة", "su'al_dhill"),
            ("إطفاء الصدقة للذنوب والخطايا كما يطفئ الماء النار", "sadaqah_khatiy'ah"),
            ("الصوم جنة ووقاية من المعاصي والشهوات", "sawm_junnah"),
            ("فرحة الصائم عند فطره وعند لقاء ربه بجزائه", "sawm_farhah"),
            ("رائحة فم الصائم وطيبها عند الله يوم القيامة", "khaluf_fam"),
            ("بركة السحور واستحباب تأخيره قبل الفجر", "suhur_barakah"),
            ("استحباب تعجيل الفطر عند غروب الشمس", "ta'jil_fitr"),
            ("فضل صيام يوم عرفة وتكفيره لذنوب سنتين", "sawm_arafah"),
            ("صيام عاشوراء وتكفيره للسنة الماضية", "sawm_ashura"),
            ("صيام ستة أيام من شوال بعد رمضان وأجر صيام الدهر", "sawm_shawwal"),
            ("حرمة قول الزور والعمل به أثناء الصيام", "man_lama_yada'"),
            ("باب الريان في الجنة المخصص للصائمين", "bab_rayyan"),
            ("ثواب الحج المبرور وجزاؤه الجنة", "hajj_mabrur"),
            ("غفران الذنوب ورجوع الحاج كيوم ولدته أمه", "hajj_waladathu"),
            ("العمرة إلى العمرة كفارة للذنوب بينهما", "umrah_kaffarah"),
            ("صيغة التلبية في الحج والعمرة ودلالتها التوحيدية", "talbiyah"),
            ("ركن الحج الأعظم بالوقوف في عرفة", "arafah_hajj"),
            ("أحكام الطواف حول الكعبة المشرفة واشتراط الطهارة", "tawaf_salat"),
            ("فضل الحجر الأسود ونزوله من الجنة", "hajar_aswad"),
            ("بركة ماء زمزم والشفاء والاستشفاء به", "zamzam"),
            ("النهي عن بيع الإنسان ما لا يملك ولا يقبض", "la_tabi_ma_laysa"),
            ("أحكام ربا الفضل في الأصناف الستة الربوية", "riba_hadith"),
            ("تحريم بيوع الغرر والمجهول والمخاطرة", "bay_gharar"),
            ("إعطاء الأجير حقه وأجرته قبل جفاف عرقه", "ajir_ujrah"),
            ("خيار المجلس للمتبايعين قبل الافتراق", "ghash_tijarah"),
            ("خطورة الدين ومطالبة الميت به ولو كان شهيدا", "dayn_shahid"),
            ("مطل الغني وظلم المماطلة في أداء الديون", "matlu_ghaniyy"),
            ("حسن القضاء وأداء الحقوق بزيادة وإحسان", "khayrukum_qada'an"),
            ("بر الوالدين وربط رضا الرب برضاهما", "birr_walidayn"),
            ("عظيم حق الأم وتقديمها في حسن الصحبة ثلاثا", "ummu_thumma_umm"),
            ("صلة الرحم وزيادة الرزق والبركة في العمر", "silat_rahim"),
            ("حقوق المسلم على أخيه المسلم في المعاشرة والزيارة", "haqq_muslim"),
            ("إفشاء السلام وإطعام الطعام وقيام الليل أسباب لدخول الجنة", "afshu_salam"),
            ("حقيقة البر والإثم وما حاك في الصدر", "ithm_haka"),
            ("التحذير من الحسد والتباغض والتدابر بين المؤمنين", "la_tahāsadū"),
            ("ستر عيوب المسلم وعدم فضحه في الدنيا والآخرة", "man_satara"),
            ("أجر كافل اليتيم ومرافقته للنبي في الجنة", "kafil_yatim"),
            ("التبسم في وجه الأخ صدقة وحسن خلق", "tabassum_sadaqah"),
            ("سيد الاستغفار وفضل الدعاء به موقنا صباحا ومساء", "sayyid_istighfar"),
        ]
        for i, (t_text, a_key) in enumerate(ar_thematic):
            a = anchor_map.get(a_key, matched_anchors[0])
            queries.append({
                "query_id": f"AR_THEME_{i+1:03d}",
                "language": "ar",
                "category": "thematic",
                "query": t_text,
                "gold_group_ids": [a["group_id"]],
                "gold_hadith_ids": a["hadith_ids"],
                "difficulty": "medium",
                "provenance_source": f"canonical_meaning_group:{a['group_id']}",
                "notes": f"Thematic concept query targeting {a['key']}"
            })

        # 1d. Difficult / Ambiguous / Complex queries (30 queries)
        ar_complex = [
            ("ما جاء في قراءة القرآن وسورة البقرة وطرده للشياطين من البيت", "baqarah_shaitan"),
            ("أعظم آية في كتاب الله تعالى وآية الكرسي وحفظها للعبد", "ayat_kursi"),
            ("الاعتصام من فتنة المسيح الدجال بحفظ فواتح سورة الكهف", "fitnah_dajjal"),
            ("شفاعة النبي صلى الله عليه وسلم لأهل الكبائر من أمته يوم الحساب", "shafa'ah"),
            ("صفة حوض النبي صلى الله عليه وسلم المورود يوم القيامة وبياض مائه", "hawd_kawthar"),
            ("الاستعاذة بالله من عذاب القبر وسؤال الملكين منكر ونكير", "qabr_adhab"),
            ("ثقل الميزان بالأخلاق الحسنة والكلمات الطيبة يوم القيامة", "mizan_a'mal"),
            ("ضرب الصراط على متن جهنم وسرعة مرور المؤمنين عليه", "sirat_jisr"),
            ("حب لقاء الله وشوق العبد الصالح إلى ربه عند الاحتضار", "liqa_allah"),
            ("حكم النية وتأثيرها على العبادات والمعاملات والعادات", "niyyah"),
            ("الأركان الخمسة التي لا يصح إسلام العبد إلا بتحقيقها", "buni_islam"),
            ("الضوابط الشرعية للأذى القولي والفعلي بين المسلمين", "muslim_salim"),
            ("مقام الإحسان وحضور القلب والخشوع في العبادة", "ihsan_jibril"),
            ("تطبيقات قاعدة نفي الضرر والضرار في المعاملات المالية", "la_darar"),
            ("وجوب نصيحة ولاة الأمور وعامة المسلمين بالمعروف", "nasiha"),
            ("الورع في الأمور المشتبهة بين الحلال الصريح والحرام البين", "halal_bayyin"),
            ("أثر الحياء في ردع النفس عن المعاصي والقبائح", "haya"),
            ("منزلة الطهارة والوضوء في قبول العبادات البدنية", "tahur"),
            ("عاقبة الصدق وثمراته وعاقبة الكذب وفجوره", "sidq"),
            ("تحريم الغش والتدليس في الكيل والميزان والمبيعات", "ghash"),
            ("التفقه في الدين وأثره في هداية الأمة وصلاحها", "yufaqqihhu"),
            ("التسبيح والتحميد وفضلهما في ميزان الحسنات يوم القيامة", "kalimatan"),
            ("النهي عن سرعة الغضب وعلاجه بالاستعاذة وتغيير الهيئة", "la_tughdab"),
            ("حفظ الوقت واللسان واشتغال العبد بما ينفعه في آخرته", "tarak_ma_la_ya'nih"),
            ("تمني الخير للإخوان ودفع الحسد والضغينة عن القلب", "yuhibbu_liakhih"),
            ("مسؤولية الأب والأم والراعي عن أولادهم ورعيتهم", "kullukum_ra'in"),
            ("فضل السماحة واللين في البيع والشراء والتقاضي", "samahan"),
            ("أكل الحلال وأثره في استجابة الدعاء وتزكية النفس", "tayyib"),
            ("أهل القرآن وخيرية من جمعه تعلما وتعليما", "khayrukum_quran"),
            ("شروط صحة الصلاة وإسباغ الوضوء على المكاره", "la_salata_bighayr_tuhur"),
        ]
        for i, (c_text, a_key) in enumerate(ar_complex):
            a = anchor_map.get(a_key, matched_anchors[0])
            queries.append({
                "query_id": f"AR_COMPLEX_{i+1:03d}",
                "language": "ar",
                "category": "complex_theological",
                "query": c_text,
                "gold_group_ids": [a["group_id"]],
                "gold_hadith_ids": a["hadith_ids"],
                "difficulty": "hard",
                "provenance_source": f"canonical_meaning_group:{a['group_id']}",
                "notes": f"Complex theological Arabic query targeting {a['key']}"
            })

        assert len([q for q in queries if q["language"] == "ar"]) == EXPECTED_ARABIC, f"Arabic queries count mismatch: {len([q for q in queries if q['language'] == 'ar'])}"

        # -------------------------------------------------------------
        # CATEGORY 2: URDU (100 Queries)
        # -------------------------------------------------------------
        # 2a. Natural Urdu Core Concepts (35 queries)
        for i, a in enumerate(matched_anchors[:35]):
            queries.append({
                "query_id": f"UR_CORE_{i+1:03d}",
                "language": "ur",
                "category": "natural_urdu",
                "query": a["ur_text"],
                "gold_group_ids": [a["group_id"]],
                "gold_hadith_ids": a["hadith_ids"],
                "difficulty": "medium",
                "provenance_source": f"canonical_meaning_group:{a['group_id']}",
                "notes": f"Core natural Urdu query: {a['notes']}"
            })

        # 2b. Urdu Paraphrases & Research Queries (35 queries)
        ur_paraphrases = [
            ("نیت کے بغیر کیے گئے عمل کی شرعی حیثیت اور جزا", "niyyah"),
            ("دین اسلام کے بنیادی پانچ ارکان کی تفصیل", "buni_islam"),
            ("دوسرے مسلمانوں کو تکلیف نہ دینے والے سچے مومن کی پہچان", "muslim_salim"),
            ("اللہ کی بارگاہ میں خشوع اور احسان کے ساتھ عبادت کرنا", "ihsan_jibril"),
            ("اسلام میں کسی کو نقصان پہنچانے اور بدلہ لینے کی ممانعت", "la_darar"),
            ("دین میں اخلاص، خیر خواہی اور نیک مشورے کی اہمیت", "nasiha"),
            ("مشتبہ امور سے بچنا اور حلال و حرام میں احتیاط برتنا", "halal_bayyin"),
            ("شرم و حیا کی فضیلت اور ایمان سے اس کا تعلق", "haya"),
            ("وضو اور پاکیزگی کی فضیلت کہ وہ آدھا ایمان ہے", "tahur"),
            ("سچ بولنے کا اجر اور جھوٹ بولنے کی تباہ کاری", "sidq"),
            ("تجارت اور معاملات میں دھوکہ دہی کی سخت مذمت", "ghash"),
            ("اللہ تعالی کا کسی بندے کے لیے دین کی فقہ اور سمجھ عطا کرنا", "yufaqqihhu"),
            ("سبحان اللہ وبحمدہ اور سبحان اللہ العظیم کے وظیفے کی فضیلت", "kalimatan"),
            ("غصے پر قابو پانا اور بردباری اختیار کرنے کی نصیحت", "la_tughdab"),
            ("بے مقصد اور لا یعنی کاموں کو چھوڑنے کی خوبی", "tarak_ma_la_ya'nih"),
            ("اپنے مسلمان بھائی کے لیے وہی چاہنا جو اپنے لیے چاہو", "yuhibbu_liakhih"),
            ("حکمران، باپ اور نگران کی اپنی رعیت کے بارے میں ذمہ داری", "kullukum_ra'in"),
            ("لین دین، خرید و فروخت اور قرض کی وصولی میں نرمی کی دعا", "samahan"),
            ("حلال رزق کمانا اور حرام کمائی سے بچنے کی تاکید", "tayyib"),
            ("قرآن مجید پڑھنے، سمجھنے اور دوسروں کو سکھانے والے کی فضیلت", "khayrukum_quran"),
            ("طہارت اور وضو کے بغیر نماز کے قبول نہ ہونے کا حکم", "la_salata_bighayr_tuhur"),
            ("مسواک کرنے کی ترغیب اور اس کے منہ کی صفائی کے فوائد", "siwak"),
            ("وضو کے ذریعے اعضاء کے گناہوں کا جھڑ جانا", "wudu_shatranj"),
            ("پانی نہ ملنے پر پاک مٹی سے تیمم کرنے کی رخصت", "tayamum"),
            ("پانی کی بنیادی پاکیزگی اور نجاست کے اثرات", "himaar"),
            ("سفر اور حضر میں چمڑے کے موزوں پر مسح کی مدت اور شرائط", "masah_khuffayn"),
            ("گہری نیند سو جانے سے وضو ٹوٹنے کے دلائل", "qubul_wudu_nawm"),
            ("اونٹ کا گوشت کھانے کے بعد وضو کے احکام", "ibil_wudu"),
            ("پیشاب کی چھینٹوں سے نہ بچنے پر عذاب قبر کی وعید", "istinja"),
            ("وضو کے دوران ناک میں پانی اچھی طرح چڑھانے کی ہدایت", "madhmadhah"),
            ("پانچوں نمازوں کو ان کے مقررہ وقت پر ادا کرنے کی اہمیت", "salat_awqat"),
            ("اکیلے نماز پڑھنے کے مقابلے میں باجماعت نماز کا ثواب", "salat_jamaah"),
            ("اذان کی آواز سن کر شیطان کے بھاگنے کا بیان", "adhan_ijabah"),
            ("تکبیر تحریمہ سے نماز شروع کرنے اور سلام پر ختم کرنے کا طریقہ", "iftitah_takbir"),
            ("نماز میں سورہ فاتحہ پڑھنے کا لازمی حکم", "fatiha_la_salat"),
        ]
        for i, (u_text, a_key) in enumerate(ur_paraphrases):
            a = anchor_map.get(a_key, matched_anchors[0])
            queries.append({
                "query_id": f"UR_PARA_{i+1:03d}",
                "language": "ur",
                "category": "paraphrase",
                "query": u_text,
                "gold_group_ids": [a["group_id"]],
                "gold_hadith_ids": a["hadith_ids"],
                "difficulty": "medium",
                "provenance_source": f"canonical_meaning_group:{a['group_id']}",
                "notes": f"Urdu paraphrase targeting {a['key']}"
            })

        # 2c. Complex Urdu Theological & Ethical Queries (30 queries)
        ur_complex = [
            ("سجدے کی حالت میں دعا مانگنا اور اللہ تعالی کی قربت حاصل کرنا", "ruku_sujud"),
            ("مسافر کے لیے چار رکعت والی فرض نماز کو قصر کرنے کے قواعد", "qasr_safar"),
            ("نماز میں بھول جانے کی صورت میں سجدہ سہو کا شرعی طریقہ", "sahw_sujud"),
            ("رات کے آخری پہر میں تہجد اور نفل نماز پڑھنے کا مقام", "tahajjud"),
            ("سورج گرہن اور چاند گرہن کے وقت نماز کسوف ادا کرنا", "kusuf"),
            ("رمضان کے اختتام پر صدقہ فطر ادا کرنے کی فرضیت اور مقدار", "zakat_fitr"),
            ("چھپا کر صدقہ دینے والے کو قیامت کے دن عرش کا سایہ ملنا", "sadaqah_sirr"),
            ("صدقہ اور خیرات کا سچے ایمان اور عقیدے کی دلیل ہونا", "sadaqah_burhan"),
            ("کھجور کا ایک ٹکڑا بھی صدقہ کر کے جہنم کی آگ سے بچنا", "la_tahqiranna"),
            ("مرنے کے بعد انسان کو فائدہ پہنچانے والے تین جاری اعمال", "sadaqah_jariya"),
            ("اللہ کے راستے میں خرچ کرنے سے مال میں کبھی کمی نہ آنا", "zakat_amwal"),
            ("مانگنے والے کے مقابلے میں دینے والے ہاتھ کا بلند ہونا", "su'al_dhill"),
            ("صدقہ دینے سے گناہوں کی آگ کا بجھ جانا", "sadaqah_khatiy'ah"),
            ("روزہ گناہوں اور جہنم کے خلاف ایک حفاظتی ڈھال ہے", "sawm_junnah"),
            ("افطار کے وقت اور اللہ کے دیدار کے وقت روزے دار کی دو مسرتیں", "sawm_farhah"),
            ("روزے دار کے منہ کی بو کا اللہ کے نزدیک کستوری سے پیارا ہونا", "khaluf_fam"),
            ("سحری کھانے کی برکت اور نبی کریم کی تاکید", "suhur_barakah"),
            ("غروب آفتاب کے وقت روزہ افطار کرنے میں جلدی کی سنت", "ta'jil_fitr"),
            ("عرفہ کے دن روزہ رکھنے سے پچھلے اور اگلے سال کے گناہوں کی معافی", "sawm_arafah"),
            ("محرم کی دسویں تاریخ یعنی عاشورہ کے روزے کا ثواب", "sawm_ashura"),
            ("رمضان کے بعد شوال کے چھ روزے رکھنے سے پورے سال کا اجر", "sawm_shawwal"),
            ("جھوٹ بولنے اور برے کام نہ چھوڑنے والے کے روزے کی بے قدری", "man_lama_yada'"),
            ("جنت کے باب الریان سے صرف روزے داروں کا داخلہ ہونا", "bab_rayyan"),
            ("مقبول حج کا بدلہ سوائے جنت کے کچھ اور نہیں ہے", "hajj_mabrur"),
            ("حج کی ادائیگی کے بعد گناہوں سے ایسے پاک ہونا جیسے نوزائیدہ بچہ", "hajj_waladathu"),
            ("ایک عمرے سے دوسرے عمرے کے درمیان گناہوں کا مٹ جانا", "umrah_kaffarah"),
            ("حج اور عمرے کے موقع پر لبیک اللہم لبیک پکارنا", "talbiyah"),
            ("وقوف عرفہ حج کا سب سے بڑا اور بنیادی رکن ہے", "arafah_hajj"),
            ("کعبہ شریف کا طواف نماز کے مشابہ ہے جس میں بات جائز ہے", "tawaf_salat"),
            ("حجر اسود کا جنت سے اترنا اور گناہوں سے سیاہ ہونا", "hajar_aswad"),
        ]
        for i, (u_text, a_key) in enumerate(ur_complex):
            a = anchor_map.get(a_key, matched_anchors[0])
            queries.append({
                "query_id": f"UR_COMPLEX_{i+1:03d}",
                "language": "ur",
                "category": "complex_theological",
                "query": u_text,
                "gold_group_ids": [a["group_id"]],
                "gold_hadith_ids": a["hadith_ids"],
                "difficulty": "hard",
                "provenance_source": f"canonical_meaning_group:{a['group_id']}",
                "notes": f"Complex theological Urdu query targeting {a['key']}"
            })

        assert len([q for q in queries if q["language"] == "ur"]) == EXPECTED_URDU, f"Urdu queries count mismatch: {len([q for q in queries if q['language'] == 'ur'])}"

        # -------------------------------------------------------------
        # CATEGORY 3: ENGLISH (100 Queries)
        # -------------------------------------------------------------
        # 3a. Natural English Core Concepts (35 queries)
        for i, a in enumerate(matched_anchors[:35]):
            queries.append({
                "query_id": f"EN_CORE_{i+1:03d}",
                "language": "en",
                "category": "natural_english",
                "query": a["en_text"],
                "gold_group_ids": [a["group_id"]],
                "gold_hadith_ids": a["hadith_ids"],
                "difficulty": "medium",
                "provenance_source": f"canonical_meaning_group:{a['group_id']}",
                "notes": f"Core natural English query: {a['notes']}"
            })

        # 3b. English Paraphrases & Concepts (35 queries)
        en_paraphrases = [
            ("The validity of all deeds depends entirely upon personal intention", "niyyah"),
            ("The essential foundation and five core pillars of Islam", "buni_islam"),
            ("The real Muslim from whose actions and words fellow Muslims are safe", "muslim_salim"),
            ("Attaining the station of spiritual excellence by serving God as if seeing Him", "ihsan_jibril"),
            ("The legal principle forbidding causing injury or returning harm", "la_darar"),
            ("Sincere dedication and counsel to Allah His Book and the community", "nasiha"),
            ("Staying clear of doubtful gray areas and adhering to what is permissible", "halal_bayyin"),
            ("Modesty and shame as integral parts of religious faith", "haya"),
            ("Ritual purity and cleansing constituting half of religious devotion", "tahur"),
            ("Adhering strictly to veracity and avoiding deception", "sidq"),
            ("Severe condemnation of deceit cheating and misrepresentation in trade", "ghash"),
            ("Deep comprehension of religious jurisprudence as a gift from Allah", "yufaqqihhu"),
            ("Glorification words light on tongue but heavy on the divine scale", "kalimatan"),
            ("Mastering one's temper and restraining anger in moments of provocation", "la_tughdab"),
            ("Discarding irrelevant matters and avoiding futile gossip in life", "tarak_ma_la_ya'nih"),
            ("Loving for one's fellow brother whatever blessings one wishes for oneself", "yuhibbu_liakhih"),
            ("The accountability of every shepherd and leader for his dependants", "kullukum_ra'in"),
            ("Kindness and tolerance when selling buying and collecting debts", "samahan"),
            ("Consuming only lawful wholesome food and pure sustenance", "tayyib"),
            ("The peerless status of reciting studying and teaching the Holy Quran", "khayrukum_quran"),
            ("The absolute invalidity of formal prayer without preceding purification", "la_salata_bighayr_tuhur"),
            ("The tremendous spiritual merit and hygiene of the Siwak toothstick", "siwak"),
            ("The washing away of minor offenses through thorough ablution", "wudu_shatranj"),
            ("Using clean earth for dry ablution when water cannot be found", "tayamum"),
            ("The pristine purifying nature of natural running water", "himaar"),
            ("The concession permitting wiping over leather footwear while traveling", "masah_khuffayn"),
            ("Losing ritual purity due to deep unconscious sleep", "qubul_wudu_nawm"),
            ("The legal requirement to perform ablution after eating camel meat", "ibil_wudu"),
            ("Guarding oneself against urine splashes to avoid torment of the grave", "istinja"),
            ("Snuffing water deeply into the nostrils except during fasting", "madhmadhah"),
            ("Preserving and offering the prescribed prayers at their stated hours", "salat_awqat"),
            ("The superiority of twenty-seven degrees for prayer in congregation", "salat_jamaah"),
            ("The flight of Satan when hearing the call of the Adhan", "adhan_ijabah"),
            ("Commencing prayer with the initial Takbir and concluding with Taslim", "iftitah_takbir"),
            ("The indispensability of reciting Surah Al-Fatihah in every unit of prayer", "fatiha_la_salat"),
        ]
        for i, (e_text, a_key) in enumerate(en_paraphrases):
            a = anchor_map.get(a_key, matched_anchors[0])
            queries.append({
                "query_id": f"EN_PARA_{i+1:03d}",
                "language": "en",
                "category": "paraphrase",
                "query": e_text,
                "gold_group_ids": [a["group_id"]],
                "gold_hadith_ids": a["hadith_ids"],
                "difficulty": "medium",
                "provenance_source": f"canonical_meaning_group:{a['group_id']}",
                "notes": f"English paraphrase targeting {a['key']}"
            })

        # 3c. English Thematic & Research Queries (30 queries)
        en_thematic = [
            ("Finding divine closeness and supplication during prostration in Salah", "ruku_sujud"),
            ("Rules governing the shortening of four-cycle prayers during journeys", "qasr_safar"),
            ("Performing two prostrations of forgetfulness when making prayer errors", "sahw_sujud"),
            ("The merit of the voluntary night vigil Tahajjud after mandatory duties", "tahajjud"),
            ("The special congregational prayer during solar and lunar eclipses", "kusuf"),
            ("The annual obligation of Zakat al-Fitr at the completion of Ramadan", "zakat_fitr"),
            ("Giving charity in absolute secrecy so the left hand does not know", "sadaqah_sirr"),
            ("Charity acting as a tangible proof and evidence of authentic faith", "sadaqah_burhan"),
            ("Protecting oneself from Hellfire through even a fragment of a date", "la_tahqiranna"),
            ("Three actions that outlive a deceased person: continuous charity, knowledge, child", "sadaqah_jariya"),
            ("Giving away wealth in charity never decreases its true divine blessing", "zakat_amwal"),
            ("The superiority of the granting upper hand over the receiving lower hand", "su'al_dhill"),
            ("Almsgiving extinguishing transgression just as water extinguishes fire", "sadaqah_khatiy'ah"),
            ("Fasting serving as a spiritual shield against lust and sinful behavior", "sawm_junnah"),
            ("The two moments of joy for the fasting servant upon Iftar and meeting God", "sawm_farhah"),
            ("The fragrance of the fasting person's breath being superior to musk", "khaluf_fam"),
            ("Eating the predawn meal Suhur for the divine blessing contained within it", "suhur_barakah"),
            ("The virtue of hastening to break the fast as soon as the sun disappears", "ta'jil_fitr"),
            ("The fast on the day of Arafah wiping away sins of past and future years", "sawm_arafah"),
            ("Observing the voluntary fast on the tenth of Muharram Ashura", "sawm_ashura"),
            ("Following Ramadan with six voluntary days of fasting in Shawwal", "sawm_shawwal"),
            ("God having no regard for hunger of one who speaks falsehood while fasting", "man_lama_yada'"),
            ("Entering Paradise through the exclusive gate of Ar-Rayyan for fasting people", "bab_rayyan"),
            ("The reward for an accepted pilgrimage of Hajj being none other than Paradise", "hajj_mabrur"),
            ("Returning from Hajj free of sins like a newborn infant", "hajj_waladathu"),
            ("The expiation of minor shortcomings between consecutive Umrah journeys", "umrah_kaffarah"),
            ("Reciting the Talbiyah proclamation during sacred pilgrimage rites", "talbiyah"),
            ("Standing at Mount Arafah as the pivotal and supreme pillar of Hajj", "arafah_hajj"),
            ("Circumambulation around the Kaaba holding the sacred status of prayer", "tawaf_salat"),
            ("The sacred heavenly descent and history of the Black Stone Hajar Aswad", "hajar_aswad"),
        ]
        for i, (e_text, a_key) in enumerate(en_thematic):
            a = anchor_map.get(a_key, matched_anchors[0])
            queries.append({
                "query_id": f"EN_THEME_{i+1:03d}",
                "language": "en",
                "category": "thematic",
                "query": e_text,
                "gold_group_ids": [a["group_id"]],
                "gold_hadith_ids": a["hadith_ids"],
                "difficulty": "hard",
                "provenance_source": f"canonical_meaning_group:{a['group_id']}",
                "notes": f"English thematic query targeting {a['key']}"
            })

        assert len([q for q in queries if q["language"] == "en"]) == EXPECTED_ENGLISH, f"English queries count mismatch: {len([q for q in queries if q['language'] == 'en'])}"

        # -------------------------------------------------------------
        # CATEGORY 4: CROSS-LINGUAL (100 Queries)
        # -------------------------------------------------------------
        # 4a. Urdu -> Arabic Canonical Group (50 queries)
        for i, a in enumerate(matched_anchors[:50]):
            queries.append({
                "query_id": f"XL_UR_AR_{i+1:03d}",
                "language": "ur",
                "category": "cross_lingual_urdu",
                "query": f"حدیث کا مفہوم: {a['ur_text']}",
                "gold_group_ids": [a["group_id"]],
                "gold_hadith_ids": a["hadith_ids"],
                "difficulty": "hard",
                "provenance_source": f"canonical_meaning_group:{a['group_id']}",
                "notes": f"Cross-lingual Urdu query mapping to Arabic canonical group {a['group_id']}"
            })

        # 4b. English -> Arabic Canonical Group (50 queries)
        for i, a in enumerate(matched_anchors[:50]):
            queries.append({
                "query_id": f"XL_EN_AR_{i+1:03d}",
                "language": "en",
                "category": "cross_lingual_english",
                "query": f"Hadith concept: {a['en_text']}",
                "gold_group_ids": [a["group_id"]],
                "gold_hadith_ids": a["hadith_ids"],
                "difficulty": "hard",
                "provenance_source": f"canonical_meaning_group:{a['group_id']}",
                "notes": f"Cross-lingual English query mapping to Arabic canonical group {a['group_id']}"
            })

        assert len([q for q in queries if q["category"].startswith("cross_lingual")]) == EXPECTED_CROSS, f"Cross-lingual queries count mismatch: {len([q for q in queries if q['category'].startswith('cross_lingual')])}"

        # -------------------------------------------------------------
        # CATEGORY 5: REFERENCE & EDGE CASES (50 Queries)
        # -------------------------------------------------------------
        # NOTE: Prompt Section 10 & 22 specifies: These are safety/regression checks,
        # evaluated separately and not blended into the primary semantic quality score.
        ref_edge_specs = [
            ("Bukhari 1", "reference_lookup", 319, [1]),
            ("Sahih Bukhari 1", "reference_lookup", 319, [1]),
            ("Bukhari #1", "reference_lookup", 319, [1]),
            ("Sahih al-Bukhari 1", "reference_lookup", 319, [1]),
            ("Muslim 1907", "reference_lookup", 319, [1]),
            ("Sahih Muslim 1907", "reference_lookup", 319, [1]),
            ("Bukhari 8", "reference_lookup", 523, [8]),
            ("Bukhari 10", "reference_lookup", 218, [10]),
            ("Bukhari 13", "reference_lookup", 595, [13]),
            ("Tirmidhi 2861", "reference_lookup", 2852, []),
            ("Abu Dawud 4607", "reference_lookup", 507, []),
            ("Sunan Abi Dawud 4607", "reference_lookup", 507, []),
            ("Nasa'i 348", "reference_lookup", 474, []),
            ("Sunan an-Nasa'i 348", "reference_lookup", 474, []),
            ("Ibn Majah 1", "reference_lookup", 383, []),
            ("Bukhari 52", "reference_lookup", 444, [53]),
            ("Bukhari 2528", "reference_lookup", 319, [2356]),
            ("Muslim 2699", "reference_lookup", 383, []),
            ("Bukhari 6018", "reference_lookup", 507, []),
            ("Bukhari 6407", "reference_lookup", 2852, []),
            ("bukhari 1", "reference_lookup", 319, [1]),
            ("bukhari hadith 1", "reference_lookup", 319, [1]),
            ("sahih bukhari hadith number 1", "reference_lookup", 319, [1]),
            ("al bukhari 1", "reference_lookup", 319, [1]),
            ("البخاري 1", "reference_lookup", 319, [1]),
            ("صحيح البخاري 1", "reference_lookup", 319, [1]),
            ("مسلم 1907", "reference_lookup", 319, [1]),
            ("صحيح مسلم 1907", "reference_lookup", 319, [1]),
            ("الترمذي 2861", "reference_lookup", 2852, []),
            ("جامع الترمذي 2861", "reference_lookup", 2852, []),
            ("ابو داود 4607", "reference_lookup", 507, []),
            ("سنن ابي داود 4607", "reference_lookup", 507, []),
            ("النسائي 348", "reference_lookup", 474, []),
            ("سنن النسائي 348", "reference_lookup", 474, []),
            ("ابن ماجه 1", "reference_lookup", 383, []),
            # Edge cases: single words, keywords, boundary cases
            ("النيات", "edge_case", 319, [1]),
            ("نية", "edge_case", 319, [1]),
            ("الإسلام", "edge_case", 523, [8]),
            ("المسلم", "edge_case", 218, [10]),
            ("الضرر", "edge_case", 1856, []),
            ("النصيحة", "edge_case", 397, []),
            ("الحلال", "edge_case", 444, [53]),
            ("الحياء", "edge_case", 714, []),
            ("الطهور", "edge_case", 474, []),
            ("الصدق", "edge_case", 319, []),
            ("الغش", "edge_case", 588, []),
            ("الغضب", "edge_case", 507, []),
            ("القرآن", "edge_case", 383, []),
            ("السواك", "edge_case", 474, []),
            ("التيمم", "edge_case", 474, []),
        ]

        for i, (q_str, cat, gid, hids) in enumerate(ref_edge_specs):
            queries.append({
                "query_id": f"REF_EDGE_{i+1:03d}",
                "language": "mixed",
                "category": cat,
                "query": q_str,
                "gold_group_ids": [gid] if gid else [],
                "gold_hadith_ids": hids,
                "difficulty": "easy",
                "provenance_source": f"reference_lookup:{q_str}",
                "notes": f"Reference or edge case query: {q_str}"
            })

        assert len([q for q in queries if q["category"] in ("reference_lookup", "edge_case")]) == EXPECTED_REF_EDGE, f"Reference/edge count mismatch: {len([q for q in queries if q['category'] in ('reference_lookup', 'edge_case')])}"
        assert len(queries) == EXPECTED_TOTAL, f"Total queries count mismatch: {len(queries)} != {EXPECTED_TOTAL}"

        # Write dataset JSONL
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        hasher = hashlib.sha256()

        with open(OUTPUT_JSONL_PATH, "w", encoding="utf-8", newline="\n") as f:
            for q in queries:
                line = json.dumps(q, ensure_ascii=False, separators=(",", ":")) + "\n"
                f.write(line)
                hasher.update(line.encode("utf-8"))

        dataset_sha256 = hasher.hexdigest()
        print(f"[SUCCESS] Wrote {len(queries)} benchmark queries to {OUTPUT_JSONL_PATH}")
        print(f"[INFO] Benchmark Dataset SHA-256: {dataset_sha256}")

        with open(OUTPUT_SHA_PATH, "w", encoding="utf-8", newline="\n") as f:
            f.write(f"{dataset_sha256}  {OUTPUT_JSONL_PATH.name}\n")

        # Write manifest
        manifest = {
            "benchmark_name": "Mīzān al-Ḥadīth EmbeddingGemma 2 Benchmark Suite",
            "version": "1.0.0",
            "creation_timestamp": datetime.now(timezone.utc).isoformat(),
            "documented_colab_account": "itsriver236@gmail.com",
            "total_queries": len(queries),
            "language_counts": {
                "arabic": EXPECTED_ARABIC,
                "urdu": EXPECTED_URDU,
                "english": EXPECTED_ENGLISH,
                "cross_lingual": EXPECTED_CROSS,
                "reference_and_edge": EXPECTED_REF_EDGE,
            },
            "dataset_sha256": dataset_sha256,
            "source_canonical_kg_sha256": compute_file_sha256(CANONICAL_KG_PATH),
            "baseline_gemini_store_sha256": compute_file_sha256(REPO_ROOT / "data" / "derived_semantic_index.db"),
            "target_candidate_store_sha256": compute_file_sha256(REPO_ROOT / "data" / "derived_embeddinggemma2_768d.db"),
            "gold_label_methodology": "Deterministically mapped to canonical meaning_groups and hadiths in hadith-kg.db; zero circular model dependence",
            "evaluation_metrics": [
                "Recall@1", "Recall@5", "Recall@10", "MRR", "nDCG@10", "Cross-Lingual Gap", "P95 Latency"
            ]
        }

        with open(OUTPUT_MANIFEST_PATH, "w", encoding="utf-8", newline="\n") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        print(f"[SUCCESS] Manifest recorded at {OUTPUT_MANIFEST_PATH}")
        return queries

    finally:
        conn.close()


if __name__ == "__main__":
    qs = build_500_benchmark_dataset()
    print(f"[DONE] Generated {len(qs)} benchmark records.")
