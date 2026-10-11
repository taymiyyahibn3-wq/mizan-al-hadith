import subprocess
import os

def mix_v2():
    audio_dir = "video/audio/v2"
    sfx_dir = "video/audio"
    out_file = "video/audio/v2_final_master.wav"
    
    # 1. Voice segments with exact starts
    voice_cues = [
        ("v2_s1_opening.mp3", 0.8),
        ("v2_s2_problem.mp3", 8.2),
        ("v2_s3_transition.mp3", 18.8),
        ("v2_s4_search.mp3", 29.2),
        ("v2_s5_detail.mp3", 40.8),
        ("v2_s6_sanad.mp3", 52.8),
        ("v2_s7_crossref.mp3", 64.6),
        ("v2_s8_hero.mp3", 74.6),
    ]
    
    # 2. Subtle SFX
    sfx_cues = [
        (os.path.join(sfx_dir, "chime.wav"), 1.0, 0.30),
        (os.path.join(sfx_dir, "whoosh.wav"), 7.6, 0.22),
        (os.path.join(sfx_dir, "whoosh.wav"), 18.2, 0.22),
        (os.path.join(sfx_dir, "whoosh.wav"), 28.6, 0.22),
        (os.path.join(sfx_dir, "typing.wav"), 30.5, 0.25),
        (os.path.join(sfx_dir, "click.wav"), 32.5, 0.30),
        (os.path.join(sfx_dir, "whoosh.wav"), 40.2, 0.22),
        (os.path.join(sfx_dir, "whoosh.wav"), 52.2, 0.22),
        (os.path.join(sfx_dir, "whoosh.wav"), 64.0, 0.22),
        (os.path.join(sfx_dir, "whoosh.wav"), 73.8, 0.22),
        (os.path.join(sfx_dir, "chime.wav"), 74.2, 0.30),
    ]
    
    inputs = []
    # Input 0: Music Bed
    inputs.extend(["-i", os.path.join(audio_dir, "music_bed.wav")])
    
    filter_parts = []
    
    # Inputs 1 to 8: Voiceovers
    for idx, (filename, delay_sec) in enumerate(voice_cues, start=1):
        filepath = os.path.join(audio_dir, filename)
        inputs.extend(["-i", filepath])
        delay_ms = int(delay_sec * 1000)
        filter_parts.append(f"[{idx}:a]adelay={delay_ms}|{delay_ms}[v{idx}]")
        
    voice_mix_inputs = "".join(f"[v{i}]" for i in range(1, len(voice_cues) + 1))
    filter_parts.append(f"{voice_mix_inputs}amix=inputs={len(voice_cues)}:normalize=0[voice_bus]")
    
    # Inputs 9 to 19: SFX
    for idx, (filepath, delay_sec, vol) in enumerate(sfx_cues, start=len(voice_cues) + 1):
        inputs.extend(["-i", filepath])
        delay_ms = int(delay_sec * 1000)
        filter_parts.append(f"[{idx}:a]volume={vol},adelay={delay_ms}|{delay_ms}[sfx{idx}]")
        
    sfx_mix_inputs = "".join(f"[sfx{i}]" for i in range(len(voice_cues) + 1, len(voice_cues) + 1 + len(sfx_cues)))
    filter_parts.append(f"{sfx_mix_inputs}amix=inputs={len(sfx_cues)}:normalize=0[sfx_bus]")
    
    # Duck music bed using voice bus as sidechain detector
    filter_parts.append("[0:a][voice_bus]sidechaincompress=threshold=0.08:ratio=4:attack=50:release=400[ducked_music]")
    
    # Final master mix
    filter_parts.append("[ducked_music][voice_bus][sfx_bus]amix=inputs=3:normalize=0[master_out]")
    
    filter_complex = ";".join(filter_parts)
    
    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[master_out]",
        "-t", "81.5",
        "-ar", "48000",
        "-ac", "2",
        out_file
    ]
    
    print("Executing FFmpeg master audio mix with automatic sidechain ducking...")
    subprocess.check_call(cmd)
    print(f"Master V2 audio soundtrack created: {out_file}")

if __name__ == "__main__":
    mix_v2()
