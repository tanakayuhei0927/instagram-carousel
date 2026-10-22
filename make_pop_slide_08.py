"""Summary slide (pop_slide_08.png), last page of the series.

Closing palette that uses every series color in small doses: three summary
lines with number badges colored like points ①②③, a question with
button-style answer choices, a big "コメントで教えてね！" label and a small
save reminder. No swipe hint.
"""
from pop_common import (BLACK, GREEN_DEEP, GREEN_LIGHT, H, PINK, PINK_DEEP, PINK_DOT, ROOT,
                        SKY, W, YELLOW, big_label, circle, decor, headline, load_font,
                        new_page, outlined_text, rounded_label, save_and_check)

OUT_PATH = ROOT / "pop_slide_08.png"

# badge colors follow the bubble colors of points 1-3 (slides 5-7)
SUMMARY = [("まず野菜から", GREEN_DEEP), ("たんぱく質も確保", YELLOW), ("主食は活動量で", SKY)]
CHOICES = [("朝", PINK_DEEP), ("夕方", YELLOW), ("夜", SKY), ("トレーニング後", GREEN_DEEP)]


def draw_summary(draw):
    num_font = load_font(44)
    text_font = load_font(56)
    for i, (text, color) in enumerate(SUMMARY):
        y = 468 + i * 94
        circle(draw, 148, y + 4, 40, BLACK)  # badge shadow
        draw.ellipse((104, y - 40, 184, y + 40), fill=color, outline=BLACK, width=5)
        outlined_text(draw, (144, y), str(i + 1), num_font, stroke_w=6,
                      label=f"summary no.{i + 1}", fill_holes=True)
        outlined_text(draw, (214, y), text, text_font, stroke_w=9, anchor="lm",
                      label=f"summary {text}", fill_holes=True)


def draw_question(draw):
    outlined_text(draw, (W // 2, 785), "一番お腹が空くのはいつ？", load_font(56), stroke_w=9,
                  label="question", fill_holes=True)
    font = load_font(42)
    gap, y = 22, 895
    widths = [draw.textlength(c, font=font) + 12 + 64 for c, _ in CHOICES]
    x = (W - sum(widths) - gap * (len(CHOICES) - 1)) / 2
    for (choice, color), w in zip(CHOICES, widths):
        box = (x, y - 42, x + w, y + 42)
        draw.rounded_rectangle((box[0] + 6, box[1] + 8, box[2] + 6, box[3] + 8), radius=42,
                               fill=BLACK)  # button shadow
        draw.rounded_rectangle(box, radius=42, fill=color, outline=BLACK, width=5)
        outlined_text(draw, (x + w / 2, y), choice, font, stroke_w=6, label=f"choice {choice}",
                      container=box, fill_holes=True)
        x += w + gap


def draw_save_hint(draw):
    f = load_font(36)
    l, t, r, b = outlined_text(draw, (W // 2 + 26, H - 95), "あとで見返せるように保存もどうぞ", f,
                               stroke_w=6, label="save hint", fill_holes=True)
    bx, by = l - 52, (t + b) / 2 - 24  # bookmark icon in front of the text
    draw.polygon([(bx, by), (bx + 34, by), (bx + 34, by + 50), (bx + 17, by + 36), (bx, by + 50)],
                 fill=YELLOW, outline=BLACK, width=4)


def main():
    img, draw = new_page(PINK, PINK_DOT)
    decor(draw, YELLOW, SKY, PINK_DEEP)
    circle(draw, 1030, 760, 60, GREEN_LIGHT)  # small extra accents
    circle(draw, 40, 690, 36, YELLOW)
    rounded_label(draw, (80, 90), "シリーズ1", load_font(40), label="series label")
    headline(draw, "今日からできること、まとめ", 270, PINK_DEEP)
    draw_summary(draw)
    draw_question(draw)
    big_label(draw, "コメントで教えてね！", 1050, YELLOW)
    draw_save_hint(draw)
    save_and_check(img, OUT_PATH)


if __name__ == "__main__":
    main()
