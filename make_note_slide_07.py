"""Point 3 slide (note_slide_07.png): set the staple food by activity level.

An activity scale with stick figures, a sticky memo in the margin listing
ご飯 / いも類, two speech bubbles, and a small caveat at the bottom.
"""
import math

from PIL import ImageDraw

from note_common import (INK, ROOT, arc_points, draw_footer, draw_headline, draw_small_note,
                         draw_text, hand_path, load_font, marker_stroke, new_page,
                         save_and_check, speech_bubble, wobbly_line)

OUT_PATH = ROOT / "note_slide_07.png"

MEMO = (640, 440, 990, 770)  # margin memo box


def stick_figure(draw, x, y, running=False):
    """Stick person; (x, y) is the head center."""
    hand_path(draw, arc_points(x, y, 15, 15, 0, 360, 20), 4)
    if running:
        hip = (x - 10, y + 62)
        hand_path(draw, [(x - 2, y + 15), hip], 4)
        hand_path(draw, [(x - 26, y + 40), (x - 4, y + 28), (x + 18, y + 44), (x + 30, y + 34)], 4)
        hand_path(draw, [(x - 40, y + 82), (x - 26, y + 90), hip, (x + 6, y + 88), (x + 20, y + 110)], 4)
    else:
        hip = (x, y + 62)
        hand_path(draw, [(x, y + 15), hip], 4)
        hand_path(draw, [(x - 22, y + 56), (x, y + 30), (x + 22, y + 56)], 4)
        hand_path(draw, [(x - 14, y + 110), hip, (x + 14, y + 110)], 4)


def draw_scale(img, draw):
    f = load_font(52)
    l, t, r, b = draw.textbbox((345, 470), "活動量", font=f, anchor="mm")
    marker_stroke(img, l - 10, r + 10, b - 8, 36)
    draw = ImageDraw.Draw(img)
    draw_text(draw, (345, 470), "活動量", f, label="scale title")

    y = 640
    wobbly_line(draw, 110, y, 590, y, 5, INK, amp=1.5, waves=1.0)
    hand_path(draw, [(568, y - 16), (592, y), (568, y + 16)], 5)
    hand_path(draw, [(110, y - 12), (110, y + 12)], 4)

    stick_figure(draw, 150, 510)
    stick_figure(draw, 540, 510, running=True)
    small = load_font(36)
    draw_text(draw, (180, 690), "ゆっくりの日", small, label="scale low")
    draw_text(draw, (520, 690), "よく動く日", small, label="scale high")
    return draw


def rice_bowl(draw, cx, cy):
    """Small bowl with a rounded mound of rice."""
    hand_path(draw, arc_points(cx, cy, 44, 11, 0, 180, 20), 3)  # front rim
    hand_path(draw, arc_points(cx, cy, 44, 38, 0, 180, 24), 4)
    hand_path(draw, arc_points(cx, cy, 44, 30, 180, 360, 24), 4)  # rice above the rim
    hand_path(draw, [(cx - 16, cy + 37), (cx - 14, cy + 45), (cx + 14, cy + 45), (cx + 16, cy + 37)], 3)
    for dx, dy in ((-18, -10), (0, -18), (16, -8)):  # rice grains
        hand_path(draw, arc_points(cx + dx, cy + dy, 6, 3, 0, 360, 10), 2)


def sweet_potato(draw, cx, cy):
    """Tilted sweet potato with pointed ends and a few skin marks."""
    pts = []
    for i in range(61):
        t = math.radians(i * 6)
        x, yy = 50 * math.cos(t), 20 * math.sin(t) * (0.55 + 0.45 * abs(math.sin(t)))
        a = math.radians(-18)
        pts.append((cx + x * math.cos(a) - yy * math.sin(a), cy + x * math.sin(a) + yy * math.cos(a)))
    hand_path(draw, pts, 4)
    for dx in (-18, 4, 24):
        hand_path(draw, [(cx + dx, cy - 4 - dx * 0.3), (cx + dx + 8, cy - 1 - dx * 0.3)], 3)


def draw_memo(draw):
    x0, y0, x1, y1 = MEMO
    fold = 36
    hand_path(draw, [(x0, y0), (x1, y0 + 2), (x1 - 1, y1 - fold), (x1 - fold, y1),
                     (x0 + 1, y1 - 1), (x0, y0)], 4)
    hand_path(draw, [(x1 - 1, y1 - fold), (x1 - fold + 4, y1 - fold + 4), (x1 - fold, y1)], 3)

    title = load_font(40)
    l, t, r, b = draw_text(draw, ((x0 + x1) // 2, y0 + 50), "主食メモ", title,
                           label="memo title", container=MEMO)
    wobbly_line(draw, l, b + 10, r, b + 8, 3, INK, amp=1.0)

    item = load_font(44)
    for text, y, doodle in (("・ご飯", 570, rice_bowl), ("・いも類", 690, sweet_potato)):
        draw_text(draw, (x0 + 26, y), text, item, anchor="lm", label=f"memo {text}",
                  container=(x0, y0, x1 - 110, y1))
        doodle(draw, x1 - 64, y)


def draw_bubbles(draw):
    f = load_font(40)
    speech_bubble(draw, 330, 830, "体を動かす日は主食もOK", f, tail_to=(520, 720),
                  label="bubble 体を動かす日は主食もOK")
    speech_bubble(draw, 775, 960, "活動量に合わせて調整", f, tail_to=(820, 785),
                  label="bubble 活動量に合わせて調整")


def main():
    img, draw = new_page(7)
    draw_headline(draw, "ポイント③：主食は活動量で決める")
    draw = draw_scale(img, draw)
    draw_memo(draw)
    draw_bubbles(draw)
    draw_small_note(draw, "※必要量は人によって違います")
    draw_footer(draw)
    save_and_check(img, OUT_PATH)


if __name__ == "__main__":
    main()
