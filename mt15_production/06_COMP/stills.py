"""Turns approved 4K stills into moving shots for the film, at no generation cost.

Usage:  python3 stills.py STILLS_DIR FRAMES_DIR
  STILLS_DIR  the 2160x3840 stills (K01, K02, K07, K11 ...), PNG or JPG
  FRAMES_DIR  the film frames dir; writes S01, S02, S07, S11 as 1080x1920 PNG sequences,
              each marked with a PLATE file so post.py treats it as finished footage.

S01 / S11: the download screen is corner-pinned onto the blank TV, with a slow push-in.
S02: slow push on the helmet with a glint crossing the visor (the idea landing).
S03: the helmet-on still with a small snap on the buckle click.
S05: the hanging-drop still with the CG colour burst (FRAMES_DIR/S05_burst, from film.py --burst-only) laid over it.
S07: the puddle still, with ripples made to travel outward by a radial warp.
"""
import glob
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(os.path.dirname(HERE), "04_CG", "textures")
W, H = 1080, 1920


def find(stills_dir, key):
    hits = sorted(glob.glob(os.path.join(stills_dir, f"{key}_*")))
    if not hits:
        raise SystemExit(f"missing still {key} in {stills_dir}")
    return Image.open(hits[-1]).convert("RGB")


def tv_quad(im):
    """Corners (TL, TR, BR, BL) of the blank blue TV screen."""
    a = np.asarray(im, dtype=np.float32) / 255.0
    mask = (a[..., 2] > 0.74) & (a[..., 0] < 0.16) & (a[..., 1] < 0.16)       # the screen itself, not its glow on the wall
    cols, rows = mask.sum(0), mask.sum(1)
    xs = np.where(cols > cols.max() * 0.5)[0]
    ys = np.where(rows > rows.max() * 0.5)[0]
    x0, x1, y0, y1 = xs[0], xs[-1], ys[0], ys[-1]
    sub = mask[y0:y1 + 1, x0:x1 + 1]
    yy, xx = np.nonzero(sub)
    pick = lambda score: (int(xx[np.argmax(score)] + x0), int(yy[np.argmax(score)] + y0))
    return [pick(-(xx + yy)), pick(xx - yy), pick(xx + yy), pick(yy - xx)]


def tv_quad_lines(im):
    """Corners of the blue screen from its four edges, so a corner hidden behind something is still found.
    Each edge is a straight line fitted to the screen boundary, with points off the line (hair, a hand) dropped."""
    a = np.asarray(im, dtype=np.float32) / 255.0
    mask = (a[..., 2] > 0.60) & (a[..., 0] < 0.25) & (a[..., 1] < 0.25)
    cols, rows = mask.sum(0), mask.sum(1)
    xs = np.where(cols > cols.max() * 0.5)[0]
    ys = np.where(rows > rows.max() * 0.5)[0]
    x0, x1, y0, y1 = xs[0], xs[-1], ys[0], ys[-1]

    def fit(u, v):                                        # v = m*u + c: the line most boundary points agree on
        u, v = np.asarray(u, dtype=np.float64), np.asarray(v, dtype=np.float64)
        pick = np.random.default_rng(0)
        best = None
        for _ in range(400):
            i, j = pick.choice(len(u), 2, replace=False)
            if u[i] == u[j]:
                continue
            m = (v[j] - v[i]) / (u[j] - u[i])
            ok = np.abs(v - (m * u + v[i] - m * u[i])) <= 1.5
            if best is None or ok.sum() > best.sum():
                best = ok
        return np.polyfit(u[best], v[best], 1)

    cx = np.arange(x0 + (x1 - x0) // 8, x1 - (x1 - x0) // 8)
    top = fit(cx, [np.argmax(mask[:, x]) for x in cx])
    bot = fit(cx, [mask.shape[0] - 1 - np.argmax(mask[::-1, x]) for x in cx])
    cy = np.arange(y0 + (y1 - y0) // 8, y1 - (y1 - y0) // 8)
    left = fit(cy, [np.argmax(mask[y, :]) for y in cy])                       # x = m*y + c
    right = fit(cy, [mask.shape[1] - 1 - np.argmax(mask[y, ::-1]) for y in cy])

    def meet(h, v):                                       # y = mh*x + ch  with  x = mv*y + cv
        (mh, ch), (mv, cv) = h, v
        y = (mh * cv + ch) / (1 - mh * mv)
        return (float(mv * y + cv), float(y))

    return [meet(top, left), meet(top, right), meet(bot, right), meet(bot, left)]


def perspective_coeffs(dst, src):
    """PIL PERSPECTIVE coefficients that map output (dst) points back to input (src) points."""
    m = []
    for (x, y), (u, v) in zip(dst, src):
        m.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        m.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    b = np.array(src, dtype=np.float64).reshape(8)
    return np.linalg.solve(np.array(m, dtype=np.float64), b).tolist()


def put_screen(im, ui, quad, brightness=1.0, behind=False):
    """Corner-pin the UI onto the TV. Keeps some of the plate's own blue so it still lights the room.
    behind=True: only pixels that are still screen-blue take the UI, so anything in front of the TV stays in front."""
    inset = 3
    cx, cy = sum(p[0] for p in quad) / 4, sum(p[1] for p in quad) / 4
    q = [(x + inset * np.sign(cx - x), y + inset * np.sign(cy - y)) for x, y in quad]
    uw, uh = ui.size
    coeffs = perspective_coeffs(q, [(0, 0), (uw, 0), (uw, uh), (0, uh)])
    warped = ui.transform(im.size, Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).polygon(q, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1.2))
    a = np.asarray(im, dtype=np.float32) / 255.0
    u = np.asarray(warped, dtype=np.float32) / 255.0
    m = np.asarray(mask, dtype=np.float32)[..., None] / 255.0
    if behind:
        blue = ((a[..., 2] > 0.45) & (a[..., 0] < 0.30) & (a[..., 1] < 0.30)).astype(np.uint8) * 255
        blue = Image.fromarray(blue).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.0))
        m = m * np.asarray(blue, dtype=np.float32)[..., None] / 255.0
    screen = np.clip(u * 1.25 * brightness + a * 0.22, 0, 1)        # UI over a little of the original glow
    return Image.fromarray((np.clip(a * (1 - m) + screen * m, 0, 1) * 255).astype(np.uint8))


