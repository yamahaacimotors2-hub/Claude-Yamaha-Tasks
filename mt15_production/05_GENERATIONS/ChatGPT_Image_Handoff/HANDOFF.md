# Master handoff for ChatGPT — Higgsfield image generation
## Yamaha MT-15 V2 Cyan Storm, 16-second film

You are working with Niloy on a Yamaha Bangladesh / ACI Motors short film. Your job in this handoff is **still images only**, generated through the **Higgsfield connector** with **GPT Image 2.6**. Read this whole file and look at every file in `refs/` before generating anything.

**Reply to Niloy in short, simple Banglish** (Bangla in Latin letters), with English technical terms. Lead with what happened, then what you need from him.

---

## 1. Rules that override everything else

1. **Images only.** Do not start any video generation. One video is approved (section 8), and only Niloy can trigger it by saying so in this chat.
2. **Quote before every generation.** Show the credit price and wait for nothing more if it is within budget; stop and ask if it is not.
3. **Budget cap: 10 credits total for this handoff.** The live price was 0.25 credit per GPT Image 2.6 image (checked on 14 Nov 2026). If a quote is higher than 0.5 credit per image, stop and tell Niloy.
4. **Do the product gate first (K06).** If K06 fails after 4 attempts, stop and report. Do not go on to the other bike images.
5. **Never invent the motorcycle.** Every image that shows the bike must have `refs/MT15_V2_Cyan_Storm_OFFICIAL.png` attached, and must be checked against `refs/PRODUCT_QC_crops.jpg`.
6. **No text in any image.** No titles, captions, numbers, watermarks, signboards with readable words. TV screens stay blank. All text is added later in post.
7. **No game material.** No game titles, logos, characters, HUD, minimap, artwork or typefaces from any game. The film is inspired by open-world games only in mood.
8. **Safety and brand.** Whenever the rider is on the bike: full-face helmet with visor down, jacket, gloves, trousers, boots; normal road speed; both wheels on the road; no stunts. No invented Yamaha logos, badges, parts or colours beyond what the official photo shows.
9. **Do not use the layout images as style.** The `layout_*.jpg` files are low-poly CG frames from our previs. Take **only camera angle and composition** from them. The bike in them is a box proxy and must never be copied.
10. If the connector cannot attach reference images, stop and tell Niloy. Do not generate bike images from text alone.

---

## 2. The film in five lines

A young man in Dhaka is stuck watching a game download at 3%. He notices his helmet, puts it on, and rides his MT-15 out into the rain. The headlight beam enters a hanging raindrop and it bursts into amber and magenta. Wherever the beam touches the roadside, the kerb and railing assemble and the street opens into a palm-lined waterfront at dusk. Hard cut: same room, helmet still on, download at 4%. End line: "Map লোড হয় চাকার নিচে।"

**Two looks**
- **Look A, real rainy Dhaka:** cool blue-grey rain light, wet asphalt, small pools of muted amber from a tea stall. Used in K04, K05, K06, K07.
- **Look B, the loaded world:** coral-to-violet dusk sky, cyan and magenta neon, warm windows, pastel Art Deco fronts, palms, wet reflective road. Used in K10, K12.
- **Room:** dark bedroom, one warm lamp, cool glow from the TV. Used in A4, K01, K02, K03, K11.

**Locked geography:** the road bends right. **Water is on the left** of the direction of travel, with a kerb and a low railing. **The tea stall and buildings are on the right.** The bike keeps to the left lane (Bangladesh drives on the left). See `refs/map_top_down.png`.

---

## 3. Reference files

| File | Use |
|---|---|
| `refs/MT15_V2_Cyan_Storm_OFFICIAL.png` | The only product reference. Attach to every image that shows the bike |
| `refs/PRODUCT_QC_crops.jpg` | Seven details to check on every bike image |
| `refs/layout_S01.jpg` … `layout_S11.jpg` | Camera angle and composition only, one per shot |
| `refs/layout_S12_background.jpg` | Composition for the end-card background plate |
| `refs/map_top_down.png` | Which side is water, which side is town |

The official photo shows the bike from the **front-right three-quarter**. Images that show the bike from that side (K04, K06) are the safe ones. There is **no official photo of the rear**, so K10 is blocked until Niloy supplies one.

---

## 4. Order of work

| Step | ID | What | Attempts allowed |
|---|---|---|---|
| 1 | **K06** | Product gate: bike keyframe for shot S06 | 4 |
| 2 | **A1** | Character sheet | 3 |
| 3 | **A4** | Empty room master | 3 |
| 4 | A2, A3, A5 | Expressions, wardrobe, helmet prop | 2 each |
| 5 | K01, K02, K03, K11 | Room keyframes | 2 each |
| 6 | K04, K05, K07 | Rain keyframes | 2 each |
| 7 | K12 | End-card background plate (optional) | 2 |
| blocked | K10 | Rear chase: needs an official rear photo | 0 |

All images: **9:16 portrait**, highest resolution the model offers, photoreal, cinematic, no text.

---

## 5. Prompts

### K06 — product gate (shot S06)
Attach: `MT15_V2_Cyan_Storm_OFFICIAL.png`, `layout_S06.jpg`

