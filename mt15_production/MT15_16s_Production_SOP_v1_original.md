# Yamaha MT-15 V2 Cyan Storm
## ১৬ সেকেন্ডের AI + CG film production SOP

**১০টি production phase · ১০০টি numbered action · ৬টি review gate**

**Start here:** ০১–১০ করে brief ও folders তৈরি করো। ১১–২০ করে animatic lock করো। এরপর asset lock এবং ৫ সেকেন্ডের CG proof। **সম্পূর্ণ film render করার আগে proof pass করাও।** প্রতিটি step-এর শেষে যে file বা evidence চাওয়া হয়েছে, সেটি থাকলেই step complete চিহ্ন দাও। সমস্যা হলে নিচের **Blocker card** কপি করো। একই step থেকে resume করো।

**Project:** ১৬.০০ সেকেন্ড, 9:16, AI/CG only। Revised ১৬-frame storyboard governing reference। আগের ১৮s animatic pre-hybrid reference। ১৫ ও ১৬ একই end-card shot-এর দুই state। Latest board: `exec-3f8723b6-ebb6-4f6e-8c46-8024f1009060.png`। Official product reference: `MT15_V2_Cyan_Storm.png`।

**Story:** ঢাকার এক তরুণ GTA VI download ৩%-এ আটকে দেখে বিরক্ত। Helmet চোখে পড়তেই তার মাথায় একটা idea আসে। Buckle click-এর পর Cyan Storm-এ সে বৃষ্টিভেজা ঢাকায় বের হয়। Raindrop রঙে ফাটে, puddle-এ স্বপ্নের boulevard দেখা যায়। Headlight curb ছুঁতেই পাথর ও railing বসে, শহর খুলে যায় palm-lined waterfront-এ। TV preview-এর বাঁকে তাকে ride করতে দেখি। Hard cut করে একই ঘরে ফিরি। Download ৪%। End line **“Map লোড হয় চাকার নিচে।”**

**Status:** Storyboard আছে। New animatic, hero proof, footage এবং final master এই SOP-এর পরের কাজ। Public version-এ plain-text game title clearance pending। TV text editable রাখো। Earlier storyboard generation approval দিয়ে নতুন paid run বা retry submit করার অনুমতি হয় না।

---

## ১. Brief, scope ও project setup

**০১.** `00_BRIEF/Brief_v001.md`-এ লিখো: এই ১৬ সেকেন্ডে audience আগে GTA VI reference চিনবে, তারপর বুঝবে Yamaha চলতেই নিজের ঢাকা বদলেছে। Opening, hero build ও ৪% callback-কে তিনটি must-read beat হিসেবে tick দাও।

**০২.** Written scope-এ ১টি vertical master, ৫s proof, CG/VFX, edit, grade, sound এবং QC রাখো। ৳২ লাখ প্রস্তাবিত fee হিসেবে লিখো। Proof ও final-cut feedback-এর round সংখ্যা, extra revisions, source project handover, timeline এবং payment terms আলোচনার জায়গা আলাদা করে চিহ্নিত করো।

**০৩.** Rights sheet বানাও। প্রতি asset-এর filename, source, intended use, owner/license এবং clearance status লিখো। GTA VI plain text approval copy-তে থাকবে। Public title clearance-এর owner ও status লিখে রাখো। Official logo, game footage, original game UI এবং reference ad footage export-এ ঢুকবে না।

**০৪.** এই folder tree বানাও। Original files read-only copy হিসেবে রাখো।

```text
00_BRIEF/  01_REFERENCES/  02_ASSET_BIBLE/  03_ANIMATIC/
04_CG/  05_GENERATIONS/  06_COMP/  07_EDIT_SOUND/
08_REVIEW/  09_DELIVERY/
```

**০৫.** Naming lock করো। `S07_bikeRain_take02`, `S10_curbComp_v003`, `MT15_master_v005`। একই নামে পুরোনো file overwrite করার বদলে version বাড়াও। Status লিখো `planned / WIP / review / approved / superseded`।

**০৬.** Tracker-এ এক row প্রতি shot। Columns: shot ID, timecode, exact input refs, owner, status, take/version, quote, job ID, issue, approval। একা করলে owner column-এ director, CG, comp, editor ও QC hat লিখে কাজ বদলানোর সময় কোন দায়িত্বে আছ বোঝো।

