"""Point 2 slide (pop_slide_06.png): keep some protein.

Pink base (accents: pink + yellow). Three item rows (鶏肉・魚 / 卵 / 豆腐)
with food icons and yellow memo bubbles, a big "野菜だけでは足りない？"
label, and a small "個人差があります" note.
"""
from pop_common import (BLACK, PINK, PINK_DEEP, PINK_DOT, ROOT, WHITE, YELLOW, big_label,
                        decor, draw_footer, headline, icon_fish, item_row, load_font,
                        new_page, rounded_label, save_and_check, small_note)

OUT_PATH = ROOT / "pop_slide_06.png"

MEAT = (222, 168, 118)  # neutral food color
TOFU_SIDE = (226, 226, 220)


def icon_meat_fish(draw, cx, cy):
    # drumstick: bone first, then the meat over its end
    draw.line([(cx - 2, cy - 14), (cx + 34, cy - 40)], fill=BLACK, width=16)
    draw.line([(cx - 2, cy - 14), (cx + 34, cy - 40)], fill=WHITE, width=8)
    for dx, dy in ((30, -50), (44, -38)):
        draw.ellipse((cx + dx - 9, cy + dy - 9, cx + dx + 9, cy + dy + 9), fill=WHITE,
                     outline=BLACK, width=4)
    draw.ellipse((cx - 52, cy - 34, cx + 6, cy + 10), fill=MEAT, outline=BLACK, width=4)
    icon_fish(draw, cx + 6, cy + 30, 0.5)


def icon_eggs(draw, cx, cy):
    draw.ellipse((cx - 52, cy - 40, cx - 6, cy + 24), fill=WHITE, outline=BLACK, width=4)
    draw.ellipse((cx - 8, cy - 18, cx + 54, cy + 30), fill=WHITE, outline=BLACK, width=4)
    draw.ellipse((cx + 8, cy - 6, cx + 38, cy + 20), fill=YELLOW, outline=BLACK, width=4)


def icon_tofu(draw, cx, cy, s=58, d=22):
    x0, y0 = cx - s / 2 - d / 2, cy - s / 2 + d / 2
    draw.polygon([(x0, y0), (x0 + d, y0 - d), (x0 + s + d, y0 - d), (x0 + s, y0)],
                 fill=WHITE, outline=BLACK, width=4)
    draw.polygon([(x0 + s, y0), (x0 + s + d, y0 - d), (x0 + s + d, y0 + s - d), (x0 + s, y0 + s)],
                 fill=TOFU_SIDE, outline=BLACK, width=4)
    draw.rectangle((x0, y0, x0 + s, y0 + s), fill=WHITE, outline=BLACK, width=4)


ROWS = [("鶏肉・魚", "鶏むね・サバなど", icon_meat_fish),
        ("卵", "ゆで卵・オムレツに", icon_eggs),
        ("豆腐", "冷ややっこ・みそ汁に", icon_tofu)]


def main():
    img, draw = new_page(PINK, PINK_DOT)
    decor(draw, YELLOW, YELLOW, PINK_DEEP)
    rounded_label(draw, (80, 90), "シリーズ1", load_font(40), label="series label")
    headline(draw, "ポイント②：たんぱく質も確保", 270, PINK_DEEP)
    for i, (name, memo, icon) in enumerate(ROWS):
        item_row(draw, 500 + i * 190, name, memo, YELLOW, icon)
    big_label(draw, "野菜だけでは足りない？", 1060, PINK_DEEP, size=66)
    small_note(draw, "※個人差があります")
    draw_footer(draw)
    save_and_check(img, OUT_PATH)


if __name__ == "__main__":
    main()
