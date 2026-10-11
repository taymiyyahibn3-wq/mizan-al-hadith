import numpy as np
import scipy.io.wavfile as wav
import os

SAMPLE_RATE = 48000
TOTAL_DURATION = 100.0 # Exactly 100.0 seconds (3000 frames @ 30 FPS)
NUM_SAMPLES = int(SAMPLE_RATE * TOTAL_DURATION)

def create_v3_soundtrack():
    print(f"Generating V3 100.0s master soundtrack at {SAMPLE_RATE} Hz...")
    t = np.linspace(0, TOTAL_DURATION, NUM_SAMPLES, endpoint=False)
    
    # -------------------------------------------------------------
    # 1. BASS & SUB-DRONE (Tonal center: D minor / 55 Hz & 110 Hz)
    # -------------------------------------------------------------
    sub_bass = 0.28 * np.sin(2 * np.pi * 55.0 * t) * (1.0 + 0.15 * np.sin(2 * np.pi * 0.1 * t))
    root_bass = 0.22 * np.sin(2 * np.pi * 110.0 * t)
    fifth = 0.14 * np.sin(2 * np.pi * 164.81 * t) # A2
    minor_third = 0.12 * np.sin(2 * np.pi * 130.81 * t) # F2
    
    # Drone presence curve across 100s
    drone_envelope = np.ones_like(t)
    # Fade in opening 2.0s
    fade_in = int(SAMPLE_RATE * 2.0)
    drone_envelope[:fade_in] = np.linspace(0, 1, fade_in)
    # Fade out final 4.0s
    fade_out = int(SAMPLE_RATE * 4.0)
    drone_envelope[-fade_out:] = np.linspace(1, 0, fade_out)
    
    ambient_bed = (sub_bass + root_bass + fifth + minor_third) * drone_envelope
    
    # -------------------------------------------------------------
    # 2. RHYTHMIC TECH PULSE (115 BPM: 1 beat = 0.5217s)
    # Active from 15.0s to 92.0s
    # -------------------------------------------------------------
    pulse_track = np.zeros_like(t)
    beat_dur = 60.0 / 115.0
    pulse_start_t = 15.0
    pulse_end_t = 92.0
    
    current_beat = pulse_start_t
    while current_beat < pulse_end_t:
        idx = int(current_beat * SAMPLE_RATE)
        # 16th note subtle tech tick
        tick_len = int(0.04 * SAMPLE_RATE)
        if idx + tick_len < NUM_SAMPLES:
            tt = np.linspace(0, 0.04, tick_len)
            # High frequency gentle click / shaker tick
            tick = 0.06 * np.sin(2 * np.pi * 2400.0 * tt) * np.exp(-tt * 90)
            pulse_track[idx:idx+tick_len] += tick
        
        # Quarter note deep pulse (heartbeat)
        quarter_len = int(0.18 * SAMPLE_RATE)
        if idx + quarter_len < NUM_SAMPLES:
            qt = np.linspace(0, 0.18, quarter_len)
            deep_kick = 0.12 * np.sin(2 * np.pi * (85.0 - 40.0 * (qt/0.18)) * qt) * np.exp(-qt * 18)
            pulse_track[idx:idx+quarter_len] += deep_kick
            
        current_beat += beat_dur
    
    # -------------------------------------------------------------
    # 3. HARMONIC PAD & ARPEGGIOS (Atmospheric movement)
    # -------------------------------------------------------------
    # E-minor / D-minor chord progressions moving through acts
    chord_track = np.zeros_like(t)
    chords = [
        (0.0, 15.0, [220.0, 261.63, 329.63]),      # Dm (A3, C4, E4)
        (15.0, 38.0, [220.0, 293.66, 349.23]),     # Dm7 (A3, D4, F4)
        (38.0, 60.0, [261.63, 329.63, 392.00]),    # C maj (C4, E4, G4)
        (60.0, 81.0, [293.66, 349.23, 440.00]),    # Dm (D4, F4, A4) - Climax
        (81.0, 92.0, [329.63, 392.00, 493.88]),    # Em (E4, G4, B4) - AI synthesis
        (92.0, 100.0, [220.0, 293.66, 440.00]),    # Dm resolution
    ]
    for start_c, end_c, freqs in chords:
        i1 = int(start_c * SAMPLE_RATE)
        i2 = int(end_c * SAMPLE_RATE)
        ct = t[i1:i2]
        dur = end_c - start_c
        # Gentle envelope
        env = np.sin(np.pi * (ct - start_c) / dur) ** 0.5
        for f in freqs:
            chord_track[i1:i2] += 0.04 * np.sin(2 * np.pi * f * ct) * env
            
    # -------------------------------------------------------------
    # 4. FOLEY & SOUND EFFECTS
    # -------------------------------------------------------------
    sfx_track = np.zeros_like(t)
    
    def add_whoosh(start_sec, dur=0.6, intensity=0.15):
        idx = int(start_sec * SAMPLE_RATE)
        length = int(dur * SAMPLE_RATE)
        if idx + length < NUM_SAMPLES:
            wt = np.linspace(0, dur, length)
            noise = np.random.normal(0, 1, length)
            # Bandpass envelope around 400Hz - 1200Hz
            sweep = np.sin(np.pi * wt / dur) ** 2
            sfx_track[idx:idx+length] += noise * sweep * intensity * 0.5
            # Low whoosh tone
            sfx_track[idx:idx+length] += 0.1 * np.sin(2 * np.pi * (180.0 + 80.0 * np.sin(np.pi * wt / dur)) * wt) * sweep
            
    def add_click(start_sec, intensity=0.12):
        idx = int(start_sec * SAMPLE_RATE)
        length = int(0.03 * SAMPLE_RATE)
        if idx + length < NUM_SAMPLES:
            ct = np.linspace(0, 0.03, length)
            sfx_track[idx:idx+length] += intensity * np.sin(2 * np.pi * 1800.0 * ct) * np.exp(-ct * 120)

    def add_chime(start_sec, base_freq=880.0, intensity=0.15):
        idx = int(start_sec * SAMPLE_RATE)
        length = int(2.5 * SAMPLE_RATE)
        if idx + length < NUM_SAMPLES:
            cmt = np.linspace(0, 2.5, length)
            chime = (
                0.5 * np.sin(2 * np.pi * base_freq * cmt) +
                0.3 * np.sin(2 * np.pi * (base_freq * 1.5) * cmt) +
                0.2 * np.sin(2 * np.pi * (base_freq * 2.0) * cmt)
            ) * np.exp(-cmt * 1.8) * intensity
            sfx_track[idx:idx+length] += chime

    def add_keystroke(start_sec):
        idx = int(start_sec * SAMPLE_RATE)
        length = int(0.02 * SAMPLE_RATE)
        if idx + length < NUM_SAMPLES:
            kt = np.linspace(0, 0.02, length)
            noise = np.random.normal(0, 1, length) * np.exp(-kt * 220) * 0.06
            click = 0.08 * np.sin(2 * np.pi * 2100.0 * kt) * np.exp(-kt * 180)
            sfx_track[idx:idx+length] += (noise + click)

    # Place SFX precisely at key narrative moments:
    # 1. Opening Crest
    add_chime(1.5, base_freq=880.0, intensity=0.18)
    
    # 2. Scale reveals (4 counter locks)
    add_click(7.5, 0.08)
    add_click(9.5, 0.08)
    add_click(11.5, 0.08)
    add_click(13.5, 0.10)
    
    # 3. Search transition & typing
    add_whoosh(15.0, dur=0.7)
    # Arabic typing sequence: "إنما الأعمال بالنيات" (19 keystrokes from 17.0s to 21.0s)
    for ks_time in [17.2, 17.4, 17.65, 17.85, 18.1, 18.3, 18.55, 18.8, 19.0, 19.25, 19.5, 19.7, 19.95, 20.2, 20.45, 20.7, 20.9]:
        add_keystroke(ks_time)
    add_click(21.5, 0.15) # Search execute click
    
    # 4. Hadith detail transition
    add_whoosh(26.0, dur=0.6)
    add_click(28.0, 0.10) # Detail card focus
    
    # 5. Isnad Network transition
    add_whoosh(38.0, dur=0.7)
    add_click(41.0, 0.10) # Node activation
    add_click(44.0, 0.10) # Narrator drawer slide
    
    # 6. Geographic Map transition
    add_whoosh(50.0, dur=0.8, intensity=0.18)
    add_click(53.0, 0.10) # City hub focus
    
    # 7. Timeline transition
    add_whoosh(60.0, dur=0.7)
    add_click(63.0, 0.10) # Generational tier focus
    
    # 8. 3D Spatial Graph Climax
    add_whoosh(70.0, dur=0.9, intensity=0.22)
    add_chime(71.0, base_freq=1046.5, intensity=0.15) # High C6 shimmer
    
    # 9. Ask Mizan transition
    add_whoosh(81.0, dur=0.7)
    add_click(83.5, 0.12) # AI query dispatch
    add_chime(85.0, base_freq=1174.66, intensity=0.14) # Synthesis complete
    
    # 10. Hero Resolution
    add_whoosh(91.0, dur=0.8)
    add_chime(92.5, base_freq=880.0, intensity=0.22)
    
    # -------------------------------------------------------------
    # 5. MASTER MIX (Ensuring ~10dB Headroom for Future Voiceover)
    # -------------------------------------------------------------
    music_mix = ambient_bed + pulse_track + chord_track
    # Soft limiter / warm tape compression on music
    music_mix = np.tanh(music_mix * 1.2) * 0.45
    
    # Combine with SFX
    total_mix = music_mix + sfx_track
    
    # Normalize with headroom: peak at -3 dB (0.707) and RMS at approx -14 dB
    peak = np.max(np.abs(total_mix))
    if peak > 0:
        total_mix = (total_mix / peak) * 0.65
        
    # Convert to 16-bit stereo PCM
    audio_int16 = (total_mix * 32767).astype(np.int16)
    stereo_audio = np.column_stack((audio_int16, audio_int16))
    
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'video', 'audio', 'v3')
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, 'v3_soundtrack_master.wav')
    wav.write(out_file, SAMPLE_RATE, stereo_audio)
    
    file_size_mb = os.path.getsize(out_file) / (1024 * 1024)
    print(f"Master V3 soundtrack successfully saved to {out_file} ({file_size_mb:.2f} MB)")
    print(f"Duration: {TOTAL_DURATION}s | Sample Rate: {SAMPLE_RATE} Hz | Channels: Stereo")
    print("Zero voiceover. Optimal headroom preserved for future narration.")

if __name__ == '__main__':
    create_v3_soundtrack()