def push(im, u, zoom, cx, cy):
    """Frame from a still: zoom in by `zoom` at progress u, centred on (cx, cy) in 0..1."""
    z = 1.0 + (zoom - 1.0) * u
    w, h = im.size
    cw, ch = w / z, h / z
    x0 = min(max(cx * w - cw / 2, 0), w - cw)
    y0 = min(max(cy * h - ch / 2, 0), h - ch)
    return im.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))


def save(frames_dir, shot, frames):
    d = os.path.join(frames_dir, shot)
    if os.path.isdir(d) and not os.path.exists(os.path.join(d, "PLATE")):
        os.rename(d, d + "_cg")                     # keep the CG version beside it
    os.makedirs(d, exist_ok=True)
    for i, f in enumerate(frames, 1):
        f.save(os.path.join(d, f"f{i:04d}.png"))
    open(os.path.join(d, "PLATE"), "w").close()
    print("stills ->", shot, len(frames), flush=True)


def room(stills_dir, key, ui_name, n, zoom, pulse_at=None):
    plate = find(stills_dir, key)
    quad = tv_quad(plate)
    ui = Image.open(os.path.join(TEX, ui_name)).convert("RGB")
    cx = sum(p[0] for p in quad) / 4 / plate.width
    cy = (sum(p[1] for p in quad) / 4 / plate.height) * 0.55 + 0.5 * 0.45      # push toward the TV, not onto it
    out = []
    rng = np.random.default_rng(2)
    for i in range(n):
        b = 1.0 + rng.normal(0, 0.012)                                         # a screen is never perfectly steady
        if pulse_at is not None and pulse_at <= i < pulse_at + 5:
            b += 0.22 * (1 - (i - pulse_at) / 5)                               # the number ticks over
        out.append(push(put_screen(plate, ui, quad, b), i / (n - 1), zoom, cx, cy))
    return out


def helmet(stills_dir, n):
    plate = find(stills_dir, "K02")
    w, h = plate.size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    visor = np.exp(-(((xx - 0.50 * w) / (0.36 * w)) ** 2 + ((yy - 0.52 * h) / (0.11 * h)) ** 2) * 1.6)
    a = np.asarray(plate, dtype=np.float32) / 255.0
    out = []
    for i in range(n):
        t = (i - 8) / 8.0                                                      # the glint crosses on frames 8-16
        frame = a
        if 0 <= t <= 1:
            band = np.exp(-(((xx + 0.35 * (yy - 0.5 * h)) - (0.10 + 0.85 * t) * w) / (0.035 * w)) ** 2)
            glint = (band * visor * np.sin(np.pi * t))[..., None] * np.array((0.75, 0.86, 1.0), dtype=np.float32)
            frame = np.clip(a + glint * 0.85, 0, 1)
        im = Image.fromarray((frame * 255).astype(np.uint8))
        out.append(push(im, i / (n - 1), 1.09, 0.52, 0.52))
    return out


def puddle(stills_dir, n):
    plate = find(stills_dir, "K07").resize((W, H), Image.LANCZOS)
    a = np.asarray(plate)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy, squash = 0.50 * W, 0.535 * H, 0.36                                 # the crown; rings are ellipses in view
    dx, dy = xx - cx, (yy - cy) / squash
    r = np.hypot(dx, dy) + 1e-3
    ux, uy = dx / r, dy / r * squash
    env = np.clip(r / 60, 0, 1) * np.exp(-r / 900)
    out = []
    for i in range(n):
        phase = 2 * np.pi * (r - 26.0 * i) / 120.0                             # rings travel outward 26 px a frame
        d = 5.0 * np.sin(phase) * env
        sx = np.clip(np.rint(xx - ux * d), 0, W - 1).astype(np.int32)
        sy = np.clip(np.rint(yy - uy * d), 0, H - 1).astype(np.int32)
        shade = 1.0 + 0.10 * np.cos(phase) * env                               # crests catch a little more light
        frame = np.clip(a[sy, sx].astype(np.float32) * shade[..., None], 0, 255).astype(np.uint8)
        out.append(push(Image.fromarray(frame), i / (n - 1), 1.05, 0.5, 0.54))
    return out


