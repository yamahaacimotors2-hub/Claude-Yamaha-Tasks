# Yamaha MT-15 V2 Cyan Storm — Final SOP v2

**১৬ সেকেন্ড · 9:16 · AI + CG · একা একজন বানাতে পারবে এমনভাবে সাজানো**

আগের SOP: ১০০ step, ১৫ shot, ৬ gate। এই version: **৩৬ step, ১২ shot, ৬ gate**। গল্প, end line আর product lock একই আছে।

---

## ০. এক নজরে: কী বদলালো আর কেন

| # | বদল | কেন |
|---|---|---|
| ১ | Bike আর CG শহর আলাদা বানিয়ে After Effects-এ জোড়া লাগানো **বাদ** (hero build ছাড়া) | পুরোনো SOP-র সবচেয়ে কঠিন অংশ ছিল এটা: spoke, mirror, fork ধরে roto, wheel shadow, wet reflection। একা করলে কয়েক দিন যাবে, তবু নকল দেখাতে পারে |
| ২ | Hero build shot-এ শুধু **সামনের চাকা, fork আর beam** দেখা যাবে | ACI-র কাছে 3D file নেই। পুরো bike নিখুঁত বানানো যাবে না, কিন্তু cyan rim, gold fork, disc আর tyre Blender-এ ঠিকঠাক বানানো যায়। আর line টাই তো "Map লোড হয় **চাকার নিচে**" |
| ৩ | End card-এ **official PNG টাই** বসবে | Generate করলে decal বা ABS ring বদলে যেতে পারে। আসল ছবি বসালে product ১০০% ঠিক |
| ৪ | ১৫ shot থেকে ১২ shot | Hero build পেত মাত্র ২.২৫ সেকেন্ড। এখন পায় ৩ সেকেন্ড |
| ৫ | Game title-এর clearance **শুরুতেই চাওয়া**, শেষে না | পুরোনো SOP-তে clearance ছিল step ৯৫-এ। ততদিনে সব বানানো শেষ, তখন "না" এলে opening টাই ভেঙে যায় |
| ৬ | টাকা খরচের আগে **একটা product test** | AI video MT-15 ঠিক রাখতে পারে কি না, এটা এক take-এই জানা যায়। না পারলে বাকি plan বদলাতে হবে |

---

## ১. Audit: পুরোনো SOP-তে যে gap পেয়েছি

### বড় gap (এগুলো ঠিক না করলে film আটকাবে)

1. **Step ২৬, ৬৩–৬৫: bike plate + CG comp।** উপরের ১ নম্বর বদল দেখো। এটাই পুরো SOP-র সবচেয়ে বড় ঝুঁকি ছিল।
2. **Step ০১, ০৩, ৯৫: "GTA VI" লেখা।** অন্য কোম্পানির game-এর নাম Yamaha-র বিজ্ঞাপনে ব্যবহার করা একটা legal প্রশ্ন, আর সিদ্ধান্তটা ACI/Yamaha-র। আগের handoff-এ lock ছিল "game title, name, logo বাদ"; নতুন SOP তার উল্টো বলছে। আমি আইনজীবী নই, তাই শুধু ঝুঁকিটা জানাচ্ছি। **সিদ্ধান্ত:** নাম সহ version-ই main। TV-র লেখা আলাদা layer থাকবে, আর ACI-র লিখিত clearance publish-এর আগে লাগবে।
3. **পানি কোন পাশে?** নতুন SOP বলছে বাঁয়ে পানি, ডানে চায়ের দোকান। আগের board-এ (frame ১২, ১৪) উল্টো ছিল, আর আমার Blender proof-ও সেই উল্টোটা ধরে বানানো। Lock হয়েছে: পানি বাঁয়ে। Proof v3 এই map-এ বানানো।
4. **Product reference মাত্র একটা angle।** Official PNG শুধু সামনে-ডান ৩/৪ দেখায়। পেছন আর পাশ কোথাও নেই। তাই chase shot (১৩) আর high side shot (০৮)-এ AI আন্দাজে বানাবে। ACI-র কাছে 3D নেই, কিন্তু অন্য angle-এর official ছবি থাকার কথা। সেগুলো চেয়ে নাও।
5. **কোন রঙের কারণ কী?** SOP-তে লেখা "raindrop রঙে ফাটে", কারণ লেখা নেই। তুমি আগেই ঠিক করেছ: headlight-এর আলো drop-এ ঢুকে রঙ তৈরি করে। এটা SOP-তে ছিল না, এখন আছে।

