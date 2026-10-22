"""Point 2 slide (note_slide_06.png): don't forget protein.

Three checkbox items (鶏肉・魚 / 卵 / 豆腐), each with a short memo and a small
doodle, a marker on "野菜だけでは足りない？", and a small caveat at the bottom.
"""
import math

from note_common import (ROOT, arc_points, draw_checklist, draw_fish, draw_footer,
                         draw_headline, draw_marker_point, draw_small_note, hand_path,
                         new_page, save_and_check)

OUT_PATH = ROOT / "note_slide_06.png"

ROWS = [("鶏肉・魚", "鶏むね・サバなど"),
        ("卵", "ゆで卵・オムレツに"),
        ("豆腐", "冷ややっこ・みそ汁に")]
ROW_Y = [510, 710, 910]
BOX_X = 110
DOODLE_X = 880


def pen(n):
    return n


def drumstick(draw, cx, cy):
    """Chicken drumstick: teardrop meat tapering into a bone with a knob."""
    meat = arc_points(cx - 22, cy - 12, 34, 30, 105, 345, 30)
    meat += [(cx + 12, cy + 12), meat[0]]
    hand_path(draw, meat, 4)
    hand_path(draw, [(cx + 4, cy + 18), (cx + 36, cy + 40)], 4)
    hand_path(draw, [(cx + 14, cy + 8), (cx + 44, cy + 32)], 4)
    for dx, dy in ((38, 48), (52, 34)):  # bone knob
        hand_path(draw, arc_points(cx + dx, cy + dy, 9, 9, 0, 360, 14), 4)


def egg(draw, cx, cy, rx=36, ry=46):
    """Egg outline, narrower at the top."""
    pts = []
    for i in range(61):
        t = math.radians(i * 6)
        pts.append((cx + rx * math.cos(t) * (1 + 0.14 * math.sin(t)), cy + ry * math.sin(t)))
    hand_path(draw, pts, 4)


def half_egg(draw, cx, cy):
    """Boiled egg cut in half: white with a round yolk."""
    hand_path(draw, arc_points(cx, cy, 42, 32, 0, 362, 40), 4)
    hand_path(draw, arc_points(cx, cy + 2, 18, 16, 0, 362, 24), 4)


def tofu(draw, cx, cy, s=58, d=26):
    """Block of tofu drawn as a simple cube."""
    x0, y0 = cx - s / 2 - d / 2, cy - s / 2 + d / 2
    front = [(x0, y0), (x0 + s, y0), (x0 + s, y0 + s), (x0, y0 + s), (x0, y0)]
    hand_path(draw, front, 4)
    hand_path(draw, [(x0, y0), (x0 + d, y0 - d), (x0 + s + d, y0 - d), (x0 + s, y0)], 4)
    hand_path(draw, [(x0 + s + d, y0 - d), (x0 + s + d, y0 + s - d), (x0 + s, y0 + s)], 4)


def draw_items(img, draw):
    draw = draw_checklist(img, draw, ROWS, ROW_Y, BOX_X, DOODLE_X)
    drumstick(draw, DOODLE_X - 60, ROW_Y[0] + 10)
    draw_fish(draw, DOODLE_X + 40, ROW_Y[0] - 40, 0.62, pen)
    egg(draw, DOODLE_X - 40, ROW_Y[1] - 12)
    half_egg(draw, DOODLE_X + 50, ROW_Y[1] + 4)
    tofu(draw, DOODLE_X, ROW_Y[2] - 10)
    return draw


def main():
    img, draw = new_page(6)
    draw_headline(draw, "ポイント②：たんぱく質も忘れずに")
    draw = draw_items(img, draw)
    draw = draw_marker_point(img, draw, "野菜だけでは足りない？", 1080)
    draw_small_note(draw, "※個人差があります")
    draw_footer(draw)
    save_and_check(img, OUT_PATH)


if __name__ == "__main__":
    main()
