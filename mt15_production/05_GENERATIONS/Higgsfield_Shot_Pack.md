# Higgsfield shot pack — credit খরচের আগে পড়ার জন্য

এই film-এর v1 পুরোটা Blender CG দিয়ে বানানো আছে। নিচের ৮টা shot Higgsfield দিয়ে বদলালে কী লাভ, কী ঝুঁকি, আর কী দিয়ে generate করতে হবে, সেটা এখানে। **কোনো generation চালানো হয়নি।** প্রতিটার আগে live quote নাও।

## কোনটায় লাভ সবচেয়ে বেশি

| অগ্রাধিকার | Shot | v1-এ এখন যা আছে | Higgsfield-এ লাভ | ঝুঁকি |
|---|---|---|---|---|
| ১ | **S06** bike low front ৩/৪ | Box-এর মতো proxy bike, silhouette | আসল Cyan Storm দেখা যাবে। পুরো film-এ bike স্পষ্ট দেখার একমাত্র চলন্ত shot | Decal, ABS ring, headlight বদলে যেতে পারে। **এটাই product test** |
| ২ | **S01+S02** ঘর, TV, helmet | পেছন থেকে silhouette, মুখ নেই | মানুষের মুখ আর অভিনয়: বিরক্তি → helmet-এ চোখ → হাসি | মুখ S11-এর সাথে মিলতে হবে |
| ৩ | **S11** ঘর, ৪% | Helmet পরা silhouette | একই মানুষ, ভেজা jacket, হাসি | S01-এর একই still থেকে না বানালে ঘর মিলবে না |
| ৪ | **S04** বৃষ্টিভেজা ঢাকা | Low-poly রাস্তা আর দোকান | আসল ঢাকার texture, বৃষ্টি, মানুষ | Bike দূরে, তাই product ঝুঁকি মাঝারি |
| ৫ | **S10** rear chase | Proxy bike পেছন থেকে | আসল bike আর rider | **পেছনের official ছবি নেই।** আগে ACI থেকে ছবি নাও, না হলে এটা CG-ই থাকুক |
| ৬ | **S03** visor/buckle | CG helmet | হাত, strap, আসল helmet | হাতের আঙুল |
| ৭ | **S05** raindrop burst | CG ফোঁটা আর রঙের ধারা | আসল পানির মতো তরল | কম |
| ৮ | **S07** puddle ripple | CG ripple | সামান্য | কম। CG-ই রাখা যায় |

**S08 (hero build), S09 (aerial), S12 (end card) Higgsfield-এ যাবে না।** ওগুলো CG আর official ছবিতেই নির্ভুল।

## সবচেয়ে কম খরচের পথ
শুধু **S06 এক take** চালাও। পাস করলে S01+S02 আর S11। বাকিগুলো v1 দেখে ঠিক করো।

## সব shot-এর common settings
9:16 · audio off · test-এ 720p, final-এ 1080p · ৪ সেকেন্ডের take (film-এ trim হবে) · প্রতিটার job ID `00_BRIEF/Shot_Tracker.csv`-তে।

**v1-এর CG still সরাসরি video-র start frame হিসেবে দিও না।** ওগুলো low-poly, আর bike টা box proxy; video সেটাই চালিয়ে দেবে। দুই ধাপে করো: (১) GPT Image 2.6 দিয়ে photoreal keyframe বানাও, CG still শুধু camera angle আর composition দেখানোর জন্য (প্রতি image ০.২৫ credit), (২) সেই keyframe থেকে Seedance 2.5 দিয়ে video। Keyframe-এই product ভুল ধরা পড়লে video-র credit বাঁচে। উদাহরণ: `S06_product_test/RUNBOOK.md`।

## Live দাম (connector থেকে নেওয়া, 9:16)
| জিনিস | দাম |
|---|---|
| Seedance 2.5, 720p | সেকেন্ডে ৭ credit (৪s = ২৮, ৫s = ৩৫) |
| Seedance 2.5, 1080p | সেকেন্ডে ১৬ credit (৪s = ৬৪, ৫s = ৮০) |
| GPT Image 2.6 | প্রতি image ০.২৫ credit |

