"""Shared drawing rules for the monochrome dark carousel (dark_slide_XX.png).

Palette (near-black, grays, one neon-green accent), bundled Noto Sans JP
variable font, the hard-edged frame, corner labels, swipe hint, neon check
marks / underlines, and the post-draw text checks. Separate from the RPG,
notebook and pop series.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
FONT_PATH = ROOT / "fonts" / "NotoSansJP-VF.ttf"

W, H = 1080, 1350
FRAME = 48          # outer frame inset
SAFE = FRAME + 24   # text keeps this far from the canvas edge (inside the frame)

# Palette: background within #111-#222, grays, and a single neon accent
BG = (0x16, 0x16, 0x16)
PANEL = (0x1E, 0x1E, 0x1E)
LINE = (0x5C, 0x5C, 0x5C)
LINE_DIM = (0x33, 0x33, 0x33)
WHITE = (0xF4, 0xF4, 0xF4)
GRAY_TEXT = (0x9A, 0x9A, 0x9A)
NEON = (57, 255, 20)


def load_font(size, weight=900):
    if not FONT_PATH.exists():
        sys.exit(f"[ERROR] 日本語フォントが見つかりません: {FONT_PATH}")
    font = ImageFont.truetype(str(FONT_PATH), size)
    font.set_variation_by_axes([weight])
    return font


# ---------------------------------------------------------------- checks

text_boxes = []  # (label, text, font, bbox, container)


def missing_glyphs(font, text):
    """Chars the font renders as the same box as a surely-missing codepoint."""
    def render(c):
        im = Image.new("L", (font.size * 2, font.size * 2), 0)
        ImageDraw.Draw(im).text((font.size // 2, font.size // 2), c, font=font, fill=255)
        return im.tobytes()

    tofu = render("")
    return [c for c in set(text) if not c.isspace() and render(c) == tofu]


def check_text():
    ok = True
    full = (SAFE, SAFE, W - SAFE, H - SAFE)
    for label, text, font, bbox, container in text_boxes:
        box = container or full
        miss = missing_glyphs(font, text)
        inside = (bbox[0] >= box[0] and bbox[1] >= box[1]
                  and bbox[2] <= box[2] and bbox[3] <= box[3])
        status = "OK" if inside and not miss else "NG"
        ok &= status == "OK"
        print(f"[{status}] {label}: bbox={tuple(round(v) for v in bbox)} box={tuple(round(v) for v in box)}"
              + (f" missing={miss}" if miss else ""))
    return ok


def save_and_check(img, out_path):
    img.convert("RGB").save(out_path)
    print(f"saved: {out_path} ({W}x{H})")
    if not check_text():
        sys.exit("[ERROR] 文字の欠け・はみ出しがあります")
    print("all text checks passed")


# ---------------------------------------------------------------- text

def draw_text(draw, xy, text, font, fill=WHITE, anchor="mm", label=None, container=None):
    draw.text(xy, text, font=font, fill=fill, anchor=anchor)
    bbox = draw.textbbox(xy, text, font=font, anchor=anchor)
    text_boxes.append((label or text, text, font, bbox, container))
    return bbox


def tracked_text(draw, xy, text, font, fill=GRAY_TEXT, tracking=6, align="left", label=None):
    """Letter-spaced Latin text (e.g. "GYM START"); xy is the left or right baseline end."""
    widths = [font.getlength(c) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x, y = xy
    if align == "right":
        x -= total
    start = x
    for c, w in zip(text, widths):
        draw.text((x, y), c, font=font, fill=fill, anchor="ls")
        x += w + tracking
    l, t, r, b = draw.textbbox((start, y), text, font=font, anchor="ls")
    bbox = (start, t, start + total, b)
    text_boxes.append((label or text, text, font, bbox, None))
    return bbox


# ---------------------------------------------------------------- page parts

def draw_frame(draw):
    """Thin gray outer frame with bright corner brackets."""
    x0, y0, x1, y1 = FRAME, FRAME, W - FRAME, H - FRAME
    draw.rectangle((x0, y0, x1, y1), outline=LINE, width=2)
    arm = 44
    for cx, cy, dx, dy in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        draw.line([(cx, cy + dy * arm), (cx, cy), (cx + dx * arm, cy)], fill=WHITE, width=5)


def draw_corner_labels(draw, number):
    f = load_font(30, 700)
    tracked_text(draw, (SAFE + 12, 128), "GYM START", f, tracking=7, label="label GYM START")
    tracked_text(draw, (W - SAFE - 12, 128), f"{number:02d}", f, tracking=4, align="right",
                 label="label number")
    draw.line((SAFE + 12, 158, W - SAFE - 12, 158), fill=LINE_DIM, width=2)


def draw_footer(draw):
    draw.line((SAFE + 12, H - 158, W - SAFE - 12, H - 158), fill=LINE_DIM, width=2)
    draw_text(draw, (W - SAFE - 12, H - 110), "スワイプしてね →", load_font(34, 500),
              fill=GRAY_TEXT, anchor="rs", label="swipe hint")


def neon_layer(img, paint):
    """Draw neon strokes with a soft glow: paint(draw) is called on a blurred
    glow layer and again on a crisp layer."""
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    paint(ImageDraw.Draw(glow), glow=True)
    glow = glow.filter(ImageFilter.GaussianBlur(10))
    img.alpha_composite(glow)
    crisp = Image.new("RGBA", img.size, (0, 0, 0, 0))
    paint(ImageDraw.Draw(crisp), glow=False)
    img.alpha_composite(crisp)


def check_mark(draw, x, y, size, width, color):
    """Check mark whose bounding box starts at (x, y)."""
    draw.line([(x, y + size * 0.55), (x + size * 0.38, y + size * 0.9), (x + size, y + size * 0.1)],
              fill=color, width=width, joint="curve")


def new_page():
    img = Image.new("RGBA", (W, H), BG + (255,))
    draw = ImageDraw.Draw(img)
    draw_frame(draw)
    return img, draw
