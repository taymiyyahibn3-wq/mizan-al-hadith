import os
import wave
import struct
import numpy as np

SAMPLE_RATE = 48000

def save_wav(filename, samples, sample_rate=SAMPLE_RATE):
    # Ensure float32 in [-1, 1]
    samples = np.clip(samples, -1.0, 1.0)
    int_samples = (samples * 32767).astype(np.int16)
    
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(2 if samples.ndim == 2 else 1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(int_samples.tobytes())

def generate_ambient_soundtrack(duration_sec=82.0, out_path="video/audio/ambient_bed.wav"):
    """
    Creates a warm, serious, documentary-style ambient cinematic bed.
    Dark, contemplative, subtle gold-hued pad with low sub drone and gentle harmonic movement.
    """
    t = np.linspace(0, duration_sec, int(SAMPLE_RATE * duration_sec), endpoint=False)
    
    # Root frequencies (D minor / A tonal center)
    d1 = 55.0     # D1 Sub drone
    d2 = 110.0    # D2 Bass
    a2 = 164.81   # A2 Fifth
    f3 = 174.61   # F3 Minor third
    d3 = 220.0    # D3
    a3 = 329.63   # A3
    
    # Slow undulating LFOs
    lfo1 = 0.5 + 0.5 * np.sin(2 * np.pi * 0.08 * t)
    lfo2 = 0.5 + 0.5 * np.sin(2 * np.pi * 0.13 * t + 1.2)
    lfo3 = 0.5 + 0.5 * np.cos(2 * np.pi * 0.05 * t + 2.4)
    
    # Layers
    drone_left = (
        0.28 * np.sin(2 * np.pi * d1 * t) +
        0.20 * np.sin(2 * np.pi * d2 * t + 0.3) +
        0.14 * np.sin(2 * np.pi * a2 * t) * lfo1 +
        0.08 * np.sin(2 * np.pi * f3 * t + 0.7) * lfo2 +
        0.05 * np.sin(2 * np.pi * d3 * t) * lfo3
    )
    
    drone_right = (
        0.28 * np.sin(2 * np.pi * d1 * t + 0.2) +
        0.20 * np.sin(2 * np.pi * d2 * t + 0.5) +
        0.14 * np.sin(2 * np.pi * a2 * t + 0.8) * lfo2 +
        0.08 * np.sin(2 * np.pi * f3 * t + 1.1) * lfo1 +
        0.05 * np.sin(2 * np.pi * a3 * t) * lfo3
    )
    
    # Subtle tape warmth / gentle saturation
    drone_left = np.tanh(drone_left * 1.2)
    drone_right = np.tanh(drone_right * 1.2)
    
    # Envelope: smooth 4s fade in, 4s fade out
    fade_in_len = int(SAMPLE_RATE * 3.5)
    fade_out_len = int(SAMPLE_RATE * 4.0)
    fade_in = np.linspace(0, 1, fade_in_len)
    fade_out = np.linspace(1, 0, fade_out_len)
    
    env = np.ones(len(t))
    env[:fade_in_len] = fade_in
    env[-fade_out_len:] = fade_out
    
    stereo = np.column_stack((drone_left * env * 0.25, drone_right * env * 0.25))
    save_wav(out_path, stereo)
    print(f"Generated ambient soundtrack: {out_path} ({duration_sec}s)")

def generate_sfx(audio_dir="video/audio"):
    os.makedirs(audio_dir, exist_ok=True)
    
    # 1. Whoosh (soft cinematic transition)
    dur = 1.0
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), endpoint=False)
    # Bandpassed noise sweep
    noise = np.random.normal(0, 0.4, len(t))
    env = np.sin(np.pi * (t / dur)) ** 3
    freq_sweep = np.sin(2 * np.pi * (80 + 350 * (t / dur)) * t)
    whoosh = (noise * 0.35 + freq_sweep * 0.25) * env * 0.4
    save_wav(os.path.join(audio_dir, "whoosh.wav"), whoosh)
    
    # 2. UI Click
    dur = 0.08
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), endpoint=False)
    click_env = np.exp(-t * 90)
    click = np.sin(2 * np.pi * 1800 * t) * click_env * 0.3
    save_wav(os.path.join(audio_dir, "click.wav"), click)
    
    # 3. Typing sequence (a short burst of realistic subtle key taps)
    dur = 1.8
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), endpoint=False)
    typing = np.zeros(len(t))
    tap_times = [0.1, 0.22, 0.36, 0.52, 0.65, 0.78, 0.95, 1.1, 1.25, 1.4, 1.55]
    for tap in tap_times:
        idx = int(tap * SAMPLE_RATE)
        tap_len = int(0.04 * SAMPLE_RATE)
        if idx + tap_len < len(t):
            sub_t = np.linspace(0, 0.04, tap_len, endpoint=False)
            freq = 900 + np.random.uniform(-150, 150)
            tap_sound = np.sin(2 * np.pi * freq * sub_t) * np.exp(-sub_t * 120) * 0.2
            typing[idx:idx+tap_len] += tap_sound
    save_wav(os.path.join(audio_dir, "typing.wav"), typing)
    
    # 4. Golden Chime / Shimmer (for logo reveal and hero finish)
    dur = 3.5
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), endpoint=False)
    chime_env = np.exp(-t * 1.2)
    chime = (
        0.3 * np.sin(2 * np.pi * 880 * t) +
        0.2 * np.sin(2 * np.pi * 1320 * t) +
        0.15 * np.sin(2 * np.pi * 1760 * t) +
        0.1 * np.sin(2 * np.pi * 2640 * t)
    ) * chime_env * 0.35
    save_wav(os.path.join(audio_dir, "chime.wav"), chime)
    print("Generated SFX: whoosh, click, typing, chime")

if __name__ == "__main__":
    generate_ambient_soundtrack(82.0)
    generate_sfx()
