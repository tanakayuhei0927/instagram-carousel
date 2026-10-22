"""Point 3 slide (pop_slide_07.png): set the staple food by activity level.

Pink base (accents: pink + light blue). Two picture cards side by side
(ご飯 / いも類), two light-blue speech bubbles, and a small
"必要量は人によって違います" note.
"""
import math

from pop_common import (BLACK, PINK, PINK_DEEP, PINK_DOT, ROOT, SKY, WHITE, bubble, decor,
                        draw_footer, headline, load_font, new_page, outlined_text,
                        rice_bowl_full, rounded_label, save_and_check, small_note)

OUT_PATH = ROOT / "pop_slide_07.png"

POTATO = (222, 190, 138)      # neutral food colors
POTATO_EYE = (168, 132, 88)
CUT_FACE = (252, 238, 200)

CARDS = [(290, "ご飯"), (790, "いも類")]
CARD_Y0, CARD_Y1 = 480, 730


def card(draw, cx):
    box = (cx - 200, CARD_Y0, cx + 200, CARD_Y1)
    draw.rounded_rectangle((box[0] + 8, box[1] + 10, box[2] + 8, box[3] + 10), radius=36,
                           fill=BLACK)
    draw.rounded_rectangle(box, radius=36, fill=WHITE, outline=BLACK, width=6)


def sweet_potato(draw, cx, cy, a=math.radians(-20)):
    pts = []
    for i in range(48):
        t = 2 * math.pi * i / 48
        x, y = 92 * math.cos(t), 36 * math.sin(t) * (0.6 + 0.4 * abs(math.sin(t)))
        pts.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
    draw.polygon(pts, fill=PINK_DEEP, outline=BLACK, width=5)
    # cut end showing the inside
    ex, ey = cx + 70 * math.cos(a), cy + 70 * math.sin(a)
    draw.ellipse((ex - 16, ey - 24, ex + 16, ey + 24), fill=CUT_FACE, outline=BLACK, width=4)


def potato(draw, cx, cy):
    draw.ellipse((cx - 58, cy - 44, cx + 58, cy + 44), fill=POTATO, outline=BLACK, width=5)
    for dx, dy in ((-24, -12), (14, -20), (26, 14), (-10, 18)):
        draw.ellipse((cx + dx - 4, cy + dy - 4, cx + dx + 4, cy + dy + 4), fill=POTATO_EYE)


def draw_cards(draw):
    for cx, _ in CARDS:
        card(draw, cx)
    rice_bowl_full(draw, CARDS[0][0], 630, 1.0, bowl=SKY)
    sweet_potato(draw, CARDS[1][0] - 40, 575)
    potato(draw, CARDS[1][0] + 70, 655)
    f = load_font(56)
    for cx, name in CARDS:
        outlined_text(draw, (cx, 800), name, f, stroke_w=9, label=f"card {name}", fill_holes=True)


def main():
    img, draw = new_page(PINK, PINK_DOT)
    decor(draw, SKY, SKY, PINK_DEEP)
    rounded_label(draw, (80, 90), "シリーズ1", load_font(40), label="series label")
    headline(draw, "ポイント③：主食は活動量で決める", 270, PINK_DEEP)
    draw_cards(draw)

    # side by side, each pointing up at its card name
    f = load_font(36)
    bubble(draw, 302, 950, "体を動かす日は主食もOK", f, SKY, tail_to=(290, 848))
    bubble(draw, 796, 950, "活動量に合わせて調整", f, SKY, tail_to=(790, 848))
    small_note(draw, "※必要量は人によって違います")
    draw_footer(draw)
    save_and_check(img, OUT_PATH)


if __name__ == "__main__":
    main()
