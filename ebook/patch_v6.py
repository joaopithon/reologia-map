# -*- coding: utf-8 -*-
"""v6 — formato de livro: folhas com tamanho de página, rodapés correntes,
aberturas de capítulo e a cadeia de ácido hialurônico como ornamento da
identidade visual (inspirada no desenho de formação do hidrogel)."""
import math, re, urllib.parse

P = '/tmp/claude-0/-home-user-reologia-map/cd216e96-b088-57d1-abe3-2409c365400d/scratchpad/build_ebook.py'
src = open(P, encoding='utf-8').read()

# ---------------------------------------------------------------- ornamentos
def _chain(w, h, amp, period, n, x0=3):
    """Pontos de uma cadeia senoidal de AH (como no desenho de reticulação)."""
    pts = []
    for i in range(n + 1):
        x = x0 + i * (w - 2 * x0) / n
        y = h / 2 - amp * math.sin(2 * math.pi * (x - x0) / period)
        pts.append((round(x, 2), round(y, 2)))
    return pts

def orn_cadeia(w=152, h=20, cor='%23C08A2E'):
    """Cadeia de AH em contas — ornamento de rodapé (SVG puro p/ data URI)."""
    pts = _chain(w, h, 5.4, 38, 30)
    d = 'M' + ' L'.join(f'{x},{y}' for x, y in pts)
    beads = ''
    n = len(pts)
    for i, (x, y) in enumerate(pts):
        if i % 2: continue
        t = i / (n - 1)
        op = round(0.30 + 0.70 * math.sin(math.pi * t) ** 0.6, 2)   # some nas pontas
        r = round(1.7 + 1.5 * math.sin(math.pi * t) ** 0.7, 2)
        beads += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{cor}" opacity="{op}"/>'
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}' width='{w}' height='{h}'>"
            f"<path d='{d}' fill='none' stroke='{cor}' stroke-width='1' opacity='.42'/>{beads}</svg>")

def data_uri(svg):
    return 'data:image/svg+xml,' + urllib.parse.quote(svg, safe="")

ORN_LIGHT = data_uri(orn_cadeia(cor='%23C08A2E'))
ORN_DARK  = data_uri(orn_cadeia(cor='%23D6A048'))

# ---- ornamentos inline (usam currentColor / vars: viram elementos no HTML) ----
ORN_FUNCS = '''
# ---------------- ornamentos da identidade: cadeia e rede de AH ----------------
def _ha_pts(w, h, amp, period, n, x0=3):
    return [(round(x0 + i*(w-2*x0)/n, 2),
             round(h/2 - amp*math.sin(2*math.pi*(x0 + i*(w-2*x0)/n - x0)/period), 2))
            for i in range(n+1)]

def orn(kind='cadeia', width=150, cls='orn'):
    """Ornamento inspirado no desenho oficial de formação do hidrogel:
    cadeias de ácido hialurônico em contas, pontos de reticulação e água."""
    if kind == 'cadeia':
        w, h = 150, 20
        pts = _ha_pts(w, h, 5.4, 38, 30)
        d = 'M' + ' L'.join(f'{x},{y}' for x, y in pts)
        beads = ''
        for i, (x, y) in enumerate(pts):
            if i % 2: continue
            t = i/(len(pts)-1)
            op = round(.28 + .72*math.sin(math.pi*t)**.6, 2)
            r  = round(1.6 + 1.5*math.sin(math.pi*t)**.7, 2)
            beads += f'<circle cx="{x}" cy="{y}" r="{r}" class="orn-b" opacity="{op}"/>'
        body = f'<path d="{d}" class="orn-l"/>{beads}'
    elif kind == 'rede':
        # duas cadeias unidas por um ponto de reticulação + moléculas de água
        w, h = 132, 54
        a = _ha_pts(w, 30, 5.0, 40, 26); b = _ha_pts(w, 30, 5.0, 40, 26)
        da = 'M' + ' L'.join(f'{x},{y+3}' for x, y in a)
        db = 'M' + ' L'.join(f'{x},{y+27}' for x, y in b)
        beads = ''
        for pts, dy in ((a, 3), (b, 27)):
            for i, (x, y) in enumerate(pts):
                if i % 2: continue
                t = i/(len(pts)-1)
                beads += (f'<circle cx="{x}" cy="{y+dy}" r="{round(1.5+1.3*math.sin(math.pi*t)**.7,2)}" '
                          f'class="orn-b" opacity="{round(.3+.7*math.sin(math.pi*t)**.6,2)}"/>')
        xs = [40, 92]
        links = ''.join(f'<line x1="{x}" y1="{a[0][1]+9}" x2="{x}" y2="{b[0][1]+21}" class="orn-x"/>'
                        f'<circle cx="{x}" cy="{h/2}" r="2.6" class="orn-n"/>' for x in xs)
        agua = ''.join(f'<circle cx="{x}" cy="{y}" r="1.5" class="orn-w"/>'
                       for x, y in ((20,27),(66,22),(66,33),(114,27)))
        body = f'<path d="{da}" class="orn-l"/><path d="{db}" class="orn-l"/>{links}{agua}{beads}'
    else:  # 'gota' — gel: gota com rede interna
        w, h = 62, 74
        body = ('<path d="M31,4 C31,4 54,32 54,46 A23,23 0 0,1 8,46 C8,32 31,4 31,4 Z" class="orn-g"/>'
                '<path d="M17,44 C24,38 38,38 45,44" class="orn-l"/>'
                '<path d="M15,54 C23,48 39,48 47,54" class="orn-l"/>'
                '<circle cx="22" cy="42" r="2.2" class="orn-b"/><circle cx="31" cy="40" r="2.6" class="orn-b"/>'
                '<circle cx="40" cy="42" r="2.2" class="orn-b"/><circle cx="20" cy="52" r="2.2" class="orn-b"/>'
                '<circle cx="31" cy="50" r="2.6" class="orn-b"/><circle cx="42" cy="52" r="2.2" class="orn-b"/>'
                '<line x1="31" y1="40" x2="31" y2="50" class="orn-x"/>'
                '<circle cx="26" cy="61" r="1.5" class="orn-w"/><circle cx="37" cy="62" r="1.5" class="orn-w"/>')
    return (f'<svg class="{cls}" viewBox="0 0 {w} {h}" role="presentation" aria-hidden="true" '
            f'style="width:{width}px">{body}</svg>')

def filete(kind='cadeia', width=150):
    """Filete ornamental centrado: régua — ornamento — régua."""
    return f'<div class="filete"><span></span>{orn(kind, width)}<span></span></div>'

'''
anchor = '# ---------------- radar ----------------'
assert anchor in src
src = src.replace(anchor, ORN_FUNCS + anchor, 1)

