# -*- coding: utf-8 -*-
"""Nova ilustração facial: rosto feminino delicado em vista frontal (line art),
com os pontos nas posições anatômicas corretas."""
P = '/tmp/claude-0/-home-user-reologia-map/cd216e96-b088-57d1-abe3-2409c365400d/scratchpad/build_ebook.py'
src = open(P, encoding='utf-8').read()

i0 = src.index('FACE_PATH = (')
i1 = src.index('def gel_icons():')

NEW = r'''FACE_ART = """
<g class="fc-hair">
 <path d="M70,152 C67,102 103,71 150,71 C197,71 233,102 230,152"/>
 <path d="M70,152 C62,182 58,216 60,250"/>
 <path d="M230,152 C238,182 242,216 240,250"/>
 <path d="M97,86 C88,110 84,133 84,155"/>
 <path d="M203,86 C212,110 216,133 216,155"/>
</g>
<path class="fc-face" d="M150,344 C176,342 197,327 211,305 C223,287 230,261 232,229
 C234,198 233,169 229,145 C225,119 208,101 186,93 C174,89 162,87 150,87
 C138,87 126,89 114,93 C92,101 75,119 71,145 C67,169 66,198 68,229
 C70,261 77,287 89,305 C103,327 124,342 150,344 Z"/>
<g class="fc-feat">
 <path d="M101,151 C112,142 129,141 139,148"/>
 <path d="M161,148 C171,141 188,142 199,151"/>
 <path d="M103,169 C111,159 128,159 136,169 C128,178 111,178 103,169 Z"/>
 <path d="M164,169 C172,159 189,159 197,169 C189,178 172,178 164,169 Z"/>
 <path d="M150,181 C149,196 147,208 145,216"/>
 <path d="M137,222 C142,227 158,227 163,222"/>
 <path d="M137,222 C132,218 134,212 138,211"/>
 <path d="M163,222 C168,218 166,212 162,211"/>
 <path d="M130,258 C137,250 145,248 150,253 C155,248 163,250 170,258 C160,261 140,261 130,258 Z"/>
 <path d="M130,258 C139,273 161,273 170,258"/>
 <path d="M120,338 C119,356 117,368 114,380"/>
 <path d="M180,338 C181,356 183,368 186,380"/>
</g>
<circle class="fc-iris" cx="119.5" cy="169" r="4.4"/>
<circle class="fc-iris" cx="180.5" cy="169" r="4.4"/>
"""

def face_svg(width=250, marks=None, cls='facesvg', aria='rosto feminino em vista frontal',
             vw=300, dx=0, leader=False):
    """marks: (x, y, cor, label, lado) — lado 'L'/'R' com leader, ou ancoragem simples."""
    m = ''
    if marks:
        for mk in marks:
            if leader:
                x, y, c, label, side = mk; x += dx
                lx = (vw - 8) if side == 'R' else 8
                ex = x + 9 if side == 'R' else x - 9
                m += (f'<line x1="{ex}" y1="{y}" x2="{lx}" y2="{y}" class="fc-ld"/>'
                      f'<text x="{lx - 3 if side == "R" else lx + 3}" y="{y - 5}" class="fc-lb" '
                      f'text-anchor="{"end" if side == "R" else "start"}">{html.escape(label)}</text>')
            else:
                x, y, c, label, anch = mk; x += dx
                if label:
                    lx = x + (12 if anch == 'start' else -12)
                    m += (f'<line x1="{x}" y1="{y}" x2="{lx}" y2="{y}" class="fc-ld"/>'
                          f'<text x="{lx + (4 if anch == "start" else -4)}" y="{y + 3.5}" class="fc-lb" '
                          f'text-anchor="{anch}">{html.escape(label)}</text>')
            m += (f'<circle cx="{x}" cy="{y}" r="7.5" fill="{CHIP[c]}" class="fc-dot"/>'
                  f'<circle cx="{x}" cy="{y}" r="12" fill="{CHIP[c]}" class="fc-halo"/>')
    g0 = f'<g transform="translate({dx},0)">' if dx else ''
    g1 = '</g>' if dx else ''
    return (f'<svg class="{cls}" viewBox="0 0 {vw} 400" role="img" aria-label="{aria}" '
            f'style="width:{width}px">{g0}{FACE_ART}{g1}{m}</svg>')

'''
src = src[:i0] + NEW + src[i1:]