**০৭.** Tool দায়িত্ব ঠিক করো। Image generation দিয়ে keyframe, Seedance দিয়ে selected motion plates, Blender দিয়ে deterministic city build, After Effects দিয়ে roto/comp, Premiere দিয়ে edit/sound, FFmpeg দিয়ে file check। Codex বা Claude Code দিয়ে versioned scripts, shot logs ও troubleshooting; একটিই authoritative project tree।

**০৮.** Actual workstation check। Blender খুলে default cube still render করে file reopen করো। AE/Premiere-এ একটি clip import ও ১s test export করো। Agent/cloud session-এ executable ও writable output path পরীক্ষা করো। কোন app/bridge কোথায় verified, tracker-এ লেখো।

**০৯.** Safe baseline হিসেবে 1080×1920, 24 fps, SDR output, 48 kHz audio প্রস্তাব রাখো। ১৬s = ৩৮৪ frames। Source frame rates, interpretation ও colour tags লিখে রাখো। Timeline fps animatic-এর আগেই lock করো।

**১০.** Budget log-এ CG/comp time, AI credits, audio, review/finishing এবং contingency লিখো। প্রতিটি paid request-এর আগে model/settings, output count, quote ও approval লিখো। Paid batch ছড়িয়ে দেওয়ার আগে representative take পাস করাও।

**Gate ১ — Brief lock।** Latest board, scope, rights tracker, fps এবং actual tool test evidence আছে। Title clearance pending থাকলে work copy চালাও এবং publish gate-এ status ধরে রাখো।

## ২. Storyboard থেকে exact cut

**১১.** ১৬ panel আলাদা still হিসেবে বের করো। Panel numbering ধরে রাখো। ১৫–১৬-কে একই end-card plate-এর start ও hold ধরো। `03_ANIMATIC/Frame_Index.csv`-এ panel ও shot ID map করো।

**১২.** ১৬.০০s timeline বানিয়ে এই frame budget বসাও। Ranges start-inclusive, end-exclusive। এগুলো working allocations। Animatic review-তেই fine timing lock হবে।

| Keyframe | 24 fps range | কী পড়বে |
|---|---:|---|
| ০১ | 000–028 | মুখে বিরক্তি, controller ঢিলে, TV ৩% |
| ০২ | 028–046 | Helmet-এর দিকে চোখ, মাথা ওঠে, idea |
| ০৩ | 046–060 | Buckle click |
| ০৪ | 060–094 | Rainy Dhaka, same tea stall ও rail |
| ০৫ | 094–106 | ঝুলে থাকা drop |
| ০৬ | 106–119 | Amber-magenta liquid burst |
| ০৭ | 119–139 | Low front 3/4, স্পষ্ট Cyan Storm |
| ০৮ | 139–155 | High side view, বৃষ্টি ফেরে |
| ০৯ | 155–168 | Puddle ripple-এ স্বপ্নের waterfront |
| ১০ | 168–194 | Headlight hits slot, curb stone seats |
| ১১ | 194–222 | Railing post seats, light ও reflection আসে |
| ১২ | 222–258 | Aerial-এ একই বাঁকের তিন অবস্থা |
| ১৩ | 258–288 | একটাই rear chase payoff |
| ১৪ | 288–332 | Hard cut, same room, download ৪% |
| ১৫–১৬ | 332–384 | একটাই product hold, copy ও logo |

**১৩.** ০১-এ phone-size-এ একই সঙ্গে মুখ এবং TV text পড়ছে কি না পরীক্ষা করো। Frame ২-এর eye-line-এ helmet রাখো। দরকার হলে অল্প contrast বাড়াও বা crop বদলাও। Acting cue: slouch → head lift → eyes settle → slight smile।

**১৪.** Opening TV-তে boulevard preview-এর right bend, বাঁয়ে পানি, ডানে stall composition lock করো। Preview-এর read দুর্বল হলে একই TV insert-এর ভেতরে preview বড় করো। অপ্রয়োজনীয় নতুন shot যোগ করার আগে crop test করো।

**১৫.** ০৩–০৪-এ buckle click-এর সঙ্গে hard cut বসাও। বাইরে প্রথম frame-এ full gear, Cyan Storm ও চায়ের দোকান একবার দেখা চাই। Room-to-street-এর জন্য আলাদা door montage দরকার হলে প্রথমে duration trade-off পরীক্ষা করো।

**১৬.** ০৫–০৯-এ পাঁচটি rain beat রেখে phone-এ loop করো। ০৬-এর fluid direction এবং ০৭-এর splash direction মিলাও। ০৭–০৮-এ silhouette-এর জায়গায় স্পষ্ট bike রাখো। মাথা, wheels ও bodywork-এর ওপর splash ঢেকে দিলে mask/placement বদলাও।

