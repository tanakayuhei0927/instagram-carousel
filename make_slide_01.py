"""Instagram carousel slide 01 (cover) — retro 16bit RPG diet guide.

Usage: python3 make_slide_01.py  ->  slide_01.png (1080x1350)
"""
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FONT_PATH = ROOT / "fonts" / "NotoSansJP-VF.ttf"
OUT_PATH = ROOT / "slide_01.png"

W, H = 1080, 1350

# Palette: navy / grass green / cream / gold (+ minimal accents)
NAVY_DEEP = (10, 18, 44)
NAVY = (18, 32, 72)
NAVY_LIGHT = (34, 54, 108)
GREEN_DARK = (30, 92, 48)
GREEN = (58, 150, 72)
GREEN_LIGHT = (108, 196, 92)
CREAM = (248, 238, 206)
CREAM_DARK = (214, 196, 150)
GOLD = (236, 184, 58)
GOLD_DARK = (168, 116, 28)
GOLD_LIGHT = (255, 222, 120)
RED = (226, 72, 58)
INK = (12, 10, 24)

# Squirrel colors
SQ_OUT = (40, 20, 10)
SQ_MAIN = (204, 116, 52)
SQ_SHADE = (150, 74, 30)
SQ_LIGHT = (236, 156, 84)
SQ_BELLY = (250, 228, 184)
SQ_PINK = (240, 140, 140)
SQ_EYE = (20, 12, 10)
SQ_WHITE = (255, 255, 255)
SQ_TEAR = (120, 190, 255)


def load_font(size, weight):
    if not FONT_PATH.exists():
        sys.exit(f"[ERROR] 日本語フォントが見つかりません: {FONT_PATH}")
    font = ImageFont.truetype(str(FONT_PATH), size)
    font.set_variation_by_axes([weight])
    return font


# ---------------------------------------------------------------- text helpers

text_boxes = []  # (label, bbox, container) — checked after drawing


def draw_text(draw, xy, text, font, fill, anchor="mm", shadow=None, shadow_off=6,
              stroke=0, stroke_fill=None, label=None, container=None):
    x, y = xy
    if shadow:
        draw.text((x + shadow_off, y + shadow_off), text, font=font, fill=shadow,
                  anchor=anchor, stroke_width=stroke, stroke_fill=shadow)
    draw.text((x, y), text, font=font, fill=fill, anchor=anchor,
              stroke_width=stroke, stroke_fill=stroke_fill)
    bbox = draw.textbbox((x, y), text, font=font, anchor=anchor, stroke_width=stroke)
    if shadow:
        bbox = (bbox[0], bbox[1], bbox[2] + shadow_off, bbox[3] + shadow_off)
    text_boxes.append((label or text, text, font, bbox, container or (0, 0, W, H)))
    return bbox


def fit_font(text, max_width, size, weight, stroke=0):
    """Shrink font size until the text fits into max_width."""
    while size > 10:
        font = load_font(size, weight)
        l, _, r, _ = font.getbbox(text, stroke_width=stroke)
        if r - l <= max_width:
            return font
        size -= 2
    return load_font(size, weight)


# ---------------------------------------------------------------- pixel helpers

def px_rect(draw, x0, y0, x1, y1, fill):
    draw.rectangle([x0, y0, x1 - 1, y1 - 1], fill=fill)


