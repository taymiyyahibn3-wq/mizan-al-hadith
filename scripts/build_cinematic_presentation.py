"""
Build MĪZĀN AL-ḤADĪTH — Presentation 01
Cinematic Interactive Standalone HTML Presentation
Output: Mizan_Al_Hadith_Presentation_01.html
"""

import os
import sys
import shutil

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

HTML_HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="color-scheme" content="dark">
  <meta name="theme-color" content="#050811">
  <title>MĪZĀN AL-ḤADĪTH (مِيزَانُ الحَدِيث) — Cinematic Presentation 01</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400;1,700&family=Cinzel:wght@400;600;700;800;900&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
"""

CSS_STYLES = """
/* ==============================================================================
   MĪZĀN AL-ḤADĪTH — CINEMATIC INTERACTIVE PRESENTATION STYLESHEET
   Aesthetics: Deep Obsidian / Midnight / Radiant Antique Gold / Deep Emerald / Crimson
   ============================================================================== */

:root {
  --bg-deep: #050811;
  --bg-space: #070c18;
  --bg-surface: #0a1122;
  --bg-glass: rgba(10, 17, 34, 0.75);
  --bg-glass-elevated: rgba(14, 23, 46, 0.88);
  --bg-card-border: rgba(212, 175, 55, 0.18);
  --bg-card-hover-border: rgba(212, 175, 55, 0.45);

  --gold-primary: #d4af37;
  --gold-bright: #fbbf24;
  --gold-amber: #f59e0b;
  --gold-soft: rgba(212, 175, 55, 0.12);
  --gold-glow: rgba(212, 175, 55, 0.35);

  --emerald-primary: #10b981;
  --emerald-deep: #064e3b;
  --emerald-glow: rgba(16, 185, 129, 0.35);
  --emerald-soft: rgba(16, 185, 129, 0.12);

  --teal-primary: #14b8a6;
  --teal-glow: rgba(20, 184, 166, 0.3);

  --crimson-primary: #e11d48;
  --crimson-glow: rgba(225, 29, 72, 0.4);
  --crimson-soft: rgba(225, 29, 72, 0.12);

  --text-primary: #f8fafc;
  --text-secondary: #cbd5e1;
  --text-muted: #94a3b8;
  --text-dim: #64748b;

  --font-display: "Cinzel", Georgia, serif;
  --font-arabic: "Amiri", "Traditional Arabic", serif;
  --font-sans: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-mono: "JetBrains Mono", "Consolas", monospace;

  --shadow-glow-gold: 0 0 35px rgba(212, 175, 55, 0.25);
  --shadow-glow-emerald: 0 0 35px rgba(16, 185, 129, 0.25);
  --shadow-glow-crimson: 0 0 35px rgba(225, 29, 72, 0.3);
  --shadow-glass: 0 20px 50px rgba(0, 0, 0, 0.6);
}

*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
  background-color: var(--bg-deep);
  color: var(--text-primary);
  font-family: var(--font-sans);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  user-select: none;
}

/* Atmospheric Background Canvas & Layers */
#canvas-wrap {
  position: fixed;
  inset: 0;
  z-index: 1;
  pointer-events: none;
}

canvas#bgCanvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.ambient-nebula {
  position: fixed;
  width: 60vw;
  height: 60vh;
  border-radius: 50%;
  filter: blur(120px);
  pointer-events: none;
  z-index: 2;
  opacity: 0.15;
  transition: opacity 1.5s ease;
}

.nebula-gold {
  top: -10vh;
  right: -10vw;
  background: radial-gradient(circle, var(--gold-primary) 0%, transparent 70%);
}

.nebula-emerald {
  bottom: -15vh;
  left: -10vw;
  background: radial-gradient(circle, var(--emerald-primary) 0%, transparent 70%);
}

.ambient-vignette {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 3;
  background: radial-gradient(circle at center, transparent 40%, rgba(5, 8, 17, 0.85) 100%);
}

/* DECK HEADER DOCK */
.deck-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 4.25rem;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2.5rem;
  background: rgba(5, 8, 17, 0.65);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(212, 175, 55, 0.12);
}

.brand-unit {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.brand-emblem {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.5rem;
  border: 1px solid var(--gold-primary);
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.25), rgba(16, 185, 129, 0.1));
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-arabic);
  font-size: 1.25rem;
  color: var(--gold-bright);
  box-shadow: 0 0 15px var(--gold-glow);
}

.brand-text-block {
  display: flex;
  flex-direction: column;
}

