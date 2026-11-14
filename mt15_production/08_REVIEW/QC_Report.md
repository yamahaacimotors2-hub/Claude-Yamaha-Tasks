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

---
## v008 addendum (14 Nov 2026) — no generation cost
Owner notes on v007: **track A chosen**; the bike sound around seconds 2-4 was odd and the mix should be
smoother; the bell on the helmet shot should be something else.
- **Engine rebuilt as one continuous voice.** Before, each shot had its own gated engine segment, so the level
  stepped at every cut: it came in hard and loud at 2.58 s (about 12 dB above the room), and a steady 118 Hz note
  kept running over the slow-motion raindrop from 4.25 to 5.25 s. Now level and pitch follow curves: the bike
  swells in, peaks as it crosses the stall, and falls away; there is **no engine at all during the raindrop shot**;
  it returns with the bike at 5.25 s. The tone is softer (fewer high harmonics) and has wet-tyre hiss mixed in.
  The pass-by peak is about 7 dB lower than in v007.
- **Rain** now fades in over 0.2 s, starting two frames before the cut, instead of switching on.
- **Helmet shot:** the bell is gone. In its place: a soft airy swish that follows the glint across the visor
  and a low double thump, like a heartbeat, under it.
- Burst boom slightly lower so the limiter works less on the drop.
- Picture unchanged from v007. Master and phone copy carry track A.
Technical check: 384 frames, 16.000 s, -14.1 LUFS, peak -1.4 dBFS, no decode errors (`technical_qc_v008.txt`).
Still measured, not listened to, on this side.

---
## v009 addendum (14 Nov 2026) — sound only, no generation cost
Owner notes on v008: the opening should read as boredom (and show a bored face); the sound should go
boring room, then a bike revving that comes in smoothly, then the instrumental music.
- **Room (0 - 1.4 s):** no music at all now. A wall clock (tick-tock every 0.5 s) and a slow ceiling fan over room
  tone. The clock and fan come back in the last room shot, so the film ends where it began.
- **The idea (from 1.4 s, the helmet shot):** the engine starts inside the room, muffled, with two rising revs,
  while the clock and fan fade away. It runs straight into the pass-by on the road; no gap, no step.
  The swish and heartbeat from v008 are gone; the engine is the idea.
- **Music** enters with the rain at 2.58 s, filtered and opening up, drops out while the raindrop hangs, and hits
  on the burst as before.
- Level contour by quarter second, start to drop (dBFS before mastering): -41 in the room, -29 as the rev starts,
  -24 at the rev peak, -23 on the road, -30 on the hanging drop, -15 on the burst.
- Picture unchanged. **Open picture problem:** S01 still shows the man from behind, so no bored face is visible;
  storyboard panels 01 and 02 (bored face beside the TV, then a glance at the helmet) need a new generated take.
Technical check: 384 frames, 16.000 s, no decode errors (`technical_qc_v009.txt`). Engine and clock are still
synthesised; a recorded-sounding rev would need a generated sound effect (1 credit quoted).

---
## v010 addendum (14 Nov 2026) — new opening shot and rev sound, 29.25 credits (approved)
- **S01 + S02 are now one generated take of the man's face** (storyboard panels 01 and 02): slumped on the sofa,
  cheek on his fist, a slow heavy blink and sigh, then his eyes go to the helmet and he half-smiles.
  The download screen ("GTA VI 3%") is composited onto the blank blue TV behind him, frame by frame; his hair
  stays in front of it. The old S01 (man from behind) and S02 (helmet still with a glint) are out.
- The take ran slower than asked, so it is retimed: the boredom at 2.3x (the long sigh reads as one slow blink),
  the glance and smile at 1.5x. Frame-accurate picks, no blending. Worth watching for jerkiness in the glance.
- **Engine from the glance to the end of the pass-by is a generated, recording-like effect**, not the synth:
  its idle fades in muffled in the room at 1.35 s, its rev lands on the cut to the road (about 2.55 - 3.05 s),
  and it falls away as time stops on the raindrop. The synth engine is used only under the music from 5.25 s.
- Continuity notes: his hair is fuller in the opening than the face inside the helmet in S03 suggests;
  S11 (last room shot) is still the old still seen from behind, with the helmet on.
Technical check: 384 frames, 16.000 s, -14.1 LUFS, peak -1.4 dBFS, no decode errors (`technical_qc_v010.txt`).
Sound still measured only, not listened to, on this side.

---
## v011 addendum (14 Nov 2026) — sound only, no generation cost
Owner note on v010: the opening needs a tension background music, playing very low.
- **Tension bed under the room (0 - 2.6 s).** It is made from track A itself: 1.2 s of the track smeared into a
  dark drone (70 - 900 Hz), so it is in key with the music that follows. It pulses softly on the beat (every
  0.5 s, with the clock), swells slowly toward the cut, and hands over to the track as the rain starts.
- Level: about 22 dB below the ride music; the room as a whole rises from about -37 to -32 dBFS before the
  engine comes in (it was -41 with clock and fan only).
- The wall clock now ticks on the same beat grid as the music.
- Picture unchanged from v010.
Technical check: 384 frames, 16.000 s, no decode errors (`technical_qc_v011.txt`). Measured, not listened to.
If the bed does not read as tension by ear, the alternative is a short generated suspense cue (2.33 credits
for one, 9.32 for four variations), which needs the owner's approval.

---
## v012 addendum (14 Nov 2026) — owner's clip for the helmet shot, no generation cost
- **S03 is now the clip the owner supplied** (`05_GENERATIONS/takes/S03_owner_buckle_clip_v001.mp4`, 784x1168,
  37 frames): front view of the helmet, gloved hands at the chin strap, the dark visor closes. The Seedance
  visor take is out of the cut.
- Fitted as: centre-cropped to 9:16, every second frame (double speed), 16 frames in the film (was 12).
  The 4 extra frames come from the tea-stall shot (S04, now 24). The visor seats on local frame 10, where the
  click is. The engine rev stays anchored on the cut to the road, which moved to frame 66 (2.75 s).
- Things to know about this clip:
  1. The helmet and both gloves carry **Yamaha wordmarks and tuning-fork emblems**. If the clip is generated,
     the marks are drawn by the model, not placed from the official file: ACI should check them before publishing.
  2. Continuity: here the visor is dark and the helmet has a logo; in the riding shots the helmet is plain and
     in the last room shot the visor is clear. The clip is also near black-and-white on a grey background,
     while the room shots are blue and amber.
  3. Source and rights of the clip are not recorded; added to the rights sheet as owner-supplied, to confirm.
Technical check: 384 frames, 16.000 s, -14.1 LUFS, peak -1.4 dBFS, no decode errors (`technical_qc_v012.txt`).
