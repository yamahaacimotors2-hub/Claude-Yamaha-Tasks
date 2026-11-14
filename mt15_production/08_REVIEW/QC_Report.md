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

---
## v006 addendum (14 Nov 2026) — three Seedance takes, 84.25 credits (approved)
- **S05 (raindrop) is now a real take and the best shot in the film.** The headlight star arrives behind the drop,
  the drop opens on its right side and throws an amber sheet that turns magenta at the edges, with ligaments and
  droplets, in slow motion. It matches storyboard panel 06. The shot is 36 frames now (was 30); the 6 frames
  come from the tea-stall shot (S04, now 28). The burst starts on local frame 12, on the whoosh.
- **S03 (visor)** is a real take: the visor snaps down on the click, the face stays visible through the clear visor.
  Note: the helmet shell changes slightly as the visor closes (top vent, surface). It passes at speed; it shows
  if you step through frames.
- **S09 (aerial) is back**, generated from a new photoreal keyframe (K09). One frame shows the finished street
  behind, the city appearing around the bike and plain white blocks ahead. Played at double speed (frame pairs
  averaged) so the build reads in 1.5 s. The bike is small; product detail is not checkable at this size.
- S10 is back to 30 frames. Sound: aerial engine and stone levels restored to the v004 mix; S03 click is the visor.
- Continuity note: the aerial ends with white blocks ahead, the chase (S10) opens on a fully built street.
Technical check repeated: 384 frames, 16.000 s, -14.1 LUFS, no decode errors (`technical_qc_v006.txt`).
Still open: S08 stones read as white blocks; S01/S11 are stills (the man does not move); bike shots are 720p
upscaled; Yamaha logo is a placeholder; game-title clearance and the Bangladesh rear fitment are unconfirmed;
nobody has listened to the synthesised sound on a phone yet.

---
## v007 addendum (14 Nov 2026) — music and re-cut, 9.32 credits (approved)
Owner note on v006: picture fine, raindrop as wanted, sound design not right; wanted the feel of the game's music.
The game's own music cannot be used (third-party copyright). Instead: four original 1980s Miami synthwave
tracks, generated from our own prompt, and the film re-cut to them.
- **Picture is now cut on the beat.** The music's first beat is the raindrop burst (frame 102, 4.25 s) and a beat
  falls every 12 frames after it. S06 (126), S07 (150), S08 (162), S09 (234), S10 (270), S11 (306) and the end
  card (342) all start on a beat. Changed lengths: S07 12 (was 14), S10 36 (was 30), S11 36 (was 40).
- **Music shape:** low and muffled in the room, opening in the rain, silent for the half second the drop hangs,
  full from the burst, stops dead on the hard cut to the room, and the track's own final hit lands on the end card.
- **Sound effects** stay synthesised and sit under the music: rain, engine (lower during the ride), visor click,
  whoosh and a low boom on the burst, puddle plink, kerb stones on the eighth notes from 7.0 s, TV blip.
  Pitched extras from the old score (burst chord, lamp chimes, end pad) are off so they cannot clash with the key.
- **Loudness** is now one fixed gain to -14 LUFS with a peak limiter. The old one-pass normaliser rode the level,
  which lifted the quiet room and pulled the loud part down.
- Four phone copies, same picture: `MT15_mobile_v007_musicA/B/C.mp4` and `MT15_mobile_v007.mp4` (track D).
  The master carries track D until one is chosen.
Checked by measurement only: kicks sit within about 10 ms of the beat grid in A, B and D; C has a dotted rhythm
that could not be checked the same way. **Nobody has listened to these mixes yet** — the choice of track and
the balance of music against effects need the owner's ears.
Technical check: 384 frames, 16.000 s, -14.3 LUFS, peak -1.4 dBFS, no decode errors (`technical_qc_v007.txt`).
