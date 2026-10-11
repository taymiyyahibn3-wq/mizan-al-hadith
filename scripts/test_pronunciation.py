import asyncio
import edge_tts
import subprocess
import os

VOICE = "en-US-AndrewMultilingualNeural" # Or en-US-BrianNeural, en-US-ChristopherNeural

candidates = [
    ("test_orig", "Mīzān al-Ḥadīth. Built for serious Hadith research."),
    ("test_phonetic1", "Mee-zaan al-Ha-deeth. Built for serious Hadith research."),
    ("test_phonetic2", "Meezan al-Hadeeth. Built for serious Hadith research."),
    ("test_phonetic3", "Meezahn al Ha-deeth. Built for serious Hadith research."),
    ("test_phonetic4", "Meezahn al Hadeeth. Built for serious Hadith research."),
    ("test_ssml", '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US"><phoneme alphabet="ipa" ph="miːˈzɑːn æl hɑːˈdiːθ">Meezan al Hadeeth</phoneme>. Built for serious Hadith research.</speak>')
]

async def run():
    os.makedirs("video/audio/tests", exist_ok=True)
    for name, text in candidates:
        out_path = f"video/audio/tests/{name}.mp3"
        print(f"Generating {name}...")
        try:
            comm = edge_tts.Communicate(text, VOICE, rate="-2%", pitch="-1Hz")
            await comm.save(out_path)
            cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", out_path]
            dur = subprocess.check_output(cmd).decode().strip()
            print(f"  {name} duration: {float(dur):.2f}s")
        except Exception as e:
            print(f"  {name} failed: {e}")

if __name__ == "__main__":
    asyncio.run(run())
