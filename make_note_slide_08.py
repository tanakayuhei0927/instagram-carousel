"""Summary slide (note_slide_08.png), last page of the series.

Three numbered takeaways, a question with circled answer choices, a marker
on "コメントで教えてね！" and a small save reminder. No swipe hint.
"""
from note_common import (INK, ROOT, W, draw_headline, draw_marker_point, draw_text, hand_path,
                         load_font, new_page, save_and_check, wobbly_ellipse)

OUT_PATH = ROOT / "note_slide_08.png"

SUMMARY = ["まず野菜から", "たんぱく質も確保", "主食は活動量で"]
CHOICES = ["朝", "夕方", "夜", "トレーニング後"]


def draw_summary(draw):
    num_font = load_font(40)
    text_font = load_font(54)
    for i, text in enumerate(SUMMARY):
        y = 490 + i * 96
        draw_text(draw, (150, y), str(i + 1), num_font, label=f"summary no.{i + 1}")
        wobbly_ellipse(draw, 150, y, 30, 28, 4, INK)
        draw_text(draw, (210, y), text, text_font, anchor="lm", label=f"summary {text}")
        for x in range(110, W - 110, 30):  # dashed notebook rule under each line
            hand_path(draw, [(x, y + 44), (x + 14, y + 44)], 2)


def draw_question(draw):
    draw_text(draw, (W // 2, 820), "Q. 一番お腹が空くのはいつ？", load_font(52), label="question")

    font = load_font(44)
    gap, y = 30, 935
    # loop wide enough that the text's corners stay inside the ellipse
    widths = [font.getlength(c) * 1.15 + 52 for c in CHOICES]
    x = (W - sum(widths) - gap * (len(CHOICES) - 1)) / 2
    for choice, w in zip(CHOICES, widths):
        cx = x + w / 2
        draw_text(draw, (cx, y), choice, font, label=f"choice {choice}")
        wobbly_ellipse(draw, cx, y, w / 2, 48, 4, INK)
        x += w + gap


def draw_save_hint(draw):
    f = load_font(34)
    l, t, r, b = draw_text(draw, (W // 2 + 24, 1200), "あとで見返せるように保存もどうぞ", f,
                           label="save hint")
    # small bookmark doodle in front of the text
    bx, by = l - 46, t - 6
    hand_path(draw, [(bx, by), (bx + 28, by), (bx + 28, by + 44), (bx + 14, by + 32),
                     (bx, by + 44), (bx, by)], 3)


def main():
    img, draw = new_page(8)
    draw_headline(draw, "今日からできること、まとめ")
    draw_summary(draw)
    draw_question(draw)
    draw = draw_marker_point(img, draw, "コメントで教えてね！", 1075)
    draw_save_hint(draw)
    save_and_check(img, OUT_PATH)


if __name__ == "__main__":
    main()
