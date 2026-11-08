#!/usr/bin/env python3
"""Downloads the Higgsfield step clips listed in art-src/video-urls.txt ("name url" per line)
and encodes them for the game: vid/<name>.mp4, 960 px wide, no sound, a keyframe every
3 frames so the child's finger can scrub the clip smoothly."""
import subprocess
import urllib.request
from pathlib import Path

root = Path(__file__).parent
src = root / "art-src" / "video"
out = root / "vid"
src.mkdir(parents=True, exist_ok=True)
out.mkdir(exist_ok=True)
FF = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"

for line in (root / "art-src" / "video-urls.txt").read_text().split("\n"):
    if not line.strip():
        continue
    name, url = line.split()
    raw = src / f"{name}.mp4"
    if not raw.exists():
        urllib.request.urlretrieve(url, raw)
    subprocess.run([FF, "-v", "error", "-y", "-i", str(raw), "-vf", "scale=960:-2,fps=24", "-an",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "27", "-pix_fmt", "yuv420p",
                    "-g", "3", "-keyint_min", "3", "-movflags", "+faststart", str(out / f"{name}.mp4")], check=True)
    print(name, (out / f"{name}.mp4").stat().st_size // 1024, "KB")