### মাঝারি gap

6. **সময় খুব টাইট।** ০৫, ০৬, ০৯ প্রতিটা প্রায় আধা সেকেন্ড। Puddle-এর ভেতরে স্বপ্নের waterfront ১৩ frame-এ phone-এ পড়া যাবে না। আমার পরামর্শ: puddle শুধু ripple দেখাক আর beam-এর হাতে তুলে দিক। (সিদ্ধান্ত হয়ে গেছে: শুধু ripple।)
7. **প্রথম frame-এ চারটা জিনিস পড়তে হবে:** মুখ, TV title, ৩%, আর TV-র ভেতরে preview। ২৮ frame-এ এটা বেশি। সমাধান: TV দিয়ে শুরু, তারপর মুখ।
8. **Step ৪৯, ৬১: EXR, Cryptomatte, colour pipeline।** ১ নম্বর বদলের পর এগুলো শুধু hero build shot-এ লাগবে, বাকিতে লাগবে না।
9. **বাংলা লেখা।** After Effects আর Premiere-এ বাংলা যুক্তাক্ষর ভেঙে যেতে পারে। Tagline Photoshop-এ লিখে PNG হিসেবে export করো, তারপর বসাও। আগে একবার test করে দেখো।
10. **Backup step নেই।** Cloud session মুছে যায়। প্রতিদিন কাজ শেষে Git push আর বড় video Google Drive-এ।
11. **মোট credit-এর আন্দাজ নেই।** নিচে section ৬-এ দিয়েছি।

### যা ভালো ছিল, রেখে দিয়েছি

Frame table-এর যোগফল ঠিক ৩৮৪ (আমি গুনে দেখেছি)। Version naming, tracker, sound off-এ তিনজন নতুন দর্শকের test, paid run-এর আগে quote আর approval, product QC crop, blocker card: সব ভালো, সব আছে।

---

## ২. কোন tool কী করবে

| কাজ | Tool | কোথায় চলবে |
|---|---|---|
| Room, buckle, rain, bike-এর shot (still + video) | **Higgsfield** (image + Seedance video) | Claude app-এর connector, বা Higgsfield website |
| শহর তৈরির hero shot, aerial, chase-এর layout | **Blender** | তোমার computer (final render-এর জন্য GPU লাগবে) |
| Blender চালানো, script লেখা | **Claude Code + Blender MCP** | তোমার computer |
| Animatic, cut জোড়া, file check, tracker | **Claude Code** (FFmpeg script) | Cloud বা local, দুটোতেই চলে |
| প্রতিটা gate-এ দ্বিতীয় চোখ | **ChatGPT Codex** | একই project folder, শুধু review |
| TV-র লেখা বসানো, end card | **After Effects** | তোমার computer |
| বাংলা tagline, end card-এর bike | **Photoshop** | তোমার computer |
| Edit, sound, grade | **Premiere Pro** | তোমার computer |
| বড় file-এর backup | **Google Drive** | — |
| Script, SOP, tracker, ছোট file | **GitHub repo** (`Claude-Yamaha-Tasks`) | — |

**Android Studio লাগবে না**, বন্ধ করে দিতে পারো।

**Claude Code আর Codex-এর নিয়ম:** একই file দুজন একসাথে বদলাবে না। Claude Code বানায়, Codex দেখে আর issue লেখে।

### যা install / download করতে হবে

| কী | কেন | কীভাবে |
|---|---|---|
| **Claude Code** (desktop app বা CLI), তোমার computer-এ | Blender চালাতে | Repo টা clone করে সেই folder-এ খোলো |
| **uv** | Blender MCP চালাতে লাগে | Official installer দিয়ে। `pip install uv` দিয়ে না |
| **Blender MCP add-on** (`addon.py`) | Claude আর Blender-এর সংযোগ | `github.com/ahujasid/blender-mcp` থেকে file নামাও → Blender: Edit > Preferences > Add-ons > Install → enable করো |
| Blender MCP server | একই | Terminal-এ: `claude mcp add blender uvx blender-mcp` |
| **FFmpeg** | File check, animatic | Windows: `winget install ffmpeg` · Mac: `brew install ffmpeg` |
| **বাংলা font** | Tagline | Brand font থাকলে সেটা; না থাকলে Hind Siliguri বা Noto Sans Bengali (free) |
| Official MT-15 ছবি, সব angle | Product reference | ACI থেকে: সামনে, দুই পাশ, পেছন, উপর |

