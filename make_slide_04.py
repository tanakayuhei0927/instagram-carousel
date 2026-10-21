"""Instagram carousel slide 04 (strategy 1) — vegetables & mushrooms as items.

Usage: python3 make_slide_04.py  ->  slide_04.png (1080x1350)
"""
import math
import random
import sys

from PIL import Image, ImageDraw

from rpg_common import (
    CREAM, GOLD, GOLD_DARK, GOLD_LIGHT, GREEN, GREEN_DARK, GREEN_LIGHT,
    INK, NAVY, NAVY_DEEP, NAVY_LIGHT, ROOT, H, W,
    BROCCOLI, BULB, CABBAGE, ICON_COLORS, SHIITAKE_ICON, TOMATO, VEG_COLORS,
    build_squirrel, decor_boxes, draw_squirrel, draw_text, fit_font, load_font,
    pixel_icon, px_rect, rpg_window, verify_all,
)

OUT_PATH = ROOT / "slide_04.png"

ITEMS = [
    ("キャベツ", "汁物やサラダに、ざく切りでたっぷり", CABBAGE),
    ("ブロッコリー", "ゆでて付け合わせに、スープの具にも", BROCCOLI),
    ("きのこ", "スープや炒め物に、数種類を混ぜても", SHIITAKE_ICON),
    ("トマト", "サラダや付け合わせで、彩りもプラス", TOMATO),
]


# ---------------------------------------------------------------- background

