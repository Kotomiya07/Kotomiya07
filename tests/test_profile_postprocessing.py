from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).parents[1]


class ProfilePostprocessingTest(unittest.TestCase):
    def test_simplify_readme_keeps_intro_and_adds_activity_cards(self) -> None:
        generated = """<picture>hero</picture>

English tagline

## Foreground jobs

repositories

## Process tree

processes
"""

        with tempfile.TemporaryDirectory() as directory:
            readme = Path(directory) / "README.md"
            readme.write_text(generated, encoding="utf-8")
            subprocess.run(
                [sys.executable, ROOT / "scripts/simplify-readme.py", readme],
                check=True,
            )
            result = readme.read_text(encoding="utf-8")

        self.assertIn("<picture>hero</picture>", result)
        self.assertIn("English tagline", result)
        self.assertIn("Kotomiya07 GitHub statistics", result)
        self.assertIn("Kotomiya07 most used languages", result)
        self.assertNotIn("Foreground jobs", result)
        self.assertNotIn("Process tree", result)

    def test_simplify_hero_removes_repository_listing_and_reduces_height(self) -> None:
        generated = """<svg width="1200" height="360" viewBox="0 0 1200 360">
<rect width="1200" height="360"/>
<rect width="1172" height="332"/>
<g><text><tspan fill="#B6493A" font-weight="700">$</tspan></text></g>
<g class="ln" style="animation-delay:650ms"><text>ls flagships/</text></g>
<g><text>repository-name</text></g>
</svg>
"""

        with tempfile.TemporaryDirectory() as directory:
            assets = Path(directory)
            hero = assets / "hero-light.svg"
            hero.write_text(generated, encoding="utf-8")
            subprocess.run(
                [sys.executable, ROOT / "scripts/simplify-hero.py", assets],
                check=True,
            )
            result = hero.read_text(encoding="utf-8")

        self.assertIn('height="270" viewBox="0 0 1200 270"', result)
        self.assertIn('width="1172" height="242"', result)
        self.assertIn('y="206"', result)
        self.assertNotIn("ls flagships/", result)
        self.assertNotIn("repository-name", result)


if __name__ == "__main__":
    unittest.main()