Blender MCP একবারে একটা app থেকেই চালাও (Claude Code অথবা Claude Desktop, দুটো একসাথে না)।

### MCP / connector কোথায়

- **Blender MCP:** শুধু তোমার computer-এ। Cloud session থেকে তোমার Blender ধরা যায় না।
- **Higgsfield connector:** Claude app-এ। (যে cloud session-এ এই SOP লেখা, সেখানে Higgsfield-এর video generation tool গুলো load হয়নি, তাই generation ওখান থেকে না।)
- **Google Drive connector:** backup-এর জন্য, ঐচ্ছিক।
- **Adobe connector:** এই session-এ connect হয়নি। এর উপর ভরসা কোরো না; After Effects আর Premiere হাতে চালাও।

### Cloud session (Claude Code on the web) কীসে কাজে লাগে

Script লেখা, low-res Blender proof (৫৪০×৯৬০, প্রতি frame প্রায় ৯ সেকেন্ড, GPU নেই), FFmpeg দিয়ে animatic, audio transcribe, tracker। **Final 1080p render ওখানে না**, তোমার computer-এ।

---

## ৩. নতুন cut: ১২ shot, ৩৮৪ frame

24 fps। Range-এর শুরু ধরা, শেষ বাদ।

| Shot | Frame | সেকেন্ড | কী পড়বে |
|---|---:|---:|---|
| S01 | 000–030 | 1.25 | TV: download ৩%, তারপর বিরক্ত মুখ |
| S02 | 030–050 | 0.83 | Helmet-এ চোখ, মাথা ওঠে, হালকা হাসি |
| S03 | 050–062 | 0.50 | Buckle click |
| S04 | 062–096 | 1.42 | বৃষ্টিভেজা ঢাকা, চায়ের দোকান আর rail চেনা যায় |
| S05 | 096–126 | 1.25 | ঝুলে থাকা drop → headlight-এর আলো ঢোকে → amber-magenta burst (এক take) |
| S06 | 126–150 | 1.00 | Low front ৩/৪, স্পষ্ট Cyan Storm, রঙিন spray পেছনে |
| S07 | 150–164 | 0.58 | Puddle-এ ripple |
| S08 | 164–236 | **3.00** | **Hero build, এক টানা shot:** চাকার পাশে নিচু camera। Beam খালি slot ছোঁয় → curb-এর পাথর বসে → rail post ওঠে → আলো জ্বলে → ভেজা রাস্তায় reflection |
| S09 | 236–272 | 1.50 | Aerial: পেছনে তৈরি, bike-এর কাছে তৈরি হচ্ছে, সামনে grey |
| S10 | 272–302 | 1.25 | Rear chase, waterfront খুলে যায় |
| S11 | 302–342 | 1.67 | Hard cut, একই ঘর, download ৪% |
| S12 | 342–384 | 1.75 | End card: bike, "Map লোড হয় চাকার নিচে।", Yamaha logo |

যোগফল ৩৮৪ frame = ১৬.০০ সেকেন্ড।

**পুরোনো থেকে যা বাদ বা জোড়া:** পুরোনো ০৫+০৬ এখন এক take (S05)। পুরোনো ০৮ (high side view) বাদ, কারণ ওই angle-এর product reference নেই। পুরোনো ১০+১১ এখন এক টানা shot (S08)। পুরোনো ১৫+১৬ এক hold (S12)।

---

## ৪. Shot ধরে: কোনটা কীভাবে বানাবে

