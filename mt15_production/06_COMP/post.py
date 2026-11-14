"""Comp, grade and assembly for the MT-15 16 s film, v1.

Usage:  python3 post.py FRAMES_DIR OUT_DIR
  FRAMES_DIR  holds S01..S11 (720x1280 PNG sequences) and BG12/f0001.png (1080x1920), from 04_CG/film.py
  OUT_DIR     receives 384 finished 1080x1920 frames as %04d.png

What it does: rain overlay (S04-S07), per-shot grade, bloom, vignette, grain, upscale to 1080x1920,
and the S12 end card (official product PNG on the CG waterfront, tagline, logo placeholder).
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TEX = os.path.join(ROOT, "04_CG", "textures")
PRODUCT = os.path.join(ROOT, "01_REFERENCES", "MT15_V2_Cyan_Storm.png")
W, H = 1080, 1920

# shot, frames, look
EDIT = [("S01", 30, "room"), ("S02", 20, "room"), ("S03", 12, "room"), ("S04", 34, "rain"),
        ("S05", 30, "macro"), ("S06", 24, "rain"), ("S07", 14, "macro"), ("S08", 72, "dusk"),
        ("S09", 36, "dusk"), ("S10", 30, "dusk"), ("S11", 40, "room"), ("S12", 42, "card")]
assert sum(n for _, n, _ in EDIT) == 384

LOOKS = {   # gain per channel, contrast, saturation
    "room": ((1.00, 1.00, 1.06), 1.08, 1.05),
    "rain": ((0.94, 1.00, 1.08), 1.12, 0.92),
    "macro": ((1.00, 1.00, 1.02), 1.08, 1.10),
    "dusk": ((1.04, 0.99, 1.03), 1.10, 1.16),
}


def grade(a, look):
    gain, contrast, sat = LOOKS[look]
    a = a * np.array(gain, dtype=np.float32)
    a = (a - 0.5) * contrast + 0.5
    luma = (a * np.array((0.2126, 0.7152, 0.0722), dtype=np.float32)).sum(-1, keepdims=True)
    return luma + (a - luma) * sat


def blur(a, radius):
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(radius)), dtype=np.float32) / 255.0


def finish(a, rng, bloom=0.34):
    """Bloom on the highlights, soft vignette, fine grain."""
    hi = np.clip(a - 0.62, 0, 1) * 1.6
    glow = blur(hi, a.shape[1] / 60)
    a = 1 - (1 - np.clip(a, 0, 1)) * (1 - glow * bloom)
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.hypot((xx - w / 2) / (w * 0.75), (yy - h / 2) / (h * 0.75))
    a = a * (1 - 0.30 * np.clip(d - 0.35, 0, 1) ** 1.6)[..., None]
    a = a + rng.normal(0, 0.012, a.shape[:2]).astype(np.float32)[..., None]
    return np.clip(a, 0, 1)


class Rain:
    """Two depths of streaks. Positions are a pure function of the frame number."""

    def __init__(self, w, h, seed=3):
        r = np.random.default_rng(seed)
        self.w, self.h = w, h
        self.layers = []
        for count, (l0, l1), (v0, v1), (a0, a1), width in ((240, (16, 38), (52, 74), (0.10, 0.22), 1),
                                                           (24, (90, 170), (110, 150), (0.16, 0.30), 2)):
            self.layers.append((r.uniform(0, w * 1.2, count), r.uniform(0, h, count), r.uniform(l0, l1, count),
                                r.uniform(v0, v1, count), r.uniform(a0, a1, count), width))

    def frame(self, i, amount=1.0):
        im = Image.new("L", (self.w, self.h), 0)
        d = ImageDraw.Draw(im)
        for x, y0, ln, v, al, width in self.layers:
            y = (y0 + v * i) % (self.h + 200) - 100
            for k in range(len(x)):
                d.line((x[k], y[k], x[k] - 0.13 * ln[k], y[k] + ln[k]), fill=int(255 * al[k] * amount), width=width)
        return np.asarray(im.filter(ImageFilter.GaussianBlur(0.7)), dtype=np.float32)[..., None] / 255.0


def load(path):
    return np.asarray(Image.open(path).convert("RGB"), dtype=np.float32) / 255.0


def upscale(a):
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    return np.asarray(im.resize((W, H), Image.LANCZOS), dtype=np.float32) / 255.0


def over(dst, src_rgba, x, y, opacity=1.0):
    """Alpha-composite a float RGBA array onto dst at integer (x, y), clipped to the frame."""
    h, w = src_rgba.shape[:2]
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if x0 >= x1 or y0 >= y1:
        return
    s = src_rgba[y0 - y:y1 - y, x0 - x:x1 - x]
    al = s[..., 3:4] * opacity
    dst[y0:y1, x0:x1] = dst[y0:y1, x0:x1] * (1 - al) + s[..., :3] * al


def rgba(path, width=None):
    im = Image.open(path).convert("RGBA")
    if width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    return np.asarray(im, dtype=np.float32) / 255.0


def end_card(frames_dir, n, rng):
    """S12: the official product photo on the CG waterfront. The bike pixels are not regenerated."""
    bg0 = Image.open(os.path.join(frames_dir, "BG12", "f0001.png")).convert("RGB")
    bike = rgba(PRODUCT, 960)
    a = Image.open(PRODUCT).convert("RGBA").split()[-1].getbbox()          # trim to the bike itself
    k = 960 / Image.open(PRODUCT).width
    bx0, by0, bx1, by1 = [round(v * k) for v in a]
    bike = bike[by0:by1, bx0:bx1]
    bh, bw = bike.shape[:2]
    # dusk on the bodywork: a little cooler and darker, colours kept
    bike[..., :3] = np.clip(bike[..., :3] * np.array((0.86, 0.86, 0.95), dtype=np.float32) + 0.01, 0, 1)
    refl = bike[::-1].copy()
    fade = np.linspace(0.42, 0.0, bh, dtype=np.float32)[:, None] ** 1.3
    refl[..., 3] *= fade
    refl_im = Image.fromarray((refl * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(5))
    refl = np.asarray(refl_im, dtype=np.float32) / 255.0
    shadow = Image.new("L", (bw + 200, 150), 0)
    ImageDraw.Draw(shadow).ellipse((60, 40, bw + 140, 110), fill=215)
    shadow = np.asarray(shadow.filter(ImageFilter.GaussianBlur(22)), dtype=np.float32) / 255.0
    shadow = np.dstack([np.zeros((*shadow.shape, 3), np.float32), shadow])
    tag, model, logo = rgba(os.path.join(TEX, "tagline.png"), 880), rgba(os.path.join(TEX, "model_line.png"), 900), \
        rgba(os.path.join(TEX, "logo_placeholder.png"), 400)
    out = []
    for i in range(n):
        u = i / (n - 1)
        z = 1.0 + 0.045 * u                                        # slow push on the background
        cw, ch = W / z, H / z
        bg = bg0.resize((W, H), Image.LANCZOS, box=((W - cw) / 2, (H - ch) * 0.55, (W + cw) / 2,
                                                    (H - ch) * 0.55 + ch))
        a = np.asarray(bg, dtype=np.float32) / 255.0
        a = grade(a, "dusk")
        a = np.asarray(Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).filter(
            ImageFilter.GaussianBlur(2.2)), dtype=np.float32) / 255.0   # background a touch soft: bike is the subject
        a = a * 0.86
        x = (W - bw) // 2 + round(18 * (1 - u))                    # the bike settles into place
        y = 1470 - bh
        over(a, shadow, x - 100, y + bh - 82)
        over(a, refl, x, y + bh - 6)
        over(a, bike, x, y)
        a = finish(a, rng, bloom=0.22)
        t_in = np.clip((i - 5) / 9, 0, 1) ** 0.7                   # copy arrives after the bike reads
        over(a, tag, (W - tag.shape[1]) // 2, 330 - round(14 * (1 - t_in)), t_in)
        over(a, model, (W - model.shape[1]) // 2, 560, np.clip((i - 10) / 9, 0, 1))
        over(a, logo, (W - logo.shape[1]) // 2, 1500, np.clip((i - 14) / 9, 0, 1))
        out.append(np.clip(a, 0, 1))
    return out


def main():
    frames_dir, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    rng = np.random.default_rng(1)
    rain = Rain(720, 1280)
    g = 0
    for shot, n, look in EDIT:
        if shot == "S12":
            for a in end_card(frames_dir, n, rng):
                Image.fromarray((a * 255).astype(np.uint8)).save(os.path.join(out_dir, f"{g:04d}.png"))
                g += 1
            continue
        for f in range(1, n + 1):
            a = load(os.path.join(frames_dir, shot, f"f{f:04d}.png"))
            a = grade(a, look)
            amount = {"S04": 1.0, "S06": 1.0, "S07": 0.55}.get(shot, 0.0)
            if shot == "S05":                                      # time is frozen until the burst
                amount = float(np.clip((f - 20) / 8, 0, 1)) * 0.8
            if amount:
                streaks = rain.frame(g, amount)
                if shot == "S04":       # the camera stands under the stall roof: rain only out on the road
                    yy = np.linspace(0, 1, streaks.shape[0], dtype=np.float32)[:, None, None]
                    streaks = streaks * np.clip((yy - 0.20) / 0.06, 0, 1) * np.clip((0.60 - yy) / 0.06, 0, 1)
                a = a + streaks * np.array((0.80, 0.88, 1.0), dtype=np.float32)
            a = finish(a, rng)
            Image.fromarray((upscale(a) * 255).astype(np.uint8)).save(os.path.join(out_dir, f"{g:04d}.png"))
            g += 1
        print("comped", shot, g, flush=True)
    assert g == 384, g
    print("ALL 384 FRAMES")


if __name__ == "__main__":
    main()
