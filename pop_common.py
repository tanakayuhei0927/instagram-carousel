"""Shared drawing rules for the pop & colorful carousel (pop_slide_XX.png).

Palette, bundled rounded-gothic font, outlined text, rounded labels, the
swipe hint, and the post-draw text checks. Separate from the RPG
(slide_XX.png) and notebook (note_slide_XX.png) series.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FONT_PATH = ROOT / "fonts" / "ZenMaruGothic-Black.ttf"

W, H = 1080, 1350
SAFE = 50  # keep every text box at least this far from the canvas edge

# Palette: pink base, accents pink + yellow; light blue only for decorative shapes
PINK = (255, 150, 186)
PINK_DEEP = (236, 72, 136)
YELLOW = (255, 218, 62)
SKY = (138, 214, 244)  # shapes only, never text
WHITE = (255, 255, 255)
BLACK = (24, 20, 28)


def load_font(size):
    if not FONT_PATH.exists():
        sys.exit(f"[ERROR] 日本語フォントが見つかりません: {FONT_PATH}")
    return ImageFont.truetype(str(FONT_PATH), size)


# ---------------------------------------------------------------- checks

text_boxes = []  # (label, text, font, bbox, container)


def missing_glyphs(font, text):
    """Chars the font renders as the same box as a surely-missing codepoint."""
    def render(c):
        im = Image.new("L", (font.size * 2, font.size * 2), 0)
        ImageDraw.Draw(im).text((font.size // 2, font.size // 2), c, font=font, fill=255)
        return im.tobytes()

    tofu = render("")
    return [c for c in set(text) if not c.isspace() and render(c) == tofu]


def check_text():
    ok = True
    full = (SAFE, SAFE, W - SAFE, H - SAFE)
    for label, text, font, bbox, container in text_boxes:
        box = container or full
        miss = missing_glyphs(font, text)
        inside = (bbox[0] >= box[0] and bbox[1] >= box[1]
                  and bbox[2] <= box[2] and bbox[3] <= box[3])
        status = "OK" if inside and not miss else "NG"
        ok &= status == "OK"
        print(f"[{status}] {label}: bbox={tuple(round(v) for v in bbox)} box={tuple(round(v) for v in box)}"
              + (f" missing={miss}" if miss else ""))
    return ok


def save_and_check(img, out_path):
    img.convert("RGB").save(out_path)
    print(f"saved: {out_path} ({W}x{H})")
    if not check_text():
        sys.exit("[ERROR] 文字の欠け・はみ出しがあります")
    print("all text checks passed")


# ---------------------------------------------------------------- text

def outlined_text(draw, xy, text, font, fill=WHITE, stroke=BLACK, stroke_w=10,
                  shadow=None, shadow_off=(0, 0), anchor="mm", label=None, container=None):
    """Text with a thick outline and an optional offset shadow; the bbox includes both."""
    x, y = xy
    if shadow:
        sx, sy = shadow_off
        draw.text((x + sx, y + sy), text, font=font, fill=shadow, anchor=anchor,
                  stroke_width=stroke_w, stroke_fill=shadow)
    draw.text(xy, text, font=font, fill=fill, anchor=anchor,
              stroke_width=stroke_w, stroke_fill=stroke)
    l, t, r, b = draw.textbbox(xy, text, font=font, anchor=anchor, stroke_width=stroke_w)
    if shadow:
        l, t = min(l, l + shadow_off[0]), min(t, t + shadow_off[1])
        r, b = max(r, r + shadow_off[0]), max(b, b + shadow_off[1])
    bbox = (l, t, r, b)
    text_boxes.append((label or text, text, font, bbox, container))
    return bbox


def rounded_label(draw, xy, text, font, fill=YELLOW, text_fill=BLACK, pad_x=30, pad_y=14,
                  border=5, label=None):
    """Pill-shaped label with a black border; xy is the top-left corner."""
    x, y = xy
    l, t, r, b = draw.textbbox((0, 0), text, font=font, anchor="lt")
    w, h = r - l + pad_x * 2, b - t + pad_y * 2
    box = (x, y, x + w, y + h)
    draw.rounded_rectangle(box, radius=h // 2, fill=fill, outline=BLACK, width=border)
    draw.text((x + pad_x - l, y + pad_y - t), text, font=font, fill=text_fill, anchor="lt")
    tb = draw.textbbox((x + pad_x - l, y + pad_y - t), text, font=font, anchor="lt")
    text_boxes.append((label or text, text, font, tb, box))
    return box


def draw_footer(draw):
    outlined_text(draw, (W - 70, H - 80), "スワイプしてね →", load_font(50), stroke_w=7,
                  anchor="rs", label="swipe hint")
