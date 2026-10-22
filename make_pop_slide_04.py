"""Before/After comparison slide (pop_slide_04.png).

Left half gray (Before), right half green (After); accents green + yellow.
A meal illustration on each side, the three comparison items in the
center column, and a "続けやすさがポイント" label at the bottom.
"""
from pop_common import (BLACK, GRAY_BG, GRAY_DOT, GREEN_BG, GREEN_DEEP, GREEN_DOT,
                        GREEN_LIGHT, H, ROOT, W, YELLOW, big_label, circle, draw_footer,
                        draw_meal, headline, load_font, new_page, outlined_text, polka,
                        rounded_label, save_and_check, wave_floor)

OUT_PATH = ROOT / "pop_slide_04.png"

MID = W // 2
LEFT_X, RIGHT_X = 270, 810
LEFT_HALF = (50, 50, MID - 10, H - 50)
RIGHT_HALF = (MID + 10, 50, W - 50, H - 50)
WAVE_GRAY = (206, 208, 214)
BOWL_GRAY = (214, 216, 222)
SHADOW = (70, 72, 80)


def draw_background(draw):
    draw.rectangle((MID, 0, W, H), fill=GREEN_BG)
    polka(draw, (MID, 0, W, H), GREEN_DOT)
    circle(draw, 60, 250, 150, WAVE_GRAY)
    circle(draw, 1000, 230, 210, YELLOW)
    wave_floor(draw, 0, MID, 1180, 24, 300, WAVE_GRAY)
    wave_floor(draw, MID, W, 1180, 24, 300, GREEN_LIGHT)
    draw.line((MID, 0, MID, H), fill=BLACK, width=6)


def arrow(draw, x0, y, x1, width=6, head=16):
    draw.line((x0, y, x1 - head, y), fill=BLACK, width=width)
    draw.polygon([(x1, y), (x1 - head * 1.4, y - head), (x1 - head * 1.4, y + head)], fill=BLACK)


def big_arrow(draw, cx, cy):
    """Chunky yellow arrow with a black outline."""
    pts = [(cx - 52, cy - 18), (cx + 4, cy - 18), (cx + 4, cy - 44), (cx + 56, cy),
           (cx + 4, cy + 44), (cx + 4, cy + 18), (cx - 52, cy + 18)]
    draw.polygon(pts, fill=YELLOW, outline=BLACK, width=6)


def draw_columns(draw):
    f = load_font(34)
    outlined_text(draw, (LEFT_X, 420), "Before：ご飯だけ減らす", f, stroke_w=7,
                  label="column Before", container=LEFT_HALF, fill_holes=True)
    outlined_text(draw, (RIGHT_X, 420), "After：野菜を先に足す", f, stroke_w=7,
                  label="column After", container=RIGHT_HALF, fill_holes=True)
    draw_meal(draw, LEFT_X, 590, s=0.56, bowl=BOWL_GRAY)
    draw_meal(draw, RIGHT_X, 590, s=0.56, bowl=YELLOW, veg=True)
    big_arrow(draw, MID, 590)


def draw_compare(draw):
    item_font = load_font(44)
    note_font = load_font(36)
    rows = [("量", "少なめ", "増えた感じ"),
            ("満足感", "物足りない？", "アップ？"),
            ("続けやすさ", "つらいかも？", "続けやすい？")]
    for i, (item, before, after) in enumerate(rows):
        y = 765 + i * 88
        l, t, r, b = draw.textbbox((MID, y), item, font=item_font, anchor="mm", stroke_width=6)
        pill = (min(l, MID - 90) - 26, t - 12, max(r, MID + 90) + 26, b + 12)
        draw.rounded_rectangle(pill, radius=(pill[3] - pill[1]) // 2, fill=GREEN_DEEP,
                               outline=BLACK, width=5)
        outlined_text(draw, (MID, y), item, item_font, stroke_w=6, label=f"item {item}",
                      container=pill, fill_holes=True)
        outlined_text(draw, (190, y), before, note_font, stroke_w=6, label=f"before {item}",
                      container=(50, 50, pill[0] - 70, H - 50), fill_holes=True)
        outlined_text(draw, (W - 190, y), after, note_font, stroke_w=6, label=f"after {item}",
                      container=(pill[2] + 70, 50, W - 50, H - 50), fill_holes=True)
        arrow(draw, 320, y, pill[0] - 12)
        arrow(draw, pill[2] + 12, y, 762)


def main():
    img, draw = new_page(GRAY_BG, GRAY_DOT)
    draw_background(draw)
    rounded_label(draw, (80, 90), "シリーズ1", load_font(40), label="series label")
    headline(draw, "Before と After を比べてみる", 280, SHADOW)
    draw_columns(draw)
    draw_compare(draw)
    big_label(draw, "続けやすさがポイント", 1090, YELLOW)
    draw_footer(draw)
    save_and_check(img, OUT_PATH)


if __name__ == "__main__":
    main()
