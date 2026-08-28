# -*- coding: utf-8 -*-
"""v9 — Mapa anatômico das regiões faciais por grupo: uma face por grupo,
com as regiões demarcadas nas cores das assinaturas do Mapa da Reologia."""
P = 'build_ebook.py'
src = open(P, encoding='utf-8').read()

FUNCS = '''
# ---------------- mapa anatômico: regiões faciais por grupo ----------------
FACE_CLIP = ("M150,344 C176,342 197,327 211,305 C223,287 230,261 232,229 "
             "C234,198 233,169 229,145 C225,119 208,101 186,93 C174,89 162,87 150,87 "
             "C138,87 126,89 114,93 C92,101 75,119 71,145 C67,169 66,198 68,229 "
             "C70,261 77,287 89,305 C103,327 124,342 150,344 Z")

# lado esquerdo do observador; as bilaterais são espelhadas por transform
REG = {
 'fronte':      ('c', 'M96,148 C98,112 122,99 150,99 C178,99 202,112 204,148 C180,138 120,138 96,148 Z'),
 'temporal':    ('b', 'M72,142 C77,131 87,127 95,133 C93,152 92,172 93,192 C82,187 74,170 72,150 Z'),
 'supercilio':  ('b', 'M98,155 C110,143 130,142 142,150 L140,159 C129,152 111,153 100,162 Z'),
 'infraorb':    ('b', 'M101,181 C110,176 130,177 138,183 C133,197 112,200 102,191 Z'),
 'zigoma':      ('b', 'M82,197 C95,190 116,193 127,202 C125,218 103,227 86,218 Z'),
 'bochecha':    ('b', 'M83,222 C97,216 118,220 129,230 C127,252 105,265 86,254 Z'),
 'auricular':   ('b', 'M62,205 C70,202 77,207 79,214 C79,232 79,246 79,260 C69,255 62,240 60,223 Z'),
 'nariz':       ('c', 'M142,156 C147,152 153,152 158,156 C160,180 161,200 161,214 '
                      'C159,225 141,225 139,214 C139,200 140,180 142,156 Z'),
 'nasolabial':  ('b', 'M135,221 C128,231 123,246 125,263 L133,265 C131,249 134,235 141,225 Z'),
 'labios':      ('c', 'M126,256 C136,247 145,250 150,253 C155,250 164,247 174,256 C166,275 134,275 126,256 Z'),
 'perioral':    ('c', 'M118,251 C130,237 142,243 150,246 C158,243 170,237 182,251 '
                      'C180,272 168,285 150,287 C132,285 120,272 118,251 Z'
                      'M126,256 C134,274 166,274 174,256 C164,247 155,250 150,253 C145,250 136,247 126,256 Z'),
 'labiomentual':('c', 'M131,287 C140,281 160,281 169,287 C161,295 139,295 131,287 Z'),
 'mento':       ('c', 'M127,297 C137,291 163,291 173,297 C175,321 165,337 150,341 C135,337 125,321 127,297 Z'),
 'mandibula':   ('b', 'M77,266 C84,295 102,321 127,338 L122,346 C95,329 76,300 69,270 Z'),
 'prejowl':     ('b', 'M106,299 C117,294 128,299 133,308 C126,321 111,321 104,312 Z'),
}

GRUPOS_REG = [
 dict(n='1', nome='FLUIDOS DINÂMICOS', cores=['a', 'p'],
      regs=['perioral'],
      txt='Região oral e perioral.',
      leg='Baixo G′ com componente dinâmica: acompanha a mímica sem criar relevo próprio.'),
 dict(n='2', nome='FLUIDOS COM CORPO', cores=['a', 'm', 'p'],
      regs=['labios', 'temporal', 'fronte', 'supercilio', 'nasolabial', 'labiomentual'],
      txt='Região labial quando se quer mais volume · têmpora, fronte e supercílio · '
          'sulco nasolabial e sulco labiomentual.',
      leg='Baixo G′ com corpo: ainda integra, mas já sustenta um mínimo de volume.'),
 dict(n='3', nome='EQUILIBRADOS', cores=['m'],
      regs=['labiomentual', 'nasolabial', 'prejowl', 'bochecha', 'auricular', 'mandibula'],
      txt='Sulco labiomentual e sulco nasolabial · pré-jowl · bochecha · '
          'região auricular anterior · valorização de mandíbula.',
      leg='G′ intermediário: preenche e equilibra sem impor projeção.'),
 dict(n='4', nome='PROJETORES PUROS', cores=['r'],
      regs=['mento', 'nariz', 'zigoma', 'mandibula'],
      txt='Mento · nariz · arco zigomático · mandíbula.',
      leg='Roxo puro — projeção: alto G′ com tan δ baixo, o gel que mantém o vértice.'),
 dict(n='5', nome='ESTRUTURAIS MOLDÁVEIS', cores=['r', 'v'],
      regs=['mandibula', 'mento', 'nasolabial', 'zigoma', 'temporal', 'nariz'],
      txt='Regiões de volumização: contorno de mandíbula · mento · sulco nasolabial muito '
          'profundo · arco zigomático · crown lift · nariz.',
      leg='Alto G′ com uma segunda cor associada — azul, amarelo, verde ou rosa: '
          'estrutura que ainda se deixa moldar.'),
 dict(n='6', nome='PRECISOS — BAIXO SWELLING FACTOR', cores=['s'],
      regs=['infraorb'],
      txt='Exclusivamente região infraorbitária e olheiras.',
      leg='Cor própria do critério funcional. Gel de alto G′, baixa concentração de ácido '
          'hialurônico e partículas grandes. 💧 O swelling factor não foi medido neste estudo.'),
]

CORREG = {'a': 'var(--fam-a)', 'm': 'var(--fam-m)', 'r': 'var(--fam-r)',
          'v': 'var(--fam-v)', 'p': 'var(--chip-rosa)', 's': 'var(--sf)'}

def face_regioes(g, width=196):
    """Face frontal com as regiões do grupo demarcadas nas cores da assinatura."""
    uid = f'fr{g["n"]}'
    fill = CORREG[g['cores'][0]]
    stroke = CORREG[g['cores'][-1]] if len(g['cores']) > 1 else fill
    shapes = ''
    for r in g['regs']:
        lado, d = REG[r]
        rule = ' fill-rule="evenodd"' if r == 'perioral' else ''
        shapes += f'<path d="{d}" class="rg"{rule}><title>{r}</title></path>'
        if lado == 'b':
            shapes += (f'<g transform="translate(300,0) scale(-1,1)">'
                       f'<path d="{d}" class="rg"{rule}/></g>')
    return (f'<svg class="facereg" viewBox="0 0 300 400" role="img" '
            f'style="width:{width}px;--rg-f:{fill};--rg-s:{stroke}" '
            f'aria-label="regiões faciais do grupo {g["n"]}: {html.escape(g["txt"])}">'
            f'<defs><clipPath id="{uid}"><path d="{FACE_CLIP}"/></clipPath></defs>'
            f'{FACE_ART}<g clip-path="url(#{uid})">{shapes}</g>'
            f'<path d="{FACE_CLIP}" class="fc-edge"/></svg>')

def mapa_regioes():
    cards = ''
    for g in GRUPOS_REG:
        chips = ''.join(f'<i style="background:{CORREG[c]}"></i>' for c in g['cores'])
        cards += (f'<figure class="regcard rc-{g["cores"][0]}">'
                  f'<figcaption><span class="rc-n">{g["n"]}</span>'
                  f'<span class="rc-t">{g["nome"]}</span>'
                  f'<span class="rc-chips">{chips}</span></figcaption>'
                  f'{face_regioes(g)}'
                  f'<p class="rc-reg">{g["txt"]}</p>'
                  f'<p class="rc-leg">{g["leg"]}</p></figure>')
    return f'<div class="mapareg">{cards}</div>'

'''
anchor = '# ---------------- seções de grupos ----------------'
assert anchor in src
src = src.replace(anchor, FUNCS + anchor, 1)

