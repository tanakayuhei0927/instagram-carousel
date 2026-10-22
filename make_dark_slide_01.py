"""Cover slide (dark_slide_01.png) for the monochrome dark carousel series.

Near-black background with a hard-edged frame, a big white bold headline,
and neon green used only for the check marks and the underline. After
drawing, every text box is checked for missing glyphs and overflow.
"""
from PIL import ImageDraw

from dark_common import (GRAY_TEXT, LINE, LINE_DIM, NEON, PANEL, ROOT, W, check_mark,
                         draw_corner_labels, draw_footer, draw_text, load_font, neon_layer,
                         new_page, save_and_check)

OUT_PATH = ROOT / "dark_slide_01.png"

LINES = [("ジム初日の", 92, 330), ("持ち物", 180, 505), ("チェックリスト", 118, 695)]
ROWS_Y = [880, 960, 1040]
BOX_X, BOX = 290, 46


def draw_headline(img, draw):
    boxes = [draw_text(draw, (W // 2, y), text, load_font(size), label=f"headline {i + 1}")
             for i, (text, size, y) in enumerate(LINES)]
    l, t, r, b = boxes[-1]
    underline_y = b + 34

    def paint(d, glow):
        d.line((l, underline_y, r, underline_y), fill=NEON + ((150,) if glow else (255,)),
               width=16 if glow else 9)

    neon_layer(img, paint)
    return ImageDraw.Draw(img)


def draw_checklist(img, draw):
    """Three checked boxes with placeholder lines, hinting at a checklist."""
    for y in ROWS_Y:
        draw.rectangle((BOX_X, y - BOX // 2, BOX_X + BOX, y + BOX // 2), fill=PANEL,
                       outline=GRAY_TEXT, width=3)
        draw.rounded_rectangle((BOX_X + BOX + 40, y - 4, W - BOX_X, y + 4), radius=4,
                               fill=LINE if y == ROWS_Y[0] else LINE_DIM)

    def paint(d, glow):
        for y in ROWS_Y:
            check_mark(d, BOX_X + 6, y - BOX // 2 - 6, BOX + 4, 12 if glow else 7,
                       NEON + ((150,) if glow else (255,)))

    neon_layer(img, paint)
    return ImageDraw.Draw(img)


def main():
    img, draw = new_page()
    draw_corner_labels(draw, 1)
    draw = draw_headline(img, draw)
    draw = draw_checklist(img, draw)
    draw_footer(draw)
    save_and_check(img, OUT_PATH)


if __name__ == "__main__":
    main()
