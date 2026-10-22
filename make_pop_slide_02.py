"""Before slide (pop_slide_02.png): cutting only the rice.

Gray background for a slightly lonely mood (accents: light blue + yellow),
a flat illustration of a meal with little rice, two speech bubbles and a
big "満足感が少ない？" label.
"""
from pop_common import (GRAY_BG, GRAY_DEEP, GRAY_DOT, ROOT, SKY, W, WAVE_GRAY, YELLOW,
                        big_label, bubble, decor, draw_footer, draw_meal, headline, load_font,
                        new_page, rounded_label, save_and_check)

OUT_PATH = ROOT / "pop_slide_02.png"


def main():
    img, draw = new_page(GRAY_BG, GRAY_DOT)
    decor(draw, SKY, WAVE_GRAY, WAVE_GRAY)
    rounded_label(draw, (80, 90), "シリーズ1", load_font(40), label="series label")
    headline(draw, "ご飯だけを減らすと…", 270, GRAY_DEEP)
    draw_meal(draw, W // 2, 610, bowl=SKY)

    f = load_font(44)
    bubble(draw, 280, 880, "お腹がすく", f, SKY, tail_to=(330, 790))
    bubble(draw, 730, 880, "つい間食したくなる", f, SKY, tail_to=(740, 790))
    big_label(draw, "満足感が少ない？", 1060, YELLOW)
    draw_footer(draw)
    save_and_check(img, OUT_PATH)


if __name__ == "__main__":
    main()
