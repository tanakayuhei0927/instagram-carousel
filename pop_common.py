"""Shared drawing rules for the pop & colorful carousel (pop_slide_XX.png).

Palette, bundled rounded-gothic font, outlined text, rounded labels, the
swipe hint, and the post-draw text checks. Separate from the RPG
(slide_XX.png) and notebook (note_slide_XX.png) series.
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
FONT_PATH = ROOT / "fonts" / "ZenMaruGothic-Black.ttf"

W, H = 1080, 1350
SAFE = 50  # keep every text box at least this far from the canvas edge

# Palette: pink base, accents pink + yellow; light blue only for decorative shapes
PINK = (255, 150, 186)
PINK_DEEP = (236, 72, 136)
YELLOW = (255, 218, 62)
SKY = (138, 214, 244)  # shapes only, never text
WHITE = (255, 255, 255)
BLACK = (24, 20, 28)


def load_font(size):
    if not FONT_PATH.exists():
        sys.exit(f"[ERROR] 日本語フォントが見つかりません: {FONT_PATH}")
    return ImageFont.truetype(str(FONT_PATH), size)


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

def outlined_text(draw, xy, text, font, fill=WHITE, stroke=BLACK, stroke_w=10,
                  shadow=None, shadow_off=(0, 0), anchor="mm", label=None, container=None,
                  fill_holes=False):
    """Text with a thick outline and an optional offset shadow; the bbox includes both.

    fill_holes paints the tiny gaps left inside closed counters (e.g. 田 in 野)
    with the outline color, so the background doesn't show through as specks.
    """
    x, y = xy
    if shadow:
        sx, sy = shadow_off
        draw.text((x + sx, y + sy), text, font=font, fill=shadow, anchor=anchor,
                  stroke_width=stroke_w, stroke_fill=shadow)
    draw.text(xy, text, font=font, fill=fill, anchor=anchor,
              stroke_width=stroke_w, stroke_fill=stroke)
    if fill_holes:
        mask = Image.new("L", (W, H), 0)
        ImageDraw.Draw(mask).text(xy, text, font=font, fill=255, anchor=anchor,
                                  stroke_width=stroke_w, stroke_fill=255)
        mask = mask.point(lambda v: 255 if v else 0)
        ImageDraw.floodfill(mask, (0, 0), 128)  # everything reachable from outside
        holes = mask.point(lambda v: 255 if v == 0 else 0)
        # grow by 1px so the anti-aliased rim of each hole is covered too,
        # but never paint over the glyph body itself
        body = Image.new("L", (W, H), 0)
        ImageDraw.Draw(body).text(xy, text, font=font, fill=255, anchor=anchor)
        paint = ImageChops.subtract(holes.filter(ImageFilter.MaxFilter(3)), body)
        draw.bitmap((0, 0), paint, fill=stroke)
    l, t, r, b = draw.textbbox(xy, text, font=font, anchor=anchor, stroke_width=stroke_w)
    if shadow:
        l, t = min(l, l + shadow_off[0]), min(t, t + shadow_off[1])
        r, b = max(r, r + shadow_off[0]), max(b, b + shadow_off[1])
    bbox = (l, t, r, b)
    text_boxes.append((label or text, text, font, bbox, container))
    return bbox


def rounded_label(draw, xy, text, font, fill=YELLOW, text_fill=BLACK, pad_x=30, pad_y=14,
                  border=5, label=None):
    """Pill-shaped label with a black border; xy is the top-left corner."""
    x, y = xy
    l, t, r, b = draw.textbbox((0, 0), text, font=font, anchor="lt")
    w, h = r - l + pad_x * 2, b - t + pad_y * 2
    box = (x, y, x + w, y + h)
    draw.rounded_rectangle(box, radius=h // 2, fill=fill, outline=BLACK, width=border)
    draw.text((x + pad_x - l, y + pad_y - t), text, font=font, fill=text_fill, anchor="lt")
    tb = draw.textbbox((x + pad_x - l, y + pad_y - t), text, font=font, anchor="lt")
    text_boxes.append((label or text, text, font, tb, box))
    return box


def draw_footer(draw):
    outlined_text(draw, (W - 70, H - 80), "スワイプしてね →", load_font(50), stroke_w=7,
                  anchor="rs", label="swipe hint")


# ---------------------------------------------------------------- page parts (slides 2+)

GRAY_BG = (184, 186, 194)
GRAY_DOT = (198, 200, 207)
GRAY_DEEP = (120, 122, 132)
GREEN_BG = (134, 212, 108)
GREEN_DOT = (156, 224, 132)
GREEN_DEEP = (52, 150, 66)
GREEN_LIGHT = (188, 236, 160)

# neutral food colors (not emphasis colors)
TRAY = (252, 249, 242)
BOWL_IN = (236, 232, 226)
FISH = (196, 202, 212)
SOUP = (228, 206, 170)
CHOPSTICK = (96, 84, 78)
MUSH_CAP = (206, 176, 146)
MUSH_STEM = (244, 234, 218)


def polka(draw, box, dot, step=90, r=9):
    """Offset polka dots inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    for row, y in enumerate(range(y0 + 30, y1, step)):
        for x in range(x0 + 30 + (row % 2) * step // 2, x1, step):
            draw.ellipse((x - r, y - r, x + r, y + r), fill=dot)


def circle(draw, cx, cy, r, fill):
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill)


