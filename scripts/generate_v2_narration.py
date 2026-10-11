import asyncio
import edge_tts
import subprocess
import os

VOICE = "en-US-AndrewMultilingualNeural" # Calm, authoritative, mature
RATE = "-2%"
PITCH = "-1Hz"

V2_SEGMENTS = [
    {
        "id": "v2_s1_opening",
        "text": "Mee-zaan al-Ha-deeth. ... Built for serious Hadith research.",
        "target_start": 0.8
    },
    {
        "id": "v2_s2_problem",
        "text": "Hadith research can mean moving between books, sources, narrators, chains, gradings, translations, and different numbering systems.",
        "target_start": 8.2
    },
    {
        "id": "v2_s3_transition",
        "text": "Mee-zaan brings this research into one structured environment.",
        "target_start": 18.8
    },
    {
        "id": "v2_s4_search",
        "text": "Search through a large Hadith corpus and move from discovery to investigation in seconds.",
        "target_start": 29.2
    },
    {
        "id": "v2_s5_detail",
        "text": "Open a Hadith and explore its source, numbering, translation, grading, and available research data.",
        "target_start": 40.8
    },
    {
        "id": "v2_s6_sanad",
        "text": "Follow chains of transmission and investigate narrator-level information where the data is available.",
        "target_start": 52.8
    },
    {
        "id": "v2_s7_crossref",
        "text": "Connect the information. Compare the evidence. Research with structure.",
        "target_start": 64.6
    },
    {
        "id": "v2_s8_hero",
        "text": "Mee-zaan al-Ha-deeth. ... Built for serious Hadith research.",
        "target_start": 74.6
    }
]

async def generate():
    audio_dir = "video/audio/v2"
    os.makedirs(audio_dir, exist_ok=True)
    
    report = []
    print("==================================================")
    print(" GENERATING V2 NARRATION AUDIO STEMS")
    print("==================================================")
    
    for seg in V2_SEGMENTS:
        out_file = os.path.join(audio_dir, f"{seg['id']}.mp3")
        # Generate with edge-tts
        comm = edge_tts.Communicate(seg["text"], VOICE, rate=RATE, pitch=PITCH)
        await comm.save(out_file)
        
        # Measure duration with ffprobe
        cmd = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", out_file
        ]
        dur = float(subprocess.check_output(cmd).decode().strip())
        
        start_t = seg["target_start"]
        end_t = start_t + dur
        report.append({
            "id": seg["id"],
            "start": start_t,
            "end": end_t,
            "duration": dur,
            "file": out_file
        })
        print(f"[{seg['id']}] Start: {start_t:.1f}s | Duration: {dur:.2f}s | End: {end_t:.1f}s")

    print("\n--------------------------------------------------")
    print(" VERIFYING ZERO SPEECH OVERLAP")
    print("--------------------------------------------------")
    has_overlap = False
    for i in range(len(report) - 1):
        gap = report[i+1]["start"] - report[i]["end"]
        print(f"Gap between {report[i]['id']} and {report[i+1]['id']}: {gap:.2f}s pause")
        if gap < 0.3:
            print(f"  WARNING: Potential overlap or tight gap between {report[i]['id']} and {report[i+1]['id']}!")
            has_overlap = True
            
    if not has_overlap:
        print("✓ SUCCESS: All voiceover segments have generous, clean pauses. ZERO OVERLAP.")

if __name__ == "__main__":
    asyncio.run(generate())