সব shot ৩ সেকেন্ডের নিচে, তাই ৪ সেকেন্ডের take যথেষ্ট। ৮ shot × ২ test take (720p) + ৮ final (1080p) + ২৪ image = ৯৬৬ credit।

## Prompt

**S06 (product test)** — reference: `01_REFERENCES/MT15_V2_Cyan_Storm.png` + `08_REVIEW/stills/S06.png`
> Shot S06, 5 s, 9:16. Exact Yamaha MT-15 V2 Cyan Storm from the attached official product reference. Preserve graphite panels, cyan factory rims and graphics, gold forks, real headlight, correct front brake and ABS ring, exhaust and proportions. Adult rider in full protective gear, full-face helmet with visor down. The bike rides steadily toward camera in light rain at dusk on a wet city road beside dark water. Low front three-quarter tracking shot from the bike's right, camera travelling with the bike. Cool blue-grey rain light with a soft fill on the bike; amber and magenta water spray trails behind the rear wheel. Bike unobstructed, stable, in contact with the road. No wheelie, speeding, added logos, text or parts.

**S01+S02** — reference: one approved room still (generate the still first) + `08_REVIEW/stills/S01.png`
> Shot S01-S02, 5 s, 9:16. Dim bedroom in Dhaka at night, one warm lamp, a wall-mounted TV with a blank dark screen. A young Bangladeshi man in a plain muted olive T-shirt sits slouched on a sofa, bored, game controller hanging loose in one hand. He glances to a full-face motorcycle helmet on the console under the TV, his head lifts, a slight smile. Locked-off over-the-shoulder camera with a very slow push-in. Keep the TV screen blank and flat for a later screen replacement.

**S11** — reference: the SAME room still as S01
> Shot S11, 5 s, 9:16. Same room, same camera, same man, now in a wet riding jacket with the helmet still on, visor up, sitting back on the sofa. He looks at the TV and shakes his head with an amused smile. Keep the TV screen blank and flat for a later screen replacement.

**S03**
> Shot S03, 5 s, 9:16. Extreme close-up, three-quarter front. A gloved hand fastens the chin strap of a matte black full-face helmet with one clean click, then the visor snaps down. Dark room, blue TV glow from behind, warm edge light. One buckle action only. No extra straps, no text, no logos.

**S04** — reference: `08_REVIEW/stills/S04.png`
> Shot S04, 5 s, 9:16. Rainy evening in Dhaka seen from under the tin roof of a small roadside tea stall: glasses of tea and a kettle on the counter in the foreground, a hanging bulb. A rider in full gear on the exact Yamaha MT-15 V2 Cyan Storm from the attached reference passes left to right on the wet road. Beyond the road, an unfinished waterfront and dark water. Cool blue-grey rain, small warm pools of light. Normal riding speed. No added logos or text.

**S05**
> Shot S05, 5 s, 9:16. Macro. A single raindrop hangs from the tip of a leaf, other drops suspended motionless in the air, a rainy road out of focus behind. A white headlight beam sweeps in from behind and enters the drop; the drop bursts sideways to the right into ribbons of amber and magenta liquid. Shallow depth of field. No text.

**S07**
> Shot S07, 5 s, 9:16. Macro, low angle. One coloured drop falls into a dark puddle on wet asphalt; concentric ripples spread, catching amber and magenta reflections. A white light begins to sweep across the top of the frame. No text.

**S10** — only if ACI supplies an official rear photo
> Shot S10, 5 s, 9:16. Rear chase, camera low behind the exact Yamaha MT-15 V2 Cyan Storm from the attached official references, rider in full gear with full-face helmet. Wet boulevard at coral-violet dusk: water and a lamp-lit railing on the left, pastel Art Deco fronts with cyan and magenta neon and palms on the right. Normal riding speed, bike stable and in contact with the road. No added logos or text.

## প্রতিটা take-এ যা দেখবে
প্রথম, মাঝের আর শেষ frame official crop-এর পাশে রাখো: headlight, tank graphics, gold fork, cyan rim, ABS ring, exhaust, seat। একটা ভুল থাকলে take বাতিল। আবার চালালে একটাই জিনিস বদলাও।
