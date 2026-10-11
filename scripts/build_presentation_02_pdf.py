"""
Generate MĪZĀN AL-ḤADĪTH Presentation 02 PDF
Renders presentation_02.html into a high-fidelity 16:9 widescreen PDF using Microsoft Edge headless.
"""

import os
import sys
import subprocess
import pypdf

WORKSPACE_DIR = r"c:\Users\taymi\discord-hadith-bot"
HTML_PATH = os.path.join(WORKSPACE_DIR, "presentation_02.html")
PDF_PATH_1 = os.path.join(WORKSPACE_DIR, "Mizan_al_Hadith_Presentation_02_Roadmap_and_Funding.pdf")
PDF_PATH_2 = os.path.join(WORKSPACE_DIR, "presentation_02.pdf")

PRINT_CSS = """
/* ==============================================================================
   PRINT MEDIA RULES — 16:9 WIDESCREEN HIGH FIDELITY SLIDE PDF EXPORT
   ============================================================================== */
@media print {
  @page {
    size: 16in 9in;
    margin: 0;
  }

  *, *::before, *::after {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }

  html, body {
    width: 16in !important;
    height: auto !important;
    min-height: auto !important;
    overflow: visible !important;
    background-color: #050811 !important;
    background: #050811 !important;
    margin: 0 !important;
    padding: 0 !important;
  }

  #canvas-wrap,
  #control-bar,
  #sources-drawer,
  .ambient-nebula,
  .ambient-vignette {
    display: none !important;
  }

  #deck-viewport {
    position: static !important;
    inset: auto !important;
    width: 16in !important;
    height: auto !important;
    display: block !important;
    overflow: visible !important;
  }

  .slide {
    position: relative !important;
    inset: auto !important;
    width: 16in !important;
    height: 9in !important;
    max-height: 9in !important;
    min-height: 9in !important;
    box-sizing: border-box !important;
    padding: 38px 56px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: flex-start !important;
    opacity: 1 !important;
    visibility: visible !important;
    transform: none !important;
    pointer-events: auto !important;
    overflow: hidden !important;
    page-break-after: always !important;
    break-after: page !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
    background: #050811 !important;
  }

  .slide:last-child,
  .slide:last-of-type,
  #slide-22 {
    page-break-after: avoid !important;
    break-after: avoid !important;
  }
}
"""

def inject_print_css_if_needed():
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    if "@media print" not in content:
        # Inject right before </style>
        idx = content.find("</style>")
        if idx != -1:
            new_content = content[:idx] + "\n" + PRINT_CSS + "\n" + content[idx:]
            with open(HTML_PATH, "w", encoding="utf-8") as f:
                f.write(new_content)
            print("Successfully injected @media print rules into presentation_02.html")
        else:
            print("Could not find </style> tag in presentation_02.html")
    else:
        print("@media print already present in presentation_02.html")

def find_edge():
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

def render_pdf():
    edge_exe = find_edge()
    if not edge_exe:
        raise RuntimeError("Microsoft Edge not found on this system.")

    html_url = f"file:///{HTML_PATH.replace(os.sep, '/')}"
    
    cmd = [
        edge_exe,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
        f"--print-to-pdf={PDF_PATH_1}",
        html_url
    ]

    print(f"Executing: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Edge exited with error code {res.returncode}: {res.stderr}")

    if not os.path.exists(PDF_PATH_1):
        raise RuntimeError(f"PDF was not generated at {PDF_PATH_1}")

    # Copy to presentation_02.pdf as well
    with open(PDF_PATH_1, "rb") as src, open(PDF_PATH_2, "wb") as dst:
        dst.write(src.read())

    size_mb = os.path.getsize(PDF_PATH_1) / (1024 * 1024)
    print(f"PDF Successfully Created: {PDF_PATH_1} ({size_mb:.2f} MB)")
    print(f"Also mirrored to: {PDF_PATH_2}")

    # Verify with pypdf
    reader = pypdf.PdfReader(PDF_PATH_1)
    num_pages = len(reader.pages)
    print(f"Total Pages in PDF: {num_pages}")
    for i, page in enumerate(reader.pages):
        box = page.mediabox
        print(f"  Page {i+1:02d}: width = {box.width} pt ({float(box.width)/72:.2f} in), height = {box.height} pt ({float(box.height)/72:.2f} in)")

if __name__ == "__main__":
    inject_print_css_if_needed()
    render_pdf()