> Photoreal cinematic still, 9:16. The motorcycle is the exact Yamaha MT-15 V2 Cyan Storm from the attached official product photo: graphite grey bodywork, cyan factory graphics on the tank shrouds, cyan cast wheels, gold upside-down front fork, the same headlight face with the small central projector and two position lights, the same front brake disc with ABS sensor ring, the same exhaust, seat and proportions. Do not redesign, simplify or add anything to the motorcycle.
> Take only the camera position and composition from the second attached image, a rough layout: low camera, front three-quarter view from the motorcycle's right side, the bike riding toward the camera in the left lane, dark water and a far shoreline beyond it. Ignore the layout's low-poly style and its box-shaped bike.
> An adult rider in full protective gear: black full-face helmet with the visor down, dark riding jacket, gloves, riding trousers and boots. Normal riding speed, both wheels on the road.
> Rainy evening in Dhaka, cool blue-grey light, wet asphalt with reflections, soft fill light on the bike so its colours read clearly, headlight on. A fine spray of water behind the rear wheel catches amber and magenta light. Shallow depth of field, the bike sharp. No text, no logos added, no watermark.

**Pass only if all seven details in `PRODUCT_QC_crops.jpg` match.** Report each one as match / wrong.

### A1 — character sheet (explicit request: please make a character sheet)
Attach: nothing

> Character reference sheet, photoreal, neutral grey studio background, even soft light, 9:16. One young Bangladeshi man, about 24, short black hair, light stubble, slim build, an ordinary friendly face, original and not resembling any real person. Four views of the same man on one sheet: front, three-quarter, profile, and full length standing. He wears a plain muted olive T-shirt and dark jeans. Neutral expression. Same face, hairline, skin tone and proportions in every view. No text, no labels.

### A2 — three expressions
Attach: the approved A1

> The same man as in the attached character sheet, same face, hairline and skin tone. Three head-and-shoulders portraits side by side on one image, neutral grey background, soft light: (1) bored and slumped, eyes half closed; (2) an idea dawning, eyes lifted, eyebrows up; (3) quietly amused, small smile. Plain muted olive T-shirt. Photoreal. No text.

### A3 — two wardrobe states
Attach: the approved A1

> The same man as in the attached character sheet, full length, two versions side by side on a neutral grey background, photoreal. Left: at home, plain muted olive T-shirt, dark jeans, barefoot. Right: ready to ride, the same olive T-shirt collar visible under an understated dark riding jacket with protective shoulders, riding gloves, protective trousers, boots, holding a matte black full-face helmet under one arm. No logos, no text.

### A4 — empty room master
Attach: `layout_S01.jpg`

> Photoreal cinematic still, 9:16, no people. A small, lived-in bedroom in a Dhaka apartment at night. A flat TV mounted on the wall in the upper middle of the frame, its screen switched on but completely blank, an even deep blue glow with no image and no text, viewed almost straight on so the screen is a clean rectangle. Under the TV a low dark console; on the right end of the console sits a matte black full-face motorcycle helmet. A warm floor lamp at the left edge. In the foreground at the bottom of the frame, the back of a dark fabric sofa. Dark blue-grey walls, a window with night light on the left wall. Camera position and framing as in the attached layout; ignore its low-poly style. Light only from the TV, the lamp and the window. No text anywhere.

### A5 — helmet prop
Attach: nothing

> Product-style photoreal still, 9:16, dark background. A matte black full-face motorcycle helmet with a clear-to-smoke visor, three-quarter front view, no brand logos, no graphics. Soft blue light from the left, warm rim light from the right. No text.

### K01 — shot S01, bored at 3%
Attach: approved A4, approved A1, `layout_S01.jpg`

> Photoreal cinematic still, 9:16. The same room as the attached room image, same camera, same TV, console, helmet and lamp. The same man as in the attached character sheet sits on the sofa in the foreground, seen from behind and slightly to the side so the edge of his face is visible, slumped, a game controller hanging loose in his right hand. He wears the plain muted olive T-shirt. The TV screen stays completely blank, an even deep blue glow, no image, no text. His head sits below the TV so it does not cover the screen. Light from the TV on his hair and shoulder. No text.

### K02 — shot S02, the helmet
Attach: approved A4, approved A5, `layout_S02.jpg`

> Photoreal cinematic close-up, 9:16. The matte black full-face helmet from the attached helmet image sitting on the dark TV console in the room from the attached room image. The blank blue TV glow reflects softly in the visor; a warm edge of lamp light on the shell. Shallow depth of field, the helmet sharp, the room dark and soft behind it. Composition as in the attached layout; ignore its style. No text, no logos.

### K03 — shot S03, visor up before the snap
Attach: approved A1, approved A5, `layout_S03.jpg`

> Photoreal cinematic close-up, 9:16, three-quarter front. The same man as in the attached character sheet wearing the matte black full-face helmet from the attached helmet image, visor fully raised so his eyes are visible, a gloved hand fastening the chin strap. Dark riding jacket collar. Dark room behind him with the blank blue TV glow out of focus and a warm edge light. Exactly five fingers on the hand, one strap, one buckle. No text, no logos.

