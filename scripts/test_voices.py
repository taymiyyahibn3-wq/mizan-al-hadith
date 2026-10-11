import asyncio
import edge_tts
import subprocess
import os

voices = [
    ("andrew", "en-US-AndrewMultilingualNeural"),
    ("ryan", "en-GB-RyanNeural"),
    ("brian", "en-US-BrianNeural"),
    ("christopher", "en-US-ChristopherNeural")
]

async def run():
    text = "Mee-zaan al-Ha-deeth. Built for serious Hadith research."
    os.makedirs("video/audio/tests_voices", exist_ok=True)
    for name, v in voices:
        out_path = f"video/audio/tests_voices/{name}.mp3"
        comm = edge_tts.Communicate(text, v, rate="-3%", pitch="-1Hz")
        await comm.save(out_path)
        print(f"Generated {name} with voice {v}")

if __name__ == "__main__":
    asyncio.run(run())
