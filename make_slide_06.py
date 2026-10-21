"""Instagram carousel slide 06 (strategy 3) — keep the staple food, item cards + dialog.

Usage: python3 make_slide_06.py  ->  slide_06.png (1080x1350)
"""
import math
import random
import sys

from PIL import Image, ImageDraw

from rpg_common import (
    CREAM, GOLD, GOLD_DARK, GOLD_LIGHT, GREEN, GREEN_DARK, GREEN_LIGHT,
    INK, NAVY, NAVY_DEEP, NAVY_LIGHT, ROOT, H, W,
    BREAD, ICON_COLORS, NOODLES, ONIGIRI, RICE_BOWL, STAPLE_COLORS, SWEET_POTATO_ICON,
    build_squirrel, decor_boxes, draw_squirrel, draw_text, fit_font, load_font,
    pixel_icon, px_rect, rpg_window, verify_all,
)

OUT_PATH = ROOT / "slide_06.png"

ITEMS = [
    ("ごはん", ["おにぎりや", "丼ものに"], RICE_BOWL),
    ("パン", ["具だくさん", "サンドに"], BREAD),
    ("めん類", ["野菜や卵を", "のせて"], NOODLES),
    ("いも類", ["主食の", "代わりにも"], SWEET_POTATO_ICON),
]
DIALOG = [
    "主食をゼロにすると、エネルギーが切れて",
    "続けにくくなりがち。",
    "量を調整しながら、毎食とるのがコツ！",
]


# ---------------------------------------------------------------- background