| Shot | পদ্ধতি | Product ঝুঁকি |
|---|---|---|
| S01, S02 | Higgsfield: একটা room still → **এক take**-এ বিরক্তি, glance, হাসি। TV screen ফাঁকা রাখো | নেই |
| S11 | S01-এর **একই still** থেকে আরেকটা take | নেই |
| S03 | Higgsfield: ছোট insert | নেই |
| S04 | Blender-এর map থেকে একটা layout frame → Higgsfield image → video | মাঝারি (bike দূরে) |
| S05 | Higgsfield: macro, bike নেই | নেই |
| S06 | Higgsfield: official PNG reference দিয়ে। Reference-এর angle-এর সাথে মেলে | **এটাই product test, সবার আগে** |
| S07 | Higgsfield: macro | নেই |
| S08 | **Blender**, final render। Frame-এ শুধু সামনের চাকা, fork, fender, beam | কম (চাকা আর fork Blender-এ বানানো) |
| S09 | **Blender**, bike খুব ছোট | কম |
| S10 | দুই পথ: (ক) ACI থেকে পেছনের official ছবি পেলে Higgsfield; (খ) না পেলে Blender, bike দূরে আর ছোট | **বেশি**, পেছনের reference না থাকলে |
| S12 | **Photoshop + After Effects:** official PNG কেটে waterfront background-এ, নিচে shadow আর reflection | শূন্য |
| TV-র লেখা (৩%, ৪%, title) | After Effects: corner pin | — |

---

## ৫. ৩৬ step

প্রতিটা step-এ লেখা কে করবে: **তুমি**, **CC** (Claude Code), **Codex**, বা **HF** (Higgsfield)।

### Phase ১ — সিদ্ধান্ত আর setup (আধা দিন)

**০১. তুমি:** ACI-কে তিনটা জিনিস জিজ্ঞেস করো: (ক) TV-তে game-এর নাম থাকতে পারবে কি না, (খ) MT-15-এর সব angle-এর official ছবি, (গ) Yamaha logo file আর brand font।
**০২. তুমি:** তিনটা সিদ্ধান্ত ঠিক করো। (হয়ে গেছে, section ৭ দেখো।)
**০৩. তুমি:** উপরের install list শেষ করো।
**০৪. CC:** Folder tree আর tracker বানাও (পুরোনো SOP step ০৪–০৬ যেমন ছিল)।
**০৫. তুমি + CC:** Tool test। Blender-এ MCP দিয়ে একটা cube render; AE আর Premiere-এ ১ সেকেন্ডের export; Photoshop-এ বাংলা tagline লিখে PNG।
**০৬. CC:** উপর থেকে দেখা map আঁকো: ডানে বাঁক, পানি বাঁয়ে, চায়ের দোকান ডানে, rail পানির পাশে, তিনটা landmark, চলার দিক। এই map আর বদলাবে না।

> **Gate ১.** Title-এর সিদ্ধান্ত, ACI-কে পাঠানো clearance request, map, cut আর tool test হাতে আছে।

### Phase ২ — Animatic (আধা দিন)

**০৭. তুমি:** Latest board (`exec-3f8723b6…png`) Claude Code-কে দাও।
**০৮. CC:** Board কেটে panel আলাদা করো, section ৩-এর timing অনুযায়ী FFmpeg দিয়ে `MT15_animatic_v001.mp4` বানাও, shot নম্বর burn-in সহ।
**০৯. তুমি:** তিনজন নতুন মানুষকে sound off-এ একবার দেখাও। তিন প্রশ্ন: কী download হচ্ছিল? ছেলেটা কেন বের হলো? শহর বদলালো কীভাবে?
**১০. Codex:** Animatic আর উত্তরগুলো দেখে দুর্বল জায়গার list দিক।

> **Gate ২.** তিন প্রশ্নের উত্তর ঠিক আসে। না এলে timing বদলাও, shot যোগ কোরো না।

### Phase ৩ — Asset আর product test (১ দিন)

**১১. HF:** Protagonist-এর একটা face reference আর room still (TV ফাঁকা)।
**১২. তুমি:** Official PNG থেকে QC crop: headlight, tank decal, fork, rim, ABS ring, exhaust, seat।
**১৩. HF:** **Product test।** S06-এর একটাই take, official PNG reference দিয়ে। আগে live quote নাও।
**১৪. তুমি + Codex:** Test take-এর প্রথম, মাঝের আর শেষ frame QC crop-এর সাথে পাশাপাশি মেলাও।

