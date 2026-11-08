"""품목별 예시 이미지(그림)를 만든다. 실제 제품 사진이 생기면 그 사진으로 바꾼다.

    python3 tools/make_samples.py

images/products/<품목 id>.jpg (600x600) 로 저장한다.
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "images" / "products"
S = 1200  # 크게 그린 뒤 600 으로 줄여 가장자리를 매끄럽게

BLUE = (22, 80, 166)
RED = (142, 27, 30)
YELLOW = (242, 194, 48)
TEAL = (42, 110, 138)
INK = (27, 35, 48)

FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FONT_BLACK = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"


def font(size, black=False):
    return ImageFont.truetype(FONT_BLACK if black else FONT_BOLD, size, index=1)  # index 1 = KR


def canvas(top, bottom):
    """위에서 아래로 은은하게 바뀌는 배경."""
    im = Image.new("RGB", (S, S), top)
    d = ImageDraw.Draw(im)
    for y in range(S):
        t = y / S
        d.line([(0, y), (S, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)))
    return im


def shadow(im, shape_fn, offset=(18, 26), blur=28, alpha=70):
    """shape_fn(draw) 로 그린 모양의 그림자를 깐다."""
    m = Image.new("L", (S, S), 0)
    shape_fn(ImageDraw.Draw(m), 255)
    m = m.filter(ImageFilter.GaussianBlur(blur))
    sh = Image.new("RGB", (S, S), (20, 30, 50))
    layer = Image.new("L", (S, S), 0)
    layer.paste(m.point(lambda v: v * alpha // 255), offset)
    im.paste(sh, (0, 0), layer)


def center_text(d, xy, text, f, fill):
    d.text(xy, text, font=f, fill=fill, anchor="mm")


def save(im, name):
    im = im.resize((600, 600), Image.LANCZOS)
    im.save(OUT / f"{name}.jpg", quality=86, optimize=True, progressive=True)


# 1. 일반스티커: 종이 한 장에 원형 스티커 9개
def normal():
    im = canvas((236, 241, 249), (214, 223, 238))
    x0, y0, x1, y1 = 210, 190, 990, 1010
    shadow(im, lambda d, c: d.rounded_rectangle((x0, y0, x1, y1), 24, fill=c))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((x0, y0, x1, y1), 24, fill=(255, 255, 255))
    colors = [BLUE, RED, YELLOW, TEAL, RED, BLUE, YELLOW, TEAL, BLUE]
    words = ["감사", "SALE", "NEW", "BEST", "HOT", "선물", "OPEN", "맛집", "추천"]
    k = 0
    for r in range(3):
        for c in range(3):
            cx, cy = x0 + 135 + c * 255, y0 + 140 + r * 270
            rad = 105
            d.ellipse((cx - rad - 6, cy - rad - 6, cx + rad + 6, cy + rad + 6), outline=(225, 229, 236), width=3)
            d.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), fill=colors[k])
            d.ellipse((cx - rad + 14, cy - rad + 14, cx + rad - 14, cy + rad - 14), outline=(255, 255, 255), width=5)
            fg = INK if colors[k] == YELLOW else (255, 255, 255)
            center_text(d, (cx, cy), words[k], font(52, True), fg)
            k += 1
    # 한 장 떼어 낸 스티커
    d.ellipse((860, 860, 1100, 1100), fill=YELLOW)
    d.ellipse((878, 878, 1082, 1082), outline=(255, 255, 255), width=6)
    center_text(d, (980, 980), "신성", font(64, True), INK)
    return im


# 2. 유포지스티커: 물방울 맺힌 병에 붙은 라벨
def yupo():
    im = canvas((222, 238, 244), (190, 220, 232))
    bx0, bx1, top, bot = 380, 820, 300, 1080
    def bottle(d, c):
        d.rounded_rectangle((bx0, top, bx1, bot), 70, fill=c)
        d.rounded_rectangle((520, 150, 680, 320), 20, fill=c)
    shadow(im, bottle)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((520, 150, 680, 320), 20, fill=(70, 150, 180))
    d.rounded_rectangle((505, 120, 695, 190), 18, fill=TEAL)
    d.rounded_rectangle((bx0, top, bx1, bot), 70, fill=(120, 190, 215))
    d.rounded_rectangle((bx0 + 30, top + 40, bx0 + 80, bot - 60), 25, fill=(170, 220, 236))
    # 라벨
    lx0, ly0, lx1, ly1 = bx0, 520, bx1, 880
    d.rectangle((lx0, ly0, lx1, ly1), fill=(255, 255, 255))
    d.rectangle((lx0, ly0, lx1, ly0 + 70), fill=TEAL)
    center_text(d, (600, ly0 + 36), "FRESH", font(44, True), (255, 255, 255))
    center_text(d, (600, ly0 + 150), "생과일 주스", font(64, True), INK)
    center_text(d, (600, ly0 + 230), "냉장 보관 · 500ml", font(36), (90, 100, 115))
    for i in range(5):
        d.ellipse((470 + i * 60, ly1 - 70, 500 + i * 60, ly1 - 40), fill=[RED, YELLOW, TEAL, BLUE, RED][i])
    # 물방울
    rnd = random.Random(3)
    for _ in range(60):
        x, y, r = rnd.randint(bx0 + 20, bx1 - 20), rnd.randint(top + 30, bot - 30), rnd.randint(8, 20)
        if ly0 - 10 < y < ly1 + 10 and bx0 + 70 < x < bx1 - 70:
            continue  # 라벨 글자는 가리지 않게
        d.ellipse((x - r, y - r, x + r, y + r), fill=(235, 248, 252), outline=(150, 200, 220), width=2)
        d.ellipse((x - r // 2, y - r // 2, x, y), fill=(255, 255, 255))
    return im


# 3. 바코드스티커: 바코드 라벨 여러 장
def barcode():
    im = canvas((242, 238, 236), (226, 218, 214))
    rnd = random.Random(7)
    def label(cx, cy, ang, price, code):
        w, h = 620, 380
        lab = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(lab)
        d.rounded_rectangle((0, 0, w - 1, h - 1), 22, fill=(255, 255, 255, 255), outline=(220, 220, 220, 255), width=3)
        d.text((40, 30), "신성마트", font=font(40, True), fill=RED)
        d.text((w - 40, 30), price, font=font(48, True), fill=INK, anchor="ra")
        x = 60
        while x < w - 60:
            bw = rnd.choice([4, 4, 6, 8, 10])
            d.rectangle((x, 120, x + bw, 290), fill=INK)
            x += bw + rnd.choice([4, 6, 8])
        center_text(d, (w // 2, 330), code, font(34), INK)
        lab = lab.rotate(ang, expand=True, resample=Image.BICUBIC)
        sh = Image.new("RGBA", lab.size, (20, 30, 50, 0))
        sh.putalpha(lab.getchannel("A").point(lambda v: v * 60 // 255).filter(ImageFilter.GaussianBlur(16)))
        im.paste(sh, (cx - lab.width // 2 + 14, cy - lab.height // 2 + 22), sh)
        im.paste(lab, (cx - lab.width // 2, cy - lab.height // 2), lab)
    label(540, 400, 8, "₩3,500", "8 801234 567890")
    label(660, 800, -6, "₩12,000", "8 809876 543210")
    return im


# 4. 로타리 롤스티커: 감긴 롤과 풀려 나온 라벨 줄
def roll():
    im = canvas((246, 242, 228), (232, 224, 200))
    cx, cy, R = 430, 560, 300
    shadow(im, lambda d, c: d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=c))
    d = ImageDraw.Draw(im)
    # 풀려 나온 띠
    d.rectangle((cx, cy + R - 150, 1150, cy + R), fill=(255, 255, 255))
    d.line((cx, cy + R, 1150, cy + R), fill=(215, 210, 195), width=3)
    for i in range(4):
        x = 560 + i * 160
        d.rounded_rectangle((x, cy + R - 130, x + 130, cy + R - 20), 16, fill=YELLOW)
        center_text(d, (x + 65, cy + R - 75), "SS", font(46, True), INK)
    # 롤 단면
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(255, 255, 255))
    for r in range(R, 110, -14):
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(232, 226, 210), width=2)
    d.ellipse((cx - 110, cy - 110, cx + 110, cy + 110), fill=(196, 160, 110))
    d.ellipse((cx - 80, cy - 80, cx + 80, cy + 80), fill=(150, 116, 74))
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=(205, 198, 180), width=4)
    return im


# 5. 은무데드롱: 은색 무광 명판
def silver_pet():
    im = canvas((48, 56, 70), (28, 34, 44))
    x0, y0, x1, y1 = 170, 290, 1030, 910
    shadow(im, lambda d, c: d.rounded_rectangle((x0, y0, x1, y1), 30, fill=c), alpha=120)
    plate = Image.new("RGB", (x1 - x0, y1 - y0))
    pd = ImageDraw.Draw(plate)
    for x in range(plate.width):
        v = int(188 + 34 * math.sin(x / plate.width * math.pi * 1.4 + .6))
        pd.line([(x, 0), (x, plate.height)], fill=(v, v + 2, v + 6))
    plate = plate.filter(ImageFilter.GaussianBlur(2))
    m = Image.new("L", plate.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, plate.width - 1, plate.height - 1), 30, fill=255)
    im.paste(plate, (x0, y0), m)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((x0 + 30, y0 + 30, x1 - 30, y1 - 30), 18, outline=(70, 76, 88), width=4)
    d.text((x0 + 70, y0 + 70), "SHINSUNG", font=font(64, True), fill=INK)
    rows = [("MODEL", "SS-2026"), ("POWER", "220V ~ 60Hz"), ("RATED", "1,200W"), ("SERIAL", "2611-08-0427")]
    for i, (k, v) in enumerate(rows):
        y = y0 + 190 + i * 76
        d.text((x0 + 70, y), k, font=font(38), fill=(70, 76, 88))
        d.text((x0 + 330, y), v, font=font(40, True), fill=INK)
    tx, ty = x1 - 200, y0 + 300
    d.polygon([(tx, ty - 110), (tx + 120, ty + 95), (tx - 120, ty + 95)], fill=YELLOW, outline=INK)
    center_text(d, (tx, ty + 25), "!", font(130, True), INK)
    d.text((x0 + 70, y1 - 110), "MADE IN KOREA", font=font(34, True), fill=(70, 76, 88))
    return im


# 6. 홀로그램스티커: 무지갯빛 원형 인증 스티커
def hologram():
    im = canvas((34, 40, 58), (18, 22, 34))
    cx, cy, R = 600, 600, 340
    holo = Image.new("RGB", (S, S))
    hp = holo.load()
    for y in range(cy - R, cy + R):
        for x in range(cx - R, cx + R):
            a = math.atan2(y - cy, x - cx)
            t = (x + y) / (2 * S)
            h = (a / (2 * math.pi) + t * 1.5) % 1.0
            r = int(170 + 85 * math.sin(2 * math.pi * h))
            g = int(170 + 85 * math.sin(2 * math.pi * (h + .33)))
            b = int(170 + 85 * math.sin(2 * math.pi * (h + .66)))
            hp[x, y] = (r, g, b)
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).ellipse((cx - R, cy - R, cx + R, cy + R), fill=255)
    glow = m.filter(ImageFilter.GaussianBlur(40)).point(lambda v: v * 90 // 255)
    im.paste((150, 170, 255), (0, 0), glow)
    im.paste(holo, (0, 0), m)
    d = ImageDraw.Draw(im)
    d.ellipse((cx - R + 30, cy - R + 30, cx + R - 30, cy + R - 30), outline=(255, 255, 255), width=8)
    pts = []
    for i in range(10):
        rr = 120 if i % 2 == 0 else 52
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + rr * math.cos(a), cy - 70 + rr * math.sin(a)))
    d.polygon(pts, fill=(255, 255, 255))
    center_text(d, (cx, cy + 110), "정품 인증", font(78, True), (255, 255, 255))
    center_text(d, (cx, cy + 195), "GENUINE", font(42, True), (255, 255, 255))
    # 반짝임
    for (x, y, s) in [(390, 360, 30), (820, 450, 22), (760, 820, 26)]:
        d.polygon([(x, y - s), (x + 6, y - 6), (x + s, y), (x + 6, y + 6), (x, y + s), (x - 6, y + 6), (x - s, y), (x - 6, y - 6)], fill=(255, 255, 255))
    return im


# 7. 은무지/금무지스티커: 금색·은색 원형 감사 스티커
def metallic():
    im = canvas((120, 24, 30), (84, 14, 20))
    def disc(cx, cy, R, base, text, sub):
        shadow(im, lambda d, c: d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=c), alpha=110)
        g = Image.new("RGB", (2 * R, 2 * R))
        gd = ImageDraw.Draw(g)
        for y in range(2 * R):
            t = y / (2 * R)
            k = .78 + .3 * math.sin(t * math.pi * 1.2 + .4)
            gd.line([(0, y), (2 * R, y)], fill=tuple(min(255, int(c * k)) for c in base))
        m = Image.new("L", (2 * R, 2 * R), 0)
        ImageDraw.Draw(m).ellipse((0, 0, 2 * R - 1, 2 * R - 1), fill=255)
        im.paste(g, (cx - R, cy - R), m)
        d = ImageDraw.Draw(im)
        dark = tuple(int(c * .45) for c in base)
        d.ellipse((cx - R + 22, cy - R + 22, cx + R - 22, cy + R - 22), outline=dark, width=5)
        center_text(d, (cx, cy - 22), text, font(int(R * .3), True), dark)
        center_text(d, (cx, cy + R * .32), sub, font(int(R * .14), True), dark)
    disc(470, 500, 280, (232, 196, 110), "감사합니다", "THANK YOU")
    disc(810, 840, 230, (214, 218, 226), "Gift", "FOR YOU")
    return im


# 8. 투명지스티커: 유리병에 붙은 투명 스티커
def clear():
    im = canvas((250, 246, 240), (232, 226, 216))
    x0, y0, x1, y1 = 330, 260, 870, 1060
    def jar(d, c):
        d.rounded_rectangle((x0, y0, x1, y1), 90, fill=c)
    shadow(im, jar, alpha=50)
    glass = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glass)
    gd.rounded_rectangle((x0, y0, x1, y1), 90, fill=(205, 228, 236, 150), outline=(160, 196, 210, 255), width=6)
    gd.rounded_rectangle((x0 - 10, y0 - 90, x1 + 10, y0 + 10), 24, fill=(70, 60, 50, 255))
    # 내용물(꿀)
    gd.rounded_rectangle((x0 + 14, y0 + 300, x1 - 14, y1 - 14), 78, fill=(232, 168, 50, 210))
    gd.rounded_rectangle((x0 + 40, y0 + 60, x0 + 90, y1 - 120), 25, fill=(255, 255, 255, 110))
    im.paste(glass, (0, 0), glass)
    d = ImageDraw.Draw(im)
    # 투명 스티커: 바탕 없이 글자만, 가장자리는 아주 옅게
    d.rounded_rectangle((x0 + 90, y0 + 330, x1 - 90, y0 + 700), 26, outline=(255, 255, 255), width=3)
    center_text(d, (600, y0 + 430), "HONEY", font(96, True), (60, 36, 16))
    center_text(d, (600, y0 + 540), "전주 야생화 꿀", font(52, True), (60, 36, 16))
    center_text(d, (600, y0 + 625), "100% PURE · 500g", font(34, True), (90, 60, 30))
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in [("normal", normal), ("yupo", yupo), ("barcode", barcode), ("roll", roll),
                     ("silver-pet", silver_pet), ("hologram", hologram), ("metallic", metallic), ("clear", clear)]:
        save(fn(), name)
        print("만듦:", OUT / f"{name}.jpg")


if __name__ == "__main__":
    main()
