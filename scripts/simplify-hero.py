#!/usr/bin/env python3
"""Remove repository listings from generated Terminal hero SVG assets."""

from pathlib import Path
import re
import sys

FLAGSHIPS_MARKER = '<g class="ln" style="animation-delay:650ms">'
PRIMARY_COLOR_PATTERN = re.compile(r'<tspan fill="(#[0-9A-Fa-f]{6})" font-weight="700">\$')


def simplify_hero(path: Path) -> None:
    content = path.read_text(encoding="utf-8")

    if content.count(FLAGSHIPS_MARKER) != 1:
        raise RuntimeError(f"Expected one generated flagships section in {path}")

    primary_match = PRIMARY_COLOR_PATTERN.search(content)
    if primary_match is None:
        raise RuntimeError(f"Primary prompt color was not found in {path}")

    prefix = content.split(FLAGSHIPS_MARKER, maxsplit=1)[0]
    primary = primary_match.group(1)
    prompt = (
        f'<g class="ln" style="animation-delay:650ms">'
        f'<text x="46" y="206" font-size="13" fill="{primary}" font-weight="700">$</text>'
        f'<rect class="cur" x="61" y="194" width="8" height="15" fill="{primary}"/></g>'
    )
    updated = prefix + prompt + "\n    </svg>\n"
    replacements = {
        'height="360" viewBox="0 0 1200 360"': 'height="270" viewBox="0 0 1200 270"',
        '<rect width="1200" height="360"': '<rect width="1200" height="270"',
        'width="1172" height="332"': 'width="1172" height="242"',
    }

    for source, replacement in replacements.items():
        if source not in updated:
            raise RuntimeError(f"Expected generated geometry was not found in {path}: {source}")
        updated = updated.replace(source, replacement, 1)

    path.write_text(updated, encoding="utf-8")


def main() -> None:
    assets_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".profile-output/assets")
    hero_assets = sorted(assets_dir.glob("hero-*.svg"))

    if not hero_assets:
        raise FileNotFoundError(f"No Terminal hero SVG assets found in {assets_dir}")

    for asset in hero_assets:
        simplify_hero(asset)


if __name__ == "__main__":
    main()
