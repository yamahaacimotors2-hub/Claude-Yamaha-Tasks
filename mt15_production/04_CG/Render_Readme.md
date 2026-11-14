# Render readme (v1)

| Item | Value |
|---|---|
| Tool | Blender 5.3 as the `bpy` Python module, Cycles, CPU |
| Scene source | `film.py` (all shots) built on `../../mt15_blender_proof/proof.py` |
| Frame rate | 24 fps |
| Render size | 720x1280 for S01-S11, 1080x1920 for the end-card background (BG12) |
| Samples | 16 (road), 24 (room and macro), 64 (BG12), OpenImageDenoise on |
| Output | 8-bit sRGB PNG sequences, one folder per shot, `f0001.png` ... |
| Colour | AgX view (Blender default) for room and road shots, Standard for S05 and S07 |
| Motion blur | On for S04, S05, S06, S07, S08, S10 (shutter 0.5) |
| Passes | Beauty only. No EXR or Cryptomatte in v1: nothing is composited over the CG yet |

Render everything:  `./render_all.sh /path/to/frames`
One shot or a few frames:  `python3 film.py --shot S08 --frames 30-40 --out /path/to/frames/S08`
Title-free TV screens:  add `--tv clean` to S01 and S11.
TV screens and text PNGs:  `NODE_PATH=<global node_modules> node make_assets.mjs` (needs Playwright/Chromium).

Then: `python3 ../06_COMP/post.py FRAMES OUT` (rain, grade, bloom, end card, upscale to 1080x1920)
and `python3 ../07_EDIT_SOUND/audio.py mix.wav` (soundtrack).
