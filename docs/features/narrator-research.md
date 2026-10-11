# FEATURE — NARRATOR RESEARCH & BIOGRAPHICAL CRITIQUE

**Document Identifier:** `docs/features/narrator-research.md`  
**Frontend Routes:** `/narrators`, `/narrator/[id]`  
**Backend Endpoints:** `/api/narrators`, `/api/narrator/{id}`, `/api/narrator/{id}/aqwal`, `/api/narrator/{id}/network`  

---

## 1. Overview & Capabilities

The science of Hadith transmitters (*ʿIlm al-Rijāl*) is the bedrock of hadith authenticity evaluation. Mīzān al-Ḥadīth contains biographical profiles for **49,844 individual transmitters**, enriched with **127,863 classical critical opinions** (*Aqwāl al-Jarḥ wa al-Taʿdīl*).

---

## 2. Biographical Profile Capabilities (`/narrator/[id]`)

1. **Full Name & Lineage (*Nasab*):** Complete historical names, patronymics (*Kunyah*), regional origins (*Nisbah*), and generation tiers.
2. **Chronological Span:** Birth and death years (in Hijri years AH) with generation tier mapping (Sahaba, Senior Tabi'in, Later Tabi'in, Atba' al-Tabi'in).
3. **Critical Consensus Rank (*Rutbah*):** Classical summaries (e.g., *Thiqah* [Trustworthy], *Ṣadūq* [Truthful], *Ḍaʿīf* [Weak], *Majhūl* [Unknown]).
4. **Scholarly Judgments Matrix (*Aqwāl*):** Verbatim statements from master critics (Imam Ahmad ibn Hanbal, Yahya ibn Ma'in, Ali ibn al-Madini, al-Bukhari, Abu Hatim al-Razi, al-Nasa'i, Ibn Hajar al-'Asqalani).
5. **Teacher & Student Network:** Direct links to every scholar this narrator transmitted from (teachers) and to every scholar who received narrations from them (students).
6. **Scholarly Collision Caveats:** Automated detection of father/son and similar-name ambiguities.

---

## 3. Disambiguation & Scholarly Collision Protection

When multiple historical figures share names or patronymics, Mīzān's identity resolution engine (`identity_resolution.py`) intervenes to prevent false attribution:
- Transmitters with common names (such as *Sufyan*, *Hammad*, *Sulayman*) are linked to unique canonical IDs (`rawi_id`).
- Historical ambiguities (such as whether a praise statement applies to a father or son) are marked with `attribution_status = "father_son_collision"` and displayed with explicit cautionary banners.

---

## 4. Technical Implementation

- **Frontend Components:**
  - `src/app/narrators/page.tsx`
  - `src/app/narrator/[id]/page.tsx`
  - `src/app/components/ScholarlyStatementCard.tsx`
  - `src/app/isnad/NarratorResearchPanel.tsx`
- **Backend Endpoints:**
  - `GET /api/narrators?search={q}&limit=50&offset=0`
  - `GET /api/narrator/{id}`
  - `GET /api/narrator/{id}/aqwal`
  - `GET /api/narrator/{id}/network`
- **Data Dependencies:** `data/hadith-kg.db` (`rawis`, `alems`, `aqwal`, `sanad_rawis`).