# ---- chamadas atualizadas com as posições anatômicas corretas ----
i2 = src.index('FACE_CAPA = face_svg('); i3 = src.index('page=f')
NEW_CALLS = """FACE_CAPA = face_svg(196, marks=[
    (150,126,'a','','start'),   # fronte
    (120,187,'s','','start'),   # olheira / infraorbitário
    (198,214,'v','','start'),   # malar
    (176,243,'m','','start'),   # sulco nasolabial
    (150,330,'r','','start')],  # mento
    cls='facesvg capa-face', aria='rosto com os pontos das famílias do Mapa')

FACE_GEO = face_svg(320, marks=[
    (108,205,'m','CURVA · malar','L'),
    (128,232,'r','SUPORTE · profundo','L'),
    (180,240,'m','VALE · sulco nasolabial','R'),
    (170,259,'a','LINHA · perioral','R'),
    (156,332,'r','VÉRTICE · mento','R')],
    cls='facesvg', aria='tarefas geométricas do preenchimento sobre a face',
    vw=430, dx=65, leader=True)

"""
src = src[:i2] + NEW_CALLS + src[i3:]

# ---- CSS da ilustração ----
OLD_CSS = """.fc-line{{fill:none;stroke:var(--ink2);stroke-width:2.6;stroke-linecap:round}}
.fc-thin{{stroke-width:1.8;opacity:.75}}
.fc-dot{{stroke:var(--card);stroke-width:2}}
.fc-ld{{stroke:var(--ink3);stroke-width:1;stroke-dasharray:2 3}}
.fc-lb{{fill:var(--ink2);font:600 11px 'Source Sans 3',sans-serif}}"""
NEW_CSS = """.fc-face{{fill:var(--face-fill);stroke:var(--face-line);stroke-width:2.2;stroke-linejoin:round}}
.fc-hair path{{fill:none;stroke:var(--face-line);stroke-width:2.2;stroke-linecap:round;opacity:.9}}
.fc-feat path{{fill:none;stroke:var(--face-line);stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}}
.fc-iris{{fill:var(--face-line);opacity:.62}}
.fc-dot{{stroke:var(--card);stroke-width:2.2}}
.fc-halo{{opacity:.17}}
.fc-ld{{stroke:var(--ink3);stroke-width:1;stroke-dasharray:2 3}}
.fc-lb{{fill:var(--ink2);font:600 11.5px 'Barlow',sans-serif;letter-spacing:.02em}}
.capa-face .fc-face{{fill:rgba(255,255,255,.05);stroke:rgba(255,255,255,.62)}}
.capa-face .fc-hair path{{stroke:rgba(255,255,255,.5)}}
.capa-face .fc-feat path{{stroke:rgba(255,255,255,.58)}}
.capa-face .fc-iris{{fill:rgba(255,255,255,.6)}}
.capa-face .fc-dot{{stroke:rgba(10,53,87,.9)}}"""
assert OLD_CSS in src
src = src.replace(OLD_CSS, NEW_CSS, 1)

# tokens da face
src = src.replace(" --title-ink:#10486F; --gold-ink:#10486F;",
                  " --title-ink:#10486F; --gold-ink:#10486F; --face-line:#5A6C7A; --face-fill:#FFFCF7;", 1)
src = src.replace(" --title-ink:#E8EEF4; --gold-ink:#E9B968;",
                  " --title-ink:#E8EEF4; --gold-ink:#E9B968; --face-line:#8CA3B5; --face-fill:rgba(255,255,255,.04);")

# legenda da figura
OLD_CAP = """<figcaption><b>Figura 1.</b> As cinco tarefas geométricas do preenchimento sobre a face: <b>LINHA</b> (microdepressão superficial — perioral), <b>VALE</b> (depressão — sulco nasolabial, pré-jowl), <b>CURVA</b> (convexidade difusa — malar/bochecha), <b>SUPORTE</b> (sustentação profunda — fossa piriforme, supraperiostal) e <b>VÉRTICE</b> (projeção focal — mento, ângulo, zigoma). A cor de cada ponto indica a família de G′ tipicamente exigida; o gel é escolhido para a tarefa, não para a região inteira.</figcaption>"""
NEW_CAP = """<figcaption><b>Figura 2.</b> As cinco tarefas geométricas do preenchimento sobre a face: <b>LINHA</b> (microdepressão superficial — perioral), <b>VALE</b> (depressão — sulco nasolabial, pré-jowl), <b>CURVA</b> (convexidade difusa — malar/bochecha), <b>SUPORTE</b> (sustentação profunda — fossa piriforme, supraperiostal) e <b>VÉRTICE</b> (projeção focal — mento, ângulo, zigoma). A cor de cada ponto indica a família de G′ tipicamente exigida: <span style="color:var(--fam-a)"><b>azul</b></span> baixo, <span style="color:var(--fam-m)"><b>amarelo</b></span> intermediário, <span style="color:var(--fam-r)"><b>roxo</b></span> alto. O gel é escolhido para a tarefa, não para a região inteira.</figcaption>"""
assert OLD_CAP in src
src = src.replace(OLD_CAP, NEW_CAP, 1)

open(P, 'w', encoding='utf-8').write(src)
print('face redesenhada')
