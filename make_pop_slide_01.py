"""Cover slide (pop_slide_01.png) for the pop & colorful carousel series.

Pink background with polka dots, a big yellow circle, light-blue waves,
a big white headline with a thick black outline, a series label and the
swipe hint. After drawing, every text box is checked for missing glyphs
and overflow.
"""
import math

from PIL import Image, ImageDraw

from pop_common import (BLACK, PINK, PINK_DEEP, ROOT, SKY, W, H, YELLOW, draw_footer,
                        load_font, outlined_text, rounded_label, save_and_check)

OUT_PATH = ROOT / "pop_slide_01.png"

PINK_DOT = (255, 178, 206)  # slightly lighter pink for the polka dots


def wave_band(draw, x0, x1, y, thickness, amp, wavelength, fill):
    """Filled band whose top and bottom edges follow the same sine wave."""
    n = 80
    top, bottom = [], []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        off = amp * math.sin(2 * math.pi * (x - x0) / wavelength)
        top.append((x, y + off))
        bottom.append((x, y + off + thickness))
    draw.polygon(top + bottom[::-1], fill=fill)


def wave_floor(draw, y, amp, wavelength, fill):
    """Sine-wave edge filled down to the bottom of the canvas."""
    pts = [(x, y + amp * math.sin(2 * math.pi * x / wavelength)) for x in range(0, W + 1, 10)]
    draw.polygon(pts + [(W, H), (0, H)], fill=fill)


def sparkle(draw, cx, cy, r, fill):
    """Four-point star."""
    k = r * 0.28
    draw.polygon([(cx, cy - r), (cx + k, cy - k), (cx + r, cy), (cx + k, cy + k),
                  (cx, cy + r), (cx - k, cy + k), (cx - r, cy), (cx - k, cy - k)],
                 fill=fill, outline=BLACK, width=4)


def draw_background(draw):
    draw.rectangle((0, 0, W, H), fill=PINK)
    for row, y in enumerate(range(30, H, 90)):  # offset polka dots
        for x in range(30 + (row % 2) * 45, W, 90):
            draw.ellipse((x - 9, y - 9, x + 9, y + 9), fill=PINK_DOT)

    # waves run edge to edge and pass behind the circles
    wave_band(draw, -20, W + 20, 290, 34, 18, 180, SKY)
    wave_band(draw, -20, W + 20, 1030, 28, 14, 160, SKY)
    draw.ellipse((850 - 340, 330 - 340, 850 + 340, 330 + 340), fill=YELLOW)
    draw.ellipse((130 - 130, 1120 - 130, 130 + 130, 1120 + 130), fill=YELLOW)
    wave_floor(draw, 1180, 26, 300, SKY)

    sparkle(draw, 110, 400, 30, YELLOW)
    sparkle(draw, 980, 760, 36, YELLOW)


def draw_headline(draw):
    lines = [("今日のごはん、", 128, 540), ("ちょっと", 112, 700), ("盛り足し！", 170, 890)]
    for i, (text, size, y) in enumerate(lines):
        outlined_text(draw, (W // 2, y), text, load_font(size), stroke_w=14,
                      shadow=PINK_DEEP, shadow_off=(10, 12), label=f"headline {i + 1}")


def main():
    img = Image.new("RGB", (W, H), PINK)
    draw = ImageDraw.Draw(img)
    draw_background(draw)
    rounded_label(draw, (80, 90), "シリーズ1", load_font(40), label="series label")
    draw_headline(draw)
    draw_footer(draw)
    save_and_check(img, OUT_PATH)


if __name__ == "__main__":
    main()
