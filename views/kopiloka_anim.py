"""
kopiloka_anim.py - mesin animasi startup Kopiloka (pixel art).
Hanya butuh Pillow dan tidak bergantung pada GUI apa pun:
render(state_at(ms, progress)) menghasilkan gambar PIL berukuran W x H piksel,
jadi bisa dipakai di Tkinter, PyQt, Kivy, atau pygame.
"""
import math
from PIL import Image

W, H, SCALE = 88, 90, 8          # kanvas asli 88x88 piksel, diperbesar 8x
CX, CY = 44, 36                  # titik tengah cangkir
HANDLE_ANGLE = 225               # derajat searah jarum jam dari jam 12 (225 = jam 7:30)

# ---- palet Kopiloka ----
BG       = (24, 15, 10)
ESPRESSO = (43, 27, 18)
CREMA    = (110, 68, 40)
RIPPLE   = (66, 42, 28)
INNER    = (196, 168, 140)
CREAM    = (245, 230, 211)
LIGHT    = (255, 250, 240)
SHADE    = (214, 190, 163)
MOCHA    = (74, 48, 34)
CARAMEL  = (200, 135, 58)
DIM      = (150, 118, 90)
FOAM     = (214, 172, 120)
FOAM_HI  = (244, 218, 180)
STEAM    = (238, 228, 216)
CARAMEL_HI = (224, 162, 84)
CARAMEL_LO = (160, 104, 42)
SAUCER_R = 21                    # jari-jari alas cangkir

# ---- font pixel 3x5 ----
FONT = {
    "A": [".X.", "X.X", "XXX", "X.X", "X.X"],
    "C": ["XXX", "X..", "X..", "X..", "XXX"],
    "E": ["XXX", "X..", "XX.", "X..", "XXX"],
    "F": ["XXX", "X..", "XX.", "X..", "X.."],
    "I": ["XXX", ".X.", ".X.", ".X.", "XXX"],
    "K": ["X.X", "X.X", "XX.", "X.X", "X.X"],
    "L": ["X..", "X..", "X..", "X..", "XXX"],
    "M": ["X.X", "XXX", "XXX", "X.X", "X.X"],
    "N": ["XX.", "X.X", "X.X", "X.X", "X.X"],
    "O": ["XXX", "X.X", "X.X", "X.X", "XXX"],
    "P": ["XXX", "X.X", "XXX", "X..", "X.."],
    "S": ["XXX", "X..", "XXX", "..X", "XXX"],
}

# gelembung busa: (dx, dy dari pusat, ukuran)
BUBBLES = [(-7, -6, 2), (-5, -8, 1), (-2, -9, 1), (3, -9, 1),
           (8, -5, 1), (6, 5, 2), (5, 8, 1), (-6, 7, 1),
           (-3, 8, 1), (-1, 9, 1), (2, 9, 1)]

# uap: (offset x, fase, kecepatan)
STEAMS = [(-7, 0.0, 1.0), (0, 2.1, 1.0), (7, 4.2, 1.0)]

SPARKLES = [(-27, -17, 0.00), (28, -14, 0.35), (29, 12, 0.60), (-30, 3, 0.85)]


def dist(x, y):
    return math.hypot(x - CX, y - CY)


def put(px, x, y, c):
    if 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def blend(px, x, y, a):
    if 0 <= x < W and 0 <= y < H:
        r, g, b = px[x, y]
        px[x, y] = (int(r + (STEAM[0] - r) * a),
                    int(g + (STEAM[1] - g) * a),
                    int(b + (STEAM[2] - b) * a))


def text(px, s, x, y, color, count=None, flash=False, clip=None):
    """Gambar teks pixel. color boleh warna atau fungsi(i) -> warna."""
    for i, ch in enumerate(s):
        if count is not None and i >= count:
            break
        if ch == " ":
            continue
        col = color(i) if callable(color) else color
        if flash and count is not None and i == count - 1:
            col = LIGHT
        for r, line in enumerate(FONT[ch]):
            for c, v in enumerate(line):
                x_ = x + i * 4 + c
                if v == "X" and (clip is None or x_ < clip):
                    put(px, x_, y + r, col)


def centered_x(s):
    return (W - (len(s) * 4 - 1)) // 2