> **Gate ৩.** MT-15 তিন frame-এই ঠিক থাকে। না থাকলে থামো: reference বদলাও বা camera move ছোট করো, তারপর আবার এক take। এই gate পাস না হলে বাকি bike shot-এ credit খরচ কোরো না।

### Phase ৪ — Blender hero build (২ দিন)

**১৫. CC:** আগের proof (`mt15_blender_proof/proof.py`) নতুন map অনুযায়ী ঘোরাও।
**১৬. CC:** সামনের চাকার assembly বানাও: tyre, cyan rim, disc + ABS ring, gold fork, fender। Official crop-এর সাথে মেলাও।
**১৭. CC:** S08-এর camera: চাকার পাশে নিচু, beam-এর দিকে তাকানো। Frame-এ চাকা, beam-এর patch, খালি slot আর পাথর বসা একসাথে।
**১৮. CC:** ৫৪০×৯৬০-এ S08, S09, S10-এর proof render।
**১৯. তুমি:** Phone-এ sound off-এ দেখো। একটা পাথর আর একটা rail post বসতে দেখা যায়? পেছনের অংশ তৈরি থাকে?
**২০. CC:** পাস হলে detail বাড়াও (bevel, puddle, দোকান, জানালা), তারপর তোমার GPU-তে 1080×1920 final render।

> **Gate ৪.** Beam ছোঁয়া → বসা → আলো → reflection → পেছনে তৈরি থাকা। আগের proof v2-তে এগুলো তিন shot মিলিয়ে দেখা গেছে; এক shot-এ চাকা সহ এখনও দেখানো হয়নি।

### Phase ৫ — বাকি shot generate (১–২ দিন)

**২১. HF:** S01+S02 এক take।
**২২. HF:** S11, একই still থেকে।
**২৩. HF:** S03, S05, S07।
**২৪. HF:** S04, Blender layout frame থেকে।
**২৫. HF বা CC:** S10, section ৪-এর দুই পথের একটা।
**২৬. তুমি:** প্রতিটা take-এ: job ID tracker-এ, original আর trim আলাদা। Fail করলে **একটাই** জিনিস বদলে আবার।

### Phase ৬ — Comp, edit, sound, grade (২ দিন)

**২৭. তুমি (AE):** TV-তে ৩%, ৪% আর title corner pin দিয়ে। Title আলাদা layer-এ রাখো।
**২৮. তুমি (Photoshop + AE):** S12 end card: official PNG, shadow, reflection, tagline PNG, logo।
**২৯. তুমি (Premiere):** ১২ shot বসাও, animatic নিচে reference। ৩৮৪ frame মেলাও।
**৩০. তুমি:** Sound: fan/controller, buckle, rain, drop, পাথর আর metal-এর click, swell, hard cut-এ room tone, end sting। Engine আর music rights-clear উৎস থেকে।
**৩১. তুমি:** Grade: ঘর warm, ঢাকা cool rain, স্বপ্নের শহর coral-violet। Bike-এর cyan আর gold fork সব shot-এ একই।
**৩২. CC:** Export-এ FFmpeg check: size, fps, ৩৮৪ frame, audio, error।

> **Gate ৫.** Product, helmet/gear, কারণ-ফলাফল আর TV-র লেখা পাস।

### Phase ৭ — QC আর delivery (আধা দিন)

**৩৩. Codex:** পুরো film frame ধরে দেখে issue list।
**৩৪. তুমি:** Phone-এ full screen: লেখা app-এর button-এর নিচে পড়ছে না তো? ৩%, ৪%, model-এর বানান, বাংলা tagline অক্ষরে অক্ষরে।
**৩৫. তুমি:** ACI-র approval আর title clearance লিখে রাখো।
**৩৬. তুমি:** Master + mobile copy `09_DELIVERY`-তে, Drive-এ backup। Publish আলাদা অনুমতির কাজ।

> **Gate ৬.** Approved version, rights, product QC, mobile playback আর technical check পাস।

মোট আনুমানিক ৭–৮ কাজের দিন, ACI-র উত্তরের অপেক্ষা বাদে।

---

## ৬. Credit-এর আন্দাজ

তোমার পুরোনো quote ধরে হিসাব (এখনকার দাম আলাদা হতে পারে, প্রতিবার live quote নাও):

