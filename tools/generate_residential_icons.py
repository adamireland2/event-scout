#!/usr/bin/env python3
"""Generate green-tinted icons for the Residential edition.

Takes every PNG in icons/ and shifts the indigo hues to emerald,
writing the results to icons-residential/. Run from the repo root:

    python3 tools/generate_residential_icons.py
"""
import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "icons"
DST = ROOT / "icons-residential"

# Indigo hue is ~247 deg (176/255); emerald ~160 deg (113/255).
HUE_SHIFT = int((160 - 247) / 360 * 255)  # negative shift


def tint(path: pathlib.Path, out: pathlib.Path) -> None:
    img = Image.open(path).convert("RGBA")
    r, g, b, a = img.split()
    hsv = Image.merge("RGB", (r, g, b)).convert("HSV")
    h, s, v = hsv.split()
    h = h.point(lambda x: (x + HUE_SHIFT) % 256)
    rgb = Image.merge("HSV", (h, s, v)).convert("RGB")
    result = Image.merge("RGBA", (*rgb.split(), a))
    result.save(out)


def main() -> None:
    DST.mkdir(exist_ok=True)
    for png in sorted(SRC.glob("*.png")):
        tint(png, DST / png.name)
        print(f"tinted {png.name}")


if __name__ == "__main__":
    main()
