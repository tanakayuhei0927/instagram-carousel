"""Instagram carousel slide 05 (strategy 2) — secure protein, as a battle screen.

Usage: python3 make_slide_05.py  ->  slide_05.png (1080x1350)
"""
import random
import sys

from PIL import Image, ImageDraw

from rpg_common import (
    CREAM, GOLD, GOLD_DARK, GOLD_LIGHT, GREEN, GREEN_DARK, GREEN_LIGHT,
    INK, NAVY, NAVY_DEEP, NAVY_LIGHT, RED, ROOT, H, W,
    BOILED_EGG, DRUMSTICK, FISH, PROTEIN_COLORS, TOFU,
    build_squirrel, decor_boxes, draw_squirrel, draw_text, fit_font, load_font,
    pixel_icon, px_rect, rpg_window, verify_all,
)

OUT_PATH = ROOT / "slide_05.png"

ITEMS = [
    ("鶏肉", "焼く・蒸す・汁物に", DRUMSTICK),
    ("魚", "焼き魚や缶詰でも", FISH),
    ("卵", "ゆで卵で一品追加", BOILED_EGG),
    ("豆腐", "汁物や冷ややっこに", TOFU),
]


# ---------------------------------------------------------------- background

def draw_background(draw, keep_out):
    # night sky over the whole canvas, brighter toward the middle (battle backdrop)
    bands = [NAVY_DEEP, (12, 22, 54), (14, 26, 62), NAVY, (22, 38, 82), NAVY, (14, 26, 62), (12, 22, 54)]
    band_h = H / len(bands)
    for i, c in enumerate(bands):
        px_rect(draw, 0, int(i * band_h), W, int((i + 1) * band_h) + 1, c)
    rnd = random.Random(47)
    for _ in range(120):
        x = rnd.randrange(0, W // 6) * 6
        y = rnd.randrange(0, H // 6) * 6
        if any(x0 - 12 <= x <= x1 + 12 and y0 - 12 <= y <= y1 + 12 for x0, y0, x1, y1 in keep_out):
            continue
        px_rect(draw, x, y, x + 6, y + 6, rnd.choice([CREAM, GOLD_LIGHT, NAVY_LIGHT, NAVY_LIGHT]))


def battle_platform(draw, cx, cy, rx, ry):
    """Oval grass platform, like the ground under a monster in an RPG battle."""
    u = 6
    cells = {(x, y) for x in range(-rx, rx + 1) for y in range(-ry, ry + 1)
             if (x / rx) ** 2 + (y / ry) ** 2 <= 1}
    for (x, y) in cells:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x + dx, y + dy) not in cells:
                px_rect(draw, cx + (x + dx) * u, cy + (y + dy) * u, cx + (x + dx + 1) * u, cy + (y + dy + 1) * u, INK)
    for (x, y) in cells:
        t = (x / rx) ** 2 + (y / ry) ** 2
        c = GREEN_LIGHT if y < -ry * 0.4 and t < 0.7 else GREEN if t < 0.75 else GREEN_DARK
        px_rect(draw, cx + x * u, cy + y * u, cx + (x + 1) * u, cy + (y + 1) * u, c)


def warning_icon(draw, x0, y0, u):
    rows = [
        ".....XX.....",
        "....XYYX....",
        "....XYYX....",
        "...XYYYYX...",
        "...XYXXYX...",
        "..XYYXXYYX..",
        "..XYYXXYYX..",
        ".XYYYXXYYYX.",
        ".XYYYYYYYYX.",
        "XYYYYXXYYYYX",
        "XYYYYYYYYYYX",
        "XXXXXXXXXXXX",
    ]
    return pixel_icon(draw, rows, {"X": INK, "Y": GOLD}, x0, y0, u, name="warning-icon")


def power_lines(draw, cx, cy):
    """Short gold strokes around the squirrel for a 'let's go!' feel."""
    for (dx, dy, w, h) in ((-176, -60, 26, 6), (-170, -10, 18, 6), (136, -80, 30, 6), (146, -30, 22, 6),
                           (-110, -150, 6, 24), (96, -160, 6, 24)):
        px_rect(draw, cx + dx, cy + dy, cx + dx + w, cy + dy + h, GOLD)
        decor_boxes.append(("power-line", (cx + dx, cy + dy, cx + dx + w, cy + dy + h)))


# ---------------------------------------------------------------- main

def main():
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)
    margin = 54

    win = (margin, 500, W - margin, 1066)
    warn = (margin, 1088, W - margin, 1306)
    keep_out = [(margin, 40, W - margin, 100), (380, 110, W - margin, 470), win, warn, (40, 150, 380, 490)]
    draw_background(draw, keep_out)

    # --- top HUD (same rules as slides 02-04)
    f_tag = load_font(32, 900)
    tag = (margin, 44, margin + 250, 100)
    px_rect(draw, *tag, INK)
    px_rect(draw, tag[0] + 4, tag[1] + 4, tag[2] - 4, tag[3] - 4, GOLD)
    px_rect(draw, tag[0] + 4, tag[1] + 4, tag[2] - 4, tag[1] + 10, GOLD_LIGHT)
    draw_text(draw, ((tag[0] + tag[2]) // 2, (tag[1] + tag[3]) // 2 - 2), "STAGE 4", f_tag, INK,
              label="stage-tag", container=tag)
    draw_text(draw, (W - margin, 72), "攻略②", load_font(30, 700), CREAM, anchor="rm",
              shadow=NAVY_DEEP, shadow_off=4, label="hud-right")

    # --- squirrel on a battle platform (left), headline right-aligned (mirror of slide 04)
    plat_cx, plat_cy = 232, 456
    battle_platform(draw, plat_cx, plat_cy, 22, 4)
    grid = build_squirrel("determined", pose="fight")
    s = 8
    cols = max(x for x, _ in grid) - min(x for x, _ in grid) + 1
    rows = max(y for _, y in grid) - min(y for _, y in grid) + 1
    sq_box = draw_squirrel(img, grid, plat_cx - cols * s // 2 + 8, plat_cy - rows * s + 4, s)
    power_lines(draw, plat_cx, sq_box[1] + 150)

    lines = ["たんぱく質を", "確保！"]
    head_box = (400, 110, W - margin, 480)
    f_head = min((fit_font(l, head_box[2] - head_box[0] - 16, 100, 900, stroke=5) for l in lines),
                 key=lambda f: f.size)
    for i, line in enumerate(lines):
        draw_text(draw, (W - margin - 12, 236 + i * 128), line, f_head, CREAM if i == 0 else GOLD_LIGHT,
                  anchor="rm", shadow=INK, shadow_off=7, stroke=5, stroke_fill=INK,
                  label=f"headline-{i + 1}", container=head_box)

    # --- item window: 2x2 grid
    inner = rpg_window(draw, *win, dither=False)
    ix0, iy0, ix1, iy1 = inner
    draw_text(draw, (ix0 + 32, iy0 + 46), "攻略アイテム", load_font(40, 900), GOLD_LIGHT, anchor="lm",
              label="item-title", container=inner)
    draw_text(draw, (ix1 - 32, iy0 + 46), "毎食ひとつ取り入れよう", load_font(28, 700), CREAM,
              anchor="rm", label="item-subtitle", container=inner)
    for x in range(ix0 + 24, ix1 - 24, 12):
        px_rect(draw, x, iy0 + 88, x + 6, iy0 + 92, GOLD_DARK)

    gx0, gy0, gx1, gy1 = ix0 + 24, iy0 + 104, ix1 - 24, iy1 - 12
    cw = (gx1 - gx0) // 2
    ch = (gy1 - gy0) // 2
    slot = 112
    for i, (name, usage, icon) in enumerate(ITEMS):
        cx0 = gx0 + (i % 2) * cw
        cy0 = gy0 + (i // 2) * ch
        sx, sy = cx0 + 12, cy0 + (ch - slot) // 2
        # item slot (same frame as slide 04)
        px_rect(draw, sx, sy, sx + slot, sy + slot, INK)
        px_rect(draw, sx + 4, sy + 4, sx + slot - 4, sy + slot - 4, GOLD_DARK)
        px_rect(draw, sx + 4, sy + 4, sx + slot - 4, sy + 8, GOLD)
        px_rect(draw, sx + 10, sy + 10, sx + slot - 10, sy + slot - 10, NAVY_DEEP)
        unit = 7 if max(len(r) for r in icon) > 10 else 8
        iw, ih = max(len(r) for r in icon) * unit, len(icon) * unit
        pixel_icon(draw, icon, PROTEIN_COLORS, sx + (slot - iw) // 2, sy + (slot - ih) // 2, unit)
        decor_boxes.append(("slot", (sx, sy, sx + slot, sy + slot)))

        tx = sx + slot + 24
        cell = (cx0, cy0, cx0 + cw - 8, cy0 + ch)
        f_name = fit_font(name, cell[2] - tx, 44, 900)
        draw_text(draw, (tx, sy + 32), name, f_name, CREAM, anchor="lm", label=f"item-{i + 1}-name", container=cell)
        f_use = fit_font(usage, cell[2] - tx, 30, 500)
        draw_text(draw, (tx, sy + 84), usage, f_use, CREAM, anchor="lm", label=f"item-{i + 1}-usage", container=cell)
    for y in range(gy0, gy1, 12):  # dotted grid lines
        px_rect(draw, gx0 + cw - 2, y, gx0 + cw + 2, y + 6, NAVY_LIGHT)
    for x in range(gx0, gx1, 12):
        px_rect(draw, x, gy0 + ch - 2, x + 6, gy0 + ch + 2, NAVY_LIGHT)

    # --- caution window
    wi = rpg_window(draw, *warn, dither=False)
    warning_icon(draw, wi[0] + 28, (wi[1] + wi[3]) // 2 - 42, 7)
    tx = wi[0] + 28 + 84 + 28
    pill_font = load_font(26, 900)
    px_rect(draw, tx, wi[1] + 16, tx + 92, wi[1] + 56, INK)
    px_rect(draw, tx + 4, wi[1] + 20, tx + 88, wi[1] + 52, RED)
    draw_text(draw, (tx + 46, wi[1] + 35), "注意", pill_font, CREAM, label="warn-pill",
              container=(tx + 4, wi[1] + 20, tx + 88, wi[1] + 52))
    l1 = "野菜だけでは、たんぱく質は十分に取れません。"
    l2 = "野菜とたんぱく質を、組み合わせて食べよう。"
    f1 = fit_font(l1, wi[2] - 24 - tx, 34, 900)
    f2 = fit_font(l2, wi[2] - 24 - tx, 30, 500)
    draw_text(draw, (tx, wi[1] + 98), l1, f1, CREAM, anchor="lm", label="warn-1", container=wi)
    draw_text(draw, (tx, wi[1] + 146), l2, f2, CREAM, anchor="lm", label="warn-2", container=wi)

    img.save(OUT_PATH)
    print(f"saved: {OUT_PATH}")
    return verify_all()


if __name__ == "__main__":
    sys.exit(main())
