"""Shared drawing rules for the handwritten-notebook carousel (note_slide_XX.png).

Palette, bundled handwritten font, graph-paper background, notebook header,
hand-drawn lines / marker / memos, and the post-draw text checks.
Every make_note_slide_XX.py builds on this module.
"""
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FONT_PATH = ROOT / "fonts" / "YuseiMagic-Regular.ttf"

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


def fit_font(text, max_w, max_size, min_size=40):
    """Largest font (<= max_size) whose rendered text fits in max_w."""
    for size in range(max_size, min_size - 1, -2):
        font = load_font(size)
        if font.getlength(text) <= max_w:
            return font
    return load_font(min_size)


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


def hand_path(draw, pts, width, fill=INK, jitter=0.8):
    """Pen stroke through the given points with light jitter and round ends."""
    pts = [(x + random.uniform(-jitter, jitter), y + random.uniform(-jitter, jitter))
           for x, y in pts]
    draw.line(pts, fill=fill, width=width, joint="curve")
    r = width // 2
    for x, y in (pts[0], pts[-1]):
        draw.ellipse((x - r, y - r, x + r, y + r), fill=fill)


def arc_points(cx, cy, rx, ry, a0, a1, n=60):
    """Points along an ellipse arc, angles in degrees (0 = right, 90 = down)."""
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


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


def speech_bubble(draw, cx, cy, text, font, tail_to, label, pad_x=36, pad_y=26, r=34):
    """Hand-drawn rounded bubble around text with a tail pointing at tail_to."""
    l, t, rr, b = draw.textbbox((cx, cy), text, font=font, anchor="mm")
    x0, y0, x1, y1 = l - pad_x, t - pad_y, rr + pad_x, b + pad_y
    # tail base sits on the edge closest to the target
    tx, ty = tail_to
    side_top = ty < y0
    base_y = y0 if side_top else y1
    bx = min(max(tx, x0 + r + 30), x1 - r - 30)
    gap0, gap1 = bx - 20, bx + 20

    pts = []
    # walk clockwise from the top-left corner, leaving a gap for the tail
    pts += arc_points(x0 + r, y0 + r, r, r, 180, 270, 12)
    if side_top:
        pts += [(gap0, y0), (tx, ty), (gap1, y0)]
    pts += arc_points(x1 - r, y0 + r, r, r, 270, 360, 12)
    pts += arc_points(x1 - r, y1 - r, r, r, 0, 90, 12)
    if not side_top:
        pts += [(gap1, y1), (tx, ty), (gap0, y1)]
    pts += arc_points(x0 + r, y1 - r, r, r, 90, 180, 12)
    pts.append(pts[0])
    hand_path(draw, pts, 4)
    return draw_text(draw, (cx, cy), text, font, label=label,
                     container=(x0, y0, x1, y1)), (x0, y0, x1, y1), base_y


# ---------------------------------------------------------------- page parts

def draw_paper(draw):
    draw.rectangle((0, 0, W, H), fill=PAPER)
    for i, x in enumerate(range(0, W + 1, GRID_STEP)):
        draw.line((x, 0, x, H), fill=GRID_BOLD if i % 5 == 0 else GRID, width=1)
    for i, y in enumerate(range(0, H + 1, GRID_STEP)):
        draw.line((0, y, W, y), fill=GRID_BOLD if i % 5 == 0 else GRID, width=1)


def draw_header(draw, number):
    # Notebook header: "No." and "Date" fields, then the series tag
    f = load_font(36)
    draw_text(draw, (100, 120), f"No. {number:02d}", f, anchor="ls", label="header No.")
    wobbly_line(draw, 100, 134, 250, 134, 3, INK, amp=1.2)
    draw_text(draw, (690, 120), "Date", f, anchor="ls", label="header Date")
    draw_text(draw, (840, 120), ".     .", f, anchor="ls", label="header dots")
    wobbly_line(draw, 690, 134, 980, 134, 3, INK, amp=1.2)

    tag = load_font(40)
    draw_text(draw, (100, 230), "ごはんノート", tag, anchor="ls", label="series tag")


