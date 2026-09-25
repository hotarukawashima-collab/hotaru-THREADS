# -*- coding: utf-8 -*-
"""投稿を出す前の機械検査。すべての検査を1本にまとめたもの。

使い方:
    python3 tools/inspect.py contents/_posts35_source.py 2026-09-25
    python3 tools/inspect.py --text "投稿本文をそのまま"

検査:
  1. テーマ語   本文にテーマ語が入っているか(なければジャンルが消える)
  2. NG語       結果を保証する語・自己責任に落とす語
  3. 抽象語     中身の代わりに指し示す語を置いていないか
  4. 字数帯     型ごとの適正字数
  5. 絵文字     数と位置
  6. 重複       過去の投稿と近すぎないか
  7. 一致       参考アカウントの原文との連続一致
"""
import sys, os, re, json, glob, runpy
from difflib import SequenceMatcher

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

# ───────── 設定(ジャンルごとに、ここだけ書き換える) ─────────
CONFIG = {
    # 1. テーマ語:どれか1つは本文に必要。無ければジャンルが消える
    'THEME_WORDS': ['夫', '夫婦', '旦那'],
    'THEME_FALSE_POSITIVE': ['大丈夫'],   # 「夫」を含むが該当しない語

    # 2. NG語:結果を保証する / 悪化を本人のせいにする
    'NG_WORDS': {
        '絶対戻': '結果を保証している',
        '必ず戻': '結果を保証している',
        '絶対に元通り': '結果を保証している',
        '我慢して待': '危険なケースの滞在を延ばす',
        '離婚は逃げ': '離婚を否定している',
        'あなたの波動が': '関係悪化を本人のせいにしている',
        'あなたのせいで': '関係悪化を本人のせいにしている',
        'それはモラハラ': '投稿だけで診断できない',
    },

    # 3. 抽象語:中身の代わりに置かれがちな語。直前後に具体語が要る
    'VAGUE_WORDS': ['その中', 'それ', 'そこ', 'この状況', 'ちゃんとした',
                    '大きい', '本当の', '本質', 'ちゃんと向き合'],

    # 3b. 他人の行動・関係の結果を予言していないか
    #     予言していいのは「読者自身に起きること」まで。
    #     相手の行動や関係の結果を約束すると、外れたとき読者が自分を責める。
    'PROMISE_PATTERNS': [
        (r'夫[がは][^。\n]{0,12}(してくる|くれる|戻る|変わる)[^。\n]{0,6}(よ|日|から)',
         '夫の行動を約束している。読者自身に起きること(気づく/思う/感じる)にする'),
        (r'(夫婦仲|関係|二人)[^。\n]{0,10}(戻る|戻って|良くなる|元通り)',
         '関係の結果を約束している'),
        (r'ほど[^。\n]{0,10}(戻る|良くなる|うまくいく)',
         '「〜ほど良くなる」は根拠のない逆張り'),
    ],

    # 4. 型ごとの適正字数(実測から)
    'LEN_BY_TYPE': {
        '型4': (13, 35),    # 予言・一言断言。短いほど強い
        '型6': (39, 90),    # 対話
        '型5': (80, 130),   # 体験談(4要素)
        '型1': (30, 60),
        '型2': (40, 85),
        '型3': (40, 70),
    },
    'LEN_DEFAULT': (13, 130),

    # 5. 絵文字
    'EMOJI_MAX': 2,

    # 6/7. しきい値
    'DUP_RATIO': 0.62,      # 過去投稿との類似度
    'REF_MAX_MATCH': 20,    # 参考アカウントとの連続一致(字)
}
# ────────────────────────────────────────────────────

EMOJI = re.compile('[\U0001F300-\U0001FAFF☀-➿⬀-⯿]')

def load_refs():
    out = []
    for f in glob.glob(os.path.join(ROOT, 'analysis/accounts/*/posts.jsonl')):
        for line in open(f, encoding='utf-8'):
            try: d = json.loads(line)
            except Exception: continue
            t = (d.get('text') or '').replace('\n', '')
            if t: out.append(t)
    for f in glob.glob(os.path.join(ROOT, 'reference/*/*.txt')):
        out.append(re.sub(r'[\s　]', '', open(f, encoding='utf-8').read()))
    return out

