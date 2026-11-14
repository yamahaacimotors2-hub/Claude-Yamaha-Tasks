"""Turns approved 4K stills into moving shots for the film, at no generation cost.

Usage:  python3 stills.py STILLS_DIR FRAMES_DIR
  STILLS_DIR  the 2160x3840 stills (K01, K02, K07, K11 ...), PNG or JPG
  FRAMES_DIR  the film frames dir; writes S01, S02, S07, S11 as 1080x1920 PNG sequences,
              each marked with a PLATE file so post.py treats it as finished footage.

S01 / S11: the download screen is corner-pinned onto the blank TV, with a slow push-in.
S02: slow push on the helmet with a glint crossing the visor (the idea landing).
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


def perspective_coeffs(dst, src):
    """PIL PERSPECTIVE coefficients that map output (dst) points back to input (src) points."""
    m = []
    for (x, y), (u, v) in zip(dst, src):
        m.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        m.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    b = np.array(src, dtype=np.float64).reshape(8)
    return np.linalg.solve(np.array(m, dtype=np.float64), b).tolist()


def put_screen(im, ui, quad, brightness=1.0):
    """Corner-pin the UI onto the TV. Keeps some of the plate's own blue so it still lights the room."""
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


def main():
    stills_dir, frames_dir = sys.argv[1], sys.argv[2]
    only = sys.argv[3:]                                  # optional: shot IDs to rebuild
    jobs = {"S01": lambda: room(stills_dir, "K01", "tv_3_named.png", 30, 1.07),
            "S02": lambda: helmet(stills_dir, 20),
            "S07": lambda: puddle(stills_dir, 14),
            "S11": lambda: room(stills_dir, "K11", "tv_4_named.png", 40, 1.05, pulse_at=13)}
    for shot, make in jobs.items():
        if not only or shot in only:
            save(frames_dir, shot, make())


if __name__ == "__main__":
    main()