.brand-title {
  font-family: var(--font-display);
  font-size: 0.95rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.brand-subtitle-mini {
  font-size: 0.7rem;
  color: var(--gold-primary);
  letter-spacing: 0.05em;
  font-family: var(--font-mono);
}

.header-center-info {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.slide-tag-pill {
  padding: 0.35rem 1rem;
  background: rgba(212, 175, 55, 0.08);
  border: 1px solid rgba(212, 175, 55, 0.25);
  border-radius: 9999px;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--gold-bright);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.deck-controls {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.timer-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem 0.85rem;
  background: rgba(10, 17, 34, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 9999px;
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}

.timer-badge:hover {
  border-color: var(--gold-primary);
  color: #ffffff;
}

.timer-indicator {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background: var(--emerald-primary);
  box-shadow: 0 0 8px var(--emerald-primary);
}

.btn-icon {
  background: rgba(14, 23, 46, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: var(--text-secondary);
  padding: 0.4rem 0.85rem;
  border-radius: 0.5rem;
  font-size: 0.8rem;
  font-family: var(--font-mono);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  transition: all 0.2s ease;
}

.btn-icon:hover {
  background: rgba(212, 175, 55, 0.15);
  border-color: var(--gold-primary);
  color: #ffffff;
  box-shadow: 0 0 12px var(--gold-glow);
}

.btn-icon.active {
  background: var(--gold-primary);
  color: #050811;
  font-weight: 700;
  border-color: var(--gold-bright);
}

/* PRESENTATION STAGE */
.stage-viewport {
  position: relative;
  z-index: 10;
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  perspective: 1400px;
  overflow: hidden;
}

.slide-scene {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 5rem 6vw 4.5rem;
  opacity: 0;
  pointer-events: none;
  transform: translate3d(0, 0, -120px) scale(0.92);
  transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1),
              transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
  will-change: opacity, transform;
}

.slide-scene.active {
  opacity: 1;
  pointer-events: auto;
  transform: translate3d(0, 0, 0) scale(1);
}

.slide-scene.prev-scene {
  transform: translate3d(-100px, 0, -80px) scale(0.94);
}

.slide-scene.next-scene {
  transform: translate3d(100px, 0, -80px) scale(0.94);
}

/* TYPOGRAPHIC HIERARCHY */
.scene-kicker {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  letter-spacing: 0.18em;
  color: var(--gold-bright);
  text-transform: uppercase;
  margin-bottom: 0.75rem;
}

.scene-kicker::before {
  content: "";
  display: inline-block;
  width: 0.5rem;
  height: 0.5rem;
  background: var(--gold-bright);
  border-radius: 50%;
  box-shadow: 0 0 8px var(--gold-bright);
}

.scene-title {
  font-family: var(--font-display);
  font-size: clamp(2rem, 3.2vw, 3.25rem);
  font-weight: 700;
  line-height: 1.15;
  letter-spacing: -0.01em;
  color: #ffffff;
  text-align: center;
  max-width: 58rem;
  margin-bottom: 0.75rem;
}

.scene-title-gradient {
  background: linear-gradient(135deg, #ffffff 40%, #e2e8f0 70%, var(--gold-bright) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.scene-subtitle {
  font-family: var(--font-sans);
  font-size: clamp(1rem, 1.3vw, 1.25rem);
  font-weight: 300;
  color: var(--text-secondary);
  text-align: center;
  max-width: 48rem;
  line-height: 1.6;
  margin-bottom: 2rem;
}

/* DECK FOOTER */
.deck-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3.5rem;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2.5rem;
  background: rgba(5, 8, 17, 0.7);
  backdrop-filter: blur(16px);
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.footer-source-note {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.footer-source-dot {
  width: 0.4rem;
  height: 0.4rem;
  border-radius: 50%;
  background: var(--gold-primary);
}

.footer-nav-track {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.btn-nav-arrow {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #ffffff;
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s;
}

.btn-nav-arrow:hover:not(:disabled) {
  background: var(--gold-soft);
  border-color: var(--gold-primary);
  color: var(--gold-bright);
}

.btn-nav-arrow:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.slide-counter-display {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  color: var(--gold-bright);
}

.progress-track-wrap {
  width: 14rem;
  height: 4px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 2px;
  overflow: hidden;
  position: relative;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--emerald-primary), var(--gold-bright));
  width: 5%;
  transition: width 0.4s ease;
  box-shadow: 0 0 10px var(--gold-glow);
}

/* CINEMATIC COMPONENT STYLES */

/* Glass Panels */
.glass-panel {
  background: var(--bg-glass);
  border: 1px solid var(--bg-card-border);
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: var(--shadow-glass);
  backdrop-filter: blur(20px);
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  overflow: hidden;
}

.glass-panel::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.4), transparent);
}

.glass-panel:hover {
  border-color: var(--bg-card-hover-border);
  transform: translateY(-3px);
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.7), var(--shadow-glow-gold);
}

