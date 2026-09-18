// 有料note用 解説図ジェネレータ
// 使い方: TRIM_PY=<python> node images/gen_figures.js  → images/out/fig*.png
// 方針: 図の「位置・高さ・距離」そのものに意味を持たせる。文字は最小限。
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const OUT = path.join(__dirname, 'out');
const FONTS = path.join(__dirname, 'fonts');
fs.mkdirSync(OUT, { recursive: true });

const C = { cream:'#FBF8F1', ink:'#3F3C36', mute:'#8C8474',
            g:'#7A9A6E', gBg:'#E3EEDD', gLine:'#C6DABC',
            r:'#C08163', rBg:'#F3E2DA', rLine:'#E4C3B4', line:'#DCD4C2' };

const BASE = `
  @font-face { font-family:"ZenMaru"; font-weight:400;
    src:url("file://${FONTS}/ZenMaruGothic-Regular.ttf") format("truetype"); }
  @font-face { font-family:"ZenMaru"; font-weight:700;
    src:url("file://${FONTS}/ZenMaruGothic-Bold.ttf") format("truetype"); }
  * { margin:0; padding:0; box-sizing:border-box; }
  html,body { width:1280px; height:auto; overflow:hidden; }
  body { font-family:"ZenMaru",sans-serif; background:${C.cream}; color:${C.ink};
         padding:60px 64px 48px; }
  h1 { font-size:44px; font-weight:700; margin-bottom:10px; }
  .sub { font-size:24px; color:${C.mute}; letter-spacing:.16em; margin-bottom:12px; }
  .cap { font-size:30px; color:${C.mute}; line-height:1.65; margin-top:34px; }
  svg { display:block; width:100%; height:auto; }
  .t  { font-family:"ZenMaru",sans-serif; }
`;

