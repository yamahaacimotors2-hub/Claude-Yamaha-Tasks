# Suno prompt sheet — music and background bed for the MT-15 16 s film

Suno cannot be run from the Claude Code session (no Suno connector, no official API, and Suno is not in the
Higgsfield model list on this account). The owner generates on suno.com with the prompts below and hands the
files over; the cut to picture, the mix and the loudness are then done with `audio.py`.

## How to generate
1. suno.com → **Create** → **Custom** mode, newest model.
2. Turn **Instrumental** off, paste the *Style* text into the style box and the *Structure* text into the lyrics box.
   The structure text contains only section tags, so the result is still instrumental. (If the result has singing,
   regenerate with Instrumental on and the style text only.)
3. Each run gives two songs. Run each prompt once or twice.
4. Download as **WAV** if the plan allows it, otherwise MP3. Do not trim anything: the full song is needed.
5. Name the files `suno_main_A1.wav`, `suno_main_B2.wav`, `suno_room_1.wav` and so on.

Suno songs run one to three minutes; the film needs 16 s. The useful part is: a few quiet seconds, a clear drop,
about 9 s of full music after it, and a single final hit. The rest is cut away.

Keep **120 BPM** in every main prompt. The picture is cut on a 120 BPM grid (one beat every 12 frames, first beat
on the raindrop burst at 4.25 s). A track that comes back within about 4 % of 120 is stretched to fit; further off,
the picture is re-cut to it.

Do not put the game's name, a song title or an artist's name in a prompt.

## Main track (pick one direction, or try all three)

### A — Miami synthwave (closest to the current track)
Style:
```
1980s Miami synthwave, instrumental, 120 BPM, D minor, neon night drive in the rain, punchy gated-reverb drums, driving analog bass arpeggio, bright brass synth lead hook, wide warm pads, cinematic, energetic, hard ending
```

### B — 80s driving pop-rock
Style:
```
1980s driving pop-rock instrumental, 120 BPM, D major, open-road energy, chiming electric guitars, steady four-on-the-floor kick, big gated snare, warm analog synth pads, uplifting guitar lead hook, cinematic, hard ending
```

### C — 80s electro-funk
Style:
```
1980s electro-funk boogie instrumental, 120 BPM, D minor, slap bass groove, tight drum machine with claps, funky synth stabs, glossy lead synth hook, neon city at night, confident and playful, hard ending
```

Structure (same for A, B and C):
```
[Intro: quiet filtered pad only, no drums, 4 bars]
[Build: rising filter sweep and snare roll, 2 bars]
[Drop: full drums, full bass, lead hook enters]
[Main theme: full energy, same hook, 8 bars]
[Break: one bar of silence]
[Final hit: one big chord, long reverb tail]
[End]
```

## Room bed (optional: the bored room at the start and in the last room shot)
The current cut has no music in the room, only a wall clock and a ceiling fan. If the room should have music too:

Style:
```
sleepy lo-fi waiting-room muzak, instrumental, 60 BPM, D major, dull soft electric piano, lazy brushed drums, muffled as if from a small TV speaker, boring, slow, quiet, loopable
```
Structure:
```
[Intro: soft electric piano loop]
[Loop: same idea, nothing changes]
[End]
```

## Where the music sits in the film
| Film time | Picture | Music |
|---|---|---|
| 0.00 – 2.58 s | Bored face, glance at the helmet, visor | None today (clock, fan, engine idle). Room bed here if wanted |
| 2.58 – 3.75 s | Bike passes the tea stall in the rain | Main track's quiet intro, filtered, opening up |
| 3.75 – 4.25 s | Raindrop hangs | Silence |
| 4.25 s | Raindrop bursts | **The drop**: beat one |
| 4.25 – 12.75 s | Bike, puddle, city builds, aerial, chase | Full track, 17 beats |
| 12.75 – 14.25 s | Back in the room, 4 % | Music stops dead (room bed here if wanted) |
| 14.25 – 16.00 s | End card | The track's final hit and tail |

## Handing the files over
Upload them in the chat, or put them in a Google Drive folder and send the link. After that: tempo and drop
position are measured for each file, each one is laid to picture as a phone copy for listening, and the chosen
one becomes the next film version.

## Rights
Use a paid Suno plan for these generations and keep a note of the plan and date in `00_BRIEF/Rights_Sheet.csv`:
Suno's terms tie commercial use to songs made while subscribed. Confirm on the plan page before publishing.
