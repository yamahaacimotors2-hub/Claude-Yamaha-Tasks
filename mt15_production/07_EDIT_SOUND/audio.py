"""Sound design and music for the MT-15 16 s film, v1. Everything here is synthesised from scratch
(no samples, no recordings), so there is nothing to clear.

Usage:  python3 audio.py OUT.wav [CUE_SHEET.csv]

The city is built in time with the music: at 8 m/s one kerb stone seats every 1/8 s, which is a
sixteenth note at 120 BPM. Rail posts land on the eighths and the rail lamps light on the half beats.
"""
import csv
import sys

import numpy as np

SR, FPS, DUR = 48000, 24, 16.0
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(4)
CUT = {"S01": 0, "S02": 30, "S03": 50, "S04": 62, "S05": 96, "S06": 126, "S07": 150, "S08": 164,
       "S09": 236, "S10": 272, "S11": 302, "S12": 342, "END": 384}
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
rain_level = env(T["S04"], T["S11"], 0.01, 0.01) * freeze
rain_level *= 1 - 0.55 * env(T["S08"], T["S11"], 0.8, 0.01)             # the rain thins as the city arrives
amb += rain * 0.060 * rain_level
cue(T["S01"], "room tone, TV fan", "AMBIENCE")
cue(T["S04"], "hard cut to rain bed", "AMBIENCE")
cue(T["S11"], "hard cut back to room tone", "AMBIENCE")

# ---- room beats
for k in range(5):                                                       # the download that will not move
    place(fx, tone(1320, 0.05, 0.012), 0.20 + k * 0.5, 0.05)
cue(0.20, "UI tick, repeats every 0.5 s", "FOLEY")
place(fx, reverb_small := tone(2637, 0.9, 0.22, (1.0, 0.4, 0.15)), T["S02"] + 12 / FPS, 0.10)
cue(T["S02"] + 12 / FPS, "idea: glint ting on the visor", "FOLEY")
snap = click(0.05, 1500, 9000, 0.006) * 0.9 + np.pad(tone(140, 0.05, 0.02), (0, 0))[: int(0.05 * SR)] * 0.8
place(fx, snap, T["S03"] + 7 / FPS, 0.34)
cue(T["S03"] + 7 / FPS, "chin-strap buckle click", "FOLEY")

# ---- vehicle: a synthesised single-cylinder note, never a recording
def engine(start, end, f0, f1, gain, pan_bias=0.0):
    seg = (t >= start) & (t < end)
    u = np.clip((t - start) / (end - start), 0, 1)
    freq = f0 + (f1 - f0) * u
    phase = 2 * np.pi * np.cumsum(freq) / SR
    saw = sum(np.sin(phase * k) / k for k in range(1, 14))
    pulse = 0.6 + 0.4 * np.sin(phase * 0.5) ** 2                          # firing pulses
    return bandpass(saw * pulse, 60, 1900) * seg * gain * env(start, end, 0.04, 0.04)


veh += engine(T["S04"], T["S05"], 92, 118, 0.20)                          # pass-by from the stall
veh += engine(T["S05"], T["S06"], 118, 118, 0.20) * freeze
veh += engine(T["S06"], T["S07"], 118, 126, 0.24)
veh += engine(T["S07"], T["S08"], 126, 126, 0.10)
veh += engine(T["S08"], T["S09"], 126, 132, 0.17)
veh += engine(T["S09"], T["S10"], 132, 138, 0.19)                         # v005: chase picture from here
veh += engine(T["S10"], T["S11"], 138, 150, 0.22)
cue(T["S04"], "engine pass-by (synth)", "VEHICLE")
cue(T["S10"], "engine opens up", "VEHICLE")

# ---- the raindrop
glass = tone(3520, 0.6, 0.25, (1.0, 0.3)) + tone(5274, 0.6, 0.2)
place(fx, glass, T["S05"] + 0.02, 0.035)
cue(T["S05"], "time freezes: rain and engine drop out, glass tone", "VFX")
burst_t = T["S05"] + 12 / FPS
whoosh = bandpass(rng.normal(0, 1, int(0.7 * SR)), 500, 7000) * np.exp(-np.arange(int(0.7 * SR)) / SR / 0.16)
place(fx, whoosh, burst_t, 0.30)
place(mus, tone(220, 1.2, 0.5, (1.0, 0.5, 0.3)) + tone(277.18, 1.2, 0.5, (1.0, 0.4)) + tone(329.63, 1.2, 0.5),
      burst_t, 0.10)
