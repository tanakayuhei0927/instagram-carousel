"""Checklist slide (dark_slide_02.png): the three basics.

Empty white-framed checkboxes for タオル / 水筒 / 着替え with a gray memo
under each, under a headline with a neon underline.
"""
from dark_common import (ROOT, checklist_rows, draw_corner_labels, draw_footer, draw_headline,
                         new_page, save_and_check)

OUT_PATH = ROOT / "dark_slide_02.png"

ROWS = [("タオル", "汗を拭く用"),
        ("水筒", "こまめな水分補給に"),
        ("着替え", "トレーニング後の着替えに")]


def main():
    img, draw = new_page()
    draw_corner_labels(draw, 2)
    draw = draw_headline(img, draw, "持ち物① 基本の3つ")
    checklist_rows(draw, ROWS, [500, 730, 960])
    draw_footer(draw)
    save_and_check(img, OUT_PATH)


if __name__ == "__main__":
    main()
