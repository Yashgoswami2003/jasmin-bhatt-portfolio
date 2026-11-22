import os
import re
import shutil
from datetime import datetime

HTML_FILES = [
    "index.html",
    "about.html",
    "works.html",
    "literature-stories.html",
    "media-gallery.html",
    "contact.html",
]

MARKER_START = "/* === AUTO-MOBILE-IMAGE-FIX-START === */"
MARKER_END = "/* === AUTO-MOBILE-IMAGE-FIX-END === */"

GLOBAL_FIX_CSS = f"""
{MARKER_START}
html, body {{
  max-width: 100%;
  overflow-x: hidden;
  -webkit-text-size-adjust: 100%;
}}

*, *::before, *::after {{
  box-sizing: border-box;
  min-width: 0;
}}

img, picture, svg, video, iframe {{
  display: block;
  max-width: 100%;
}}

/* Portrait: clean top-focused framing across mobile & desktop */
img[src*="assets/media/portrait/"] {{
  width: 100%;
  height: auto;
  max-height: 460px;
  object-fit: cover !important;
  object-position: center top !important;
  border-radius: 0.75rem;
}}

/* Book covers: full cover visible with zero extra vertical gap */
img[src*="assets/media/books/"] {{
  width: auto !important;
  height: auto !important;
  max-width: 100% !important;
  max-height: 380px;
  margin-left: auto !important;
  margin-right: auto !important;
  object-fit: contain !important;
  object-position: center !important;
  border-radius: 0.65rem;
}}

/* Cinema / theatre posters & stills: full poster visible without extra empty box gap */
img[src*="assets/media/cinema-theatre/"] {{
  width: auto !important;
  height: auto !important;
  max-width: 100% !important;
  max-height: 300px;
  margin-left: auto !important;
  margin-right: auto !important;
  object-fit: contain !important;
  object-position: center !important;
  border-radius: 0.65rem;
}}

/* Gallery slots: clean fit without excessive empty space */
img[src*="assets/media/gallery/"] {{
  width: auto !important;
  height: auto !important;
  max-width: 100% !important;
  max-height: 280px;
  margin-left: auto !important;
  margin-right: auto !important;
  object-fit: contain !important;
  object-position: center !important;
  border-radius: 0.65rem;
}}

/* Collapse oversized aspect-ratio wrappers when holding full-fit media */
div:has(> img[src*="assets/media/books/"]),
div:has(> img[src*="assets/media/cinema-theatre/"]),
div:has(> img[src*="assets/media/gallery/"]) {{
  aspect-ratio: auto !important;
  height: auto !important;
  min-height: 0 !important;
  padding: 0.5rem !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}}

@media (max-width: 767px) {{
  h1 {{
    font-size: clamp(1.9rem, 8vw, 2.55rem) !important;
    line-height: 1.12 !important;
    word-break: break-word;
  }}

  h2 {{
    font-size: clamp(1.55rem, 6.4vw, 2.1rem) !important;
    line-height: 1.16 !important;
    word-break: break-word;
  }}

  h3 {{
    word-break: break-word;
  }}

  a, button {{
    min-height: 40px;
  }}

  img[src*="assets/media/books/"] {{
    max-height: 340px;
  }}

  img[src*="assets/media/cinema-theatre/"] {{
    max-height: 250px;
  }}

  img[src*="assets/media/portrait/"] {{
    max-height: 360px;
  }}
}}
{MARKER_END}
"""


def backup_files():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join("_backup_html", stamp)
    os.makedirs(backup_dir, exist_ok=True)
    for fname in HTML_FILES:
        if os.path.exists(fname):
            shutil.copy2(fname, os.path.join(backup_dir, fname))
    print(f"[Backup] Saved original HTML copies to: {backup_dir}")


def patch_html(content: str) -> str:
    content = re.sub(
        r'<meta\s+name="viewport"\s+content="width=device-width,\s*initial-scale=1\.0"\s*/?>',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />',
        content,
        flags=re.IGNORECASE,
    )

    pattern_existing = re.compile(
        re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
        flags=re.DOTALL,
    )
    if pattern_existing.search(content):
        content = pattern_existing.sub(GLOBAL_FIX_CSS.strip(), content)
    elif "</style>" in content:
        content = content.replace("</style>", f"{GLOBAL_FIX_CSS}\n  </style>", 1)
    elif "</head>" in content:
        content = content.replace("</head>", f"  <style>{GLOBAL_FIX_CSS}\n  </style>\n</head>", 1)

    return content


def main():
    backup_files()
    updated_count = 0

    for fname in HTML_FILES:
        if not os.path.exists(fname):
            print(f"[Skip] {fname} not found")
            continue

        with open(fname, "r", encoding="utf-8") as f:
            original = f.read()

        patched = patch_html(original)

        with open(fname, "w", encoding="utf-8") as f:
            f.write(patched)

        updated_count += 1
        print(f"[Updated] {fname}")

    print(f"\nDone! {updated_count} HTML files updated cleanly.")


if __name__ == "__main__":
    main()