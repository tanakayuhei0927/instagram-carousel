"""Instagram carousel slide 03 (basics) — hint screen: build meals by combination.

Usage: python3 make_slide_03.py  ->  slide_03.png (1080x1350)
"""
import random
import sys

from PIL import Image, ImageDraw

from rpg_common import (
    CREAM, GOLD, GOLD_DARK, GOLD_LIGHT, GREEN, GREEN_DARK, GREEN_LIGHT,
    INK, NAVY, NAVY_DEEP, NAVY_LIGHT, RED, ROOT, H, W,
    build_squirrel, draw_squirrel, draw_text, fit_font, load_font, number_badge,
    pixel_icon, px_rect, rpg_window, verify_all,
)

OUT_PATH = ROOT / "slide_03.png"

NORI = (24, 52, 36)
ICON_COLORS = {"X": INK, "C": CREAM, "R": RED, "Y": GOLD, "L": GOLD_LIGHT, "G": NORI,
               "D": GOLD_DARK, "W": (255, 255, 255)}

MUSHROOM = [
    "...XXXX...",
    ".XXRRRRXX.",
    "XRRCRRRRRX",
    "XRRRRRCRRX",
    "XXXXXXXXXX",
    "...XCCX...",
    "...XCCX...",
    "...XXXX...",
]
EGG = [
    "..XXXXX...",
    ".XCCCCCXX.",
    "XCCCYYCCCX",
    "XCCYLYYCCX",
    "XCCYYYYCX.",
    ".XCCYYCCX.",
    "..XCCCCX..",
    "...XXXX...",
]
ONIGIRI = [
    "....XX....",
    "...XCCX...",
    "..XCCCCX..",
    ".XCCCCCCX.",
    "XCCCCCCCCX",
    "XCCGGGGCCX",
    "XCCGGGGCCX",
    ".XXXXXXXX.",
]
BULB = [
    "..XXXXX..",
    ".XLLYYYX.",
    "XLWYYYYYX",
    "XLYYYYYYX",
    "XYYYYYYYX",
    ".XYYYYYX.",
    "..XDDDX..",
    "..XCCCX..",
    "...XXX...",
]

HINTS = [
    ("野菜やきのこで量を増やす", ["かさが増えて、お皿の満足感アップ。", "スープや炒め物に足すだけでもOK。"], MUSHROOM),
    ("たんぱく質で満足感を支える", ["肉・魚・卵・大豆製品を毎食ひとつ。", "食べごたえが出やすくなる。"], EGG),
    ("主食も必要量を確保する", ["ごはんやパンを抜きすぎないのがコツ。", "エネルギー切れを防いで続けやすく。"], ONIGIRI),
]


# ---------------------------------------------------------------- background

