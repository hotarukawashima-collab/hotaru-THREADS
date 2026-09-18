# -*- coding: utf-8 -*-
"""コアラの原文と、自分の書いた文章の一致箇所を検出する。

使い方:
    python3 tools/check_similarity.py <自分のファイル> [しきい値]

しきい値(既定12)は「何文字以上の連続一致を報告するか」。
コアラのPDFから抽出したテキストを reference/ に置いておくこと。
"""
import sys, os, re, glob
from difflib import SequenceMatcher

REF_DIR = os.path.join(os.path.dirname(__file__), '..', 'reference', 'koara')

def norm(t):
    t = re.sub(r'【.*?】', '', t)          # 見出しマーカーを除く
    t = re.sub(r'▼▼▼.*?▼▼▼', '', t)      # 画像マーカーを除く
    return re.sub(r'[\s　]', '', t)

def main():
    if len(sys.argv) < 2:
        print(__doc__); return 1
    target = sys.argv[1]
    th = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    mine = norm(open(target, encoding='utf-8').read())
    refs = sorted(glob.glob(os.path.join(REF_DIR, '*.txt')))
    if not refs:
        print(f'参照テキストが無い: {REF_DIR}'); return 1

    hits = []
    for r in refs:
        kt = norm(open(r, encoding='utf-8').read())
        for b in SequenceMatcher(None, kt, mine, autojunk=False).get_matching_blocks():
            seg = kt[b.a:b.a + b.size]
            # 日本語を含む一致だけを見る(記号の羅列や英数字は除く)
            if b.size >= th and re.search(r'[ぁ-んァ-ヶ一-龥]', seg):
                hits.append((b.size, os.path.basename(r), seg))

    total = sum(h[0] for h in hits)
    print(f'{os.path.basename(target)}  本文{len(mine)}字')
    print(f'{th}文字以上の連続一致: {len(hits)}箇所 / 合計{total}字 '
          f'({total/len(mine)*100:.1f}%) 最長{max([h[0] for h in hits], default=0)}字\n')
    for size, src, seg in sorted(hits, reverse=True):
        print(f'  {size}字 <- {src}: {seg}')

    # 判定
    print()
    if not hits:
        print('判定: OK(一致なし)')
    elif max(h[0] for h in hits) >= 20 or total / len(mine) > 0.03:
        print('判定: ★要修正 --- 20字以上の一致、または本文の3%超が一致している')
        return 2
    else:
        print('判定: 許容範囲(一般的な日本語表現の範囲)')
    return 0

if __name__ == '__main__':
    sys.exit(main())
