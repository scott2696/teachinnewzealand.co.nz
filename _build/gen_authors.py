#!/usr/bin/env python3
"""Process author portraits into the sizes the site uses.

Square crop biased toward the upper third so the face sits centred in a circular
mask, then 1x and 2x renditions for the byline avatar and the profile box.
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "images", "authors")
SRC = "/Users/scotthamilton/.claude/image-cache/15c42dcc-aafa-4271-8dbb-7ab0bb5abf60"

PEOPLE = [("11.png", "nikau-te-aho"), ("12.png", "charlotte-wilson")]

def square(im, bias=0.42):
    """Crop to a square, keeping `bias` of the excess height above the centre."""
    w, h = im.size
    if w == h:
        return im
    if h > w:
        top = int((h - w) * bias)
        return im.crop((0, top, w, top + w))
    left = (w - h) // 2
    return im.crop((left, 0, left + h, h))

for src, slug in PEOPLE:
    im = Image.open(os.path.join(SRC, src)).convert("RGB")
    sq = square(im)
    for size, suffix in ((160, ""), (320, "@2x")):
        sq.resize((size, size), Image.LANCZOS).save(
            os.path.join(OUT, f"{slug}{suffix}.jpg"), quality=88, optimize=True)
    print(f"  {slug}: {im.size} -> {sq.size} -> 160 + 320")
