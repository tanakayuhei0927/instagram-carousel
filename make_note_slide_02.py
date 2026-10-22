"""Before slide (note_slide_02.png): cutting only the rice.

A simple line drawing of a meal with a small helping of rice, speech-bubble
memos about getting hungry, and a marker on "満足感が少ない？".
"""
from note_common import (ROOT, draw_footer, draw_headline, draw_marker_point, draw_meal,
                         draw_text, hand_path, load_font, new_page, save_and_check,
                         speech_bubble)

OUT_PATH = ROOT / "note_slide_02.png"


def draw_illustration(draw):
    tray = draw_meal(draw)

    # "ご飯 少なめ" label with an arrow to the rice
    f = load_font(38)
    draw_text(draw, (206, 518), "ご飯 少なめ", f, anchor="lm", label="label rice",
              container=tray)
    hand_path(draw, [(280, 548), (300, 600), (328, 652)], 4)
    hand_path(draw, [(306, 636), (328, 652), (330, 626)], 4)


def draw_bubbles(draw):
    f = load_font(44)
    speech_bubble(draw, 300, 910, "お腹がすく", f, tail_to=(330, 810), label="bubble お腹がすく")
    speech_bubble(draw, 710, 920, "つい間食したくなる", f, tail_to=(720, 815),
                  label="bubble つい間食したくなる")


def main():
    img, draw = new_page(2)
    draw_headline(draw, "ご飯だけを減らすと…")
    draw_illustration(draw)
    draw_bubbles(draw)
    draw = draw_marker_point(img, draw, "満足感が少ない？", 1090)
    draw_footer(draw)
    save_and_check(img, OUT_PATH)


if __name__ == "__main__":
    main()