.glass-panel-emerald {
  border-color: rgba(16, 185, 129, 0.25);
}
.glass-panel-emerald:hover {
  border-color: var(--emerald-primary);
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.7), var(--shadow-glow-emerald);
}

.glass-panel-crimson {
  border-color: rgba(225, 29, 72, 0.3);
  background: rgba(30, 10, 18, 0.8);
}
.glass-panel-crimson:hover {
  border-color: var(--crimson-primary);
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.7), var(--shadow-glow-crimson);
}

/* Luminous Counters */
.counter-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1.5rem 1rem;
  text-align: center;
}

.counter-value {
  font-family: var(--font-display);
  font-size: clamp(2rem, 3.2vw, 3.5rem);
  font-weight: 800;
  line-height: 1;
  color: #ffffff;
  margin-bottom: 0.5rem;
}

.counter-gold {
  color: var(--gold-bright);
  text-shadow: 0 0 20px rgba(251, 191, 36, 0.4);
}

.counter-emerald {
  color: var(--emerald-primary);
  text-shadow: 0 0 20px rgba(16, 185, 129, 0.4);
}

.counter-crimson {
  color: var(--crimson-primary);
  text-shadow: 0 0 20px rgba(225, 29, 72, 0.4);
}

.counter-label {
  font-family: var(--font-display);
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  color: var(--text-primary);
}

.counter-sub {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-top: 0.25rem;
}

/* Layout Grids */
.layout-grid-2 {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  width: 100%;
  max-width: 72rem;
}

.layout-grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  width: 100%;
  max-width: 76rem;
}

.layout-grid-4 {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem;
  width: 100%;
  max-width: 80rem;
}

/* Badges & Tags */
.neon-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.25rem 0.65rem;
  border-radius: 9999px;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.04em;
}

.neon-badge-emerald {
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid var(--emerald-primary);
  color: var(--emerald-primary);
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.2);
}

.neon-badge-gold {
  background: rgba(212, 175, 55, 0.15);
  border: 1px solid var(--gold-bright);
  color: var(--gold-bright);
  box-shadow: 0 0 10px rgba(212, 175, 55, 0.2);
}

.neon-badge-crimson {
  background: rgba(225, 29, 72, 0.15);
  border: 1px solid var(--crimson-primary);
  color: var(--crimson-primary);
  box-shadow: 0 0 10px rgba(225, 29, 72, 0.2);
}

.neon-badge-cyan {
  background: rgba(20, 184, 166, 0.15);
  border: 1px solid var(--teal-primary);
  color: var(--teal-primary);
  box-shadow: 0 0 10px rgba(20, 184, 166, 0.2);
}

/* Slide 01: Hero Calligraphy & Title */
.hero-arabic-calligraphy {
  font-family: var(--font-arabic);
  font-size: clamp(3.5rem, 6vw, 6.5rem);
  font-weight: 700;
  line-height: 1.3;
  color: var(--gold-bright);
  text-shadow: 0 0 35px rgba(251, 191, 36, 0.45), 0 0 70px rgba(212, 175, 55, 0.25);
  margin-bottom: 0.5rem;
  letter-spacing: 0.02em;
}

.hero-main-title {
  font-family: var(--font-display);
  font-size: clamp(2.5rem, 4.5vw, 4.5rem);
  font-weight: 900;
  letter-spacing: 0.25em;
  color: #ffffff;
  text-shadow: 0 0 30px rgba(255, 255, 255, 0.2);
  margin-bottom: 1rem;
}

.hero-divider {
  width: 14rem;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--gold-bright), transparent);
  margin: 0 auto 1.5rem;
}

