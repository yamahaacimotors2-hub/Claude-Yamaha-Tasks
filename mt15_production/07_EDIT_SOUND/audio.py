"""Sound design and music for the MT-15 16 s film.

Usage:  python3 audio.py OUT.wav [CUE_SHEET.csv] [A|B|C|D]

Without a letter: everything is synthesised here (no samples, no recordings).
With a letter: the music is one of the four generated synthwave tracks in music/ (ElevenLabs Music v2.5 through
Higgsfield, 120 BPM), re-cut to the picture; the sound effects stay synthesised.

The picture is cut on the music's beat grid, which is anchored on the raindrop burst (frame 102, 4.25 s):
a beat falls every 12 frames from there, and S06, S07, S08, S09, S10, S11 and the end card all start on one.
"""
import csv
import os
import subprocess
import sys

import numpy as np

SR, FPS, DUR = 48000, 24, 16.0
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(4)
CUT = {"S01": 0, "S02": 30, "S03": 50, "S04": 62, "S05": 90, "S06": 126, "S07": 150, "S08": 162,
       "S09": 234, "S10": 270, "S11": 306, "S12": 342, "END": 384}
TRACK = sys.argv[3] if len(sys.argv) > 3 else None       # generated music variation, or None for the synth score
HERE = os.path.dirname(os.path.abspath(__file__))
T = {k: v / FPS for k, v in CUT.items()}
cues = []


def cue(time, name, track):
    cues.append((round(time * FPS), f"{time:.3f}", track, name))