def rpg_window(draw, x0, y0, x1, y1, bg=NAVY, step=6):
    """16bit-style message window: ink / gold / cream / gold frame with notched corners."""
    s = step
    # outer ink with notched corners
    px_rect(draw, x0 + s, y0, x1 - s, y1, INK)
    px_rect(draw, x0, y0 + s, x1, y1 - s, INK)
    # gold
    px_rect(draw, x0 + 2 * s, y0 + s, x1 - 2 * s, y1 - s, GOLD_DARK)
    px_rect(draw, x0 + s, y0 + 2 * s, x1 - s, y1 - 2 * s, GOLD_DARK)
    px_rect(draw, x0 + 2 * s, y0 + s, x1 - 2 * s, y0 + 2 * s, GOLD_LIGHT)
    px_rect(draw, x0 + s, y0 + 2 * s, x0 + 2 * s, y1 - 2 * s, GOLD)
    # cream line
    px_rect(draw, x0 + 2 * s, y0 + 2 * s, x1 - 2 * s, y1 - 2 * s, CREAM)
    # inner
    px_rect(draw, x0 + 3 * s, y0 + 3 * s, x1 - 3 * s, y1 - 3 * s, INK)
    px_rect(draw, x0 + 3 * s + 3, y0 + 3 * s + 3, x1 - 3 * s - 3, y1 - 3 * s - 3, bg)
    # dithered gradient at the bottom of the window for depth
    iy0 = y0 + 3 * s + 3
    iy1 = y1 - 3 * s - 3
    for yy in range(iy0, iy1, 6):
        t = (yy - iy0) / max(1, iy1 - iy0)
        if t < 0.78:
            continue
        for xx in range(x0 + 3 * s + 3, x1 - 3 * s - 3, 6):
            if ((xx // 6) + (yy // 6)) % 2 == 0 or t > 0.9:
                px_rect(draw, xx, yy, min(xx + 6, x1 - 3 * s - 3), min(yy + 6, iy1), NAVY_DEEP)
    return (x0 + 3 * s + 3, y0 + 3 * s + 3, x1 - 3 * s - 3, y1 - 3 * s - 3)


# ---------------------------------------------------------------- background

STAR_KEEP_OUT = [(40, 40, 1040, 120), (40, 130, 1040, 710), (540, 710, 1040, 1000)]


def in_keep_out(x, y):
    return any(x0 - 12 <= x <= x1 + 12 and y0 - 12 <= y <= y1 + 12 for x0, y0, x1, y1 in STAR_KEEP_OUT)


def draw_background(img, draw, horizon):
    # night sky in banded steps (no smooth gradient → retro look)
    bands = [NAVY_DEEP, (12, 22, 54), (14, 26, 62), NAVY, (22, 38, 82), (28, 46, 96)]
    band_h = horizon / len(bands)
    for i, c in enumerate(bands):
        px_rect(draw, 0, int(i * band_h), W, int((i + 1) * band_h) + 1, c)
    # dither between bands
    for i in range(1, len(bands)):
        y = int(i * band_h)
        for x in range(0, W, 12):
            px_rect(draw, x + (6 if (x // 12) % 2 else 0), y - 6, x + (6 if (x // 12) % 2 else 0) + 6, y, bands[i])

    rnd = random.Random(7)
    for _ in range(70):
        x = rnd.randrange(0, W // 6) * 6
        y = rnd.randrange(0, int(horizon - 40) // 6) * 6
        c = rnd.choice([CREAM, CREAM, GOLD_LIGHT, NAVY_LIGHT])
        if in_keep_out(x, y):
            continue
        px_rect(draw, x, y, x + 6, y + 6, c)
    for (x, y) in [(500, 1000), (1010, 1030), (120, 720), (30, 400)]:
        px_rect(draw, x, y - 12, x + 6, y + 18, GOLD_LIGHT)
        px_rect(draw, x - 12, y, x + 18, y + 6, GOLD_LIGHT)
        px_rect(draw, x, y, x + 6, y + 6, CREAM)

    # distant hills
    for x in range(0, W, 12):
        h = int(40 + 26 * math.sin(x / 90) + 16 * math.sin(x / 37 + 1))
        h = max(12, (h // 6) * 6)
        px_rect(draw, x, horizon - h, x + 12, horizon, GREEN_DARK)
    # grass field
    px_rect(draw, 0, horizon, W, H, GREEN)
    for y in range(horizon, H, 36):
        for x in range(0, W, 36):
            if ((x // 36) + (y // 36)) % 2 == 0:
                px_rect(draw, x, y, x + 36, y + 36, (54, 140, 66))
    px_rect(draw, 0, horizon, W, horizon + 6, GREEN_LIGHT)
    rnd = random.Random(3)
    for _ in range(80):
        x = rnd.randrange(0, W // 6) * 6
        y = rnd.randrange(horizon + 12, H - 12) // 6 * 6
        px_rect(draw, x, y, x + 6, y + 12, GREEN_LIGHT)
        px_rect(draw, x + 6, y + 6, x + 12, y + 12, GREEN_DARK)
    for _ in range(14):
        x = rnd.randrange(2, W // 6 - 2) * 6
        y = rnd.randrange(horizon + 24, H - 24) // 6 * 6
        c = rnd.choice([CREAM, GOLD_LIGHT])
        px_rect(draw, x, y - 6, x + 6, y + 12, c)
        px_rect(draw, x - 6, y, x + 12, y + 6, c)
        px_rect(draw, x, y, x + 6, y + 6, GOLD_DARK)


# ---------------------------------------------------------------- squirrel

def ellipse_cells(cx, cy, rx, ry):
    cells = set()
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1:
                cells.add((x, y))
    return cells


def outline(cells):
    out = set()
    for (x, y) in cells:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n not in cells:
                out.add(n)
    return out


def shade_layer(grid, cells, cx, cy, rx, ry, main, shade, light):
    for (x, y) in cells:
        u = (x + 0.5 - cx) / rx
        v = (y + 0.5 - cy) / ry
        if u * 0.6 + v * 0.8 > 0.55:
            grid[(x, y)] = shade
        elif u * 0.6 + v * 0.8 < -0.6:
            grid[(x, y)] = light
        else:
            grid[(x, y)] = main


def build_squirrel():
    """Return {(x, y): color} pixel grid of a hungry, troubled squirrel."""
    grid = {}

    def put_layer(cells, painter):
        for c in outline(cells):
            grid[c] = SQ_OUT
        painter(cells)

    # --- tail (behind): stacked blobs curling up over the head
    tail_parts = [(23, 28, 6.5, 5.5), (27.5, 21, 6.5, 7), (27, 12, 6.5, 6), (22.5, 5.5, 5.5, 4.5)]
    tail = set()
    for p in tail_parts:
        tail |= ellipse_cells(*p)

    def paint_tail(cells):
        for (x, y) in cells:
            grid[(x, y)] = SQ_MAIN
        for (x, y) in cells:  # shade along the lower-left edge
            if any((x + dx, y + dy) not in cells for dx, dy in ((-1, 0), (0, 1), (-1, 1), (-2, 0))):
                grid[(x, y)] = SQ_SHADE
        for (x, y) in cells:  # fluffy highlight along the upper-right edge
            if any((x + dx, y + dy) not in cells for dx, dy in ((2, 0), (0, -2), (2, -1))) \
                    and all((x + dx, y + dy) in cells for dx, dy in ((1, 0), (0, -1))):
                grid[(x, y)] = SQ_LIGHT
        # fur tufts (short dark strokes)
        for (x, y) in [(28, 16), (29, 17), (25, 24), (26, 25), (27, 8), (28, 9), (22, 30)]:
            if (x, y) in cells:
                grid[(x, y)] = SQ_SHADE

    put_layer(tail, paint_tail)

    # --- feet
    for fx in (6, 15):
        feet = ellipse_cells(fx, 32, 3.2, 1.7)
        put_layer(feet, lambda c: [grid.__setitem__(k, SQ_SHADE) for k in c])

    # --- body
    body = ellipse_cells(10.5, 24.5, 8, 8)
    put_layer(body, lambda c: shade_layer(grid, c, 10.5, 24.5, 8, 8, SQ_MAIN, SQ_SHADE, SQ_LIGHT))
    for k in ellipse_cells(10.5, 26, 5, 5.8):
        if k in body:
            grid[k] = SQ_BELLY

    # --- ears
    ears = set()
    for (ex, flip) in ((5, 1), (16, -1)):
        for row in range(5):
            w = row // 2 + 1
            for i in range(-w, w + 1):
                ears.add((ex + i, 1 + row))
        ears.add((ex - flip, 0))  # ear tuft
    put_layer(ears, lambda c: [grid.__setitem__(k, SQ_MAIN) for k in c])
    for (ex, _) in ((5, 1), (16, -1)):
        for row in range(2, 5):
            grid[(ex, 1 + row)] = SQ_PINK

    # --- head
    head = ellipse_cells(10.5, 11, 9.5, 7)
    put_layer(head, lambda c: shade_layer(grid, c, 10.5, 11, 9.5, 7, SQ_MAIN, SQ_SHADE, SQ_LIGHT))
    for k in ellipse_cells(10.5, 14.2, 4.6, 3.4):  # muzzle
        if k in head:
            grid[k] = SQ_BELLY

    # worried eyebrows (inner ends raised)
    for k in [(5, 8), (6, 8), (7, 7), (8, 7), (13, 7), (14, 7), (15, 8), (16, 8)]:
        grid[k] = SQ_OUT
    # eyes (2x3) with highlight
    for ex in (6, 14):
        for dy in range(3):
            for dx in range(2):
                grid[(ex + dx, 10 + dy)] = SQ_EYE
        grid[(ex, 10)] = SQ_WHITE
    # tears
    for k in [(6, 13), (6, 14), (15, 13), (15, 14), (15, 15)]:
        grid[k] = SQ_TEAR
    # cheeks
    for k in [(3, 13), (4, 13), (17, 13), (18, 13)]:
        grid[k] = SQ_PINK
    # nose + wavy mouth
    for k in [(10, 13), (11, 13)]:
        grid[k] = SQ_OUT
    for k in [(9, 16), (10, 15), (11, 15), (12, 16)]:  # troubled frown
        grid[k] = SQ_OUT

    # --- arms clutching the stomach
    for ax in (7, 14):
        arm = ellipse_cells(ax, 23.5, 2.1, 3.4)
        put_layer(arm, lambda c: shade_layer(grid, c, ax, 23.5, 2.1, 3.4, SQ_MAIN, SQ_SHADE, SQ_LIGHT))
    for k in [(8, 26), (13, 26)]:  # paw tips pressing the stomach
        grid[k] = SQ_SHADE

    # --- sweat drops near the head
    for (sx, sy) in ((-2, 6), (21, 4)):
        drop = {(sx, sy), (sx, sy + 1), (sx - 1, sy + 2), (sx, sy + 2), (sx + 1, sy + 2), (sx, sy + 3)}
        for c in outline(drop):
            grid[c] = SQ_OUT
        for c in drop:
            grid[c] = SQ_TEAR
        grid[(sx, sy + 2)] = SQ_WHITE
    return grid


def draw_squirrel(img, grid, ox, oy, s):
    draw = ImageDraw.Draw(img)
    xs = [x for x, _ in grid]
    ys = [y for _, y in grid]
    minx, miny = min(xs), min(ys)
    maxx, maxy = max(xs), max(ys)
    # ground shadow
    sh_y = oy + (maxy - miny + 1) * s - s
    for i, w in enumerate((26, 22)):
        px_rect(draw, ox + (14 - w // 2 + 5) * s, sh_y + i * s - s,
                ox + (14 + w // 2 + 5) * s, sh_y + (i + 1) * s - s, GREEN_DARK)
    for (x, y), c in grid.items():
        px = ox + (x - minx) * s
        py = oy + (y - miny) * s
        px_rect(draw, px, py, px + s, py + s, c)
    return (ox, oy, ox + (maxx - minx + 1) * s, oy + (maxy - miny + 1) * s)


# ---------------------------------------------------------------- gauge

def draw_gauge(draw, x, y, w, label, ratio, color, font_label, value_text, font_value, value_color):
    bar_h = 36
    lb = draw_text(draw, (x, y + bar_h // 2), label, font_label, CREAM, anchor="lm",
                   label=f"gauge-label:{label}")
    bx0 = x + 108
    bx1 = x + w - 112
    px_rect(draw, bx0, y, bx1, y + bar_h, INK)
    px_rect(draw, bx0 + 4, y + 4, bx1 - 4, y + bar_h - 4, NAVY_DEEP)
    segs = 8
    seg_w = (bx1 - bx0 - 8 - (segs - 1) * 4) / segs
    filled = round(segs * ratio)
    for i in range(segs):
        sx0 = int(bx0 + 4 + i * (seg_w + 4))
        sx1 = int(sx0 + seg_w)
        if i < filled:
            px_rect(draw, sx0, y + 4, sx1, y + bar_h - 4, color)
            px_rect(draw, sx0, y + 4, sx1, y + 10, CREAM)
        else:
            px_rect(draw, sx0, y + 4, sx1, y + bar_h - 4, NAVY_LIGHT)
    draw_text(draw, (x + w, y + bar_h // 2), value_text, font_value, value_color, anchor="rm",
              stroke=3, stroke_fill=INK, label=f"gauge-value:{value_text}")


# ---------------------------------------------------------------- main

def main():
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    horizon = 1060
    draw_background(img, draw, horizon)

    margin = 54

    # --- top HUD: quest title
    f_quest = load_font(34, 900)
    tag = (margin, 52, margin + 260, 112)
    px_rect(draw, tag[0], tag[1], tag[2], tag[3], INK)
    px_rect(draw, tag[0] + 4, tag[1] + 4, tag[2] - 4, tag[3] - 4, GOLD)
    px_rect(draw, tag[0] + 4, tag[1] + 4, tag[2] - 4, tag[1] + 10, GOLD_LIGHT)
    draw_text(draw, ((tag[0] + tag[2]) // 2, (tag[1] + tag[3]) // 2 - 2), "QUEST 01", f_quest, INK,
              label="quest-tag", container=tag)
    f_hud = load_font(30, 700)
    draw_text(draw, (W - margin, 82), "ダイエット攻略の書", f_hud, CREAM, anchor="rm",
              shadow=NAVY_DEEP, shadow_off=4, label="hud-right")

    # --- headline window
    win = (margin, 140, W - margin, 560)
    inner = rpg_window(draw, *win)
    pad = 36
    head_max_w = inner[2] - inner[0] - pad * 2
    lines = ["減量中、空腹で", "毎回負ける人へ。"]
    f_head = None
    for line in lines:  # same size for both lines, fitted to the longer one
        f = fit_font(line, head_max_w, 112, 900, stroke=6)
        if f_head is None or f.size < f_head.size:
            f_head = f
    cx = (inner[0] + inner[2]) // 2
    line_gap = int(f_head.size * 1.32)
    top_y = (inner[1] + inner[3]) // 2 - line_gap // 2 - 4
    for i, line in enumerate(lines):
        color = CREAM if i == 0 else GOLD_LIGHT
        draw_text(draw, (cx, top_y + i * line_gap), line, f_head, color,
                  shadow=INK, shadow_off=8, stroke=6, stroke_fill=INK,
                  label=f"headline-{i + 1}", container=inner)
    # message cursor ▼
    tx, ty = inner[2] - 40, inner[3] - 30
    for r in range(3):
        px_rect(draw, tx - 18 + r * 6, ty + r * 6, tx + 18 - r * 6, ty + r * 6 + 6, GOLD)

    # --- subtitle ribbon
    rib = (margin + 40, 590, W - margin - 40, 690)
    rx0, ry0, rx1, ry1 = rib
    # ribbon tails with a V notch, drawn in 6px rows
    tail_w, drop = 54, 22
    t_y0, t_y1 = ry0 + drop, ry1 + drop
    mid = (t_y0 + t_y1) / 2
    for yy in range(t_y0, t_y1, 6):
        notch = int(max(0, 24 - abs(yy + 3 - mid) * 0.9) // 6 * 6)
        for side in (-1, 1):
            if side < 0:
                x_out, x_in = rx0 - tail_w + notch, rx0 + 6
            else:
                x_out, x_in = rx1 + tail_w - notch, rx1 - 6
            a, b = sorted((x_out, x_in))
            px_rect(draw, a, yy, b, yy + 6, INK)
            if t_y0 < yy < t_y1 - 6:
                px_rect(draw, a + 6, yy, b - 6, yy + 6, GOLD_DARK)
    px_rect(draw, rx0, ry0, rx1, ry1, INK)
    px_rect(draw, rx0 + 6, ry0 + 6, rx1 - 6, ry1 - 6, GOLD)
    px_rect(draw, rx0 + 6, ry0 + 6, rx1 - 6, ry0 + 14, GOLD_LIGHT)
    px_rect(draw, rx0 + 6, ry1 - 14, rx1 - 6, ry1 - 6, GOLD_DARK)
    sub = "食事を減らす前に変える3つ"
    rib_inner = (rx0 + 24, ry0 + 6, rx1 - 24, ry1 - 6)
    f_sub = fit_font(sub, rib_inner[2] - rib_inner[0], 58, 900)
    draw_text(draw, ((rx0 + rx1) // 2, (ry0 + ry1) // 2 - 2), sub, f_sub, NAVY_DEEP,
              label="subtitle", container=rib_inner)

    # --- squirrel
    grid = build_squirrel()
    s = 13
    sq_box = draw_squirrel(img, grid, 70, 735, s)

    # stomach growl
    f_growl = load_font(54, 900)
    draw_text(draw, (600, 1052), "グゥゥ〜…", f_growl, GOLD_LIGHT, anchor="lm",
              stroke=5, stroke_fill=INK, label="growl")

    # --- status window
    st = (556, 726, W - margin, 990)
    st_inner = rpg_window(draw, *st, step=5)
    f_name = load_font(34, 900)
    f_lab = load_font(30, 900)
    f_val = load_font(30, 900)
    sx0 = st_inner[0] + 22
    sx1 = st_inner[2] - 22
    draw_text(draw, (sx0, st_inner[1] + 34), "リス", f_name, CREAM, anchor="lm",
              label="status-name", container=st_inner)
    draw_text(draw, (sx1, st_inner[1] + 34), "Lv.1 減量中", f_lab, GOLD_LIGHT, anchor="rm",
              label="status-level", container=st_inner)
    px_rect(draw, sx0, st_inner[1] + 62, sx1, st_inner[1] + 66, NAVY_LIGHT)
    draw_gauge(draw, sx0, st_inner[1] + 104, sx1 - sx0, "やる気", 0.2, RED,
               f_lab, "ピンチ", f_val, CREAM)
    draw_gauge(draw, sx0, st_inner[1] + 174, sx1 - sx0, "空腹", 1.0, GOLD,
               f_lab, "MAX!!", load_font(32, 900), GOLD_LIGHT)

    # --- call to action
    f_cta = load_font(42, 900)
    cta = "スワイプして攻略スタート"
    cta_box = (margin + 60, 1210, W - margin - 60, 1300)
    bx0, by0, bx1, by1 = cta_box
    px_rect(draw, bx0, by0, bx1, by1, INK)
    px_rect(draw, bx0 + 5, by0 + 5, bx1 - 5, by1 - 5, NAVY)
    px_rect(draw, bx0 + 5, by0 + 5, bx1 - 5, by0 + 9, NAVY_LIGHT)
    arrow_x = bx0 + 44
    for r in range(5):
        px_rect(draw, arrow_x + r * 6, (by0 + by1) // 2 - 30 + r * 6, arrow_x + r * 6 + 6,
                (by0 + by1) // 2 + 30 - r * 6, GOLD)
    cta_inner = (arrow_x + 48, by0 + 5, bx1 - 70, by1 - 5)
    f_cta = fit_font(cta, cta_inner[2] - cta_inner[0], 42, 900)
    draw_text(draw, ((cta_inner[0] + cta_inner[2]) // 2, (by0 + by1) // 2 - 2), cta, f_cta, CREAM,
              label="cta", container=cta_inner)
    # right arrows »
    for k in range(2):
        ax = bx1 - 60 + k * 18
        for r in range(4):
            px_rect(draw, ax + r * 4, (by0 + by1) // 2 - 16 + r * 4, ax + r * 4 + 6,
                    (by0 + by1) // 2 + 16 - r * 4, GOLD_LIGHT)

    img.save(OUT_PATH)
    print(f"saved: {OUT_PATH}")
    return verify()


# ---------------------------------------------------------------- verification

def glyph_signature(font, ch):
    canvas = Image.new("L", (font.size * 2, font.size * 2), 0)
    ImageDraw.Draw(canvas).text((font.size // 2, font.size // 2), ch, font=font, fill=255)
    return canvas.tobytes()


def verify():
    """Check every text: inside its container / canvas, and no missing glyphs (tofu)."""
    ok = True
    notdef_cache = {}
    print("\n--- text check ---")
    for label, text, font, bbox, cont in text_boxes:
        problems = []
        if bbox[0] < 0 or bbox[1] < 0 or bbox[2] > W or bbox[3] > H:
            problems.append("canvas overflow")
        if bbox[0] < cont[0] or bbox[1] < cont[1] or bbox[2] > cont[2] or bbox[3] > cont[3]:
            problems.append(f"container overflow {cont}")
        key = id(font)
        if key not in notdef_cache:
            notdef_cache[key] = glyph_signature(font, "\ue000")  # unassigned PUA → .notdef
        notdef = notdef_cache[key]
        missing = [ch for ch in text if not ch.isspace() and glyph_signature(font, ch) == notdef]
        if missing:
            problems.append(f"missing glyphs {missing}")
        status = "OK " if not problems else "NG "
        ok &= not problems
        print(f"{status} {label:22s} bbox={tuple(int(v) for v in bbox)} {'; '.join(problems)}")
    print("RESULT:", "ALL OK" if ok else "PROBLEMS FOUND")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