def buckle(stills_dir, n):
    """S03: the helmet is on, hand at the chin strap. A slow push, then a small snap on the click frame."""
    plate = find(stills_dir, "K03")
    out = []
    for i in range(n):
        z = 1.0 + 0.03 * i / 6 if i < 6 else (1.075 if i == 6 else 1.06 + 0.004 * (i - 7))
        dy = 0.004 if i == 6 else 0.0                     # the click: one frame of snap and settle
        out.append(push(plate, 1.0, z, 0.52, 0.60 + dy))
    return out


def drop(stills_dir, frames_dir, n):
    """S05: the photoreal hanging drop; the beam reaches it and the CG colour burst is laid over it."""
    plate = find(stills_dir, "K05").resize((W, H), Image.LANCZOS)
    a = np.asarray(plate, dtype=np.float32) / 255.0
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = 0.175 * W, 0.515 * H                         # centre of the drop's bulb in the still
    halo = np.exp(-(((xx - cx) / (0.20 * W)) ** 2 + ((yy - cy) / (0.13 * H)) ** 2))[..., None]
    sweep = np.clip(1.2 - np.abs(xx - cx) / (0.55 * W), 0, 1)[..., None] * \
        np.exp(-((yy - cy) / (0.20 * H)) ** 2)[..., None]
    out = []
    for i in range(n):
        f = i + 1
        beam = float(np.clip((f - 5) / 7, 0, 1))          # the headlight arrives over frames 5-12
        flash = float(np.exp(-((f - 13) / 1.6) ** 2))     # and the drop flares as it bursts
        frame = a + (halo * (0.30 * beam + 0.75 * flash) + sweep * 0.10 * beam) * np.array((0.86, 0.93, 1.0),
                                                                                         dtype=np.float32)
        src = os.path.join(frames_dir, "S05_burst", f"f{f:04d}.png")
        if f >= 12 and os.path.exists(src):
            b = Image.open(src).convert("RGBA").resize((W, H), Image.LANCZOS)
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            layer.paste(b, (-15, 30))                     # lines the CG burst origin up with the still's drop
            la = np.asarray(layer, dtype=np.float32) / 255.0
            rgb, al = la[..., :3], la[..., 3:4]
            rgb = np.clip(rgb ** 1.7 * np.array((1.0, 0.78, 0.92), dtype=np.float32), 0, 1)   # amber, not white-hot
            glow = np.asarray(Image.fromarray((np.clip(rgb * al, 0, 1) * 255).astype(np.uint8)).filter(
                ImageFilter.GaussianBlur(26)), dtype=np.float32) / 255.0
            frame = frame * (1 - al * 0.88) + rgb * al * 0.88 + glow * 0.30
        im = Image.fromarray((np.clip(frame, 0, 1) * 255).astype(np.uint8))
        out.append(push(im, i / (n - 1), 1.06, 0.30, 0.52))
    return out


def screen_on_take(frames_dir, shots, ui_name):
    """A generated take with a blank blue TV (locked-off camera): put the download screen on it, frame by frame.
    The screen corners come from the first frame of the first shot; the shots are consecutive pieces of one take."""
    ui = Image.open(os.path.join(TEX, ui_name)).convert("RGB")
    quad = None
    rng = np.random.default_rng(2)
    for shot in shots:
        d = os.path.join(frames_dir, shot)
        for f in sorted(glob.glob(os.path.join(d, "f*.png"))):
            im = Image.open(f).convert("RGB")
            if quad is None:
                quad = tv_quad_lines(im)
            put_screen(im, ui, quad, 1.0 + rng.normal(0, 0.012), behind=True).save(f)
        print("screen ->", shot, [(round(x), round(y)) for x, y in quad], flush=True)


def main():
    if sys.argv[1] == "--screen":                        # stills.py --screen FRAMES_DIR UI.png SHOT [SHOT...]
        return screen_on_take(sys.argv[2], sys.argv[4:], sys.argv[3])
    stills_dir, frames_dir = sys.argv[1], sys.argv[2]
    only = sys.argv[3:]                                  # optional: shot IDs to rebuild
    jobs = {"S01": lambda: room(stills_dir, "K01", "tv_3_named.png", 30, 1.07),
            "S02": lambda: helmet(stills_dir, 20),
            "S03": lambda: buckle(stills_dir, 12),
            "S05": lambda: drop(stills_dir, frames_dir, 30),
            "S07": lambda: puddle(stills_dir, 14),
            "S11": lambda: room(stills_dir, "K11", "tv_4_named.png", 40, 1.05, pulse_at=13)}
    for shot, make in jobs.items():
        if not only or shot in only:
            save(frames_dir, shot, make())


if __name__ == "__main__":
    main()
