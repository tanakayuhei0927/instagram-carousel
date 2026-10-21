"""Instagram carousel slide 02 (empathy) — the restrict-hunger-snack loop.

Usage: python3 make_slide_02.py  ->  slide_02.png (1080x1350)
"""
import random
import sys

from PIL import Image, ImageDraw

from rpg_common import (
    CREAM, GOLD, GOLD_DARK, GOLD_LIGHT, GREEN, GREEN_DARK, GREEN_LIGHT,
    INK, NAVY, NAVY_DEEP, NAVY_LIGHT, RED, ROOT, H, W,
    build_squirrel, decor_boxes, draw_squirrel, draw_text, fit_font, load_font, number_badge,
    outline, pill, pixel_arrow, px_rect, rpg_window, verify_all,
)

OUT_PATH = ROOT / "slide_02.png"

STEPS = [
    # (action, quote, mood label, expression, pill color, pill text color)
    ("食事を減らす", "「これくらい平気！」", "平気", "calm", GREEN_LIGHT, INK),
    ("お腹が空く", "「お腹すいた…」", "不安", "worried", GOLD, INK),
    ("間食が気になる", "「おやつ食べたいかも…」", "困惑", "confused", GOLD_DARK, CREAM),
    ("さらに食事を減らす", "「もう限界…！」", "限界", "limit", RED, CREAM),
]


# ---------------------------------------------------------------- background

