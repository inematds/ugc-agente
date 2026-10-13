"""Camada de textos do promo INEMA 15 s (9:16): PNG RGBA por quadro, 30 fps, sincronizada com vo3_amanda (+0,2 s)."""
import os, sys
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, DUR = 1080, 1920, 30, 15.0
OFF = 0.2  # atraso da narração no vídeo
OUT = sys.argv[1]
F = os.path.expanduser('~/.local/share/fonts/')
BLACK = F + 'Montserrat-Black.ttf'
XB = F + 'Montserrat-ExtraBold.ttf'
BLUE = (43, 140, 247)
WHITE = (255, 255, 255)
CHIP = [('Cursos de IA', (43, 140, 247)), ('Agentes de IA', (34, 170, 110)),
        ('Automação', (247, 145, 30)), ('Comunidade', (130, 90, 230))]


def font(p, s):
    return ImageFont.truetype(p, s)


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def alpha_in_out(t, a, b, fade=0.3):
    """0..1: entra em a, sai em b."""
    if t < a or t > b:
        return 0.0
    return min(ease((t - a) / fade), ease((b - t) / fade) if b < DUR else 1.0)


def text_layer(lines, size_font, y, color_fn, a, shift):
    """Desenha linhas centralizadas numa camada RGBA com sombra."""
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    yy = y + shift
    for i, (txt, fnt) in enumerate(zip(lines, size_font)):
        bb = d.textbbox((0, 0), txt, font=fnt)
        x = (W - (bb[2] - bb[0])) // 2 - bb[0]
        for dx, dy in ((0, 6), (0, 3)):
            d.text((x + dx, yy + dy), txt, font=fnt, fill=(0, 0, 0, int(150 * a)))
        c = color_fn(i)
        d.text((x, yy), txt, font=fnt, fill=c + (int(255 * a),))
        yy += (bb[3] - bb[1]) + int(fnt.size * 0.28)
    return lay


def pill(d, cx, y, txt, fnt, a, fill=BLUE):
    bb = d.textbbox((0, 0), txt, font=fnt)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pw, ph = tw + 90, th + 50
    x0 = cx - pw // 2
    d.rounded_rectangle((x0, y, x0 + pw, y + ph), radius=ph // 2, fill=fill + (int(245 * a),),
                        outline=(255, 255, 255, int(200 * a)), width=4)
    d.text((x0 + 45 - bb[0], y + 25 - bb[1]), txt, font=fnt, fill=(255, 255, 255, int(255 * a)))


def gradient(a):
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(g)
    for yy in range(H // 2, H):
        k = (yy - H // 2) / (H // 2)
        d.line([(0, yy), (W, yy)], fill=(0, 0, 0, int(190 * k * k * a)))
    return g


GRAD = gradient(1.0)
f_head = font(BLACK, 150)
f_pill = font(XB, 46)
f_mid = font(BLACK, 64)
f_chip = font(XB, 58)
f_end = font(BLACK, 128)
f_url = font(XB, 54)

os.makedirs(OUT, exist_ok=True)
for n in range(int(DUR * FPS)):
    t = n / FPS
    v = t - OFF  # tempo da fala
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gA = 1.0 if t < 10.4 + OFF else max(0.0, 1 - (t - 10.4 - OFF) / 0.4)
    img.alpha_composite(Image.blend(Image.new('RGBA', (W, H), (0, 0, 0, 0)), GRAD, gA))

    # A: gancho
    a = 1.0 if v < 2.9 else alpha_in_out(v, -1, 3.2)
    if a > 0:
        sh = 0
        img.alpha_composite(text_layer(['Aprenda', 'IA na', 'prática'], [f_head] * 3, 1230, lambda i: BLUE if i == 2 else WHITE, a, sh))
        d = ImageDraw.Draw(img)
        pill(d, W // 2, 1090 + sh, 'ACESSO GRÁTIS', f_pill, a)

    # B: o que tem
    a = alpha_in_out(v, 3.45, 7.85)
    if a > 0:
        ImageDraw.Draw(img).rounded_rectangle((170, 1125, 910, 1240), radius=30, fill=(10, 18, 40, int(200 * a)))
        img.alpha_composite(text_layer(['No INEMA.CLUB tem'], [f_mid], 1140, lambda i: WHITE, a, 0))
        d = ImageDraw.Draw(img)
        for i, (lab, col) in enumerate(CHIP):
            ci = alpha_in_out(v, [4.3, 5.25, 6.0, 6.75][i], 7.85, 0.25) * a
            if ci <= 0:
                continue
            y = 1270 + i * 130 + int(30 * (1 - ci))
            x0, x1 = 170, 910
            d.rounded_rectangle((x0, y, x1, y + 108), radius=26, fill=(255, 255, 255, int(235 * ci)))
            d.rounded_rectangle((x0 + 18, y + 18, x0 + 90, y + 90), radius=16, fill=col + (int(255 * ci),))
            d.text((x0 + 120, y + 22), lab, font=f_chip, fill=(25, 30, 45, int(255 * ci)))

    # C: valor
    a = alpha_in_out(v, 7.95, 10.3)
    if a > 0:
        sh = int(30 * (1 - ease((v - 7.95) / 0.4)))
        bd = ImageDraw.Draw(img)
        bd.rounded_rectangle((90, 1410 + sh, 990, 1640 + sh), radius=36, fill=(10, 18, 40, int(200 * a)))
        img.alpha_composite(text_layer(['Mais conhecimento,', 'mais liberdade.'], [f_mid, f_mid], 1455, lambda i: BLUE if i == 1 else WHITE, a, sh))

    # D: fecho
    a = alpha_in_out(v, 10.45, 99)
    if a > 0:
        dim = Image.new('RGBA', (W, H), (8, 14, 30, int(150 * a)))
        img.alpha_composite(dim)
        s = 0.9 + 0.1 * ease((v - 10.45) / 0.5)
        fe = font(BLACK, int(128 * s))
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        p1, p2 = 'INEMA', '.CLUB'
        b1, b2 = d.textbbox((0, 0), p1, font=fe), d.textbbox((0, 0), p2, font=fe)
        tw = (b1[2] - b1[0]) + (b2[2] - b2[0])
        x = (W - tw) // 2
        y = 820
        for (pp, bb, col) in ((p1, b1, WHITE), (p2, b2, BLUE)):
            d.text((x + 0, y + 6), pp, font=fe, fill=(0, 0, 0, int(160 * a)))
            d.text((x - bb[0], y), pp, font=fe, fill=col + (int(255 * a),))
            x += bb[2] - bb[0]
        pill(d, W // 2, 1010, 'ACESSO GRÁTIS', f_pill, a)
        bb = d.textbbox((0, 0), 'Aprenda IA na prática', font=f_url)
        d.text(((W - (bb[2] - bb[0])) // 2, 1150), 'Aprenda IA na prática', font=f_url, fill=(255, 255, 255, int(255 * a)))
        img.alpha_composite(lay)

    img.save(f'{OUT}/f{n:04d}.png', compress_level=1)
print('ok', n + 1)
