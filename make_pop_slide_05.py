"""Point 1 slide (pop_slide_05.png): vegetables and mushrooms first.

Pink base like the cover (accents: pink + green). Three item rows
(キャベツ / きのこ / ブロッコリー), each with a food icon and a green memo
bubble, plus a small "個人差があります" note.
"""
from pop_common import (BLACK, GREEN_BG, GREEN_DEEP, GREEN_LIGHT, PINK, PINK_DEEP, PINK_DOT,
                        ROOT, decor, draw_footer, headline, icon_mushroom, item_row,
                        load_font, new_page, rounded_label, save_and_check, small_note)

OUT_PATH = ROOT / "pop_slide_05.png"


def icon_cabbage(draw, cx, cy):
    for side in (-1, 1):  # outer leaves peeking out at the sides
        draw.chord((cx + side * 22 - 46, cy - 30, cx + side * 22 + 46, cy + 52),
                   90 if side < 0 else -90, 270 if side < 0 else 90,
                   fill=GREEN_BG, outline=BLACK, width=4)
    draw.ellipse((cx - 44, cy - 46, cx + 44, cy + 40), fill=GREEN_LIGHT, outline=BLACK, width=4)
    for dx in (-18, 0, 18):  # leaf veins fanning from the core
        draw.line([(cx, cy + 30), (cx + dx * 0.4, cy), (cx + dx, cy - 30)], fill=GREEN_DEEP,
                  width=4, joint="curve")


def icon_mushrooms(draw, cx, cy):
    icon_mushroom(draw, cx - 18, cy - 4, 1.0)
    icon_mushroom(draw, cx + 30, cy + 10, 0.72)


def icon_broccoli(draw, cx, cy):
    draw.polygon([(cx - 14, cy), (cx + 14, cy), (cx + 18, cy + 48), (cx - 18, cy + 48)],
                 fill=GREEN_LIGHT, outline=BLACK, width=4)
    for dx, dy, r in ((-30, -10, 24), (30, -10, 24), (-14, -34, 26), (16, -34, 26), (0, -8, 26)):
        draw.ellipse((cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r), fill=GREEN_BG,
                     outline=BLACK, width=4)


ROWS = [("キャベツ", "汁物やサラダに", icon_cabbage),
        ("きのこ", "スープや炒め物に", icon_mushrooms),
        ("ブロッコリー", "ゆでて副菜に", icon_broccoli)]


def main():
    img, draw = new_page(PINK, PINK_DOT)
    decor(draw, GREEN_LIGHT, GREEN_LIGHT, PINK_DEEP)
    rounded_label(draw, (80, 90), "シリーズ1", load_font(40), label="series label")
    headline(draw, "ポイント①：野菜・きのこを先に", 270, PINK_DEEP)
    for i, (name, memo, icon) in enumerate(ROWS):
        item_row(draw, 515 + i * 215, name, memo, GREEN_DEEP, icon)
    small_note(draw, "※個人差があります")
    draw_footer(draw)
    save_and_check(img, OUT_PATH)


if __name__ == "__main__":
    main()
