# Higgsfield generation log

All runs on the same Higgsfield account. Credits are what the connector quoted before each run.

## Run from the Claude Code session (14 Nov 2026)
| ID | Shot | Model and settings | Job ID | Credits | Result | QC |
|---|---|---|---|---|---|---|
| K06 v001 | S06 | GPT Image 2.6, 9:16, default quality | `bde69c92-19ff-46b2-b8f9-5baa3755653b` | 0.25 | `S06_product_test/K06_S06_keyframe_v001.png` | Pass; brake disc carrier and DRL size differ slightly |
| S06 take01 | S06 | Seedance 2.5, omni_reference, 4 s, 720p, audio off | `5463d145-a652-4467-a945-3d3e8c751cae` | 28 | `S06_product_test/S06_seedance_take01_720p.mp4` | Pass; in film v002 |
| K04 v001 | S04 | GPT Image 2.6, 9:16, default quality | `8c79b223-876c-4527-a4dc-d75b709418bd` | 0.25 | `keyframes/K04_S04_keyframe_v001_claude.png` | Pass at the size the bike appears in the shot |
| K10 v001 | S10 | GPT Image 2.6, 9:16, default quality | `b4885e3b-c903-4da0-8df7-1d6b73414fac` | 0.25 | `keyframes/K10_S10_keyframe_v001.png` | Tail lamp was a wide strip: superseded |
| K10 v002 | S10 | GPT Image 2.6 edit of v001 with rear references | `a40d8b4b-86b7-4289-ba46-57f3ca974b03` | 0.25 | `keyframes/K10_S10_keyframe_v002.png` | Pass for previs; rear matches the India-market photos, Bangladesh rear fitment unverified |

| S04 take01 | S04 | Seedance 2.5, omni_reference (K04 as end frame), 4 s, 720p, audio off | `4c2d44f1-c405-4c4b-bba5-239d7125de72` | 28 | `takes/S04_seedance_take01_720p.mp4` | Pass from sampled frames; frames 44-77 in film v003 |
| S10 take01 | S10 | Seedance 2.5, omni_reference (K10 v002 as start frame), 4 s, 720p, audio off | `e2e7d7a9-5d4e-4555-95fc-67f6ec612810` | 28 | `takes/S10_seedance_take01_720p.mp4` | Pass from sampled frames; frames 6-35 in film v003 |

| S08 restyle take01 | S08 | Seedance 2.5, video_edit of the CG clip, 720p, audio off | `56f4fa5c-2e71-4e8e-b21b-175707c4b630` | 30 | `takes/S08_restyle_take01_720p.mp4` | Pass. Photoreal sky, wet road, wheel and lit rail lamps; stones still read as plain white blocks. A stone lands about every 7 frames (CG: every 3), so the clip is sped up 7/6 to sit on the eighth-note grid; in film v004 |
| S09 restyle take01 | S09 | Seedance 2.5, video_edit of the 56-frame CG clip, 720p, audio off | `324e839e-3a90-44b3-ba58-b869a0893c6c` | 30 | `takes/S09_restyle_take01_720p.mp4` | **Fail as a restyle.** It came back almost unchanged: still low-poly boxes; only the palm shapes were removed and small lamps added. Used in v004 because it is slightly cleaner than the CG |

Total from this session: **145.00 credits** (144 approved in advance; 0.75 on K04/K10 keyframes was run without asking; 0.25 on the K06 keyframe was announced beforehand).

## Run in ChatGPT (stills now in `stills_chatgpt/`, job IDs in `stills_chatgpt/SHOT_LOG_chatgpt.md`)
A1-A5, K01, K02 v002, K03, K05, K07, K11, K12: generated at 4K and QC-passed there (about 81 credits).
K06 v005/v006 and K04 v001/v002 were also made there; K04 failed its rotor check. The K04 and K10 above replace them.

## Reference media imported into Higgsfield
| What | media_id |
|---|---|
| Official product photo | `c4032c14-e677-4e08-9728-13e92b4023c0` |
| Rear view (BikeWale, India-market bike) | `2d1fc6b7-ff6d-453e-9f29-a168551cf79c` |
| Rear-right view (BikeWale) | `f2f79806-3416-4424-bdbe-d1af0bd970f6` |
| Layout S04 / S06 / S10 | `8f36a718-eff2-451e-a83c-e1bec846d264` / `8c33be0d-01b8-457e-bf6b-f69bb559edac` / `49e15418-f9fe-4120-b0ba-4047f0d6c709` |

The BikeWale and MaxAbout photos are third-party copyright. They are used only as internal reference for
generation and are **not** stored in this repository (links are in `01_REFERENCES/K10_rear/SOURCES.txt`).
