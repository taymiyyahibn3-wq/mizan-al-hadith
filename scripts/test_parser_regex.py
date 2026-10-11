import re
from typing import Optional, Tuple, Dict, Any

def clean_target_name(name: str) -> str:
    if not name:
        return ""
    n = name.strip()
    # Strip common filler prefixes
    n = re.sub(r"^(?:the\s+narrator|narrator|rawi|the\s+rawi|al[- ]rawi|الراوي)\s+", "", n, flags=re.I)
    n = re.sub(r"^(?:imam|shaykh|sheikh|sayyiduna|hadrat|الإمام|الشيخ)\s+", "", n, flags=re.I)
    # Strip trailing punctuation
    n = n.rstrip("?؟.:!").strip()
    return n

def extract_narrator_name_from_query(text: str) -> Optional[str]:
    clean = text.strip().rstrip("?؟.").strip()
    
    # Pattern 1: "Who is/was [the narrator] <Name>" or "من هو [الراوي] <Name>"
    m = re.search(r"^(?:who\s+(?:is|was)\s+(?:the\s+narrator\s+)?|من\s+هو\s+(?:الراوي\s+)?)(.+)$", clean, re.I)
    if m:
        t = clean_target_name(m.group(1))
        if t and not re.match(r"^(?:he|him|his|she|her|this|that|it)$", t, re.I):
            return t

    # Pattern 2: "What did (?:the\s+)?scholars say about (?:narrator\s+)?<Name>"
    m = re.search(r"(?:scholars\s+say\s+about|العلماء\s+في|أقوال\s+العلماء\s+في)\s+(.+)$", clean, re.I)
    if m:
        t = clean_target_name(m.group(1))
        if t and not re.match(r"^(?:he|him|his|she|her|this|that|it|this\s+narrator)$", t, re.I):
            return t

    # Pattern 3: "What did <Scholar> say about (?:narrator\s+)?<Name>"
    m = re.search(r"(?:say\s+about|قال\s+.*?\s+في)\s+(.+)$", clean, re.I)
    if m:
        t = clean_target_name(m.group(1))
        if t and not re.match(r"^(?:he|him|his|she|her|this|that|it|this\s+narrator)$", t, re.I):
            return t

    # Pattern 4: "(?:jarh\s+wa\s+ta'?dil|evaluations?|verdicts?|جرح\s+وتعديل)\s+(?:statements?\s+)?(?:about|on|for|في)\s+(.+)$"
    m = re.search(r"(?:jarh\s+wa\s+ta'?dil|evaluations?|verdicts?|جرح\s+وتعديل)\s+(?:statements?\s+)?(?:about|on|for|في)\s+(.+)$", clean, re.I)
    if m:
        t = clean_target_name(m.group(1))
        if t and not re.match(r"^(?:he|him|his|she|her|this|that|it|this\s+narrator)$", t, re.I):
            return t

    # Pattern 5: "teachers\s+and\s+students\s+of\s+<Name>" or "teachers\s+of\s+<Name>" or "students\s+of\s+<Name>"
    m = re.search(r"(?:teachers\s+(?:and\s+students\s+)?of|students\s+of|شيوخ|تلاميذ)\s+(.+)$", clean, re.I)
    if m:
        t = clean_target_name(m.group(1))
        if t and not re.match(r"^(?:he|him|his|she|her|this|that|it|this\s+narrator)$", t, re.I):
            return t

    # Pattern 6: "tell\s+me\s+about\s+(?:the\s+narrator\s+)?<Name>"
    m = re.search(r"(?:tell\s+me\s+about|about\s+the\s+narrator|عن\s+الراوي)\s+(.+)$", clean, re.I)
    if m:
        t = clean_target_name(m.group(1))
        if t and not re.match(r"^(?:he|him|his|she|her|this|that|it|this\s+narrator)$", t, re.I):
            return t

    # Pattern 7: "narrator\s+<Name>" or "rawi\s+<Name>"
    m = re.search(r"\b(?:narrator|rawi|الراوي)\s+([A-Za-z\s'’\-]+|[\u0621-\u064A\s]+)$", clean, re.I)
    if m:
        t = clean_target_name(m.group(1))
        if t and not re.match(r"^(?:he|him|his|she|her|this|that|it|this\s+narrator)$", t, re.I):
            return t

    return None

test_queries = [
    "Who is Abdur Rahman al-Musalli?",
    "What did the scholars say about Abdur Rahman al-Musalli?",
    "Who were his teachers and students?",
    "What are the jarh wa ta'dil statements about this narrator?",
    "What did Yahya ibn Ma'in say about Abdur Rahman al-Musalli?",
    "Tell me about the narrator Abu Hurayrah",
    "Who is Yahya ibn Sa'id?",
    "Did Yahya ibn Ma'in grade this narrator?",
]

for q in test_queries:
    print(f"Q: '{q}' -> Narrator Name: '{extract_narrator_name_from_query(q)}'")