def draw_background(draw, horizon, keep_out):
    bands = [NAVY_DEEP, (12, 22, 54), (14, 26, 62), NAVY, (22, 38, 82), (28, 46, 96)]
    band_h = horizon / len(bands)
    for i, c in enumerate(bands):
        px_rect(draw, 0, int(i * band_h), W, int((i + 1) * band_h) + 1, c)
    rnd = random.Random(59)
    for _ in range(90):
        x = rnd.randrange(0, W // 6) * 6
        y = rnd.randrange(0, (horizon - 30) // 6) * 6
        if any(x0 - 12 <= x <= x1 + 12 and y0 - 12 <= y <= y1 + 12 for x0, y0, x1, y1 in keep_out):
            continue
        px_rect(draw, x, y, x + 6, y + 6, rnd.choice([CREAM, GOLD_LIGHT, NAVY_LIGHT]))
    # low hills and a meadow at the bottom where the squirrel stands
    for x in range(0, W, 12):
        h = max(12, int(36 + 22 * math.sin(x / 80 + 4) + 10 * math.sin(x / 29)) // 6 * 6)
        px_rect(draw, x, horizon - h, x + 12, horizon, GREEN_DARK)
    px_rect(draw, 0, horizon, W, H, GREEN)
    for y in range(horizon, H, 36):
        for x in range(0, W, 36):
            if ((x // 36) + (y // 36)) % 2 == 0:
                px_rect(draw, x, y, x + 36, y + 36, (54, 140, 66))
    px_rect(draw, 0, horizon, W, horizon + 6, GREEN_LIGHT)
    for _ in range(30):
        x = rnd.randrange(0, W // 6) * 6
        y = rnd.randrange(horizon + 12, H - 12) // 6 * 6
        px_rect(draw, x, y, x + 6, y + 12, GREEN_LIGHT)
        px_rect(draw, x + 6, y + 6, x + 12, y + 12, GREEN_DARK)


def item_card(draw, box, idx, name, usage, icon):
    inner = rpg_window(draw, *box, step=5, dither=False)
    ix0, iy0, ix1, iy1 = inner
    slot = 104
    sx, sy = (ix0 + ix1) // 2 - slot // 2, iy0 + 14
    px_rect(draw, sx, sy, sx + slot, sy + slot, INK)
    px_rect(draw, sx + 4, sy + 4, sx + slot - 4, sy + slot - 4, GOLD_DARK)
    px_rect(draw, sx + 4, sy + 4, sx + slot - 4, sy + 8, GOLD)
    px_rect(draw, sx + 10, sy + 10, sx + slot - 10, sy + slot - 10, NAVY_DEEP)
    unit = 7
    iw, ih = max(len(r) for r in icon) * unit, len(icon) * unit
    pixel_icon(draw, icon, STAPLE_COLORS, sx + (slot - iw) // 2, sy + (slot - ih) // 2, unit)
    decor_boxes.append(("slot", (sx, sy, sx + slot, sy + slot)))
    cx = (ix0 + ix1) // 2
    max_w = ix1 - ix0 - 16
    draw_text(draw, (cx, sy + slot + 40), name, fit_font(name, max_w, 38, 900), GOLD_LIGHT,
              label=f"item-{idx + 1}-name", container=inner)
    for j, line in enumerate(usage):
        draw_text(draw, (cx, sy + slot + 92 + j * 38), line, fit_font(line, max_w, 28, 500), CREAM,
                  label=f"item-{idx + 1}-usage-{j + 1}", container=inner)


def speech_tail(draw, cx, y_top, rows=8):
    """Stepped tail under the dialog window, pointing down to the speaker."""
    for k in range(rows):
        w = max(0, 30 - k * 3)
        y = y_top + k * 6
        px_rect(draw, cx - w - 6, y, cx + w + 6, y + 6, INK)
        if w > 0:
            px_rect(draw, cx - w - 3, y, cx + w + 3, y + 6, GOLD)
        if w > 3:
            px_rect(draw, cx - w + 3, y, cx + w - 3, y + 6, NAVY)
    decor_boxes.append(("speech-tail", (cx - 36, y_top + 30, cx + 36, y_top + rows * 6)))


# ---------------------------------------------------------------- main

def main():
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)
    margin = 54
    horizon = 980

    cards_y = (282, 600)
    dialog = (margin, 636, W - margin, 926)
    note = (390, 1034, W - margin, 1296)
    keep_out = [(margin, 40, W - margin, 250), (margin, cards_y[0], W - margin, cards_y[1]), dialog]
    draw_background(draw, horizon, keep_out)

    # --- top HUD (same rules as slides 02-05)
    f_tag = load_font(32, 900)
    tag = (margin, 44, margin + 250, 100)
    px_rect(draw, *tag, INK)
    px_rect(draw, tag[0] + 4, tag[1] + 4, tag[2] - 4, tag[3] - 4, GOLD)
    px_rect(draw, tag[0] + 4, tag[1] + 4, tag[2] - 4, tag[1] + 10, GOLD_LIGHT)
    draw_text(draw, ((tag[0] + tag[2]) // 2, (tag[1] + tag[3]) // 2 - 2), "STAGE 5", f_tag, INK,
              label="stage-tag", container=tag)
    draw_text(draw, (W - margin, 72), "攻略③", load_font(30, 700), CREAM, anchor="rm",
              shadow=NAVY_DEEP, shadow_off=4, label="hud-right")

    # --- headline: one centered line
    head = "主食も必要量を確保！"
    f_head = fit_font(head, W - margin * 2 - 16, 96, 900, stroke=5)
    draw_text(draw, (W // 2, 186), head, f_head, GOLD_LIGHT, shadow=INK, shadow_off=7, stroke=5,
              stroke_fill=INK, label="headline")

    # --- four item cards in a row
    gap = 16
    cw = (W - margin * 2 - gap * 3) // 4
    for i, (name, usage, icon) in enumerate(ITEMS):
        x0 = margin + i * (cw + gap)
        item_card(draw, (x0, cards_y[0], x0 + cw, cards_y[1]), i, name, usage, icon)

    # --- dialog window: the squirrel explains why
    di = rpg_window(draw, *dialog, dither=False)
    px_rect(draw, di[0] + 24, di[1] + 18, di[0] + 124, di[1] + 62, INK)
    px_rect(draw, di[0] + 28, di[1] + 22, di[0] + 120, di[1] + 58, GOLD)
    draw_text(draw, (di[0] + 74, di[1] + 39), "リス", load_font(28, 900), INK, label="speaker",
              container=(di[0] + 28, di[1] + 22, di[0] + 120, di[1] + 58))
    f_dlg = min((fit_font(l, di[2] - di[0] - 64, 34, 700) for l in DIALOG), key=lambda f: f.size)
    for j, line in enumerate(DIALOG):
        draw_text(draw, (di[0] + 32, di[1] + 106 + j * 50), line, f_dlg, CREAM, anchor="lm",
                  label=f"dialog-{j + 1}", container=di)

    # --- squirrel (speaker) on the meadow, happy with an onigiri
    grid = build_squirrel("happy", pose="hold", item=ONIGIRI, item_colors=ICON_COLORS)
    s = 8
    rows = max(y for _, y in grid) - min(y for _, y in grid) + 1
    sq_box = draw_squirrel(img, grid, 70, 1300 - rows * s, s)
    speech_tail(draw, sq_box[0] + 11 * s, dialog[3] - 24, rows=min(10, (sq_box[1] - dialog[3] + 24) // 6))

    # --- point window: tie back to the combination idea of slide 03
    ni = rpg_window(draw, *note, step=5, dither=False)
    px_rect(draw, ni[0] + 20, ni[1] + 16, ni[0] + 160, ni[1] + 58, INK)
    px_rect(draw, ni[0] + 24, ni[1] + 20, ni[0] + 156, ni[1] + 54, GOLD)
    draw_text(draw, (ni[0] + 90, ni[1] + 36), "ポイント", load_font(26, 900), INK, label="point-pill",
              container=(ni[0] + 24, ni[1] + 20, ni[0] + 156, ni[1] + 54))
    pts = ["主食＋野菜＋たんぱく質で、", "バランスよく組み合わせよう。"]
    f_pt = min((fit_font(l, ni[2] - ni[0] - 48, 34, 900) for l in pts), key=lambda f: f.size)
    for j, line in enumerate(pts):
        draw_text(draw, (ni[0] + 24, ni[1] + 112 + j * 52), line, f_pt, CREAM, anchor="lm",
                  label=f"point-{j + 1}", container=ni)

    img.save(OUT_PATH)
    print(f"saved: {OUT_PATH}")
    return verify_all()


if __name__ == "__main__":
    sys.exit(main())
