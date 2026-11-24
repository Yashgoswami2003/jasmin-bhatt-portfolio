from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent
SKIP_DIRS = {"_backup_html", ".git", "node_modules", "__pycache__"}

IMAGE_URL = "https://jasmin-bhatt-portfolio.yr676742.workers.dev/assets/media/portrait/jasmin-bhatt-profile.jpeg"
IMAGE_ALT = "Jasmin Bhatt — Writer, Director, Actor, Poet, Author &amp; Tax Consultant"

OG_BLOCK = f"""  <meta property="og:image" content="{IMAGE_URL}" />
  <meta property="og:image:secure_url" content="{IMAGE_URL}" />
  <meta property="og:image:alt" content="{IMAGE_ALT}" />
  <meta name="twitter:image" content="{IMAGE_URL}" />
  <meta name="twitter:image:alt" content="{IMAGE_ALT}" />"""


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def update_html_file(html_path: Path) -> bool:
    content = html_path.read_text(encoding="utf-8")

    # Remove existing og:image / twitter:image tags if present to avoid duplicates
    cleaned = re.sub(
        r'\s*<meta\s+(?:property="og:image(?::[^"]*)?"|name="twitter:image(?::[^"]*)?")\s+[^>]*>\s*',
        "\n",
        content,
        flags=re.IGNORECASE,
    )

    if re.search(r'<meta\s+name="twitter:description"[^>]*>', cleaned, flags=re.IGNORECASE):
        updated = re.sub(
            r'(<meta\s+name="twitter:description"[^>]*>)',
            rf"\1\n{OG_BLOCK}",
            cleaned,
            count=1,
            flags=re.IGNORECASE,
        )
    elif re.search(r'<meta\s+property="og:description"[^>]*>', cleaned, flags=re.IGNORECASE):
        updated = re.sub(
            r'(<meta\s+property="og:description"[^>]*>)',
            rf"\1\n{OG_BLOCK}",
            cleaned,
            count=1,
            flags=re.IGNORECASE,
        )
    elif re.search(r"</head>", cleaned, flags=re.IGNORECASE):
        updated = re.sub(
            r"(</head>)",
            rf"{OG_BLOCK}\n\1",
            cleaned,
            count=1,
            flags=re.IGNORECASE,
        )
    else:
        return False

    if updated != content:
        html_path.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> None:
    html_files = [p for p in BASE_DIR.rglob("*.html") if not should_skip(p)]
    updated_count = 0

    for file_path in sorted(html_files):
        if update_html_file(file_path):
            updated_count += 1
            print(f"[Updated] {file_path.relative_to(BASE_DIR)}")
        else:
            print(f"[Unchanged] {file_path.relative_to(BASE_DIR)}")

    print(f"\nDone. {updated_count} HTML file(s) updated.")


if __name__ == "__main__":
    main()