.hero-metric-ribbon {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-top: 2rem;
  padding: 0.85rem 2rem;
  background: rgba(10, 17, 34, 0.6);
  border: 1px solid rgba(212, 175, 55, 0.25);
  border-radius: 9999px;
  backdrop-filter: blur(12px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.hero-ribbon-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.hero-ribbon-val {
  font-family: var(--font-mono);
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--gold-bright);
}

.hero-ribbon-label {
  font-size: 0.68rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.hero-ribbon-sep {
  width: 1px;
  height: 1.5rem;
  background: rgba(255, 255, 255, 0.1);
}

/* SPEAKER NOTES DRAWER */
.notes-drawer {
  position: fixed;
  bottom: 3.5rem;
  left: 0;
  right: 0;
  max-height: 16rem;
  background: rgba(7, 12, 24, 0.95);
  border-top: 1px solid var(--gold-primary);
  backdrop-filter: blur(20px);
  z-index: 150;
  padding: 1.5rem 3rem;
  transform: translateY(100%);
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 -20px 50px rgba(0, 0, 0, 0.8);
}

.notes-drawer.open {
  transform: translateY(0);
}

.notes-header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 0.5rem;
  margin-bottom: 0.75rem;
}

.notes-heading {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--gold-bright);
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.notes-text-body {
  font-family: Georgia, serif;
  font-size: 1rem;
  line-height: 1.6;
  color: var(--text-secondary);
  max-width: 64rem;
}

/* OVERVIEW MODAL GRID */
.overview-modal {
  position: fixed;
  inset: 0;
  background: rgba(5, 8, 17, 0.92);
  backdrop-filter: blur(20px);
  z-index: 200;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 3rem;
}

.overview-modal.open {
  display: flex;
}

.overview-container {
  width: 100%;
  max-width: 80rem;
  max-height: 85vh;
  overflow-y: auto;
  background: var(--bg-surface);
  border: 1px solid var(--gold-primary);
  border-radius: 1.25rem;
  padding: 2rem;
  box-shadow: var(--shadow-glass);
}

.overview-grid-20 {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1rem;
  margin-top: 1.5rem;
}

.overview-card-tile {
  background: var(--bg-glass);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 6.5rem;
}

.overview-card-tile:hover {
  border-color: var(--gold-primary);
  background: rgba(212, 175, 55, 0.1);
  transform: translateY(-2px);
}

.overview-card-tile.active {
  border-color: var(--emerald-primary);
  background: rgba(16, 185, 129, 0.15);
  box-shadow: 0 0 15px var(--emerald-glow);
}

.overview-tile-num {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--gold-bright);
}

.overview-tile-title {
  font-family: var(--font-display);
  font-size: 0.8rem;
  font-weight: 700;
  color: #ffffff;
  line-height: 1.3;
  margin: 0.35rem 0;
}

.overview-tile-cat {
  font-size: 0.65rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Reduced Motion Override */
@media (prefers-reduced-motion: reduce) {
  .slide-scene {
    transition: opacity 0.3s ease !important;
    transform: none !important;
  }
  .ambient-nebula {
    animation: none !important;
  }
}
"""

HTML_BODY_START = """
  </style>
</head>
<body>
  <!-- Ambient Atmospheric Canvases -->
  <div id="canvas-wrap">
    <canvas id="bgCanvas"></canvas>
  </div>
  <div class="ambient-nebula nebula-gold"></div>
  <div class="ambient-nebula nebula-emerald"></div>
  <div class="ambient-vignette"></div>

  <!-- DECK TOP HEADER -->
  <header class="deck-header">
    <div class="brand-unit">
      <div class="brand-emblem">م</div>
      <div class="brand-text-block">
        <div class="brand-title">MĪZĀN AL-ḤADĪTH <span style="font-family: var(--font-arabic); font-size: 1rem; color: var(--gold-bright);">ميزان الحديث</span></div>
        <div class="brand-subtitle-mini">FORENSIC DIGITAL HUMANITIES PLATFORM</div>
      </div>
    </div>

    <div class="header-center-info">
      <div class="slide-tag-pill" id="slideTagPill">SLIDE 01 · INSTITUTIONAL INTRODUCTION</div>
    </div>

    <div class="deck-controls">
      <div class="timer-badge" id="timerBadge" title="Click to pause/resume presentation timer">
        <span class="timer-indicator" id="timerIndicator"></span>
        <span id="timerText">00:00</span>
      </div>
      <button class="btn-icon" id="btnNotesToggle" title="Toggle Speaker Notes [N]">
        <span>📝</span> Notes
      </button>
      <button class="btn-icon" id="btnOverviewToggle" title="Toggle 20-Slide Grid [O]">
        <span>⚏</span> Overview
      </button>
      <button class="btn-icon" id="btnFullscreen" title="Toggle Fullscreen [F]">
        <span>⤢</span> Fullscreen
      </button>
    </div>
  </header>

  <!-- PRESENTATION MAIN STAGE (20 SCENES) -->
  <main class="stage-viewport" id="stageViewport">
"""

print("Writing HTML structure and styling components...")
