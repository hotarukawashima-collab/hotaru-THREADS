# 図版PNGの下端にできる余白を自動で切り落とす
import sys, os, glob
from PIL import Image
BG = (251, 248, 241)  # #FBF8F1
PAD = 64 * 2          # 下に残す余白(2倍解像度)
for f in sorted(glob.glob(os.path.join(sys.argv[1], 'fig*.png'))):
    im = Image.open(f).convert('RGB')
    w, h = im.size
    px = im.load()
    last = 0
    for y in range(h - 1, -1, -1):
        if any(px[x, y] != BG for x in range(0, w, 7)):
            last = y; break
    new_h = min(h, last + PAD)
    if new_h < h:
        im.crop((0, 0, w, new_h)).save(f)
    print(f'  trim {os.path.basename(f)}: {h} -> {new_h}')