**১৭.** ০৯ → ১০-এ ripple-এর brightest arc ও headlight-এর contact patch একই screen region-এ align করো। Puddle glimpse দর্শককে preview মনে করাবে। Physical assembly শুরু হবে beam curb ছোঁয়ার পরে।

**১৮.** ১০–১২-এ আলাদা scale ব্যবহার করো। Curb close → railing medium → aerial wide। ১৩ হবে একটাই chase payoff। একই front-3/4 tracking বারবার ফিরলে adjacent shot trim বা merge করো।

**১৯.** ১৩ → ১৪-তে hard cut দাও। Engine/rain হঠাৎ কেটে room tone। ১৪-এর জন্য একই room plate বা একই camera/layout reference। ৪% পড়তে দাও, তারপর ১৫–১৬-এ single hold।

**২০.** Temp sound ও numbered burn-in দিয়ে `MT15_animatic_v001.mp4` export করো। তিনজন fresh viewer-কে sound off-এ একবার দেখাও। জিজ্ঞেস করো কী download হচ্ছিল, ছেলেটা কেন বের হলো, শহর বদলালো কীভাবে। উত্তর লিখে রাখো।

**Gate ২ — Animatic lock।** ১৬s ঠিক, প্রথম ১s-এ title পড়া যায়, idea বোঝা যায়, hero build-এর আগে-পরে clear, ৪% callback পড়া যায়।

## ৩. Character, product ও environment asset bible

**২১.** `02_ASSET_BIBLE/Character`-এ একজন adult Bangladeshi protagonist-এর neutral front, 3/4, profile ও full-length reference lock করো। Original synthetic face বা consented reference ব্যবহার করো। একটাই face ID।

**২২.** একই face-এর তিন expression still বানাও: bored, idea dawns, amused at ৪%। Hairline, চোখ, skin tone ও face shape compare করো। Opening/closing মুখের continuity মুখের pose-এর চেয়ে অগ্রাধিকার পাবে।

**২৩.** দুই wardrobe state লিখে still lock করো। ঘরে muted olive plain T-shirt ও dark jeans। Ride-এ একই collar cue, understated protective jacket, gloves, full-face helmet visor down, protective trousers ও boots।

**২৪.** Helmet, controller, TV, lamp ও room-এর আলাদা prop reference board বানাও। TV-এর চার corner, lamp ও plant-এর position mark করো। ০১ ও ১৪-এর জন্য একই layout ব্যবহার করো।

**২৫.** Official Cyan Storm PNG আলাদা করো। Graphite body, cyan rims/decals, gold fork, headlight shape, wheel spokes, ABS ring, exhaust, mirrors ও seat-এর QC crop বানাও। Generated board-কে product reference হিসেবে ব্যবহার করার আগে official crop মিলাও।

**২৬.** Approved 3D bike asset আছে কি না team-কে জিজ্ঞেস করো। 2D PNG থেকে hidden side বা exact 3D geometry নিশ্চিত হয় না। Approved 3D asset থাকলে version ও rights লিখো। না থাকলে official photo-এর কাছাকাছি angles-এ approved generated plate। Blender proxy শুধু proof-এর জন্য।

**২৭.** `ENV_A`-এর overhead sketch আঁকো। একটাই curve, বাঁয়ে পানি, ডানে amber-lit tea stall, curb, railing, apartment frontage। Direction arrow এবং স্থির landmark তিনটা mark করো।

**২৮.** একই sketch duplicate করে `ENV_B` বানাও। Curve ও stall-এর position preserve করে road widening, palm median, Art Deco layers, practical lights ও waterfront view বসাও। Dream geography TV preview-এর framing অনুযায়ী রাখো।

**২৯.** Material/light board বানাও। A = rainy blue-grey, muted amber। B = coral-violet dusk, cyan-magenta practicals। Bike-এর factory cyan দুই state-এই official reference-এর সঙ্গে দেখো। Wetness এবং reflections light source-এর অবস্থান অনুযায়ী রাখো।

**৩০.** Reference folder থেকে প্রত্যেক shot-এর ২–৪টি governing input বাছো। Manifest-এ লিখো কোনটা face, কোনটা bike, কোনটা camera, কোনটা environment। Rain reference-এর ০৫–০৯ framing lock করো। ০৭–০৮-এ generic silhouette replace করার note দাও।

**Gate ৩ — Asset lock।** Room, face, wardrobe, product এবং একই road-এর A/B map approved। Assets-এর origin ও status trace করা যায়।

