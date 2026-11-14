// Renders the TV screens and the end-card text as PNG files (Chromium does the Bangla shaping).
// Usage: node make_assets.mjs   (needs the 'playwright' package; set NODE_PATH if it is installed globally)
import { createRequire } from 'module';
const { chromium } = createRequire(import.meta.url)('playwright');
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
const here = path.dirname(fileURLToPath(import.meta.url));
const preview = fs.readFileSync(path.join(here, 'textures', 'preview.png')).toString('base64');
const f = n => 'file://' + path.join(here, 'fonts', n);
const fonts = `
@font-face{font-family:Inter;font-weight:800;src:url(${f('inter-latin-800-normal.woff2')})}
@font-face{font-family:Inter;font-weight:500;src:url(${f('inter-latin-500-normal.woff2')})}
@font-face{font-family:Hind;font-weight:700;src:url(${f('hind-siliguri-bengali-700-normal.woff2')})}
@font-face{font-family:Hind;font-weight:700;src:url(${f('hind-siliguri-latin-700-normal.woff2')});unicode-range:U+0000-00FF}
*{margin:0;box-sizing:border-box}`;
const tv = (pct, title) => `<style>${fonts}
body{width:1280px;height:720px;background:radial-gradient(120% 140% at 20% 30%,#17306e 0%,#0a1438 55%,#050a1f 100%);
 font-family:Inter;color:#fff;overflow:hidden;position:relative}
.label{position:absolute;left:64px;top:52px;font:500 26px Inter;letter-spacing:8px;color:#8fb6ff}
.title{position:absolute;left:60px;top:88px;font:800 ${title.length > 8 ? 78 : 118}px Inter;letter-spacing:2px}
.pct{position:absolute;left:52px;top:236px;font:800 300px/1 Inter;color:#e9f6ff;text-shadow:0 0 60px #2f7dff}
.pct small{font-size:150px}
.bar{position:absolute;left:64px;right:64px;bottom:92px;height:26px;border-radius:13px;background:#ffffff26}
.bar i{display:block;height:100%;width:${pct}%;min-width:26px;border-radius:13px;background:#35d0ff;box-shadow:0 0 30px #35d0ff}
.left{position:absolute;left:64px;bottom:38px;font:500 30px Inter;color:#b9c8ee}
.prev{position:absolute;right:64px;top:64px;width:520px;height:430px;border-radius:22px;overflow:hidden;
 box-shadow:0 0 0 3px #ffffff40,0 20px 60px #000a}
.prev img{width:100%;height:100%;object-fit:cover}
.tag{position:absolute;right:64px;top:510px;width:520px;text-align:right;font:500 22px Inter;letter-spacing:6px;color:#8fb6ff}
</style><div class=label>DOWNLOADING</div><div class=title>${title}</div>
<div class=pct>${pct}<small>%</small></div><div class=bar><i></i></div>
<div class=left>About ${pct == 3 ? '14 hours' : '13 hours 58 min'} left</div>
<div class=prev><img src="data:image/png;base64,${preview}"></div><div class=tag>PREVIEW</div>`;
const tagline = `<style>${fonts}body{width:1000px;height:300px;background:transparent}
.t{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
 font:700 86px Hind;color:#fff;text-shadow:0 4px 30px #000c,0 0 2px #000;white-space:nowrap}
.t b{font:800 78px Inter;margin-right:18px;color:#35d0ff}</style>
<div class=t><b>Map</b>লোড হয় চাকার নিচে।</div>`;
const model = `<style>${fonts}body{width:1000px;height:120px;background:transparent}
.t{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
 font:500 34px Inter;letter-spacing:10px;color:#fffc;text-shadow:0 2px 16px #000c}</style>
<div class=t>MT-15 V2 · CYAN STORM</div>`;
const logo = `<style>${fonts}body{width:520px;height:150px;background:transparent}
.t{position:absolute;inset:10px;border:3px dashed #ffffffb0;border-radius:14px;display:flex;flex-direction:column;
 align-items:center;justify-content:center;font:800 34px Inter;letter-spacing:6px;color:#ffffffd0}
.t small{font:500 17px Inter;letter-spacing:2px;margin-top:6px}</style>
<div class=t>YAMAHA LOGO<small>placeholder: official file goes here</small></div>`;
const b = await chromium.launch();
const shot = async (html, w, h, name, transparent) => {
  const p = await b.newPage({ viewport: { width: w, height: h } });
  await p.setContent(html, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(here, 'textures', name), omitBackground: !!transparent });
  await p.close();
};
for (const pct of [3, 4]) {
  await shot(tv(pct, 'GTA VI'), 1280, 720, `tv_${pct}_named.png`);
  await shot(tv(pct, 'NEW GAME'), 1280, 720, `tv_${pct}_clean.png`);
}
await shot(tagline, 1000, 300, 'tagline.png', true);
await shot(model, 1000, 120, 'model_line.png', true);
await shot(logo, 520, 150, 'logo_placeholder.png', true);
await b.close();
console.log('assets done');
