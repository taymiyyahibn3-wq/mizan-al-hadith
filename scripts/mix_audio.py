import subprocess
import os

def mix_audio():
    audio_dir = "video/audio"
    out_file = os.path.join(audio_dir, "final_soundtrack.wav")
    
    # Scene voiceover files and their exact start times (in seconds)
    cues = [
        ("ambient_bed.wav", 0.0, 0.40),
        ("chime.wav", 1.0, 0.50),
        ("scene1_opening.mp3", 0.6, 1.0),
        ("whoosh.wav", 7.2, 0.40),
        ("scene2_problem.mp3", 7.8, 1.0),
        ("whoosh.wav", 17.7, 0.45),
        ("scene3_transition.mp3", 18.2, 1.0),
        ("whoosh.wav", 28.2, 0.45),
        ("typing.wav", 29.2, 0.60),
        ("click.wav", 31.2, 0.70),
        ("scene4_search.mp3", 28.8, 1.0),
        ("whoosh.wav", 39.2, 0.45),
        ("click.wav", 40.0, 0.60),
        ("scene5_detail.mp3", 39.8, 1.0),
        ("whoosh.wav", 50.2, 0.45),
        ("scene6_sanad.mp3", 50.8, 1.0),
        ("whoosh.wav", 61.2, 0.45),
        ("scene7_crossref.mp3", 61.8, 1.0),
        ("whoosh.wav", 72.2, 0.50),
        ("chime.wav", 73.0, 0.60),
        ("scene8_hero.mp3", 73.2, 1.0),
    ]
    
    inputs = []
    filter_parts = []
    
    for idx, (filename, delay_sec, volume) in enumerate(cues):
        filepath = os.path.join(audio_dir, filename)
        inputs.extend(["-i", filepath])
        delay_ms = int(delay_sec * 1000)
        filter_parts.append(
            f"[{idx}:a]volume={volume},adelay={delay_ms}|{delay_ms}[a{idx}]"
        )
    
    mix_inputs = "".join(f"[a{i}]" for i in range(len(cues)))
    filter_complex = ";".join(filter_parts) + f";{mix_inputs}amix=inputs={len(cues)}:normalize=0[aout]"
    
    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[aout]",
        "-t", "82.0",
        "-ar", "48000",
        "-ac", "2",
        out_file
    ]
    
    print("Running FFmpeg audio mix...")
    subprocess.check_call(cmd)
    print(f"Final audio soundtrack created: {out_file}")

if __name__ == "__main__":
    mix_audio()
