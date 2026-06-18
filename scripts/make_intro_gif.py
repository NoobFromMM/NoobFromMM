"""
Generate assets/intro.gif — dark-themed typewriter + network topology banner.

CUSTOMIZATION — edit these before running:
  - first_name (line ~145):  your full display name
  - insert_part (line ~148): the nickname prefix inserted before "MM"
  - The pause counts control animation pacing (lines ~158, ~169, ~175, ~181)

Usage:
    .venv/bin/python scripts/make_intro_gif.py

Requires: Pillow only (no browser, no external assets).
Output:  assets/intro.gif
"""

from __future__ import annotations

import math
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WIDTH = 900
HEIGHT = 160
OUT = Path("assets/intro.gif")
OUT.parent.mkdir(parents=True, exist_ok=True)

random.seed(42)

# ---------- Fonts ----------
def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/SFNSMono.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]

    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except Exception:
            pass

    return ImageFont.load_default()


TITLE_FONT = load_font(31, bold=True)

# ---------- Network background ----------
nodes = [
    # x, y, radius, phase, glow
    (20, 82, 3, 0.2, False),
    (85, 42, 4, 1.3, True),
    (150, 74, 3, 2.4, False),
    (210, 108, 4, 0.7, True),
    (292, 92, 3, 1.8, False),
    (380, 62, 3, 2.9, False),
    (465, 95, 4, 0.4, True),
    (545, 56, 3, 1.1, False),
    (620, 84, 3, 2.1, True),
    (700, 42, 4, 0.6, True),
    (775, 70, 3, 1.6, False),
    (845, 36, 4, 2.7, True),
    (890, 112, 3, 0.9, False),
    (120, 128, 3, 2.2, False),
    (335, 124, 3, 1.5, True),
    (590, 122, 3, 0.8, False),
    (760, 126, 4, 2.5, True),
]

extra_nodes = []
for _ in range(28):
    extra_nodes.append((
        random.randint(0, WIDTH),
        random.randint(10, HEIGHT - 10),
        random.choice([1, 1, 2, 2, 3]),
        random.random() * math.tau,
        random.random() > 0.72,
    ))

nodes.extend(extra_nodes)


def node_pos(node, frame_index: int):
    x, y, r, phase, glow = node
    t = frame_index / 12.0
    dx = math.sin(t * 0.55 + phase) * 6
    dy = math.cos(t * 0.45 + phase) * 4
    return x + dx, y + dy, r, glow


def draw_gradient_background() -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), "#061b38")
    px = img.load()

    for y in range(HEIGHT):
        for x in range(WIDTH):
            nx = x / WIDTH
            ny = y / HEIGHT

            # dark blue -> teal gradient
            r = int(4 + 0 * nx + 0 * ny)
            g = int(23 + 48 * nx + 20 * (1 - ny))
            b = int(55 + 55 * nx + 20 * (1 - ny))

            # subtle light bloom on right
            bloom = max(0, 1 - ((x - 820) ** 2 + (y - 30) ** 2) / 90000)
            g = min(255, int(g + bloom * 55))
            b = min(255, int(b + bloom * 45))

            px[x, y] = (r, g, b)

    return img


def draw_network(base: Image.Image, frame_index: int) -> Image.Image:
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    positions = [node_pos(n, frame_index) for n in nodes]

    # Lines
    for i, a in enumerate(positions):
        ax, ay, ar, aglow = a
        for j in range(i + 1, len(positions)):
            bx, by, br, bglow = positions[j]
            dist = math.hypot(ax - bx, ay - by)

            if dist < 135:
                alpha = int(max(12, 95 - dist * 0.55))
                if aglow or bglow:
                    alpha += 24

                color = (70, 220, 255, min(145, alpha))
                draw.line((ax, ay, bx, by), fill=color, width=1)

    # Nodes + glow
    for x, y, r, glow in positions:
        if glow:
            for rr, alpha in [(14, 28), (9, 55), (5, 110)]:
                draw.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(0, 238, 255, alpha))

        fill = (32, 235, 255, 230) if glow else (128, 210, 235, 155)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=fill)

    # Very subtle scan/grid lines
    for x in range(0, WIDTH, 4):
        draw.line((x, 0, x, HEIGHT), fill=(255, 255, 255, 8), width=1)

    return Image.alpha_composite(base.convert("RGBA"), layer)


# ── Text animation ──────────────────────────────────────────
# EDIT HERE: change first_name and insert_part to customize.
# ────────────────────────────────────────────────────────────
prefix = "Hi there! I'm "
first_name = "Myat Thaw Maung"
insert_part = "NoobFrom"
# ── END CUSTOMIZE ──
first_text = prefix + first_name
keep_text = prefix + "MM"
final_text = prefix + insert_part + "MM"

timeline: list[str] = []

# Type "Hi there! I'm Myat Thaw Maung"
for i in range(1, len(first_text) + 1):
    timeline.append(first_text[:i])

# Pause after full name
for _ in range(16):
    timeline.append(first_text)

# Delete Myat Thaw Maung, then leave MM
# This intentionally ends with "Hi there! I'm MM"
current_name = first_name
while len(current_name) > 0:
    current_name = current_name[:-1]
    if current_name:
        timeline.append(prefix + current_name)
    else:
        timeline.append(keep_text)

for _ in range(6):
    timeline.append(keep_text)

# Type NoobFrom in front of kept MM:
# "Hi there! I'm MM" -> "Hi there! I'm NoobFromMM"
for i in range(1, len(insert_part) + 1):
    timeline.append(prefix + insert_part[:i] + "MM")

# Final pause
for _ in range(34):
    timeline.append(final_text)


def text_size(draw: ImageDraw.ImageDraw, text: str, font) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def draw_centered_text(img: Image.Image, text: str, frame_index: int) -> Image.Image:
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    display_text = "👋 " + text
    tw, th = text_size(draw, display_text, TITLE_FONT)
    x = (WIDTH - tw) // 2
    y = (HEIGHT - th) // 2 - 2

    # text glow/shadow
    for offset, alpha in [((0, 0), 80), ((0, 2), 100), ((2, 2), 60)]:
        draw.text((x + offset[0], y + offset[1]), display_text, font=TITLE_FONT, fill=(0, 0, 0, alpha))

    # main text
    draw.text((x, y), display_text, font=TITLE_FONT, fill=(242, 250, 255, 255))

    # cursor
    cursor_on = (frame_index // 6) % 2 == 0
    if cursor_on:
        # Cursor after displayed text
        cursor_x = x + tw + 8
        cursor_y = y + 4
        draw.rectangle(
            (cursor_x, cursor_y, cursor_x + 10, cursor_y + th + 2),
            fill=(44, 255, 150, 230),
        )

    return Image.alpha_composite(img.convert("RGBA"), layer)


def make_frame(text: str, frame_index: int) -> Image.Image:
    base = draw_gradient_background()
    bg = draw_network(base, frame_index)
    composed = draw_centered_text(bg, text, frame_index)

    # Convert with adaptive palette for GIF size
    return composed.convert("P", palette=Image.Palette.ADAPTIVE, colors=128)


frames = [make_frame(text, idx) for idx, text in enumerate(timeline)]

OUT.parent.mkdir(parents=True, exist_ok=True)
frames[0].save(
    OUT,
    save_all=True,
    append_images=frames[1:],
    duration=55,
    loop=0,
    optimize=True,
    disposal=2,
)

print(f"Generated: {OUT}")
print(f"Frames: {len(frames)}")
print(f"Size: {OUT.stat().st_size / 1024:.1f} KB")
