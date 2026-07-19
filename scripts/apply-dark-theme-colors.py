#!/usr/bin/env python3
"""Apply accessible accent colors to generated dark-theme SVG assets."""

from pathlib import Path
import sys

COLOR_REPLACEMENTS = {
    "#B6493A": "#D96B5C",
    "#315B73": "#6694AA",
}


def update_svg(path: Path) -> None:
    content = path.read_text(encoding="utf-8")
    updated = content

    for source, replacement in COLOR_REPLACEMENTS.items():
        updated = updated.replace(source, replacement)

    if updated == content:
        raise RuntimeError(f"No theme colors found in {path}")

    path.write_text(updated, encoding="utf-8")


def main() -> None:
    assets_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".profile-output/assets")
    dark_assets = sorted(assets_dir.glob("*-dark.svg"))

    if not dark_assets:
        raise FileNotFoundError(f"No dark-theme SVG assets found in {assets_dir}")

    for asset in dark_assets:
        update_svg(asset)


if __name__ == "__main__":
    main()
