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

# Agar 'New profile pic' ka exact naam + extension pata ho toh yahan likh do;
# khali ("") chhodne par assets/media/portrait/ ke andar 'New profile pic*' automatically dhoondh lega.
NEW_PROFILE_FILENAME = ""

MARKER_START = "/* === AUTO-MOBILE-IMAGE-FIX-START === */"
MARKER_END = "/* === AUTO-MOBILE-IMAGE-FIX-END === */"

GLOBAL_FIX_CSS = f"""
{MARKER_START}
/* Attractive Light Editorial Page + Rich Spotlight Hero + Crisp Cards */
html {{
  overflow-x: hidden;
  -webkit-text-size-adjust: 100%;
}}

body {{
  background-color: #F7F3EA !important;
  background-image:
    radial-gradient(ellipse 85% 45% at 15% 0%, rgba(180, 123, 30, 0.11), transparent 60%),
    radial-gradient(ellipse 70% 40% at 88% 12%, rgba(140, 59, 43, 0.07), transparent 58%),
    linear-gradient(180deg, #FAF7F0 0%, #F4EFE4 55%, #ECE4D3 100%) !important;
  color: #1E293B !important;
  font-family: "Plus Jakarta Sans", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
  background-attachment: fixed;
  overflow-x: clip;
  max-width: 100%;
}}

header.sticky {{
  background-color: rgba(255, 255, 255, 0.97) !important;
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(180, 123, 30, 0.24) !important;
  box-shadow: 0 6px 22px -12px rgba(15, 23, 42, 0.14) !important;
  padding-top: 2px;
}}

/* Rich editorial spotlight on first section of EVERY page while keeping rest of page light */
body > section:first-of-type,
body > section:first-of-type[class*="bg-"] {{
  position: relative;
  background:
    radial-gradient(ellipse 75% 65% at 88% 18%, rgba(224, 168, 62, 0.22), transparent 58%),
    radial-gradient(ellipse 70% 60% at 12% 90%, rgba(140, 59, 43, 0.25), transparent 60%),
    linear-gradient(135deg, #121B2E 0%, #1A2842 52%, #261B25 100%) !important;
  color: #F8FAFC !important;
  border-bottom: 2px solid rgba(224, 168, 62, 0.55) !important;
  box-shadow: 0 24px 55px -20px rgba(15, 23, 42, 0.35) !important;
}}

body > section:first-of-type h1,
body > section:first-of-type h2,
body > section:first-of-type h3,
body > section:first-of-type strong {{
  color: #FFFFFF !important;
}}

body > section:first-of-type p,
body > section:first-of-type li,
body > section:first-of-type span {{
  color: inherit;
}}

body > section:first-of-type .text-slate-950,
body > section:first-of-type .text-slate-900,
body > section:first-of-type .text-slate-800 {{
  color: #FFFFFF !important;
}}

body > section:first-of-type .text-slate-700,
body > section:first-of-type .text-slate-600 {{
  color: rgba(241, 245, 249, 0.90) !important;
}}

body > section:first-of-type .text-slate-500 {{
  color: rgba(226, 232, 240, 0.80) !important;
}}

/* Light cards/pills inside hero stay high-contrast so text is always sharp */
body > section:first-of-type .bg-white,
body > section:first-of-type .bg-ivoryCard,
body > section:first-of-type a.group,
body > section:first-of-type .quick-jump-card {{
  background: linear-gradient(180deg, #FFFFFF 0%, #FFFDF8 100%) !important;
  color: #0F172A !important;
  border: 1px solid rgba(224, 168, 62, 0.45) !important;
  box-shadow: 0 14px 28px -12px rgba(0, 0, 0, 0.30) !important;
}}

body > section:first-of-type .bg-white .text-slate-950,
body > section:first-of-type .bg-white .text-slate-900,
body > section:first-of-type .bg-white .text-slate-800,
body > section:first-of-type .bg-white .font-semibold,
body > section:first-of-type .bg-ivoryCard .text-slate-950,
body > section:first-of-type .bg-ivoryCard .text-slate-900,
body > section:first-of-type .bg-ivoryCard .text-slate-800,
body > section:first-of-type .bg-ivoryCard .font-semibold,
body > section:first-of-type a.group .font-semibold,
body > section:first-of-type .quick-jump-card .font-semibold {{
  color: #0F172A !important;
}}

body > section:first-of-type .bg-white .text-slate-700,
body > section:first-of-type .bg-white .text-slate-600,
body > section:first-of-type .bg-white .text-slate-500,
body > section:first-of-type .bg-ivoryCard .text-slate-700,
body > section:first-of-type .bg-ivoryCard .text-slate-600,
body > section:first-of-type .bg-ivoryCard .text-slate-500,
body > section:first-of-type a.group .text-slate-500,
body > section:first-of-type .quick-jump-card .text-slate-500 {{
  color: #475569 !important;
}}

body > section:not(:first-of-type).bg-white,
body > section:not(:first-of-type).bg-ivory,
body > section:not(:first-of-type).bg-cream {{
  background-color: rgba(255, 254, 250, 0.82) !important;
}}

body > section:not(:first-of-type).bg-obsidian {{
  background-color: transparent !important;
}}

body > section:not(:first-of-type).bg-charcoal {{
  background-color: rgba(239, 232, 218, 0.85) !important;
}}

body > section:not(:first-of-type) article.luxury-card,
body > section:not(:first-of-type) article.award-card,
body > section:not(:first-of-type) figure.gallery-item,
body > section:not(:first-of-type) .stat-pill {{
  background-color: #FFFFFF !important;
  border-color: rgba(180, 123, 30, 0.26) !important;
  box-shadow: 0 14px 34px -14px rgba(15, 23, 42, 0.13), 0 2px 6px rgba(15, 23, 42, 0.04) !important;
}}

footer {{
  background-image:
    radial-gradient(ellipse 80% 60% at 50% 0%, rgba(180, 123, 30, 0.14), transparent 70%),
    linear-gradient(180deg, #EFE8D8 0%, #E3D8C3 100%) !important;
  border-top: 2px solid rgba(180, 123, 30, 0.55) !important;
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
  body {{
    background-attachment: scroll;
  }}

  h1 {{
    font-size: clamp(2rem, 8.2vw, 2.7rem) !important;
    line-height: 1.1 !important;
    letter-spacing: -0.015em;
    word-break: break-word;
  }}

  h2 {{
    font-size: clamp(1.6rem, 6.5vw, 2.2rem) !important;
    line-height: 1.15 !important;
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


def resolve_new_profile_src() -> str | None:
    portrait_dir = os.path.join("assets", "media", "portrait")
    if not os.path.isdir(portrait_dir):
        return None

    if NEW_PROFILE_FILENAME.strip():
        candidate = os.path.join(portrait_dir, NEW_PROFILE_FILENAME.strip())
        if os.path.isfile(candidate):
            return f"assets/media/portrait/{NEW_PROFILE_FILENAME.strip()}"

    # Look for any file starting with 'new profile pic' (case-insensitive)
    for entry in os.listdir(portrait_dir):
        full_path = os.path.join(portrait_dir, entry)
        if not os.path.isfile(full_path):
            continue
        stem, _ = os.path.splitext(entry)
        if stem.strip().lower().startswith("new profile pic") or stem.strip().lower().startswith("new-profile-pic"):
            return f"assets/media/portrait/{entry}"

    return None


def find_existing_media_by_folder(subfolder: str) -> list[str]:
    folder_path = os.path.join("assets", "media", subfolder)
    if not os.path.isdir(folder_path):
        return []
    valid_exts = {".jpg", ".jpeg", ".png", ".webp"}
    files = []
    for entry in sorted(os.listdir(folder_path)):
        full_path = os.path.join(folder_path, entry)
        if os.path.isfile(full_path):
            _, ext = os.path.splitext(entry)
            if ext.lower() in valid_exts:
                files.append(f"assets/media/{subfolder}/{entry}")
    return files


def update_index_profile(content: str) -> str:
    new_src = resolve_new_profile_src()
    if not new_src:
        print("[Info] New profile photo not found in assets/media/portrait/; skipped index image swap.")
        return content

    # Replace portrait image inside index.html (preferring OFFICIAL PORTRAIT / portrait folder match)
    updated, count = re.subn(
        r'(<img\b[^>]*\bsrc=["\'])assets/media/portrait/[^"\']+(["\'][^>]*>)',
        rf"\g<1>{new_src}\g<2>",
        content,
        count=1,
        flags=re.IGNORECASE,
    )
    if count > 0:
        print(f"[Index Portrait] Updated index.html profile image -> {new_src}")
    return updated


def populate_media_gallery_slots(content: str) -> str:
    portraits = find_existing_media_by_folder("portrait")
    books = find_existing_media_by_folder("books")
    cinema = find_existing_media_by_folder("cinema-theatre")
    gallery_existing = find_existing_media_by_folder("gallery")

    # Pick best available images per slot category without breaking missing files
    best_portrait = portraits[0] if portraits else None
    best_book = books[0] if books else None
    best_cinema = cinema[0] if cinema else None
    best_theatre = next((p for p in cinema if "theatre" in p.lower() or "stage" in p.lower()), best_cinema)
    best_poetry = gallery_existing[0] if gallery_existing else best_portrait
    best_awards = gallery_existing[1] if len(gallery_existing) > 1 else (best_book or best_portrait)

    slot_mapping = [
        ("PORTRAIT SLOT", best_portrait, "Jasmin Bhatt Official Portrait"),
        ("BOOKS SLOT", best_book, "Published Book Cover"),
        ("CINEMA & OTT SLOT", best_cinema, "Film & OTT Poster"),
        ("THEATRE SLOT", best_theatre, "Theatre & Stage Production"),
        ("POETRY & EVENTS SLOT", best_poetry, "Poetry & Literary Event"),
        ("CREDENTIALS & AWARDS SLOT", best_awards, "Credentials & Recognition"),
    ]

    for slot_label, img_src, alt_text in slot_mapping:
        if not img_src:
            continue

        # Match a placeholder card/container mentioning slot_label that doesn't already have an <img>
        pattern = re.compile(
            rf'(<div\b[^>]*>(?:(?!<div\b).)*?{re.escape(slot_label)}.*?)(</div>)',
            flags=re.DOTALL | re.IGNORECASE,
        )

        def _inject_img(match):
            block = match.group(1)
            closing = match.group(2)
            if "<img" in block.lower():
                return match.group(0)
            img_tag = (
                f'\n    <div class="w-full flex items-center justify-center p-2">'
                f'<img src="{img_src}" alt="{alt_text}" loading="lazy" />'
                f'</div>\n  '
            )
            return f"{block}{img_tag}{closing}"

        content, replaced = pattern.subn(_inject_img, content, count=1)
        if replaced > 0:
            print(f"[Gallery Slot] Populated '{slot_label}' -> {img_src}")

    return content


def patch_html(content: str, fname: str = "") -> str:
    content = re.sub(
        r'<meta\s+name="viewport"\s+content="width=device-width,\s*initial-scale=1\.0"\s*/?>',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />',
        content,
        flags=re.IGNORECASE,
    )

    if fname.lower() == "index.html":
        content = update_index_profile(content)

    if fname.lower() == "media-gallery.html":
        content = populate_media_gallery_slots(content)

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

        patched = patch_html(original, fname=fname)

        with open(fname, "w", encoding="utf-8") as f:
            f.write(patched)

        updated_count += 1
        print(f"[Updated] {fname}")

    print(f"\nDone! {updated_count} HTML files updated cleanly.")


if __name__ == "__main__":
    main()