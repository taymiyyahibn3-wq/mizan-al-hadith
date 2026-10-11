"""
MĪZĀN AL-ḤADĪTH — PRESENTATION 01
CINEMATIC INTERACTIVE HTML PRESENTATION GENERATOR
"""

import os
import sys
import shutil

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

def get_html_head():
    return """<!DOCTYPE html>
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

def get_css():
    return """
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

def get_body_start():
    return """
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

def get_slides_html():
    # 20 Cinematic Slide Scenes
    slides = [
        # SLIDE 01: TITLE FOLIO
        """
    <!-- SLIDE 01: CINEMATIC OPENING -->
    <section class="slide-scene active" id="scene-1"
      data-id="1"
      data-tag="SLIDE 01 · INSTITUTIONAL INTRODUCTION"
      data-title="Mīzān al-Ḥadīth: Institutional Introduction"
      data-cat="Vision"
      data-time="1.5 min"
      data-citation="Phase 18 Certified Release Baseline · data/hadith-kg.db · October 2026"
      data-notes="Good morning, Professor Syed and colleagues. Today, we are presenting Mīzān al-Ḥadīth. For centuries, Islamic scholars have engaged in some of the most rigorous historical-critical analysis in human civilization. Yet our modern digital tools have remained flat, fragmented, and disconnected. Mīzān was created to bring the full power of modern relational graphs and digital humanities to this sacred heritage—without compromising a single principle of classical methodology.">
      
      <div style="text-align: center; display: flex; flex-direction: column; align-items: center; max-width: 64rem;">
        <div class="scene-kicker">● Academic Research Platform &amp; Digital Humanities Infrastructure</div>
        <div class="hero-arabic-calligraphy" dir="rtl">مِيزَانُ الحَدِيث</div>
        <h1 class="hero-main-title">MĪZĀN AL-ḤADĪTH</h1>
        <div class="hero-divider"></div>
        <p class="scene-subtitle" style="max-width: 44rem; margin-bottom: 1.5rem;">
          A Research Platform for Exploring Hadith, Narrators, Isnād, Commentaries, and Scholarly Evaluation
        </p>

        <div class="hero-metric-ribbon">
          <div class="hero-ribbon-item">
            <span class="hero-ribbon-val">715,790</span>
            <span class="hero-ribbon-label">Canonical Hadiths</span>
          </div>
          <div class="hero-ribbon-sep"></div>
          <div class="hero-ribbon-item">
            <span class="hero-ribbon-val">425</span>
            <span class="hero-ribbon-label">Collections</span>
          </div>
          <div class="hero-ribbon-sep"></div>
          <div class="hero-ribbon-item">
            <span class="hero-ribbon-val">49,844</span>
            <span class="hero-ribbon-label">Verified Transmitters</span>
          </div>
          <div class="hero-ribbon-sep"></div>
          <div class="hero-ribbon-item">
            <span class="hero-ribbon-val">577,024</span>
            <span class="hero-ribbon-label">Transmission Chains</span>
          </div>
          <div class="hero-ribbon-sep"></div>
          <div class="hero-ribbon-item">
            <span class="hero-ribbon-val">65,420</span>
            <span class="hero-ribbon-label">Scholarly Grades</span>
          </div>
          <div class="hero-ribbon-sep"></div>
          <div class="hero-ribbon-item">
            <span class="hero-ribbon-val" style="color: var(--emerald-primary);">35 / 35</span>
            <span class="hero-ribbon-label">Audit Gates (GO)</span>
          </div>
        </div>

        <div style="margin-top: 2rem; font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-muted);">
          Prepared for Professor Mairaj Syed, Islamic Studies &amp; Digital Humanities Researchers · October 2026
        </div>
      </div>
    </section>
    """,

        # SLIDE 02: THE PROBLEM (FLOATING DISCONNECTED FRAGMENTS)
        """
    <!-- SLIDE 02: THE SCHOLARLY DILEMMA -->
    <section class="slide-scene" id="scene-2"
      data-id="2"
      data-tag="SLIDE 02 · RESEARCH FRICTION"
      data-title="The Problem: Rich Knowledge, Fragmented Access"
      data-cat="Problem"
      data-time="2.0 min"
      data-citation="Academic Workflow Analysis · Hadith Studies Domain Research"
      data-notes="Every serious researcher in this room knows the exhaustion of modern hadith research. If you search Maktaba Shamela, you get 50 hits with zero relational links. If you look at a consumer website, the grading is flattened to a single word like 'Sahih', hiding the debate between al-Albani and Shu'ayb al-Arna'ut. And if you ask modern AI, it will happily invent a Sahabi that never existed. We call this the Digital Hadith Trilemma.">
      
      <div style="text-align: center; max-width: 54rem;">
        <div class="scene-kicker">The Scholarly Dilemma</div>
        <h2 class="scene-title">Hadith knowledge is rich — but finding the connections is difficult.</h2>
        <p class="scene-subtitle">Critical evidence is scattered across incompatible numbering systems, unlinked biographical dictionaries, detached commentaries, and ungrounded AI tools.</p>
      </div>

      <div class="layout-grid-4" style="margin-top: 1rem;">
        <div class="glass-panel" style="border-top: 3px solid var(--crimson-primary);">
          <div style="font-family: var(--font-mono); font-size: 0.7rem; color: var(--crimson-primary); font-weight: bold; margin-bottom: 0.5rem;">01 · NUMBERING CHAOS</div>
          <h3 style="font-family: var(--font-display); font-size: 1.1rem; color: #ffffff; margin-bottom: 0.5rem;">Conflicting Editions</h3>
          <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.5;">
            Cairo, Beirut, and Riyadh publishers use conflicting numbering for the exact same hadith. Citing #1986 refers to completely different texts.
          </p>
          <div style="margin-top: 1rem; padding: 0.5rem; background: var(--crimson-soft); border-radius: 0.35rem; font-size: 0.72rem; color: #fda4af;">
            ⚠ Manual crosswalk required
          </div>
        </div>

        <div class="glass-panel" style="border-top: 3px solid var(--gold-amber);">
          <div style="font-family: var(--font-mono); font-size: 0.7rem; color: var(--gold-bright); font-weight: bold; margin-bottom: 0.5rem;">02 · OPAQUE CHAINS</div>
          <h3 style="font-family: var(--font-display); font-size: 1.1rem; color: #ffffff; margin-bottom: 0.5rem;">Unstructured Text Strings</h3>
          <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.5;">
            Isnāds remain dead text paragraphs. Identifying the central transmitter (madār), co-transmitters, or missing links requires hours of manual drafting.
          </p>
          <div style="margin-top: 1rem; padding: 0.5rem; background: var(--gold-soft); border-radius: 0.35rem; font-size: 0.72rem; color: var(--gold-bright);">
            ⚡ Invisible network topology
          </div>
        </div>

        <div class="glass-panel" style="border-top: 3px solid var(--teal-primary);">
          <div style="font-family: var(--font-mono); font-size: 0.7rem; color: var(--teal-primary); font-weight: bold; margin-bottom: 0.5rem;">03 · FLATTENED LABELS</div>
          <h3 style="font-family: var(--font-display); font-size: 1.1rem; color: #ffffff; margin-bottom: 0.5rem;">Erased Disagreements</h3>
          <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.5;">
            Modern portals flatten centuries of nuanced debate into binary "Authentic/Weak" tags, hiding whether the text is sound while the chain is weak.
          </p>
          <div style="margin-top: 1rem; padding: 0.5rem; background: rgba(20, 184, 166, 0.12); border-radius: 0.35rem; font-size: 0.72rem; color: #5eead4;">
            ⚖ Scholarly nuance destroyed
          </div>
        </div>

        <div class="glass-panel" style="border-top: 3px solid var(--crimson-primary);">
          <div style="font-family: var(--font-mono); font-size: 0.7rem; color: var(--crimson-primary); font-weight: bold; margin-bottom: 0.5rem;">04 · UNGROUNDED AI</div>
          <h3 style="font-family: var(--font-display); font-size: 1.1rem; color: #ffffff; margin-bottom: 0.5rem;">Hallucinated Sources</h3>
          <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.5;">
            Commercial LLMs generate eloquent but completely fictitious hadiths, inventing narrators and attributing false statements to classical imams.
          </p>
          <div style="margin-top: 1rem; padding: 0.5rem; background: var(--crimson-soft); border-radius: 0.35rem; font-size: 0.72rem; color: #fda4af;">
            🛑 Academically toxic
          </div>
        </div>
      </div>
    </section>
    """,

        # SLIDE 03: THE IDEA (THE CONNECTED GRAPH)
        """
    <!-- SLIDE 03: CORE PARADIGM SHIFT -->
    <section class="slide-scene" id="scene-3"
      data-id="3"
      data-tag="SLIDE 03 · THE CONNECTED SYSTEM"
      data-title="The Basic Idea: A Connected Research Graph"
      data-cat="Architecture"
      data-time="2.0 min"
      data-citation="Relational Ontology Architecture · Mīzān Schema Design"
      data-notes="Mīzān fundamentally re-imagines how hadith data is organized. Instead of isolated text files or flat spreadsheets, Mīzān treats the entire hadith corpus as a connected, multidimensional knowledge graph where every text, edition, narrator, isnād, evaluation, and commentary note is explicitly linked.">
      
      <div style="text-align: center; max-width: 58rem;">
        <div class="scene-kicker">Core Conceptual Breakthrough</div>
        <h2 class="scene-title">What if hadith research could be explored as a connected system?</h2>
        <p class="scene-subtitle">Deconstructing the classical hadith from an isolated textual blob into an interconnected relational knowledge graph.</p>
      </div>

      <div class="glass-panel" style="width: 100%; max-width: 72rem; padding: 2rem; margin-top: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; gap: 0.5rem; flex-wrap: wrap;">
          <div style="flex: 1; min-width: 130px; background: rgba(16, 185, 129, 0.15); border: 1px solid var(--emerald-primary); padding: 1rem; border-radius: 0.75rem; text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.25rem;">📜</div>
            <div style="font-family: var(--font-display); font-size: 0.85rem; font-weight: 700; color: #ffffff;">Hadith Text</div>
            <div style="font-size: 0.7rem; color: var(--emerald-primary); margin-top: 0.2rem;">Canonical Anchor</div>
          </div>
          <div style="color: var(--gold-bright); font-size: 1.25rem;">➔</div>

          <div style="flex: 1; min-width: 130px; background: rgba(212, 175, 55, 0.15); border: 1px solid var(--gold-primary); padding: 1rem; border-radius: 0.75rem; text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.25rem;">📚</div>
            <div style="font-family: var(--font-display); font-size: 0.85rem; font-weight: 700; color: #ffffff;">Editions</div>
            <div style="font-size: 0.7rem; color: var(--gold-bright); margin-top: 0.2rem;">18 Schemes Mapped</div>
          </div>
          <div style="color: var(--gold-bright); font-size: 1.25rem;">➔</div>

          <div style="flex: 1; min-width: 130px; background: rgba(16, 185, 129, 0.15); border: 1px solid var(--emerald-primary); padding: 1rem; border-radius: 0.75rem; text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.25rem;">👤</div>
            <div style="font-family: var(--font-display); font-size: 0.85rem; font-weight: 700; color: #ffffff;">Narrators</div>
            <div style="font-size: 0.7rem; color: var(--emerald-primary); margin-top: 0.2rem;">49,844 Biographies</div>
          </div>
          <div style="color: var(--gold-bright); font-size: 1.25rem;">➔</div>

          <div style="flex: 1; min-width: 130px; background: rgba(212, 175, 55, 0.15); border: 1px solid var(--gold-primary); padding: 1rem; border-radius: 0.75rem; text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.25rem;">⛓️</div>
            <div style="font-family: var(--font-display); font-size: 0.85rem; font-weight: 700; color: #ffffff;">Transmission</div>
            <div style="font-size: 0.7rem; color: var(--gold-bright); margin-top: 0.2rem;">577,024 Isnāds</div>
          </div>
          <div style="color: var(--gold-bright); font-size: 1.25rem;">➔</div>

          <div style="flex: 1; min-width: 130px; background: rgba(16, 185, 129, 0.15); border: 1px solid var(--emerald-primary); padding: 1rem; border-radius: 0.75rem; text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.25rem;">⚖️</div>
            <div style="font-family: var(--font-display); font-size: 0.85rem; font-weight: 700; color: #ffffff;">Evaluations</div>
            <div style="font-size: 0.7rem; color: var(--emerald-primary); margin-top: 0.2rem;">9-Scholar Matrix</div>
          </div>
          <div style="color: var(--gold-bright); font-size: 1.25rem;">➔</div>

          <div style="flex: 1; min-width: 130px; background: rgba(212, 175, 55, 0.15); border: 1px solid var(--gold-primary); padding: 1rem; border-radius: 0.75rem; text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.25rem;">📖</div>
            <div style="font-family: var(--font-display); font-size: 0.85rem; font-weight: 700; color: #ffffff;">Commentary</div>
            <div style="font-size: 0.7rem; color: var(--gold-bright); margin-top: 0.2rem;">Scoped Sharḥ Junction</div>
          </div>
        </div>

        <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(5, 8, 17, 0.6); border-radius: 0.5rem; border-left: 3px solid var(--gold-bright); display: flex; justify-content: space-between; align-items: center;">
          <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5;">
            <strong>The Scholarly Shift:</strong> Navigating a hadith is no longer a static reading exercise. A single query simultaneously accesses its cross-edition numbers, transmitter reliability network, geographical dispersal, variant texts, and classical commentaries.
          </div>
          <div class="neon-badge neon-badge-emerald" style="white-space: nowrap; margin-left: 1.5rem;">
            ✔ 6 Normalized Relational Planes
          </div>
        </div>
      </div>
    </section>
    """,

        # SLIDE 04: WHAT IS MĪZĀN? (ORBITAL WORKBENCH)
        """
    <!-- SLIDE 04: PLATFORM ARCHITECTURE -->
    <section class="slide-scene" id="scene-4"
      data-id="4"
      data-tag="SLIDE 04 · PLATFORM ARCHITECTURE"
      data-title="What Mīzān Actually Is: Research Workbench"
      data-cat="Overview"
      data-time="2.0 min"
      data-citation="Mīzān System Feature Inventory · Production Release Core"
      data-notes="Mīzān is not a generic consumer hadith app or a basic keyword search box. It is a purpose-built digital humanities platform engineered specifically for academic research. It provides four specialized primary modules: a Cross-Edition Reader, an Isnād Graph Explorer, a Multi-Scholar Evaluation Matrix, and a Relational Commentary Engine.">
      
      <div style="text-align: center; max-width: 58rem;">
        <div class="scene-kicker">Architecture &amp; Features</div>
        <h2 class="scene-title">Mīzān is more than a hadith search box.</h2>
        <p class="scene-subtitle">Translating classical Islamic disciplines (*ʿUlūm al-Ḥadīth*) into specialized computational research instruments.</p>
      </div>

      <div class="layout-grid-4" style="margin-top: 1rem;">
        <div class="glass-panel glass-panel-emerald">
          <div style="font-size: 2rem; margin-bottom: 0.75rem;">📚</div>
          <h3 style="font-family: var(--font-display); font-size: 1.15rem; color: #ffffff; margin-bottom: 0.5rem;">Cross-Edition Reader</h3>
          <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.5;">
            Compare publications side-by-side with complete vocalization, English translations, and synchronized edition aliases (Bughā, Darussalam, Shamela).
          </p>
          <div style="margin-top: 1rem;" class="neon-badge neon-badge-emerald">Concordance Engine</div>
        </div>

        <div class="glass-panel">
          <div style="font-size: 2rem; margin-bottom: 0.75rem;">🕸️</div>
          <h3 style="font-family: var(--font-display); font-size: 1.15rem; color: #ffffff; margin-bottom: 0.5rem;">Isnād Multigraph</h3>
          <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.5;">
            Interactive graph visualizer displaying generational tabaqāt strata, the central common link (*madār*), co-transmitters, and defect detection.
          </p>
          <div style="margin-top: 1rem;" class="neon-badge neon-badge-gold">5-View Isnād Suite</div>
        </div>

        <div class="glass-panel glass-panel-emerald">
          <div style="font-size: 2rem; margin-bottom: 0.75rem;">⚖️</div>
          <h3 style="font-family: var(--font-display); font-size: 1.15rem; color: #ffffff; margin-bottom: 0.5rem;">Multi-Scholar Matrix</h3>
          <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.5;">
            Preserves 65,420 exact evaluations across 9 classical and modern scholars, distinguishing between chain quality and text authenticity.
          </p>
          <div style="margin-top: 1rem;" class="neon-badge neon-badge-emerald">Evaluative Matrix</div>
        </div>

        <div class="glass-panel">
          <div style="font-size: 2rem; margin-bottom: 0.75rem;">📑</div>
          <h3 style="font-family: var(--font-display); font-size: 1.15rem; color: #ffffff; margin-bottom: 0.5rem;">Relational Sharḥ</h3>
          <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.5;">
            Precision commentary engine linking classical explanations directly to target hadith scopes, strictly insulating unrelated narrations.
          </p>
          <div style="margin-top: 1rem;" class="neon-badge neon-badge-gold">Scope Junction</div>
        </div>
      </div>
    </section>
    """,

        # SLIDE 05: DATA FOUNDATION (EMPIRICAL SCALE)
        """
    <!-- SLIDE 05: VERIFIED CENSUS -->
    <section class="slide-scene" id="scene-5"
      data-id="5"
      data-tag="SLIDE 05 · VERIFIED SCALE"
      data-title="The Data Foundation: Interconnected Scale"
      data-cat="Data"
      data-time="2.0 min"
      data-citation="Phase 18 Master Global Census Reconciliation · Cryptographic Hash Verification"
      data-notes="The foundation of Mīzān is not a mock or toy dataset. It contains 715,790 hadiths, 425 collections and books, nearly 50,000 verified narrators, over 577,000 transmission chains, 4.4 million transmission links, and 65,420 scholarly evaluations across 9 major critical authorities.">
      
      <div style="text-align: center; max-width: 58rem;">
        <div class="scene-kicker">Empirical Scale</div>
        <h2 class="scene-title">Built on a large interconnected data layer</h2>
        <p class="scene-subtitle">Mathematically reconciled across 5,262,799 verified entities in Phase 18 with zero unauthorized database mutations.</p>
      </div>

      <div class="layout-grid-3" style="margin-top: 1rem;">
        <div class="glass-panel counter-box">
          <div class="counter-value counter-emerald" data-target="715790">715,790</div>
          <div class="counter-label">Canonical Hadiths</div>
          <div class="counter-sub">Across 425 collections &amp; classical musnads</div>
        </div>

        <div class="glass-panel counter-box">
          <div class="counter-value counter-gold" data-target="49844">49,844</div>
          <div class="counter-label">Verified Transmitters (Rijāl)</div>
          <div class="counter-sub">Cross-referenced biographical registry</div>
        </div>

        <div class="glass-panel counter-box">
          <div class="counter-value counter-emerald" data-target="577024">577,024</div>
          <div class="counter-label">Transmission Chains (Sanads)</div>
          <div class="counter-sub">4,414,211 verified sequence steps</div>
        </div>

        <div class="glass-panel counter-box">
          <div class="counter-value counter-gold" data-target="65420">65,420</div>
          <div class="counter-label">Scholarly Evaluations</div>
          <div class="counter-sub">9 classical &amp; contemporary hadith critics</div>
        </div>

        <div class="glass-panel counter-box">
          <div class="counter-value counter-emerald" data-target="127863">127,863</div>
          <div class="counter-label">Biographical Critical Aqwāl</div>
          <div class="counter-sub">Jarḥ wa Taʿdīl evaluation statements</div>
        </div>

        <div class="glass-panel counter-box">
          <div class="counter-value counter-gold" data-target="1015">1,015</div>
          <div class="counter-label">Historical Critical Imāms</div>
          <div class="counter-sub">Spanning 12 centuries of continuous scholarship</div>
        </div>
      </div>

      <div style="margin-top: 1.5rem; width: 100%; max-width: 76rem; background: rgba(10, 17, 34, 0.7); border: 1px solid rgba(212, 175, 55, 0.2); border-radius: 0.5rem; padding: 0.75rem 1.5rem; display: flex; justify-content: space-between; align-items: center; font-family: var(--font-mono); font-size: 0.75rem;">
        <span style="color: var(--emerald-primary);">✔ 4 Canonical Databases: hadith-kg.db · hadith_numbering.db · citation_enrichment.db · hadith_commentaries.db</span>
        <span style="color: var(--gold-bright);">Sub-5ms Query Latency (Local SQLite WAL)</span>
      </div>
    </section>
    """,

        # SLIDE 06: MULTIPLE EDITIONS & NUMBERING
        """
    <!-- SLIDE 06: NUMBERING CRISIS -->
    <section class="slide-scene" id="scene-6"
      data-id="6"
      data-tag="SLIDE 06 · NUMBERING HARMONIZATION"
      data-title="Multiple Editions & Numbering Systems"
      data-cat="Concordance"
      data-time="2.0 min"
      data-citation="Phase 04 Multi-Edition Numbering Audit · data/hadith_numbering.db"
      data-notes="One of the greatest headaches for researchers is numbering divergence. In Ṣaḥīḥ al-Bukhārī, al-Bugha uses one numbering, Fatḥ al-Bārī another, and Dār al-Salām yet another. Mīzān harmonizes these editions under a unified canonical identifier while preserving every print edition's native numbering.">
      
      <div style="text-align: center; max-width: 58rem;">
        <div class="scene-kicker">Concordance Architecture</div>
        <h2 class="scene-title">One hadith can have different numbers.</h2>
        <p class="scene-subtitle">Mīzān connects varying print numbering systems without conflating or confusing them.</p>
      </div>

      <div class="layout-grid-2" style="margin-top: 1rem;">
        <div class="glass-panel">
          <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--crimson-primary); font-weight: bold; margin-bottom: 0.5rem;">
            CASE STUDY: SUNAN IBN MĀJAH #1986 DISASSOCIATION
          </div>
          <p style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">
            A student consulting the Darussalam print edition cites <strong>Hadith #1986</strong> regarding <em>Marriage &amp; Divorce (*ʿIddah*)</em>. When searching for #1986 in Arabic software like Shamela, an 82-hadith sequence offset occurs:
          </p>
          <div style="margin-top: 1rem; display: flex; flex-direction: column; gap: 0.5rem;">
            <div style="background: rgba(225, 29, 72, 0.15); border: 1px solid var(--crimson-primary); padding: 0.75rem; border-radius: 0.5rem; font-size: 0.8rem;">
              <strong style="color: #fda4af;">Darussalam Edition #1986:</strong> Kitāb al-Nikāḥ (Divorce Waiting Period)
            </div>
            <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid var(--gold-amber); padding: 0.75rem; border-radius: 0.5rem; font-size: 0.8rem;">
              <strong style="color: var(--gold-bright);">Maktaba Shamela #1986:</strong> Kitāb al-Tijārāt (Commercial Sale Transactions)
            </div>
          </div>
        </div>

        <div class="glass-panel glass-panel-emerald">
          <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--emerald-primary); font-weight: bold; margin-bottom: 0.5rem;">
            MĪZĀN'S CANONICAL RESOLUTION
          </div>
          <p style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">
            Mīzān establishes an immutable canonical surrogate key (<code>bukhari:1</code> or <code>ibn_majah:1986</code>) and maps every printed edition as a verified alias crosswalk:
          </p>
          <div style="margin-top: 1rem; display: flex; flex-direction: column; gap: 0.5rem; font-family: var(--font-mono); font-size: 0.8rem;">
            <div style="display: flex; justify-content: space-between; padding: 0.6rem 1rem; background: rgba(5, 8, 17, 0.8); border: 1px solid var(--emerald-primary); border-radius: 0.35rem;">
              <span>Canonical Anchor:</span>
              <strong style="color: var(--emerald-primary);">ibn_majah:1986 [Canonical]</strong>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.6rem 1rem; background: rgba(5, 8, 17, 0.6); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 0.35rem;">
              <span>Darussalam English Print:</span>
              <span style="color: var(--gold-bright);">Vol 3, Hadith #1986</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.6rem 1rem; background: rgba(5, 8, 17, 0.6); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 0.35rem;">
              <span>Fu'ād ʿAbd al-Bāqī Cairo:</span>
              <span style="color: var(--gold-bright);">Kitāb al-Nikāḥ, Hadith #1904</span>
            </div>
          </div>
          <div style="margin-top: 1rem; font-size: 0.75rem; color: var(--text-muted); text-align: center;">
            95,598 Crosswalk rows verified across 18 edition numbering schemes.
          </div>
        </div>
      </div>
    </section>
    """,

        # SLIDE 07: MULTI-SCHOLAR EVALUATION
        """
    <!-- SLIDE 07: SCHOLARLY NUANCE -->
    <section class="slide-scene" id="scene-7"
      data-id="7"
      data-tag="SLIDE 07 · SCHOLARLY NUANCE"
      data-title="Preserving Scholarly Disagreement"
      data-cat="Gradings"
      data-time="2.0 min"
      data-citation="Phase 11 &amp; Phase 13 Evaluation Audits · data/hadith-kg.db"
      data-notes="Different hadith scholars evaluate narrations using different methodological criteria. Al-Tirmidhī, al-Albānī, al-Arna'ūṭ, and Ibn Ḥajar frequently differ in their technical phrasing. Mīzān presents each authority's original wording side-by-side, preserving nuanced scholarly distinctions.">
      
      <div style="text-align: center; max-width: 58rem;">
        <div class="scene-kicker">Multi-Scholar Evaluative Matrix</div>
        <h2 class="scene-title">Scholars do not always express a judgment in the same way.</h2>
        <p class="scene-subtitle">Mīzān preserves each authority's exact evaluation instead of flattening nuance into binary labels.</p>
      </div>

      <div class="glass-panel" style="width: 100%; max-width: 74rem; margin-top: 1rem; padding: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding-bottom: 0.75rem; margin-bottom: 1rem;">
          <span style="font-family: var(--font-mono); font-size: 0.8rem; color: var(--gold-bright);">
            EXEMPLAR: JĀMIʿ AL-TIRMIDHĪ #2897 (CANONICAL ID: 15295)
          </span>
          <span class="neon-badge neon-badge-emerald">Preserved Technical Vocabulary</span>
        </div>

        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 1.25rem; background: rgba(5, 8, 17, 0.7); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 0.5rem;">
            <div>
              <strong style="color: #ffffff; font-size: 0.95rem;">Shaykh Muḥammad Nāṣir al-Dīn al-Albānī</strong>
              <div style="font-size: 0.75rem; color: var(--text-muted);">Ṣaḥīḥ Sunan al-Tirmidhī, Vol. 3, Hadith #2897</div>
            </div>
            <div class="neon-badge neon-badge-emerald" style="font-size: 0.9rem; padding: 0.35rem 1rem;">
              Ṣaḥīḥ (صحيح)
            </div>
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 1.25rem; background: rgba(5, 8, 17, 0.7); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 0.5rem;">
            <div>
              <strong style="color: #ffffff; font-size: 0.95rem;">Ḥāfiẓ Zubayr ʿAlī Zaʾī</strong>
              <div style="font-size: 0.75rem; color: var(--text-muted);">Anwār al-Ṣaḥīfah fī Fadāʾil al-Aʿmāl, p. 142 · Darussalam #2954</div>
            </div>
            <div class="neon-badge neon-badge-gold" style="font-size: 0.9rem; padding: 0.35rem 1rem;">
              Ḥasan li-Ghayrihī (حسن لغيره)
            </div>
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 1.25rem; background: rgba(5, 8, 17, 0.7); border: 1px solid rgba(20, 184, 166, 0.3); border-radius: 0.5rem;">
            <div>
              <strong style="color: #ffffff; font-size: 0.95rem;">Shaykh Shuʿayb al-Arnāʾūṭ</strong>
              <div style="font-size: 0.75rem; color: var(--text-muted);">Taḥqīq al-Musnad, Hadith #14201</div>
            </div>
            <div class="neon-badge neon-badge-cyan" style="font-size: 0.85rem; padding: 0.35rem 1rem;">
              Ḍaʿīf al-Isnād wa-Ṣaḥīḥ bi-Shawāhidih (ضعيف الإسناد وصحيح بشواهده)
            </div>
          </div>
        </div>

        <div style="margin-top: 1.25rem; display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem; text-align: center; font-family: var(--font-mono); font-size: 0.75rem;">
          <div style="background: rgba(212, 175, 55, 0.1); border: 1px solid rgba(212, 175, 55, 0.2); padding: 0.5rem; border-radius: 0.35rem; color: var(--gold-bright);">
            al-Albānī: 18,301 judgments
          </div>
          <div style="background: rgba(212, 175, 55, 0.1); border: 1px solid rgba(212, 175, 55, 0.2); padding: 0.5rem; border-radius: 0.35rem; color: var(--gold-bright);">
            Zubayr: 18,089 cert.
          </div>
          <div style="background: rgba(212, 175, 55, 0.1); border: 1px solid rgba(212, 175, 55, 0.2); padding: 0.5rem; border-radius: 0.35rem; color: var(--gold-bright);">
            al-Arnāʾūṭ: 6,374 judgments
          </div>
          <div style="background: rgba(212, 175, 55, 0.1); border: 1px solid rgba(212, 175, 55, 0.2); padding: 0.5rem; border-radius: 0.35rem; color: var(--gold-bright);">
            Abū Ghuddah: 5,627 judgments
          </div>
        </div>
      </div>
    </section>
    """,

        # SLIDE 08: ZERO-GUESS PRINCIPLE
        """
    <!-- SLIDE 08: ZERO-GUESS PRINCIPLE -->
    <section class="slide-scene" id="scene-8"
      data-id="8"
      data-tag="SLIDE 08 · FORENSIC RIGOR"
      data-title="The Zero-Guess Principle: Scientific Quarantine"
      data-cat="Integrity"
      data-time="2.5 min"
      data-citation="validation/phase_14/01_phase14_master_report.md &amp; Phase 18 Gate 12"
      data-notes="This is one of the most critical principles in Mīzān: when data is ambiguous, we do not guess. In Phase 14, out of 18,375 records from Zubayr's collection, 18,089 were certified with certainty. The remaining 286 records had disputed boundary markers. Rather than guessing, Mīzān isolated them in quarantine. Accuracy is never sacrificed for artificial coverage.">
      
      <div style="text-align: center; max-width: 58rem;">
        <div class="scene-kicker" style="color: var(--crimson-primary);">Data Integrity Mandate</div>
        <h2 class="scene-title">When the evidence is unclear, Mīzān does not guess.</h2>
        <p class="scene-subtitle">Coverage is never prioritized over scholarly precision. Ambiguity is quarantined, not manufactured.</p>
      </div>

      <div class="layout-grid-2" style="margin-top: 1rem;">
        <div class="glass-panel glass-panel-emerald" style="text-align: left; padding: 2rem;">
          <div style="font-family: var(--font-display); font-size: 3rem; font-weight: 800; color: var(--emerald-primary); line-height: 1;">
            18,089
          </div>
          <div style="font-family: var(--font-display); font-size: 1.15rem; color: #ffffff; margin-top: 0.5rem; font-weight: 700;">
            Certified Core Corpus (98.4%)
          </div>
          <p style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.75rem; line-height: 1.6;">
            Demonstrated 100% deterministic textual fidelity, verified publisher cross-references, and unbroken chains of scholarly transmission.
          </p>
          <div style="margin-top: 1.5rem;" class="neon-badge neon-badge-emerald">
            ✔ Cryptographically Sealed Baseline
          </div>
        </div>

        <div class="glass-panel glass-panel-crimson" style="text-align: left; padding: 2rem;">
          <div style="font-family: var(--font-display); font-size: 3rem; font-weight: 800; color: var(--crimson-primary); line-height: 1;">
            286
          </div>
          <div style="font-family: var(--font-display); font-size: 1.15rem; color: #ffffff; margin-top: 0.5rem; font-weight: 700;">
            Strictly Quarantined (1.6%)
          </div>
          <p style="font-size: 0.85rem; color: #fecdd3; margin-top: 0.75rem; line-height: 1.6;">
            Disputed editorial boundaries and ambiguous numbering were quarantined rather than forced into artificial canonical IDs.
          </p>
          <div style="margin-top: 1.5rem;" class="neon-badge neon-badge-crimson">
            🛑 QUARANTINE_ESCAPE_COUNT = 0
          </div>
        </div>
      </div>

      <div style="margin-top: 1.5rem; font-family: var(--font-arabic); font-size: 1.25rem; color: var(--gold-bright); text-align: center; text-shadow: 0 0 20px rgba(251, 191, 36, 0.4);">
        « دَعْ مَا يَرِيبُكَ إِلَى مَا لاَ يَرِيبُكَ »
      </div>
      <div style="font-family: Georgia, serif; font-style: italic; font-size: 0.85rem; color: var(--text-muted); margin-top: 0.25rem;">
        "Leave that which makes you doubt for that which does not make you doubt."
      </div>
    </section>
    """,

        # SLIDE 09: ISNĀD VISUALIZATION
        """
    <!-- SLIDE 09: ISNĀD NETWORK GRAPH -->
    <section class="slide-scene" id="scene-9"
      data-id="9"
      data-tag="SLIDE 09 · NETWORK EXPLORATION"
      data-title="Isnād Visualization: Transmission Networks"
      data-cat="Visualization"
      data-time="2.0 min"
      data-citation="Isnād Graph Engine Specification · D3/Canvas Visualizer"
      data-notes="Instead of viewing an isnād as a lifeless list of names, Mīzān transforms it into a multi-generational transmission graph. Researchers can instantly identify the common link (madār), see branch points, explore co-transmitters (mutāba'āt), and inspect narrator reliability scores.">
      
      <div style="text-align: center; max-width: 58rem;">
        <div class="scene-kicker">Interactive Network Architecture</div>
        <h2 class="scene-title">From a chain of names to a transmission network.</h2>
        <p class="scene-subtitle">Visualizing generational tabaqāt strata, co-transmitters, branch points, and common links (*Madār al-Isnād*).</p>
      </div>

      <div class="glass-panel" style="width: 100%; max-width: 76rem; padding: 1.5rem; margin-top: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding-bottom: 0.5rem;">
          <span style="font-family: var(--font-mono); font-size: 0.8rem; color: var(--gold-bright);">
            TRANSMISSION CHAIN: ṢAḤĪḤ AL-BUKHĀRĪ HADITH #1 (GENERATIONAL STRATA)
          </span>
          <span class="neon-badge neon-badge-emerald">Interactive Topology</span>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; gap: 0.5rem; flex-wrap: wrap; text-align: center;">
          <div style="flex: 1; min-width: 120px; background: rgba(5, 8, 17, 0.8); border: 1px solid var(--gold-primary); padding: 0.85rem 0.5rem; border-radius: 0.5rem;">
            <div style="font-size: 0.65rem; color: var(--gold-bright); font-family: var(--font-mono);">STRATUM 0</div>
            <strong style="font-size: 0.85rem; color: #ffffff; display: block; margin-top: 0.25rem;">Prophet Muhammad ﷺ</strong>
            <span style="font-size: 0.7rem; color: var(--text-muted);">Source</span>
          </div>
          <div style="color: var(--emerald-primary);">➔</div>

          <div style="flex: 1; min-width: 120px; background: rgba(5, 8, 17, 0.8); border: 1px solid rgba(255, 255, 255, 0.15); padding: 0.85rem 0.5rem; border-radius: 0.5rem;">
            <div style="font-size: 0.65rem; color: var(--emerald-primary); font-family: var(--font-mono);">COMPANION</div>
            <strong style="font-size: 0.85rem; color: #ffffff; display: block; margin-top: 0.25rem;">ʿUmar ibn al-Khaṭṭāb</strong>
            <span style="font-size: 0.7rem; color: var(--text-muted);">d. 23 AH</span>
          </div>
          <div style="color: var(--emerald-primary);">➔</div>

          <div style="flex: 1; min-width: 120px; background: rgba(5, 8, 17, 0.8); border: 1px solid rgba(255, 255, 255, 0.15); padding: 0.85rem 0.5rem; border-radius: 0.5rem;">
            <div style="font-size: 0.65rem; color: var(--emerald-primary); font-family: var(--font-mono);">SUCCESSOR</div>
            <strong style="font-size: 0.85rem; color: #ffffff; display: block; margin-top: 0.25rem;">ʿAlqamah ibn Waqqāṣ</strong>
            <span style="font-size: 0.7rem; color: var(--text-muted);">Madīnah</span>
          </div>
          <div style="color: var(--emerald-primary);">➔</div>

          <div style="flex: 1; min-width: 120px; background: rgba(16, 185, 129, 0.2); border: 2px solid var(--emerald-primary); padding: 0.85rem 0.5rem; border-radius: 0.5rem; box-shadow: 0 0 15px var(--emerald-glow);">
            <div style="font-size: 0.65rem; color: var(--emerald-primary); font-family: var(--font-mono); font-weight: bold;">MADĀR (COMMON LINK)</div>
            <strong style="font-size: 0.85rem; color: #ffffff; display: block; margin-top: 0.25rem;">Yaḥyā ibn Saʿīd</strong>
            <span style="font-size: 0.7rem; color: var(--gold-bright);">Branch Point</span>
          </div>
          <div style="color: var(--emerald-primary);">➔</div>

          <div style="flex: 1; min-width: 120px; background: rgba(5, 8, 17, 0.8); border: 1px solid rgba(255, 255, 255, 0.15); padding: 0.85rem 0.5rem; border-radius: 0.5rem;">
            <div style="font-size: 0.65rem; color: var(--emerald-primary); font-family: var(--font-mono);">TRANSMITTER</div>
            <strong style="font-size: 0.85rem; color: #ffffff; display: block; margin-top: 0.25rem;">Sufyān ibn ʿUyaynah</strong>
            <span style="font-size: 0.7rem; color: var(--text-muted);">Makkah</span>
          </div>
          <div style="color: var(--emerald-primary);">➔</div>

          <div style="flex: 1; min-width: 120px; background: rgba(5, 8, 17, 0.8); border: 1px solid var(--gold-primary); padding: 0.85rem 0.5rem; border-radius: 0.5rem;">
            <div style="font-size: 0.65rem; color: var(--gold-bright); font-family: var(--font-mono);">COMPILER</div>
            <strong style="font-size: 0.85rem; color: #ffffff; display: block; margin-top: 0.25rem;">Imām al-Bukhārī</strong>
            <span style="font-size: 0.7rem; color: var(--text-muted);">d. 256 AH</span>
          </div>
        </div>

        <div style="margin-top: 1.5rem; display: flex; justify-content: space-between; align-items: center; background: rgba(5, 8, 17, 0.6); padding: 0.75rem 1.25rem; border-radius: 0.5rem; border-left: 3px solid var(--emerald-primary);">
          <div style="font-size: 0.8rem; color: var(--text-secondary);">
            <strong>Integrated Biographical Drawer:</strong> Clicking any node pulls up their full <em>Tahdhīb al-Kamāl</em> profile, teacher/student records, and jarḥ/taʿdīl verdicts.
          </div>
          <div class="neon-badge neon-badge-gold">5-View Isnād Suite</div>
        </div>
      </div>
    </section>
    """,

        # SLIDE 10: GEOGRAPHY / ATLAS
        """
    <!-- SLIDE 10: HISTORICAL ATLAS -->
    <section class="slide-scene" id="scene-10"
      data-id="10"
      data-tag="SLIDE 10 · CARTOGRAPHY & TIME"
      data-title="Geography & Transmission: Geographic Dispersion"
      data-cat="Geography"
      data-time="2.0 min"
      data-citation="07_ISNAD_GEOGRAPHY_SPEC.md &amp; geoData.ts · Historical Spatial Registry"
      data-notes="Hadith transmission was a physical, geographic journey across the classical Islamic world. Mīzān models the spatial movement of hadith—from Medina and Mecca through Kufa, Basra, Damascus, Baghdad, and into Khurasan and Central Asia.">
      
      <div style="text-align: center; max-width: 58rem;">
        <div class="scene-kicker">Cartography of Tradition</div>
        <h2 class="scene-title">Where did this transmission travel?</h2>
        <p class="scene-subtitle">Tracing the physical journeys of hadith transmission (*al-Riḥlah fī Ṭalab al-Ḥadīth*) across 12 verified intellectual centers.</p>
      </div>

      <div class="glass-panel" style="width: 100%; max-width: 76rem; padding: 2rem; margin-top: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding-bottom: 0.5rem;">
          <span style="font-family: var(--font-mono); font-size: 0.8rem; color: var(--gold-bright);">
            SPATIO-TEMPORAL FLOW ARCS (ZERO SPECULATION ENFORCED)
          </span>
          <span class="neon-badge neon-badge-emerald">12 Classical Metropolitan Centers</span>
        </div>

        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;">
          <div style="background: rgba(5, 8, 17, 0.7); border: 1px solid var(--emerald-primary); padding: 1rem; border-radius: 0.5rem; text-align: center;">
            <div style="font-family: var(--font-arabic); font-size: 1.3rem; color: var(--gold-bright);">المدينة المنورة / مكة</div>
            <strong style="color: #ffffff; font-size: 0.85rem; display: block; margin-top: 0.25rem;">1. The Ḥijāz Core</strong>
            <p style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.25rem;">Prophetic generation, early Companions, and foundational transmission.</p>
          </div>

          <div style="background: rgba(5, 8, 17, 0.7); border: 1px solid var(--gold-primary); padding: 1rem; border-radius: 0.5rem; text-align: center;">
            <div style="font-family: var(--font-arabic); font-size: 1.3rem; color: var(--gold-bright);">الكوفة / البصرة</div>
            <strong style="color: #ffffff; font-size: 0.85rem; display: block; margin-top: 0.25rem;">2. Iraq Metropolitan Centers</strong>
            <p style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.25rem;">Successor proliferation, systematic compilation, and critical isnād testing.</p>
          </div>

          <div style="background: rgba(5, 8, 17, 0.7); border: 1px solid var(--teal-primary); padding: 1rem; border-radius: 0.5rem; text-align: center;">
            <div style="font-family: var(--font-arabic); font-size: 1.3rem; color: var(--gold-bright);">دمشق / بغداد</div>
            <strong style="color: #ffffff; font-size: 0.85rem; display: block; margin-top: 0.25rem;">3. Imperial Capitals</strong>
            <p style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.25rem;">Juridical synthesis, cross-regional verification, and scholarly debate.</p>
          </div>

          <div style="background: rgba(5, 8, 17, 0.7); border: 1px solid var(--emerald-primary); padding: 1rem; border-radius: 0.5rem; text-align: center;">
            <div style="font-family: var(--font-arabic); font-size: 1.3rem; color: var(--gold-bright);">نيسابور / بخارى</div>
            <strong style="color: #ffffff; font-size: 0.85rem; display: block; margin-top: 0.25rem;">4. Khurāsān &amp; Central Asia</strong>
            <p style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.25rem;">The golden age of canonical compendia compilation (al-Bukhārī, Muslim).</p>
          </div>
        </div>

        <div style="margin-top: 1.5rem; font-size: 0.8rem; color: var(--text-muted); text-align: center;">
          Geographic arcs are only generated when primary biographical sources record an authentic teacher-student encounter in that city.
        </div>
      </div>
    </section>
    """,

        # SLIDE 11: MATN COMPARISON
        """
    <!-- SLIDE 11: MATN COMPARISON -->
    <section class="slide-scene" id="scene-11"
      data-id="11"
      data-tag="SLIDE 11 · TEXTUAL CRITICISM"
      data-title="Matn Comparison: Wording Variants"
      data-cat="Matn"
      data-time="2.0 min"
      data-citation="Matn Difference Engine · Token Alignment Algorithm"
      data-notes="In hadith textual criticism, analyzing slight wording additions or omissions (ziyādāt al-thiqāt) is crucial for evaluating authenticity. Mīzān's Matn Comparison engine displays word-level differences side-by-side with color-coded additions, omissions, and lexical variants.">
      
      <div style="text-align: center; max-width: 58rem;">
        <div class="scene-kicker">Textual Criticism</div>
        <h2 class="scene-title">Compare the wording — not just the translation.</h2>
        <p class="scene-subtitle">Token-level textual alignment identifying shared core words, additions (*Ziyādāt*), and lexical substitutions.</p>
      </div>

      <div class="layout-grid-2" style="margin-top: 1rem;">
        <div class="glass-panel">
          <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding-bottom: 0.5rem; margin-bottom: 1rem;">
            <span style="font-family: var(--font-mono); font-size: 0.8rem; color: var(--emerald-primary);">
              WITNESS A: ṢAḤĪḤ AL-BUKHĀRĪ #1
            </span>
            <span class="neon-badge neon-badge-emerald">Plural Form</span>
          </div>

          <div style="font-family: var(--font-arabic); font-size: 1.35rem; line-height: 2.2; text-align: right; background: rgba(5, 8, 17, 0.7); padding: 1.25rem; border-radius: 0.5rem; border: 1px solid rgba(255, 255, 255, 0.1);" dir="rtl">
            « إِنَّمَا الأَعْمَالُ <span style="background: rgba(16, 185, 129, 0.3); color: #6ee7b7; padding: 0.1rem 0.5rem; border-radius: 0.25rem; border: 1px solid var(--emerald-primary);">بِالنِّيَّاتِ</span>، وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى... »
          </div>
          <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.75rem;">
            Standard plural form (بِالنِّيَّاتِ) transmitted across the majority of classical Iraqi &amp; Hijazi chains.
          </p>
        </div>

        <div class="glass-panel glass-panel-gold">
          <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding-bottom: 0.5rem; margin-bottom: 1rem;">
            <span style="font-family: var(--font-mono); font-size: 0.8rem; color: var(--gold-bright);">
              WITNESS B: ṢAḤĪḤ MUSLIM #1907
            </span>
            <span class="neon-badge neon-badge-gold">Singular Variant</span>
          </div>

          <div style="font-family: var(--font-arabic); font-size: 1.35rem; line-height: 2.2; text-align: right; background: rgba(5, 8, 17, 0.7); padding: 1.25rem; border-radius: 0.5rem; border: 1px solid rgba(212, 175, 55, 0.2);" dir="rtl">
            « إِنَّمَا الأَعْمَالُ <span style="background: rgba(245, 158, 11, 0.3); color: var(--gold-bright); padding: 0.1rem 0.5rem; border-radius: 0.25rem; border: 1px solid var(--gold-bright);">بِالنِّيَّةِ</span>، وَإِنَّمَا لِامْرِئٍ مَا نَوَى... »
          </div>
          <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.75rem;">
            Singular lexical variant (بِالنِّيَّةِ) documented in specific parallel transmission paths.
          </p>
        </div>
      </div>

      <div style="margin-top: 1.5rem; width: 100%; max-width: 72rem; display: flex; justify-content: space-around; background: rgba(5, 8, 17, 0.6); padding: 0.75rem; border-radius: 0.5rem; border: 1px solid rgba(255, 255, 255, 0.1); font-size: 0.78rem;">
        <span style="color: #6ee7b7;">● Green: Verbatim Shared Core (Mutawātir)</span>
        <span style="color: var(--gold-bright);">● Amber: Lexical / Singular-Plural Shift</span>
        <span style="color: #d8b4fe;">● Purple: Textual Addition (*Ziyādāt al-Thiqāt*)</span>
      </div>
    </section>
    """,

        # SLIDE 12: COMMENTARY (RELATIONAL SHARḤ)
        """
    <!-- SLIDE 12: RELATIONAL COMMENTARY -->
    <section class="slide-scene" id="scene-12"
      data-id="12"
      data-tag="SLIDE 12 · COMMENTARY INTEGRATION"
      data-title="Commentary: Exact Relational Linking"
      data-cat="Commentary"
      data-time="2.0 min"
      data-citation="Phase 12 Commentary Audit · hadith_commentaries.db"
      data-notes="Attaching classical commentaries to hadith is notoriously error-prone when done blindly. Mīzān's Phase 12 audit verified 1,202 commentary records across 1,203 links. As demonstrated in Record #428, commentary can link to Hadith 12427 as primary and 12428 as secondary, while rigorously excluding neighboring Hadith 12426.">
      
      <div style="text-align: center; max-width: 58rem;">
        <div class="scene-kicker">Relational Sharḥ Integration</div>
        <h2 class="scene-title">Connect the hadith to its scholarly commentary.</h2>
        <p class="scene-subtitle">Precision linking ensures commentaries are attached only to the exact narrations they explain, avoiding neighboring contamination.</p>
      </div>

      <div class="glass-panel" style="width: 100%; max-width: 76rem; padding: 2rem; margin-top: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding-bottom: 0.5rem;">
          <span style="font-family: var(--font-mono); font-size: 0.8rem; color: var(--gold-bright);">
            RECORD #428 AUTOPSY: MULTI-HADITH COMMENTARY SCOPE
          </span>
          <span class="neon-badge neon-badge-emerald">Phase 12 Certified</span>
        </div>

        <div class="layout-grid-3">
          <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid var(--emerald-primary); padding: 1.5rem; border-radius: 0.5rem; text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🟢</div>
            <h4 style="color: #ffffff; font-size: 1rem;">Hadith #12427</h4>
            <div class="neon-badge neon-badge-emerald" style="margin-top: 0.5rem;">PRIMARY LINK</div>
            <p style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.75rem;">
              The direct textual subject of the commentary chapter. Fully linked with complete text exposition.
            </p>
          </div>

          <div style="background: rgba(20, 184, 166, 0.15); border: 1px solid var(--teal-primary); padding: 1.5rem; border-radius: 0.5rem; text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🔵</div>
            <h4 style="color: #ffffff; font-size: 1rem;">Hadith #12428</h4>
            <div class="neon-badge neon-badge-cyan" style="margin-top: 0.5rem;">SECONDARY LINK</div>
            <p style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.75rem;">
              A corroborating narration discussed within the footnote commentary. Explicitly tagged as secondary scope.
            </p>
          </div>

          <div style="background: rgba(225, 29, 72, 0.15); border: 1px solid var(--crimson-primary); padding: 1.5rem; border-radius: 0.5rem; text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🛑</div>
            <h4 style="color: #ffffff; font-size: 1rem;">Hadith #12426</h4>
            <div class="neon-badge neon-badge-crimson" style="margin-top: 0.5rem;">ZERO LINK</div>
            <p style="font-size: 0.75rem; color: #fecdd3; margin-top: 0.75rem;">
              A physically adjacent hadith on the printed page, strictly isolated against contamination.
            </p>
          </div>
        </div>

        <div style="margin-top: 1.5rem; display: flex; justify-content: space-between; align-items: center; background: rgba(5, 8, 17, 0.6); padding: 0.75rem 1.25rem; border-radius: 0.5rem; font-family: var(--font-mono); font-size: 0.75rem;">
          <span style="color: var(--gold-bright);">Phase 12 Verified: 1,202 Commentary Records across 1,203 Relational Junction Links</span>
          <span style="color: var(--emerald-primary);">Zero False Adjacency Spillover</span>
        </div>
      </div>
    </section>
    """,

        # SLIDE 13: ASK MĪZĀN (RAG)
        """
    <!-- SLIDE 13: GROUNDED AI PIPELINE -->
    <section class="slide-scene" id="scene-13"
      data-id="13"
      data-tag="SLIDE 13 · GROUNDED AI PIPELINE"
      data-title="Ask Mīzān: Evidence-Grounded AI"
      data-cat="AI/RAG"
      data-time="2.0 min"
      data-citation="Ask Mīzān RAG Architecture · Retrieval-Augmented Synthesis"
      data-notes="Ask Mīzān is not a free-form chatbot that hallucinates citations. It employs a strict Retrieval-Augmented Generation pipeline. When a user asks a research question, Mīzān retrieves verified records, constructs an evidence pack, and constrains the AI to answer solely from that evidence with clickable citations.">
      
      <div style="text-align: center; max-width: 58rem;">
        <div class="scene-kicker">Grounded Synthesis</div>
        <h2 class="scene-title">AI that starts with evidence.</h2>
        <p class="scene-subtitle">"The AI is not the source. The underlying verified evidence is."</p>
      </div>

      <div class="glass-panel" style="width: 100%; max-width: 76rem; padding: 2rem; margin-top: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
          <div style="flex: 1; min-width: 150px; background: rgba(5, 8, 17, 0.7); border: 1px solid rgba(255, 255, 255, 0.15); padding: 1.25rem 1rem; border-radius: 0.5rem; text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">❓</div>
            <strong style="color: #ffffff; font-size: 0.9rem;">1. Research Query</strong>
            <p style="font-size: 0.72rem; color: var(--text-muted); margin-top: 0.25rem;">Academic prompt or hadith concept</p>
          </div>
          <div style="color: var(--gold-bright); font-size: 1.25rem;">➔</div>

          <div style="flex: 1; min-width: 150px; background: rgba(5, 8, 17, 0.7); border: 1px solid var(--gold-primary); padding: 1.25rem 1rem; border-radius: 0.5rem; text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🔍</div>
            <strong style="color: #ffffff; font-size: 0.9rem;">2. Hybrid Retrieval</strong>
            <p style="font-size: 0.72rem; color: var(--gold-bright); margin-top: 0.25rem;">Canonical DB + vector search</p>
          </div>
          <div style="color: var(--gold-bright); font-size: 1.25rem;">➔</div>

          <div style="flex: 1; min-width: 150px; background: rgba(16, 185, 129, 0.15); border: 1px solid var(--emerald-primary); padding: 1.25rem 1rem; border-radius: 0.5rem; text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">📦</div>
            <strong style="color: #ffffff; font-size: 0.9rem;">3. Evidence Pack</strong>
            <p style="font-size: 0.72rem; color: var(--emerald-primary); margin-top: 0.25rem;">Cryptographically sealed records</p>
          </div>
          <div style="color: var(--gold-bright); font-size: 1.25rem;">➔</div>

          <div style="flex: 1; min-width: 150px; background: rgba(5, 8, 17, 0.7); border: 1px solid var(--gold-bright); padding: 1.25rem 1rem; border-radius: 0.5rem; text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">✍️</div>
            <strong style="color: #ffffff; font-size: 0.9rem;">4. Cited Synthesis</strong>
            <p style="font-size: 0.72rem; color: var(--gold-bright); margin-top: 0.25rem;">Strict context-bounded generation</p>
          </div>
        </div>

        <div style="margin-top: 1.5rem; padding: 1rem 1.5rem; background: rgba(5, 8, 17, 0.8); border-radius: 0.5rem; border-left: 3px solid var(--crimson-primary); font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">
          <strong>Fail-Closed Anti-Hallucination Policy:</strong> If the retrieved evidence pack does not contain sufficient textual support to answer an inquiry, Ask Mīzān explicitly replies: <em>"The verified corpus does not contain sufficient textual evidence to confirm this claim."</em> It is programmatically blocked from fabricating hadiths or companions.
        </div>
      </div>
    </section>
    """,

        # SLIDE 14: FORENSIC VALIDATION
        """
    <!-- SLIDE 14: VALIDATION TIMELINE -->
    <section class="slide-scene" id="scene-14"
      data-id="14"
      data-tag="SLIDE 14 · FORENSIC VALIDATION"
      data-title="Trust & Forensic Validation: 18 Audit Phases"
      data-cat="Validation"
      data-time="2.0 min"
      data-citation="Validation Phases 01–18 Summary · Certified Machine Acceptance Logs"
      data-notes="How do we know the system is reliable? Because it underwent 18 distinct audit phases. We verified that canonical databases cannot be mutated, cryptographic SHA-256 hashes match across environments, and fail-closed quarantine prevents invalid data from leaking.">
      
      <div style="text-align: center; max-width: 58rem;">
        <div class="scene-kicker">Empirical Accountability</div>
        <h2 class="scene-title">How do we know the system is reliable?</h2>
        <p class="scene-subtitle">18 comprehensive validation phases testing integrity, boundary conditions, and adversarial regression.</p>
      </div>

      <div class="layout-grid-4" style="margin-top: 1rem;">
        <div class="glass-panel glass-panel-emerald">
          <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🔒</div>
          <h4 style="color: #ffffff; font-size: 1rem;">Zero DB Mutations</h4>
          <p style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.5rem;">
            Read-only canonical databases; user queries and API endpoints are strictly prohibited from mutating underlying SQLite files.
          </p>
          <div style="margin-top: 1rem;" class="neon-badge neon-badge-emerald">SHA-256 Verified</div>
        </div>

        <div class="glass-panel">
          <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🔑</div>
          <h4 style="color: #ffffff; font-size: 1rem;">Cross-DB Integrity</h4>
          <p style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.5rem;">
            Bidirectional foreign key relationships mathematically reconciled across all 4 databases without dangling references.
          </p>
          <div style="margin-top: 1rem;" class="neon-badge neon-badge-gold">5.96M+ Edges</div>
        </div>

        <div class="glass-panel glass-panel-crimson">
          <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🛑</div>
          <h4 style="color: #ffffff; font-size: 1rem;">Quarantine Gates</h4>
          <p style="font-size: 0.75rem; color: #fecdd3; margin-top: 0.5rem;">
            Automated regression suites test every public endpoint to ensure zero quarantined records leak into production queries.
          </p>
          <div style="margin-top: 1rem;" class="neon-badge neon-badge-crimson">Fail-Closed</div>
        </div>

        <div class="glass-panel">
          <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🛡️</div>
          <h4 style="color: #ffffff; font-size: 1rem;">AppSec Hardened</h4>
          <p style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.5rem;">
            Tested against SQL injections, prototype pollution, path traversals, and prompt injections in Ask Mīzān.
          </p>
          <div style="margin-top: 1rem;" class="neon-badge neon-badge-gold">15 Vectors Blocked</div>
        </div>
      </div>

      <div style="margin-top: 1.5rem; font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-muted); text-align: center;">
        Pre-audit hashes == Post-audit hashes across all Phase 18 runs (100% byte-identical consistency).
      </div>
    </section>
    """,

        # SLIDE 15: ZERO-TRUST RESULT
        """
    <!-- SLIDE 15: ZERO-TRUST AUDIT RESULT -->
    <section class="slide-scene" id="scene-15"
      data-id="15"
      data-tag="SLIDE 15 · AUDIT CERTIFICATION"
      data-title="Zero-Trust Result: Phase 18 Final Audit"
      data-cat="Audit"
      data-time="2.0 min"
      data-citation="Phase 18 Master Validation Audit · Unconditional Decision: GO"
      data-notes="In Phase 18, an adversarial zero-trust audit was executed across 35 machine acceptance gates. Across 5.96 million entities and relationships, exactly zero quarantine escapes occurred, and zero critical, high, medium, or low defects were found. The system received an unconditional GO.">
      
      <div style="text-align: center; max-width: 58rem;">
        <div class="scene-kicker">Phase 18 Final Audit Result</div>
        <h2 class="scene-title">The system was tested as if it could fail.</h2>
        <p class="scene-subtitle">Adversarial audit completed across 35 machine acceptance gates with zero defects and zero quarantine escapes.</p>
      </div>

      <div class="layout-grid-4" style="margin-top: 1.5rem;">
        <div class="glass-panel counter-box" style="border-top: 4px solid var(--emerald-primary);">
          <div class="counter-value counter-emerald">35 / 35</div>
          <div class="counter-label">Machine Gates Passed</div>
          <div class="counter-sub">100% automated test compliance</div>
        </div>

        <div class="glass-panel counter-box" style="border-top: 4px solid var(--gold-bright);">
          <div class="counter-value counter-gold">5.96M+</div>
          <div class="counter-label">Entities &amp; Relations</div>
          <div class="counter-sub">Total verified data volume</div>
        </div>

        <div class="glass-panel counter-box" style="border-top: 4px solid var(--emerald-primary);">
          <div class="counter-value counter-emerald">0</div>
          <div class="counter-label">Quarantine Escapes</div>
          <div class="counter-sub">Strict quarantine boundary held</div>
        </div>

        <div class="glass-panel counter-box" style="border-top: 4px solid var(--emerald-primary); box-shadow: 0 0 35px var(--emerald-glow);">
          <div class="counter-value counter-emerald" style="letter-spacing: 0.1em;">GO</div>
          <div class="counter-label">Final Audit Verdict</div>
          <div class="counter-sub">Unconditional production certification</div>
        </div>
      </div>

      <div style="margin-top: 2rem; padding: 0.75rem 2rem; background: rgba(16, 185, 129, 0.15); border: 1px solid var(--emerald-primary); border-radius: 9999px; font-family: var(--font-mono); font-size: 0.8rem; color: var(--emerald-primary);">
        ● Zero Critical · Zero High · Zero Medium · Zero Low Vulnerabilities
      </div>
    </section>
    """,

        # SLIDE 16: THE ACTUAL PRODUCT
        """
    <!-- SLIDE 16: WORKING PRODUCT TOUR -->
    <section class="slide-scene" id="scene-16"
      data-id="16"
      data-tag="SLIDE 16 · FUNCTIONAL PLATFORM"
      data-title="What Has Already Been Built: Functional Modules"
      data-cat="Built"
      data-time="2.0 min"
      data-citation="Mīzān Production Core · Next.js 15 &amp; FastAPI Backend"
      data-notes="Mīzān is not just an idea or a slide deck. All core research capabilities have been implemented in functional software, including full-text search, hadith reader, isnād visualizer, multi-scholar grading matrix, relational commentary, and Ask Mīzān.">
      
      <div style="text-align: center; max-width: 58rem;">
        <div class="scene-kicker">Concrete Reality</div>
        <h2 class="scene-title">This is not just a concept.</h2>
        <p class="scene-subtitle">A fully functional, high-performance research platform running on modern web architecture.</p>
      </div>

      <div class="layout-grid-3" style="margin-top: 1rem;">
        <div class="glass-panel glass-panel-emerald">
          <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">⚡</div>
          <h4 style="color: #ffffff; font-size: 1rem;">Full-Text &amp; Root Search</h4>
          <p style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.5rem;">
            Sub-second Arabic root, stem, and fuzzy search across 715,790 hadiths and all 425 collections.
          </p>
        </div>

        <div class="glass-panel">
          <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">📖</div>
          <h4 style="color: #ffffff; font-size: 1rem;">Canonical Reader</h4>
          <p style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.5rem;">
            Fully vocalized Arabic display with side-by-side English translations and cross-edition numbering.
          </p>
        </div>

        <div class="glass-panel glass-panel-emerald">
          <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🕸️</div>
          <h4 style="color: #ffffff; font-size: 1rem;">Transmission Visualizer</h4>
          <p style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.5rem;">
            Interactive canvas and graph rendering of transmission networks with narrator biographical overlays.
          </p>
        </div>

        <div class="glass-panel">
          <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">⚖️</div>
          <h4 style="color: #ffffff; font-size: 1rem;">Grading Matrix</h4>
          <p style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.5rem;">
            Nine-scholar comparative evaluation display showing consensus, differences, and specific rulings.
          </p>
        </div>

        <div class="glass-panel glass-panel-emerald">
          <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">💬</div>
          <h4 style="color: #ffffff; font-size: 1rem;">Relational Sharḥ</h4>
          <p style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.5rem;">
            Commentary engine linking specific hadiths to classical explanations with verified boundary scopes.
          </p>
        </div>

        <div class="glass-panel">
          <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🤖</div>
          <h4 style="color: #ffffff; font-size: 1rem;">Ask Mīzān (RAG)</h4>
          <p style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.5rem;">
            Evidence-grounded conversational research assistant powered by verified database context.
          </p>
        </div>
      </div>
    </section>
    """,

        # SLIDE 17: WHAT IS STILL GROWING (BUILT VS NEXT)
        """
    <!-- SLIDE 17: TRANSPARENT ROADMAP -->
    <section class="slide-scene" id="scene-17"
      data-id="17"
      data-tag="SLIDE 17 · HONEST ROADMAP"
      data-title="What is Still Growing: Current vs Next"
      data-cat="Roadmap"
      data-time="2.0 min"
      data-citation="Mīzān Strategic Development Roadmap · Milestone Deliverables"
      data-notes="We believe in complete scholarly transparency. Mīzān is functional and certified today, but hadith scholarship is vast. We clearly separate what is completed right now from what is slated for subsequent research phases.">
      
      <div style="text-align: center; max-width: 58rem;">
        <div class="scene-kicker">Honest Growth Path</div>
        <h2 class="scene-title">Mīzān is already usable — but the work is not finished.</h2>
        <p class="scene-subtitle">Distinguishing current certified deliverables from ongoing expansion initiatives.</p>
      </div>

      <div class="layout-grid-2" style="margin-top: 1rem;">
        <div class="glass-panel glass-panel-emerald" style="padding: 1.75rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(16, 185, 129, 0.3); padding-bottom: 0.5rem; margin-bottom: 1rem;">
            <span style="font-family: var(--font-display); font-size: 1.1rem; color: var(--emerald-primary); font-weight: bold;">
              CURRENT (Built &amp; Certified)
            </span>
            <span class="neon-badge neon-badge-emerald">Production Ready</span>
          </div>
          <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.65rem; font-size: 0.85rem; color: var(--text-secondary);">
            <li>✔ Kutub al-Sittah core &amp; 425 collections fully normalized</li>
            <li>✔ 49,844 verified narrator biographical profiles</li>
            <li>✔ 95,598 cross-edition numbering mappings across 18 schemes</li>
            <li>✔ 65,420 scholarly evaluations across 9 authorities</li>
            <li>✔ Phase 12 relational commentary prototype (1,202 units)</li>
            <li>✔ Evidence-bounded Ask Mīzān RAG pipeline</li>
          </ul>
        </div>

        <div class="glass-panel" style="padding: 1.75rem; border-color: rgba(245, 158, 11, 0.3);">
          <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(245, 158, 11, 0.3); padding-bottom: 0.5rem; margin-bottom: 1rem;">
            <span style="font-family: var(--font-display); font-size: 1.1rem; color: var(--gold-bright); font-weight: bold;">
              NEXT (In Development &amp; Planned)
            </span>
            <span class="neon-badge neon-badge-gold">Strategic Roadmap</span>
          </div>
          <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.65rem; font-size: 0.85rem; color: var(--text-secondary);">
            <li>⏳ Expanding commentary coverage across complete classical compendia</li>
            <li>⏳ High-resolution physical manuscript facsimile alignment</li>
            <li>⏳ Morphological Arabic NLP parsing and semantic relation tagging</li>
            <li>⏳ Direct integration with academic citation and export formats</li>
            <li>⏳ Expanded biographical coverage for obscure early transmitters</li>
            <li>⏳ Institutional multi-user collaborative workspace</li>
          </ul>
        </div>
      </div>
    </section>
    """,

        # SLIDE 18: THE LONG-TERM VISION
        """
    <!-- SLIDE 18: LONG-TERM VISION -->
    <section class="slide-scene" id="scene-18"
      data-id="18"
      data-tag="SLIDE 18 · LONG-TERM VISION"
      data-title="The Long-Term Vision: Digital Research Infrastructure"
      data-cat="Vision"
      data-time="2.0 min"
      data-citation="Digital Humanities Strategic Framework · Long-Term Vision"
      data-notes="Our long-term goal is to build an open, enduring research infrastructure for the entire discipline of Islamic Studies. By combining strict fidelity to classical principles with modern computational tools, Mīzān can serve as the foundational research workbench for scholars worldwide.">
      
      <div style="text-align: center; max-width: 58rem;">
        <div class="scene-kicker">Disciplinary Transformation</div>
        <h2 class="scene-title">From a database to a research infrastructure.</h2>
        <p class="scene-subtitle">Preserving classical scholarly provenance while empowering the next century of digital humanities.</p>
      </div>

      <div class="layout-grid-3" style="margin-top: 1rem;">
        <div class="glass-panel glass-panel-emerald" style="padding: 2rem; text-align: center;">
          <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">🏛️</div>
          <h3 style="font-family: var(--font-display); font-size: 1.15rem; color: #ffffff; margin-bottom: 0.5rem;">Scholarly Preservation</h3>
          <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.6;">
            Safeguards classical textual traditions and nuanced critical methodologies in standardized, permanent digital form.
          </p>
        </div>

        <div class="glass-panel" style="padding: 2rem; text-align: center;">
          <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">🔬</div>
          <h3 style="font-family: var(--font-display); font-size: 1.15rem; color: #ffffff; margin-bottom: 0.5rem;">Computational Research</h3>
          <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.6;">
            Enables macro-level analysis of transmission networks, lexical evolution, and geographical dissemination across millions of data points.
          </p>
        </div>

        <div class="glass-panel glass-panel-emerald" style="padding: 2rem; text-align: center;">
          <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">🌐</div>
          <h3 style="font-family: var(--font-display); font-size: 1.15rem; color: #ffffff; margin-bottom: 0.5rem;">Global Academic Access</h3>
          <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.6;">
            Democratizes access to primary sources, cross-edition references, and commentaries for university researchers worldwide.
          </p>
        </div>
      </div>
    </section>
    """,

        # SLIDE 19: WHY THIS MATTERS
        """
    <!-- SLIDE 19: ACADEMIC IMPACT -->
    <section class="slide-scene" id="scene-19"
      data-id="19"
      data-tag="SLIDE 19 · SCHOLARLY IMPACT"
      data-title="Why This Matters: Impact on Islamic Studies"
      data-cat="Impact"
      data-time="2.0 min"
      data-citation="Academic Value Assessment · Digital Humanities Methodologies"
      data-notes="Why does this matter for a university professor or funding institution? Because it transforms months of tedious manual cross-referencing into minutes of verified analysis, while creating an open foundation for collaborative research and pedagogical excellence.">
      
      <div style="text-align: center; max-width: 58rem;">
        <div class="scene-kicker">Scholarly Value Proposition</div>
        <h2 class="scene-title">Why could this matter for Islamic Studies?</h2>
        <p class="scene-subtitle">Accelerating research, illuminating transmission networks, and setting a standard for digital humanities.</p>
      </div>

      <div class="layout-grid-4" style="margin-top: 1rem;">
        <div class="glass-panel glass-panel-emerald">
          <div style="font-size: 1.75rem; margin-bottom: 0.5rem;">⏱️</div>
          <h4 style="color: #ffffff; font-size: 1rem;">Accelerates Research</h4>
          <p style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.5rem;">
            Tasks requiring weeks in library stacks—tracing isnād variants or cross-referencing editions—take seconds.
          </p>
        </div>

        <div class="glass-panel">
          <div style="font-size: 1.75rem; margin-bottom: 0.5rem;">📊</div>
          <h4 style="color: #ffffff; font-size: 1rem;">Novel Methodologies</h4>
          <p style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.5rem;">
            Enables network analysis, chronological mapping, and lexical variant tracking across millions of data points.
          </p>
        </div>

        <div class="glass-panel glass-panel-emerald">
          <div style="font-size: 1.75rem; margin-bottom: 0.5rem;">🎓</div>
          <h4 style="color: #ffffff; font-size: 1rem;">Pedagogical Power</h4>
          <p style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.5rem;">
            Provides students with intuitive, visual mental models of complex hadith sciences and isnād structures.
          </p>
        </div>

        <div class="glass-panel">
          <div style="font-size: 1.75rem; margin-bottom: 0.5rem;">🤝</div>
          <h4 style="color: #ffffff; font-size: 1rem;">Scholarly Transparency</h4>
          <p style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.5rem;">
            Every claim, grade, and text is traceable to physical print volumes with zero AI guesswork.
          </p>
        </div>
      </div>
    </section>
    """,

        # SLIDE 20: FINAL SCENE (HORIZON & INVITATION)
        """
    <!-- SLIDE 20: HORIZON & CLOSING -->
    <section class="slide-scene" id="scene-20"
      data-id="20"
      data-tag="SLIDE 20 · INVITATION TO PARTNER"
      data-title="Closing: Let's Build the Next Stage Together"
      data-cat="Closing"
      data-time="2.0 min"
      data-citation="Mīzān al-Ḥadīth Project Initiative · Academic Partnership"
      data-notes="Professor Syed, colleagues, and supporters: Mīzān al-Ḥadīth was built to serve researchers like you. We have proved that computational digital humanities can be executed with absolute fidelity to classical Islamic scholarship. But to realize its full potential requires institutional partnership and sustained philanthropic support. We invite you to join us in establishing Mīzān as an enduring foundation for Islamic studies.">
      
      <div style="text-align: center; display: flex; flex-direction: column; align-items: center; max-width: 60rem;">
        <div class="hero-arabic-calligraphy" dir="rtl" style="font-size: clamp(3rem, 5.5vw, 5.5rem);">مِيزَانُ الحَدِيث</div>
        <h1 class="hero-main-title" style="font-size: clamp(2rem, 3.5vw, 3.5rem); margin-bottom: 0.5rem;">MĪZĀN AL-ḤADĪTH</h1>
        <div class="hero-divider" style="margin-bottom: 1.25rem;"></div>
        <p style="font-family: var(--font-arabic); font-size: 1.35rem; color: var(--gold-bright); font-style: italic; max-width: 44rem; margin-bottom: 1.5rem;">
          "Preserving the evidence. Connecting the scholarship. Making hadith research easier to explore."
        </p>

        <div class="layout-grid-2" style="max-width: 52rem; margin-top: 0.5rem; text-align: left;">
          <div class="glass-panel glass-panel-emerald" style="padding: 1.25rem;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--emerald-primary); font-weight: bold; margin-bottom: 0.25rem;">CURRENT ACCOMPLISHMENT</div>
            <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.5;">
              Built, rigorously tested, and certified across 18 audit phases with 35 machine acceptance gates and zero critical defects.
            </p>
          </div>
          <div class="glass-panel" style="padding: 1.25rem; border-color: rgba(212, 175, 55, 0.4);">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--gold-bright); font-weight: bold; margin-bottom: 0.25rem;">NEXT STAGE COLLABORATION</div>
            <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.5;">
              Academic partnership, faculty advisory guidance, manuscript integration, and institutional endowment support.
            </p>
          </div>
        </div>

        <div style="margin-top: 2rem; font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-muted);">
          Repository / public release: not yet published · Prepared for Academic Review · October 2026
        </div>
      </div>
    </section>
    """
    ]
    return "\n".join(slides)

def get_html_footer():
    return """
  </main>

  <!-- DECK BOTTOM FOOTER -->
  <footer class="deck-footer">
    <div class="footer-source-note" id="footerSourceNote">
      <span class="footer-source-dot"></span>
      <span id="footerSourceText">Source: Phase 18 Certified Release Baseline · October 2026</span>
    </div>

    <div class="footer-nav-track">
      <button class="btn-nav-arrow" id="btnPrev" title="Previous Slide [←, Left Arrow]" disabled>←</button>
      <div class="progress-track-wrap">
        <div class="progress-bar-fill" id="progressBarFill"></div>
      </div>
      <span class="slide-counter-display" id="slideCounterDisplay">01 / 20</span>
      <button class="btn-nav-arrow" id="btnNext" title="Next Slide [→, Space, Right Arrow]">→</button>
    </div>
  </footer>

  <!-- SPEAKER NOTES DRAWER -->
  <aside class="notes-drawer" id="notesDrawer">
    <div class="notes-header-bar">
      <div class="notes-heading">SPEAKER SCRIPT &amp; ACADEMIC RATIONALE</div>
      <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--emerald-primary);" id="notesPacingEst">Est: 1.5 min</div>
    </div>
    <div class="notes-text-body" id="notesBody">
      "Good morning, Professor Syed and colleagues. Today, we are presenting Mīzān al-Ḥadīth. For centuries, Islamic scholars have engaged in some of the most rigorous historical-critical analysis in human civilization..."
    </div>
  </aside>

  <!-- 20-SLIDE OVERVIEW MODAL -->
  <div class="overview-modal" id="overviewModal">
    <div class="overview-container">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding-bottom: 1rem;">
        <div>
          <h3 style="font-family: var(--font-display); font-size: 1.25rem; color: #ffffff;">Mīzān al-Ḥadīth · 20-Slide Directory</h3>
          <span style="font-size: 0.75rem; color: var(--gold-bright); font-family: var(--font-mono);">Click any tile to jump · Press [ESC] or [O] to Close</span>
        </div>
        <button class="btn-icon" id="btnCloseOverview">✕ Close</button>
      </div>
      <div class="overview-grid-20" id="overviewGrid20"></div>
    </div>
  </div>
