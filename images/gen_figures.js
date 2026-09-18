// 有料note用 解説図ジェネレータ
// 使い方: node images/gen_figures.js   → images/out/fig_*.png
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const OUT = path.join(__dirname, 'out');
const FONTS = path.join(__dirname, 'fonts');
fs.mkdirSync(OUT, { recursive: true });

const BASE = `
  @font-face { font-family:"ZenMaru"; font-weight:400;
    src:url("file://${FONTS}/ZenMaruGothic-Regular.ttf") format("truetype"); }
  @font-face { font-family:"ZenMaru"; font-weight:700;
    src:url("file://${FONTS}/ZenMaruGothic-Bold.ttf") format("truetype"); }
  * { margin:0; padding:0; box-sizing:border-box; }
  html,body { width:1280px; overflow:hidden; }
  body { font-family:"ZenMaru",sans-serif; background:#FBF8F1; color:#3F3C36;
         padding:64px 72px; }
  h1 { font-size:46px; font-weight:700; margin-bottom:56px; letter-spacing:.02em; }
  h1 .sub { display:block; font-size:25px; color:#A79E8B; font-weight:400;
            letter-spacing:.16em; margin-bottom:14px; }
  .row { background:#FFFDF8; border:3px solid #E9E2D2; border-radius:32px;
         padding:38px 44px; margin-bottom:28px; }
  .row.ok { border-color:#C6DABC; background:#F6FAF4; }
  .row.ng { border-color:#E8D6CE; background:#FDF7F4; }
  .lead { font-size:28px; color:#8C8474; margin-bottom:20px; letter-spacing:.08em; }
  .big { font-size:44px; font-weight:700; line-height:1.5; }
  .note { font-size:30px; color:#6F6858; margin-top:18px; line-height:1.6; }
  .tag { display:inline-block; padding:10px 26px; border-radius:999px; font-size:26px;
         font-weight:700; margin-bottom:18px; }
  .tag.g { background:#E3EEDD; color:#5A7751; }
  .tag.r { background:#F3E2DA; color:#9A6B57; }
  .tag.n { background:#EDE7DA; color:#8A8271; }
`;

