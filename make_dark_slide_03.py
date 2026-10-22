"""Checklist slide (dark_slide_03.png): shoes and wear.

Empty white-framed checkboxes for 運動靴 / 動きやすい服 / 汗拭きシート with a
gray memo under each, under a headline with a neon underline.
"""
from dark_common import (ROOT, checklist_rows, draw_corner_labels, draw_footer, draw_headline,
                         new_page, save_and_check)

OUT_PATH = ROOT / "dark_slide_03.png"

ROWS = [("運動靴", "普段履きより、室内用の靴が安心"),
        ("動きやすい服", "伸縮性のある服が動きやすい"),
        ("タオル以外の汗拭きシート", "さっと拭けて、着替えの前にも便利")]


def main():
    img, draw = new_page()
    draw_corner_labels(draw, 3)
    draw = draw_headline(img, draw, "持ち物② シューズ・ウェア")
    checklist_rows(draw, ROWS, [500, 730, 960])
    draw_footer(draw)
    save_and_check(img, OUT_PATH)


if __name__ == "__main__":
    main()
