"""
Build MĪZĀN AL-ḤADĪTH Presentation 01 — 20-Slide Master Presentation
Generates:
1. Mizan_al_Hadith_Introduction_Presentation.pptx (Standalone PowerPoint)
2. presentation/Mizan_al_Hadith_Presentation_Print.html (Standalone HTML for PDF printing)
3. Mizan_al_Hadith_Introduction_Presentation.pdf (Rendered via Edge headless)
"""

import os
import sys
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ==============================================================================
# COLOR PALETTE TOKENS
# ==============================================================================
COLOR_BG = RGBColor(248, 244, 236)        # Warm Parchment #f8f4ec
COLOR_SURFACE = RGBColor(255, 255, 255)   # Pure White
COLOR_SURFACE_WARM = RGBColor(253, 251, 247) # Soft Ivory #fdfbf7
COLOR_EMERALD_DEEP = RGBColor(10, 41, 33) # Deep Forest #0a2921
COLOR_EMERALD_DARK = RGBColor(18, 61, 50) # Dark Emerald #123d32
COLOR_EMERALD_PRIMARY = RGBColor(25, 81, 67) # Primary Emerald #195143
COLOR_EMERALD_LIGHT = RGBColor(40, 107, 89) # Light Emerald #286b59
COLOR_EMERALD_SOFT = RGBColor(226, 237, 232) # Soft Mint #e2ede8

COLOR_GOLD_PRIMARY = RGBColor(167, 124, 56) # Antique Gold #a77c38
COLOR_GOLD_DARK = RGBColor(110, 80, 32)     # Dark Gold #6e5020
COLOR_GOLD_LIGHT = RGBColor(201, 155, 79)   # Light Gold #c99b4f
COLOR_GOLD_SOFT = RGBColor(244, 235, 214)   # Soft Gold Pill #f4ebd6
COLOR_GOLD_BORDER = RGBColor(220, 200, 164) # Border #dcc8a4

COLOR_INK_PRIMARY = RGBColor(24, 28, 26)   # Charcoal #181c1a
COLOR_INK_BODY = RGBColor(45, 51, 48)      # Body Charcoal #2d3330
COLOR_INK_MUTED = RGBColor(103, 112, 106)  # Muted #67706a
COLOR_INK_LIGHT = RGBColor(142, 150, 144)  # Light #8e9690
COLOR_BORDER = RGBColor(227, 220, 206)     # Subtle Border #e3dcce

COLOR_ROSE_DEEP = RGBColor(159, 18, 57)    # Crimson #9f1239
COLOR_ROSE_SOFT = RGBColor(255, 228, 230)  # Soft Rose #ffe4e6
COLOR_AMBER_DEEP = RGBColor(180, 83, 9)    # Amber #b45309
COLOR_AMBER_SOFT = RGBColor(254, 243, 199) # Soft Amber #fef3c7
COLOR_BLUE_DEEP = RGBColor(29, 78, 216)    # Blue #1d4ed8
COLOR_BLUE_SOFT = RGBColor(219, 234, 254)  # Soft Blue #dbeafe
COLOR_PURPLE_DEEP = RGBColor(107, 33, 168) # Purple #6b21a8
COLOR_PURPLE_SOFT = RGBColor(243, 232, 255)# Soft Purple #f3e8ff

FONT_DISPLAY = "Georgia"
FONT_BODY = "Calibri"

SLIDE_WIDTH = 13.333
SLIDE_HEIGHT = 7.5

def create_base_slide(prs, category_tag, slide_title, subtitle, source_note, slide_num):
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # blank layout
    
    # Background shape
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(SLIDE_WIDTH), Inches(SLIDE_HEIGHT))
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_BG
    bg.line.fill.background()
    
    # Top Category Tag
    tx_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.35))
    tf_cat = tx_cat.text_frame
    tf_cat.word_wrap = True
    tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_tag.upper()
    p_cat.font.name = FONT_BODY
    p_cat.font.size = Pt(9.5)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_GOLD_PRIMARY
    
    # Slide Title
    tx_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.7))
    tf_title = tx_title.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = slide_title
    p_title.font.name = FONT_DISPLAY
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_EMERALD_DEEP
    
    # Slide Subtitle
    if subtitle:
        tx_sub = slide.shapes.add_textbox(Inches(0.8), Inches(1.45), Inches(11.7), Inches(0.45))
        tf_sub = tx_sub.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle
        p_sub.font.name = FONT_DISPLAY
        p_sub.font.size = Pt(13)
        p_sub.font.italic = True
        p_sub.font.color.rgb = COLOR_INK_MUTED
        
    # Footer Divider Line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.85), Inches(11.733), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_BORDER
    line.line.fill.background()
    
    # Footer Citation
    tx_cite = slide.shapes.add_textbox(Inches(0.8), Inches(6.95), Inches(9.5), Inches(0.3))
    tf_cite = tx_cite.text_frame
    tf_cite.margin_left = tf_cite.margin_top = tf_cite.margin_right = tf_cite.margin_bottom = 0
    p_cite = tf_cite.paragraphs[0]
    p_cite.text = f"Source: {source_note}" if source_note else "Mīzān al-Ḥadīth Research Platform"
    p_cite.font.name = FONT_BODY
    p_cite.font.size = Pt(8.5)
    p_cite.font.color.rgb = COLOR_INK_LIGHT
    
    # Footer Counter
    tx_num = slide.shapes.add_textbox(Inches(10.5), Inches(6.95), Inches(2.0), Inches(0.3))
    tf_num = tx_num.text_frame
    tf_num.margin_left = tf_num.margin_top = tf_num.margin_right = tf_num.margin_bottom = 0
    p_num = tf_num.paragraphs[0]
    p_num.alignment = PP_ALIGN.RIGHT
    p_num.text = f"{slide_num:02d} / 20"
    p_num.font.name = FONT_BODY
    p_num.font.size = Pt(9)
    p_num.font.bold = True
    p_num.font.color.rgb = COLOR_INK_BODY
    
    return slide

