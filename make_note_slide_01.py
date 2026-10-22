"""Cover slide (note_slide_01.png) for the handwritten-notebook carousel series.

Separate series from slide_XX.png. Graph-paper background, big handwritten
headline with a marker stroke underneath, and scribbled memos in the margins.
After drawing, every text box is checked for missing glyphs and overflow.
"""
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FONT_PATH = ROOT / "fonts" / "YuseiMagic-Regular.ttf"
OUT_PATH = ROOT / "note_slide_01.png"

W, H = 1080, 1350
SAFE = 60  # keep every text box at least this far from the canvas edge

# Palette: cream paper / dark gray ink / one marker accent
PAPER = (251, 247, 234)
GRID = (222, 220, 212)
GRID_BOLD = (205, 203, 195)
INK = (58, 58, 62)
MARKER = (255, 214, 64)

GRID_STEP = 40

random.seed(7)  # same wobble on every run


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
        print(f"[{status}] {label}: bbox={tuple(round(v) for v in bbox)} box={box}"
              + (f" missing={miss}" if miss else ""))
    return ok


# ---------------------------------------------------------------- drawing helpers

def draw_text(draw, xy, text, font, fill=INK, anchor="mm", label=None, container=None):
    draw.text(xy, text, font=font, fill=fill, anchor=anchor)
    bbox = draw.textbbox(xy, text, font=font, anchor=anchor)
    text_boxes.append((label or text, text, font, bbox, container))
    return bbox


def wobbly_line(draw, x0, y0, x1, y1, width, fill, amp=3.0, waves=2.5):
    """Hand-drawn looking line: slight sine wobble plus jitter."""
    n = max(int(math.hypot(x1 - x0, y1 - y0) / 6), 2)
    phase = random.uniform(0, math.pi)
    pts = []
    for i in range(n + 1):
        t = i / n
        off = amp * math.sin(t * waves * math.pi * 2 + phase) + random.uniform(-0.6, 0.6)
        pts.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + off))
    draw.line(pts, fill=fill, width=width, joint="curve")
    r = width // 2
    for x, y in (pts[0], pts[-1]):
        draw.ellipse((x - r, y - r, x + r, y + r), fill=fill)


def marker_stroke(base, x0, x1, y, height):
    """Translucent highlighter swipe, slightly tilted, with ragged ends."""
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    color = MARKER + (210,)
    tilt = random.uniform(-4, 4)
    for k in range(3):  # overlapping passes give an uneven marker edge
        dy = (k - 1) * height * 0.22
        wobbly_line(d, x0 + random.uniform(-6, 6), y + dy - tilt,
                    x1 + random.uniform(-6, 6), y + dy + tilt,
                    int(height * 0.55), color, amp=2.0, waves=1.2)
    base.alpha_composite(layer)


def wobbly_ellipse(draw, cx, cy, rx, ry, width, fill, turns=1.12):
    """Loose hand-drawn loop that overshoots its start like a pen circle."""
    n = 120
    start = random.uniform(0, math.pi * 2)
    pts = []
    for i in range(int(n * turns) + 1):
        a = start + i / n * math.pi * 2
        grow = 1 + 0.06 * i / n
        pts.append((cx + rx * grow * math.cos(a) + random.uniform(-0.8, 0.8),
                    cy + ry * grow * math.sin(a) + random.uniform(-0.8, 0.8)))
    draw.line(pts, fill=fill, width=width, joint="curve")