def wave_band(draw, x0, x1, y, thickness, amp, wavelength, fill):
    """Filled band whose top and bottom edges follow the same sine wave."""
    n = 80
    top, bottom = [], []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        off = amp * math.sin(2 * math.pi * (x - x0) / wavelength)
        top.append((x, y + off))
        bottom.append((x, y + off + thickness))
    draw.polygon(top + bottom[::-1], fill=fill)


def wave_floor(draw, x0, x1, y, amp, wavelength, fill):
    """Sine-wave edge filled down to the bottom of the canvas."""
    pts = [(x, y + amp * math.sin(2 * math.pi * x / wavelength)) for x in range(x0, x1 + 1, 10)]
    draw.polygon(pts + [(x1, H), (x0, H)], fill=fill)


def headline(draw, text, y, shadow, max_size=110, max_w=W - 2 * 70):
    size = max_size
    while size > 48 and load_font(size).getlength(text) + 28 > max_w:
        size -= 2
    return outlined_text(draw, (W // 2, y), text, load_font(size), stroke_w=12,
                         shadow=shadow, shadow_off=(8, 10), label="headline", fill_holes=True)


def bubble(draw, cx, cy, text, font, fill, tail_to, pad_x=38, pad_y=26, bw=6):
    """Filled speech bubble with one continuous black outline and a tail to tail_to."""
    l, t, r, b = draw.textbbox((cx, cy), text, font=font, anchor="mm", stroke_width=6)
    box = (l - pad_x, t - pad_y, r + pad_x, b + pad_y)
    radius = (box[3] - box[1]) // 2
    tx, ty = tail_to
    if box[0] <= tx <= box[2]:  # tail out of the top or bottom edge
        edge_y = box[1] + 4 if ty < box[1] else box[3] - 4
        bx = min(max(tx, box[0] + radius + 24), box[2] - radius - 24)
        tail = [(bx - 24, edge_y), (tx, ty), (bx + 24, edge_y)]
    else:  # tail out of the left or right edge
        edge_x = box[0] + 4 if tx < box[0] else box[2] - 4
        by = (box[1] + box[3]) / 2
        tail = [(edge_x, by - 18), (tx, ty), (edge_x, by + 18)]
    # black silhouette first, then the fill on top: one outline around box + tail
    draw.line(tail + [tail[0]], fill=BLACK, width=bw * 2, joint="curve")
    draw.polygon(tail, fill=BLACK)
    draw.rounded_rectangle((box[0] - bw, box[1] - bw, box[2] + bw, box[3] + bw),
                           radius=radius + bw, fill=BLACK)
    draw.polygon(tail, fill=fill)
    draw.rounded_rectangle(box, radius=radius, fill=fill)
    outlined_text(draw, (cx, cy), text, font, stroke_w=6, label=f"bubble {text}", container=box,
                  fill_holes=True)
    return box


def big_label(draw, text, y, fill, size=72, cx=W // 2):
    """Large pill label with outlined white text."""
    font = load_font(size)
    l, t, r, b = draw.textbbox((cx, y), text, font=font, anchor="mm", stroke_width=9)
    box = (l - 48, t - 26, r + 48, b + 26)
    draw.rounded_rectangle((box[0] + 8, box[1] + 10, box[2] + 8, box[3] + 10),
                           radius=(box[3] - box[1]) // 2, fill=BLACK)  # drop shadow
    draw.rounded_rectangle(box, radius=(box[3] - box[1]) // 2, fill=fill, outline=BLACK, width=6)
    outlined_text(draw, (cx, y), text, font, stroke_w=9, label=f"label {text}", container=box,
                  fill_holes=True)
    return box


# ---------------------------------------------------------------- flat meal illustration

def draw_meal(draw, cx, cy, s=1.0, bowl=YELLOW, veg=False):
    """Flat sticker-style tray meal with only a little rice.

    veg=True puts a cabbage/mushroom plate beside the fish and mushrooms in
    the soup. Drawn in a 700x310 box centered at (cx, cy), scaled by s.
    """
    def P(x, y):
        return cx + (x - 540) * s, cy + (y - 625) * s

    def box(x, y, rx, ry):
        (x0, y0), (x1, y1) = P(x - rx, y - ry), P(x + rx, y + ry)
        return x0, y0, x1, y1

    bw = max(3, round(5 * s))
    thin = max(2, round(3 * s))
    draw.rounded_rectangle(P(190, 470) + P(890, 780), radius=36 * s, fill=TRAY,
                           outline=BLACK, width=bw)

    def fish_plate(x, y, k):
        draw.ellipse(box(x, y, 150 * k, 58 * k), fill=WHITE, outline=BLACK, width=bw)
        draw.polygon([P(x + 58 * k, y), P(x + 96 * k, y - 24 * k), P(x + 96 * k, y + 24 * k)],
                     fill=FISH, outline=BLACK, width=bw)
        draw.ellipse(box(x - 15 * k, y, 78 * k, 27 * k), fill=FISH, outline=BLACK, width=bw)
        draw.ellipse(box(x - 66 * k, y - 4 * k, 6 * k, 6 * k), fill=BLACK)

    def salad_plate(x, y, k):
        draw.ellipse(box(x, y, 150 * k, 58 * k), fill=WHITE, outline=BLACK, width=bw)
        for dx, dy, r in ((-70, 4, 40), (-28, -10, 42), (10, 8, 38), (-44, 20, 30)):
            leaf = box(x + dx * k, y + dy * k, r * k * 1.15, r * k * 0.7)
            draw.ellipse(leaf, fill=GREEN_LIGHT if dx % 2 else GREEN_BG, outline=BLACK, width=thin)
            vein = box(x + dx * k, y + (dy + 14) * k, r * k * 0.7, r * k * 0.4)
            draw.arc(vein, 200, 340, fill=GREEN_DEEP, width=thin)
        for dx, dy, kk in ((66, 2, 1.0), (104, 12, 0.8)):  # mushrooms
            mx, my = x + dx * k, y + dy * k
            draw.rectangle(box(mx, my + 10 * k * kk, 8 * k * kk, 14 * k * kk),
                           fill=MUSH_STEM, outline=BLACK, width=thin)
            draw.chord(box(mx, my, 24 * k * kk, 20 * k * kk), 180, 360,
                       fill=MUSH_CAP, outline=BLACK, width=thin)

    if veg:
        fish_plate(392, 566, 0.86)
        salad_plate(700, 566, 0.86)
    else:
        fish_plate(540, 570, 1.0)

    # rice bowl: mostly empty inside, with a small mound of rice
    bx, by = 340, 680
    draw.rounded_rectangle(box(bx, by + 86, 36, 12), radius=6 * s, fill=bowl, outline=BLACK, width=bw)
    draw.chord(box(bx, by, 96, 84), 0, 180, fill=bowl, outline=BLACK, width=bw)
    draw.ellipse(box(bx, by, 96, 24), fill=BOWL_IN, outline=BLACK, width=bw)
    draw.chord(box(bx, by + 8, 34, 16), 180, 360, fill=WHITE, outline=BLACK, width=thin)

    # soup bowl
    sx, sy = 740, 680
    draw.rounded_rectangle(box(sx, sy + 78, 32, 12), radius=6 * s, fill=bowl, outline=BLACK, width=bw)
    draw.chord(box(sx, sy, 90, 76), 0, 180, fill=bowl, outline=BLACK, width=bw)
    draw.ellipse(box(sx, sy, 90, 22), fill=SOUP, outline=BLACK, width=bw)
    if veg:
        for dx in (-40, 0, 40):
            draw.chord(box(sx + dx, sy + 6, 17, 12), 180, 360, fill=MUSH_CAP,
                       outline=BLACK, width=thin)
    else:
        for dx in (-30, 0, 30):
            pts = [P(sx + dx + 8 * math.sin(i / 3), sy - 40 - i * 4) for i in range(13)]
            draw.line(pts, fill=BLACK, width=thin, joint="curve")

    for y0, y1 in ((750, 740), (764, 758)):  # chopsticks
        draw.line([P(470, y0), P(640, y1)], fill=CHOPSTICK, width=bw + 2)
    return P(190, 470) + P(890, 780)


def new_page(bg, dot):
    img = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(img)
    polka(draw, (0, 0, W, H), dot)
    return img, draw


# ---------------------------------------------------------------- points & summary pages

PINK_DOT = (255, 178, 206)
PINK_LIGHT = (255, 194, 216)
WAVE_GRAY = (206, 208, 214)


def decor(draw, big, small, wave):
    """Standard page decoration: wave band, big top-right circle, small
    bottom-left circle and a wavy floor."""
    wave_band(draw, -20, W + 20, 390, 30, 16, 180, wave)
    circle(draw, 930, 200, 230, big)
    circle(draw, 90, 1000, 150, small)
    wave_floor(draw, 0, W, 1180, 24, 300, wave)


def icon_disc(draw, cx, cy, r=74):
    """White sticker disc that holds a small food icon."""
    draw.ellipse((cx - r - 6, cy - r + 4, cx + r + 6, cy + r + 10), fill=BLACK)  # drop shadow
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=WHITE, outline=BLACK, width=6)


def item_row(draw, y, name, memo, fill, icon, x=70, gap=52):
    """One line: icon disc, big item name, then a memo bubble right after the
    name whose short tail points back at it."""
    icon_disc(draw, x + 74, y)
    icon(draw, x + 74, y)
    name_font = load_font(54)
    l, t, r, b = outlined_text(draw, (x + 176, y), name, name_font, stroke_w=9, anchor="lm",
                               label=f"item {name}", fill_holes=True)
    memo_font = load_font(38)
    pad_x = 30
    tw = draw.textlength(memo, font=memo_font) + 12
    bubble(draw, r + gap + pad_x + tw / 2, y, memo, memo_font, fill, tail_to=(r + 10, y),
           pad_x=pad_x)


def small_note(draw, text):
    """Small caveat at the bottom-left, on the same baseline as the swipe hint."""
    outlined_text(draw, (70, H - 80), text, load_font(32), stroke_w=5, anchor="ls",
                  label=f"note {text}", fill_holes=True)


# ---------------------------------------------------------------- flat food icons (~60px radius)

def icon_fish(draw, cx, cy, k=0.6):
    draw.polygon([(cx + 40 * k, cy), (cx + 78 * k, cy - 26 * k), (cx + 78 * k, cy + 26 * k)],
                 fill=FISH, outline=BLACK, width=4)
    draw.ellipse((cx - 90 * k, cy - 30 * k, cx + 50 * k, cy + 30 * k), fill=FISH,
                 outline=BLACK, width=4)
    draw.ellipse((cx - 64 * k, cy - 8 * k, cx - 52 * k, cy + 4 * k), fill=BLACK)


def icon_mushroom(draw, cx, cy, k=1.0):
    draw.rounded_rectangle((cx - 11 * k, cy - 4 * k, cx + 11 * k, cy + 36 * k), radius=6 * k,
                           fill=MUSH_STEM, outline=BLACK, width=4)
    draw.chord((cx - 36 * k, cy - 34 * k, cx + 36 * k, cy + 22 * k), 180, 360,
               fill=MUSH_CAP, outline=BLACK, width=4)


def rice_bowl_full(draw, cx, cy, k=1.0, bowl=YELLOW):
    """Bowl with a normal rounded mound of rice."""
    draw.rounded_rectangle((cx - 34 * k, cy + 70 * k, cx + 34 * k, cy + 90 * k), radius=6 * k,
                           fill=bowl, outline=BLACK, width=5)
    draw.chord((cx - 92 * k, cy - 80 * k, cx + 92 * k, cy + 80 * k), 0, 180,
               fill=bowl, outline=BLACK, width=5)
    draw.chord((cx - 88 * k, cy - 66 * k, cx + 88 * k, cy + 66 * k), 180, 360,
               fill=WHITE, outline=BLACK, width=5)
    for dx, dy in ((-40, -30), (-6, -50), (30, -34), (54, -14), (-62, -12)):  # grains
        draw.ellipse((cx + (dx - 7) * k, cy + (dy - 4) * k, cx + (dx + 7) * k, cy + (dy + 4) * k),
                     outline=BOWL_IN, width=3)