## ৪. Blender blockout ও ৫s proof

**৩১.** Blender-এ `04_CG/Dhaka_WorldBuild_v001.blend` save করো। Metric units, 24 fps, proof range frames 1–120। Low-res 540×960 proxy এবং final 1080×1920 composition guide রাখো।

**৩২.** এক curve দিয়ে road centerline, এক curve দিয়ে bike path। A এবং B collections একই coordinates-এ রাখো। Camera framing-এ tea stall ও rail যেন identifiable থাকে। Top-view screenshot save করো।

**৩৩.** Simple blocks দিয়ে lake edge, asphalt, curb, railing, stall ও façade massing বসাও। B-এর জন্য অন্তত ৩ curb module, ২ rail module, ১ façade অংশ ও ১ median/palm section বানাও।

**৩৪.** Unbranded bike proxy-তে wheel contact plane, rider volume ও headlight emitter বসাও। Path animation করো। Camera চালানোর আগেই side view-এ wheels road-এর ওপর থাকে কি না দেখো।

**৩৫.** একটি ground-level/low 3/4 camera ও একটি aerial camera বানাও। Low camera-তে beam ও target একসঙ্গে পড়তে হবে। Aerial-এ road curve ও একই landmark পড়তে হবে। Focal length ও transforms export বা note করো।

**৩৬.** প্রতি module-এ ID, road-distance position এবং target transform লিখো। Bike curve-এ যতটা এগোয়, তার সামনে headlight-এর contact point কোথায়, সেটি test করো। Simplest proof-এ contact frame হাতে mark করলেই হবে।

**৩৭.** প্রথম curb stone-এর জন্য তিন key: slot empty, stone halfway, stone seated। Headlight পৌঁছানোর পরে move শুরু, ৬–১০ frames-এ settle একটি working starting point। 24 fps playback-এ পড়তে সুবিধা হলে timing lock করো।

**৩৮.** একই pattern rail post এবং horizontal rail-এ দাও। Completed geometry শেষ পর্যন্ত active রাখো। Frame ১, midpoint ও শেষ থেকে screenshot তুলে verify করো কোনো module ফিরে disappear করছে কি না।

**৩৯.** Practical light keyframe geometry settle হওয়ার পর বসাও। Wet asphalt-এ roughness variation রাখো। Reflection আলাদা graphics হিসেবে screen-এ টেনে নেবে না। Source light উঠলে road-এর একই অংশে reflection দেখা চাই।

**৪০.** ৫s proof render করো। Export: `WB_proof_v001.mp4`, three diagnostic stills, `.blend`, current issue list। প্রথমে 540×960, 24 fps। Phone-এ sound off-এ দেখো এবং অন্তত একটি curb ও একটি rail post বসতে দেখাও।

**Gate ৪ — Proof lock।** Beam contact → physical assembly → light/reflection → completed section persists। Build fail করলে full frame count render করার আগে এই beat fix।

## ৫. Final CG, VFX ও rain plates

**৪১.** Proof scene version up করো। Approved camera/path duplicate বা link করো। Hero shot-এর handles কত frame দরকার edit থেকে লিখে নাও। Render range এবং delivery range আলাদা রাখো।

**৪২.** Final curb ও asphalt mesh detail করো। Edge bevel, puddle depression ও contact texture add করো। Empty sockets খুব ছোট হলে phone crop-এ readable করতে framing adjust করো।

**৪৩.** Rail-এর anchors, caps, horizontal bars ও shadow geometry যোগ করো। Post pivot base-এ রাখো। Mid-seat frame-এ অংশগুলি physical support-এর সঙ্গে align করো।

**৪৪.** Tea stall-এর original location, roof ও amber practical keep করো। চারপাশের building-এ frame, window recess, balcony এবং stepped frontage build করো। Anchor stall-এর position A/B-তে compare করো।

**৪৫.** Road widening এবং palm median তৈরি করো। Geometry module-by-module reveal দাও, travel direction বরাবর। One-way progress বজায় রাখো। Aerial-এ arbitrary split-এর বদলে active beam zone পড়তে হবে।

**৪৬.** ০৫/০৬-এর droplet clear-glass look set করো। ০৬-এ amber-magenta liquid visible, bike plate থেকে আলাদা। Stock/CG/AI element যেটা নাও তার source লিখো এবং macro image-এ scale ও direction lock করো।

