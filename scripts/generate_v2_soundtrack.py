import numpy as np
import wave
import os

SAMPLE_RATE = 48000
TOTAL_DURATION = 81.5

def save_wav(filename, samples, sample_rate=SAMPLE_RATE):
    samples = np.clip(samples, -1.0, 1.0)
    int_samples = (samples * 32767).astype(np.int16)
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(2 if samples.ndim == 2 else 1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(int_samples.tobytes())

def generate_v2_ambient_score():
    t = np.linspace(0, TOTAL_DURATION, int(SAMPLE_RATE * TOTAL_DURATION), endpoint=False)
    
    # Base tonal roots: D minor progression (D -> F -> G -> Bb -> D)
    d1 = 55.0
    d2 = 110.0
    a2 = 164.81
    f3 = 174.61
    g3 = 196.00
    bb3 = 233.08
    a3 = 220.00
    d4 = 293.66
    
    # 1. Base Pad (Contemplative & Warm)
    pad = (
        0.30 * np.sin(2 * np.pi * d1 * t) +
        0.22 * np.sin(2 * np.pi * d2 * t + 0.3) +
        0.16 * np.sin(2 * np.pi * a2 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.08 * t)) +
        0.12 * np.sin(2 * np.pi * f3 * t + 0.5) * (0.6 + 0.4 * np.cos(2 * np.pi * 0.05 * t))
    )
    
    # 2. Middle Phase (18s to 64s): Subtle intellectual pulse / technological texture
    pulse_t = np.clip((t - 18.0) / 10.0, 0, 1) * np.clip((74.0 - t) / 6.0, 0, 1)
    pulse_carrier = np.sin(2 * np.pi * 1.833 * t)
    d3 = 220.0
    pulse_synth = np.sin(2 * np.pi * d3 * t) * (np.maximum(0, pulse_carrier) ** 4) * 0.12
    pulse_synth += np.sin(2 * np.pi * 329.63 * t) * (np.maximum(0, -pulse_carrier) ** 4) * 0.08
    
    # 3. High Research Shimmer (40s to 74s): Subtle harmonic glass texture
    shimmer_env = np.clip((t - 40.0) / 12.0, 0, 1) * np.clip((75.0 - t) / 4.0, 0, 1)
    shimmer = (
        0.05 * np.sin(2 * np.pi * 587.33 * t) +
        0.04 * np.sin(2 * np.pi * 880.00 * t + 0.4) +
        0.03 * np.sin(2 * np.pi * 1174.66 * t + 0.8)
    ) * shimmer_env * (0.6 + 0.4 * np.sin(2 * np.pi * 0.25 * t))
    
    # 4. Final Climax Lift (64s to 79s): Controlled emotional warmth
    lift_env = np.clip((t - 64.0) / 8.0, 0, 1) * np.clip((80.0 - t) / 3.0, 0, 1)
    lift = (
        0.15 * np.sin(2 * np.pi * d2 * t) +
        0.12 * np.sin(2 * np.pi * a2 * t) +
        0.10 * np.sin(2 * np.pi * d4 * t)
    ) * lift_env
    
    music_mono = (pad + pulse_synth * pulse_t + shimmer + lift)
    music_mono = np.tanh(music_mono * 1.1) # Gentle analog saturation
    
    # Smooth master fade-in (3s) and fade-out (3s)
    fade_in = np.clip(t / 3.0, 0, 1)
    fade_out = np.clip((TOTAL_DURATION - t) / 3.0, 0, 1)
    master_env = fade_in * fade_out
    
    left = music_mono * master_env * 0.28
    right = np.roll(music_mono, int(SAMPLE_RATE * 0.015)) * master_env * 0.28 # 15ms Haas stereo widening
    
    stereo_music = np.column_stack((left, right))
    os.makedirs("video/audio/v2", exist_ok=True)
    save_wav("video/audio/v2/music_bed.wav", stereo_music)
    print(f"Generated v2/music_bed.wav ({TOTAL_DURATION}s)")

if __name__ == "__main__":
    generate_v2_ambient_score()
