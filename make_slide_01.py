"""Instagram carousel slide 01 (cover) — retro 16bit RPG diet guide.

Usage: python3 make_slide_01.py  ->  slide_01.png (1080x1350)
"""
import math
import random
import sys

from PIL import Image, ImageDraw

from rpg_common import (
    CREAM, GOLD, GOLD_DARK, GOLD_LIGHT, GREEN, GREEN_DARK, GREEN_LIGHT, INK, NAVY, NAVY_DEEP,
    NAVY_LIGHT, RED, ROOT, H, W,
    build_squirrel, draw_squirrel, draw_text, fit_font, load_font, px_rect, rpg_window, verify_all,
)

OUT_PATH = ROOT / "slide_01.png"


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
    return verify_all()


if __name__ == "__main__":
    sys.exit(main())
