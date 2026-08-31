# -*- coding: utf-8 -*-
"""Versao para impressao do documento das regioes da face.

Duas armadilhas do WeasyPrint tratadas aqui:
1. Sem <meta charset> declarado no arquivo ele assume latin-1 e os acentos
   quebram — o wrapper do Artifact injeta o charset na publicacao, o arquivo
   cru nao tem.
2. Regras CSS de classe NAO alcancam elementos dentro de SVG inline. Sem
   atributos de apresentacao a figura sai preenchida de preto. Por isso as
   classes do SVG recebem fill/stroke direto.
"""
import os, pathlib, re
from weasyprint import HTML

RAIZ = pathlib.Path(__file__).resolve().parents[1]

TOK = {'papel':'#F7F5F2','papel2':'#EFEBE5','tinta':'#1E2530','tinta2':'#454E5C',
 'tinta3':'#6E7683','linha':'#D8D2C9','carmim':'#8E3B46','carmim-fr':'#F0E3E2',
 'pele':'#E4C3AC','pele-sh':'#CFA48B','pele-or':'#DCB9A1','sobranc':'#4E3B2C',
 'iris':'#6B5236','pupila':'#1A1410','labio-s':'#B87B72','labio-i':'#C68C82',
 'esclera':'#FBF7F3'}
_T = TOK.get

ATTR = {
 'pl':     f'fill="{_T("pele")}" stroke="{_T("tinta")}" stroke-width="1.6" stroke-linejoin="round"',
 'orelha': f'fill="{_T("pele-or")}" stroke="{_T("tinta")}" stroke-width="1.5" stroke-linejoin="round"',
 'ln2':    f'fill="none" stroke="{_T("tinta")}" stroke-width="1.2" stroke-linecap="round" opacity=".78"',
 'ln3':    f'fill="none" stroke="{_T("tinta")}" stroke-width="1" stroke-linecap="round" opacity=".42"',
 'sh':     f'fill="{_T("pele-sh")}" stroke="none" opacity=".32"',
 'brow':   f'fill="{_T("sobranc")}" stroke="none"',
 'olho':   f'fill="{_T("esclera")}" stroke="{_T("tinta")}" stroke-width="1.2"',
 'lid':    f'fill="none" stroke="{_T("tinta")}" stroke-width="2.1" stroke-linecap="round"',
 'iris':   f'fill="{_T("iris")}"',
 'pup':    f'fill="{_T("pupila")}"',
 'lipup':  f'fill="{_T("labio-s")}" stroke="{_T("tinta")}" stroke-width="1.1"',
 'liplo':  f'fill="{_T("labio-i")}" stroke="{_T("tinta")}" stroke-width="1.1"',
 'rg':     f'fill="none" stroke="{_T("tinta")}" stroke-width="1.2" opacity=".9" stroke-linecap="round"',
 'rgl':    f'fill="none" stroke="{_T("tinta")}" stroke-width="1.2" opacity=".9" stroke-linecap="round"',
 'ld':     f'fill="none" stroke="{_T("tinta")}" stroke-width=".9" opacity=".66"',
 'an':     f'fill="{_T("carmim")}" stroke="{_T("papel2")}" stroke-width="1"',
 'lb':     f'fill="{_T("tinta")}" font-family="Asap Condensed, Asap, sans-serif" font-size="15.5"',
}

CSS_IMPRESSO = """
@page{size:A4;margin:15mm 14mm 14mm}
.env{max-width:100%;padding:0} .col{max-width:100%}
body{font-size:10pt;background:#fff}
h1{font-size:25pt;margin-bottom:10px} .sub{font-size:11.5pt}
h2{font-size:17pt;margin-top:26px} h3{margin:26px 0 8px;page-break-after:avoid}
figure{margin-top:22px}
.pr-wrap{page-break-inside:avoid;break-inside:avoid;padding:6px 0;background:#FBFAF8}
.gl-it{page-break-inside:avoid;break-inside:avoid;padding:12px 0;
 grid-template-columns:31% 1fr;gap:0 18px}
.gl-cp>p{font-size:9.6pt;margin-bottom:5px} .gl-nome{font-size:11.5pt}
.nota{page-break-inside:avoid;padding:14px 16px;margin:22px 0}
.nota p{font-size:9.8pt}
figcaption{font-size:9.6pt} .rod{font-size:9.4pt}
"""

def build(origem=None, destino=None):
    origem = pathlib.Path(origem or RAIZ / 'docs/regioes/regioes-da-face.html')
    destino = pathlib.Path(destino or RAIZ / 'docs/regioes/Regioes-da-Face-e-do-Pescoco.pdf')
    h = '<!DOCTYPE html>\n<meta charset="utf-8">\n' + origem.read_text(encoding='utf-8')
    h = re.sub(r'@media \(prefers-color-scheme:dark\)\{.*?\n \}\n\}', '', h, flags=re.S)
    h = re.sub(r':root\[data-theme="dark"\]\{.*?\n\}', '', h, flags=re.S)

    def injeta(m):
        cls = m.group(1)
        return f'class="{cls}" ' + ATTR[cls] if cls in ATTR else m.group(0)
    i0, i1 = h.index('<svg'), h.index('</svg>') + 6
    h = h[:i0] + re.sub(r'class="([a-z0-9 ]+)"', injeta, h[i0:i1]) + h[i1:]

    h = re.sub(r'var\(--([a-z0-9-]+)\)', lambda m: TOK.get(m.group(1), '#1E2530'), h)
    h = h.replace('</style>', CSS_IMPRESSO + '</style>')

    tmp = destino.with_suffix('.tmp.html')
    tmp.write_text(h, encoding='utf-8')
    HTML(filename=str(tmp), encoding='utf-8').write_pdf(str(destino))
    tmp.unlink()
    return destino

if __name__ == '__main__':
    d = build()
    print(f'OK {d}  ·  {d.stat().st_size//1024} KB')