cue(burst_t, "burst: whoosh and a bright chord", "VFX")
plink_t = T["S07"] + 3 / FPS
tt = np.arange(int(0.35 * SR)) / SR
plink = np.sin(2 * np.pi * (1500 * tt - 1100 * tt ** 2)) * np.exp(-tt / 0.07)
place(fx, plink, plink_t, 0.30)
cue(plink_t, "drop hits the puddle", "FOLEY")

# ---- the build, on the sixteenth-note grid
BEAT0 = T["S08"] + 0.375                      # the first kerb stone lands here
stone = click(0.07, 250, 2600, 0.016) + 0.7 * np.pad(tone(95, 0.07, 0.03), (0, 0))[: int(0.07 * SR)]
post = tone(1180, 0.16, 0.035, (1.0, 0.5, 0.25)) * 0.7 + click(0.16, 3000, 9000, 0.004)[: int(0.16 * SR)] * 0.4
lamp = tone(1760, 0.5, 0.16, (1.0, 0.3)) + tone(2637, 0.5, 0.12)
k = 0
while BEAT0 + k * 0.125 < T["S11"]:
    tm = BEAT0 + k * 0.125
    near = 1.0 if tm < T["S09"] else 0.6                                # hero shot close, then the chase
    hero = tm < T["S09"]            # in the restyled hero shot a stone lands every eighth note, not every sixteenth
    if not hero or k % 2 == 0:
        place(fx, stone * (0.9 + 0.2 * rng.random()), tm, (0.20 if hero else 0.16) * near)
    if k % (4 if hero else 2) == 0:
        place(fx, post, tm + 0.004, 0.07 * near)
    if k % 4 == 2:
        place(fx, lamp, tm + 0.46, 0.035 * near)
    k += 1
cue(BEAT0, "kerb stones seat: one every 1/4 s in the hero shot (eighths at 120 BPM), sixteenths after", "FOLEY")
cue(BEAT0, "rail posts land on the eighths, metal tick", "FOLEY")
cue(BEAT0 + 0.71, "rail lamps light: soft chime on the half beats", "FOLEY")

# ---- music: restrained synth, opens up with the city
def pad(freqs, start, end, gain):
    s = np.zeros(N)
    for f in freqs:
        for det in (-0.4, 0.0, 0.5):
            s += np.sin(2 * np.pi * (f + det) * t + rng.random() * 6.28)
            s += 0.3 * np.sin(2 * np.pi * (2 * f + det) * t)
    return s / len(freqs) * env(start, end, 0.5, 0.5) * gain


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
cue(T["S04"], "low D drone under the rain", "MUSIC")
cue(T["S08"], "pulse, arpeggio and pad enter at 120 BPM", "MUSIC")
cue(T["S10"], "widest chord, arpeggio up an octave", "MUSIC")
cue(T["S11"], "clean stop on the hard cut", "MUSIC")

# ---- 4% and the end card
place(fx, tone(880, 0.08, 0.03), T["S11"] + 0.55, 0.16)
place(fx, tone(1174.66, 0.14, 0.05), T["S11"] + 0.66, 0.16)
cue(T["S11"] + 0.55, "TV blip: 4%", "FOLEY")
sting = pad((146.83, 220.0, 293.66, 369.99, 440.0), T["S12"], T["END"] + 1, 0.13)   # D major: resolved
sub = tone(55, 1.5, 0.5) * 0.9
mus += sting
place(mus, sub, T["S12"], 0.30)
place(fx, tone(1174.66, 1.2, 0.4, (1.0, 0.3)), T["S12"] + 0.25, 0.05)
cue(T["S12"], "end sting: D major pad and sub", "MUSIC")

# ---- mix
wet = reverb(fx * 1.0 + mus * 0.9, 1.6, 0.22)
dry = amb + veh
mix = wet + dry
mix *= np.clip((T["END"] - t) / 0.12, 0, 1)                    # no click on the last frame
width = bandpass(rng.normal(0, 1, N), 2000, 9000) * 0.004 * rain_level
left, right = mix + width, mix - width
peak = max(np.abs(left).max(), np.abs(right).max())
stereo = np.stack([left, right], 1) / peak * 0.80

import wave
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((stereo * 32767).astype("<i2").tobytes())
if len(sys.argv) > 2:
    with open(sys.argv[2], "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["frame", "seconds", "track", "cue"])
        wr.writerows(sorted(cues))
print("audio written", sys.argv[1], f"{DUR}s", f"peak {peak:.3f}")