# ---------------------------------------------------------------- abertura de capítulo
CAP_FUNC = '''
def cap_head(eyebrow, titulo, sub=''):
    """Abertura de capítulo em formato de livro: numeral, ornamento e regra."""
    m = re.match(r'Cap[ií]tulo\\s+([0-9]+)', eyebrow)
    num = m.group(1) if m else ''
    resto = eyebrow if not m else eyebrow[m.end():].strip(' ·')
    marca = f'<span class="cap-n">{num}</span>' if num else ''
    extra = f'<span class="cap-extra">{resto}</span>' if resto else ''
    subp = f'<p class="cap-sub">{sub}</p>' if sub else ''
    return (f'<div class="cap-abre">{marca}<div class="cap-tx">'
            f'<p class="cap-eyebrow">{"Capítulo" if num else eyebrow}{extra}</p>'
            f'<h2>{titulo}</h2>{subp}</div>{orn("rede", 108)}</div>')

'''
src = src.replace(anchor, CAP_FUNC + anchor, 1)

# ---------------------------------------------------------------- CSS: livro
CSS_BOOK = f'''
/* ================= FORMATO DE LIVRO: folhas, rodapés e ornamentos ================= */
main{{max-width:none;margin:0;padding:1.6rem 1rem 4rem;background:var(--book-bg);counter-reset:folha}}
.folha{{max-width:74rem;margin:0 auto 2rem;background:var(--card);border:1px solid var(--line);
 border-radius:2px;padding:clamp(1.5rem,3.2vw,3rem) clamp(1.1rem,3vw,3.2rem) 0;position:relative;
 box-shadow:0 1px 2px rgba(10,53,87,.06),0 14px 30px -20px rgba(10,53,87,.30);counter-increment:folha}}
.folha::before{{content:"";position:absolute;left:0;right:0;top:0;height:3px;
 background:linear-gradient(90deg,var(--gold-3),var(--gold-2) 32%,var(--gold) 68%,var(--gold-3))}}
.folha::after{{content:"Reologia do Ácido Hialurônico · Reology Map · " counter(folha);
 display:block;margin:2.6rem calc(-1*clamp(1.1rem,3vw,3.2rem)) 0;
 padding:2.9rem 1rem 1.15rem;border-top:1px solid var(--line);
 background:url("{ORN_LIGHT}") no-repeat center .95rem;background-size:132px 18px;
 font-family:'Barlow',system-ui,sans-serif;font-size:.66rem;font-weight:600;letter-spacing:.2em;
 text-transform:uppercase;color:var(--ink3);text-align:center}}
/* ornamentos inline */
.orn{{display:block;height:auto;overflow:visible}}
.orn-l{{fill:none;stroke:var(--gold);stroke-width:1;opacity:.45}}
.orn-b{{fill:var(--gold)}}
.orn-x{{stroke:var(--gold-2);stroke-width:1.3;opacity:.75}}
.orn-n{{fill:var(--gold-2)}}
.orn-w{{fill:var(--accent);opacity:.45}}
.orn-g{{fill:var(--gold-soft);stroke:var(--gold-2);stroke-width:1.3}}
.filete{{display:flex;align-items:center;gap:.9rem;margin:1.8rem 0 1.2rem}}
.filete>span{{flex:1;height:1px;background:linear-gradient(90deg,transparent,var(--line) 22%,var(--line) 78%,transparent)}}
/* abertura de capítulo */
.cap-abre{{display:flex;align-items:center;gap:clamp(.8rem,2vw,1.5rem);
 border-bottom:2px solid var(--gold-2);padding-bottom:.75rem;margin:0 0 1.4rem}}
.cap-abre .cap-tx{{flex:1;min-width:0}}
.cap-abre h2{{margin:.1rem 0 0;font-size:clamp(1.5rem,3.4vw,2.15rem);color:var(--title-ink)}}
.cap-abre .cap-eyebrow{{margin:0}}
.cap-n{{font-family:'Barlow Condensed','Barlow',sans-serif;font-size:clamp(2.6rem,7vw,4rem);
 font-weight:700;line-height:.78;color:var(--gold-2);letter-spacing:-.02em;
 border-right:1px solid var(--line);padding-right:clamp(.7rem,2vw,1.3rem);align-self:stretch;
 display:flex;align-items:center}}
.cap-extra{{color:var(--ink3);font-weight:600}}
.cap-extra::before{{content:" · "}}
.cap-abre .orn{{flex:0 0 auto;opacity:.85}}
@media (max-width:620px){{.cap-abre .orn{{display:none}}}}
.cap-sub{{font-family:'Barlow',sans-serif;font-size:.9rem;color:var(--ink2);margin:.35rem 0 0;max-width:60ch}}
'''