def draw_background(draw, keep_out, ledge_top, ledge_x):
    # banded night sky over the whole canvas (same tones as slides 01-02)
    bands = [NAVY_DEEP, (12, 22, 54), (14, 26, 62), NAVY, (22, 38, 82), NAVY, (14, 26, 62)]
    band_h = H / len(bands)
    for i, c in enumerate(bands):
        px_rect(draw, 0, int(i * band_h), W, int((i + 1) * band_h) + 1, c)

    rnd = random.Random(23)
    for _ in range(110):
        x = rnd.randrange(0, W // 6) * 6
        y = rnd.randrange(0, H // 6) * 6
        if any(x0 - 12 <= x <= x1 + 12 and y0 - 12 <= y <= y1 + 12 for x0, y0, x1, y1 in keep_out):
            continue
        px_rect(draw, x, y, x + 6, y + 6, rnd.choice([CREAM, GOLD_LIGHT, NAVY_LIGHT, NAVY_LIGHT]))

    # grass cliff on the right where the squirrel stands
    x0 = ledge_x
    px_rect(draw, x0, ledge_top, W, H, INK)
    px_rect(draw, x0 + 6, ledge_top + 6, W, H, GREEN_DARK)
    for y in range(ledge_top + 36, H, 36):
        for x in range(x0 + 6, W, 36):
            if ((x // 36) + (y // 36)) % 2 == 0:
                px_rect(draw, x, y, min(x + 36, W), min(y + 36, H), (36, 104, 56))
    px_rect(draw, x0 + 6, ledge_top + 6, W, ledge_top + 30, GREEN)
    px_rect(draw, x0 + 6, ledge_top + 6, W, ledge_top + 12, GREEN_LIGHT)
    for x in range(x0 + 12, W, 30):  # grass fringe hanging over the edge
        px_rect(draw, x, ledge_top + 30, x + 12, ledge_top + 42, GREEN)
        px_rect(draw, x, ledge_top + 42, x + 12, ledge_top + 48, INK)
    for _ in range(18):
        x = rnd.randrange((x0 + 18) // 6, (W - 18) // 6) * 6
        y = rnd.randrange((ledge_top + 60) // 6, (H - 18) // 6) * 6
        px_rect(draw, x, y, x + 6, y + 12, GREEN)
    for x in (x0 + 36, W - 60):
        px_rect(draw, x, ledge_top - 6, x + 6, ledge_top + 12, CREAM)
        px_rect(draw, x - 6, ledge_top, x + 12, ledge_top + 6, CREAM)
        px_rect(draw, x, ledge_top, x + 6, ledge_top + 6, GOLD)


def thought_bubble(draw, cx, cy, r):
    """Pixel cloud bubble with a light bulb, plus small dots trailing down-left."""
    u = 6
    cells = set()
    for (bx, by, br) in ((0, 0, r), (-r * 0.55, 2, r * 0.75), (r * 0.55, 2, r * 0.75), (0, -r * 0.35, r * 0.8)):
        for y in range(-r - 2, r + 3):
            for x in range(-2 * r, 2 * r + 1):
                if ((x - bx) / (br * 1.25)) ** 2 + ((y - by) / br) ** 2 <= 1:
                    cells.add((x, y))
    for (x, y) in cells:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x + dx, y + dy) not in cells:
                px_rect(draw, cx + (x + dx) * u, cy + (y + dy) * u, cx + (x + dx + 1) * u,
                        cy + (y + dy + 1) * u, INK)
    for (x, y) in cells:
        px_rect(draw, cx + x * u, cy + y * u, cx + (x + 1) * u, cy + (y + 1) * u, CREAM)
    xs = [x for x, _ in cells]
    ys = [y for _, y in cells]
    rect = (cx + (min(xs) - 1) * u, cy + (min(ys) - 1) * u, cx + (max(xs) + 2) * u, cy + (max(ys) + 2) * u)
    pixel_icon(draw, BULB, ICON_COLORS, cx - 27 + u // 2, cy - 30, 6, name="bulb")
    # rays
    for (x0, y0, x1, y1) in ((-48, -30, -36, -24), (42, -30, 54, -24), (-6, -54, 0, -42)):
        px_rect(draw, cx + x0 + 3, cy + y0, cx + x1 + 3, cy + y1, GOLD)
    return rect


# ---------------------------------------------------------------- main

def main():
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)
    margin = 54

    win = (margin, 384, 772, 1180)
    ledge_top, ledge_x = 1052, 790
    footer_y = 1262
    keep_out = [(margin, 40, W - margin, 350), win, (margin, footer_y - 30, 772, footer_y + 30),
                (790, 520, W, 1052)]
    draw_background(draw, keep_out, ledge_top, ledge_x)

    # --- top HUD (same rules as slide 02)
    f_tag = load_font(32, 900)
    tag = (margin, 44, margin + 250, 100)
    px_rect(draw, *tag, INK)
    px_rect(draw, tag[0] + 4, tag[1] + 4, tag[2] - 4, tag[3] - 4, GOLD)
    px_rect(draw, tag[0] + 4, tag[1] + 4, tag[2] - 4, tag[1] + 10, GOLD_LIGHT)
    draw_text(draw, ((tag[0] + tag[2]) // 2, (tag[1] + tag[3]) // 2 - 2), "STAGE 2", f_tag, INK,
              label="stage-tag", container=tag)
    draw_text(draw, (W - margin, 72), "攻略の基本", load_font(30, 700), CREAM, anchor="rm",
              shadow=NAVY_DEEP, shadow_off=4, label="hud-right")

    # --- headline, left aligned this time
    lines = ["攻略のカギは、", "食事の組み合わせ！"]
    f_head = min((fit_font(l, W - margin * 2 - 16, 92, 900, stroke=5) for l in lines), key=lambda f: f.size)
    for i, line in enumerate(lines):
        draw_text(draw, (margin + 4, 182 + i * 116), line, f_head, CREAM if i == 0 else GOLD_LIGHT,
                  anchor="lm", shadow=INK, shadow_off=7, stroke=5, stroke_fill=INK, label=f"headline-{i + 1}")

    # --- hint window (game "tips" screen)
    inner = rpg_window(draw, *win, dither=False)
    ix0, iy0, ix1, iy1 = inner
    pixel_icon(draw, BULB, ICON_COLORS, ix0 + 26, iy0 + 20, 5, name="title-bulb")
    draw_text(draw, (ix0 + 84, iy0 + 46), "攻略ヒント", load_font(40, 900), GOLD_LIGHT, anchor="lm",
              label="hint-title", container=inner)
    for x in range(ix0 + 24, ix1 - 24, 12):
        px_rect(draw, x, iy0 + 88, x + 6, iy0 + 92, GOLD_DARK)

    badge_font = load_font(30, 900)
    entry_top = iy0 + 116
    entry_h = (iy1 - 16 - entry_top) // 3
    text_x = ix0 + 92
    icon_unit = 6
    icon_x = ix1 - 24 - 10 * icon_unit
    for i, (title, desc, icon) in enumerate(HINTS):
        ey = entry_top + i * entry_h
        number_badge(draw, ix0 + 24, ey, i + 1, badge_font)
        pixel_icon(draw, icon, ICON_COLORS, icon_x, ey + 2, icon_unit, name=f"icon-{i + 1}")
        f_title = fit_font(title, icon_x - 18 - text_x, 40, 900)
        draw_text(draw, (text_x, ey + 26), title, f_title, CREAM, anchor="lm",
                  label=f"hint-{i + 1}-title", container=inner)
        for j, line in enumerate(desc):
            f_desc = fit_font(line, ix1 - 24 - text_x, 31, 500)
            draw_text(draw, (text_x, ey + 92 + j * 48), line, f_desc, CREAM, anchor="lm",
                      label=f"hint-{i + 1}-desc-{j + 1}", container=inner)
        if i < len(HINTS) - 1:
            sy = ey + entry_h - 18
            for x in range(text_x, ix1 - 24, 12):
                px_rect(draw, x, sy, x + 6, sy + 4, NAVY_LIGHT)

    # --- squirrel standing beside the hint window, thinking
    grid = build_squirrel("thinking", pose="think")
    s = 7
    cols = max(x for x, _ in grid) - min(x for x, _ in grid) + 1
    rows = max(y for _, y in grid) - min(y for _, y in grid) + 1
    col_cx = (ledge_x + W) // 2
    sq_box = draw_squirrel(img, grid, col_cx - cols * s // 2, ledge_top + 6 - rows * s, s)
    bubble_cy = sq_box[1] - 140
    thought_bubble(draw, col_cx - 6, bubble_cy, 9)
    for (x, y, size) in ((col_cx - 20, sq_box[1] - 62, 18), (col_cx - 38, sq_box[1] - 30, 12)):
        px_rect(draw, x - 4, y - 4, x + size + 4, y + size + 4, INK)
        px_rect(draw, x, y, x + size, y + size, CREAM)

    # --- footer note
    note = "※ 必要な量は、体格や活動量によって人それぞれです。"
    f_note = fit_font(note, 772 - margin, 28, 700)
    draw_text(draw, (margin + 4, footer_y), note, f_note, CREAM, anchor="lm",
              label="footer-note", container=(margin, footer_y - 30, 772, footer_y + 30))

    img.save(OUT_PATH)
    print(f"saved: {OUT_PATH}")
    return verify_all(allowed={("hint-title", "title-bulb")})


if __name__ == "__main__":
    sys.exit(main())