def draw_background(draw, field):
    # banded night sky (same tones as slide 01)
    bands = [NAVY_DEEP, (12, 22, 54), (14, 26, 62), NAVY]
    band_h = field[1] / len(bands)
    for i, c in enumerate(bands):
        px_rect(draw, 0, int(i * band_h), W, int((i + 1) * band_h) + 1, c)
    px_rect(draw, 0, field[1], W, H, NAVY_DEEP)
    rnd = random.Random(11)
    for _ in range(40):
        x = rnd.randrange(0, W // 6) * 6
        y = rnd.randrange(0, 40) * 6
        if 30 < y < 330 and 30 < x < 1050:  # keep the headline area clean
            if not (y < 110 and (x < 330 or x > 700)):
                continue
        px_rect(draw, x, y, x + 6, y + 6, rnd.choice([CREAM, GOLD_LIGHT, NAVY_LIGHT]))
    for (x, y) in [(36, 300), (1032, 260)]:
        px_rect(draw, x, y - 12, x + 6, y + 18, GOLD_LIGHT)
        px_rect(draw, x - 12, y, x + 18, y + 6, GOLD_LIGHT)

    # grass "world map" board that holds the loop
    x0, y0, x1, y1 = field
    s = 6
    px_rect(draw, x0 + s, y0, x1 - s, y1, INK)
    px_rect(draw, x0, y0 + s, x1, y1 - s, INK)
    px_rect(draw, x0 + s, y0 + s, x1 - s, y1 - s, GREEN_DARK)
    px_rect(draw, x0 + 2 * s, y0 + 2 * s, x1 - 2 * s, y1 - 2 * s, GREEN)
    for y in range(y0 + 2 * s, y1 - 2 * s, 36):
        for x in range(x0 + 2 * s, x1 - 2 * s, 36):
            if ((x // 36) + (y // 36)) % 2 == 0:
                px_rect(draw, x, y, min(x + 36, x1 - 2 * s), min(y + 36, y1 - 2 * s), (54, 140, 66))
    px_rect(draw, x0 + 2 * s, y0 + 2 * s, x1 - 2 * s, y0 + 3 * s, GREEN_LIGHT)
    for _ in range(50):
        x = rnd.randrange((x0 + 24) // 6, (x1 - 36) // 6) * 6
        y = rnd.randrange((y0 + 24) // 6, (y1 - 36) // 6) * 6
        px_rect(draw, x, y, x + 6, y + 12, GREEN_LIGHT)
        px_rect(draw, x + 6, y + 6, x + 12, y + 12, GREEN_DARK)


# ---------------------------------------------------------------- parts


def draw_card(img, draw, box, idx, step, fonts):
    action, quote, mood, expression, pill_bg, pill_fg = step
    inner = rpg_window(draw, *box, step=5, dither=False)
    ix0, iy0, ix1, iy1 = inner
    number_badge(draw, ix0 + 12, iy0 + 12, idx + 1, fonts["badge"])
    pill(draw, ix1 - 12, iy0 + 13, mood, pill_bg, pill_fg, fonts["pill"], f"mood-{idx + 1}")

    # squirrel — same pixel grid as the cover, anchored on a fixed origin so
    # every expression lines up (sweat drops change the grid's bounds)
    grid = build_squirrel(expression)
    s = 6
    sq_w = 39 * s
    ox = (ix0 + ix1) // 2 - sq_w // 2 + (min(x for x, _ in grid) + 3) * s
    draw_squirrel(img, grid, ox, iy0 + 4, s)

    max_w = ix1 - ix0 - 36
    f_act = fit_font(action, max_w, 42, 900)
    draw_text(draw, ((ix0 + ix1) // 2, iy0 + 242), action, f_act, CREAM,
              stroke=0, label=f"action-{idx + 1}", container=inner)
    f_q = fit_font(quote, max_w, 28, 700)
    draw_text(draw, ((ix0 + ix1) // 2, iy0 + 284), quote, f_q, GOLD_LIGHT,
              label=f"quote-{idx + 1}", container=inner)


def loop_emblem(draw, cx, cy, font):
    r = 7  # in 6px units, pixel circle
    cells = {(x, y) for x in range(-r, r + 1) for y in range(-r, r + 1)
             if x * x + y * y <= r * r + 2}
    for (x, y) in outline(cells):
        px_rect(draw, cx + x * 6 - 3, cy + y * 6 - 3, cx + x * 6 + 3, cy + y * 6 + 3, INK)
    for (x, y) in cells:
        c = GOLD_LIGHT if y < -r + 3 and x * x + y * y > (r - 2) ** 2 else GOLD
        px_rect(draw, cx + x * 6 - 3, cy + y * 6 - 3, cx + x * 6 + 3, cy + y * 6 + 3, c)
    rr = (r + 1) * 6
    decor_boxes.append(("emblem", (cx - rr - 3, cy - rr - 3, cx + rr + 3, cy + rr + 3)))
    draw_text(draw, (cx, cy - 2), "ループ", font, INK, label="emblem-text",
              container=(cx - r * 6, cy - r * 6, cx + r * 6, cy + r * 6))

# ---------------------------------------------------------------- main

def main():
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)
    margin = 54

    field = (margin - 24, 368, W - margin + 24, 1146)
    draw_background(draw, field)

    # --- top HUD
    f_tag = load_font(32, 900)
    tag = (margin, 44, margin + 250, 100)
    px_rect(draw, *tag, INK)
    px_rect(draw, tag[0] + 4, tag[1] + 4, tag[2] - 4, tag[3] - 4, GOLD)
    px_rect(draw, tag[0] + 4, tag[1] + 4, tag[2] - 4, tag[1] + 10, GOLD_LIGHT)
    draw_text(draw, ((tag[0] + tag[2]) // 2, (tag[1] + tag[3]) // 2 - 2), "STAGE 1", f_tag, INK,
              label="stage-tag", container=tag)
    draw_text(draw, (W - margin, 72), "陥りやすいループ", load_font(30, 700), CREAM, anchor="rm",
              shadow=NAVY_DEEP, shadow_off=4, label="hud-right")

    # --- headline (no window here: open composition, unlike the cover)
    lines = ["食事を減らすほど、", "つらくなってない？"]
    max_w = W - margin * 2
    f_head = min((fit_font(l, max_w, 86, 900, stroke=5) for l in lines), key=lambda f: f.size)
    for i, line in enumerate(lines):
        draw_text(draw, (W // 2, 176 + i * 112), line, f_head, CREAM if i == 0 else GOLD_LIGHT,
                  shadow=INK, shadow_off=7, stroke=5, stroke_fill=INK, label=f"headline-{i + 1}")

    # --- loop cards (clockwise 1 → 2 → 3 → 4 → 1)
    fonts = {"badge": load_font(30, 900), "pill": load_font(28, 900)}
    pad, gap = 24, 52
    gx0, gy0, gx1, gy1 = field[0] + pad, field[1] + pad, field[2] - pad, field[3] - pad
    cw = (gx1 - gx0 - gap) // 2
    ch = (gy1 - gy0 - gap) // 2
    boxes = [
        (gx0, gy0, gx0 + cw, gy0 + ch),
        (gx1 - cw, gy0, gx1, gy0 + ch),
        (gx1 - cw, gy1 - ch, gx1, gy1),
        (gx0, gy1 - ch, gx0 + cw, gy1),
    ]
    for i, (box, step) in enumerate(zip(boxes, STEPS)):
        draw_card(img, draw, box, i, step, fonts)

    mid_x = (gx0 + gx1) // 2
    mid_y = (gy0 + gy1) // 2
    pixel_arrow(draw, mid_x, gy0 + 110, "right")
    pixel_arrow(draw, gx1 - 66, mid_y, "down")
    pixel_arrow(draw, mid_x, gy1 - ch + 110, "left")
    pixel_arrow(draw, gx0 + 66, mid_y, "up")
    loop_emblem(draw, mid_x, mid_y, load_font(24, 900))

    # --- note: a common pattern, not a diagnosis
    note = (margin, 1170, W - margin, 1312)
    ni = rpg_window(draw, *note, step=5)
    f_note = fit_font("がんばる人ほど、ハマりやすいパターンです。", ni[2] - ni[0] - 48, 36, 900)
    draw_text(draw, ((ni[0] + ni[2]) // 2, ni[1] + 30), "がんばる人ほど、ハマりやすいパターンです。",
              f_note, CREAM, label="note-1", container=ni)
    f_next = fit_font("次のページで、抜け出すヒントを紹介", ni[2] - ni[0] - 120, 30, 700)
    nb = draw_text(draw, ((ni[0] + ni[2]) // 2 - 16, ni[1] + 76), "次のページで、抜け出すヒントを紹介",
                   f_next, GOLD_LIGHT, label="note-2", container=ni)
    ax, ay = nb[2] + 16, (nb[1] + nb[3]) // 2
    for r in range(3):
        px_rect(draw, ax + r * 5, ay - 15 + r * 5, ax + r * 5 + 5, ay + 15 - r * 5, GOLD)
    decor_boxes.append(("note-arrow", (ax, ay - 15, ax + 20, ay + 15)))

    img.save(OUT_PATH)
    print(f"saved: {OUT_PATH}")
    return verify_all(allowed={("note-", "note-arrow"), ("emblem-text", "emblem")})


if __name__ == "__main__":
    sys.exit(main())
