# QC report — MT15_master_v001

Checked by Claude Code from still frames and measurements. **Nobody has watched it in motion yet, and nobody has heard the sound.**

## Technical (measured)
| Check | Result |
|---|---|
| Size, frame rate | 1080x1920, 24 fps |
| Frames, duration | 384 frames, 16.000 s |
| Video | H.264, yuv420p, Rec.709 tags |
| Audio | AAC stereo, 48 kHz, integrated loudness -14.2 LUFS, true peak -1.5 dBFS |
| Decode errors | None |
| Shot lengths | Match `03_ANIMATIC/Frame_Index.csv` exactly |

Raw output: `technical_qc_v001.txt`.

## What reads (from stills)
| Beat | Status |
|---|---|
| TV: game title, 3%, preview picture | Reads. Head sits below the screen |
| Helmet as the idea | Helmet reads; the glint is subtle |
| Visor snap | Reads (eyes visible, then visor shut) |
| Rainy Dhaka from the tea stall | Reads, low-poly |
| Raindrop burst | Reads as coloured beads, not liquid |
| Bike low 3/4 | Silhouette only. NOT product accurate |
| Puddle ripple | Reads |
| Hero build: beam, stones seat, posts rise, wheel | Reads |
| Hero build: lamp comes on, then its reflection | **Weak.** The rail lamps light after they have left the frame |
| Aerial: built behind, grey ahead | Reads; water side is very dark |
| Chase: the city opens | Reads |
| Same room, 4%, helmet still on | Reads |
| End card: official bike, tagline | Reads. Bangla shaped correctly |

## Known issues
1. **Product accuracy.** Only the end card shows the real MT-15 (the official photo). In every other shot the bike is a proxy; front wheel, fork and fender are modelled, the rest is not.
2. **No human face.** Room shots show the man from behind or in a helmet.
3. **Resolution.** S01-S11 were rendered at 720x1280 and upscaled. The end card is native 1080x1920.
4. **Kerb stones blow out to white** in the headlight in S08.
5. **Yamaha logo is a placeholder box.**
6. **Game title on the TV has no written clearance.** A title-free TV texture is ready (`--tv clean`).
7. **S04 geography:** the bike passes the stall a few metres before where S08 starts; fine in the cut, not literal.
8. Sound is fully synthesised and unheard by a person: levels were set by measurement only.

## Not done (needs a person or a tool this session does not have)
- Three fresh viewers watching with sound off (SOP step 09 / old step 20).
- Phone full-screen check of safe areas and readability.
- Codex review pass.
- Higgsfield shots, After Effects / Premiere / Photoshop steps on Niloy's machine.

---
## v002 addendum (14 Nov 2026)
Only change from v001: **S06 is now the Higgsfield take** (Seedance 2.5 from a GPT Image 2.6 keyframe), so the
film has a moving, product-accurate MT-15 in one shot. Same length, same sound. Technical check repeated:
384 frames, 16.000 s, -14.2 LUFS, no decode errors (`technical_qc_v002.txt`).
New continuity note: the generated road in S06 already has a waterside railing and street lamps, while the
CG shots around it show that side unfinished.

---
## v003 addendum (14 Nov 2026)
Eight of the twelve shots are now photoreal:
- **S01, S02, S07, S11** are built from the approved 4K stills with `06_COMP/stills.py` (TV screen corner-pinned,
  slow push-ins, glint on the helmet, travelling ripples on the puddle). No generation cost.
- **S04, S06, S10** are Seedance 2.5 takes. **S12** uses the generated waterfront plate behind the official bike photo.
- **Still CG:** S03 (visor), S05 (raindrop burst), S08 (hero build), S09 (aerial). They no longer match the look of
  the shots around them; this is now the main visible problem.
Technical check repeated: 384 frames, 16.000 s, -14.2 LUFS, no decode errors (`technical_qc_v003.txt`).
Known: S01 and S11 are stills with camera moves, so the man does not move; S04 and S10 were judged from six
sampled frames each, not in motion.

---
## v004 addendum (14 Nov 2026)
- **S08** is now the Seedance restyle of the CG hero shot: photoreal dusk sky, wet road, cyan wheel and gold fork,
  rail lamps that light up with reflections on the road. Stones still look like plain white blocks. Cadence changed
  from one stone per 3 frames to about one per 7; the clip is sped up 7/6 and the stone sounds moved to eighth notes.
- **S09** restyle did not work: the aerial is still visibly low-poly. It is the weakest shot in the film now.
- **Still CG:** S03 (visor), S05 (raindrop burst).
Technical check repeated: 384 frames, 16.000 s, -14.2 LUFS, no decode errors (`technical_qc_v004.txt`).

---
## v005 addendum (14 Nov 2026) — no generation cost
- **S03** is now the approved K03 still (helmet on, hand at the chin strap) with a small snap on the click frame.
  The man does not move; the sound is a buckle click.
- **S05** is the approved K05 still with the beam arriving as a 2D light and the CG colour burst laid over it.
  The drop is photoreal; the burst still reads as strings of glowing beads, not liquid.
- **S09 (aerial) is out of the cut.** Its restyle failed and it was the only visibly low-poly shot left.
  The chase (S10) now runs 66 frames (2.75 s) in its place. To restore the aerial, see the note in `06_COMP/post.py`.
- Result: every shot in the film is photoreal or built from a photoreal still. Eleven shots, 384 frames.
Technical check repeated: 384 frames, 16.000 s, -13.9 LUFS, no decode errors (`technical_qc_v005.txt`).
Lost with the aerial: the single frame that showed "built behind, building at the bike, grey ahead" all at once.
