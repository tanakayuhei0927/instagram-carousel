"""Vegetables-first slide (note_slide_03.png).

Same little-rice meal as slide 02, now with a cabbage/mushroom plate and
mushroom soup added first, speech-bubble memos, and a marker on "まず野菜から".
"""
from note_common import (ROOT, draw_footer, draw_headline, draw_marker_point, draw_meal,
                         draw_text, hand_path, load_font, new_page, save_and_check,
                         speech_bubble)

OUT_PATH = ROOT / "note_slide_03.png"


def draw_illustration(draw):
    draw_meal(draw, veg=True)

    # "キャベツ・きのこを先に！" label above the tray, pointing at the salad plate
    f = load_font(38)
    draw_text(draw, (860, 446), "キャベツ・きのこを先に！", f, anchor="rm", label="label veg")
    hand_path(draw, [(760, 470), (740, 500), (726, 524)], 4)
    hand_path(draw, [(722, 498), (726, 524), (748, 512)], 4)


def draw_bubbles(draw):
    f = load_font(40)
    speech_bubble(draw, 262, 910, "満足感がアップ？", f, tail_to=(320, 812),
                  label="bubble 満足感がアップ？")
    speech_bubble(draw, 734, 920, "量が増えた感じがする", f, tail_to=(720, 815),
                  label="bubble 量が増えた感じがする")


def main():
    img, draw = new_page(3)
    draw_headline(draw, "野菜を先に足すと？")
    draw_illustration(draw)
    draw_bubbles(draw)
    draw = draw_marker_point(img, draw, "まず野菜から", 1090)
    draw_footer(draw)
    save_and_check(img, OUT_PATH)


if __name__ == "__main__":
    main()