### K11 — shot S11, back at 4%
Attach: approved A4, approved A1, `layout_S11.jpg`

> Photoreal cinematic still, 9:16. The same room and the same camera as the attached room image. The same man as in the attached character sheet is back on the sofa, seen from behind and slightly to the side, still wearing his matte black full-face helmet with the visor raised and a dark riding jacket, both wet with rain, small drops on the helmet catching the TV light. His head is tilted in amusement. The console under the TV is now empty where the helmet used to sit. The TV screen stays completely blank, an even deep blue glow, no image, no text. No text anywhere.

### K04 — shot S04, rainy Dhaka from the tea stall
Attach: `MT15_V2_Cyan_Storm_OFFICIAL.png`, `layout_S04.jpg`

> Photoreal cinematic still, 9:16. View from under the tin roof of a small roadside tea stall in Dhaka on a rainy evening: in the foreground a worn wooden counter with small glasses of tea and an aluminium kettle, a bare bulb hanging from the roof. Beyond the counter, a wet two-lane road. On it, riding left to right at normal speed, a rider in full gear on the exact Yamaha MT-15 V2 Cyan Storm from the attached official product photo, seen from its right side: graphite bodywork, cyan graphics and cyan wheels, gold front fork, headlight on. Rider: black full-face helmet with visor down, dark jacket, gloves, trousers, boots. Beyond the road an unfinished roadside with no kerb and no railing, dark water and a dim far shore. Cool blue-grey rain light with small warm pools from the stall. Composition as in the attached layout; ignore its low-poly style and its box-shaped bike. No readable text on anything.

### K05 — shot S05, the hanging raindrop
Attach: `layout_S05.jpg`

> Photoreal macro still, 9:16. A single large raindrop hangs from the tip of a dark green leaf at the upper left, perfectly clear, the rainy street refracted upside down inside it. Several smaller drops hang motionless in the air around it, as if time has stopped. Far behind, completely out of focus, a wet road with a row of cool streetlights and one warm amber light. Cool blue-grey palette. Very shallow depth of field. No text.

### K07 — shot S07, the puddle
Attach: `layout_S07.jpg`

> Photoreal macro still, 9:16, low angle. A dark puddle on wet asphalt just after one drop has hit it: a small crown at the centre and concentric ripples spreading out, their crests catching amber and magenta highlights. Out-of-focus amber, magenta, white and cyan lights reflected along the top of the frame. A white glow beginning to enter from the top right. No text.

### K12 — end-card background plate (optional)
Attach: `layout_S12_background.jpg`

> Photoreal cinematic still, 9:16, no vehicles and no people. A wet boulevard at coral-to-violet dusk, seen from a low camera in the middle of the road looking along it as it curves gently to the right. On the left: a pale stone kerb, a low railing with small warm lamps, palms, and calm dark water beyond. On the right: pastel Art Deco building fronts with cyan and magenta neon bands, warm lit windows, palms and street lamps. Strong reflections on the wet road. The lower-middle third of the frame is open road, kept clear for a motorcycle to be placed there later. Composition as in the attached layout; ignore its low-poly style. No text, no signage.

### K10 — rear chase (BLOCKED)
Do not generate. There is no official photo of the bike's rear. Tell Niloy this is waiting on a rear photo from ACI.

---

## 6. How to judge an image

**Any image with the bike:** open `PRODUCT_QC_crops.jpg` next to it and check:
1. headlight face  2. tank graphics  3. gold fork  4. front wheel, disc and ABS ring  5. exhaust  6. seat and tail  7. rear wheel and cyan rim

One wrong detail is a fail. Also fail it for: extra or missing parts, invented logos or text, rider without full gear, wheel off the ground, water on the wrong side.

**People:** same face as A1; five fingers; no warped helmet or straps.

**Rooms:** TV screen blank and a clean rectangle (four clear corners, for tracking later); same room across K01, K02, K11.

**When a retry is needed, change one thing only** and say what you changed.

---

## 7. What to hand back

For each ID, the best image, saved with this name: `K06_S06_keyframe_v001.png`, `A1_character_sheet_v001.png`, and so on, raising the version on each retry.

Then one table:

| ID | Version kept | Attempts | Credits | Job ID | Pass / fail | What is still wrong |
|---|---|---|---|---|---|---|

And two lines: total credits spent, and anything blocked.

Niloy will put the files in `mt15_production/05_GENERATIONS/` in the project repo.

---

## 8. The one approved video (do not run unless Niloy says "run the S06 video")

Shot S06 product test: **Seedance 2.5, 4 seconds, 9:16, 720p, audio off, at most 28 credits.** Start frame: the approved K06. Keep `MT15_V2_Cyan_Storm_OFFICIAL.png` attached as reference.

> The bike rides steadily toward camera at normal speed; the camera tracks backward with it, low. Rain falls, spray trails behind the rear wheel. Keep the motorcycle exactly as in the official product photo for the whole clip. Bike stable and in contact with the road, no wheelie, no added logos or text.

Quote first. If the quote is above 28 credits, do not start.