def rotated_memo(base, center, text, font, angle, label, pad=24):
    """Draw text on its own layer, rotate it, paste it, and record the rotated bbox."""
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    l, t, r, b = tmp.textbbox((0, 0), text, font=font)
    tw, th = r - l, b - t
    layer = Image.new("RGBA", (tw + pad * 2, th + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((pad - l, pad - t), text, font=font, fill=INK)
    rot = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    x = int(center[0] - rot.width / 2)
    y = int(center[1] - rot.height / 2)
    base.alpha_composite(rot, (x, y))
    ink = rot.getbbox()  # actual ink extent after rotation
    bbox = (x + ink[0], y + ink[1], x + ink[2], y + ink[3])
    text_boxes.append((label, text, font, bbox, None))
    return bbox


# ---------------------------------------------------------------- slide

def draw_paper(draw):
    draw.rectangle((0, 0, W, H), fill=PAPER)
    for i, x in enumerate(range(0, W + 1, GRID_STEP)):
        draw.line((x, 0, x, H), fill=GRID_BOLD if i % 5 == 0 else GRID, width=1)
    for i, y in enumerate(range(0, H + 1, GRID_STEP)):
        draw.line((0, y, W, y), fill=GRID_BOLD if i % 5 == 0 else GRID, width=1)


def draw_header(draw):
    # Notebook header: "No." and "Date" fields
    f = load_font(36)
    draw_text(draw, (100, 120), "No. 01", f, anchor="ls", label="header No.")
    wobbly_line(draw, 100, 134, 250, 134, 3, INK, amp=1.2)
    draw_text(draw, (690, 120), "Date", f, anchor="ls", label="header Date")
    draw_text(draw, (840, 120), ".     .", f, anchor="ls", label="header dots")
    wobbly_line(draw, 690, 134, 980, 134, 3, INK, amp=1.2)

    tag = load_font(40)
    draw_text(draw, (100, 230), "ごはんノート", tag, anchor="ls", label="series tag")


def draw_headline(img, draw):
    font = load_font(128)
    lines = [("今日のごはん、", 470), ("こう変えてみた", 650)]
    # marker first so the ink sits on top of it
    for text, y in lines:
        l, t, r, b = draw.textbbox((W // 2, y), text, font=font, anchor="mm")
        marker_stroke(img, l - 14, r + 14, b - 16, 70)
    draw = ImageDraw.Draw(img)
    for i, (text, y) in enumerate(lines):
        draw_text(draw, (W // 2, y), text, font, label=f"headline {i + 1}",
                  container=(SAFE, SAFE, W - SAFE, H - SAFE))
    return draw


def draw_sub(draw):
    f = load_font(46)
    draw_text(draw, (W // 2, 820), "ちょっとの工夫で、毎日がラクになる", f, label="sub copy")


def draw_memos(img, draw):
    # "大事！" scribbled at the lower-left with a pen loop around it
    memo_font = load_font(72)
    cx, cy = 250, 1040
    bbox = rotated_memo(img, (cx, cy), "大事！", memo_font, 9, "memo 大事！")
    draw = ImageDraw.Draw(img)
    wobbly_ellipse(draw, cx, cy, (bbox[2] - bbox[0]) / 2 + 52, (bbox[3] - bbox[1]) / 2 + 46,
                   5, INK)
    # small arrow from the memo pointing up toward the headline
    wobbly_line(draw, 300, 930, 380, 870, 5, INK, amp=1.0, waves=0.6)
    draw.line([(380, 870), (352, 874)], fill=INK, width=5)
    draw.line([(380, 870), (372, 897)], fill=INK, width=5)

    # second note at the lower-right
    note_font = load_font(44)
    rotated_memo(img, (770, 1010), "まずは1つだけ\nやってみる", note_font, -5,
                 "memo まずは1つだけ")
    draw = ImageDraw.Draw(img)
    wobbly_line(draw, 640, 1080, 900, 1074, 4, INK, amp=1.5)
    return draw


def draw_footer(draw):
    f = load_font(42)
    draw_text(draw, (W - 100, H - 110), "スワイプしてね →", f, anchor="rs", label="swipe hint")


def main():
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    draw = ImageDraw.Draw(img)
    draw_paper(draw)
    draw_header(draw)
    draw = draw_headline(img, draw)
    draw_sub(draw)
    draw = draw_memos(img, draw)
    draw_footer(draw)

    img.convert("RGB").save(OUT_PATH)
    print(f"saved: {OUT_PATH} ({W}x{H})")
    if not check_text():
        sys.exit("[ERROR] 文字の欠け・はみ出しがあります")
    print("all text checks passed")


if __name__ == "__main__":
    main()
