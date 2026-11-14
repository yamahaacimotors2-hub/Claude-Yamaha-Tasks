"""Cuts the approved generated takes into frame sequences for the film.

Usage:  python3 takes.py FRAMES_DIR [shot IDs...]
  Reads 05_GENERATIONS/takes/*.mp4, writes FRAMES_DIR/<shot>/f0001.png... plus a PLATE marker,
  so post.py treats the shot as finished footage. An older version of the shot is kept as <shot>_prev.

CUTS: shot -> (take file, first take frame, frames in the film, step)
  step 1 = real time. step 2 = double speed; each film frame is the average of two take frames,
  which gives the motion blur a faster camera would have had.
  step = a list: the exact take frame for each film frame (used to retime a performance).

S01 and S02 are one continuous take of the man on the sofa (blank blue TV). After cutting them, put the
download screen on the TV:  python3 stills.py --screen FRAMES_DIR tv_3_named.png S01 S02
"""
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
TAKES = os.path.join(os.path.dirname(HERE), "05_GENERATIONS", "takes")

# Opening take, 97 frames: bored stare (0-11), long eyes-closed sigh (12-47), bored stare (48-66),
# eyes go to the helmet (67-80), eyebrows up and a small smile (81-96). The film has 50 frames for it, so the
# boredom plays at 2.3x (the sigh becomes one slow heavy blink) and the glance and smile at 1.5x.
BORED = [round(i * 66 / 29) for i in range(30)]
GLANCE = [67 + round(i * 29 / 19) for i in range(20)]

CUTS = {
    "S01": ("S01_bored_seedance_take01_720p.mp4", 0, 30, BORED),
    "S02": ("S01_bored_seedance_take01_720p.mp4", 0, 20, GLANCE),
    "S03": ("S03_seedance_take01_720p.mp4", 42, 12, 1),   # visor snaps down on local frame 7
    "S04": ("S04_seedance_take01_720p.mp4", 50, 28, 1),   # bike clears the stall post and rides out
    "S05": ("S05_seedance_take01_720p.mp4", 24, 36, 1),   # beam arrives, drop bursts on local frame 12
    "S09": ("S09_seedance_take01_720p.mp4", 24, 36, 2),   # the city builds under the aerial, double speed
    "S10": ("S10_seedance_take01_720p.mp4", 6, 36, 1),
}


def cut(frames_dir, shot):
    name, first, n, step = CUTS[shot]
    tmp = tempfile.mkdtemp()
    picks = step if isinstance(step, list) else None
    if picks:
        first, step = 0, 1
        last = max(picks)
    else:
        last = first + n * step - 1
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(TAKES, name), "-vf",
                    f"select='between(n\\,{first}\\,{last})'", "-vsync", "0", os.path.join(tmp, "%04d.png")],
                   check=True)
    got = sorted(os.listdir(tmp))
    assert len(got) == (last + 1 if picks else n * step), (shot, len(got))
    d = os.path.join(frames_dir, shot)
    if os.path.isdir(d):
        prev = d + "_prev"
        shutil.rmtree(prev, ignore_errors=True)
        os.rename(d, prev)
    os.makedirs(d)
    for i in range(n):
        src = [picks[i]] if picks else [i * step + k for k in range(step)]
        group = [np.asarray(Image.open(os.path.join(tmp, got[k])).convert("RGB"), dtype=np.float32) for k in src]
        Image.fromarray(np.mean(group, axis=0).astype(np.uint8)).save(os.path.join(d, f"f{i + 1:04d}.png"))
    open(os.path.join(d, "PLATE"), "w").close()
    shutil.rmtree(tmp)
    print("take ->", shot, n, flush=True)


if __name__ == "__main__":
    for s in (sys.argv[2:] or list(CUTS)):
        cut(sys.argv[1], s)
