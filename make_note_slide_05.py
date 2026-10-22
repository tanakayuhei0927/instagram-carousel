"""Point 1 slide (note_slide_05.png): vegetables and mushrooms first.

Three checkbox items (キャベツ / きのこ / ブロッコリー), each with a short memo
and a small doodle, plus a small "個人差があります" note at the bottom.
"""
import math

from PIL import ImageDraw

from note_common import (INK, ROOT, W, arc_points, draw_footer, draw_headline, draw_mushroom,
                         draw_text, hand_path, load_font, marker_stroke, new_page,
                         save_and_check, wobbly_ellipse)

OUT_PATH = ROOT / "note_slide_05.png"

ROWS = [("キャベツ", "サラダや汁物に"),
        ("きのこ", "スープや炒め物に"),
        ("ブロッコリー", "ゆでて副菜に")]
ROW_Y = [520, 745, 970]
BOX_X = 110
DOODLE_X = 880


def pen(n):
    return n


def checkbox(draw, x, y, size=60):
    hand_path(draw, [(x, y), (x + size, y + 1), (x + size - 1, y + size),
                     (x + 1, y + size - 1), (x, y)], 4)
    hand_path(draw, [(x + 12, y + size * 0.5), (x + size * 0.42, y + size - 12),
                     (x + size + 8, y - 10)], 6)


def cabbage(draw, cx, cy, r=62):
    """Round head wrapped by two outer leaves, with veins fanning from the core."""
    wobbly_ellipse(draw, cx, cy, r, r * 0.92, 4, INK, turns=1.05)
    hand_path(draw, arc_points(cx - r * 0.3, cy + r * 0.1, r * 0.85, r * 0.95, 95, 235, 24), 4)
    hand_path(draw, arc_points(cx + r * 0.3, cy + r * 0.1, r * 0.85, r * 0.95, -55, 85, 24), 4)
    core = (cx, cy + r * 0.75)
    for tx, ty in ((-0.6, -0.45), (0.0, -0.75), (0.6, -0.45)):
        mid = (cx + tx * r * 0.45, cy + r * 0.1)
        hand_path(draw, [core, mid, (cx + tx * r, cy + ty * r)], 3)


def broccoli(draw, cx, cy, rx=62, ry=44):
    """Scalloped floret crown on a thick stem."""
    crown = []
    for i in range(121):
        a = math.radians(180 + 180 * i / 120)
        bump = 9 * abs(math.sin(5 * (a - math.pi)))
        crown.append((cx + (rx + bump) * math.cos(a), cy + (ry + bump) * math.sin(a)))
    crown += arc_points(cx, cy, rx, 12, 0, 180, 20)  # soft underside
    hand_path(draw, crown, 4)
    for dx in (-26, 0, 26):  # floret texture
        hand_path(draw, arc_points(cx + dx, cy - 14, 12, 9, 200, 340, 8), 3)
    hand_path(draw, [(cx - 18, cy + 10), (cx - 14, cy + 66), (cx + 14, cy + 66),
                     (cx + 18, cy + 10)], 4)


def draw_items(img, draw):
    name_font = load_font(60)
    memo_font = load_font(38)
    # marker under each item name first so the ink sits on top
    for (name, _), y in zip(ROWS, ROW_Y):
        l, t, r, b = draw.textbbox((BOX_X + 100, y - 30), name, font=name_font, anchor="lm")
        marker_stroke(img, l - 8, r + 8, b - 8, 40)
    draw = ImageDraw.Draw(img)

    for i, ((name, memo), y) in enumerate(zip(ROWS, ROW_Y)):
        checkbox(draw, BOX_X, y - 62)
        draw_text(draw, (BOX_X + 100, y - 30), name, name_font, anchor="lm",
                  label=f"item {name}", container=(60, 60, DOODLE_X - 100, 1290))
        draw_text(draw, (BOX_X + 100, y + 48), f"→ {memo}", memo_font, anchor="lm",
                  label=f"memo {memo}", container=(60, 60, DOODLE_X - 100, 1290))
        if i < len(ROWS) - 1:  # dashed separator between rows
            for x in range(BOX_X, W - 100, 30):
                hand_path(draw, [(x, y + 108), (x + 14, y + 108)], 2)

    cabbage(draw, DOODLE_X, ROW_Y[0])
    draw_mushroom(draw, DOODLE_X - 30, ROW_Y[1] - 24, 2.2, pen)
    draw_mushroom(draw, DOODLE_X + 40, ROW_Y[1] - 4, 1.6, pen)
    broccoli(draw, DOODLE_X, ROW_Y[2] - 10)
    return draw


def main():
    img, draw = new_page(5)
    draw_headline(draw, "ポイント①：野菜・きのこを先に")
    draw = draw_items(img, draw)
    draw_text(draw, (100, 1240), "※個人差があります", load_font(32), anchor="ls",
              label="note 個人差")
    draw_footer(draw)
    save_and_check(img, OUT_PATH)


if __name__ == "__main__":
    main()
