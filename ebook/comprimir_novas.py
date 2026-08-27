# -*- coding: utf-8 -*-
"""Comprime as imagens aprovadas em drive_assets2/ para data URIs em ilustracoes2.json.
Uso: python3 comprimir_novas.py chave=arquivo.png chave2=arquivo2.png ...
     (ou sem argumentos: pega todos os .png/.jpg da pasta, chave = nome sem extensão)"""
from PIL import Image
import base64, io, json, os, sys

BASE = '/tmp/claude-0/-home-user-reologia-map/cd216e96-b088-57d1-abe3-2409c365400d/scratchpad'
SRC = os.path.join(BASE, 'drive_assets2')
OUT = os.path.join(BASE, 'ilustracoes2.json')

pairs = []
if len(sys.argv) > 1:
    for a in sys.argv[1:]:
        k, f = a.split('=', 1); pairs.append((k, f))
else:
    for f in sorted(os.listdir(SRC)):
        if f.lower().endswith(('.png', '.jpg', '.jpeg')):
            pairs.append((os.path.splitext(f)[0], f))

out = json.load(open(OUT)) if os.path.exists(OUT) else {}
tot = 0
for k, f in pairs:
    p = os.path.join(SRC, f)
    if not os.path.exists(p):
        print(f'  !! ausente: {f}'); continue
    im = Image.open(p).convert('RGB')
    w, h = im.size
    tw = 1100
    if w > tw:
        im = im.resize((tw, int(h * tw / w)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, format='JPEG', quality=78, optimize=True, progressive=True)
    d = b.getvalue(); tot += len(d)
    out[k] = 'data:image/jpeg;base64,' + base64.b64encode(d).decode()
    print(f'  {k:16s} {w}x{h} -> {im.size[0]}x{im.size[1]}  {len(d)//1024} KB')

json.dump(out, open(OUT, 'w'))
print(f'\n{len(pairs)} imagens · {tot//1024} KB jpeg · ~{int(tot*1.34)//1024} KB em base64')
print(f'total no arquivo: {len(out)} chaves')