def saucer_px(x, y):
    """Warna alas (saucer) di piksel (x, y); None kalau di luar alas."""
    d = dist(x, y)
    if d > SAUCER_R + 0.5: return None
    if d > SAUCER_R:       return MOCHA
    s = (x - CX) + (y - CY)
    if d > SAUCER_R - 1.5:                       # bibir alas: kilap & bayangan
        if s < -18: return CARAMEL_HI
        if s > 18:  return CARAMEL_LO
    if 13.5 < d <= 14.5 and s > 4:               # bayangan tipis cangkir di atas alas
        return CARAMEL_LO
    return CARAMEL


def rrect(u, v, u0, u1, hv, rad):
    """Jarak bertanda persegi bulat; <= 0 berarti di dalam.
    u = arah keluar dari cangkir, v = arah menyamping."""
    uc, hu = (u0 + u1) / 2, (u1 - u0) / 2
    qx, qy = abs(u - uc) - (hu - rad), abs(v) - (hv - rad)
    return math.hypot(max(qx, 0), max(qy, 0)) + min(max(qx, qy), 0) - rad


# ---- bentuk cangkir (tanpa kopi) dibuat sekali saja ----
def build_cup():
    cup = {}
    for y in range(H):                                 # alas (saucer)
        for x in range(W):
            c = saucer_px(x, y)
            if c: cup[(x, y)] = c

    a = math.radians(HANDLE_ANGLE)                     # gagang berbentuk "telinga"
    dx, dy = math.sin(a), -math.cos(a)                 # arah keluar (225 derajat = kiri bawah)
    qx_, qy_ = math.cos(a), math.sin(a)                # arah menyamping
    hx, hy = CX + 16 * dx, CY + 16 * dy                # pusat gagang
    for y in range(int(hy) - 12, int(hy) + 13):
        for x in range(int(hx) - 12, int(hx) + 13):
            u = (x - CX) * dx + (y - CY) * dy
            v = (x - CX) * qx_ + (y - CY) * qy_
            if rrect(u, v, 8, 21.5, 6.0, 5) <= 0:      # outline luar (ujung membulat)
                cup[(x, y)] = MOCHA
            if rrect(u, v, 8, 20.5, 5.0, 4) <= 0:      # badan gagang + kilap/bayangan
                sh = (x - hx) + (y - hy)
                cup[(x, y)] = LIGHT if sh < -3.5 else SHADE if sh > 3.5 else CREAM
            if rrect(u, v, 14.5, 18.8, 3.0, 2.1) <= 0: # tepi lubang
                cup[(x, y)] = MOCHA
            if rrect(u, v, 15.5, 17.8, 2.0, 1.1) <= 0: # lubang: yang terlihat alas
                cup[(x, y)] = saucer_px(x, y) or BG

    for y in range(H):                                 # badan cangkir
        for x in range(W):
            d = dist(x, y)
            if d <= 13.5: cup[(x, y)] = MOCHA
            if d <= 12.5:
                c = CREAM
                sh = (x - CX) + (y - CY)
                if sh < -10 and d > 11: c = LIGHT      # kilap kiri atas
                if sh > 10 and d > 11:  c = SHADE      # bayangan kanan bawah
                cup[(x, y)] = c
            if d <= 10.5: cup[(x, y)] = INNER          # dalam cangkir (kosong)
    return cup


CUP = build_cup()


def sparkle(px, x, y, phase):
    if 0.30 <= phase < 0.50 or 0.70 <= phase < 0.85:
        put(px, x, y, LIGHT)
    elif 0.50 <= phase < 0.70:
        put(px, x, y, LIGHT)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            put(px, x + dx, y + dy, CREAM)