def draw_headline(draw, text, y=340, max_size=84):
    """Page headline with a hand-drawn ink underline (slides 2+)."""
    font = fit_font(text, W - 2 * 90, max_size)
    l, t, r, b = draw_text(draw, (W // 2, y), text, font, label="headline")
    wobbly_line(draw, l, b + 22, r, b + 18, 5, INK, amp=2.0)


def draw_marker_point(img, draw, text, y, size=72):
    """Key phrase with a marker swipe under its lower half."""
    font = load_font(size)
    l, t, r, b = draw.textbbox((W // 2, y), text, font=font, anchor="mm")
    marker_stroke(img, l - 14, r + 14, b - 10, 48)
    draw = ImageDraw.Draw(img)
    draw_text(draw, (W // 2, y), text, font, label=f"point {text}")
    return draw


# ---------------------------------------------------------------- food line drawings

def draw_fish_plate(draw, px, py, k, w):
    hand_path(draw, arc_points(px, py, 150 * k, 58 * k, 0, 365), w(4))
    fish = (arc_points(px - 15 * k, py, 78 * k, 26 * k, 200, 340, 20)
            + arc_points(px - 15 * k, py, 78 * k, 26 * k, 20, 160, 20))
    hand_path(draw, fish + [fish[0]], w(4))
    hand_path(draw, [(px + 60 * k, py), (px + 96 * k, py - 22 * k),
                     (px + 96 * k, py + 22 * k), (px + 60 * k, py)], w(4))  # tail
    draw.ellipse((px - 72 * k, py - 8 * k, px - 62 * k, py + 2 * k), fill=INK)  # eye


def draw_mushroom(draw, x, y, k, w):
    """Small shimeji-style mushroom: domed cap on a short stem."""
    cap = arc_points(x, y, 24 * k, 18 * k, 180, 360, 16)
    hand_path(draw, cap + [cap[0]], w(4))
    hand_path(draw, [(x - 8 * k, y), (x - 7 * k, y + 28 * k),
                     (x + 7 * k, y + 28 * k), (x + 8 * k, y)], w(4))


def draw_salad_plate(draw, px, py, k, w):
    """Plate of shredded cabbage with a couple of mushrooms on top."""
    hand_path(draw, arc_points(px, py, 150 * k, 58 * k, 0, 365), w(4))
    for dx, dy in ((-95, -6), (-70, -22), (-62, 12), (-38, -4), (-20, 22), (-10, -26)):
        wobbly_line(draw, px + (dx - 22) * k, py + dy * k, px + (dx + 22) * k, py + (dy - 4) * k,
                    w(3), INK, amp=3 * k, waves=1.0)
    draw_mushroom(draw, px + 40 * k, py - 6 * k, k, w)
    draw_mushroom(draw, px + 92 * k, py + 2 * k, k, w)


def draw_rice_bowl(draw, bx, by, k, w):
    """Rice bowl holding only a small mound of rice, sunk low."""
    hand_path(draw, arc_points(bx, by, 96 * k, 24 * k, 0, 362), w(4))
    hand_path(draw, arc_points(bx, by, 96 * k, 82 * k, 0, 180), w(5))
    hand_path(draw, [(bx - 34 * k, by + 80 * k), (bx - 30 * k, by + 94 * k),
                     (bx + 30 * k, by + 94 * k), (bx + 34 * k, by + 80 * k)], w(4))
    hand_path(draw, arc_points(bx, by + 6 * k, 34 * k, 16 * k, 190, 350, 20), w(4))


def draw_soup_bowl(draw, sx, sy, k, w, steam=True, mushrooms=False):
    hand_path(draw, arc_points(sx, sy, 90 * k, 22 * k, 0, 362), w(4))
    hand_path(draw, arc_points(sx, sy, 90 * k, 74 * k, 0, 180), w(5))
    if steam:
        for dx in (-30, 0, 30):
            wobbly_line(draw, sx + dx * k, sy - 40 * k, sx + dx * k + 4 * k, sy - 90 * k,
                        w(3), INK, amp=5 * k, waves=1.2)
    if mushrooms:  # mushroom slices floating in the soup
        for dx in (-40, 0, 40):
            cap = arc_points(sx + dx * k, sy + 4 * k, 16 * k, 9 * k, 180, 360, 10)
            hand_path(draw, cap + [cap[0]], w(3))


def draw_meal(draw, cx=540, cy=625, s=1.0, veg=False):
    """Tray meal with little rice. veg=True adds cabbage/mushroom dishes.

    Drawn in a 700x310 box centered at (cx, cy), scaled by s.
    """
    def P(x, y):
        return cx + (x - 540) * s, cy + (y - 625) * s

    def w(n):
        return max(1, round(n * s))

    x0, y0 = P(190, 470)
    x1, y1 = P(890, 780)
    r = 30 * s
    tray = (arc_points(x0 + r, y0 + r, r, r, 180, 270, 10)
            + arc_points(x1 - r, y0 + r, r, r, 270, 360, 10)
            + arc_points(x1 - r, y1 - r, r, r, 0, 90, 10)
            + arc_points(x0 + r, y1 - r, r, r, 90, 180, 10))
    hand_path(draw, tray + [tray[0]], w(5))

    if veg:
        draw_fish_plate(draw, *P(392, 566), s * 0.86, w)
        draw_salad_plate(draw, *P(700, 566), s * 0.86, w)
    else:
        draw_fish_plate(draw, *P(540, 570), s, w)
    draw_rice_bowl(draw, *P(340, 680), s, w)
    draw_soup_bowl(draw, *P(740, 680), s, w, steam=not veg, mushrooms=veg)

    # chopsticks along the bottom of the tray
    hand_path(draw, [P(470, 752), P(640, 742)], w(4))
    hand_path(draw, [P(470, 764), P(640, 760)], w(4))
    return x0, y0, x1, y1


def draw_footer(draw):
    f = load_font(42)
    draw_text(draw, (W - 100, H - 110), "スワイプしてね →", f, anchor="rs", label="swipe hint")


def new_page(number):
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    draw = ImageDraw.Draw(img)
    draw_paper(draw)
    draw_header(draw, number)
    return img, draw