CSS = '''
/* mapa anatômico de regiões por grupo */
.mapareg{{display:grid;grid-template-columns:repeat(auto-fit,minmax(258px,1fr));gap:1rem;margin:1.2rem 0}}
.regcard{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:4px;
 padding:.55rem .8rem 1rem;text-align:center;display:flex;flex-direction:column}}
.regcard figcaption{{display:flex;align-items:center;gap:.5rem;text-align:left;
 border-bottom:1px solid var(--linesoft);padding-bottom:.45rem;margin-bottom:.3rem}}
.rc-n{{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:1.5rem;
 line-height:1;color:var(--gold);flex:0 0 auto}}
.rc-t{{font-family:'Barlow Condensed',sans-serif;font-size:.95rem;font-weight:600;
 letter-spacing:.04em;text-transform:uppercase;color:var(--title-ink);flex:1;line-height:1.05}}
.rc-chips{{display:flex;gap:3px;flex:0 0 auto}}
.rc-chips i{{width:11px;height:11px;border-radius:50%;display:block;
 border:1px solid rgba(0,0,0,.18)}}
.facereg{{display:block;margin:.2rem auto .5rem;height:auto}}
.facereg .rg{{fill:var(--rg-f);fill-opacity:.34;stroke:var(--rg-s);stroke-width:1.7;
 stroke-linejoin:round}}
.facereg .fc-edge{{fill:none;stroke:var(--face-line);stroke-width:2.2;opacity:.9}}
.rc-reg{{font-family:'Barlow',sans-serif;font-size:.82rem;color:var(--ink);
 margin:.1rem 0 .35rem;line-height:1.45;text-align:left;font-weight:600}}
.rc-leg{{font-family:'Barlow',sans-serif;font-size:.76rem;color:var(--ink2);
 margin:0;line-height:1.45;text-align:left}}
'''
mark = '/* figuras e ilustrações com moldura dourada */'
assert mark in src
src = src.replace(mark, CSS + mark, 1)

