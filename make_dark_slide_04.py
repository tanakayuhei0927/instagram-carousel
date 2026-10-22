"""Checklist slide (dark_slide_04.png): nice-to-have items.

Empty white-framed checkboxes for ロッカー用の鍵 / ヘアゴム / イヤホン with a
gray memo under each, and a small note that rules differ by facility.
"""
from dark_common import (ROOT, checklist_rows, draw_corner_labels, draw_footer, draw_headline,
                         new_page, save_and_check, small_note)

OUT_PATH = ROOT / "dark_slide_04.png"

ROWS = [("ロッカー用の鍵", "貴重品の管理に"),
        ("ヘアゴム", "長い髪をまとめる用"),
        ("イヤホン", "音楽を聴きながら集中したい時に")]


def main():
    img, draw = new_page()
    draw_corner_labels(draw, 4)
    draw = draw_headline(img, draw, "持ち物③ あると安心なもの")
    checklist_rows(draw, ROWS, [460, 670, 880])
    small_note(draw, ["※施設によって持ち物のルールが異なります。",
                      "　事前に案内を確認してください"])
    draw_footer(draw)
    save_and_check(img, OUT_PATH)


if __name__ == "__main__":
    main()
