"""Before slide (note_slide_02.png): cutting only the rice.

A simple line drawing of a meal with a small helping of rice, speech-bubble
memos about getting hungry, and a marker on "満足感が少ない？".
"""
from PIL import ImageDraw

from note_common import (INK, ROOT, W, arc_points, draw_footer, draw_text, hand_path,
                         load_font, marker_stroke, new_page, save_and_check,
                         speech_bubble, wobbly_line)

OUT_PATH = ROOT / "note_slide_02.png"


def draw_headline(draw):
    font = load_font(84)
    l, t, r, b = draw_text(draw, (W // 2, 340), "ご飯だけを減らすと…", font, label="headline")
    wobbly_line(draw, l, b + 22, r, b + 18, 5, INK, amp=2.0)


def draw_meal(draw):
    """Tray with a rice bowl holding only a little rice, a main dish and soup."""
    # tray
    x0, y0, x1, y1, r = 190, 470, 890, 780, 30
    tray = (arc_points(x0 + r, y0 + r, r, r, 180, 270, 10)
            + arc_points(x1 - r, y0 + r, r, r, 270, 360, 10)
            + arc_points(x1 - r, y1 - r, r, r, 0, 90, 10)
            + arc_points(x0 + r, y1 - r, r, r, 90, 180, 10))
    hand_path(draw, tray + [tray[0]], 5)

    # main dish: oval plate with a simple fish
    hand_path(draw, arc_points(540, 570, 150, 58, 0, 365), 4)
    fish = arc_points(525, 570, 78, 26, 200, 340, 20) + arc_points(525, 570, 78, 26, 20, 160, 20)
    hand_path(draw, fish + [fish[0]], 4)
    hand_path(draw, [(600, 570), (636, 548), (636, 592), (600, 570)], 4)  # tail
    draw.ellipse((468, 562, 478, 572), fill=INK)  # eye

    # rice bowl (front left): rim, body, foot, and a small mound of rice
    bx, by = 340, 680
    hand_path(draw, arc_points(bx, by, 96, 24, 0, 362), 4)
    hand_path(draw, arc_points(bx, by, 96, 82, 0, 180), 5)
    hand_path(draw, [(bx - 34, by + 80), (bx - 30, by + 94), (bx + 30, by + 94), (bx + 34, by + 80)], 4)
    hand_path(draw, arc_points(bx, by + 6, 34, 16, 190, 350, 20), 4)  # little rice, sunk low

    # soup bowl (front right) with steam
    sx, sy = 740, 680
    hand_path(draw, arc_points(sx, sy, 90, 22, 0, 362), 4)
    hand_path(draw, arc_points(sx, sy, 90, 74, 0, 180), 5)
    for dx in (-30, 0, 30):
        wobbly_line(draw, sx + dx, sy - 40, sx + dx + 4, sy - 90, 3, INK, amp=5, waves=1.2)

    # chopsticks along the bottom of the tray
    hand_path(draw, [(470, 752), (640, 742)], 4)
    hand_path(draw, [(470, 764), (640, 760)], 4)

    # "ご飯 少なめ" label with an arrow to the rice
    f = load_font(38)
    draw_text(draw, (206, 518), "ご飯 少なめ", f, anchor="lm", label="label rice",
              container=(x0, y0, x1, y1))
    hand_path(draw, [(280, 548), (300, 600), (328, 652)], 4)
    hand_path(draw, [(306, 636), (328, 652), (330, 626)], 4)


def draw_bubbles(draw):
    f = load_font(44)
    speech_bubble(draw, 300, 910, "お腹がすく", f, tail_to=(330, 810), label="bubble お腹がすく")
    speech_bubble(draw, 710, 920, "つい間食したくなる", f, tail_to=(720, 815),
                  label="bubble つい間食したくなる")


def draw_point(img, draw):
    font = load_font(72)
    y = 1090
    l, t, r, b = draw.textbbox((W // 2, y), "満足感が少ない？", font=font, anchor="mm")
    marker_stroke(img, l - 14, r + 14, b - 10, 48)
    draw = ImageDraw.Draw(img)
    draw_text(draw, (W // 2, y), "満足感が少ない？", font, label="point 満足感が少ない？")
    return draw


def main():
    img, draw = new_page(2)
    draw_headline(draw)
    draw_meal(draw)
    draw_bubbles(draw)
    draw = draw_point(img, draw)
    draw_footer(draw)
    save_and_check(img, OUT_PATH)


if __name__ == "__main__":
    main()