CSS_PRINT = '''
/* ================= impressão: livro em página real ================= */
@media print{
 @page{size:210mm 280mm;margin:15mm 14mm 16mm}
 html,body{background:#fff}
 main{padding:0;background:#fff}
 .folha{max-width:none;margin:0;border:none;box-shadow:none;padding:0 0 6mm;
  break-after:page;page-break-after:always}
 .folha:last-child{break-after:auto;page-break-after:auto}
 .folha::before{display:none}
 .folha::after{margin:8mm 0 0;padding-top:9mm;background-size:110px 15px}
 .cap-abre{break-after:avoid;page-break-after:avoid}
 h2,h3,h4{break-after:avoid;page-break-after:avoid}
 .box,.gelcard,.card,figure,table{break-inside:avoid;page-break-inside:avoid}
 .capa{break-after:page;page-break-after:always}
 a[href^="http"]::after{content:""}
}
'''

# insere o CSS do livro logo antes do bloco de figuras
mark = '/* figuras e ilustrações com moldura dourada */'
assert mark in src
assert '{' not in ORN_LIGHT and '{' not in ORN_DARK   # o data URI não pode ter chaves
src = src.replace(mark, CSS_BOOK.replace('{', '{{').replace('}', '}}') + mark, 1)

# print CSS no fim do <style>
src = src.replace('</style>', CSS_PRINT.replace('{', '{{').replace('}', '}}') + '</style>', 1)

# tokens de superfície do livro
src = src.replace(' --tint:12%;', ' --tint:12%; --book-bg:#EDE7DD;', 1)
src = src.replace(' --tint:22%;', ' --tint:22%; --book-bg:#04141F;')
# rodapé dourado no tema escuro
src = src.replace('/* figuras e ilustrações com moldura dourada */',
 '@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]) .folha::after{{background-image:url("'
 + ORN_DARK + '")}}}}\n'
 ':root[data-theme="dark"] .folha::after{{background-image:url("' + ORN_DARK + '")}}\n'
 '/* figuras e ilustrações com moldura dourada */', 1)

# ---------------------------------------------------------------- sections -> folhas
src = re.sub(r'<section id="(comoler|fundamentos|mapasec|forma|textura|atlas|rankings|regioes|indice|notas)">',
             r'<section class="folha" id="\1">', src)
# seções de grupos (5 famílias + grupo 6)
src = src.replace('<section class="famsec" id=', '<section class="famsec folha" id=')

# ---------------------------------------------------------------- cabeçalhos de capítulo
def repl_head(m):
    eb, tit = m.group(1), m.group(2)
    return "{cap_head('" + eb.replace("'", "\\'") + "','" + tit.replace("'", "\\'") + "')}"
src, nsub = re.subn(r'<p class="cap-eyebrow">([^<]*)</p><h2>(.*?)</h2>', repl_head, src)

open(P, 'w', encoding='utf-8').write(src)
print(f'v6 aplicado · {nsub} aberturas de capítulo convertidas')