def draw_background(draw, horizon, keep_out):
    bands = [NAVY_DEEP, (12, 22, 54), (14, 26, 62), NAVY, (22, 38, 82)]
    band_h = horizon / len(bands)
    for i, c in enumerate(bands):
        px_rect(draw, 0, int(i * band_h), W, int((i + 1) * band_h) + 1, c)
    rnd = random.Random(31)
    for _ in range(60):
        x = rnd.randrange(0, W // 6) * 6
        y = rnd.randrange(0, (horizon - 60) // 6) * 6
        if any(x0 - 12 <= x <= x1 + 12 and y0 - 12 <= y <= y1 + 12 for x0, y0, x1, y1 in keep_out):
            continue
        px_rect(draw, x, y, x + 6, y + 6, rnd.choice([CREAM, GOLD_LIGHT, NAVY_LIGHT]))

    # rolling hills + field below the horizon (the item window opens over it)
    for x in range(0, W, 12):
        h = max(12, int(30 + 20 * math.sin(x / 70 + 2) + 10 * math.sin(x / 23)) // 6 * 6)
        px_rect(draw, x, horizon - h, x + 12, horizon, GREEN_DARK)
    px_rect(draw, 0, horizon, W, H, GREEN)
    for y in range(horizon, H, 36):
        for x in range(0, W, 36):
            if ((x // 36) + (y // 36)) % 2 == 0:
                px_rect(draw, x, y, x + 36, y + 36, (54, 140, 66))
    px_rect(draw, 0, horizon, W, horizon + 6, GREEN_LIGHT)
    for _ in range(40):
        x = rnd.randrange(0, W // 6) * 6
        y = rnd.randrange(horizon + 12, H - 12) // 6 * 6
        px_rect(draw, x, y, x + 6, y + 12, GREEN_LIGHT)
        px_rect(draw, x + 6, y + 6, x + 12, y + 12, GREEN_DARK)


def sparkle(draw, cx, cy, size, color=GOLD_LIGHT):
    u = 6
    px_rect(draw, cx - u // 2, cy - size * u, cx + u // 2, cy + size * u, color)
    px_rect(draw, cx - size * u, cy - u // 2, cx + size * u, cy + u // 2, color)
    px_rect(draw, cx - u // 2, cy - u // 2, cx + u // 2, cy + u // 2, (255, 255, 255))
    decor_boxes.append(("sparkle", (cx - size * u, cy - size * u, cx + size * u, cy + size * u)))


def item_slot(draw, x0, y0, size, icon, unit):
    """Inventory slot: ink / gold frame with a dark well and the icon centered."""
    px_rect(draw, x0, y0, x0 + size, y0 + size, INK)
    px_rect(draw, x0 + 4, y0 + 4, x0 + size - 4, y0 + size - 4, GOLD_DARK)
    px_rect(draw, x0 + 4, y0 + 4, x0 + size - 4, y0 + 8, GOLD)
    px_rect(draw, x0 + 10, y0 + 10, x0 + size - 10, y0 + size - 10, NAVY_DEEP)
    iw = max(len(r) for r in icon) * unit
    ih = len(icon) * unit
    pixel_icon(draw, icon, VEG_COLORS, x0 + (size - iw) // 2, y0 + (size - ih) // 2, unit)
    decor_boxes.append(("slot", (x0, y0, x0 + size, y0 + size)))


# ---------------------------------------------------------------- main

def main():
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)
    margin = 54
    horizon = 486

    win = (margin, 520, W - margin, 1300)
    keep_out = [(margin, 40, 700, 420), (700, 40, W - margin, 110), (680, 110, W, horizon)]
    draw_background(draw, horizon, keep_out)

    # --- top HUD (same rules as slides 02-03)
    f_tag = load_font(32, 900)
    tag = (margin, 44, margin + 250, 100)
    px_rect(draw, *tag, INK)
    px_rect(draw, tag[0] + 4, tag[1] + 4, tag[2] - 4, tag[3] - 4, GOLD)
    px_rect(draw, tag[0] + 4, tag[1] + 4, tag[2] - 4, tag[1] + 10, GOLD_LIGHT)
    draw_text(draw, ((tag[0] + tag[2]) // 2, (tag[1] + tag[3]) // 2 - 2), "STAGE 3", f_tag, INK,
              label="stage-tag", container=tag)
    draw_text(draw, (W - margin, 72), "攻略①", load_font(30, 700), CREAM, anchor="rm",
              shadow=NAVY_DEEP, shadow_off=4, label="hud-right")

    # --- headline on the left, squirrel on the right of the sky
    lines = ["野菜・きのこを", "活用！"]
    head_w = 660 - margin
    f_head = min((fit_font(l, head_w, 100, 900, stroke=5) for l in lines), key=lambda f: f.size)
    for i, line in enumerate(lines):
        draw_text(draw, (margin + 8, 208 + i * 128), line, f_head, CREAM if i == 0 else GOLD_LIGHT,
                  anchor="lm", shadow=INK, shadow_off=7, stroke=5, stroke_fill=INK,
                  label=f"headline-{i + 1}", container=(margin, 110, 680, horizon))

    # --- squirrel: inspired, holding a cabbage
    grid = build_squirrel("inspired", pose="hold", item=CABBAGE, item_colors=VEG_COLORS)
    s = 8
    cols = max(x for x, _ in grid) - min(x for x, _ in grid) + 1
    rows = max(y for _, y in grid) - min(y for _, y in grid) + 1
    col_cx = 866
    sq_box = draw_squirrel(img, grid, col_cx - cols * s // 2, horizon + 18 - rows * s, s)
    head_cx = sq_box[0] + 11 * s  # head center column of the grid
    pixel_icon(draw, BULB, ICON_COLORS, head_cx - 36, sq_box[1] - 96, 8, name="bulb")
    for (x0, y0, x1, y1) in ((-76, -70, -52, -62), (52, -70, 76, -62), (-4, -128, 4, -106)):
        px_rect(draw, head_cx + x0, sq_box[1] + y0, head_cx + x1, sq_box[1] + y1, GOLD)
    sparkle(draw, sq_box[0] - 10, sq_box[1] + 70, 2)
    sparkle(draw, sq_box[0] + 12 * s + 96, sq_box[1] - 30, 2, CREAM)

    # --- item window (RPG inventory)
    inner = rpg_window(draw, *win, dither=False)
    ix0, iy0, ix1, iy1 = inner
    draw_text(draw, (ix0 + 32, iy0 + 46), "攻略アイテム", load_font(40, 900), GOLD_LIGHT, anchor="lm",
              label="item-title", container=inner)
    draw_text(draw, (ix1 - 32, iy0 + 46), "食事に取り入れてみよう", load_font(28, 700), CREAM,
              anchor="rm", label="item-subtitle", container=inner)
    for x in range(ix0 + 24, ix1 - 24, 12):
        px_rect(draw, x, iy0 + 88, x + 6, iy0 + 92, GOLD_DARK)

    slot = 112
    rows_top = iy0 + 112
    row_h = (iy1 - 12 - rows_top) // len(ITEMS)
    slot_x = ix0 + 60
    text_x = slot_x + slot + 32
    for i, (name, usage, icon) in enumerate(ITEMS):
        ry = rows_top + i * row_h
        sy = ry + (row_h - slot) // 2
        item_slot(draw, slot_x, sy, slot, icon, 9)
        if i == 0:  # selection cursor, like an RPG menu
            for r in range(4):
                px_rect(draw, ix0 + 18 + r * 5, sy + slot // 2 - 18 + r * 5, ix0 + 24 + r * 5,
                        sy + slot // 2 + 18 - r * 5, GOLD)
            decor_boxes.append(("cursor", (ix0 + 18, sy + slot // 2 - 18, ix0 + 44, sy + slot // 2 + 18)))
        f_name = fit_font(name, ix1 - 32 - text_x, 42, 900)
        draw_text(draw, (text_x, sy + 30), name, f_name, CREAM, anchor="lm",
                  label=f"item-{i + 1}-name", container=inner)
        f_use = fit_font(usage, ix1 - 32 - text_x, 32, 500)
        draw_text(draw, (text_x, sy + 84), usage, f_use, CREAM, anchor="lm",
                  label=f"item-{i + 1}-usage", container=inner)
        if i < len(ITEMS) - 1:
            ly = ry + row_h
            for x in range(slot_x, ix1 - 32, 12):
                px_rect(draw, x, ly - 2, x + 6, ly + 2, NAVY_LIGHT)

    img.save(OUT_PATH)
    print(f"saved: {OUT_PATH}")
    return verify_all()


if __name__ == "__main__":
    sys.exit(main())