**৪৭.** ০৯ puddle ripple-এর clean pass বানাও। TV preview-এর একই palm/frontage artwork reflection হিসেবে বসাও, perspective ও ripple distortion follow করো। Reflection পরিষ্কার রাখতে shot-এর focal plane নির্দিষ্ট করো।

**৪৮.** Shot depth অনুযায়ী rain ভাগ করো: near drops, mid-ground rain, background rain, wheel spray। Wheel spray ground contact থেকে ওঠে। ০৭-এ colour spray bike-এর পেছনে। ০৮-এ drop density pose ও frame-এর সঙ্গে compatible রাখো।

**৪৯.** Render passes plan করো। Beauty, object/material masks, depth এবং comp-এর জন্য প্রয়োজন হলে shadow, light/reflection contribution। EXR image sequence-এ test still নাও। Cryptomatte বা আলাদা matte যেটা downstream app-এ actually read হয় সেটি verify করো।

**৫০.** First, mid, last frame render করে still comp-এ আলো, reflections, CG edge ও colour test করো। Pass নাম, colour space, FPS ও frame range `Render_Readme.md`-এ লেখো। তিনটা still পাস হলে full sequence render queue দাও।

## ৬. AI footage generation ও selection

**৫১.** Shot list-এ আলাদা রাখো: room acting, buckle, gate exit, clear rain bike low, clear rain bike high, chase, product hold। CG proof বা still যথেষ্ট এমন parts-এ unnecessary motion generation কমাও।

**৫২.** Opening/closing room-এর এক shared approved reference still থেকে কাজ করো। Screen blank/dark clean plate রাখো। Face এবং TV focus area-তে রাখার framing দাও। পরে TV text track করে বসবে।

**৫৩.** Opening motion prompt-এ শুধু তিনটা action: bored slouch, helmet-এ glance, slight smile। অতিরিক্ত movement কম রাখো। Generation থেকে usable ০১–০২ trim আর TV track points আছে কি না দেখো।

**৫৪.** Buckle insert-এ glove, strap, buckle ও helmet underside reference দাও। একবার clean buckle action চাই। ছয় আঙুল, extra strap বা buckle teleport হলে take reject করো।

**৫৫.** Rain ০৭-এর start frame lock করো। Official bike PNG attach, full bike low front 3/4, readable headlight, cyan rims ও gold fork। Backlit droplets-এর সঙ্গে soft fill রাখো। Colour splash comp-এর জন্য clear space রাখো।

**৫৬.** ০৮-এর camera angle আলাদা lock করো। Slightly elevated side track। Full wheels ও tank পড়বে। Sharp bike, moving background/water। First/mid/last product check ছাড়া angle change approve কোরো না।

**৫৭.** Chase-এর start image TV preview-এর সেই bend ধরে বানাও। Rear identification official reference দিয়ে যতটা যাচাই করা যায় ততটাই use করো। Unverified rear detail close-up avoid করো। Full-face helmet এবং sensible speed সব frame-এ।

**৫৮.** এক take-এর model, mode, duration, aspect, resolution, audio ও reference IDs লিখে live quote নাও। Scope/credit cap approve হলে submit করো। Job ID note করো। Same job status verify করো, তারপর retry সিদ্ধান্ত নাও।

**৫৯.** Candidate takes এক grid-এ compare করো: acting, product, full gear, wheel contact, line of motion, background separation, usable duration। First/mid/last দেখার পর high-risk moving edges frame-step করো। Downloaded original ও selected trim আলাদা রাখো।

**৬০.** Shot যদি fail করে, শুধু একটি variable বদলাও: reference, action, lens/framing বা duration। Decal/ABS drift বারবার হলে tighter verified angle বা controlled compositing বেছে নাও। Requote এবং scoped approval অনুযায়ী retry।

## ৭. After Effects compositing

**৬১.** AE project-এ frame rate ও working colour settings যাচাই করো। Blender EXR, generated SDR plate ও output view-এর test still compare করো। Double transform এড়াতে pipeline note-এ কোথায় transform হচ্ছে লিখো।

**৬২.** Each shot precomp বানাও। Bottom থেকে environment, contact shadow/reflection, bike/rider, depth-based rain, local light wrap, finishing layers। File naming shot tracker-এর সঙ্গে মিলাও।

**৬৩.** Plate horizon, vanishing point ও wheel position CG camera-র সঙ্গে align করো। Lens mismatch হলে crop/reframe test করো। Front tyre slide বা plate scale pumping থাকলে take change বা limited retime test করো।

