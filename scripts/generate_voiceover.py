import asyncio
import os
import subprocess
import edge_tts

VOICE = "en-US-AndrewMultilingualNeural" # Warm, Confident, Authentic, Honest mature voice
RATE = "-4%" # Slightly measured, authoritative pacing
PITCH = "-2Hz" # Slightly deeper, serious tone

SCENES_NARRATION = [
    {
        "id": "scene1_opening",
        "text": "Mīzān al-Ḥadīth. An advanced research environment, built for the scholarly study of the prophetic tradition."
    },
    {
        "id": "scene2_problem",
        "text": "Traditional Hadith research often demands navigating across hundreds of disparate books, divergent numbering systems, fragmented narrator records, and complex chains of transmission."
    },
    {
        "id": "scene3_transition",
        "text": "Mīzān al-Ḥadīth unifies these essential dimensions into one structured research environment. Bringing over seven hundred and fifteen thousand Hadith records, four hundred and twenty-five collections, and forty-nine thousand narrators into a single coherent interface."
    },
    {
        "id": "scene4_search",
        "text": "Search across classical Arabic texts and verified English translations with microsecond precision. Moving from discovery to deep investigation in seconds."
    },
    {
        "id": "scene5_detail",
        "text": "Open any Hadith to examine its complete context: original Arabic matn, verified translations, canonical grading, and granular word-level narrator alignments."
    },
    {
        "id": "scene6_sanad",
        "text": "Trace the living chain of transmission. Follow isnād connections, inspect narrator biographies, and explore classical scholarly evaluations."
    },
    {
        "id": "scene7_crossref",
        "text": "Cross-reference variant texts across the Six Books and major Musnads, mapping parallel transmissions and textual variations across historical collections."
    },
    {
        "id": "scene8_hero",
        "text": "Mīzān al-Ḥadīth. Built for serious Hadith research."
    }
]

async def generate_all():
    audio_dir = os.path.join(os.path.dirname(__file__), "..", "video", "audio")
    os.makedirs(audio_dir, exist_ok=True)
    
    for item in SCENES_NARRATION:
        out_path = os.path.join(audio_dir, f"{item['id']}.mp3")
        print(f"Generating {item['id']} -> {out_path}")
        communicate = edge_tts.Communicate(item["text"], VOICE, rate=RATE, pitch=PITCH)
        await communicate.save(out_path)
        
        # Check duration with ffprobe
        cmd = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", out_path
        ]
        duration = subprocess.check_output(cmd).decode().strip()
        print(f"  Duration: {float(duration):.2f}s")

if __name__ == "__main__":
    asyncio.run(generate_all())
