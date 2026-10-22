"""Cover slide (note_slide_01.png) for the handwritten-notebook carousel series.

Separate series from slide_XX.png. Graph-paper background, big handwritten
headline with a marker stroke underneath, and scribbled memos in the margins.
After drawing, every text box is checked for missing glyphs and overflow.
"""
from PIL import ImageDraw

from note_common import (H, INK, ROOT, SAFE, W, draw_footer, draw_text, load_font,
                         marker_stroke, new_page, rotated_memo, save_and_check,
                         wobbly_ellipse, wobbly_line)

OUT_PATH = ROOT / "note_slide_01.png"


def draw_headline(img, draw):
    font = load_font(128)
    lines = [("今日のごはん、", 470), ("こう変えてみた", 650)]
    # marker first so the ink sits on top of it
    for text, y in lines:
        l, t, r, b = draw.textbbox((W // 2, y), text, font=font, anchor="mm")
        marker_stroke(img, l - 14, r + 14, b - 16, 70)
    draw = ImageDraw.Draw(img)
    for i, (text, y) in enumerate(lines):
        draw_text(draw, (W // 2, y), text, font, label=f"headline {i + 1}",
                  container=(SAFE, SAFE, W - SAFE, H - SAFE))
    return draw


def draw_sub(draw):
    f = load_font(46)
    draw_text(draw, (W // 2, 820), "ちょっとの工夫で、毎日がラクになる", f, label="sub copy")


def draw_memos(img, draw):
    # "大事！" scribbled at the lower-left with a pen loop around it
    memo_font = load_font(72)
    cx, cy = 250, 1040
    bbox = rotated_memo(img, (cx, cy), "大事！", memo_font, 9, "memo 大事！")
    draw = ImageDraw.Draw(img)
    wobbly_ellipse(draw, cx, cy, (bbox[2] - bbox[0]) / 2 + 52, (bbox[3] - bbox[1]) / 2 + 46,
                   5, INK)
    # small arrow from the memo pointing up toward the headline
    wobbly_line(draw, 300, 930, 380, 870, 5, INK, amp=1.0, waves=0.6)
    draw.line([(380, 870), (352, 874)], fill=INK, width=5)
    draw.line([(380, 870), (372, 897)], fill=INK, width=5)

    # second note at the lower-right
    note_font = load_font(44)
    rotated_memo(img, (770, 1010), "まずは1つだけ\nやってみる", note_font, -5,
                 "memo まずは1つだけ")
    draw = ImageDraw.Draw(img)
    wobbly_line(draw, 640, 1080, 900, 1074, 4, INK, amp=1.5)
    return draw


def main():
    img, draw = new_page(1)
    draw = draw_headline(img, draw)
    draw_sub(draw)
    draw = draw_memos(img, draw)
    draw_footer(draw)
    save_and_check(img, OUT_PATH)


if __name__ == "__main__":
    main()