**৬৪.** Bike/rider matte তৈরি করো। Helmet edge, spokes, mirrors, fork gaps, gloves এবং boot edges clean করো। Matte frame-by-frame দেখে chatter/flicker fix করো। Colour spill কমিয়ে cyan paint preserve করো।

**৬৫.** Tyre-এর নিচে contact shadow দিন এবং motion-এর সঙ্গে lock করো। Wheel reflection wet surface-এ view angle অনুযায়ী narrow/soft করো। Shadow missing থাকলে bike ভাসবে, তাই phone preview-এ আলাদা check করো।

**৬৬.** Headlight spill actual beam patch-এ match করো। Curb socket reveal-এর আগে light পৌঁছাবে। Light wrap কম রাখো যাতে exact badge, decal ও fork edges readable থাকে।

**৬৭.** Rain element সামনে/পেছনে split করো এবং rider/vehicle matte দিয়ে occlude করো। Ground spray wheels-এর দিক অনুসরণ করবে। Colour burst থেকে wet-road reflection-এ hue continuity দেখো।

**৬৮.** TV corners track করো। Editable title, ৩%/৪%, progress bar ও original preview বসাও। Screen glare আর perspective দিয়ে room-এ integrate করো। Plain text approval variant ও clean edit layer আলাদা রাখো।

**৬৯.** ০৯→১০ match cut-এ ripple arc, beam patch ও shutter colour মিলাও। ১০→১১ cut-এ bike direction একই রেখে shot scale বদলাও। Comp frame handles check করো।

**৭০.** ১০০% zoom-এ first/mid/last ও fast transitions দেখো। Edge fringing, double shadows, drifting reflections, halo, hand/part morph, missing frames fix করো। `S##_comp_review_v###` export করে tracker update করো।

**Gate ৫ — Shot lock।** Product, safety, causality, rain layering ও TV track পাস। Camera match-এ বড় সমস্যা থাকলে final edit-এর আগে সংশ্লিষ্ট shot fix।

## ৮. Edit, rhythm ও transitions

**৭১.** Approved comp clips নতুন versioned Premiere sequence-এ relink করো। Animatic underneath reference হিসেবে রাখো। Clip ranges ও handles মিলিয়ে ৩৮৪ frame নিশ্চিত করো।

**৭২.** প্রথম ৬০ frames-এ TV title, bored face, idea ও buckle পড়ছে কি না পরীক্ষা করো। Reaction too short হলে ০১/০২-এর মধ্যে time shift করো। Total cut duration ধরে রাখো।

**৭৩.** ০৪ wide shot-এ tea stall এবং rail identify করার মতো সময় রাখো। তারপর ০৫–০৬ macro jump-এ continuity leaf ও drop position দিয়ে ধরো।

**৭৪.** ০৭ ও ০৮-এ visual novelty আলাদা করো: প্রথমটায় readable headlight/tank ও colour spray, পরেরটায় high angle ও running rain। Similar beat মনে হলে end trim করো, model বদলাবে না।

**৭৫.** ০৯ puddle macro থেকে ১০ curb seat-এ প্রতিটি কাটে direction continuity দেখো। মাঝখানে অতি ছোট flash frame চোখে কষ্ট দিলে cut সরাসরি রাখো।

**৭৬.** Hero sequence-এ curb ও rail-এর completion পড়ার মতো সময় দাও। Aerial-এ একই stall/curve পড়লেই chase-এ চলে যাও। Duplicate wide বা product angle দিয়ে এই অংশ stretch কোরো না।

**৭৭.** TV preview-এর skyline ও chase-এর skyline side-by-side দেখো। Palm/curve/water/stall alignment ঠিক করো। Camera match-এর strongest frame chase-এর first readable moment-এ রাখো।

**৭৮.** ১৩→১৪ hard cut পরীক্ষা করো। Engine/rain out, room tone in। ৪% পড়ার আগে end card এলে duration বরাদ্দ বদলাও। অতিরিক্ত transition shot যোগ করার প্রয়োজন হলে fresh-viewer test দিয়ে বিচার করো।

**৭৯.** End card ১৫–১৬-এর জন্য একটি hold ব্যবহার করো। Approved tagline ও Yamaha logo clean space-এ বসাও। Phone app safe area-তে text এবং logo screen controls-এর নিচে পড়ে কি না দেখো।

**৮০.** Picture lock `MT15_picture_lock_v###` export করো। Silent playback ও 1x phone playback-এ pacing notes নাও। Frame change হলে sound cue sheet ও grade timeline-এ একই version পাঠাও।

## ৯. Music, sound design ও colour grade

