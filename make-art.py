#!/usr/bin/env python3
"""Turns the Higgsfield originals in art-src/ into game files in art/:
scene photos as webp, ingredient and fly cut-outs with transparent background."""
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

root = Path(__file__).parent
src, out = root / "art-src", root / "art"
out.mkdir(exist_ok=True)

SCENES = ["kitchen", "fridge", "wash", "crack", "milk", "salt", "whisk", "butter", "cook", "done"]
ITEMS = ["eggs", "milk", "butter", "cheese", "tomato", "cucumber", "salt", "fly"]


def key(rgb):
    """Removes the flat background by colour distance from the corner colour."""
    rgb = rgb.astype(float)
    corners = np.concatenate([rgb[:8, :8].reshape(-1, 3), rgb[:8, -8:].reshape(-1, 3), rgb[-8:, :8].reshape(-1, 3), rgb[-8:, -8:].reshape(-1, 3)])
    bg = np.median(corners, 0)
    d = np.sqrt(((rgb - bg) ** 2).sum(-1))
    alpha = np.clip((d - 38) / 45, 0, 1)
    if bg[1] > bg[0] + 40:  # green screen: despill the fringe
        g = rgb[..., 1]
        m = np.maximum(rgb[..., 0], rgb[..., 2])
        rgb[..., 1] = np.where((g > m) & (alpha < 1), m + (g - m) * .25, g)
    a = Image.fromarray((alpha * 255).astype("uint8")).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.8))
    img = Image.fromarray(rgb.astype("uint8")).convert("RGBA")
    img.putalpha(a)
    return img.crop(a.point(lambda v: 255 if v > 40 else 0).getbbox())


for name in SCENES:
    img = Image.open(src / f"{name}.png").convert("RGB")
    img.thumbnail((1400, 1400), Image.LANCZOS)
    img.save(out / f"{name}.webp", quality=78, method=6)

chef = Image.open(src / "chef.png").convert("RGB")
chef.thumbnail((360, 360), Image.LANCZOS)
chef.save(out / "chef.webp", quality=80, method=6)

for name in ITEMS:
    img = key(np.asarray(Image.open(src / f"i-{name}.png").convert("RGB")))
    img.thumbnail((420, 420), Image.LANCZOS)
    img.save(out / f"i-{name}.webp", quality=84, alpha_quality=90, method=6)

for f in sorted(out.iterdir()):
    print(f.name, f.stat().st_size // 1024, "KB")
