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
  5. 絵文字     数と位置(引き寄せ語の有無も、ここで見る)
  6. 重複       過去の投稿と近すぎないか(文字の一致)
  7. 一致       参考アカウントの原文との連続一致
  8. 主張の重複 直近N日で、言い方を変えて同じことを言っていないか
  9. マンネリ   同じ語・同じ締めを使い回していないか(その日と直近3日をまとめて見る)
"""
import sys, os, re, json, glob, runpy
from difflib import SequenceMatcher

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

# ───────── 設定(ジャンルごとに、ここだけ書き換える) ─────────
CONFIG = {
    # 1. テーマ語:どれか1つは本文に必要。無ければジャンルが消える
    'THEME_WORDS': ['夫', '夫婦', '旦那', '別居', '離婚', '結婚', '新婚'],
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

    # 8. 主張の重複:文字が違っても、同じことを言っていないか
    #    「1日7本は7つ違うことを言う」を、日をまたいで効かせるための検査。
    #    6の重複検査は文字の一致を見るので、言い方を変えた繰り返しは素通りする。
    'CLAIM_CONCEPTS': {
        '決める':   ['決め', '決ま'],
        '世界':     ['世界'],
        '今日の1日': ['今日', 'ただの1日', '1日やで', '1日やから', 'その日', '日も'],
        '夫の態度': ['態度', '機嫌', '冷た', '無視', '優しく', 'キツ', 'きつく',
                   '黙っ', 'そっけな', '返事', '怒っ', 'イラ'],
        '変わらない': ['変わってへん', '変わらへん', '消えへん', '変わらん', '崩さへん'],
        '前提': ['前提'],
        '我慢':     ['我慢', '耐え'],
        '証拠':     ['証拠', '確かめ', '確認'],
        # 2026-10-04追加:「顔色をうかがう」と「様子を見に行く」を
        # 別々の語として数えていたため、同じ日に3時間差で2回出ても素通りしていた。
        '夫を見にいく': ['顔色', '様子', '見に行', 'うかが', '反応を見'],
        '待つ':     ['待つ', '待っ', 'いつ変わる', 'いつになったら'],
        'がんばる': ['がんばる', 'がんばっ', '頑張', '力を抜'],
        '諦め':     ['諦め'],
        '比べる':   ['比べ', '羨まし', 'よその'],
        '大丈夫':   ['大丈夫', '安心'],
        '順番':     ['順番', '先に', 'あとから', 'そっちが先'],
    },
    # 9. マンネリ:同じ語を毎日使っていないか。
    #    8の主張重複は概念が3つ重なって初めて止まるので、
    #    「全部が決めるの話」のような一語の連投は素通りしていた(2026-09-30に発覚)。
    #    語を足すときの考え方:「決め」を減らしたら「叶」が5/7になった(2026-10-01)。
    #    1つ塞ぐと別の語に寄るので、核になりうる語は先に全部並べておく。
    #    同じ概念は配列にまとめて、合計で数える。
    #    「決め」と「決ま」を別々に数えていたため、合計5本でも素通りしていた(2026-10-02)。
    'MONOTONY_WORDS': [
        ['決め', '決ま', '決まっ'],      # 決める
        ['叶'],
        ['もう仲がいい', 'うちはもう仲がいい'],
        ['大丈夫', 'だいじょうぶ'],
        ['ええんよ', 'ええからね', 'ええやで'],
        ['からね'],
        ['世界'],
        ['前提'],
        ['許可'],
    ],
    'MONO_SAMEDAY_MAX': 4,      # その日7本のうち、同じ語を含んでよい本数
    'MONO_RECENT_DAYS': 3,      # 直近何日をまとめて見るか
    'MONO_RECENT_RATIO': 0.6,   # 直近の投稿のうち、同じ語を含んでよい割合
    'MONO_TAIL_LEN': 6,         # 締めの何字を「同じ締め」とみなすか
    'MONO_TAIL_MAX': 2,         # 直近で、同じ締めを使ってよい本数

    'CLAIM_WINDOW_DAYS': 7,     # 何日さかのぼって見るか
    'CLAIM_SHARED_MIN': 3,      # 概念がいくつ重なったら「同じことを言っている」とみなすか

    # 4. 型ごとの適正字数(実測から)
    'LEN_BY_TYPE': {
        '型4': (13, 35),    # 予言・一言断言。短いほど強い
        '型6': (39, 90),    # 対話
        '型5': (80, 130),   # 体験談(4要素)
        '型9': (70, 150),   # ハウツー(箇条書き・単発)。コアラの実測12本は71〜147字
        '型9a': (20, 55),   # ハウツー連投の1/2。ゆきぴーの実測は23〜50字
        '型9b': (70, 170),
        '型10': (90, 220),  # 告知投稿。コアラの実物(2026-10-04)は約180字
        '型11': (60, 140),  # フォロー誘導。運用者の自作(2026-10-05・3.90%)が約80字  # ハウツー連投の2/2
        '型12': (100, 200), # 読者の否定を❓で置く型。運用者の自作(2026-10-06・3.70%+フォロー1人)が約150字
        '型1': (30, 60),
        '型2': (40, 85),
        '型3': (40, 70),
    },
    'LEN_DEFAULT': (13, 130),

    # 5. 絵文字
    'EMOJI_MAX': 2,
    # 型12だけ上限が違う。原型が運用者の自作で、実測3.70%+フォロー1人を取った版が
    # 絵文字7個だった(2026-10-06)。コアラ由来の型ではないので、コアラの2個を当てない。
    'EMOJI_MAX_BY_TYPE': {'型12': 7},

    # 5b. 引き寄せ語:1つも無いと、ただの人生アドバイスになる
    #     このアカウントは「引き寄せ × 夫婦仲」。引き寄せが主。
    'CORE_WORDS': ['決め', '決ま', '叶', '宇宙', '世界', '設定', '許可', '前提'],

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

def claim_sig(text, cfg):
    """本文から「何を言っているか」の概念集合を取り出す。"""
    return frozenset(name for name, words in cfg.get('CLAIM_CONCEPTS', {}).items()
                     if any(w in text for w in words))


def check(body, typ, past, refs, cfg, day=None, past_dated=None):
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

    # 5b. 引き寄せ語
    #     対話型は「宇宙「」」が話者名なので、そのままだと必ず通ってしまう。
    #     話者名を取り除いてから判定する(2026-09-30に素通りが見つかった)。
    core_probe = re.sub(r'宇宙\s*(?=[「『])', '', flat)
    if cfg.get('CORE_WORDS') and not any(w in core_probe for w in cfg['CORE_WORDS']):
        ng.append(('引き寄せ', '引き寄せ語(%s)が1つも無い。一般的な人生アドバイスになっている'
                   % '/'.join(cfg['CORE_WORDS'][:4])))

    # 5. 絵文字
    n = len(EMOJI.findall(flat))
    emax = cfg.get('EMOJI_MAX_BY_TYPE', {}).get(typ, cfg["EMOJI_MAX"])
    if n > emax:
        ng.append(('絵文字', '%d個。%d個まで' % (n, emax)))

    # 6. 重複
    for p in past:
        r = SequenceMatcher(None, flat, p.replace('\n', '')).ratio()
        if r >= cfg['DUP_RATIO']:
            ng.append(('重複', '過去投稿と%.0f%%一致: %s' % (r*100, p.replace('\n','/')[:28])))
            break

    # 8. 主張の重複(日付が分かるときだけ)
    if day and past_dated and cfg.get('CLAIM_CONCEPTS'):
        import datetime
        try:
            d0 = datetime.date.fromisoformat(day)
        except ValueError:
            d0 = None
        if d0:
            sig = claim_sig(flat, cfg)
            win = cfg.get('CLAIM_WINDOW_DAYS', 7)
            need = cfg.get('CLAIM_SHARED_MIN', 3)
            best = None
            for pd, pb in past_dated:
                try:
                    d1 = datetime.date.fromisoformat(pd)
                except ValueError:
                    continue
                if not (0 < (d0 - d1).days <= win):
                    continue
                shared = sig & claim_sig(pb.replace('\n', ''), cfg)
                if len(shared) >= need and (best is None or len(shared) > len(best[0])):
                    best = (shared, pd, pb)
            if best:
                shared, pd, pb = best
                ng.append(('主張重複',
                           '%s に同じことを言っている(%s): %s'
                           % (pd, '+'.join(sorted(shared)), pb.replace('\n', '/')[:26])))

    # 7. 参考アカウントとの一致
    sz, frag = 0, ''
    for t in refs:
        m = max(SequenceMatcher(None, flat, t).get_matching_blocks(), key=lambda x: x.size)
        if m.size > sz: sz, frag = m.size, flat[m.a:m.a+m.size]
    if sz >= cfg['REF_MAX_MATCH']:
        ng.append(('一致', '参考アカウントと%d字連続一致「%s」' % (sz, frag)))

    return ng, len(flat), sz

def monotony(rows, past_dated, cfg, day):
    """その日の7本と直近N日をまとめて見る。1本ごとではなく、束の性質を見る検査。"""
    import datetime
    from collections import Counter
    out = []
    # 連投(型9a + 型9b)は1投稿として数える。2本に割っただけで
    # 語の出現本数が増えてしまうため(2026-10-03)。
    bodies = []
    for _, _, ty, b in rows:
        flat = b.replace('\n', '')
        if ty.endswith('b') and bodies:
            bodies[-1] += flat
        else:
            bodies.append(flat)
    if not bodies:
        return out

    def _grp(w):
        """監視語は文字列でも配列でもよい。配列は同じ概念としてまとめて数える。"""
        return [w] if isinstance(w, str) else list(w)

    # (a) その日の中での連投
    for w in cfg.get('MONOTONY_WORDS', []):
        g = _grp(w)
        n = sum(1 for b in bodies if any(x in b for x in g))
        if n > cfg['MONO_SAMEDAY_MAX']:
            out.append('「%s」が%d本中%d本。同じ日に%d本まで'
                       % ('/'.join(g), len(bodies), n, cfg['MONO_SAMEDAY_MAX']))

    try:
        d0 = datetime.date.fromisoformat(day)
    except (ValueError, TypeError):
        return out

    win = cfg.get('MONO_RECENT_DAYS', 3)
    recent = [b.replace('\n', '') for pd, b in past_dated
              if _within(pd, d0, win)] + bodies
    if len(recent) < 7:
        return out

    # (b) 直近N日での出現率
    for w in cfg.get('MONOTONY_WORDS', []):
        g = _grp(w)
        n = sum(1 for b in recent if any(x in b for x in g))
        r = n / len(recent)
        if r > cfg['MONO_RECENT_RATIO']:
            out.append('「%s」が直近%d日の%d本中%d本(%.0f%%)。%.0f%%まで'
                       % ('/'.join(g), win, len(recent), n, r*100, cfg['MONO_RECENT_RATIO']*100))

    # (c) 同じ締め
    tl = cfg.get('MONO_TAIL_LEN', 6)
    c = Counter(b.strip()[-tl:] for b in recent)
    for tail, n in c.most_common(3):
        if n > cfg.get('MONO_TAIL_MAX', 2):
            out.append('締めが「…%s」の投稿が直近%d日で%d本。%d本まで'
                       % (tail, win, n, cfg['MONO_TAIL_MAX']))
    return out


def _within(pd, d0, win):
    import datetime
    try:
        d1 = datetime.date.fromisoformat(pd)
    except ValueError:
        return False
    return 0 < (d0 - d1).days <= win


def main():
    cfg = CONFIG
    refs = load_refs()
    if sys.argv[1] == '--text':
        rows = [('-', '-', '型4', sys.argv[2])]
        past, past_dated = [], []
    else:
        posts = load_posts(sys.argv[1])
        day = sys.argv[2] if len(sys.argv) > 2 else None
        rows = [(d, tm, ty, b) for d, tm, ty, th, ko, b in posts if not day or d == day]
        past = [b for d, tm, ty, th, ko, b in posts if not day or d != day]
        past_dated = [(d, b) for d, tm, ty, th, ko, b in posts if not day or d != day]

    bad = 0
    print('%-11s %-6s %-5s %5s %5s  %s' % ('日付','時刻','型','字数','一致','判定'))
    print('-'*78)
    for d, tm, ty, b in rows:
        ng, ln, sz = check(b, ty, past, refs, cfg, day=d if d != '-' else None,
                           past_dated=past_dated)
        print('%-11s %-6s %-5s %5d %4d字  %s' % (d, tm, ty, ln, sz, 'OK' if not ng else '✕ %d件' % len(ng)))
        for cat, msg in ng:
            print('%31s[%s] %s' % ('', cat, msg))
            bad += 1
    print('-'*78)

    # 9. マンネリ(その日の束としての検査)
    day_id = rows[0][0] if rows and rows[0][0] != '-' else None
    mono = monotony(rows, past_dated, cfg, day_id) if day_id else []
    for msg in mono:
        print('  [マンネリ] %s' % msg)
        bad += 1
    if mono:
        print('-'*78)

    print('問題 %d件' % bad)
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main())