**৮১.** ১৬s sound cue sheet বানাও। Opening fan/controller, idea-তে tiny pulse, buckle transient, rain bed, droplet hit, concrete/metal clicks, boulevard swell, hard cut room tone, end sting। প্রতি cue-তে frame index লিখো।

**৮২.** Music source lock করো। Original বা commercial-use rights clear synth cue বাছো। যদি generation প্রয়োজন হয়, provider terms ও cost দেখে scoped approval নাও। Game score, radio track ও recognizable melody বাদ দাও।

**৮৩.** Music brief: restrained synth texture, sparse pulse early, rainfall passage-এ room, curb/rail transient-এর জন্য space, boulevard-এ wider harmonic swell, hard cut-এর জায়গায় clean stop। Lead vocal ছাড়াই test করো।

**৮৪.** Engine sound official approved existing source বা rights-cleared suitable layer থেকে নাও। New real recording দরকার হলে এই AI/CG-only scope পুনরায় confirm করো। Pitch, speed ও distance shot-এর সঙ্গে match করো।

**৮৫.** Premiere/DAW-এ MUSIC, FOLEY, VEHICLE, AMBIENCE ও VFX tracks আলাদা করো। Practical clicks picture frame-এ sync করো। Rain ও music transient ঢেকে দিলে automation দিয়ে duck করো।

**৮৬.** Headphones ও phone speaker-এ mix চালাও। Harsh high end, over-compressed rain, too-loud engine, clipped peak check করো। Output loudness spec থাকলে সেই target use করো। Reference level and true peak log রাখো।

**৮৭.** Grade-এর আগে shots match করো। Room skin tone, rainy exterior exposure এবং exact cyan bike-এর baseline set করো। Scope-এ crushed shadow বা clipped neon আছে কি না দেখো।

**৮৮.** Look pass দাও। Room warm practical + cool TV। Real Dhaka cool rain + small amber pools। Dream world coral-violet dusk + cyan-magenta practicals। Product cyan, gold fork ও skin tone selective correction-এ স্থির রাখো।

**৮৯.** Grain, bloom ও vignette restrained রাখো। Product decal/ABS details এবং TV copy হারালে effect intensity কমাও। A/B environment-এ same bike ধরে colour flicker check করো।

**৯০.** Picture lock + final mix + grade combine করে `MT15_client_review_v###.mp4` export করো। একবার mute, একবার phone speaker, একবার headphones-এ দেখো। Notes-এ frame/timecode বসাও।

## ১০. Approval, QC ও delivery

**৯১.** Review link বা file-এ exact version ও targeted questions দাও। First second-এ game reference ধরা পড়ে? Idea বোঝা যায়? কোন মুহূর্তে শহর তৈরি শুরু হয়? ৪% punchline পড়া যায়? Feedback একই tracker-এ আনো।

**৯২.** Review notes-কে fix/optional/out-of-scope লিখে owner assign করো। Approved cut-এ ripple effect বদলালে downstream grade এবং mix timing affected কি না দেখো। Extra scope হলে fee/timeline written update করো।

**৯৩.** Product QC side-by-side official crop দিয়ে করো। Headlight, tank decals, fork, rims, tyre shape, ABS ring, exhaust ও seat first/mid/last এবং motion trouble points-এ দেখো। Wrong detail থাকলে shot fail।

**৯৪.** Safety ও branding pass। Full-face helmet/gear, controlled legal riding, unchanged model, brand-approved Yamaha overlay, no stray logos/text, no official game logo/footage/UI, no unauthorized claims।

**৯৫.** Public title, rights and approval row check করো। GTA VI plain-text public use-এর clearance এবং final cut sign-off record করো। Pending থাকলে version review status-এ রাখো। Clean layer থেকে alternate export কেবল scope অনুযায়ী।

**৯৬.** High-quality master export করো agreed codec-এ। Practical handoff: ProRes 422 HQ বা DNxHR HQX যদি client spec নেয়। Mobile review/publish copy 1080×1920 H.264/AAC, 24 fps, Rec.709 SDR অনুযায়ী export। Exact client/platform settings export-এর আগে confirm করো।

**৯৭.** Technical decode run করো। FPS, size, duration, audio stream ও unexpected errors check করো। ১৬s target হলে ৩৮৪ frames মিলাও। Exported file opening, build, end card-এ seek করো।

```bash
ffprobe -v error -select_streams v:0 -count_frames \
  -show_entries stream=width,height,r_frame_rate,nb_read_frames:format=duration \
  -of json MT15_final.mp4
ffmpeg -v error -i MT15_final.mp4 -f null -
```