def bandpass(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    edge = np.clip((f - lo) / max(1.0, lo * 0.3), 0, 1) * np.clip((hi - f) / max(1.0, hi * 0.3), 0, 1)
    return np.fft.irfft(X * edge, len(x))


def env(start, end, attack=0.02, release=0.05):
    """Gate with soft edges between two times."""
    return np.clip((t - start) / attack, 0, 1) * np.clip((end - t) / release, 0, 1)


def place(buf, sig, time, gain=1.0):
    i = int(time * SR)
    if i >= N:
        return
    j = min(N, i + len(sig))
    buf[i:j] += sig[:j - i] * gain


def tone(freq, dur, decay, harmonics=(1.0,)):
    tt = np.arange(int(dur * SR)) / SR
    s = sum(a * np.sin(2 * np.pi * freq * (k + 1) * tt) for k, a in enumerate(harmonics))
    return s * np.exp(-tt / decay)


def click(dur, lo, hi, decay):
    n = int(dur * SR)
    x = rng.normal(0, 1, n)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    x = np.fft.irfft(X * ((f > lo) & (f < hi)), n)
    return x / (np.abs(x).max() + 1e-9) * np.exp(-np.arange(n) / SR / decay)


def reverb(x, seconds=1.4, mix=0.25):
    n = int(seconds * SR)
    ir = rng.normal(0, 1, n) * np.exp(-np.arange(n) / SR / (seconds / 5))
    wet = np.fft.irfft(np.fft.rfft(x, N + n) * np.fft.rfft(ir, N + n), N + n)[:N]
    return x + wet / (np.abs(wet).max() + 1e-9) * np.abs(x).max() * mix


amb, fx, veh, mus = (np.zeros(N) for _ in range(4))

# ---- ambience: room tone, then rain, then room tone again
room = bandpass(rng.normal(0, 1, N), 60, 420) * 0.5 + 0.25 * np.sin(2 * np.pi * 50 * t)
amb += room * 0.05 * (env(0, T["S04"], 0.3, 0.01) + env(T["S11"], T["END"], 0.01, 0.6))
rain = bandpass(rng.normal(0, 1, N), 1800, 9000) + 0.5 * bandpass(rng.normal(0, 1, N), 300, 1500)
freeze = 1 - 0.92 * env(T["S05"], T["S05"] + 0.50, 0.05, 0.10)          # time stops on the hanging drop
rain_level = env(T["S04"] - 0.08, T["S11"], 0.20, 0.01) * freeze                  # leads the cut by two frames
rain_level *= 1 - 0.55 * env(T["S08"], T["S11"], 0.8, 0.01)             # the rain thins as the city arrives
amb += rain * 0.060 * rain_level
cue(T["S01"], "room tone, TV fan", "AMBIENCE")
cue(T["S04"], "rain bed in, starting two frames ahead of the cut", "AMBIENCE")
cue(T["S11"], "hard cut back to room tone", "AMBIENCE")

# ---- room beats
REV_T = T["S02"] + 0.15                                                   # he looks at the helmet: the bike starts in his head
if TRACK:      # boredom: a wall clock and a slow ceiling fan. Both fade as the engine comes in, and return at the end.
    in_room = np.clip(1 - (t - REV_T) / 0.9, 0, 1) * (t < T["S04"]) + env(T["S11"], T["S12"] + 0.3, 0.01, 0.4)
    k = 0
    while 0.12 + k * 0.5 < T["END"]:
        tm = 0.12 + k * 0.5
        f = 2150 if k % 2 == 0 else 1550                                 # tick, tock
        tick = tone(f, 0.05, 0.007, (1.0, 0.35)) + 0.5 * click(0.05, 2500, 7000, 0.003)
        place(fx, tick, tm, 0.11 * float(np.interp(tm, t[::480], in_room[::480])))
        k += 1
    fan = bandpass(rng.normal(0, 1, N), 140, 900) * (0.55 + 0.45 * np.sin(2 * np.pi * 2.6 * t))
    amb += fan * 0.022 * in_room
    cue(0.12, "boredom: wall clock tick-tock every 0.5 s, slow ceiling fan", "AMBIENCE")
    cue(T["S11"], "back in the room: clock and fan again", "AMBIENCE")
else:
    for k in range(5):                                                   # the download that will not move
        place(fx, tone(1320, 0.05, 0.012), 0.20 + k * 0.5, 0.05)
    cue(0.20, "UI tick, repeats every 0.5 s", "FOLEY")
glint_t = T["S02"] + 8 / FPS                                              # the glint crosses the visor, frames 8-16
if TRACK:
    pass                                                                 # the idea is the engine (see vehicle)
else:
    place(fx, tone(2637, 0.9, 0.22, (1.0, 0.4, 0.15)), T["S02"] + 12 / FPS, 0.10)
    cue(T["S02"] + 12 / FPS, "idea: glint ting on the visor", "FOLEY")
snap = click(0.05, 1500, 9000, 0.006) * 0.9 + np.pad(tone(140, 0.05, 0.02), (0, 0))[: int(0.05 * SR)] * 0.8
place(fx, snap, T["S03"] + 7 / FPS, 0.34)
cue(T["S03"] + 7 / FPS, "visor snaps shut", "FOLEY")

# ---- vehicle: one continuous synthesised engine voice (never a recording). Level and pitch follow curves,
# so nothing steps at a cut. It swells and passes in the stall shot, is silent for the whole raindrop shot
# (macro, slow motion), and comes back with the bike.
def curve(points):
    xs, ys = zip(*points)
    return np.interp(t, xs, ys)


S4, S5, S6, S7, S8, S9, S10, S11 = (T[k] for k in ("S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11"))
pitch = curve([(REV_T, 62), (REV_T + 0.35, 62), (REV_T + 0.58, 116), (REV_T + 0.80, 76), (REV_T + 1.02, 130),
               (S4, 101), (S4 + 0.75, 104), (S5, 96),                     # two revs, then it passes the stall
               (S6, 118), (S7, 124), (S8, 126), (S9, 132), (S10, 132), (S11, 150)])
level = curve([(REV_T - 0.05, 0), (REV_T + 0.35, 0.03), (REV_T + 0.58, 0.062), (REV_T + 0.80, 0.045),
               (REV_T + 1.02, 0.075), (S4 + 0.15, 0.065) if TRACK else (S4 + 0.15, 0.035),
               (S4 + 0.75, 0.105), (S5 - 0.08, 0.05), (S5 + 0.06, 0),
               (S6 - 0.06, 0), (S6 + 0.12, 0.11), (S7 - 0.05, 0.10), (S7 + 0.08, 0.05),
               (S8 - 0.04, 0.05), (S8 + 0.12, 0.09), (S9 - 0.05, 0.09), (S9 + 0.10, 0.045),   # heard from the air
               (S10 - 0.05, 0.045), (S10 + 0.12, 0.11), (S11 - 0.006, 0.12), (S11, 0)])
phase = 2 * np.pi * np.cumsum(pitch) / SR
voice = sum(np.sin(phase * k) / k ** 1.5 for k in range(1, 10))            # softer than a raw saw
voice *= 0.65 + 0.35 * np.sin(phase * 0.5) ** 2                            # firing pulses
tyres = bandpass(rng.normal(0, 1, N), 700, 5000)                           # tyres on a wet road
outside = np.clip((t - (S4 - 0.05)) / 0.12, 0, 1)                          # 0 in the room, 1 on the road
if not TRACK:
    level = level * (t >= S4 - 0.10)                                       # synth score: no rev in the room
engine_snd = bandpass(voice, 55, 1400) * outside + bandpass(voice, 55, 420) * 1.5 * (1 - outside)   # muffled indoors
veh += (engine_snd + 0.55 * tyres * outside) * level * (1.0 if TRACK else 1.7)
if TRACK:
    cue(REV_T, "the idea: engine starts in the room, muffled, two rising revs, runs into the pass-by", "VEHICLE")
cue(S4, "engine and wet-tyre pass-by: swells, peaks as the bike crosses, falls away (synth)", "VEHICLE")
cue(S5, "engine out for the whole raindrop shot", "VEHICLE")
cue(S6, "engine back with the bike", "VEHICLE")
cue(S10, "engine opens up", "VEHICLE")

# ---- the raindrop
glass = tone(3520, 0.6, 0.25, (1.0, 0.3)) + tone(5274, 0.6, 0.2)
place(fx, glass, T["S05"] + 0.02, 0.035)
cue(T["S05"], "time freezes: rain and engine drop out, glass tone", "VFX")
burst_t = T["S05"] + 12 / FPS
whoosh = bandpass(rng.normal(0, 1, int(0.7 * SR)), 500, 7000) * np.exp(-np.arange(int(0.7 * SR)) / SR / 0.16)
place(fx, whoosh, burst_t, 0.42 if TRACK else 0.30)
tb = np.arange(int(0.6 * SR)) / SR
boom = np.sin(2 * np.pi * (38 * tb + 9.0 * (1 - np.exp(-tb / 0.06)))) * np.exp(-tb / 0.16)   # pitch falls 190 -> 38 Hz
if TRACK:
    place(fx, boom, burst_t, 0.32)
else:
    place(mus, tone(220, 1.2, 0.5, (1.0, 0.5, 0.3)) + tone(277.18, 1.2, 0.5, (1.0, 0.4)) + tone(329.63, 1.2, 0.5),
          burst_t, 0.10)
cue(burst_t, "burst: whoosh, low boom, the music drops", "VFX")
plink_t = T["S07"] + 3 / FPS
tt = np.arange(int(0.35 * SR)) / SR
plink = np.sin(2 * np.pi * (1500 * tt - 1100 * tt ** 2)) * np.exp(-tt / 0.07)
place(fx, plink, plink_t, 0.30)
cue(plink_t, "drop hits the puddle", "FOLEY")

# ---- the build, on the sixteenth-note grid
BEAT0 = T["S08"] + 0.25                       # first kerb stone: 7.0 s, an eighth note on the music grid
stone = click(0.07, 250, 2600, 0.016) + 0.7 * np.pad(tone(95, 0.07, 0.03), (0, 0))[: int(0.07 * SR)]
post = tone(1180, 0.16, 0.035, (1.0, 0.5, 0.25)) * 0.7 + click(0.16, 3000, 9000, 0.004)[: int(0.16 * SR)] * 0.4
lamp = tone(1760, 0.5, 0.16, (1.0, 0.3)) + tone(2637, 0.5, 0.12)
k = 0
while BEAT0 + k * 0.125 < T["S11"]:
    tm = BEAT0 + k * 0.125
    near = 1.0 if tm < T["S09"] else (0.45 if tm < T["S10"] else 0.7)   # close, from the air, chase
    hero = tm < T["S09"]            # in the restyled hero shot a stone lands every eighth note, not every sixteenth
    if not hero or k % 2 == 0:
        place(fx, stone * (0.9 + 0.2 * rng.random()), tm, (0.20 if hero else 0.16) * near)
    if k % (4 if hero else 2) == 0:
        place(fx, post, tm + 0.004, 0.07 * near)
    if k % 4 == 2 and not TRACK:                                        # pitched chime: only with the synth score
        place(fx, lamp, tm + 0.46, 0.035 * near)
    k += 1
cue(BEAT0, "kerb stones seat: one every 1/4 s in the hero shot (eighths at 120 BPM), sixteenths after", "FOLEY")
cue(BEAT0, "rail posts land on the eighths, metal tick", "FOLEY")
cue(BEAT0 + 0.71, "rail lamps light: soft chime on the half beats", "FOLEY")

# ---- music
musL, musR = np.zeros(N), np.zeros(N)
DROP_T = T["S05"] + 12 / FPS                  # 4.25 s: the burst, and beat one of the music
OUT_T = T["S11"]                              # 12.75 s: hard cut to the room, music stops dead
# Per track: `drop` = music time of the beat laid on the burst; `body_end` = the beat where the track's own
# ending starts (that ending becomes the end-card sting); `treat` = the track has no quiet intro of its own,
# so the part before the drop is filtered and held down.
ARR = {"A": dict(drop=5.53, body_end=13.53, treat=True),
       "B": dict(drop=5.53, body_end=12.03, treat=True),
       "C": dict(drop=8.03, body_end=16.03, treat=True),
       "D": dict(drop=6.03, body_end=13.53, treat=False)}


def synth_score():
    def pad(freqs, start, end, gain):
        s = np.zeros(N)
        for f in freqs:
            for det in (-0.4, 0.0, 0.5):
                s += np.sin(2 * np.pi * (f + det) * t + rng.random() * 6.28)
                s += 0.3 * np.sin(2 * np.pi * (2 * f + det) * t)
        return s / len(freqs) * env(start, end, 0.5, 0.5) * gain

    mus = np.zeros(N)
    mus += pad((73.42, 110.0), T["S04"], T["S08"] + 0.3, 0.030)                           # D drone in the rain
    mus += pad((146.83, 220.0, 261.63, 329.63), T["S08"], T["S09"] + 0.3, 0.045)          # Dm9, the build
    mus += pad((174.61, 261.63, 329.63, 392.0), T["S09"], T["S10"] + 0.3, 0.055)          # Fmaj9, the aerial
    mus += pad((196.0, 293.66, 349.23, 440.0, 523.25), T["S10"], T["S11"], 0.070)         # G9sus, the city opens
    arp = (293.66, 349.23, 440.0, 523.25, 440.0, 349.23)
    k = 0
    while BEAT0 + k * 0.25 < T["S11"] - 0.05:
        tm = BEAT0 + k * 0.25
        lift = 1.0 if tm < T["S10"] else 2.0
        place(mus, tone(arp[k % 6] * lift, 0.5, 0.14, (1.0, 0.35, 0.12)), tm, 0.030 + 0.012 * (tm > T["S09"]))
        k += 1
    kick = np.sin(2 * np.pi * (48 * tt[: int(0.3 * SR)] + 30 * np.exp(-tt[: int(0.3 * SR)] / 0.03))) \
        * np.exp(-tt[: int(0.3 * SR)] / 0.11)
    k = 0
    while BEAT0 + k * 0.5 < T["S11"] - 0.05:
        place(mus, kick, BEAT0 + k * 0.5, 0.16)
        k += 1
    mus *= 1 - env(T["S11"], T["S12"], 0.004, 0.004)                                      # hard cut: music out
    mus += pad((146.83, 220.0, 293.66, 369.99, 440.0), T["S12"], T["END"] + 1, 0.13)      # D major: resolved
    place(mus, tone(55, 1.5, 0.5) * 0.9, T["S12"], 0.30)
    place(fx, tone(1174.66, 1.2, 0.4, (1.0, 0.3)), T["S12"] + 0.25, 0.05)
    cue(T["S04"], "low D drone under the rain", "MUSIC")
    cue(T["S08"], "pulse, arpeggio and pad enter at 120 BPM", "MUSIC")
    cue(T["S10"], "widest chord, arpeggio up an octave", "MUSIC")
    cue(T["S11"], "clean stop on the hard cut", "MUSIC")
    cue(T["S12"], "end sting: D major pad and sub", "MUSIC")
    return mus


def generated_score(letter):
    a = ARR[letter]
    path = os.path.join(HERE, "music", f"MT15_music_{letter}.mp3")
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    src = np.frombuffer(raw, "<f4").reshape(-1, 2).astype(np.float64)
    out = np.zeros((N, 2))
    PRE = 0.020                               # every join sits 20 ms ahead of the beat, so no drum hit is cut

    def lay(film_t, music_t, length, fade_in=0.012, fade_out=0.012):
        """Copy `length` seconds of the track, starting at music_t, to film_t. Joins are short crossfades."""
        i0, m0, n = int(round(film_t * SR)), int(round(music_t * SR)), int(round(length * SR))
        if i0 < 0:
            m0, n, i0 = m0 - i0, n + i0, 0
        n = min(n, N - i0, len(src) - m0)
        seg = src[m0:m0 + n].copy()
        fi, fo = int(fade_in * SR), int(fade_out * SR)
        seg[:fi] *= np.linspace(0, 1, fi)[:, None]
        seg[n - fo:] *= np.linspace(1, 0, fo)[:, None]
        out[i0:i0 + n] += seg

    body = a["body_end"] - a["drop"]                        # seconds of full music the track gives us
    rest = (OUT_T - DROP_T) - body                          # what is still missing up to the hard cut
    lay(0.0, a["drop"] - DROP_T, DROP_T - PRE + 0.012)                                  # everything before the drop
    lay(DROP_T - PRE - 0.012, a["drop"] - PRE - 0.012, body + 0.012)                    # the drop and the ride
    if rest > 0.01:                                         # repeat from one bar back, so the bar count stays right
        lay(DROP_T + body - PRE - 0.012, a["body_end"] - 2.0 - PRE - 0.012, rest + PRE + 0.012, fade_out=0.004)
    lay(T["S12"] - PRE, a["body_end"] - PRE, T["END"] - T["S12"] + PRE, fade_in=0.004)  # the track's own ending
    ride = (t >= DROP_T) & (t < OUT_T)
    out *= 0.15 / np.sqrt((out[ride] ** 2).mean())          # same ride level for every track
    # before the drop: low and muffled in the room, opening in the rain, gone while the drop hangs
    u_rain = np.clip((t - T["S04"]) / (T["S05"] - T["S04"]), 0, 1)
    hang = np.clip((t - T["S05"]) / 0.10, 0, 1) * (t < DROP_T - PRE)
    pre = t < DROP_T - PRE
    if a["treat"]:
        low = np.stack([bandpass(out[:, c] * pre, 20, 420) for c in (0, 1)], 1)
        open_ = (0.65 * u_rain ** 1.5)[:, None]             # how much of the full-range track is let through
        gain = 10 ** ((-17 + 9 * u_rain) / 20)
        shaped = (low * (1 - open_) * 2.0 + out * open_) * gain[:, None]
    else:
        shaped = out * (10 ** (6 / 20))                     # the track's own quiet build, lifted a little
    shaped = shaped * (1 - 0.97 * hang)[:, None] * np.clip((t - (T["S04"] - 0.05)) / 0.45, 0, 1)[:, None]
    out = np.where(pre[:, None], shaped, out)
    out *= np.clip((DROP_T - PRE - t) / 0.004, 0, 1)[:, None] * pre[:, None] + (~pre)[:, None]
    place(fx, boom, T["S12"], 0.40)
    cue(T["S04"], f"music track {letter} enters with the rain, filtered, opening up (no music in the room)", "MUSIC")
    cue(T["S05"], "music out: time stops on the drop", "MUSIC")
    cue(DROP_T, "the drop: full track from here, one beat every 12 frames", "MUSIC")
    cue(OUT_T, "hard cut to the room: music stops dead", "MUSIC")
    cue(T["S12"], "end card: the track's own final hit and tail, low boom", "MUSIC")
    return out[:, 0], out[:, 1]


# ---- 4% and the end card
place(fx, tone(880, 0.08, 0.03), T["S11"] + 0.55, 0.16)
place(fx, tone(1174.66, 0.14, 0.05), T["S11"] + 0.66, 0.16)
cue(T["S11"] + 0.55, "TV blip: 4%", "FOLEY")

# ---- mix
if TRACK:
    musL, musR = generated_score(TRACK)
    wet = reverb(fx, 1.6, 0.22)
else:
    wet = reverb(fx + synth_score() * 0.9, 1.6, 0.22)
centre = wet + amb + veh
fade = np.clip((T["END"] - t) / 0.12, 0, 1)                    # no click on the last frame
width = bandpass(rng.normal(0, 1, N), 2000, 9000) * 0.004 * rain_level
left, right = (centre + musL + width) * fade, (centre + musR - width) * fade
peak = max(np.abs(left).max(), np.abs(right).max())
stereo = np.stack([left, right], 1) / peak * 0.80

import wave
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((stereo * 32767).astype("<i2").tobytes())
if len(sys.argv) > 2 and sys.argv[2] != "-":
    with open(sys.argv[2], "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["frame", "seconds", "track", "cue"])
        wr.writerows(sorted(cues))
if TRACK:                                                       # levels by section, for the mix notes
    def db(x, a, b):
        m = (t >= a) & (t < b)
        return 20 * np.log10(np.sqrt((x[m] ** 2).mean()) + 1e-9)
    for name, a, b in (("room", 0, T["S04"]), ("rain", T["S04"], T["S05"]), ("hang", T["S05"], DROP_T),
                       ("ride", DROP_T, OUT_T), ("room2", OUT_T, T["S12"]), ("card", T["S12"], T["END"])):
        print(f"  {name:6s} music {db(musL, a, b):6.1f}  ambience {db(amb, a, b):6.1f}  engine {db(veh, a, b):6.1f}"
              f"  effects {db(wet, a, b):6.1f} dB")
print("audio written", sys.argv[1], f"{DUR}s", f"peak {peak:.3f}")
