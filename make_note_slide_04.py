"""Before/After comparison slide (note_slide_04.png).

Page split in two: Before (only rice cut) on the left, After (vegetables
first) on the right, each with a small meal drawing. A center column lists
量 / 満足感 / 続けやすさ with arrows, and a marker on "続けやすさがポイント".
"""
from note_common import (INK, ROOT, W, draw_footer, draw_headline, draw_marker_point,
                         draw_meal, draw_text, hand_path, load_font, new_page,
                         save_and_check, wobbly_line)

OUT_PATH = ROOT / "note_slide_04.png"

LEFT_X, RIGHT_X = 280, 800  # column centers
MID = W // 2


def arrow(draw, x0, y, x1, width=4, head=14):
    wobbly_line(draw, x0, y, x1, y, width, INK, amp=1.0, waves=0.8)
    hand_path(draw, [(x1 - head, y - head * 0.8), (x1, y), (x1 - head, y + head * 0.8)], width)


def draw_columns(draw):
    f = load_font(34)
    left_half = (70, 60, MID - 20, 1290)
    right_half = (MID + 20, 60, W - 70, 1290)
    for x, text, half in ((LEFT_X, "Before：ご飯だけ減らす", left_half),
                          (RIGHT_X, "After：野菜を先に足す", right_half)):
        l, t, r, b = draw_text(draw, (x, 460), text, f, label=f"column {text}", container=half)
        wobbly_line(draw, l, b + 12, r, b + 10, 3, INK, amp=1.2)

    # dashed center divider, with a gap for the big arrow
    for y in range(440, 720, 28):
        if not 570 <= y <= 660:
            hand_path(draw, [(MID, y), (MID + 1, y + 14)], 3)

    draw_meal(draw, cx=LEFT_X, cy=615, s=0.58)
    draw_meal(draw, cx=RIGHT_X, cy=615, s=0.58, veg=True)
    arrow(draw, MID - 26, 615, MID + 30, width=5, head=16)


def draw_compare(draw):
    item_font = load_font(46)
    note_font = load_font(34)
    rows = [("量", "少なめ", "増えた感じ"),
            ("満足感", "物足りない？", "アップ？"),
            ("続けやすさ", "つらいかも？", "続けやすい？")]
    for i, (item, before, after) in enumerate(rows):
        y = 790 + i * 82
        draw_text(draw, (MID, y), item, item_font, label=f"item {item}")
        draw_text(draw, (LEFT_X - 70, y), before, note_font, label=f"before {item}",
                  container=(70, 60, MID - 130, 1290))
        draw_text(draw, (RIGHT_X + 70, y), after, note_font, label=f"after {item}",
                  container=(MID + 130, 60, W - 70, 1290))
        arrow(draw, LEFT_X + 70, y, MID - 140)
        arrow(draw, MID + 140, y, RIGHT_X - 70)


def main():
    img, draw = new_page(4)
    draw_headline(draw, "Before と After を比べてみる")
    draw_columns(draw)
    draw_compare(draw)
    draw = draw_marker_point(img, draw, "続けやすさがポイント", 1100)
    draw_footer(draw)
    save_and_check(img, OUT_PATH)


if __name__ == "__main__":
    main()