**৯৮.** Mobile full screen-এ UI safe area, compression, readability, first-frame load এবং final frame black flash check করো। TV ৩%, ৪%, model spelling ও Bangla tagline অক্ষরে অক্ষরে মিলাও।

**৯৯.** `09_DELIVERY`-তে approved master, mobile copy ও one-page delivery note রাখো। Version, duration, fps, codec, approval status, rights references লিখো। Source project/stems only if in scope। Share package reopen করে playback confirm করো।

**১০০.** Final gate sign-off-এর পর approved publish workflow-তে handoff করো। কে publish করবে, কোন version, এবং product outcome কীভাবে মাপবে, tracker-এ লিখো। Test ride/lead/dealer intent-এর metric owner ঠিক করো।

**Gate ৬ — Delivery lock।** Approved version, rights, product QC, mobile playback ও technical decode পাস। Publishing আলাদা authorized action।

---

## Copy-paste briefs

### Codex বা Claude Code-এ Blender proof brief

> Build a **5.00s, 540×960, 24 fps Blender proof** for the MT-15 film using a simple unbranded bike proxy. First check the actual Blender executable and test a one-frame render. Use one road curve, water on the left, one fixed tea stall on the right, three curb modules and two rail modules. The bike advances on the road. Animate a visible headlight contact patch. One curb stone and one rail post must visibly seat after light contact. Completed modules persist. A practical light appears after its module seats and reflects in wet asphalt. Keep unfinished grey modules ahead. Use a low camera that reads the contact and one aerial still. Save the .blend, build script, frame range, 5s MP4 and before/mid/after stills. Report verified observations, output paths and blockers. Use local tools within this task. Ask before spending, uploading or starting paid generations.

### Motion prompt skeleton

> Shot [ID], [duration], 9:16. Exact Yamaha MT-15 V2 Cyan Storm from the attached official product reference. Preserve graphite panels, cyan factory rims and graphics, gold forks, real headlight, correct front brake/ABS ring, exhaust and proportions. Same adult rider from approved character/wardrobe reference, full-face helmet visor down and complete protective gear. [One action]. [One camera angle and movement]. [One lighting state]. Keep bike unobstructed, stable and in contact with the road. No wheelie, speeding, added logos, text or parts. Provide a clean plate suitable for compositing.

### Blocker card

```text
SOP step / shot:
Expected result:
Actual result:
Timecode / frame and current version:
Tool + version / model + settings:
Reference filenames and job ID, if any:
Exact error or one screenshot + 2–5s sample:
What I tried and what changed:
Budget/approval remaining:
Please identify the most likely cause, give one reversible next action,
and tell me how to verify it before proceeding.
```

| সমস্যা | প্রথম reversible test |
|---|---|
| Blender render black | এক still-এ active camera, light ও render visibility check। Beauty pass inspect। |
| EXR washed out/too dark | একই test still-এর source colour space ও output transform compare। Duplicate transform একবার bypass। |
| Beam light আসে কিন্তু build বোঝা যায় না | Empty slot → halfway → seated এই তিন still render। Missing middle state fix করে ৫s loop। |
| Bike ভাসছে বা wheel slide | Side view-তে tyre contact frame-step, তারপর plate alignment/shadow check। |
| Cyan rims/decals বা ABS বদলায় | Official reference crop compare। Problem shot isolate, smaller camera move বা reference angle test। |
| ০৭–০৮-এ splash bike ঢেকে ফেলে | Colour element toggle। Bike plate ঠিক থাকলে foreground matte ও splash position fix। |
| GTA VI / ৩% পড়ে না | Phone-size still দেখো। TV crop, text scale ও contrast ঠিক করে first-second review। |
| ৪% payoff পড়ে না | একই room shot দিয়ে ১৩→১৪ hard cut test। Room tone and hold duration check। |
| Cut slow লাগে | Edit marker-এ duplicate angle identify। First cut/remove test, then re-time sound। |
| Paid job stuck | Existing job ID ও status verify। Charged/queued status clear হওয়ার আগে duplicate submit কোরো না। |

### Technical references

- [Blender background rendering](https://docs.blender.org/manual/en/latest/advanced/command_line/render.html)
- [Blender render passes and Cryptomatte](https://docs.blender.org/manual/en/latest/render/layers/passes.html)
- [Adobe Premiere and After Effects colour management](https://helpx.adobe.com/premiere/desktop/correct-color/set-up-color-management/premiere-after-effects-color-management-compatibility.html)