# substitui a Figura 7 pelo novo mapa
i = src.index('<figure class="figura">{FACE_GEO}')
j = src.index('</figcaption></figure>', i) + len('</figcaption></figure>')
NOVA = """<h3 style="margin-top:1.6rem">Mapa anatômico — que região pede qual assinatura</h3>
<p class="lead">Uma face por grupo, com as regiões demarcadas na cor da assinatura correspondente. As regiões se repetem entre grupos de propósito: <b>a mesma mandíbula</b> aparece no grupo 3 (valorizar o contorno), no 4 (projetar o ângulo) e no 5 (volumizar). O que muda não é a região — é a tarefa.</p>
{mapa_regioes()}
<p class="lead" style="font-size:.92rem"><b>Como ler as cores:</b> o preenchimento traz a <b>1ª cor</b> (a família de G′) e o contorno traz a <b>2ª cor</b> (o comportamento em tan δ). O grupo 4 é <b>roxo puro</b> — estrutura sem modificador. O grupo 6 tem <b>cor própria</b> (<span style="color:var(--sf)"><b>turquesa</b></span>), porque não é uma família de G′ e sim um critério funcional transversal.</p>
<p class="qt">A regra que atravessa o mapa: <b>o gel é escolhido para a tarefa, não para a região</b>. Um sulco nasolabial raso e um sulco nasolabial muito profundo estão em grupos diferentes — 2 e 5 — apesar de terem o mesmo nome anatômico.</p>"""
src = src[:i] + NOVA + src[j:]

open(P, 'w', encoding='utf-8').write(src)
print('v9 aplicado: mapa anatômico de regiões por grupo')
