# Delivery note — v001 (first full version, internal review)

| File | What it is |
|---|---|
| `MT15_master_v001.mp4` | 1080x1920, 24 fps, 16.000 s, 384 frames, H.264 (CRF 17, max 20 Mbps), AAC 256k, -14.2 LUFS |
| `MT15_mobile_v001.mp4` | Same picture, lighter encode (max 8 Mbps) for phones and messaging |
| `../08_REVIEW/MT15_review_burnin_v001.mp4` | 540x960 with shot ID and frame number burned in |
| `../08_REVIEW/stills/S01.jpg` ... `S12.jpg` | One frame per shot |
| `../08_REVIEW/QC_Report_v001.md` | What was checked and what is still wrong |

**Status: review, not approved, not for publishing.**
Blocking before any public use: written clearance for the game title, the official Yamaha logo,
product-accurate bike shots, client sign-off.

Rebuild from source: `04_CG/render_all.sh FRAMES` then `./finish.sh FRAMES WORK v002`.

## Latest: v006 (14 Nov 2026)
`MT15_master_v006.mp4` / `MT15_mobile_v006.mp4`, same specification, -14.1 LUFS. Twelve shots; S03, S05 and S09 are
new Seedance takes. Changes per version: `../08_REVIEW/QC_Report.md`. Status is still **review, not for publishing**.
Rebuild: `python3 06_COMP/stills.py STILLS FRAMES S01 S02 S07 S11`, `python3 06_COMP/takes.py FRAMES`,
then `./finish.sh FRAMES WORK v006` (S06 and S08 frames come from their takes as noted in `05_GENERATIONS/Generation_Log.md`).

## Latest: v007 (14 Nov 2026)
Cut to music. `MT15_master_v007.mp4` and `MT15_mobile_v007.mp4` carry music track D; `MT15_mobile_v007_musicA/B/C.mp4`
are the same picture with the other three tracks, for choosing one. Rebuild: `python3 06_COMP/takes.py FRAMES`,
`./finish.sh FRAMES WORK v007 D`, then `07_EDIT_SOUND/variants.sh WORK v007`. Status: **review, not for publishing**.
