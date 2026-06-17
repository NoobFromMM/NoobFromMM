"""Generate assets/intro.gif — a dark-themed intro banner for NoobFromMM.

Usage:
    .venv/bin/python scripts/make-intro-gif.py

Requires: Pillow (installed in .venv)
Output:  assets/intro.gif (780×200, < 500 KB)
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys

WIDTH = 780
HEIGHT = 200
BG_COLOR = (13, 17, 23)         # #0d1117
CARD_COLOR = (22, 27, 34)       # #161b22
ACCENT = (88, 166, 255)         # #58a6ff
GREEN = (63, 185, 80)           # #3fb950
MUTED = (144, 157, 171)         # #8b949e approximation of b0b8c2
WHITE = (201, 209, 217)         # #c9d1d9
CORNER = 12
FRAMES = 30
DURATION = 80  # ms per frame → ~2.4s total loop

# ── Font setup ──────────────────────────────────────────────

def find_font():
    """Find a usable monospace or system font."""
    candidates = [
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/SFNSMono.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SF-Pro.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


FONT_PATH = find_font()
if FONT_PATH:
    font_large = ImageFont.truetype(FONT_PATH, 28)
    font_medium = ImageFont.truetype(FONT_PATH, 16)
    font_small = ImageFont.truetype(FONT_PATH, 13)
    font_emoji = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", 26)
else:
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()
    font_emoji = ImageFont.load_default()
    print("Warning: no system font found, using Pillow default")


# ── Helpers ─────────────────────────────────────────────────

def draw_rounded_rect(draw, xy, radius, fill):
    """Draw a filled rounded rectangle."""
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill)


def draw_accent_bar(draw, x, y0, y1):
    """Draw a vertical accent bar."""
    draw.rectangle([x, y0, x + 3, y1], fill=ACCENT)


def blend(a, b, t):
    """Linear blend of two (R,G,B) tuples."""
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def wave_offset(frame, total):
    """Return a small vertical offset for the waving hand emoji."""
    import math
    cycle = (frame / total) * 2 * math.pi
    return int(math.sin(cycle) * 4)


# ── Frame builder ───────────────────────────────────────────

def make_frame(frame_num):
    """Build one frame of the GIF."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Card background
    draw_rounded_rect(draw, (8, 8, WIDTH - 8, HEIGHT - 8), CORNER, CARD_COLOR)

    # Left accent bar
    draw_accent_bar(draw, 16, 36, HEIGHT - 36)

    progress = frame_num / (FRAMES - 1) if FRAMES > 1 else 1.0

    # ── Waving hand ──
    hand_x = 48
    hand_y = 58 + wave_offset(frame_num, FRAMES)
    try:
        draw.text((hand_x, hand_y), "\U0001F44B", font=font_emoji, embedded_color=True)
    except Exception:
        # Fallback: draw a simple circle for the "hand"
        draw.ellipse([hand_x, hand_y, hand_x + 22, hand_y + 22], fill=ACCENT)

    # ── Main text ──
    main_text = "Hi there! I'm NoobFromMM"
    text_x = 88
    text_y = 55

    # Fade in the main text (opacity via color blend with BG)
    fade = min(1.0, progress * 3.0)  # finishes fading by frame ~10
    color = blend(CARD_COLOR, WHITE, fade)
    draw.text((text_x, text_y), main_text, font=font_large, fill=color)

    # ── Terminal cursor (blinking) ──
    blink_on = (frame_num % 6) < 4  # 4 on, 2 off
    if blink_on and fade > 0.5:
        text_bbox = draw.textbbox((text_x, text_y), main_text, font=font_large)
        cursor_x = text_bbox[2] + 4
        cursor_y0 = text_y + 4
        cursor_h = font_large.size - 4 if FONT_PATH else 20
        draw.rectangle(
            [cursor_x, cursor_y0, cursor_x + 8, cursor_y0 + cursor_h],
            fill=GREEN,
        )

    # ── Secondary text ──
    sub_text = "Network Engineer  ·  Local App Founder  ·  Server Builder"
    sub_y = 105
    sub_fade = min(1.0, max(0, (progress - 0.15) * 3.5))
    sub_color = blend(CARD_COLOR, MUTED, sub_fade)
    draw.text((text_x, sub_y), sub_text, font=font_medium, fill=sub_color)

    # ── Bottom accent line ──
    line_y = HEIGHT - 40
    line_width = int(WIDTH * 0.55)
    line_x0 = text_x
    line_progress = min(1.0, max(0, (progress - 0.25) * 2.5))
    line_end = int(line_x0 + line_width * line_progress)
    draw.line([(line_x0, line_y), (line_end, line_y)], fill=ACCENT, width=1)

    # ── Scanline effect ──
    for i in range(0, HEIGHT, 3):
        draw.line([(0, i), (WIDTH, i)], fill=(255, 255, 255, 6), width=1)

    return img


# ── Main ────────────────────────────────────────────────────

def main():
    frames = [make_frame(i) for i in range(FRAMES)]

    # Ping-pong: forward then reverse for smooth loop (skip duplicate endpoints)
    reverse_frames = frames[-2:0:-1]
    all_frames = frames + reverse_frames

    out_path = os.path.join(
        os.path.dirname(__file__), "..", "assets", "intro.gif"
    )
    out_path = os.path.abspath(out_path)

    # Convert to palette for smaller file
    paletted = []
    for f in all_frames:
        p = f.convert("P", palette=Image.ADAPTIVE, colors=64)
        paletted.append(p)

    paletted[0].save(
        out_path,
        save_all=True,
        append_images=paletted[1:],
        duration=DURATION,
        loop=0,
        optimize=True,
        disposal=2,
    )

    size_kb = os.path.getsize(out_path) / 1024
    print(f"Wrote {out_path}  ({len(all_frames)} frames, {size_kb:.0f} KB)")
    if size_kb > 500:
        print("Warning: file exceeds 500 KB target", file=sys.stderr)


if __name__ == "__main__":
    main()