"""

def get_javascript():
    return """
  <script>
  /**
   * MĪZĀN AL-ḤADĪTH — PRESENTATION 01 CINEMATIC ENGINE
   * Complete presentation controller, particle canvas, stopwatch, keyboard listener
   */
  document.addEventListener("DOMContentLoaded", () => {
    const scenes = Array.from(document.querySelectorAll(".slide-scene"));
    const slideTagPill = document.getElementById("slideTagPill");
    const footerSourceText = document.getElementById("footerSourceText");
    const slideCounterDisplay = document.getElementById("slideCounterDisplay");
    const progressBarFill = document.getElementById("progressBarFill");
    const btnPrev = document.getElementById("btnPrev");
    const btnNext = document.getElementById("btnNext");
    const btnNotesToggle = document.getElementById("btnNotesToggle");
    const notesDrawer = document.getElementById("notesDrawer");
    const notesBody = document.getElementById("notesBody");
    const notesPacingEst = document.getElementById("notesPacingEst");
    const btnOverviewToggle = document.getElementById("btnOverviewToggle");
    const btnCloseOverview = document.getElementById("btnCloseOverview");
    const overviewModal = document.getElementById("overviewModal");
    const overviewGrid20 = document.getElementById("overviewGrid20");
    const btnFullscreen = document.getElementById("btnFullscreen");
    const timerBadge = document.getElementById("timerBadge");
    const timerIndicator = document.getElementById("timerIndicator");
    const timerText = document.getElementById("timerText");

    let currentIdx = 0;
    let timerSeconds = 0;
    let timerRunning = true;
    let autoPlayInterval = null;

    // Build 20-Slide Overview Grid Tiles
    overviewGrid20.innerHTML = "";
    scenes.forEach((scene, idx) => {
      const tile = document.createElement("div");
      tile.className = `overview-card-tile ${idx === 0 ? "active" : ""}`;
      tile.innerHTML = `
        <div class="overview-tile-num">SLIDE ${String(idx + 1).padStart(2, "0")}</div>
        <div class="overview-tile-title">${scene.getAttribute("data-title") || ""}</div>
        <div class="overview-tile-cat">${scene.getAttribute("data-cat") || ""}</div>
      `;
      tile.addEventListener("click", () => {
        goToScene(idx);
        overviewModal.classList.remove("open");
        btnOverviewToggle.classList.remove("active");
      });
      overviewGrid20.appendChild(tile);
    });

    // Stopwatch Timer
    setInterval(() => {
      if (!timerRunning) return;
      timerSeconds++;
      const m = Math.floor(timerSeconds / 60);
      const s = timerSeconds % 60;
      timerText.textContent = `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
    }, 1000);

    timerBadge.addEventListener("click", () => {
      timerRunning = !timerRunning;
      timerIndicator.style.background = timerRunning ? "var(--emerald-primary)" : "var(--crimson-primary)";
      timerIndicator.style.boxShadow = timerRunning ? "0 0 8px var(--emerald-primary)" : "0 0 8px var(--crimson-primary)";
    });

    function updateSceneView(prevIdx, newIdx) {
      scenes.forEach((scene, idx) => {
        scene.classList.remove("active", "prev-scene", "next-scene");
        if (idx === newIdx) {
          scene.classList.add("active");
        } else if (idx < newIdx) {
          scene.classList.add("prev-scene");
        } else {
          scene.classList.add("next-scene");
        }
      });

      const activeScene = scenes[newIdx];
      const tag = activeScene.getAttribute("data-tag") || `SLIDE ${String(newIdx + 1).padStart(2, "0")}`;
      const citation = activeScene.getAttribute("data-citation") || "Mīzān al-Ḥadīth Certified Baseline";
      const notes = activeScene.getAttribute("data-notes") || "No speaker notes recorded.";
      const timeEst = activeScene.getAttribute("data-time") || "2.0 min";

      slideTagPill.textContent = tag;
      footerSourceText.textContent = `Source: ${citation}`;
      slideCounterDisplay.textContent = `${String(newIdx + 1).padStart(2, "0")} / ${String(scenes.length).padStart(2, "0")}`;
      notesBody.textContent = `"${notes}"`;
      notesPacingEst.textContent = `Est: ${timeEst}`;

      const progressPct = ((newIdx + 1) / scenes.length) * 100;
      progressBarFill.style.width = `${progressPct}%`;

      btnPrev.disabled = (newIdx === 0);
      btnNext.disabled = (newIdx === scenes.length - 1);

      // Update overview tiles active state
      const tiles = overviewGrid20.querySelectorAll(".overview-card-tile");
      tiles.forEach((t, i) => t.classList.toggle("active", i === newIdx));

      // Trigger animated counters if present on active scene
      const counters = activeScene.querySelectorAll(".counter-value[data-target]");
      counters.forEach(c => animateCounter(c));
    }

    function animateCounter(el) {
      const target = parseInt(el.getAttribute("data-target"), 10);
      if (isNaN(target)) return;
      const duration = 1200;
      const start = 0;
      const startTime = performance.now();

      function update(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const easeOut = 1 - Math.pow(1 - progress, 3);
        const current = Math.floor(start + (target - start) * easeOut);
        el.textContent = current.toLocaleString();
        if (progress < 1) {
          requestAnimationFrame(update);
        } else {
          el.textContent = target.toLocaleString();
        }
      }
      requestAnimationFrame(update);
    }

    function goToScene(idx) {
      if (idx < 0 || idx >= scenes.length) return;
      const prevIdx = currentIdx;
      currentIdx = idx;
      updateSceneView(prevIdx, currentIdx);
    }

    btnNext.addEventListener("click", () => goToScene(currentIdx + 1));
    btnPrev.addEventListener("click", () => goToScene(currentIdx - 1));

    // Keyboard Shortcuts
    document.addEventListener("keydown", (e) => {
      if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;

      if (e.key === "ArrowRight" || e.key === " " || e.key === "PageDown") {
        e.preventDefault();
        goToScene(currentIdx + 1);
      } else if (e.key === "ArrowLeft" || e.key === "PageUp") {
        e.preventDefault();
        goToScene(currentIdx - 1);
      } else if (e.key === "Home") {
        e.preventDefault();
        goToScene(0);
      } else if (e.key === "End") {
        e.preventDefault();
        goToScene(scenes.length - 1);
      } else if (e.key.toLowerCase() === "n") {
        e.preventDefault();
        notesDrawer.classList.toggle("open");
        btnNotesToggle.classList.toggle("active");
      } else if (e.key.toLowerCase() === "o") {
        e.preventDefault();
        const isOpen = overviewModal.classList.toggle("open");
        btnOverviewToggle.classList.toggle("active", isOpen);
      } else if (e.key.toLowerCase() === "f") {
        e.preventDefault();
        toggleFullscreen();
      } else if (e.key === "Escape") {
        if (overviewModal.classList.contains("open")) {
          overviewModal.classList.remove("open");
          btnOverviewToggle.classList.remove("active");
        }
        if (notesDrawer.classList.contains("open")) {
          notesDrawer.classList.remove("open");
          btnNotesToggle.classList.remove("active");
        }
      }
    });

    // Notes Toggle
    btnNotesToggle.addEventListener("click", () => {
      notesDrawer.classList.toggle("open");
      btnNotesToggle.classList.toggle("active");
    });

    // Overview Toggle
    btnOverviewToggle.addEventListener("click", () => {
      const isOpen = overviewModal.classList.toggle("open");
      btnOverviewToggle.classList.toggle("active", isOpen);
    });
    btnCloseOverview.addEventListener("click", () => {
      overviewModal.classList.remove("open");
      btnOverviewToggle.classList.remove("active");
    });

    // Fullscreen Toggle
    function toggleFullscreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
        btnFullscreen.classList.add("active");
      } else {
        if (document.exitFullscreen) {
          document.exitFullscreen().catch(() => {});
        }
        btnFullscreen.classList.remove("active");
      }
    }
    btnFullscreen.addEventListener("click", toggleFullscreen);

    // BACKGROUND CANVAS: PARTICLES & ISLAMIC GIRIH TESSELLATION
    const canvas = document.getElementById("bgCanvas");
    const ctx = canvas.getContext("2d");
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    window.addEventListener("resize", () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    });

    // Create 65 ambient drifting stars
    const particles = [];
    for (let i = 0; i < 65; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        r: Math.random() * 1.5 + 0.5,
        dx: (Math.random() - 0.5) * 0.3,
        dy: (Math.random() - 0.5) * 0.3,
        color: Math.random() > 0.4 ? "rgba(212, 175, 55, 0.4)" : "rgba(16, 185, 129, 0.4)"
      });
    }

    let rotAngle = 0;
    function renderBg() {
      ctx.clearRect(0, 0, width, height);

      // Draw subtle rotating Islamic 8-point geometric rosette in center background
      rotAngle += 0.0005;
      ctx.save();
      ctx.translate(width / 2, height / 2);
      ctx.rotate(rotAngle);
      ctx.strokeStyle = "rgba(212, 175, 55, 0.03)";
      ctx.lineWidth = 1;

      const size = Math.min(width, height) * 0.45;
      for (let i = 0; i < 8; i++) {
        ctx.rotate(Math.PI / 4);
        ctx.strokeRect(-size / 2, -size / 2, size, size);
      }
      ctx.restore();

      // Render drifting particles
      particles.forEach(p => {
        p.x += p.dx;
        p.y += p.dy;
        if (p.x < 0) p.x = width;
        if (p.x > width) p.x = 0;
        if (p.y < 0) p.y = height;
        if (p.y > height) p.y = 0;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.fill();
      });

      requestAnimationFrame(renderBg);
    }
    requestAnimationFrame(renderBg);

    // Initial Scene View
    updateSceneView(0, 0);
  });
  </script>
</body>
</html>
"""

def build_presentation():
    full_html = (
        get_html_head() +
        get_css() +
        get_body_start() +
        get_slides_html() +
        get_html_footer() +
        get_javascript()
    )

    out_file = os.path.abspath("Mizan_Al_Hadith_Presentation_01.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Master standalone cinematic presentation written to: {out_file}")

    # Synchronize with presentation/presentation_01/index.html
    copy_dest = os.path.abspath("presentation/presentation_01/index.html")
    with open(copy_dest, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Synchronized copy written to: {copy_dest}")

if __name__ == "__main__":
    build_presentation()
