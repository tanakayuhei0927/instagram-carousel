"""Vegetables-first slide (pop_slide_03.png).

Bright green background (accents: green + yellow), the little-rice meal with
a cabbage/mushroom plate and mushroom soup added, two speech bubbles and a
big "まず野菜から" label.
"""
from pop_common import (GREEN_BG, GREEN_DEEP, GREEN_DOT, GREEN_LIGHT, ROOT, W, YELLOW,
                        big_label, bubble, decor, draw_footer, draw_meal, headline, load_font,
                        new_page, rounded_label, save_and_check)

OUT_PATH = ROOT / "pop_slide_03.png"


def main():
    img, draw = new_page(GREEN_BG, GREEN_DOT)
    decor(draw, YELLOW, GREEN_LIGHT, GREEN_LIGHT)
    rounded_label(draw, (80, 90), "シリーズ1", load_font(40), label="series label")
    headline(draw, "野菜を先に足すと？", 270, GREEN_DEEP)
    draw_meal(draw, W // 2, 610, bowl=YELLOW, veg=True)

    f = load_font(44)
    bubble(draw, 300, 880, "満足感アップ？", f, GREEN_DEEP, tail_to=(380, 790))
    bubble(draw, 750, 880, "量が増えた感じ", f, GREEN_DEEP, tail_to=(700, 790))
    big_label(draw, "まず野菜から", 1060, YELLOW)
    draw_footer(draw)
    save_and_check(img, OUT_PATH)


if __name__ == "__main__":
    main()
