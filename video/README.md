# MĪZĀN AL-ḤADĪTH — Promotional Video Production Suite

This directory contains the complete source code, scene assets, audio stems, screen captures, and automated rendering pipeline for the **Mīzān al-Ḥadīth 1080p Cinematic Promotional Video**.

## Specification Summary
- **Format:** 16:9 Full HD (1920×1080), 30 FPS
- **Length:** 82.0 Seconds (2,460 frames)
- **Audio:** 48 kHz Stereo AAC (320 kbps) with documentary neural voiceover, ambient drone soundtrack, and synchronized UI Foley SFX
- **Encoding:** High-Profile H.264 (`-crf 17`, `-preset slow`, `yuv420p`)
- **Data Integrity:** 100% verified live application data (`715,790` hadiths, `425` collections, `49,844` narrators, `577,024` isnāds)

---

## Directory Architecture

- **`index.html`**: Master 1920×1080 HTML5/Canvas/WebGL composition player. Can be opened directly in any browser for interactive preview, frame scrubbing, and playback (use `?controls=1` in URL to display transport controls).
- **`render.js`**: Master automated render pipeline using Puppeteer-Core and FFmpeg. Evaluates each frame from 0 to 2,459 and pipes raw image frames directly into FFmpeg to produce `output/mizan_promo_1080p.mp4`.
- **`test_preview_frames.js`**: QA utility script that renders sample preview frames of all 8 scenes for visual quality and layout inspection.
- **`benchmark.js`**: Frame capture performance benchmark utility.
- **`components/`**:
  - `DrawingUtils.js`: High-end motion design utilities, easing curves, glassmorphism cards, drop shadows, and animated OS mouse cursor.
  - `GeometricBackground.js`: Procedural 8-fold Islamic geometric star rosette, rotating astronomical measurement rings, and floating golden dust particles.
  - `RealUIAssets.js`: Synchronous base64 bundle of real high-resolution screenshots captured from the running Mīzān web app.
  - `generate_assets_bundle.js`: Node script to bundle screenshots into `RealUIAssets.js`.
- **`scenes/`**:
  - `Scene1_Opening.js` (0.0s – 7.5s | Frames 0 – 225): Atmospheric sacred geometry, golden Mīzān crest, title reveal with light shimmer.
  - `Scene2_Problem.js` (7.5s – 18.0s | Frames 225 – 540): 3D floating cards representing the 6 pain points of traditional research fragmentation.
  - `Scene3_Transition.js` (18.0s – 28.5s | Frames 540 – 855): Convergence shockwave into the unified platform with animated counters for verified database stats.
  - `Scene4_Search.js` (28.5s – 39.5s | Frames 855 – 1185): Instant search query animation for *"إنما الأعمال بالنيات"*, keyboard Foley, and staggered search results.
  - `Scene5_Detail.js` (39.5s – 50.5s | Frames 1185 – 1515): Hadith 1 contextual breakdown with canonical grading badge (`صحيح`), word-level narrator alignments, and classical commentary.
  - `Scene6_Sanad.js` (50.5s – 61.5s | Frames 1515 – 1845): Interactive Isnād network view, 8-step transmission chain for Hadith 1, and Imam al-Bukhari biographical profile with 41 classical *aqwāl*.
  - `Scene7_Crossref.js` (61.5s – 72.5s | Frames 1845 – 2175): Real Hadith Visualizer matn graph connecting Bukhari #1 with Muslim #3537, Tirmidhi #1569, and Musnad Ahmad #166 & #291 with algorithmic similarity metrics.
  - `Scene8_Hero.js` (72.5s – 82.0s | Frames 2175 – 2460): 3D floating multi-card perspective pullback, golden Mīzān emblem, dignified serif branding, and call to action (*Search • Investigate • Connect • Research*).
- **`audio/`**:
  - `ambient_bed.wav`: Procedural 82-second ambient cinematic soundtrack (D-minor contemplative drone, 55 Hz sub-bass, slow LFOs, analog tape warmth).
  - `final_soundtrack.wav`: Master 48 kHz stereo mixed audio track containing soundtrack, synchronized voiceover narration, and UI SFX.
  - `whoosh.wav`, `click.wav`, `typing.wav`, `chime.wav`: Custom Foley and sound design assets.
  - `scene1_opening.mp3` through `scene8_hero.mp3`: Neural voiceover stems.
- **`screenshots/`**:
  - `1_homepage_hero.png` through `7_narrator_profile.png`: Real UI screenshots captured from `http://localhost:3000`.
  - `preview_scene1.png` through `preview_scene8.png`: High-resolution preview verification frames.
- **`output/`**:
  - `mizan_promo_1080p.mp4`: Final master promotional video.

---

## How to Re-Render or Edit

### 1. Re-render the Full Master Video
```bash
node video/render.js
```

### 2. Live Interactive Browser Preview
Open `video/index.html?controls=1` in Google Chrome or Microsoft Edge. Use the Play/Pause button or scrub across the timeline.

### 3. Generate Vertical 9:16 Version (For Shorts / Reels / TikTok)
Because all primary focal points and title cards are centered within the 608px inner safe column, a vertical 9:16 cut can be created instantly without rebuilding the project:
```bash
ffmpeg -i video/output/mizan_promo_1080p.mp4 -vf "crop=608:1080:656:0" -c:v libx264 -crf 17 -c:a copy video/output/mizan_promo_9x16.mp4
```