const FIGS = [
{ file:'fig1_時差', title:'決めたあと、現実が追いつくまで', sub:'ステップ1 ── 時差',
  body:`
  <div class="row">
    <div class="lead">お金の引き寄せ</div>
    <div class="tl">
      <span class="pt g">決めた</span>
      <span class="line"><span class="lbl">時差のあいだ、静か</span></span>
      <span class="pt g">叶う</span>
    </div>
  </div>
  <div class="row ng">
    <div class="lead">夫婦仲の引き寄せ</div>
    <div class="tl">
      <span class="pt g">決めた</span>
      <span class="line ng"><span class="lbl">「は? また同じこと言ってる」</span>
        <span class="x">✕</span><span class="x x2">✕</span></span>
      <span class="pt g">良くなる</span>
    </div>
    <div class="note">否定が返ってくるのは、この時差のあいだだけ。<br>
      ここで決めたことを下ろしちゃうと、ふりだしに戻るの。</div>
  </div>
  <div class="row">
    <div class="big">だから、折れないように<br>最初からゆるめておくの🦥</div>
  </div>`,
  css:`
   .tl { display:flex; align-items:center; gap:18px; }
   .pt { flex:0 0 auto; padding:18px 30px; border-radius:20px; font-size:32px; font-weight:700; }
   .pt.g { background:#E3EEDD; color:#4E6B46; }
   .line { flex:1; height:6px; background:#DCD4C2; border-radius:999px; position:relative; }
   .line.ng { background:#E4C3B4; }
   .lbl { position:absolute; left:50%; transform:translateX(-50%); top:-52px;
          white-space:nowrap; font-size:27px; color:#8C8474; }
   .x { position:absolute; top:-17px; left:32%; font-size:38px; color:#C98A6E; }
   .x2 { left:64%; }` },

{ file:'fig2_手放す', title:'手放すのは「条件」だけ', sub:'ステップ5 ── 手放す',
  body:`
  <div class="row ok">
    <span class="tag g">残していい</span>
    <div class="big">「仲良くなりたい」</div>
    <div class="note">望みのほう。これは握ってていいの。</div>
  </div>
  <div class="row ng">
    <span class="tag r">これだけ外す</span>
    <div class="big">「変わってくれなきゃ、<br>わたしは幸せになれない」</div>
    <div class="note">条件のほう。自分の幸せを、人に預けちゃってる状態だよ。</div>
  </div>
  <div class="row">
    <div class="big">手放す ＝ 諦める、じゃないよ🌿</div>
    <div class="note">望みは残して、条件だけ外す。これが「手放す」の意味。</div>
  </div>` },

{ file:'fig3_証拠のハードル', title:'探すものを、変えるだけ', sub:'ステップ3 ── 証拠のハードル',
  body:`
  <div class="row ng">
    <span class="tag r">高すぎる</span>
    <div class="big">「愛されてる証拠」</div>
    <div class="note">「ありがとう」も言われてないんだから、そりゃ見つからないよ…💤</div>
  </div>
  <div class="row ok">
    <span class="tag g">これでいい</span>
    <div class="big">「わたしのほうを向いた瞬間」</div>
    <div class="note">一瞬でいいの。愛じゃなくていい。こっちに意識が向いた、それだけ。</div>
  </div>
  <div class="row">
    <span class="tag n">たとえば</span>
    <ul class="ex">
      <li>「ごはんいる?」って聞いてきた</li>
      <li>お風呂、先に入れてくれてた</li>
      <li>買い物のついでに、なんか買ってきた</li>
      <li>自分の話を、こっちにしてきた</li>
    </ul>
    <div class="note">どれも、やらなくて困らないことでしょ。<br>
      やったってことは、一瞬でもあなたを考えたってことだよ🦥</div>
  </div>`,
  css:`.ex { list-style:none; } .ex li { font-size:33px; line-height:1.85; padding-left:38px;
        position:relative; } .ex li:before { content:"・"; position:absolute; left:6px; color:#9EB894; }` },

{ file:'fig4_だったら', title:'願うのを、やめるだけ', sub:'ステップ2 ── だったらゲーム',
  body:`
  <div class="row ng">
    <span class="tag r">まだ持ってない人の言葉</span>
    <div class="big">「仲良くなれますように」</div>
    <div class="note">願うほど「うちはまだ仲良くない」を毎回確認しちゃう。<br>
      だから、やればやるほどしんどくなるの…💤</div>
  </div>
  <div class="row ok">
    <span class="tag g">もう持ってる人の言葉</span>
    <div class="big">「もう仲のいい夫婦だったら、<br>今どうしてる?」</div>
    <div class="note">質問されると、脳が勝手に答えを探し始めるの。<br>
      意志がいらないから、疲れないよ🦥</div>
  </div>` },
];

const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
for (const f of FIGS) {
  const doc = `<!doctype html><html><head><meta charset="utf-8"><style>${BASE}${f.css||''}
    html,body{height:auto;min-height:0}</style></head><body>
    <h1><span class="sub">${f.sub}</span>${f.title}</h1>${f.body}
    <div style="height:1px"></div></body></html>`;
  const tmp = `/tmp/fig_${f.file}.html`;
  fs.writeFileSync(tmp, doc);
  // 余裕をもって高く描画 → 下の余白は trim.py が自動で切る
  execSync(`"${CHROME}" --headless --no-sandbox --disable-gpu --hide-scrollbars ` +
    `--force-device-scale-factor=2 --window-size=1280,2600 --virtual-time-budget=3000 ` +
    `--screenshot="${OUT}/${f.file}.png" "file://${tmp}" 2>/dev/null`);
  console.log('✓', f.file + '.png (trim前)');
}
// 下端の余白を自動で切り落とす
execSync(`${process.env.TRIM_PY || 'python3'} ${path.join(__dirname,'trim.py')} ${OUT}`,
  { stdio:'inherit' });