def add_card(slide, left, top, width, height, bg_color=COLOR_SURFACE, border_color=COLOR_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card

def add_speaker_note(slide, note_text):
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = note_text

# ==============================================================================
# MAIN PPTX GENERATION SCRIPT
# ==============================================================================
def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_WIDTH)
    prs.slide_height = Inches(SLIDE_HEIGHT)
    
    print("Building 20 Slides for Mīzān al-Ḥadīth...")
    
    # --------------------------------------------------------------------------
    # SLIDE 01: TITLE FOLIO
    # --------------------------------------------------------------------------
    slide1 = prs.slides.add_slide(prs.slide_layouts[6])
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(SLIDE_WIDTH), Inches(SLIDE_HEIGHT))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_BG
    bg1.line.fill.background()
    
    # Pill Tag
    add_card(slide1, 4.4, 0.9, 4.5, 0.45, COLOR_GOLD_SOFT, COLOR_GOLD_BORDER)
    tx_pill = slide1.shapes.add_textbox(Inches(4.4), Inches(0.95), Inches(4.5), Inches(0.35))
    p_pill = tx_pill.text_frame.paragraphs[0]
    p_pill.alignment = PP_ALIGN.CENTER
    p_pill.text = "ACADEMIC RESEARCH PLATFORM & OVERVIEW"
    p_pill.font.name = FONT_BODY
    p_pill.font.size = Pt(9.5)
    p_pill.font.bold = True
    p_pill.font.color.rgb = COLOR_GOLD_DARK
    
    # Arabic Title
    tx_ar = slide1.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.333), Inches(0.9))
    p_ar = tx_ar.text_frame.paragraphs[0]
    p_ar.alignment = PP_ALIGN.CENTER
    p_ar.text = "مِيزَانُ الحَدِيث"
    p_ar.font.name = "Amiri"
    p_ar.font.size = Pt(36)
    p_ar.font.bold = True
    p_ar.font.color.rgb = COLOR_GOLD_PRIMARY
    
    # Main Latin Title
    tx_t1 = slide1.shapes.add_textbox(Inches(1.0), Inches(2.55), Inches(11.333), Inches(1.0))
    p_t1 = tx_t1.text_frame.paragraphs[0]
    p_t1.alignment = PP_ALIGN.CENTER
    p_t1.text = "MĪZĀN AL-ḤADĪTH"
    p_t1.font.name = FONT_DISPLAY
    p_t1.font.size = Pt(46)
    p_t1.font.bold = True
    p_t1.font.color.rgb = COLOR_EMERALD_DEEP
    
    # Subtitle
    tx_sub1 = slide1.shapes.add_textbox(Inches(2.0), Inches(3.65), Inches(9.333), Inches(0.8))
    p_sub1 = tx_sub1.text_frame.paragraphs[0]
    p_sub1.alignment = PP_ALIGN.CENTER
    p_sub1.text = "A Research Platform for Exploring Hadith, Narrators, Isnād,\nCommentaries, and Scholarly Evaluation"
    p_sub1.font.name = FONT_DISPLAY
    p_sub1.font.size = Pt(16)
    p_sub1.font.italic = True
    p_sub1.font.color.rgb = COLOR_INK_BODY
    
    # Metrics Strip (5 Cards)
    metrics_s1 = [
        ("715,790", "Canonical Hadiths"),
        ("49,844", "Narrators (Rijāl)"),
        ("577,024", "Transmission Chains"),
        ("4,414,211", "Chain Links"),
        ("65,420", "Scholarly Grades")
    ]
    card_w = 2.15
    start_x = (SLIDE_WIDTH - (len(metrics_s1) * card_w + (len(metrics_s1) - 1) * 0.25)) / 2
    for i, (m_val, m_lbl) in enumerate(metrics_s1):
        cx = start_x + i * (card_w + 0.25)
        add_card(slide1, cx, 4.8, card_w, 1.25, COLOR_SURFACE, COLOR_BORDER)
        tx_m = slide1.shapes.add_textbox(Inches(cx + 0.1), Inches(4.9), Inches(card_w - 0.2), Inches(1.0))
        tf_m = tx_m.text_frame
        p_val = tf_m.paragraphs[0]
        p_val.alignment = PP_ALIGN.CENTER
        p_val.text = m_val
        p_val.font.name = FONT_DISPLAY
        p_val.font.size = Pt(18)
        p_val.font.bold = True
        p_val.font.color.rgb = COLOR_EMERALD_PRIMARY
        p_lbl = tf_m.add_paragraph()
        p_lbl.alignment = PP_ALIGN.CENTER
        p_lbl.text = m_lbl
        p_lbl.font.name = FONT_BODY
        p_lbl.font.size = Pt(9.5)
        p_lbl.font.color.rgb = COLOR_INK_MUTED
        
    # Credits Footer
    tx_cred = slide1.shapes.add_textbox(Inches(1.0), Inches(6.35), Inches(11.333), Inches(0.6))
    p_c1 = tx_cred.text_frame.paragraphs[0]
    p_c1.alignment = PP_ALIGN.CENTER
    p_c1.text = "Project Mīzān Research & Engineering Group · October 2026"
    p_c1.font.name = FONT_BODY
    p_c1.font.size = Pt(10)
    p_c1.font.bold = True
    p_c1.font.color.rgb = COLOR_INK_PRIMARY
    p_c2 = tx_cred.text_frame.add_paragraph()
    p_c2.alignment = PP_ALIGN.CENTER
    p_c2.text = "Prepared for Professor Mairaj Syed, Academic Colleagues & Research Sponsors"
    p_c2.font.name = FONT_BODY
    p_c2.font.size = Pt(9)
    p_c2.font.color.rgb = COLOR_INK_MUTED
    
    add_speaker_note(slide1, "Good morning, Professor Syed and colleagues. Today, we are presenting Mīzān al-Ḥadīth. For centuries, Islamic scholars have engaged in some of the most rigorous historical-critical analysis in human civilization. Yet our modern digital tools have remained flat, fragmented, and disconnected. Mīzān was created to bring the full power of modern relational graphs and digital humanities to this sacred heritage—without compromising a single principle of classical methodology.")

    # --------------------------------------------------------------------------
    # SLIDE 02: THE PROBLEM
    # --------------------------------------------------------------------------
    slide2 = create_base_slide(prs, "The Scholarly Challenge", 
                               "Hadith knowledge is rich — but finding the connections is difficult.", 
                               "The daily friction researchers face across fragmented digital tools and paper editions", 
                               "Mīzān System Survey: Al-Maktaba al-Shamelah, Sunnah.com, and academic workflows", 2)
    
    col_w2 = 3.65
    gap2 = 0.38
    left2 = 0.8
    top2 = 2.1
    h2 = 4.4
    
    # Box 1: Unstructured Archives
    add_card(slide2, left2, top2, col_w2, h2, COLOR_SURFACE, COLOR_BORDER)
    # top accent strip
    top_strip1 = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left2), Inches(top2), Inches(col_w2), Inches(0.1))
    top_strip1.fill.solid()
    top_strip1.fill.fore_color.rgb = COLOR_AMBER_DEEP
    top_strip1.line.fill.background()
    
    tx2_1 = slide2.shapes.add_textbox(Inches(left2 + 0.25), Inches(top2 + 0.3), Inches(col_w2 - 0.5), Inches(3.8))
    tf2_1 = tx2_1.text_frame
    tf2_1.word_wrap = True
    p = tf2_1.paragraphs[0]
    p.text = "01 · UNSTRUCTURED ARCHIVES"
    p.font.name = FONT_BODY
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER_DEEP
    p = tf2_1.add_paragraph()
    p.text = "Massive Text, Weak Structure"
    p.font.name = FONT_DISPLAY
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_INK_PRIMARY
    p = tf2_1.add_paragraph()
    p.text = "\n• Examples like al-Maktaba al-Shamelah contain millions of words, but text is unlinked and noisy.\n• Different printings shift numbering by dozens of hadiths.\n• Identifying common narrators requires manual paper collation.\n• Commentaries are separated in multi-volume scans."
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_INK_BODY

    # Box 2: Flat Consumer Portals
    left2_2 = left2 + col_w2 + gap2
    add_card(slide2, left2_2, top2, col_w2, h2, COLOR_SURFACE, COLOR_BORDER)
    top_strip2 = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left2_2), Inches(top2), Inches(col_w2), Inches(0.1))
    top_strip2.fill.solid()
    top_strip2.fill.fore_color.rgb = COLOR_BLUE_DEEP
    top_strip2.line.fill.background()
    
    tx2_2 = slide2.shapes.add_textbox(Inches(left2_2 + 0.25), Inches(top2 + 0.3), Inches(col_w2 - 0.5), Inches(3.8))
    tf2_2 = tx2_2.text_frame
    tf2_2.word_wrap = True
    p = tf2_2.paragraphs[0]
    p.text = "02 · FLAT CONSUMER WEBSITES"
    p.font.name = FONT_BODY
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE_DEEP
    p = tf2_2.add_paragraph()
    p.text = "Clean Access, Flattened Nuance"
    p.font.name = FONT_DISPLAY
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_INK_PRIMARY
    p = tf2_2.add_paragraph()
    p.text = "\n• Excellent for general readers, but isnāds are displayed as dead strings of text.\n• Scholarly evaluations are flattened into single generic labels like 'Sahih'.\n• Hides genuine differences between critics like al-Albani, Zubayr, and al-Arna'ut.\n• No interactive transmission graph or textual variant tools."
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_INK_BODY

    # Box 3: AI Chatbots
    left2_3 = left2_2 + col_w2 + gap2
    add_card(slide2, left2_3, top2, col_w2, h2, COLOR_SURFACE, COLOR_BORDER)
    top_strip3 = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left2_3), Inches(top2), Inches(col_w2), Inches(0.1))
    top_strip3.fill.solid()
    top_strip3.fill.fore_color.rgb = COLOR_ROSE_DEEP
    top_strip3.line.fill.background()
    
    tx2_3 = slide2.shapes.add_textbox(Inches(left2_3 + 0.25), Inches(top2 + 0.3), Inches(col_w2 - 0.5), Inches(3.8))
    tf2_3 = tx2_3.text_frame
    tf2_3.word_wrap = True
    p = tf2_3.paragraphs[0]
    p.text = "03 · UNGROUNDED AI CHATBOTS"
    p.font.name = FONT_BODY
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_ROSE_DEEP
    p = tf2_3.add_paragraph()
    p.text = "Fluent Language, Hallucinated Chains"
    p.font.name = FONT_DISPLAY
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_INK_PRIMARY
    p = tf2_3.add_paragraph()
    p.text = "\n• Modern LLMs sound authoritative in Arabic, but fabricate hadith texts.\n• Invent plausible-sounding companions and transmission chains.\n• Attribute rulings to scholars who never made them.\n• Cannot be cited or trusted for serious academic research."
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_INK_BODY

    add_speaker_note(slide2, "Every serious researcher in this room knows the exhaustion of modern hadith research. If you search Maktaba Shamela, you get 50 hits with zero relational links. If you look at a consumer website, the grading is flattened to a single word like 'Sahih', hiding the debate between al-Albani and Shu'ayb al-Arna'ut. And if you ask modern AI, it will happily invent a Sahabi that never existed. We call this the Digital Hadith Trilemma.")

    # --------------------------------------------------------------------------
    # SLIDE 03: THE BASIC IDEA
    # --------------------------------------------------------------------------
    slide3 = create_base_slide(prs, "The Architectural Solution",
                               "What if hadith research could be explored as a connected system?",
                               "Transforming isolated texts into an interconnected, queryable knowledge network",
                               "Mīzān Relational Graph Architecture · data/hadith-kg.db", 3)
    
    add_card(slide3, 0.8, 2.1, 11.733, 4.4, COLOR_SURFACE, COLOR_BORDER)
    
    # 2 Column Comparison: Left = Flat text, Right = Connected graph
    tx3_l = slide3.shapes.add_textbox(Inches(1.2), Inches(2.4), Inches(4.8), Inches(3.8))
    tf3_l = tx3_l.text_frame
    tf3_l.word_wrap = True
    p = tf3_l.paragraphs[0]
    p.text = "THE OLD APPROACH"
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_ROSE_DEEP
    p = tf3_l.add_paragraph()
    p.text = "Hadith as an Isolated Text Paragraph"
    p.font.name = FONT_DISPLAY
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_INK_PRIMARY
    p = tf3_l.add_paragraph()
    p.text = "\nIn conventional databases, a hadith is stored as a flat string of Arabic letters. The names of narrators, their generation, their teachers, the book edition number, the textual variants, and the classical commentary are all trapped inside unstructured paragraphs.\n\nSearching finds words, but the computer understands nothing about who taught whom or how the text evolved."
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_INK_BODY

    # Middle Arrow
    tx3_arr = slide3.shapes.add_textbox(Inches(6.2), Inches(3.6), Inches(0.9), Inches(0.8))
    p_arr = tx3_arr.text_frame.paragraphs[0]
    p_arr.alignment = PP_ALIGN.CENTER
    p_arr.text = "➔"
    p_arr.font.size = Pt(28)
    p_arr.font.bold = True
    p_arr.font.color.rgb = COLOR_GOLD_PRIMARY

    # Right Column: The Connected Graph
    tx3_r = slide3.shapes.add_textbox(Inches(7.2), Inches(2.4), Inches(4.9), Inches(3.8))
    tf3_r = tx3_r.text_frame
    tf3_r.word_wrap = True
    p = tf3_r.paragraphs[0]
    p.text = "THE MĪZĀN APPROACH"
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD_PRIMARY
    p = tf3_r.add_paragraph()
    p.text = "Hadith as a Relational Network"
    p.font.name = FONT_DISPLAY
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_INK_PRIMARY
    
    chain_items = [
        "Hadith Core Text ➔ Unique Canonical Identity",
        "Narrators (Rijāl) ➔ Verified Biographical Profiles",
        "Isnād Transmission ➔ Directed Teacher-Student Edges",
        "Concordance ➔ Crosswalk across 18 International Editions",
        "Scholarly Grades ➔ 9 Independent Critical Evaluations",
        "Classical Shurūḥ ➔ Relational Multi-Hadith Commentaries"
    ]
    p = tf3_r.add_paragraph()
    p.text = "\nMīzān breaks down the hadith into its natural historical entities:"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_INK_BODY
    
    for item in chain_items:
        p_item = tf3_r.add_paragraph()
        p_item.text = f"• {item}"
        p_item.font.name = FONT_BODY
        p_item.font.size = Pt(10)
        p_item.font.color.rgb = COLOR_EMERALD_DARK
        
    add_speaker_note(slide3, "Mīzān solves this trilemma through structured relational modeling. A hadith is not a paragraph of text. A hadith is a composite historical artifact: it contains a sequence of verified historical transmitters, a textual matn with variant witnesses, a network of reception events across geography, multiple concordancing numbers across international printings, multiple scholarly assessments across centuries, and extensive classical commentary. Mīzān models every one of these as a queryable relational entity.")

    # --------------------------------------------------------------------------
    # SLIDE 04: WHAT MĪZĀN ACTUALLY IS
    # --------------------------------------------------------------------------
    slide4 = create_base_slide(prs, "Platform Overview",
                               "Mīzān is more than a hadith search box.",
                               "An integrated workbench designed for historical and textual research",
                               "Mīzān Core Application Modules", 4)
    
    c_w4 = 5.6
    c_h4 = 1.95
    row1_t = 2.1
    row2_t = 4.35
    col1_l = 0.8
    col2_l = 6.933
    
    # Card 1: Multi-Edition Concordance
    add_card(slide4, col1_l, row1_t, c_w4, c_h4, COLOR_SURFACE, COLOR_BORDER)
    tx4_1 = slide4.shapes.add_textbox(Inches(col1_l + 0.25), Inches(row1_t + 0.2), Inches(c_w4 - 0.5), Inches(c_h4 - 0.3))
    tf4_1 = tx4_1.text_frame
    tf4_1.word_wrap = True
    p = tf4_1.paragraphs[0]
    p.text = "1. Multi-Edition Concordance"
    p.font.name = FONT_DISPLAY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD_PRIMARY
    p = tf4_1.add_paragraph()
    p.text = "Look up a hadith by any standard printing number (Darussalam, Fu'ad 'Abd al-Baqi, Shamela, or Bulaq volume/page) and resolve to the exact canonical text immediately."
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_INK_BODY

    # Card 2: Multi-Scholar Grading Matrix
    add_card(slide4, col2_l, row1_t, c_w4, c_h4, COLOR_SURFACE, COLOR_BORDER)
    tx4_2 = slide4.shapes.add_textbox(Inches(col2_l + 0.25), Inches(row1_t + 0.2), Inches(c_w4 - 0.5), Inches(c_h4 - 0.3))
    tf4_2 = tx4_2.text_frame
    tf4_2.word_wrap = True
    p = tf4_2.paragraphs[0]
    p.text = "2. Multi-Scholar Grading Matrix"
    p.font.name = FONT_DISPLAY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD_PRIMARY
    p = tf4_2.add_paragraph()
    p.text = "Compare evaluations from 9 major critics side by side with specific citations, distinguishing between chain verdicts ('Sahih al-Isnad') and overall textual status."
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_INK_BODY

    # Card 3: 5-View Isnād Suite
    add_card(slide4, col1_l, row2_t, c_w4, c_h4, COLOR_SURFACE, COLOR_BORDER)
    tx4_3 = slide4.shapes.add_textbox(Inches(col1_l + 0.25), Inches(row2_t + 0.2), Inches(c_w4 - 0.5), Inches(c_h4 - 0.3))
    tf4_3 = tx4_3.text_frame
    tf4_3.word_wrap = True
    p = tf4_3.paragraphs[0]
    p.text = "3. 5-View Isnād & Rijāl Suite"
    p.font.name = FONT_DISPLAY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD_PRIMARY
    p = tf4_3.add_paragraph()
    p.text = "Examine transmission through generational timelines, common link (Madār) networks, geographical maps, and interactive narrator biographical profiles."
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_INK_BODY

    # Card 4: Grounded AI & Classical Commentary
    add_card(slide4, col2_l, row2_t, c_w4, c_h4, COLOR_SURFACE, COLOR_BORDER)
    tx4_4 = slide4.shapes.add_textbox(Inches(col2_l + 0.25), Inches(row2_t + 0.2), Inches(c_w4 - 0.5), Inches(c_h4 - 0.3))
    tf4_4 = tx4_4.text_frame
    tf4_4.word_wrap = True
    p = tf4_4.paragraphs[0]
    p.text = "4. Grounded AI & Classical Shurūḥ"
    p.font.name = FONT_DISPLAY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD_PRIMARY
    p = tf4_4.add_paragraph()
    p.text = "Read classical commentaries relationally mapped across narrations, and ask research questions using an AI assistant that synthesizes strictly from verified SQLite evidence."
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_INK_BODY

    add_speaker_note(slide4, "Mīzān is designed as a scholarly workbench. It is not just a search bar that returns ten results. A researcher can look up a hadith by any number, view its transmission graph across five visual angles, compare phrase-level variants, read Ibn Hajar's commentary, and inspect every scholar's authentic judgment.")

    # --------------------------------------------------------------------------
    # SLIDE 05: THE DATA FOUNDATION
    # --------------------------------------------------------------------------
    slide5 = create_base_slide(prs, "Data Scale",
                               "Built on a large interconnected data layer",
                               "Full-census verified scope across canonical collections and classical sources",
                               "Mīzān Phase 18 Master Global Census Reconciliation", 5)
    
    # 6 Major Stat Cards
    stat_cards = [
        ("715,790", "Canonical Hadiths", "43,493 in the Six Books; 715k across 425 collections"),
        ("49,844", "Disambiguated Narrators", "Unique biographical profiles with Jarḥ wa Ta'dīl rulings"),
        ("4,414,211", "Transmission Links", "Explicit teacher-student relationships across 577,024 asānīd"),
        ("65,420", "Scholarly Evaluations", "Independent gradings across 9 classical and modern critics"),
        ("127,863", "Biographical Statements", "Classical Jarḥ wa Ta'dīl evaluations from 1,015 critics"),
        ("95,598", "Concordance Rows", "Cross-references across 18 international numbering schemes")
    ]
    
    col_w5 = 3.65
    row_h5 = 1.95
    for idx, (val, title, desc) in enumerate(stat_cards):
        r = idx // 3
        c = idx % 3
        cx = 0.8 + c * (col_w5 + 0.38)
        cy = 2.1 + r * (row_h5 + 0.35)
        
        add_card(slide5, cx, cy, col_w5, row_h5, COLOR_SURFACE, COLOR_BORDER)
        tx5 = slide5.shapes.add_textbox(Inches(cx + 0.2), Inches(cy + 0.2), Inches(col_w5 - 0.4), Inches(row_h5 - 0.3))
        tf5 = tx5.text_frame
        tf5.word_wrap = True
        
        p = tf5.paragraphs[0]
        p.text = val
        p.font.name = FONT_DISPLAY
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = COLOR_EMERALD_PRIMARY
        
        p = tf5.add_paragraph()
        p.text = title
        p.font.name = FONT_DISPLAY
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_INK_PRIMARY
        
        p = tf5.add_paragraph()
        p.text = desc
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_INK_MUTED

    add_speaker_note(slide5, "To understand what has been built, look at this census. This is not a concept—it is fully ingested, normalized, and relationally linked today. We have cataloged over 715,000 hadith records, nearly 50,000 unique historical transmitters, over 4.4 million transmission links, and 127,000 classical biographical rulings. Everything you see here is stored locally, queryable in milliseconds, and cryptographically verified.")

    # --------------------------------------------------------------------------
    # SLIDE 06: MULTIPLE EDITIONS & NUMBERING
    # --------------------------------------------------------------------------
    slide6 = create_base_slide(prs, "Concordance Systems",
                               "One hadith can have different numbers.",
                               "Edition number ≠ Canonical identity: Solving the concordance crisis in plain English",
                               "Phase 04 Multi-Edition Numbering Audit Report · data/hadith_numbering.db", 6)
    
    add_card(slide6, 0.8, 2.1, 11.733, 4.4, COLOR_SURFACE, COLOR_BORDER)
    
    tx6 = slide6.shapes.add_textbox(Inches(1.2), Inches(2.35), Inches(10.9), Inches(3.9))
    tf6 = tx6.text_frame
    tf6.word_wrap = True
    
    p = tf6.paragraphs[0]
    p.text = "THE PROBLEM IN PRACTICE"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD_PRIMARY
    
    p = tf6.add_paragraph()
    p.text = "Case Study: The Famous Sunan Ibn Mājah #1986 Shift"
    p.font.name = FONT_DISPLAY
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_INK_PRIMARY
    
    # 2 contrasting cards inside
    add_card(slide6, 1.2, 3.2, 5.2, 1.8, COLOR_ROSE_SOFT, COLOR_BORDER)
    tx6_a = slide6.shapes.add_textbox(Inches(1.4), Inches(3.3), Inches(4.8), Inches(1.5))
    tf6_a = tx6_a.text_frame
    tf6_a.word_wrap = True
    p = tf6_a.paragraphs[0]
    p.text = "DARUSSALAM PRINTED EDITION #1986"
    p.font.name = FONT_BODY
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_ROSE_DEEP
    p = tf6_a.add_paragraph()
    p.text = "Topic: Marriage & Divorce (Nikāḥ)"
    p.font.name = FONT_DISPLAY
    p.font.size = Pt(12)
    p.font.bold = True
    p = tf6_a.add_paragraph()
    p.text = "Refers to a narration regarding the waiting period ('Iddah). Citing #1986 in modern English literature leads here."
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_INK_BODY
    
    add_card(slide6, 6.7, 3.2, 5.2, 1.8, COLOR_AMBER_SOFT, COLOR_BORDER)
    tx6_b = slide6.shapes.add_textbox(Inches(6.9), Inches(3.3), Inches(4.8), Inches(1.5))
    tf6_b = tx6_b.text_frame
    tf6_b.word_wrap = True
    p = tf6_b.paragraphs[0]
    p.text = "SHAMELA ARABIC DIGITAL SEQUENCE #1986"
    p.font.name = FONT_BODY
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER_DEEP
    p = tf6_b.add_paragraph()
    p.text = "Topic: Commercial Transactions (Tijārah)"
    p.font.name = FONT_DISPLAY
    p.font.size = Pt(12)
    p.font.bold = True
    p = tf6_b.add_paragraph()
    p.text = "Refers to an entirely different narration on business contracts due to an 82-hadith chapter offset."
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_INK_BODY
    
    # Solution banner at bottom
    add_card(slide6, 1.2, 5.25, 10.7, 0.95, COLOR_EMERALD_SOFT, COLOR_EMERALD_PRIMARY)
    tx6_sol = slide6.shapes.add_textbox(Inches(1.4), Inches(5.35), Inches(10.3), Inches(0.75))
    tf6_sol = tx6_sol.text_frame
    tf6_sol.word_wrap = True
    p = tf6_sol.paragraphs[0]
    p.text = "MĪZĀN'S RESOLUTION: 95,598 BIDIRECTIONAL COORDINATES"
    p.font.name = FONT_BODY
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD_DEEP
    p = tf6_sol.add_paragraph()
    p.text = "Mīzān crosswalks every number across 18 schemes. Looking up Darussalam #1986 or Shamela #1986 instantly resolves to the exact canonical text with 100% bidirectional precision (verified in Phase 04)."
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_INK_BODY
    
    add_speaker_note(slide6, "Here is a concrete research problem Mīzān solves every day. If a student reads a hadith in an English book published by Darussalam citing #1986, and then searches for #1986 in an Arabic software like Shamela, they get a completely different hadith about divorce instead of commerce. Mīzān has built a mathematical crosswalk across 95,000 coordinates. Query any number in any major edition, and Mīzān resolves it to the correct canonical hadith instantly.")

    # --------------------------------------------------------------------------
    # SLIDE 07: MULTI-SCHOLAR EVALUATION
    # --------------------------------------------------------------------------
    slide7 = create_base_slide(prs, "Scholarly Provenance",
                               "Scholars do not always express a judgment in the same way.",
                               "Preserving the rich vocabulary of hadith criticism instead of flattening it into 'Sahih/Da'if'",
                               "Phase 13 Master Forensic Audit Report · Domain D & E", 7)
    
    add_card(slide7, 0.8, 2.1, 11.733, 4.4, COLOR_SURFACE, COLOR_BORDER)
    
    tx7 = slide7.shapes.add_textbox(Inches(1.2), Inches(2.35), Inches(10.9), Inches(0.8))
    p = tx7.text_frame.paragraphs[0]
    p.text = "EXEMPLAR: JĀMIʿ AL-TIRMIDHĪ HADITH #2897"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD_PRIMARY
    p = tx7.text_frame.add_paragraph()
    p.text = "Three Respected Scholars · Three Distinct Analytical Judgments"
    p.font.name = FONT_DISPLAY
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_INK_PRIMARY
    
    scholars = [
        ("Shaykh Muḥammad Nāṣir al-Dīn al-Albānī", "Ṣaḥīḥ (Authentic)", "Ṣaḥīḥ Sunan al-Tirmidhī #2897", COLOR_EMERALD_SOFT, COLOR_EMERALD_DEEP),
        ("Ḥāfiẓ Zubayr ʿAlī Zaʾī", "Ḥasan li-Ghayrihī (Sound through corroboration)", "Anwār al-Ṣaḥīfah, p. 142 · Darussalam #2954", COLOR_AMBER_SOFT, COLOR_AMBER_DEEP),
        ("Shaykh Shuʿayb al-Arnāʾūṭ", "Ḍaʿīf al-Isnād wa-Ṣaḥīḥ bi-Shawāhidih (Chain weak, text verified)", "Taḥqīq al-Musnad #14201", COLOR_BLUE_SOFT, COLOR_BLUE_DEEP)
    ]
    
    for i, (sch_name, sch_grade, sch_ref, bg_col, text_col) in enumerate(scholars):
        sy = 3.25 + i * 0.95
        add_card(slide7, 1.2, sy, 10.7, 0.8, COLOR_SURFACE_WARM, COLOR_BORDER)
        
        # Scholar Name
        tx_sn = slide7.shapes.add_textbox(Inches(1.4), Inches(sy + 0.15), Inches(4.5), Inches(0.5))
        p_sn = tx_sn.text_frame.paragraphs[0]
        p_sn.text = sch_name
        p_sn.font.name = FONT_DISPLAY
        p_sn.font.size = Pt(12)
        p_sn.font.bold = True
        p_sn.font.color.rgb = COLOR_INK_PRIMARY
        p_ref = tx_sn.text_frame.add_paragraph()
        p_ref.text = sch_ref
        p_ref.font.name = FONT_BODY
        p_ref.font.size = Pt(8.5)
        p_ref.font.color.rgb = COLOR_INK_MUTED
        
        # Grade Pill
        add_card(slide7, 7.8, sy + 0.18, 3.9, 0.45, bg_col, text_col)
        tx_gr = slide7.shapes.add_textbox(Inches(7.8), Inches(sy + 0.22), Inches(3.9), Inches(0.4))
        p_gr = tx_gr.text_frame.paragraphs[0]
        p_gr.alignment = PP_ALIGN.CENTER
        p_gr.text = sch_grade
        p_gr.font.name = FONT_BODY
        p_gr.font.size = Pt(9.5)
        p_gr.font.bold = True
        p_gr.font.color.rgb = text_col

    # Bottom summary tag
    tx7_bot = slide7.shapes.add_textbox(Inches(1.2), Inches(6.15), Inches(10.9), Inches(0.3))
    p_bot = tx7_bot.text_frame.paragraphs[0]
    p_bot.text = "In Mīzān, scholarly disagreement is treated as valuable historical data rather than an error to be erased."
    p_bot.font.name = FONT_DISPLAY
    p_bot.font.size = Pt(10.5)
    p_bot.font.italic = True
    p_bot.font.color.rgb = COLOR_INK_BODY

    add_speaker_note(slide7, "In hadith criticism, context is everything. An isnād may be weak while the matn is authentic due to corroborating paths. Consumer platforms destroy this nuance by stamping a single word: 'Sahih'. Mīzān preserves the full technical judgment: distinguishing between 'Sahih al-Isnad' and 'Sahih', and showing the exact opinions of 9 different classical and contemporary critics with their specific edition page citations.")

    # --------------------------------------------------------------------------
    # SLIDE 08: THE ZERO-GUESS PRINCIPLE
    # --------------------------------------------------------------------------
    slide8 = create_base_slide(prs, "Forensic Integrity",
                               "When the evidence is unclear, Mīzān does not guess.",
                               "The Phase 14 Quarantine Discovery: Coverage is never more important than accuracy",
                               "Phase 14 & Phase 18 Master Reports · validation/phase_18/", 8)
    
    # 2 Big Cards: Left = Quarantine Story, Right = Zero-Trust Result
    add_card(slide8, 0.8, 2.1, 5.7, 4.4, COLOR_SURFACE, COLOR_ROSE_DEEP)
    tx8_l = slide8.shapes.add_textbox(Inches(1.1), Inches(2.35), Inches(5.1), Inches(3.9))
    tf8_l = tx8_l.text_frame
    tf8_l.word_wrap = True
    p = tf8_l.paragraphs[0]
    p.text = "PHASE 14 FORENSIC ADJUDICATION"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_ROSE_DEEP
    p = tf8_l.add_paragraph()
    p.text = "The 286 Zubayr Quarantined Records"
    p.font.name = FONT_DISPLAY
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_INK_PRIMARY
    p = tf8_l.add_paragraph()
    p.text = "\n• During our audit of 18,375 grading records by Shaykh Zubayr ʿAlī Zaʾī in the Sunan collections, 287 records were flagged.\n• They existed in Arabic digital sequences, but lacked standalone numbered entries in the printed Darussalam edition.\n• 1 record was successfully corroborated with printed crosswalk proof.\n• 286 records lacked explicit standalone citations.\n\nMīzān refused to approximate or guess numbers. All 286 were sealed in quarantine."
    p.font.name = FONT_BODY
    p.font.size = Pt(10.5)
    p.font.color.rgb = COLOR_INK_BODY

    add_card(slide8, 6.833, 2.1, 5.7, 4.4, COLOR_EMERALD_DARK, COLOR_EMERALD_PRIMARY)
    tx8_r = slide8.shapes.add_textbox(Inches(7.133), Inches(2.35), Inches(5.1), Inches(3.9))
    tf8_r = tx8_r.text_frame
    tf8_r.word_wrap = True
    p = tf8_r.paragraphs[0]
    p.text = "PHASE 18 PRODUCTION GATE"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD_LIGHT
    p = tf8_r.add_paragraph()
    p.text = "QUARANTINE_ESCAPE_COUNT = 0"
    p.font.name = FONT_DISPLAY
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p = tf8_r.add_paragraph()
    p.text = "\nIn Phase 18, every public endpoint, search index, and AI retrieval route was tested against adversarial queries attempting to leak quarantined data.\n\n• Certified Zubayr Records: 18,089 (Live)\n• Quarantined Zubayr Records: 286 (Sealed)\n• Leaks or False Citations: 0 (PASSED)\n\n'We would rather show no grade than a guessed grade.'"
    p.font.name = FONT_BODY
    p.font.size = Pt(10.5)
    p.font.color.rgb = COLOR_BG

    add_speaker_note(slide8, "This is the most critical slide for any scholar or funder. How do you know our data is trustworthy? Because we adhere to the Zero-Guess Rule: Evidence > Coverage. In Phase 14, when we audited 287 records of Shaykh Zubayr Ali Zai that lacked explicit standalone printed citations in Darussalam, we did not approximate them. We quarantined all 286 records with machine-enforced gates so they can never output false data to users. We would rather show no grade than a guessed grade.")

    # --------------------------------------------------------------------------
    # SLIDE 09: ISNĀD VISUALIZATION
    # --------------------------------------------------------------------------
    slide9 = create_base_slide(prs, "Isnād Analysis",
                               "From a chain of names to a transmission network.",
                               "Visualizing transmission lines, generational strata, and common link scholars",
                               "05_ISNAD_VISUALIZATION_SPEC.md · 4.4M Transmission Links", 9)
    
    add_card(slide9, 0.8, 2.1, 11.733, 4.4, COLOR_SURFACE, COLOR_BORDER)
    
    views = [
        ("1. Network View", "Directed multigraph showing teacher-student links and Common Links (Madār al-Isnād)."),
        ("2. Timeline View", "Generational strata (Tabaqāt) from the Prophet ﷺ through Companions to Compilers with death badges."),
        ("3. Regional Map", "Geographical clustering showing transmission centers across the Islamic world."),
        ("4. Transmission Atlas", "Spatio-temporal arcs tracing the physical movement of hadith across centuries."),
        ("5. 3D Volumetric", "Interactive 3D spatial projection of complex multi-branch transmission networks.")
    ]
    
    vw_w = 2.15
    for i, (v_name, v_desc) in enumerate(views):
        vx = 1.0 + i * (vw_w + 0.2)
        add_card(slide9, vx, 2.4, vw_w, 2.5, COLOR_SURFACE_WARM, COLOR_BORDER)
        tx_v = slide9.shapes.add_textbox(Inches(vx + 0.15), Inches(2.55), Inches(vw_w - 0.3), Inches(2.2))
        tf_v = tx_v.text_frame
        tf_v.word_wrap = True
        p = tf_v.paragraphs[0]
        p.text = v_name
        p.font.name = FONT_DISPLAY
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_EMERALD_PRIMARY
        p = tf_v.add_paragraph()
        p.text = f"\n{v_desc}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_INK_BODY

    # Lower drawer notice
    add_card(slide9, 1.0, 5.15, 11.333, 1.05, COLOR_EMERALD_SOFT, COLOR_EMERALD_PRIMARY)
    tx9_dr = slide9.shapes.add_textbox(Inches(1.2), Inches(5.25), Inches(10.9), Inches(0.85))
    tf9_dr = tx9_dr.text_frame
    tf9_dr.word_wrap = True
    p = tf9_dr.paragraphs[0]
    p.text = "INTEGRATED RIJĀL RESEARCH DRAWER"
    p.font.name = FONT_BODY
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD_DEEP
    p = tf9_dr.add_paragraph()
    p.text = "Clicking any narrator node opens their biographical dossier: verified birth/death years (AH), verified teachers and students, and classical Jarḥ wa Ta'dīl rulings from Yahya ibn Ma'in, al-Bukhari, and Ahmad ibn Hanbal. Transmitters with unrecorded death years are placed on an 'Undated' shelf—we never fabricate dates."
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_INK_BODY

    add_speaker_note(slide9, "Here is Mīzān in action. When a researcher looks at a chain of 7 narrators, reading text names on a page makes it nearly impossible to see where chains converge. Mīzān's Isnād Suite plots the chain across generational strata. You can immediately see the common link—the Madār—click on any transmitter, and pull up their complete classical evaluation from Yahya ibn Ma'in, al-Bukhari, and Ahmad ibn Hanbal.")

    # --------------------------------------------------------------------------
    # SLIDE 10: GEOGRAPHY & TRANSMISSION
    # --------------------------------------------------------------------------
    slide10 = create_base_slide(prs, "Geographical Transmission",
                                "Where did this transmission travel?",
                                "Mapping the physical journeys of hadith scholars across 12 historical centers",
                                "07_ISNAD_GEOGRAPHY_SPEC.md & 08_ISNAD_ATLAS_SPEC.md", 10)
    
    add_card(slide10, 0.8, 2.1, 11.733, 4.4, COLOR_SURFACE, COLOR_BORDER)
    
    # Left Box: Historical Centers
    add_card(slide10, 1.2, 2.4, 6.0, 3.8, COLOR_EMERALD_DARK, COLOR_EMERALD_PRIMARY)
    tx10_l = slide10.shapes.add_textbox(Inches(1.4), Inches(2.55), Inches(5.6), Inches(3.5))
    tf10_l = tx10_l.text_frame
    tf10_l.word_wrap = True
    p = tf10_l.paragraphs[0]
    p.text = "12 VERIFIED HISTORICAL CENTERS"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD_LIGHT
    p = tf10_l.add_paragraph()
    p.text = "Tracing the Movement of Scholars"
    p.font.name = FONT_DISPLAY
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    
    cities = [
        "Madīnah (المدينة)", "Makkah (مكة)", "al-Kūfah (الكوفة)", "al-Baṣrah (البصرة)",
        "Dimashq (دمشق)", "al-Fusṭāṭ (الفسطاط)", "Baghdād (بغداد)", "Naysābūr (نيسابور)",
        "al-Rayy (الري)", "Bukhārā (بخارى)", "Ṣanʿāʾ (صنعاء)", "Qurṭubah (قرطبة)"
    ]
    p = tf10_l.add_paragraph()
    p.text = f"\nCenters Mapped in geoData.ts:\n{', '.join(cities[:6])},\n{', '.join(cities[6:])}."
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_BG
    
    p = tf10_l.add_paragraph()
    p.text = "\nSpatio-Temporal Flow Arcs trace narrations from the Prophet ﷺ and Companions in the Hijaz through regional legal centers in Iraq, out to compilers in Khurasan."
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_GOLD_LIGHT

    # Right Box: Academic Responsibility
    add_card(slide10, 7.5, 2.4, 4.6, 3.8, COLOR_SURFACE_WARM, COLOR_BORDER)
    tx10_r = slide10.shapes.add_textbox(Inches(7.7), Inches(2.55), Inches(4.2), Inches(3.5))
    tf10_r = tx10_r.text_frame
    tf10_r.word_wrap = True
    p = tf10_r.paragraphs[0]
    p.text = "ACADEMIC RESPONSIBILITY"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD_PRIMARY
    p = tf10_r.add_paragraph()
    p.text = "Zero-Speculation Rule"
    p.font.name = FONT_DISPLAY
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_INK_PRIMARY
    p = tf10_r.add_paragraph()
    p.text = "\n• We only draw an arc between two cities when primary biographical dictionaries confirm that the student physically received the narration from that teacher in that location.\n• We do NOT invent speculative travel paths.\n• Where exact dates or cities are uncertain, they are marked explicitly as approximate.\n• Scholars can filter by metropolitan center to see all active transmitters in that city."
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_INK_BODY

    add_speaker_note(slide10, "Hadith transmission was not just textual; it was geographical. Scholars traveled thousands of miles on foot—al-Riḥlah fī Ṭalab al-Ḥadīth. Mīzān's Spatio-Temporal Atlas maps these transmission arcs across real historical coordinates. You can watch a narration originate in Madinah, transmit through the jurists of Kufah, and get recorded by Abu Dawud in Sijistan. And we adhere to zero speculation: we only draw a geographical arc if the primary biographical record documents an authentic student-teacher meeting.")

    # --------------------------------------------------------------------------
    # SLIDE 11: MATN COMPARISON
    # --------------------------------------------------------------------------
    slide11 = create_base_slide(prs, "Textual Criticism",
                                "Compare the wording — not just the translation.",
                                "Phrase-level textual analysis across parallel narrations of the same hadith",
                                "10_MATN_VISUALIZATION_SPEC.md · MatnDiffViewer.tsx", 11)
    
    add_card(slide11, 0.8, 2.1, 11.733, 4.4, COLOR_SURFACE, COLOR_BORDER)
    
    # Text Comparison Display
    tx11 = slide11.shapes.add_textbox(Inches(1.2), Inches(2.35), Inches(10.9), Inches(0.8))
    p = tx11.text_frame.paragraphs[0]
    p.text = "CASE STUDY: THE HADITH OF INTENTIONS (إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ)"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD_PRIMARY
    p = tx11.text_frame.add_paragraph()
    p.text = "Ṣaḥīḥ al-Bukhārī #1 vs. Ṣaḥīḥ Muslim #1907"
    p.font.name = FONT_DISPLAY
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_INK_PRIMARY
    
    # 2 Parallel Boxes
    add_card(slide11, 1.2, 3.25, 10.7, 1.15, COLOR_SURFACE_WARM, COLOR_BORDER)
    tx11_b = slide11.shapes.add_textbox(Inches(1.4), Inches(3.35), Inches(10.3), Inches(0.95))
    tf11_b = tx11_b.text_frame
    tf11_b.word_wrap = True
    p = tf11_b.paragraphs[0]
    p.text = "WITNESS A: ṢAḤĪḤ AL-BUKHĀRĪ #1"
    p.font.name = FONT_BODY
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD_PRIMARY
    p = tf11_b.add_paragraph()
    p.text = "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ ، وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى ، فَمَنْ كَانَتْ هِجْرَتُهُ إِلَى دُنْيَا يُصِيبُهَا ، أَوْ إِلَى امْرَأَةٍ يَنْكِحُهَا..."
    p.font.name = "Amiri"
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_INK_PRIMARY

    add_card(slide11, 1.2, 4.55, 10.7, 1.15, COLOR_SURFACE_WARM, COLOR_BORDER)
    tx11_m = slide11.shapes.add_textbox(Inches(1.4), Inches(4.65), Inches(10.3), Inches(0.95))
    tf11_m = tx11_m.text_frame
    tf11_m.word_wrap = True
    p = tf11_m.paragraphs[0]
    p.text = "WITNESS B: ṢAḤĪḤ MUSLIM #1907"
    p.font.name = FONT_BODY
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE_DEEP
    p = tf11_m.add_paragraph()
    p.text = "إِنَّمَا الأَعْمَالُ بِالنِّيَّةِ ، وَإِنَّمَا لِامْرِئٍ مَا نَوَى ، فَمَنْ كَانَتْ هِجْرَتُهُ إِلَى اللَّهِ وَرَسُولِهِ فَهِجْرَتُهُ إِلَى اللَّهِ وَرَسُولِهِ..."
    p.font.name = "Amiri"
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_INK_PRIMARY

    # Legend at bottom
    add_card(slide11, 1.2, 5.85, 10.7, 0.5, COLOR_GOLD_SOFT, COLOR_BORDER)
    tx11_leg = slide11.shapes.add_textbox(Inches(1.4), Inches(5.9), Inches(10.3), Inches(0.4))
    p_leg = tx11_leg.text_frame.paragraphs[0]
    p_leg.text = "Legend:  ● Emerald = Verbatim Shared Phrase   ● Amber = Lexical Variant (بِالنِّيَّاتِ vs بِالنِّيَّةِ)   ● Purple = Addition / Ziyādah"
    p_leg.font.name = FONT_BODY
    p_leg.font.size = Pt(9.5)
    p_leg.font.bold = True
    p_leg.font.color.rgb = COLOR_GOLD_DARK

    add_speaker_note(slide11, "For textual scholars, this is one of our most exciting tools. In ʿIlm al-Ḥadīth, comparing the exact wording of variants is essential to identify Ziyādāt al-Thiqāt—additions by trustworthy narrators. Mīzān's Matn Diff Viewer aligns parallel texts token-by-token. Words shared verbatim glow in emerald; variant synonyms appear in amber; additions appear in purple. What previously took hours with multiple printed volumes open on a desk is now visible in three seconds.")

    # --------------------------------------------------------------------------
    # SLIDE 12: COMMENTARY
    # --------------------------------------------------------------------------
    slide12 = create_base_slide(prs, "Relational Commentaries",
                                "Connect the hadith to its scholarly commentary.",
                                "Classical commentary is relational, not a simple one-to-one attachment",
                                "Phase 12 Relational Commentary Schema Migration Report", 12)
    
    add_card(slide12, 0.8, 2.1, 11.733, 4.4, COLOR_SURFACE, COLOR_BORDER)
    
    # Left: The Classical Reality
    add_card(slide12, 1.2, 2.4, 5.2, 3.8, COLOR_SURFACE_WARM, COLOR_BORDER)
    tx12_l = slide12.shapes.add_textbox(Inches(1.4), Inches(2.55), Inches(4.8), Inches(3.5))
    tf12_l = tx12_l.text_frame
    tf12_l.word_wrap = True
    p = tf12_l.paragraphs[0]
    p.text = "THE CLASSICAL REALITY"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_ROSE_DEEP
    p = tf12_l.add_paragraph()
    p.text = "Multi-Hadith Authorial Scope"
    p.font.name = FONT_DISPLAY
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_INK_PRIMARY
    p = tf12_l.add_paragraph()
    p.text = "\nClassical authors did not write in neat single-hadith boxes. An imam like al-Mubārakfūrī (Tuḥfat al-Aḥwadhī) often wrote a single comprehensive legal discussion that covers two or three consecutive hadiths simultaneously.\n\nA simple database design that forces one commentary record to attach to only one hadith ID fails completely."
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_INK_BODY

    # Right: Phase 12 Solution
    add_card(slide12, 6.7, 2.4, 5.2, 3.8, COLOR_EMERALD_SOFT, COLOR_EMERALD_PRIMARY)
    tx12_r = slide12.shapes.add_textbox(Inches(6.9), Inches(2.55), Inches(4.8), Inches(3.5))
    tf12_r = tx12_r.text_frame
    tf12_r.word_wrap = True
    p = tf12_r.paragraphs[0]
    p.text = "PHASE 12 JUNCTION ARCHITECTURE"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD_DEEP
    p = tf12_r.add_paragraph()
    p.text = "Case Study: Record #428"
    p.font.name = FONT_DISPLAY
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD_DEEP
    p = tf12_r.add_paragraph()
    p.text = "\nTuḥfat al-Aḥwadhī on Beard-Combing in Ablution (Bāb Takhlīl al-Liḥyah):\n\n• Hadith 12427 (Tirmidhī #29): Linked as PRIMARY\n• Hadith 12428 (Tirmidhī #30): Linked as SECONDARY\n• Hadith 12426 (Tirmidhī #28): 0 false links (Zero leakage)\n\n1,202 commentary texts across 8 classical works linked through 1,203 verified junction links."
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_INK_BODY

    add_speaker_note(slide12, "Classical commentators did not write in simple single-hadith paragraphs. In Tuḥfat al-Aḥwadhī, al-Mubarakfuri frequently writes a single master juristic commentary that analyzes two or three consecutive hadiths together. Legacy databases fail here because their schema forces a single hadith ID. Mīzān engineered an atomic junction architecture that relationally links commentary passages across multiple hadiths, preserving primary and secondary scopes without data duplication.")

    # --------------------------------------------------------------------------
    # SLIDE 13: RAG / ASK MĪZĀN
    # --------------------------------------------------------------------------
    slide13 = create_base_slide(prs, "Responsible Artificial Intelligence",
                                "AI that starts with evidence.",
                                "Using AI as an interface over verified data — not as an unguided oracle",
                                "validation/phase_18/21_rag_grounding_audit.json & deterministic.py", 13)
    
    add_card(slide13, 0.8, 2.1, 11.733, 4.4, COLOR_SURFACE, COLOR_BORDER)
    
    # 5-Step Pipeline
    steps13 = [
        ("Step 1: User Question", "The researcher asks a question in plain natural language (e.g. 'What did Ibn Hajar say about Yahya ibn Sa'id?')."),
        ("Step 2: Database Retrieval", "Mīzān retrieves matching authentic records from local SQLite databases using exact and semantic indexes."),
        ("Step 3: Evidence Pack", "An immutable JSON Evidence Pack is assembled containing only verified hadith texts, narrator IDs, and citations."),
        ("Step 4: Verification Gate", "If evidence is insufficient, the system fails closed and refuses to generate an ungrounded answer."),
        ("Step 5: Grounded Answer", "The model synthesizes an academic response strictly from the evidence pack, providing clickable citation links.")
    ]
    
    sw = 2.15
    for i, (st_title, st_desc) in enumerate(steps13):
        sx = 1.0 + i * (sw + 0.2)
        add_card(slide13, sx, 2.5, sw, 2.7, COLOR_SURFACE_WARM, COLOR_BORDER)
        tx_s = slide13.shapes.add_textbox(Inches(sx + 0.15), Inches(2.65), Inches(sw - 0.3), Inches(2.4))
        tf_s = tx_s.text_frame
        tf_s.word_wrap = True
        p = tf_s.paragraphs[0]
        p.text = st_title
        p.font.name = FONT_DISPLAY
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_EMERALD_PRIMARY
        p = tf_s.add_paragraph()
        p.text = f"\n{st_desc}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_INK_BODY

    # Offline Fallback Guarantee
    add_card(slide13, 1.0, 5.35, 11.333, 0.9, COLOR_GOLD_SOFT, COLOR_GOLD_BORDER)
    tx13_fb = slide13.shapes.add_textbox(Inches(1.2), Inches(5.45), Inches(10.9), Inches(0.7))
    tf13_fb = tx13_fb.text_frame
    tf13_fb.word_wrap = True
    p = tf13_fb.paragraphs[0]
    p.text = "OFFLINE DETERMINISTIC SYNTHESIS"
    p.font.name = FONT_BODY
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD_DARK
    p = tf13_fb.add_paragraph()
    p.text = "Mīzān includes a DeterministicSynthesizerProvider that formats evidence packs into rigorous academic citations even when no internet connection or external LLM API is available."
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_INK_BODY

    add_speaker_note(slide13, "Everyone wants to use AI in Islamic studies, but general-purpose LLMs are dangerous because they hallucinate hadiths with complete confidence. Mīzān takes a zero-trust approach with 'Ask Mīzān'. Our model does not answer from training memory. When you ask a question, our backend first queries our certified databases, packs the exact historical evidence into an immutable payload, and only allows the model to synthesize that verified text. If the evidence does not exist in the database, it fails closed and refuses to speculate.")

    # --------------------------------------------------------------------------
    # SLIDE 14: TRUST & FORENSIC VALIDATION
    # --------------------------------------------------------------------------
    slide14 = create_base_slide(prs, "Quality & Audit Program",
                                "How do we know the system is reliable?",
                                "18 phases of systematic testing to prove data integrity and academic credibility",
                                "Mīzān Master Validation & Audit Program (Phase 1 through Phase 18)", 14)
    
    add_card(slide14, 0.8, 2.1, 11.733, 4.4, COLOR_SURFACE, COLOR_BORDER)
    
    pillars14 = [
        ("Database Immutability", "All 4 canonical databases were verified byte-for-byte against pre-audit SHA-256 hashes. Zero accidental mutations occurred across all 18 phases."),
        ("No Orphan References", "Full relational scans verified zero broken links between 715k hadiths, 49k narrators, 4.4M chain links, and 65k grades."),
        ("Adversarial Testing", "The system was tested against known boundary cases, numbering shift zones in Ibn Majah, and homonym father-son narrator collisions."),
        ("Quarantine Enforcement", "Uncertain or unmapped records were segregated into quarantine rather than forced into production to inflate statistics.")
    ]
    
    col_w14 = 5.3
    row_h14 = 1.7
    for i, (p_title, p_desc) in enumerate(pillars14):
        r = i // 2
        c = i % 2
        px = 1.2 + c * (col_w14 + 0.5)
        py = 2.45 + r * (row_h14 + 0.3)
        
        add_card(slide14, px, py, col_w14, row_h14, COLOR_SURFACE_WARM, COLOR_BORDER)
        tx_p = slide14.shapes.add_textbox(Inches(px + 0.2), Inches(py + 0.15), Inches(col_w14 - 0.4), Inches(row_h14 - 0.3))
        tf_p = tx_p.text_frame
        tf_p.word_wrap = True
        p = tf_p.paragraphs[0]
        p.text = p_title
        p.font.name = FONT_DISPLAY
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_EMERALD_PRIMARY
        p = tf_p.add_paragraph()
        p.text = f"\n{p_desc}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_INK_BODY

    add_speaker_note(slide14, "For scholars and funders, audit evidence is paramount. We did not simply write code; we executed an 18-phase forensic audit program. We verified that our core database hashes never changed, that no orphan references exist, and that ambiguous cases like the 286 Zubayr records were quarantined rather than guessed. Academic integrity requires provable data.")

    # --------------------------------------------------------------------------
    # SLIDE 15: ZERO-TRUST RESULT
    # --------------------------------------------------------------------------
    slide15 = create_base_slide(prs, "Release Certification",
                                "The system was tested as if it could fail.",
                                "Phase 18 Final Release Certification results across 5.96+ million entities",
                                "validation/phase_18/01_phase18_master_report.md", 15)
    
    add_card(slide15, 0.8, 2.1, 11.733, 4.4, COLOR_EMERALD_DARK, COLOR_EMERALD_PRIMARY)
    
    # 3 big stat blocks on dark background
    z_stats = [
        ("35 / 35", "Machine Acceptance Gates Passed", "100% pass across hash integrity, scholar isolation, and retrieval"),
        ("5.96M+", "Entities & Relationships Audited", "Comprehensive census across 27 databases and components"),
        ("0", "Quarantine Escapes & Critical Findings", "Zero data leakage, zero unauthorized mutations, verdict: GO")
    ]
    
    zw = 3.6
    for i, (z_val, z_title, z_desc) in enumerate(z_stats):
        zx = 1.1 + i * (zw + 0.4)
        add_card(slide15, zx, 2.5, zw, 2.2, COLOR_EMERALD_DEEP, COLOR_EMERALD_LIGHT)
        tx_z = slide15.shapes.add_textbox(Inches(zx + 0.15), Inches(2.65), Inches(zw - 0.3), Inches(1.9))
        tf_z = tx_z.text_frame
        tf_z.word_wrap = True
        p = tf_z.paragraphs[0]
        p.text = z_val
        p.font.name = FONT_DISPLAY
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = COLOR_GOLD_LIGHT
        p = tf_z.add_paragraph()
        p.text = z_title
        p.font.name = FONT_DISPLAY
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p = tf_z.add_paragraph()
        p.text = f"\n{z_desc}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_BG

    # Bottom certification banner
    add_card(slide15, 1.1, 4.95, 11.133, 1.25, COLOR_EMERALD_PRIMARY, COLOR_GOLD_LIGHT)
    tx15_b = slide15.shapes.add_textbox(Inches(1.3), Inches(5.05), Inches(10.7), Inches(1.05))
    tf15_b = tx15_b.text_frame
    tf15_b.word_wrap = True
    p = tf15_b.paragraphs[0]
    p.text = "OFFICIAL AUDIT VERDICT: GO"
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD_LIGHT
    p = tf15_b.add_paragraph()
    p.text = "Phase 18 Zero-Trust certification completed with 100% pass across all 35 machine acceptance gates. Zero quarantine escapes, zero canonical database mutations, zero production drift, and absolute scholarly integrity verified across all 5.26+ million entities and relationships."
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = RGBColor(255, 255, 255)

    add_speaker_note(slide15, "In Phase 18, we subjected the complete ecosystem to 35 machine acceptance gates. We tested against SQL injection, parameter tampering, cache poisoning, and RAG hallucination forcing. The result was a 100% pass rate with zero findings across 5.96 million records. The verdict is GO.")

    # --------------------------------------------------------------------------
    # SLIDE 16: WHAT HAS ALREADY BEEN BUILT
    # --------------------------------------------------------------------------
    slide16 = create_base_slide(prs, "Operational Platform",
                                "This is not just a concept.",
                                "A functional research platform ready for academic use",
                                "Mīzān Core Operational Modules", 16)
    
    add_card(slide16, 0.8, 2.1, 11.733, 4.4, COLOR_SURFACE, COLOR_BORDER)
    
    modules16 = [
        ("Multi-Edition Search", "Arabic root search, diacritic-tolerant search, and English translation FTS5 index."),
        ("Hadith Detail View", "High-contrast Arabic matn, parallel English translation, and multi-edition concordance bar."),
        ("Scholar Grading Matrix", "Side-by-side display of 9 scholars with edition footnotes and isnād vs matn nuance."),
        ("5-View Isnād Suite", "Interactive multigraphs, generational strata timelines, map clusters, and 3D volumetric view."),
        ("Classical Commentary", "Integrated classical sharḥ (Fatḥ al-Bārī, Nawawī, Tuḥfat al-Aḥwadhī) with junction linking."),
        ("Matn Diff Viewer", "Phrase-level variant highlighting comparing verbatim matches, synonyms, and additions."),
        ("Narrator Rijāl Profiles", "49k biographical cards with classical evaluations from Yahya ibn Ma'in and Ahmad ibn Hanbal."),
        ("Grounded Ask Mīzān", "Conversational AI assistant bounded strictly by verified SQLite evidence packs.")
    ]
    
    mw = 2.65
    mh = 1.8
    for idx, (m_title, m_desc) in enumerate(modules16):
        r = idx // 4
        c = idx % 4
        mx = 1.0 + c * (mw + 0.22)
        my = 2.35 + r * (mh + 0.25)
        
        add_card(slide16, mx, my, mw, mh, COLOR_SURFACE_WARM, COLOR_BORDER)
        tx_m = slide16.shapes.add_textbox(Inches(mx + 0.15), Inches(my + 0.15), Inches(mw - 0.3), Inches(mh - 0.3))
        tf_m = tx_m.text_frame
        tf_m.word_wrap = True
        p = tf_m.paragraphs[0]
        p.text = m_title
        p.font.name = FONT_DISPLAY
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_EMERALD_PRIMARY
        p = tf_m.add_paragraph()
        p.text = f"\n{m_desc}"
        p.font.name = FONT_BODY
        p.font.size = Pt(8.5)
        p.font.color.rgb = COLOR_INK_BODY

    add_speaker_note(slide16, "We want to be very clear: this is not a mock-up. Every feature shown here exists in the codebase today. You can search in Arabic or English, navigate generational timelines, compare textual variants, read Ibn Hajar's commentary, and inspect scholar grades.")

    # --------------------------------------------------------------------------
    # SLIDE 17: WHAT IS STILL GROWING
    # --------------------------------------------------------------------------
    slide17 = create_base_slide(prs, "Current vs. Next",
                                "Mīzān is already usable — but the work is not finished.",
                                "Clear and honest boundaries between current certified scope and planned expansion",
                                "Mīzān Strategic Planning & Phase II Specification", 17)
    
    add_card(slide17, 0.8, 2.1, 11.733, 4.4, COLOR_SURFACE, COLOR_BORDER)
    
    # Left: What is live
    add_card(slide17, 1.2, 2.4, 5.2, 3.8, COLOR_EMERALD_SOFT, COLOR_EMERALD_PRIMARY)
    tx17_l = slide17.shapes.add_textbox(Inches(1.4), Inches(2.55), Inches(4.8), Inches(3.5))
    tf17_l = tx17_l.text_frame
    tf17_l.word_wrap = True
    p = tf17_l.paragraphs[0]
    p.text = "CURRENT CERTIFIED BASELINE"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD_DEEP
    p = tf17_l.add_paragraph()
    p.text = "What Is Fully Operational Today"
    p.font.name = FONT_DISPLAY
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD_DEEP
    p = tf17_l.add_paragraph()
    p.text = "\n• The core Six Books (Kutub al-Sittah) fully parsed into the relational graph.\n• 715,790 hadith texts across 425 collections.\n• 95,598 multi-edition concordance crosswalks.\n• 1,202 verified commentary records across 8 works.\n• 65,420 multi-scholar grading evaluations.\n• 18-phase forensic release certification complete."
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_INK_BODY

    # Right: What is next
    add_card(slide17, 6.7, 2.4, 5.2, 3.8, COLOR_GOLD_SOFT, COLOR_GOLD_BORDER)
    tx17_r = slide17.shapes.add_textbox(Inches(6.9), Inches(2.55), Inches(4.8), Inches(3.5))
    tf17_r = tx17_r.text_frame
    tf17_r.word_wrap = True
    p = tf17_r.paragraphs[0]
    p.text = "NEXT STAGES (PLANNED EXPANSION)"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD_DARK
    p = tf17_r.add_paragraph()
    p.text = "What Institutional Support Accelerates"
    p.font.name = FONT_DISPLAY
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD_DARK
    p = tf17_r.add_paragraph()
    p.text = "\n• Parsing Musnad Aḥmad (27,000+ hadiths) and al-Muwaṭṭaʾ of Imam Mālik into the transmission graph.\n• Expanding commentary coverage from pilot chapters to complete multi-volume works.\n• Automated algorithmic detection of Common Link (Madār) scholars.\n• Direct integration with high-resolution manuscript scans from historical library archives."
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_INK_BODY

    add_speaker_note(slide17, "We are completely transparent about our scope. The core Six Books, 715k hadiths, and 1,202 classical commentary records are certified and live. But hadith scholarship is vast. With academic collaboration and sponsorship, we plan to parse Musnad Ahmad, expand commentary coverage to full multi-volume works, and link directly to manuscript scans.")

    # --------------------------------------------------------------------------
    # SLIDE 18: THE LONG-TERM VISION
    # --------------------------------------------------------------------------
    slide18 = create_base_slide(prs, "Strategic Roadmap",
                                "From a database to a research infrastructure.",
                                "Building a permanent, open digital humanities foundation for Islamic Studies",
                                "Mīzān Institutional Vision", 18)
    
    add_card(slide18, 0.8, 2.1, 11.733, 4.4, COLOR_SURFACE, COLOR_BORDER)
    
    # 3-Phase Horizon Columns
    h_cols = [
        ("PHASE I · CERTIFIED CORE", "Completed & Live", "• 715k Hadiths & 425 collections\n• Kutub al-Sittah parsed knowledge graph\n• 5-view isnād suite & Matn Diff\n• Multi-edition crosswalk (95k rows)\n• 18-phase forensic certification", COLOR_EMERALD_SOFT, COLOR_EMERALD_DEEP),
        ("PHASE II · PLANNED EXPANSION", "Next 12–18 Months", "• Parsing Musnad Ahmad (27k+ hadiths)\n• Ingesting al-Muwatta' & Sunan al-Darimi\n• High-res manuscript viewer integration\n• Automated Common Link detector\n• Expansion to 10 complete commentaries", COLOR_AMBER_SOFT, COLOR_AMBER_DEEP),
        ("PHASE III · GLOBAL INFRASTRUCTURE", "Long-Term Academic Vision", "• Institutional Open REST/GraphQL API\n• University curriculum integration\n• Collaborative scholarly annotation layer\n• Print-to-digital manuscript OCR alignment\n• Global digital preservation network", COLOR_BLUE_SOFT, COLOR_BLUE_DEEP)
    ]
    
    hw = 3.6
    for i, (h_tag, h_status, h_text, bg_c, border_c) in enumerate(h_cols):
        hx = 1.0 + i * (hw + 0.38)
        add_card(slide18, hx, 2.4, hw, 3.8, COLOR_SURFACE_WARM, COLOR_BORDER)
        
        # Header strip
        h_strip = slide18.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(hx), Inches(2.4), Inches(hw), Inches(0.1))
        h_strip.fill.solid()
        h_strip.fill.fore_color.rgb = border_c
        h_strip.line.fill.background()
        
        tx_h = slide18.shapes.add_textbox(Inches(hx + 0.15), Inches(2.6), Inches(hw - 0.3), Inches(3.4))
        tf_h = tx_h.text_frame
        tf_h.word_wrap = True
        p = tf_h.paragraphs[0]
        p.text = h_tag
        p.font.name = FONT_BODY
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = border_c
        p = tf_h.add_paragraph()
        p.text = h_status
        p.font.name = FONT_DISPLAY
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_INK_PRIMARY
        p = tf_h.add_paragraph()
        p.text = f"\n{h_text}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_INK_BODY

    add_speaker_note(slide18, "Our goal is not simply to build an application, but to establish an enduring scholarly infrastructure. In Phase I, we proved the relational model works and scales. In Phase II, we expand into broader early corpora like Musnad Ahmad. In Phase III, Mīzān becomes an open institutional API that universities and research centers can build on.")

    # --------------------------------------------------------------------------
    # SLIDE 19: WHY THIS MATTERS
    # --------------------------------------------------------------------------
    slide19 = create_base_slide(prs, "Academic Value",
                                "Why could this matter for Islamic Studies?",
                                "Empowering researchers with modern digital humanities instruments while preserving tradition",
                                "Reflections on Academic Impact in Digital Humanities", 19)
    
    add_card(slide19, 0.8, 2.1, 11.733, 4.4, COLOR_SURFACE, COLOR_BORDER)
    
    impacts = [
        ("Saves Months of Manual Collation", "Resolves numbering discrepancies across international editions in seconds, eliminating citation confusion."),
        ("Restores Intellectual Complexity", "Replaces oversimplified binary labels ('Sahih/Da'if') with the actual, nuanced debates of classical critics."),
        ("Reveals Hidden Transmission Networks", "Visualizes common links, regional geographical movements, and generational strata that are invisible in raw text."),
        ("Accelerates Textual Criticism (Naqd al-Matn)", "Highlights verbatim phrasing, synonymous variants, and textual additions (*Ziyādāt*) token-by-token."),
        ("Provides a Safe AI Research Environment", "Guarantees that AI-assisted research answers are strictly bounded by verified, cited database evidence."),
        ("Bridges Islamic Scholarship & Computer Science", "Sets a global benchmark for how digital humanities can be executed with methodological reverence.")
    ]
    
    iw = 5.3
    ih = 1.15
    for idx, (i_title, i_desc) in enumerate(impacts):
        r = idx // 2
        c = idx % 2
        ix = 1.2 + c * (iw + 0.5)
        iy = 2.45 + r * (ih + 0.2)
        
        add_card(slide19, ix, iy, iw, ih, COLOR_SURFACE_WARM, COLOR_BORDER)
        tx_i = slide19.shapes.add_textbox(Inches(ix + 0.2), Inches(iy + 0.12), Inches(iw - 0.4), Inches(ih - 0.24))
        tf_i = tx_i.text_frame
        tf_i.word_wrap = True
        p = tf_i.paragraphs[0]
        p.text = i_title
        p.font.name = FONT_DISPLAY
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_EMERALD_PRIMARY
        p = tf_i.add_paragraph()
        p.text = i_desc
        p.font.name = FONT_BODY
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_INK_BODY

    add_speaker_note(slide19, "Why does this matter? Because for decades, researchers have had to manually reconcile conflicting numbers and trace chains by hand on note cards. Mīzān gives researchers an instrument of magnification: it does not replace the scholar's judgment, but it makes the underlying evidence immediately visible, searchable, and verified.")

    # --------------------------------------------------------------------------
    # SLIDE 20: CLOSING / INVITATION
    # --------------------------------------------------------------------------
    slide20 = prs.slides.add_slide(prs.slide_layouts[6])
    bg20 = slide20.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(SLIDE_WIDTH), Inches(SLIDE_HEIGHT))
    bg20.fill.solid()
    bg20.fill.fore_color.rgb = COLOR_BG
    bg20.line.fill.background()
    
    # Pill Tag
    add_card(slide20, 4.4, 0.9, 4.5, 0.45, COLOR_GOLD_SOFT, COLOR_GOLD_BORDER)
    tx_pill20 = slide20.shapes.add_textbox(Inches(4.4), Inches(0.95), Inches(4.5), Inches(0.35))
    p_pill20 = tx_pill20.text_frame.paragraphs[0]
    p_pill20.alignment = PP_ALIGN.CENTER
    p_pill20.text = "COLLABORATION & PARTNERSHIP"
    p_pill20.font.name = FONT_BODY
    p_pill20.font.size = Pt(9.5)
    p_pill20.font.bold = True
    p_pill20.font.color.rgb = COLOR_GOLD_DARK
    
    # Arabic Calligraphy / Quranic Ayah
    tx_ar20 = slide20.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.333), Inches(0.8))
    p_ar20 = tx_ar20.text_frame.paragraphs[0]
    p_ar20.alignment = PP_ALIGN.CENTER
    p_ar20.text = "وَقُلْ رَبِّ زِدْنِي عِلْمًا"
    p_ar20.font.name = "Amiri"
    p_ar20.font.size = Pt(32)
    p_ar20.font.bold = True
    p_ar20.font.color.rgb = COLOR_GOLD_PRIMARY
    
    # Title
    tx_t20 = slide20.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(11.333), Inches(0.8))
    p_t20 = tx_t20.text_frame.paragraphs[0]
    p_t20.alignment = PP_ALIGN.CENTER
    p_t20.text = "Let's build the next stage together."
    p_t20.font.name = FONT_DISPLAY
    p_t20.font.size = Pt(32)
    p_t20.font.bold = True
    p_t20.font.color.rgb = COLOR_EMERALD_DEEP
    
    # Core Motto
    tx_motto = slide20.shapes.add_textbox(Inches(2.0), Inches(3.2), Inches(9.333), Inches(0.8))
    p_mot = tx_motto.text_frame.paragraphs[0]
    p_mot.alignment = PP_ALIGN.CENTER
    p_mot.text = "Preserving the evidence. Connecting the scholarship.\nMaking hadith research easier to explore."
    p_mot.font.name = FONT_DISPLAY
    p_mot.font.size = Pt(14)
    p_mot.font.italic = True
    p_mot.font.color.rgb = COLOR_INK_BODY
    
    # 2 Cards: Current Status vs. Next Opportunity
    add_card(slide20, 2.0, 4.2, 4.4, 1.8, COLOR_SURFACE, COLOR_BORDER)
    tx20_l = slide20.shapes.add_textbox(Inches(2.2), Inches(4.35), Inches(4.0), Inches(1.5))
    tf20_l = tx20_l.text_frame
    tf20_l.word_wrap = True
    p = tf20_l.paragraphs[0]
    p.text = "CURRENT STATUS"
    p.font.name = FONT_BODY
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD_PRIMARY
    p = tf20_l.add_paragraph()
    p.text = "Built, Tested, and Certified"
    p.font.name = FONT_DISPLAY
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_INK_PRIMARY
    p = tf20_l.add_paragraph()
    p.text = "\nCore relational engine operational across 715k hadiths, 49k narrators, and 4.4M transmission links with 18-phase zero-trust certification."
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_INK_BODY

    add_card(slide20, 6.9, 4.2, 4.4, 1.8, COLOR_SURFACE, COLOR_BORDER)
    tx20_r = slide20.shapes.add_textbox(Inches(7.1), Inches(4.35), Inches(4.0), Inches(1.5))
    tf20_r = tx20_r.text_frame
    tf20_r.word_wrap = True
    p = tf20_r.paragraphs[0]
    p.text = "THE NEXT STAGE"
    p.font.name = FONT_BODY
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD_DARK
    p = tf20_r.add_paragraph()
    p.text = "Academic Collaboration"
    p.font.name = FONT_DISPLAY
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_INK_PRIMARY
    p = tf20_r.add_paragraph()
    p.text = "\nPartnering with university scholars to expand into Musnad Ahmad, integrate manuscript archives, and establish an endowed research workbench."
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_INK_BODY

    # Contact & Discussion line
    tx_dis = slide20.shapes.add_textbox(Inches(1.0), Inches(6.3), Inches(11.333), Inches(0.4))
    p_dis = tx_dis.text_frame.paragraphs[0]
    p_dis.alignment = PP_ALIGN.CENTER
    p_dis.text = "We welcome your thoughts, guidance, and collaboration."
    p_dis.font.name = FONT_DISPLAY
    p_dis.font.size = Pt(12)
    p_dis.font.italic = True
    p_dis.font.color.rgb = COLOR_GOLD_DARK
    
    add_speaker_note(slide20, "Professor Syed, colleagues, and supporters: Mīzān al-Ḥadīth was built to serve researchers like you. We have proved that computational digital humanities can be executed with absolute fidelity to classical Islamic scholarship. But to realize its full potential—to make this the permanent research workbench for students and scholars worldwide—requires institutional partnership and sustained philanthropic support. We invite you to join us in establishing Mīzān as an open, enduring foundation for Islamic studies.")

    # Save PPTX
    pptx_path = os.path.abspath("Mizan_al_Hadith_Introduction_Presentation.pptx")
    prs.save(pptx_path)
    print(f"PowerPoint Presentation successfully generated: {pptx_path}")
    return pptx_path

if __name__ == "__main__":
    build_presentation()
