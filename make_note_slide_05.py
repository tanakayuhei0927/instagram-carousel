"""Point 1 slide (note_slide_05.png): vegetables and mushrooms first.

Three checkbox items (キャベツ / きのこ / ブロッコリー), each with a short memo
and a small doodle, plus a small "個人差があります" note at the bottom.
"""
import math

from note_common import (INK, ROOT, arc_points, draw_checklist, draw_footer, draw_headline,
                         draw_mushroom, draw_small_note, hand_path, new_page, save_and_check,
                         wobbly_ellipse)

OUT_PATH = ROOT / "note_slide_05.png"

ROWS = [("キャベツ", "サラダや汁物に"),
        ("きのこ", "スープや炒め物に"),
        ("ブロッコリー", "ゆでて副菜に")]
ROW_Y = [520, 745, 970]
BOX_X = 110
DOODLE_X = 880


def pen(n):
    return n


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
    draw = draw_checklist(img, draw, ROWS, ROW_Y, BOX_X, DOODLE_X)
    cabbage(draw, DOODLE_X, ROW_Y[0])
    draw_mushroom(draw, DOODLE_X - 30, ROW_Y[1] - 24, 2.2, pen)
    draw_mushroom(draw, DOODLE_X + 40, ROW_Y[1] - 4, 1.6, pen)
    broccoli(draw, DOODLE_X, ROW_Y[2] - 10)
    return draw


def main():
    img, draw = new_page(5)
    draw_headline(draw, "ポイント①：野菜・きのこを先に")
    draw = draw_items(img, draw)
    draw_small_note(draw, "※個人差があります")
    draw_footer(draw)
    save_and_check(img, OUT_PATH)


if __name__ == "__main__":
    main()
