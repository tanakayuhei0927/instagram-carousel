"""Shared drawing rules for the retro 16bit RPG diet carousel.

Palette, bundled Japanese font, text drawing + checks, RPG windows, pixel parts
and the pixel-art squirrel. Every make_slide_XX.py builds on this module.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FONT_PATH = ROOT / "fonts" / "NotoSansJP-VF.ttf"

W, H = 1080, 1350

# Palette: navy / grass green / cream / gold (+ minimal accents)
NAVY_DEEP = (10, 18, 44)
NAVY = (18, 32, 72)
NAVY_LIGHT = (34, 54, 108)
GREEN_DARK = (30, 92, 48)
GREEN = (58, 150, 72)
GREEN_LIGHT = (108, 196, 92)
CREAM = (248, 238, 206)
CREAM_DARK = (214, 196, 150)
GOLD = (236, 184, 58)
GOLD_DARK = (168, 116, 28)
GOLD_LIGHT = (255, 222, 120)
RED = (226, 72, 58)
INK = (12, 10, 24)

# Squirrel colors
SQ_OUT = (40, 20, 10)
SQ_MAIN = (204, 116, 52)
SQ_SHADE = (150, 74, 30)
SQ_LIGHT = (236, 156, 84)
SQ_BELLY = (250, 228, 184)
SQ_PINK = (240, 140, 140)
SQ_EYE = (20, 12, 10)
SQ_WHITE = (255, 255, 255)
SQ_TEAR = (120, 190, 255)

def load_font(size, weight):
    if not FONT_PATH.exists():
        sys.exit(f"[ERROR] 日本語フォントが見つかりません: {FONT_PATH}")
    font = ImageFont.truetype(str(FONT_PATH), size)
    font.set_variation_by_axes([weight])
    return font


# ---------------------------------------------------------------- text helpers

text_boxes = []  # (label, bbox, container) — checked after drawing


def draw_text(draw, xy, text, font, fill, anchor="mm", shadow=None, shadow_off=6,
              stroke=0, stroke_fill=None, label=None, container=None):
    x, y = xy
    if shadow:
        draw.text((x + shadow_off, y + shadow_off), text, font=font, fill=shadow,
                  anchor=anchor, stroke_width=stroke, stroke_fill=shadow)
    draw.text((x, y), text, font=font, fill=fill, anchor=anchor,
              stroke_width=stroke, stroke_fill=stroke_fill)
    bbox = draw.textbbox((x, y), text, font=font, anchor=anchor, stroke_width=stroke)
    if shadow:
        bbox = (bbox[0], bbox[1], bbox[2] + shadow_off, bbox[3] + shadow_off)
    text_boxes.append((label or text, text, font, bbox, container or (0, 0, W, H)))
    return bbox


def fit_font(text, max_width, size, weight, stroke=0):
    """Shrink font size until the text fits into max_width."""
    while size > 10:
        font = load_font(size, weight)
        l, _, r, _ = font.getbbox(text, stroke_width=stroke)
        if r - l <= max_width:
            return font
        size -= 2
    return load_font(size, weight)


# ---------------------------------------------------------------- pixel helpers

def px_rect(draw, x0, y0, x1, y1, fill):
    draw.rectangle([x0, y0, x1 - 1, y1 - 1], fill=fill)


def rpg_window(draw, x0, y0, x1, y1, bg=NAVY, step=6, dither=True):
    """16bit-style message window: ink / gold / cream / gold frame with notched corners."""
    s = step
    # outer ink with notched corners
    px_rect(draw, x0 + s, y0, x1 - s, y1, INK)
    px_rect(draw, x0, y0 + s, x1, y1 - s, INK)
    # gold
    px_rect(draw, x0 + 2 * s, y0 + s, x1 - 2 * s, y1 - s, GOLD_DARK)
    px_rect(draw, x0 + s, y0 + 2 * s, x1 - s, y1 - 2 * s, GOLD_DARK)
    px_rect(draw, x0 + 2 * s, y0 + s, x1 - 2 * s, y0 + 2 * s, GOLD_LIGHT)
    px_rect(draw, x0 + s, y0 + 2 * s, x0 + 2 * s, y1 - 2 * s, GOLD)
    # cream line
    px_rect(draw, x0 + 2 * s, y0 + 2 * s, x1 - 2 * s, y1 - 2 * s, CREAM)
    # inner
    px_rect(draw, x0 + 3 * s, y0 + 3 * s, x1 - 3 * s, y1 - 3 * s, INK)
    px_rect(draw, x0 + 3 * s + 3, y0 + 3 * s + 3, x1 - 3 * s - 3, y1 - 3 * s - 3, bg)
    # dithered gradient at the bottom of the window for depth
    iy0 = y0 + 3 * s + 3
    iy1 = y1 - 3 * s - 3
    for yy in range(iy0, iy1, 6) if dither else ():
        t = (yy - iy0) / max(1, iy1 - iy0)
        if t < 0.78:
            continue
        for xx in range(x0 + 3 * s + 3, x1 - 3 * s - 3, 6):
            if ((xx // 6) + (yy // 6)) % 2 == 0 or t > 0.9:
                px_rect(draw, xx, yy, min(xx + 6, x1 - 3 * s - 3), min(yy + 6, iy1), NAVY_DEEP)
    return (x0 + 3 * s + 3, y0 + 3 * s + 3, x1 - 3 * s - 3, y1 - 3 * s - 3)

# ---------------------------------------------------------------- squirrel

def ellipse_cells(cx, cy, rx, ry):
    cells = set()
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1:
                cells.add((x, y))
    return cells


def outline(cells):
    out = set()
    for (x, y) in cells:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n not in cells:
                out.add(n)
    return out


def shade_layer(grid, cells, cx, cy, rx, ry, main, shade, light):
    for (x, y) in cells:
        u = (x + 0.5 - cx) / rx
        v = (y + 0.5 - cy) / ry
        if u * 0.6 + v * 0.8 > 0.55:
            grid[(x, y)] = shade
        elif u * 0.6 + v * 0.8 < -0.6:
            grid[(x, y)] = light
        else:
            grid[(x, y)] = main


WORRIED_BROWS = [(5, 8), (6, 8), (7, 7), (8, 7), (13, 7), (14, 7), (15, 8), (16, 8)]
SWEAT_DROPS = {
    "calm": (),
    "worried": ((21, 4),),
    "confused": ((-2, 6), (21, 4)),
    "limit": ((-2, 6), (21, 4)),
    "troubled": ((-2, 6), (21, 4)),
    "thinking": (),
    "inspired": (),
    "determined": (),
    "happy": (),
}


def paint_face(grid, expression):
    def put(cells, color):
        for k in cells:
            grid[k] = color

    def round_eyes():
        for ex in (6, 14):  # 2x3 with highlight
            for dy in range(3):
                for dx in range(2):
                    grid[(ex + dx, 10 + dy)] = SQ_EYE
            grid[(ex, 10)] = SQ_WHITE

    cheeks = [(3, 13), (4, 13), (17, 13), (18, 13)]
    nose = [(10, 13), (11, 13)]

    if expression == "happy":
        put([(5, 11), (6, 10), (7, 10), (8, 11), (13, 11), (14, 10), (15, 10), (16, 11)], SQ_EYE)  # ^ ^
        put(cheeks, SQ_PINK)
        put(nose, SQ_OUT)
        put([(9, 15), (10, 15), (11, 15), (12, 15), (9, 16), (12, 16), (10, 17), (11, 17)], SQ_OUT)
        put([(10, 16), (11, 16)], SQ_PINK)  # open smile
    elif expression == "determined":
        put([(4, 7), (5, 7), (6, 8), (7, 8), (8, 9), (13, 9), (14, 8), (15, 8), (16, 7), (17, 7)], SQ_OUT)
        round_eyes()  # looking straight ahead
        put(cheeks, SQ_PINK)
        put(nose, SQ_OUT)
        put([(9, 16), (10, 16), (11, 16), (12, 15)], SQ_OUT)  # confident half smile
    elif expression == "inspired":
        put([(5, 7), (6, 6), (7, 7), (14, 7), (15, 6), (16, 7)], SQ_OUT)  # raised arched brows
        round_eyes()
        for ex in (6, 14):
            grid[(ex + 1, 12)] = SQ_WHITE  # second glint: sparkling eyes
        put(cheeks, SQ_PINK)
        put(nose, SQ_OUT)
        put([(9, 15), (10, 15), (11, 15), (12, 15), (9, 16), (12, 16), (10, 17), (11, 17)], SQ_OUT)
        put([(10, 16), (11, 16)], SQ_PINK)  # open happy mouth
    elif expression == "thinking":
        put([(4, 7), (5, 6), (6, 6), (7, 6), (13, 7), (14, 7), (15, 7)], SQ_OUT)  # one brow raised
        for ex in (6, 14):  # pupils up and to the side: looking up while pondering
            put([(ex + 1, 9), (ex + 1, 10), (ex, 10), (ex, 11), (ex + 1, 11)], SQ_EYE)
            grid[(ex + 1, 9)] = SQ_WHITE
        put(cheeks, SQ_PINK)
        put(nose, SQ_OUT)
        put([(9, 16), (10, 16)], SQ_OUT)  # pursed, off-center mouth (paw covers the right side)
    elif expression == "calm":
        round_eyes()
        put(cheeks, SQ_PINK)
        put(nose, SQ_OUT)
        put([(9, 15), (10, 16), (11, 16), (12, 15)], SQ_OUT)  # smile
    elif expression == "worried":
        put(WORRIED_BROWS, SQ_OUT)
        round_eyes()
        put(cheeks, SQ_PINK)
        put(nose, SQ_OUT)
        put([(10, 16), (11, 16)], SQ_OUT)  # flat mouth
    elif expression == "confused":
        put([(5, 7), (6, 7), (7, 7), (14, 8), (15, 8), (16, 8)], SQ_OUT)  # uneven brows
        for ex in (6, 14):  # small dot eyes
            put([(ex, 11), (ex + 1, 11), (ex, 12), (ex + 1, 12)], SQ_EYE)
        put(cheeks, SQ_PINK)
        put(nose, SQ_OUT)
        put([(8, 16), (9, 15), (10, 16), (11, 15), (12, 16), (13, 15)], SQ_OUT)  # wavy mouth
    elif expression == "limit":
        put(WORRIED_BROWS, SQ_OUT)
        put([(5, 10), (6, 10), (7, 11), (6, 12), (5, 12)], SQ_EYE)  # >
        put([(16, 10), (15, 10), (14, 11), (15, 12), (16, 12)], SQ_EYE)  # <
        put([(6, 13), (6, 14), (6, 15), (15, 13), (15, 14), (15, 15)], SQ_TEAR)
        put(cheeks, SQ_PINK)
        put(nose, SQ_OUT)
        put([(9, 15), (10, 15), (11, 15), (12, 15), (9, 16), (12, 16)], SQ_OUT)  # crying mouth
        put([(10, 16), (11, 16)], SQ_PINK)
    else:  # troubled (cover)
        # worried eyebrows (inner ends raised)
        for k in [(5, 8), (6, 8), (7, 7), (8, 7), (13, 7), (14, 7), (15, 8), (16, 8)]:
            grid[k] = SQ_OUT
        # eyes (2x3) with highlight
        for ex in (6, 14):
            for dy in range(3):
                for dx in range(2):
                    grid[(ex + dx, 10 + dy)] = SQ_EYE
            grid[(ex, 10)] = SQ_WHITE
        # tears
        for k in [(6, 13), (6, 14), (15, 13), (15, 14), (15, 15)]:
            grid[k] = SQ_TEAR
        # cheeks
        for k in [(3, 13), (4, 13), (17, 13), (18, 13)]:
            grid[k] = SQ_PINK
        # nose + wavy mouth
        for k in [(10, 13), (11, 13)]:
            grid[k] = SQ_OUT
        for k in [(9, 16), (10, 15), (11, 15), (12, 16)]:  # troubled frown
            grid[k] = SQ_OUT


def build_squirrel(expression="troubled", pose="hug", item=None, item_colors=None):
    """Return {(x, y): color} pixel grid of the squirrel.

    expression: "calm" / "worried" / "confused" / "limit" / "thinking" / "troubled" (cover).
    pose: "hug" (paws on the stomach) / "think" (one paw on the chin) /
          "hold" (holding `item` — icon rows drawn through `item_colors` — in front of the chest) /
          "fight" (fists raised, fighting stance).
    """
    grid = {}

    def put_layer(cells, painter):
        for c in outline(cells):
            grid[c] = SQ_OUT
        painter(cells)

    # --- tail (behind): stacked blobs curling up over the head
    tail_parts = [(23, 28, 6.5, 5.5), (27.5, 21, 6.5, 7), (27, 12, 6.5, 6), (22.5, 5.5, 5.5, 4.5)]
    tail = set()
    for p in tail_parts:
        tail |= ellipse_cells(*p)

    def paint_tail(cells):
        for (x, y) in cells:
            grid[(x, y)] = SQ_MAIN
        for (x, y) in cells:  # shade along the lower-left edge
            if any((x + dx, y + dy) not in cells for dx, dy in ((-1, 0), (0, 1), (-1, 1), (-2, 0))):
                grid[(x, y)] = SQ_SHADE
        for (x, y) in cells:  # fluffy highlight along the upper-right edge
            if any((x + dx, y + dy) not in cells for dx, dy in ((2, 0), (0, -2), (2, -1))) \
                    and all((x + dx, y + dy) in cells for dx, dy in ((1, 0), (0, -1))):
                grid[(x, y)] = SQ_LIGHT
        # fur tufts (short dark strokes)
        for (x, y) in [(28, 16), (29, 17), (25, 24), (26, 25), (27, 8), (28, 9), (22, 30)]:
            if (x, y) in cells:
                grid[(x, y)] = SQ_SHADE

    put_layer(tail, paint_tail)

    # --- feet
    for fx in (6, 15):
        feet = ellipse_cells(fx, 32, 3.2, 1.7)
        put_layer(feet, lambda c: [grid.__setitem__(k, SQ_SHADE) for k in c])

    # --- body
    body = ellipse_cells(10.5, 24.5, 8, 8)
    put_layer(body, lambda c: shade_layer(grid, c, 10.5, 24.5, 8, 8, SQ_MAIN, SQ_SHADE, SQ_LIGHT))
    for k in ellipse_cells(10.5, 26, 5, 5.8):
        if k in body:
            grid[k] = SQ_BELLY

    # --- ears
    ears = set()
    for (ex, flip) in ((5, 1), (16, -1)):
        for row in range(5):
            w = row // 2 + 1
            for i in range(-w, w + 1):
                ears.add((ex + i, 1 + row))
        ears.add((ex - flip, 0))  # ear tuft
    put_layer(ears, lambda c: [grid.__setitem__(k, SQ_MAIN) for k in c])
    for (ex, _) in ((5, 1), (16, -1)):
        for row in range(2, 5):
            grid[(ex, 1 + row)] = SQ_PINK

    # --- head
    head = ellipse_cells(10.5, 11, 9.5, 7)
    put_layer(head, lambda c: shade_layer(grid, c, 10.5, 11, 9.5, 7, SQ_MAIN, SQ_SHADE, SQ_LIGHT))
    for k in ellipse_cells(10.5, 14.2, 4.6, 3.4):  # muzzle
        if k in head:
            grid[k] = SQ_BELLY

    paint_face(grid, expression)

    if pose == "fight":
        # fists raised at both sides of the chest, the right one a little higher
        for (ax, ay) in ((4, 22.5), (17, 22)):
            arm = ellipse_cells(ax, ay, 2, 2.6)
            put_layer(arm, lambda c: shade_layer(grid, c, ax, ay, 2, 2.6, SQ_MAIN, SQ_SHADE, SQ_LIGHT))
        for (fx, fy) in ((2.8, 19.6), (18.2, 18.8)):
            fist = ellipse_cells(fx, fy, 2.3, 2.1)
            put_layer(fist, lambda c: [grid.__setitem__(k, SQ_LIGHT) for k in c])
            for k in fist:  # bright top so the fists stand out from the fur
                if (k[0], k[1] - 1) not in fist:
                    grid[k] = SQ_BELLY
            cx, cy = int(fx), int(fy)
            for k in ((cx - 1, cy - 1), (cx - 1, cy), (cx + 1, cy - 1), (cx + 1, cy)):  # finger lines
                grid[k] = SQ_SHADE
            for dx in (-1, 0, 1):
                grid[(cx + dx, cy + 1)] = SQ_MAIN
    elif pose == "hold":
        for ax in (4, 17):
            arm = ellipse_cells(ax, 22, 2, 3)
            put_layer(arm, lambda c: shade_layer(grid, c, ax, 22, 2, 3, SQ_MAIN, SQ_SHADE, SQ_LIGHT))
        if item:
            iw = max(len(r) for r in item)
            ix0 = round(10.5 - iw / 2)
            for j, row in enumerate(item):
                for i, ch in enumerate(row):
                    if ch != ".":
                        grid[(ix0 + i, 19 + j)] = item_colors[ch]
        for px in (5.5, 15.5):  # paws gripping both sides of the item
            paw = ellipse_cells(px, 23, 1.4, 1.4)
            put_layer(paw, lambda c: [grid.__setitem__(k, SQ_LIGHT) for k in c])
    elif pose == "think":
        # one arm folded across the belly, the other propped on it with the paw on the chin
        arm = ellipse_cells(9.5, 24, 3.6, 1.9)
        put_layer(arm, lambda c: shade_layer(grid, c, 9.5, 24, 3.6, 1.9, SQ_MAIN, SQ_SHADE, SQ_LIGHT))
        grid[(12, 24)] = SQ_SHADE
        raised = set()
        for t in range(7):
            ax = round(15 - t * 0.35)
            ay = 24 - t
            raised |= {(ax, ay), (ax - 1, ay)}
        put_layer(raised, lambda c: [grid.__setitem__(k, SQ_MAIN) for k in c])
        paw = ellipse_cells(13, 17.2, 1.8, 1.3)
        put_layer(paw, lambda c: [grid.__setitem__(k, SQ_SHADE) for k in c])
    else:
        # --- arms clutching the stomach
        for ax in (7, 14):
            arm = ellipse_cells(ax, 23.5, 2.1, 3.4)
            put_layer(arm, lambda c: shade_layer(grid, c, ax, 23.5, 2.1, 3.4, SQ_MAIN, SQ_SHADE, SQ_LIGHT))
        for k in [(8, 26), (13, 26)]:  # paw tips pressing the stomach
            grid[k] = SQ_SHADE

    # --- sweat drops near the head
    for (sx, sy) in SWEAT_DROPS[expression]:
        drop = {(sx, sy), (sx, sy + 1), (sx - 1, sy + 2), (sx, sy + 2), (sx + 1, sy + 2), (sx, sy + 3)}
        for c in outline(drop):
            grid[c] = SQ_OUT
        for c in drop:
            grid[c] = SQ_TEAR
        grid[(sx, sy + 2)] = SQ_WHITE
    return grid


def draw_squirrel(img, grid, ox, oy, s):
    draw = ImageDraw.Draw(img)
    xs = [x for x, _ in grid]
    ys = [y for _, y in grid]
    minx, miny = min(xs), min(ys)
    maxx, maxy = max(xs), max(ys)
    # ground shadow
    sh_y = oy + (maxy - miny + 1) * s - s
    for i, w in enumerate((26, 22)):
        px_rect(draw, ox + (14 - w // 2 + 5) * s, sh_y + i * s - s,
                ox + (14 + w // 2 + 5) * s, sh_y + (i + 1) * s - s, GREEN_DARK)
    for (x, y), c in grid.items():
        px = ox + (x - minx) * s
        py = oy + (y - miny) * s
        px_rect(draw, px, py, px + s, py + s, c)
    return (ox, oy, ox + (maxx - minx + 1) * s, oy + (maxy - miny + 1) * s)

# ---------------------------------------------------------------- parts

decor_boxes = []  # decoration rects (arrows, icons…) — text must not overlap them

def pixel_arrow(draw, cx, cy, direction, length=9, half=2, head=4, unit=6):
    """Gold pixel arrow with ink outline. direction: right/left/up/down."""
    cells = set()
    for x in range(length):
        for y in range(-half, half + 1):
            cells.add((x, y))
    for i in range(head + 1):
        for y in range(-(head - i), head - i + 1):
            cells.add((length + i, y))
    total = length + head + 1
    rot = {
        "right": lambda x, y: (x - total // 2, y),
        "left": lambda x, y: (total // 2 - x, y),
        "down": lambda x, y: (y, x - total // 2),
        "up": lambda x, y: (y, total // 2 - x),
    }[direction]
    cells = {rot(x, y) for x, y in cells}
    ink = outline(cells)
    for (x, y) in ink | cells:
        c = GOLD if (x, y) in cells else INK
        px_rect(draw, cx + x * unit, cy + y * unit, cx + (x + 1) * unit, cy + (y + 1) * unit, c)
    # top highlight row
    for (x, y) in cells:
        if (x, y - 1) not in cells:
            px_rect(draw, cx + x * unit, cy + y * unit, cx + (x + 1) * unit, cy + y * unit + 3, GOLD_LIGHT)
    xs = [x for x, _ in ink]
    ys = [y for _, y in ink]
    decor_boxes.append(("arrow-" + direction, (cx + min(xs) * unit, cy + min(ys) * unit,
                                               cx + (max(xs) + 1) * unit, cy + (max(ys) + 1) * unit)))


# ---------------------------------------------------------------- pixel icons
# rows of characters; "." = transparent, other characters map through a color dict

NORI = (24, 52, 36)
ICON_COLORS = {"X": INK, "C": CREAM, "R": RED, "Y": GOLD, "L": GOLD_LIGHT, "G": NORI,
               "D": GOLD_DARK, "W": (255, 255, 255)}

MUSHROOM = [
    "...XXXX...",
    ".XXRRRRXX.",
    "XRRCRRRRRX",
    "XRRRRRCRRX",
    "XXXXXXXXXX",
    "...XCCX...",
    "...XCCX...",
    "...XXXX...",
]
EGG = [
    "..XXXXX...",
    ".XCCCCCXX.",
    "XCCCYYCCCX",
    "XCCYLYYCCX",
    "XCCYYYYCX.",
    ".XCCYYCCX.",
    "..XCCCCX..",
    "...XXXX...",
]
ONIGIRI = [
    "....XX....",
    "...XCCX...",
    "..XCCCCX..",
    ".XCCCCCCX.",
    "XCCCCCCCCX",
    "XCCGGGGCCX",
    "XCCGGGGCCX",
    ".XXXXXXXX.",
]
BULB = [
    "..XXXXX..",
    ".XLLYYYX.",
    "XLWYYYYYX",
    "XLYYYYYYX",
    "XYYYYYYYX",
    ".XYYYYYX.",
    "..XDDDX..",
    "..XCCCX..",
    "...XXX...",
]

LEAF_PALE = (196, 232, 150)
SHIITAKE = (132, 80, 44)
SHIITAKE_LIGHT = (176, 112, 64)
VEG_COLORS = {"X": INK, "G": GREEN_LIGHT, "g": GREEN, "d": GREEN_DARK, "P": LEAF_PALE, "R": RED,
              "W": (255, 255, 255), "C": CREAM, "B": SHIITAKE, "b": SHIITAKE_LIGHT, "r": (170, 44, 40)}

CABBAGE = [
    "...XXXX...",
    ".XXPGGPXX.",
    "XPGGPGGGPX",
    "XGPgGGPGgX",
    "XGgPGGgPGX",
    "XgGGPgPGgX",
    ".XgGGPGgX.",
    "..XXXXXX..",
]
BROCCOLI = [
    "..XXX.XXX.",
    ".XGgGXGGgX",
    "XGGgGGgGGX",
    "XgGGGgGGgX",
    ".XgGgGGgX.",
    "..XXPPXX..",
    "...XPPX...",
    "...XXXX...",
]
SHIITAKE_ICON = [
    "...XXXX...",
    ".XXbbbbXX.",
    "XbBBCBBBbX",
    "XBBBBBCBBX",
    "XXXXXXXXXX",
    "...XCCX...",
    "...XCCX...",
    "...XXXX...",
]
TOMATO = [
    "....XgX...",
    "..XXgGgXX.",
    ".XRRXgXRRX",
    "XRWRRRRRRX",
    "XRRRRRRRRX",
    "XRRRRRRRrX",
    ".XRRRRRrX.",
    "..XXXXXX..",
]


MEAT = (196, 116, 52)
MEAT_LIGHT = (232, 164, 84)
FISH_BLUE = (132, 176, 214)
FISH_LIGHT = (196, 222, 240)
PROTEIN_COLORS = {"X": INK, "M": MEAT, "m": MEAT_LIGHT, "C": CREAM, "W": (255, 255, 255),
                  "F": FISH_BLUE, "f": FISH_LIGHT, "D": CREAM_DARK, "Y": GOLD, "L": GOLD_LIGHT}

DRUMSTICK = [
    "..XXXX....",
    ".XmmmmX...",
    "XmmMMMMX..",
    "XmMMMMMX..",
    "XMMMMMMX..",
    ".XMMMMXX..",
    "..XXXXCX..",
    ".....XCCX.",
    "....XCWXCX",
    ".....XX.X.",
]
FISH = [
    "...XXXXX.....",
    "..XffffFX..XX",
    ".XfWXffFFXXFX",
    "XffXXfFFFFFFX",
    ".XFFFFFFFXXFX",
    "..XFFFFFX..XX",
    "...XXXXX.....",
]
BOILED_EGG = [
    "...XXXX...",
    "..XWWWWX..",
    ".XWWWWWCX.",
    ".XWWYYWCX.",
    "XWWYLYYWCX",
    "XWWYYYYWCX",
    "XWWWYYWWCX",
    ".XCWWWWCX.",
    "..XXXXXX..",
]
TOFU = [
    "..XXXXXXXX",
    ".XWWWWWWXX",
    "XWWWWWWXDX",
    "XXXXXXXXDX",
    "XCCCCCCXDX",
    "XCCCCCCXDX",
    "XCCCCCCXX.",
    "XXXXXXXX..",
]


BOWL_RED = (190, 56, 48)
CRUST = (196, 128, 60)
BOWL_BLUE = (132, 176, 214)
SWEET_POTATO = (150, 70, 120)
SWEET_POTATO_LIGHT = (186, 104, 152)
STAPLE_COLORS = {"X": INK, "W": (255, 255, 255), "C": CREAM, "Y": GOLD, "L": GOLD_LIGHT, "D": GOLD_DARK,
                 "R": BOWL_RED, "b": CRUST, "N": BOWL_BLUE, "P": SWEET_POTATO, "p": SWEET_POTATO_LIGHT}

RICE_BOWL = [
    "..XXXXXX..",
    ".XWWWCWWX.",
    "XWWWWWWCWX",
    "XYYYYYYYYX",
    "XRRRRRRRRX",
    ".XRRRRRRX.",
    "..XRRRRX..",
    "...XXXX...",
]
BREAD = [
    "..XXXXXX..",
    ".XbbbbbbX.",
    "XbCCCCCCbX",
    "XbCCCCCCbX",
    "XbCCCCCCbX",
    "XbCCCCCCbX",
    "XbCCCCCCbX",
    "XXXXXXXXXX",
]
NOODLES = [
    ".......X.X.",
    "......XDXDX",
    "..XXXXXDXDX",
    ".XLYLYLYLX.",
    "XYLYLYLYLYX",
    "XXXXXXXXXXX",
    "XNNNNNNNNNX",
    ".XNNNNNNNX.",
    "..XXXXXXX..",
]
SWEET_POTATO_ICON = [
    "..XXXXXXX..",
    ".XPPPPPPPX.",
    "XPPpPPPPpLX",
    "XPPPPpPPPLX",
    ".XPPPPPPPX.",
    "..XXXXXXX..",
]


def pixel_icon(draw, rows, colors, x, y, unit, name=None):
    """Draw a small pixel icon from text rows ('.' = transparent). Returns its rect."""
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch != ".":
                px_rect(draw, x + i * unit, y + j * unit, x + (i + 1) * unit, y + (j + 1) * unit, colors[ch])
    rect = (x, y, x + max(len(r) for r in rows) * unit, y + len(rows) * unit)
    if name:
        decor_boxes.append((name, rect))
    return rect


def pill(draw, x1, y0, text, bg, fg, font, label):
    """Right-aligned label pill with notched pixel corners."""
    tw = font.getbbox(text)[2] - font.getbbox(text)[0]
    x0 = x1 - tw - 40
    y1 = y0 + 46
    px_rect(draw, x0 + 4, y0, x1 - 4, y1, INK)
    px_rect(draw, x0, y0 + 4, x1, y1 - 4, INK)
    px_rect(draw, x0 + 4, y0 + 4, x1 - 4, y1 - 4, bg)
    draw_text(draw, ((x0 + x1) // 2, (y0 + y1) // 2 - 1), text, font, fg,
              label=label, container=(x0 + 4, y0 + 4, x1 - 4, y1 - 4))
    return (x0, y0, x1, y1)


def number_badge(draw, x0, y0, n, font):
    x1, y1 = x0 + 48, y0 + 48
    px_rect(draw, x0, y0, x1, y1, INK)
    px_rect(draw, x0 + 4, y0 + 4, x1 - 4, y1 - 4, GOLD)
    px_rect(draw, x0 + 4, y0 + 4, x1 - 4, y0 + 9, GOLD_LIGHT)
    draw_text(draw, ((x0 + x1) // 2, (y0 + y1) // 2 - 2), str(n), font, INK,
              label=f"badge-{n}", container=(x0 + 4, y0 + 4, x1 - 4, y1 - 4))

# ---------------------------------------------------------------- verification

def glyph_signature(font, ch):
    canvas = Image.new("L", (font.size * 2, font.size * 2), 0)
    ImageDraw.Draw(canvas).text((font.size // 2, font.size // 2), ch, font=font, fill=255)
    return canvas.tobytes()


def verify():
    """Check every text: inside its container / canvas, and no missing glyphs (tofu)."""
    ok = True
    notdef_cache = {}
    print("\n--- text check ---")
    for label, text, font, bbox, cont in text_boxes:
        problems = []
        if bbox[0] < 0 or bbox[1] < 0 or bbox[2] > W or bbox[3] > H:
            problems.append("canvas overflow")
        if bbox[0] < cont[0] or bbox[1] < cont[1] or bbox[2] > cont[2] or bbox[3] > cont[3]:
            problems.append(f"container overflow {cont}")
        key = id(font)
        if key not in notdef_cache:
            notdef_cache[key] = glyph_signature(font, "\ue000")  # unassigned PUA → .notdef
        notdef = notdef_cache[key]
        missing = [ch for ch in text if not ch.isspace() and glyph_signature(font, ch) == notdef]
        if missing:
            problems.append(f"missing glyphs {missing}")
        status = "OK " if not problems else "NG "
        ok &= not problems
        print(f"{status} {label:22s} bbox={tuple(int(v) for v in bbox)} {'; '.join(problems)}")
    print("RESULT:", "ALL OK" if ok else "PROBLEMS FOUND")
    return 0 if ok else 1


def verify_decor(allowed=()):
    """Check that no text overlaps a decoration. allowed: {(text label prefix, decor name)}."""
    print("\n--- decoration overlap check ---")
    ok = True
    for label, _, _, tb, _ in text_boxes:
        for dname, db in decor_boxes:
            if any(label.startswith(lp) and dname == dn for lp, dn in allowed):
                continue
            if tb[0] < db[2] and db[0] < tb[2] and tb[1] < db[3] and db[1] < tb[3]:
                ok = False
                print(f"NG  {label} overlaps {dname}")
    print("RESULT:", "NO OVERLAP" if ok else "OVERLAP FOUND")
    return 0 if ok else 1


def verify_all(allowed=()):
    text_status = verify()
    decor_status = verify_decor(allowed)
    return text_status or decor_status