def load_posts(path):
    ns = runpy.run_path(path)
    return ns['POSTS']

def check(body, typ, past, refs, cfg):
    flat = body.replace('\n', '')
    ng = []

    # 1. テーマ語
    probe = flat
    for fp in cfg['THEME_FALSE_POSITIVE']:
        probe = probe.replace(fp, '')
    if not any(w in probe for w in cfg['THEME_WORDS']):
        ng.append(('テーマ語', 'テーマ語(%s)が本文に無い' % '/'.join(cfg['THEME_WORDS'])))

    # 2. NG語
    for w, why in cfg['NG_WORDS'].items():
        if w in flat:
            ng.append(('NG語', '「%s」%s' % (w, why)))

    # 3b. 他人の行動・関係の結果の予言
    for pat, why in cfg.get('PROMISE_PATTERNS', []):
        m = re.search(pat, flat)
        if m:
            ng.append(('予言', '「%s」%s' % (m.group(0)[:20], why)))

    # 3. 抽象語(その語の前後10字に、かぎ括弧や固有の名詞が無ければ疑う)
    for w in cfg['VAGUE_WORDS']:
        for m in re.finditer(re.escape(w), flat):
            around = flat[max(0, m.start()-12):m.end()+12]
            if not re.search(r'[「」]', around):
                ng.append(('抽象語', '「%s」の中身が近くに書かれていない' % w))
            break

    # 4. 字数
    lo, hi = cfg['LEN_BY_TYPE'].get(typ, cfg['LEN_DEFAULT'])
    if not (lo <= len(flat) <= hi):
        ng.append(('字数', '%d字。%sの適正は%d〜%d字' % (len(flat), typ, lo, hi)))

    # 5. 絵文字
    n = len(EMOJI.findall(flat))
    if n > cfg['EMOJI_MAX']:
        ng.append(('絵文字', '%d個。%d個まで' % (n, cfg['EMOJI_MAX'])))

    # 6. 重複
    for p in past:
        r = SequenceMatcher(None, flat, p.replace('\n', '')).ratio()
        if r >= cfg['DUP_RATIO']:
            ng.append(('重複', '過去投稿と%.0f%%一致: %s' % (r*100, p.replace('\n','/')[:28])))
            break

    # 7. 参考アカウントとの一致
    sz, frag = 0, ''
    for t in refs:
        m = max(SequenceMatcher(None, flat, t).get_matching_blocks(), key=lambda x: x.size)
        if m.size > sz: sz, frag = m.size, flat[m.a:m.a+m.size]
    if sz >= cfg['REF_MAX_MATCH']:
        ng.append(('一致', '参考アカウントと%d字連続一致「%s」' % (sz, frag)))

    return ng, len(flat), sz

def main():
    cfg = CONFIG
    refs = load_refs()
    if sys.argv[1] == '--text':
        rows = [('-', '-', '型4', sys.argv[2])]
        past = []
    else:
        posts = load_posts(sys.argv[1])
        day = sys.argv[2] if len(sys.argv) > 2 else None
        rows = [(d, tm, ty, b) for d, tm, ty, th, ko, b in posts if not day or d == day]
        past = [b for d, tm, ty, th, ko, b in posts if not day or d != day]

    bad = 0
    print('%-11s %-6s %-5s %5s %5s  %s' % ('日付','時刻','型','字数','一致','判定'))
    print('-'*78)
    for d, tm, ty, b in rows:
        ng, ln, sz = check(b, ty, past, refs, cfg)
        print('%-11s %-6s %-5s %5d %4d字  %s' % (d, tm, ty, ln, sz, 'OK' if not ng else '✕ %d件' % len(ng)))
        for cat, msg in ng:
            print('%31s[%s] %s' % ('', cat, msg))
            bad += 1
    print('-'*78)
    print('問題 %d件' % bad)
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main())