def draw_foam(px, n, t):
    for i, (dx, dy, sz) in enumerate(BUBBLES[:n]):
        x, y = CX + dx, CY + dy
        if sz == 1:
            shimmer = (int(t // 4) + i) % 7 == 0
            put(px, x, y, FOAM_HI if shimmer else FOAM)
        else:
            for ox in (0, 1):
                for oy in (0, 1):
                    put(px, x + ox, y + oy, FOAM)
            put(px, x, y, FOAM_HI)


def draw_steam(px, k, t):
    """Uap bergelombang naik dari tepi atas cangkir, condong ke kanan."""
    if k <= 0:
        return
    fade_in = min(1.0, k * 1.3)
    length = int(22 * min(1.0, k * 1.2))
    y0 = CY - 14
    for bx, ph, spd in STEAMS:
        for i in range(length):
            if ((i - t * 0.9 * spd + ph * 2) % 9) >= 6:         # celah antar gumpalan
                continue
            x = CX + bx + 1.8 * math.sin(i * 0.45 + ph - t * 0.22 * spd) + 0.10 * i
            a = (0.5 if i < 8 else 0.8 if i < 15 else 0.4) * fade_in   # tipis di atas alas, jelas di udara
            xi, y = int(round(x)), y0 - i
            blend(px, xi, y, a)
            blend(px, xi + 1, y, a)


def render(s):
    img = Image.new("RGB", (W, H), BG)
    px = img.load()
    t = s["tick"]

    # 1. cangkir muncul (circular reveal dari tengah)
    r = s.get("reveal", 0)
    for (x, y), c in CUP.items():
        if dist(x, y) <= r:
            px[x, y] = c

    # 2. kopi terisi
    cr = s.get("coffee", 0)
    if cr > 0:
        for y in range(CY - 12, CY + 13):
            for x in range(CX - 12, CX + 13):
                d = dist(x, y)
                if d <= cr and d <= 10.5:
                    px[x, y] = ESPRESSO if d <= 9.5 else CREMA

    # 3. riak + busa di permukaan kopi
    rr = s.get("ripple")
    if rr is not None:
        for y in range(CY - 10, CY + 11):
            for x in range(CX - 10, CX + 11):
                if abs(dist(x, y) - rr) < 0.7 and dist(x, y) <= 9.5:
                    px[x, y] = RIPPLE
    if s.get("foam"):
        draw_foam(px, s["foam"], t)

    # 4. tulisan LOKA muncul huruf per huruf
    n = s.get("loka", 0)
    if n:
        text(px, "LOKA", CX - 7, CY - 2, CREAM, count=n, flash=s.get("flash", False))

    # 5. uap panas
    draw_steam(px, s.get("steam", 0), t)

    # 6. kilau
    if s.get("spark"):
        for dx, dy, off in SPARKLES:
            sparkle(px, CX + dx, CY + dy, (t * 0.06 + off) % 1)

    # 7. judul KOPILOKA (typewriter) dan subjudul (wipe)
    c = s.get("title", 0)
    if c:
        text(px, "KOPILOKA", centered_x("KOPILOKA"), 63,
             lambda i: CREAM if i < 4 else CARAMEL, count=c)
    sub = s.get("sub", 0)
    if sub:
        sx = centered_x("PEMESANAN CAFE")
        text(px, "PEMESANAN CAFE", sx, 72, DIM, clip=sx + sub)

    # 8. loading bar
    p = s.get("bar")
    if p is not None:
        x0, y0, bw = 20, 81, 48
        for x in range(x0, x0 + bw):
            for y in range(y0, y0 + 5):
                if x in (x0, x0 + bw - 1) or y in (y0, y0 + 4):
                    px[x, y] = MOCHA
        for x in range(x0 + 1, x0 + 1 + int((bw - 2) * p)):
            for y in range(y0 + 1, y0 + 4):
                px[x, y] = CARAMEL if y < y0 + 3 else (160, 104, 42)
    return img


def ease_out(t):
    return 1 - (1 - t) ** 3


def _clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


INTRO_MS = 2800          # lama bagian intro (cangkir sampai subjudul), sebelum bar muncul
BG_HEX = "#%02x%02x%02x" % BG


def state_at(t_ms, progress=0.0):
    """Keadaan animasi pada waktu t_ms. progress (0..1) = kemajuan loading yang NYATA."""
    s = {"tick": t_ms / 50}

    s["reveal"] = 26 * ease_out(_clamp((t_ms - 300) / 400))            # cangkir muncul
    s["coffee"] = 10.5 * ease_out(_clamp((t_ms - 700) / 600))          # kopi dituang

    u = _clamp((t_ms - 1300) / 300)                                    # riak + busa + uap
    if 1300 < t_ms < 1600:
        s["ripple"] = 1 + 8 * u
    if t_ms > 1300:
        s["foam"] = int(len(BUBBLES) * u)
        s["steam"] = 0.1 + 0.5 * u

    if t_ms >= 1600:                                                   # L-O-K-A
        k = (t_ms - 1600) / 110
        n = min(4, int(k) + 1)
        s["loka"] = n
        s["flash"] = k < 4 and (t_ms - 1600) % 110 < 60
        s["steam"] = 1.0 if k >= 4 else 0.6 + 0.1 * n
        s["spark"] = True

    if t_ms >= 2040:                                                   # KOPILOKA
        s["title"] = min(8, int((t_ms - 2040) / 55) + 1)
    if t_ms >= 2480:                                                   # subjudul
        s["sub"] = int(63 * _clamp((t_ms - 2480) / 320))
    if t_ms >= INTRO_MS:                                               # loading bar
        s["bar"] = _clamp(progress)
    return s