- পুরোনো quote: ৫ সেকেন্ড, 720p, 9:16 = ৩৫ credit।
- Generate করতে হবে ৮টা shot (S01+02, S03, S04, S05, S06, S07, S10, S11)।
- গড়ে ৩ take ধরলে ২৪ take × ৩৫ = **প্রায় ৮৪০ credit**, 720p-তে।
- 1080p final-এ খরচ বেশি: পুরোনো ১০s+৮s quote ছিল ২৮৮, অর্থাৎ সেকেন্ডে প্রায় ১৬।

আগের plan-এ ছিল ১৫ shot, প্রায় সবগুলোতে bike। এখন bike সহ generate মাত্র ৩টা (S04, S06, S10)।

---

## ৭. Lock হওয়া সিদ্ধান্ত

| # | সিদ্ধান্ত | এর মানে |
|---|---|---|
| ১ | **Game-এর নাম সহ version-ই main** | TV-তে title থাকবে। ACI/Yamaha-র লিখিত clearance tracker-এ একটা খোলা item হিসেবে থাকবে (step ০১, ৩৫)। TV-র লেখা আলাদা AE layer, তাই পরে বদলাতে হলে শুধু layer বদলালেই হবে |
| ২ | **Puddle-এ শুধু ripple** | S07-এ স্বপ্নের শহরের reflection নেই। Ripple-এর উজ্জ্বল ring টা beam-এর patch-এর সাথে match cut |
| ৩ | **পানি বাঁয়ে, দোকান আর building ডানে** | রাস্তা ডানে বাঁকে। Bike বাঁ lane-এ চলে (বাংলাদেশে বাঁ দিক দিয়ে চলা), তাই পানির পাশের curb আর rail bike-এর ঠিক পাশে |

---

## ৮. এখন পর্যন্ত যা হয়ে আছে

| জিনিস | অবস্থা |
|---|---|
| Blender proof script (`mt15_blender_proof/proof.py`) | আছে, চলে |
| Proof v2: curb-side ৫s, aerial ২s, chase ২s | আছে (`mt15_blender_proof/out/`) |
| Scene file (`.blend`) | আছে |
| নতুন map অনুযায়ী সাজানো (পানি বাঁয়ে) | হয়েছে, proof v3 |
| সামনের চাকা (cyan rim, gold fork, fender, disc) আর hero camera | হয়েছে, proof v3 (`out/v3_water_left_hero_wheel/`) |
| Animatic | বাকি, latest board লাগবে (step ০৭) |
| Product test | বাকি, তোমার approval লাগবে (step ১৩) |

---

## ৯. Copy-paste brief

### Claude Code (তোমার computer, Blender MCP চালু)

> Open `mt15_blender_proof/proof.py` in this repo. Mirror the scene to match the locked map in `00_BRIEF/map.png`. Build a front-wheel assembly for the bike proxy: tyre, cyan 5-spoke rim, brake disc with ABS ring, gold fork tubes, front fender; compare against `02_ASSET_BIBLE/product_crops/`. Add a low camera beside the front wheel looking along the headlight beam so the wheel, the beam patch, empty kerb slots and seating stones are all in frame. Render frames 1–72 at 540×960, 24 fps, and save the MP4, three stills (slot empty / stone halfway / seated) and the .blend. Report what you verified and any blockers. Do not spend credits, upload or publish.

### Codex (review)

> Review only, do not edit files. Watch `[file]` frame by frame against `MT15_Final_SOP_v2.md` Gate [N]. For each failure give the frame number, what is wrong, and the smallest fix. Check product details against `02_ASSET_BIBLE/product_crops/`. List what you could not verify.

### Motion prompt (Higgsfield)

> Shot [ID], [duration], 9:16. Exact Yamaha MT-15 V2 Cyan Storm from the attached official product reference. Preserve graphite panels, cyan factory rims and graphics, gold forks, real headlight, correct front brake/ABS ring, exhaust and proportions. Same adult rider from the approved reference, full-face helmet visor down, complete protective gear. [One action]. [One camera angle and movement]. [One lighting state]. Bike unobstructed, stable, in contact with the road. No wheelie, speeding, added logos, text or parts.

### Blocker card

পুরোনো SOP-র blocker card আর সমস্যার table যেমন ছিল তেমনই ব্যবহার করো।
