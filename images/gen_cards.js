// 有料note用 章扉画像ジェネレータ
// 使い方: node images/gen_cards.js   → images/out/*.png (1280x720)
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const OUT = path.join(__dirname, 'out');
const FONTS = path.join(__dirname, 'fonts');
fs.mkdirSync(OUT, { recursive: true });

const CARDS = [
  { file: '00_はじめに', step: null, label: 'はじめに',
    title: 'その前に、\nゆるいお願いを3つだけ', keyword: 'がんばらないこと', emoji: '🦥' },
  { file: '01_step1', step: 1,
    title: 'どんなにギスギスしてても\n効く、ひとこと', keyword: '「でも良くなってる」', emoji: '🌿' },
  { file: '02_step2', step: 2,
    title: '「仲のいい夫婦」を\n体に覚えさせる', keyword: '3つのだったらゲーム', emoji: '🦥' },
  { file: '03_step3', step: 3,
    title: '冷たい現実を、\n先に変える', keyword: 'もう仲がいい証拠集め', emoji: '🌿' },
  { file: '04_step4', step: 4,
    title: 'なぜか\n優しくされ始める', keyword: '「もう仲良し夫婦ごっこ」', emoji: '🦥' },
  { file: '05_step5', step: 5,
    title: 'しがみつきが、\nゆるゆるほどける', keyword: '手放しのワーク', emoji: '🌿' },
  { file: '06_step6', step: 6,
    title: '小さなサインを、\n良くなるにつなげる', keyword: '10秒の「お、きた」', emoji: '🦥' },
  { file: '07_step7', step: 7,
    title: '一瞬で「もう仲がいい私」に\n切り替わる', keyword: '「まあ、いっかぁ〜」', emoji: '🌿' },
];

const html = (c) => `<!doctype html><html><head><meta charset="utf-8"><style>
  @font-face { font-family:"ZenMaru"; font-weight:400;
    src:url("file://${FONTS}/ZenMaruGothic-Regular.ttf") format("truetype"); }
  @font-face { font-family:"ZenMaru"; font-weight:700;
    src:url("file://${FONTS}/ZenMaruGothic-Bold.ttf") format("truetype"); }
  * { margin:0; padding:0; box-sizing:border-box; }
  html,body { width:1280px; height:720px; overflow:hidden; }
  body {
    display:flex; align-items:center; justify-content:center;
    font-family:"ZenMaru","IPAPGothic",sans-serif;
    background:#FBF8F1; position:relative;
  }
  .blob { position:absolute; border-radius:50%; }
  .b1 { width:460px; height:460px; background:#EBF2E6; top:-170px; right:-130px; }
  .b2 { width:320px; height:320px; background:#F5EFE2; bottom:-130px; left:-100px; }
  .b3 { width:150px; height:150px; background:#F2F6EF; bottom:70px; right:110px; }
  .brand {
    position:absolute; top:58px; left:76px; font-size:24px; letter-spacing:.16em;
    color:#B0A894; font-weight:400;
  }
  .emoji { position:absolute; top:48px; right:76px; font-size:60px; }
  .inner { display:flex; flex-direction:column; align-items:center; z-index:1; }
  .step { display:flex; align-items:baseline; gap:20px; margin-bottom:40px; }
  .step .lbl { font-size:29px; letter-spacing:.26em; color:#9EB894; font-weight:700; }
  .step .num { font-size:112px; line-height:.82; color:#7A9A6E; font-weight:700; }
  .only { font-size:44px; color:#7A9A6E; letter-spacing:.14em; margin-bottom:40px; font-weight:700; }
  .title {
    font-size:58px; line-height:1.6; text-align:center; color:#3F3C36;
    white-space:pre-line; font-weight:700; letter-spacing:.02em;
  }
  .kw {
    margin-top:56px; padding:24px 56px; border-radius:999px;
    background:#EAF1E5; color:#5A7751; font-size:38px; letter-spacing:.05em; font-weight:700;
  }
</style></head><body>
  <div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>
  <div class="brand">のほほん夫婦仲引き寄せ</div>
  <div class="emoji">${c.emoji}</div>
  <div class="inner">
    ${c.step === null
      ? `<div class="only">${c.label}</div>`
      : `<div class="step"><span class="lbl">STEP</span><span class="num">${c.step}</span></div>`}
    <div class="title">${c.title}</div>
    <div class="kw">${c.keyword}</div>
  </div>
</body></html>`;

const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
for (const c of CARDS) {
  const tmp = `/tmp/card_${c.file}.html`;
  fs.writeFileSync(tmp, html(c));
  execSync(`"${CHROME}" --headless --no-sandbox --disable-gpu --hide-scrollbars ` +
    `--force-device-scale-factor=2 --window-size=1280,720 --default-background-color=00000000 ` +
    `--virtual-time-budget=3000 --screenshot="${OUT}/${c.file}.png" "file://${tmp}" 2>/dev/null`);
  console.log('✓', c.file + '.png');
}