const FIGS = [

// ── fig1 時差 : 横軸＝時間。否定が飛んでくる位置を示す ──────────────
{ file:'fig1_時差', sub:'ステップ1 ── 時差', title:'否定が飛んでくるのは、ここだけ',
  svg:`<svg viewBox="0 0 1152 470" xmlns="http://www.w3.org/2000/svg">
  <text class="t" x="0" y="34" font-size="27" fill="${C.mute}">お金の引き寄せ</text>
  <rect x="0" y="62" width="184" height="76" rx="22" fill="${C.gBg}"/>
  <text class="t" x="92" y="112" font-size="31" font-weight="700" fill="${C.g}" text-anchor="middle">決めた</text>
  <line x1="196" y1="100" x2="944" y2="100" stroke="${C.line}" stroke-width="7" stroke-linecap="round"/>
  <text class="t" x="570" y="76" font-size="26" fill="${C.mute}" text-anchor="middle">ずっと静か</text>
  <rect x="956" y="62" width="196" height="76" rx="22" fill="${C.gBg}"/>
  <text class="t" x="1054" y="112" font-size="31" font-weight="700" fill="${C.g}" text-anchor="middle">叶う</text>

  <text class="t" x="0" y="258" font-size="27" fill="${C.mute}">夫婦仲の引き寄せ</text>
  <rect x="0" y="286" width="184" height="76" rx="22" fill="${C.gBg}"/>
  <text class="t" x="92" y="336" font-size="31" font-weight="700" fill="${C.g}" text-anchor="middle">決めた</text>
  <line x1="196" y1="324" x2="944" y2="324" stroke="${C.rLine}" stroke-width="7" stroke-linecap="round"/>
  <rect x="956" y="286" width="196" height="76" rx="22" fill="${C.gBg}"/>
  <text class="t" x="1054" y="336" font-size="31" font-weight="700" fill="${C.g}" text-anchor="middle">良くなる</text>
  ${[330,500,670,840].map(x=>`
  <line x1="${x}" y1="252" x2="${x}" y2="306" stroke="${C.r}" stroke-width="6" stroke-linecap="round"/>
  <path d="M${x-13} 294 L${x} 316 L${x+13} 294 Z" fill="${C.r}"/>`).join('')}
  <text class="t" x="585" y="230" font-size="27" fill="${C.r}" text-anchor="middle">「は? また同じこと言ってる」</text>
  <path d="M196 396 L944 396" stroke="${C.rLine}" stroke-width="3" stroke-dasharray="10 10"/>
  <path d="M196 380 L196 412 M944 380 L944 412" stroke="${C.rLine}" stroke-width="3"/>
  <text class="t" x="570" y="450" font-size="29" font-weight="700" fill="${C.r}" text-anchor="middle">ここで下ろすと、ふりだし</text>
  </svg>`,
  cap:'お金の引き寄せは、時差のあいだ何も起きない。<br>夫婦仲だけが、時差のあいだに否定が返ってくるんだよ〜🦥' },

// ── fig2 手放す : ひとつの塊が2つに割れる ────────────────────────
{ file:'fig2_手放す', sub:'ステップ5 ── 手放す', title:'ふたつを、分ける',
  svg:`<svg viewBox="0 0 1152 560" xmlns="http://www.w3.org/2000/svg">
  <rect x="216" y="0" width="720" height="122" rx="34" fill="#FFFDF8" stroke="${C.line}" stroke-width="3"/>
  <text class="t" x="576" y="52" font-size="26" fill="${C.mute}" text-anchor="middle">ぜんぶ一緒に、握りしめてる</text>
  <text class="t" x="576" y="96" font-size="31" font-weight="700" fill="${C.ink}" text-anchor="middle">仲良くなりたい ＋ 変わってくれなきゃ困る</text>

  <path d="M576 130 L576 168" stroke="${C.line}" stroke-width="5" stroke-linecap="round"/>
  <path d="M576 168 L300 168 M576 168 L852 168" stroke="${C.line}" stroke-width="5" stroke-linecap="round"/>
  <path d="M300 168 L300 206 M852 168 L852 206" stroke="${C.line}" stroke-width="5" stroke-linecap="round"/>
  <path d="M287 194 L300 218 L313 194 Z" fill="${C.line}"/>
  <path d="M839 194 L852 218 L865 194 Z" fill="${C.line}"/>

  <rect x="36" y="232" width="528" height="228" rx="34" fill="${C.gBg}" stroke="${C.gLine}" stroke-width="3"/>
  <text class="t" x="300" y="300" font-size="27" fill="${C.g}" text-anchor="middle">望み</text>
  <text class="t" x="300" y="360" font-size="38" font-weight="700" fill="${C.ink}" text-anchor="middle">「仲良くなりたい」</text>
  <text class="t" x="300" y="420" font-size="30" font-weight="700" fill="${C.g}" text-anchor="middle">◯ 握ってていい</text>

  <rect x="588" y="232" width="528" height="228" rx="34" fill="${C.rBg}" stroke="${C.rLine}" stroke-width="3" opacity=".75"/>
  <text class="t" x="852" y="300" font-size="27" fill="${C.r}" text-anchor="middle">条件</text>
  <text class="t" x="852" y="352" font-size="32" font-weight="700" fill="${C.ink}" text-anchor="middle" opacity=".7">「変わってくれなきゃ、</text>
  <text class="t" x="852" y="396" font-size="32" font-weight="700" fill="${C.ink}" text-anchor="middle" opacity=".7">わたしは幸せになれない」</text>
  <text class="t" x="852" y="444" font-size="30" font-weight="700" fill="${C.r}" text-anchor="middle">✕ これだけ外す</text>

  <text class="t" x="576" y="530" font-size="31" font-weight="700" fill="${C.ink}" text-anchor="middle">手放す ＝ 諦める、じゃないよ🌿</text>
  </svg>`,
  cap:'望みは残していいの。外すのは「それがないと不幸」のほうだけ。' },

// ── fig3 証拠のハードル : 高さそのものが意味 ──────────────────────
{ file:'fig3_証拠のハードル', sub:'ステップ3 ── 証拠のハードル', title:'ハードルを、下げるだけ',
  svg:`<svg viewBox="0 0 1152 470" xmlns="http://www.w3.org/2000/svg">
  <line x1="0" y1="390" x2="1152" y2="390" stroke="${C.line}" stroke-width="6" stroke-linecap="round"/>

  <line x1="330" y1="390" x2="330" y2="96" stroke="${C.rLine}" stroke-width="9" stroke-linecap="round"/>
  <line x1="470" y1="390" x2="470" y2="96" stroke="${C.rLine}" stroke-width="9" stroke-linecap="round"/>
  <rect x="306" y="80" width="188" height="24" rx="12" fill="${C.r}"/>
  <text class="t" x="400" y="52" font-size="31" font-weight="700" fill="${C.r}" text-anchor="middle">「愛されてる証拠」</text>
  <text class="t" x="400" y="440" font-size="28" fill="${C.r}" text-anchor="middle">✕ 高すぎて、見つからない</text>

  <line x1="790" y1="390" x2="790" y2="300" stroke="${C.gLine}" stroke-width="9" stroke-linecap="round"/>
  <line x1="930" y1="390" x2="930" y2="300" stroke="${C.gLine}" stroke-width="9" stroke-linecap="round"/>
  <rect x="766" y="284" width="188" height="24" rx="12" fill="${C.g}"/>
  <text class="t" x="860" y="230" font-size="31" font-weight="700" fill="${C.g}" text-anchor="middle">「わたしのほうを</text>
  <text class="t" x="860" y="268" font-size="31" font-weight="700" fill="${C.g}" text-anchor="middle">向いた瞬間」</text>
  <text class="t" x="860" y="440" font-size="28" fill="${C.g}" text-anchor="middle">◯ 毎日どこかにある</text>

  <text x="84" y="382" font-size="62">🦥</text>
  <path d="M176 360 L246 360" stroke="${C.mute}" stroke-width="5" stroke-linecap="round"/>
  <path d="M232 348 L252 360 L232 372 Z" fill="${C.mute}"/>
  </svg>`,
  cap:'「ありがとう」も言われてないのに、愛されてる証拠は、そりゃ探せないよ〜<br>一瞬こっちを向いた、それだけで証拠にしちゃお🦥' },

// ── fig4 だったら : ゴールとの「距離」が意味 ──────────────────────
{ file:'fig4_だったら', sub:'ステップ2 ── だったらゲーム', title:'外から願うか、中から見るか',
  svg:`<svg viewBox="0 0 1152 576" xmlns="http://www.w3.org/2000/svg">
  <text class="t" x="0" y="30" font-size="27" fill="${C.r}">いままで</text>
  <circle cx="820" cy="150" r="118" fill="none" stroke="${C.rLine}" stroke-width="5" stroke-dasharray="14 12"/>
  <text class="t" x="820" y="140" font-size="27" fill="${C.r}" text-anchor="middle">仲のいい</text>
  <text class="t" x="820" y="176" font-size="27" fill="${C.r}" text-anchor="middle">夫婦</text>
  <circle cx="150" cy="150" r="34" fill="${C.rBg}" stroke="${C.rLine}" stroke-width="4"/>
  <text class="t" x="150" y="160" font-size="25" fill="${C.r}" text-anchor="middle">私</text>
  <path d="M200 150 L672 150" stroke="${C.rLine}" stroke-width="5" stroke-dasharray="14 12"/>
  <path d="M658 136 L690 150 L658 164 Z" fill="${C.rLine}"/>
  <text class="t" x="350" y="122" font-size="31" font-weight="700" fill="${C.ink}" text-anchor="middle">「仲良くなれますように」</text>
  <text class="t" x="350" y="212" font-size="27" fill="${C.r}" text-anchor="middle">外にいるから、距離が縮まらない</text>

  <line x1="0" y1="282" x2="1152" y2="282" stroke="${C.line}" stroke-width="3" stroke-dasharray="10 10"/>

  <text class="t" x="0" y="344" font-size="27" fill="${C.g}">これから</text>
  <circle cx="820" cy="430" r="118" fill="${C.gBg}" stroke="${C.gLine}" stroke-width="5"/>
  <text class="t" x="820" y="392" font-size="27" fill="${C.g}" text-anchor="middle">仲のいい夫婦</text>
  <circle cx="820" cy="452" r="34" fill="#FFFDF8" stroke="${C.g}" stroke-width="4"/>
  <text class="t" x="820" y="462" font-size="25" fill="${C.g}" text-anchor="middle">私</text>
  <text class="t" x="400" y="416" font-size="31" font-weight="700" fill="${C.ink}" text-anchor="middle">「もう仲のいい夫婦だったら、</text>
  <text class="t" x="400" y="458" font-size="31" font-weight="700" fill="${C.ink}" text-anchor="middle">今どうしてる?」</text>
  <text class="t" x="400" y="510" font-size="27" fill="${C.g}" text-anchor="middle">もう中にいるから、距離がない</text>
  </svg>`,
  cap:'「なれますように」は、まだ持ってない人の言葉。<br>「だったら」は、もう持ってる人の言葉なんだよ〜🦥' },
];

const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
for (const f of FIGS) {
  const doc = `<!doctype html><html><head><meta charset="utf-8"><style>${BASE}</style></head>
  <body><div class="sub">${f.sub}</div><h1>${f.title}</h1>
  <div style="height:28px"></div>${f.svg}<div class="cap">${f.cap}</div></body></html>`;
  const tmp = `/tmp/fig_${f.file}.html`;
  fs.writeFileSync(tmp, doc);
  execSync(`"${CHROME}" --headless --no-sandbox --disable-gpu --hide-scrollbars ` +
    `--force-device-scale-factor=2 --window-size=1280,2600 --virtual-time-budget=3000 ` +
    `--screenshot="${OUT}/${f.file}.png" "file://${tmp}" 2>/dev/null`);
  console.log('✓', f.file);
}
execSync(`${process.env.TRIM_PY || 'python3'} ${path.join(__dirname,'trim.py')} ${OUT}`,
  { stdio:'inherit' });
