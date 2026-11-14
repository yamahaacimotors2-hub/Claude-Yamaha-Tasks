# S06 product test — runbook (Plan A, approved: 1 take, 720p, 4 s, 28 credits)

**Status: not run.** The cloud session that prepared this could price Higgsfield jobs but its
generate and upload tools were not loaded, so the test has to be started from the Claude app chat
(with the Higgsfield connector) or from the Higgsfield website.

## Files in this folder
- `MT15_V2_Cyan_Storm.png` — official product photo. The only product reference.
- `S06_layout_guide.png` — our CG frame. Use it ONLY to show camera angle and composition.
  Do not use it as a video start frame: the bike in it is a box proxy.

## Step 1 — keyframe (GPT Image 2.6, about 0.25 credit)
Attach both files and ask:

> Using GPT Image 2.6, make one 9:16 photoreal keyframe. Take the motorcycle from the official
> product photo exactly: Yamaha MT-15 V2 Cyan Storm, graphite panels, cyan factory rims and
> graphics, gold forks, real headlight face, front brake disc and ABS ring, exhaust, proportions.
> Take only the camera angle and composition from the layout image (low front three-quarter from
> the bike's right, bike riding toward camera, water on the far side). Adult rider in full
> protective gear, full-face helmet, visor down. Light rain at dusk on a wet city road, cool
> blue-grey light with a soft fill on the bike, amber and magenta water spray behind the rear
> wheel. Do not copy the low-poly look of the layout image. No added logos, text or parts.
> Show me the price first.

**Check the keyframe before spending on video.** Put it beside the official photo: headlight, tank
graphics, gold fork, cyan rim, ABS ring, exhaust, seat. If one is wrong, regenerate the keyframe
(0.25 credit) instead of going to video.

## Step 2 — video (Seedance 2.5, 720p, 4 s, 9:16, audio off = 28 credits)
With the approved keyframe as the start frame and the official photo still attached as reference:

> Using Seedance 2.5, 4 seconds, 9:16, 720p, audio off, start from this keyframe. The bike rides
> steadily toward camera at normal speed; the camera tracks backward with it, low. Rain falls,
> spray trails behind the rear wheel. Keep the motorcycle exactly as in the official product photo
> for the whole clip. Bike stable and in contact with the road, no wheelie, no added logos or
> text. Show me the price first, and do not start if it is above 28 credits.

Write the job ID in `00_BRIEF/Shot_Tracker.csv`.

## Step 3 — judge it (Gate 3)
Compare the first, middle and last frame with the official photo, same seven details.
- All three match: pass. Go on to S01+S02 and S11.
- Something drifts: change ONE thing (tighter angle, smaller camera move, or shorter clip) and
  re-quote before running again.

Send the clip back to the Claude Code session and it can do the frame-by-frame comparison.
