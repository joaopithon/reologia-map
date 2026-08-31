# -*- coding: utf-8 -*-
"""eBook Reology Map v3 — 6 grupos oficiais, assinatura de cores por métrica,
ilustrações face+gel, textura visual com QR (NA PRÁTICA / SAIBA MAIS)."""
import json, math, html, re, os, unicodedata, importlib.util

BASE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('ebook_data', f'{BASE}/ebook_data.py')
ed = importlib.util.module_from_spec(spec); spec.loader.exec_module(ed)
DATA = {r['produto']: r for r in json.load(open(os.path.join(BASE, '..', 'data', 'reologia_produtos_full.json')))}
QR = json.load(open(f'{BASE}/qrs.json'))
ILU = json.load(open(f'{BASE}/ilustracoes.json'))
ILU2 = json.load(open(f'{BASE}/ilustracoes2.json'))
assert len(ed.PRODUTOS) == 76

ERR_TD = {'Perfectha Subskin': 0.15}   # errata: G″/G′ = 52,00/343,00 = 0,1516
def td_of(k): return ERR_TD.get(k, DATA[k]['tand_0.7Hz'])
def br(v, nd=2): return f'{v:,.{nd}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
def br0(v): return f'{v:,.0f}'.replace(',', '.')
def slug(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii','ignore').decode()
    return re.sub(r'[^a-z0-9]+','-', t.lower()).strip('-')
def short(k):
    s = k.replace(' Lidocaine','').replace(' Lido','').replace(' lido','')
    return s if len(s)<=26 else s[:25]+'…'

# ---------------- grupos oficiais ----------------
P2SET = {'Belotero Intense Lido','Evofill Derm','Evofill Ultra Deep','Juvéderm Skinvive','Revanesse Kiss Lido','Up Deep Lido'}
P4SET = {'Hyafilia V Plus Lido','Restylane Shaype Lido'}
def grp(p):
    if p['c']=='A': return 'G2' if p['k'] in P2SET else 'G1'
    if p['c']=='M': return 'G3'
    return 'G4' if p['k'] in P4SET else 'G5'

GRUPOS = {
 'G1': dict(num=1, nome='FLUIDOS DINÂMICOS', tec='Integrativo dinâmico · P1 · azul + rosa', fam='a',
   chave='Pouca estrutura + pouca volumização + boa mobilidade: espalha bem, cria pouco relevo e acompanha o movimento.',
   ctx='Correções suaves · áreas dinâmicas · lábio natural', ex='Belotero Balance',
   bandas='G′ 0–200 Pa · G″ geralmente 0–50 Pa · tan δ alto (> 0,20) · η* baixo'),
 'G2': dict(num=2, nome='FLUIDOS COM CORPO', tec='Integrativo volumizador · P2 · azul + amarelo + rosa', fam='a',
   chave='Mesma família do baixo G′, com G″ intermediário: mantém a integração, mas entrega mais corpo e mais capacidade de preencher.',
   ctx='Lábios com mais volume · regiões dinâmicas com corpo · sulcos com correção suave', ex='Belotero Intense',
   bandas='G′ 0–200 Pa · G″ 50–100 Pa · tan δ alto (> 0,20)'),
 'G3': dict(num=3, nome='EQUILIBRADOS', tec='Preenchedor intermediário · P3 · amarelo completo', fam='m',
   chave='Produto de transição: preenche, dá corpo e sustenta de forma equilibrada — sem rigidez extrema. "O amarelo é a cor do vale."',
   ctx='Reposição de volume moderada · sulcos e transições · versatilidade clínica', ex='Belotero Volume',
   bandas='G′ 200–300 Pa · G″ ≈ 50–100 Pa · tan δ ≈ 0,15–0,20 · η* intermediário'),
 'G4': dict(num=4, nome='PROJETORES PUROS', tec='Estrutural intenso · P4 · roxo completo', fam='r',
   chave='Máxima estrutura + projeção + definição + firmeza. Grupo raro: apenas 2 dos 76 ensaios. Permanece estável onde foi colocado.',
   ctx='Mento · mandíbula · arco zigomático · vértices estruturais (nariz: apenas racional — risco vascular)', ex='Restylane Shaype',
   bandas='G′ > 300 Pa (aqui, > 800) · G″ > 100 Pa · tan δ 0–0,15 · η* > 100'),
 'G5': dict(num=5, nome='ESTRUTURAIS MOLDÁVEIS', tec='Estrutural modulado · P5 · roxo + azul/amarelo/verde', fam='r',
   chave='Começa sempre em alto G′, mas com modulação: sustenta e modela ao mesmo tempo, com mais curva, mais corpo e volumização clínica.',
   ctx='Mandíbula e mento com corpo · têmporas e bochecha · volumização estrutural · contorno', ex='Biogelis Volumax',
   bandas='G′ > 300 Pa · G″ 0–100 Pa · tan δ 0,07–0,20 · η* intermediário a alto'),
}

# ---------------- cores por métrica (gramática oficial) ----------------
def c_g1(v): return 'a' if v < 200 else ('m' if v < 300 else 'r')
def c_g2(v): return 'a' if v < 50 else ('m' if v <= 100 else 'r')
def c_td(v): return 'r' if v <= 0.15 else ('v' if v <= 0.20 else 'p')
def c_eta(v): return 'a' if v < 50 else ('m' if v <= 100 else 'r')
OVERRIDE = {'Restylane Defyne Lido': {'g1': 'r'}}   # curadoria oficial (caso de borda)
def sig_cores(k):
    d = DATA[k]; o = OVERRIDE.get(k, {})
    return dict(g1=o.get('g1', c_g1(d['G1_0.7Hz'])), g2=o.get('g2', c_g2(d['G2_0.7Hz'])),
                td=o.get('td', c_td(td_of(k))), eta=o.get('eta', c_eta(d['eta_0.7Hz'])))
CHIP = dict(a='var(--fam-a)', m='var(--fam-m)', r='var(--fam-r)', v='var(--fam-v)', p='var(--chip-rosa)', s='var(--sf)')
CNAME = dict(a='azul', m='amarelo', r='roxo', v='verde', p='rosa')
NIVEL = {1:('1ª escolha','n1'),2:('forte','n2'),3:('boa','n3'),4:('seletiva','n4')}
FLAGTXT = {'verif':'⚑ dado em re-verificação laboratorial','pend':'◌ monografia do autor pendente','ifu':'※ contraindicações de bula listadas'}

def ranks(vals):
    order = sorted(range(len(vals)), key=lambda i: vals[i]); r=[0]*len(vals)
    for pos,i in enumerate(order): r[i]=pos/(len(vals)-1)
    return r
KEYS=[p['k'] for p in ed.PRODUTOS]; RK={}
for met,get in [('g1',lambda k:DATA[k]['G1_0.7Hz']),('g2',lambda k:DATA[k]['G2_0.7Hz']),('td',td_of),('eta',lambda k:DATA[k]['eta_0.7Hz'])]:
    for k,v in zip(KEYS,ranks([get(k) for k in KEYS])): RK.setdefault(k,{})[met]=v

X0,X1 = math.log10(30), math.log10(1000)
def xg(g,w): return (math.log10(g)-X0)/(X1-X0)*w

def dotchip(c,size=13):
    return f'<span class="chip" style="width:{size}px;height:{size}px;background:{CHIP[c]}"></span>'

def sigdots(k):
    s = sig_cores(k)
    lab = [('G′','g1'),('G″','g2'),('tan δ','td'),('η*','eta')]
    return '<span class="sigdots">' + ''.join(
        f'<span class="sd"><i style="background:{CHIP[s[m]]}" title="{CNAME[s[m]]}"></i>{l}</span>' for l,m in lab) + '</span>'


# ---------------- assinatura reológica oficial (9 combinações) ----------------
BASE_NOME = {'a':'ESPALHA','m':'PREENCHE','r':'PROJETA'}
ASSIN = {('a','p'):'INTEGRATIVO DINÂMICO',('a','v'):'INTEGRATIVO MALEÁVEL',('a','r'):'ESPALHA',
         ('m','p'):'PREENCHEDOR DINÂMICO',('m','v'):'PREENCHEDOR MODELÁVEL',('m','r'):'PREENCHE',
         ('r','p'):'ESTRUTURAL DINÂMICO',('r','v'):'ESTRUTURAL MALEÁVEL',('r','r'):'PROJETA'}
def assinatura(k):
    """Retorna (nome, cor-base, cor-modificador) conforme o Esquema de Descrição oficial."""
    s = sig_cores(k)
    b = s['g1']; m = s['td']
    return ASSIN[(b, m)], b, m
def assin_badge(k):
    nome, b, m = assinatura(k)
    dots = f'<i style="background:{CHIP[b]}"></i>' + ('' if m=='r' else f'<span class="plus">+</span><i style="background:{CHIP[m]}"></i>')
    return f'<p class="assin"><span class="assin-lbl">Assinatura Reology Map</span><span class="assin-v">{dots}<b>{nome}</b></span></p>'

# ---------------- ícones oficiais das famílias ----------------
def ico(kind, size=54):
    """ondas=baixo G′ · balanca=intermediário · coluna=alto G′ · dinamico=rosa · maleavel=verde"""
    col = {'ondas':'var(--fam-a)','balanca':'var(--fam-m)','coluna':'var(--fam-r)',
           'dinamico':'var(--chip-rosa)','maleavel':'var(--fam-v)'}[kind]
    art = {
      'ondas': ('<path d="M14,24 q7,-6 14,0 t14,0" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
                '<path d="M14,33 q7,-6 14,0 t14,0" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
                '<circle cx="19" cy="41" r="2.2" fill="#fff"/><circle cx="28" cy="43" r="2.2" fill="#fff"/><circle cx="37" cy="41" r="2.2" fill="#fff"/>'),
      'balanca': ('<path d="M28,14 v26 M16,20 h24" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
                  '<path d="M16,20 l-5,9 h10 z M40,20 l-5,9 h10 z" fill="#fff" opacity=".92"/>'
                  '<path d="M20,42 h16" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'),
      'coluna': ('<path d="M15,18 h26 M18,42 h20" stroke="#fff" stroke-width="3.4" stroke-linecap="round"/>'
                 '<path d="M22,20 v20 M28,20 v20 M34,20 v20" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/>'),
      'dinamico': ('<path d="M13,20 q7,-6 14,0 t14,0" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/>'
                   '<path d="M13,29 q7,-6 14,0 t14,0" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/>'
                   '<path d="M13,38 q7,-6 14,0 t14,0" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/>'),
      'maleavel': ('<path d="M17,22 q-4,10 2,17 q5,6 12,6 q7,0 12,-6 q6,-7 2,-17" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
                   '<path d="M23,20 v11 M31,17 v14 M39,20 v11" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/>'),
    }[kind]
    return (f'<svg class="ico" viewBox="0 0 56 56" role="img" aria-hidden="true" style="width:{size}px;height:{size}px">'
            f'<circle cx="28" cy="28" r="26" fill="{col}"/><circle cx="28" cy="28" r="26" fill="none" stroke="{col}" stroke-width="2" opacity=".55"/>{art}</svg>')

def logo(size=104):
    """Marca Reology Map — grafo de nós."""
    nodes=[(52,16),(26,32),(78,32),(20,60),(52,52),(84,60),(38,84),(68,84)]
    edges=[(0,1),(0,2),(1,3),(1,4),(2,4),(2,5),(3,6),(4,6),(4,7),(5,7),(6,7),(0,4)]
    e=''.join(f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" class="lg-e"/>' for a,b in edges)
    n=''.join(f'<circle cx="{x}" cy="{y}" r="{5.2 if i in (0,4) else 3.9}" class="lg-n"/>' for i,(x,y) in enumerate(nodes))
    return f'<svg class="logo" viewBox="0 0 104 100" role="img" aria-label="Reology Map" style="width:{size}px">{e}{n}</svg>'


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


def cap_head(eyebrow, titulo, sub=''):
    """Abertura de capítulo em formato de livro: numeral, ornamento e regra."""
    m = re.match(r'Cap[ií]tulo\s+([0-9]+)', eyebrow)
    num = m.group(1) if m else ''
    resto = eyebrow if not m else eyebrow[m.end():].strip(' ·')
    marca = f'<span class="cap-n">{num}</span>' if num else ''
    extra = f'<span class="cap-extra">{resto}</span>' if resto else ''
    subp = f'<p class="cap-sub">{sub}</p>' if sub else ''
    return (f'<div class="cap-abre">{marca}<div class="cap-tx">'
            f'<p class="cap-eyebrow">{"Capítulo" if num else eyebrow}{extra}</p>'
            f'<h2>{titulo}</h2>{subp}</div>{orn("rede", 108)}</div>')

# ---------------- radar ----------------
def radar(k, fam=None, size=96, cls='radar'):
    c=size/2; R=c-13; v=RK[k]; pts=[]
    for met,ang in [('g1',-90),('g2',0),('td',90),('eta',180)]:
        rad=5+v[met]*(R-5); a=math.radians(ang)
        pts.append((c+rad*math.cos(a), c+rad*math.sin(a)))
    poly=' '.join(f'{x:.1f},{y:.1f}' for x,y in pts)
    grid=''.join(f'<polygon points="{" ".join(f"{c+r*math.cos(math.radians(a)):.1f},{c+r*math.sin(math.radians(a)):.1f}" for a in (-90,0,90,180))}" class="rd-grid"/>' for r in (5+(R-5)/3,5+2*(R-5)/3,R))
    axes=f'<line x1="{c}" y1="{c-R}" x2="{c}" y2="{c+R}" class="rd-ax"/><line x1="{c-R}" y1="{c}" x2="{c+R}" y2="{c}" class="rd-ax"/>'
    d0=DATA[k]; tip=f"G′ {br(d0['G1_0.7Hz'])} · G″ {br(d0['G2_0.7Hz'])} · tan δ {br(td_of(k))} · η* {br(d0['eta_0.7Hz'])}"
    lbl=(f'<text x="{c}" y="9" class="rd-lb" text-anchor="middle">G′</text><text x="{size-2}" y="{c+3}" class="rd-lb" text-anchor="end">G″</text>'
         f'<text x="{c}" y="{size-2}" class="rd-lb" text-anchor="middle">tan δ</text><text x="2" y="{c+3}" class="rd-lb">η*</text>')
    s = sig_cores(k)                      # gramática oficial: 1ª cor G′, 2ª cor tan δ
    fill, stroke = CHIP[s['g1']], CHIP[s['td']]
    dots = ''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.7" fill="{CHIP[s[m]]}" '
                   f'stroke="var(--card)" stroke-width="1"/>'
                   for (x, y), m in zip(pts, ('g1', 'g2', 'td', 'eta')))
    return (f'<svg class="{cls}" viewBox="0 0 {size} {size}" role="img" aria-label="forma reológica"><title>{html.escape(tip)}</title>'
            f'{grid}{axes}<polygon points="{poly}" fill="{fill}" fill-opacity=".20" stroke="{stroke}" stroke-width="2" stroke-linejoin="round"/>'
            + dots + lbl + '</svg>')

def regua(k, fam):
    g1,td = DATA[k]['G1_0.7Hz'], td_of(k); W=168
    cx=xg(g1,W); z2,z3=xg(200,W),xg(300,W); tx=td/0.78*W
    return (f'<svg class="rg" viewBox="0 0 {W+64} 30"><line x1="0" y1="8" x2="{W}" y2="8" class="rg-tr"/>'
            f'<line x1="{z2:.1f}" y1="4" x2="{z2:.1f}" y2="12" class="rg-tick"/><line x1="{z3:.1f}" y1="4" x2="{z3:.1f}" y2="12" class="rg-tick"/>'
            f'<circle cx="{cx:.1f}" cy="8" r="5" fill="var(--fam-{fam})" class="rg-dot"/><text x="{W+6}" y="11" class="rg-lb">G′ {br0(g1)}</text>'
            f'<line x1="0" y1="24" x2="{W}" y2="24" class="rg-tr"/>'
            f'<line x1="{0.15/0.78*W:.1f}" y1="20" x2="{0.15/0.78*W:.1f}" y2="28" class="rg-tick"/>'
            f'<line x1="{0.30/0.78*W:.1f}" y1="20" x2="{0.30/0.78*W:.1f}" y2="28" class="rg-tick"/>'
            f'<circle cx="{tx:.1f}" cy="24" r="5" fill="var(--fam-{fam})" class="rg-dot"/><text x="{W+6}" y="27" class="rg-lb">tanδ {br(td)}</text></svg>')

# ---------------- ilustrações: face e gel ----------------
FACE_ART = """
<defs>
 <radialGradient id="fcSkin" cx="50%" cy="32%" r="78%">
  <stop offset="0%" stop-color="var(--face-hi)"/>
  <stop offset="60%" stop-color="var(--face-fill)"/>
  <stop offset="100%" stop-color="var(--face-sh)"/>
 </radialGradient>
 <linearGradient id="fcHair" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="var(--hair-2)"/>
  <stop offset="100%" stop-color="var(--hair-1)"/>
 </linearGradient>
</defs>
<g class="fc-body">
 <path class="fc-neck" d="M124,322 C125,345 122,357 116,367 C99,374 80,381 67,391
  C62,395 59,398 58,400 L242,400 C241,398 238,395 233,391 C220,381 201,374 184,367
  C178,357 175,345 176,322 Z"/>
 <path class="fc-sh" d="M150,369 C139,369 129,367 121,363 C115,373 111,386 109,400
  L191,400 C189,386 185,373 179,363 C171,367 161,369 150,369 Z"/>
</g>
<path class="fc-hairb" d="M150,60 C205,60 241,97 243,157 C244,192 241,228 234,260
 C231,273 227,284 222,293 L208,284 C217,252 222,215 220,178 C216,130 194,100 150,100
 C106,100 84,130 80,178 C78,215 83,252 92,284 L78,293 C73,284 69,273 66,260
 C59,228 56,192 57,157 C59,97 95,60 150,60 Z"/>
<path class="fc-face" d="M150,344 C174,341 193,326 205,305 C216,287 223,262 225,231 C227,201 226,171 222,147 C218,120 202,102 181,94 C171,90 161,88 150,88 C139,88 129,90 119,94 C98,102 82,120 78,147 C74,171 73,201 75,231 C77,262 84,287 95,305 C107,326 126,341 150,344 Z"/>
<path class="fc-hairf" d="M87,152 C89,112 114,86 150,86 C188,86 216,109 221,152
 C213,129 197,114 177,110 C157,129 116,133 95,124 C91,132 88,141 87,152 Z"/>
<g class="fc-blush"><ellipse cx="102" cy="209" rx="15" ry="9"/><ellipse cx="198" cy="209" rx="15" ry="9"/></g>
<g class="fc-feat">
 <path class="fc-brow" d="M101,152 C112,141 132,139 143,148"/>
 <path class="fc-brow" d="M157,148 C168,139 188,141 199,152"/>
 <path class="fc-eye" d="M104,170 C112,157 130,155 136,171 C129,181 112,182 104,170 Z"/>
 <path class="fc-eye" d="M164,171 C170,155 188,157 196,170 C188,182 171,181 164,171 Z"/>
 <path class="fc-lid" d="M104,170 C112,157 130,155 136,171"/>
 <path class="fc-lid" d="M164,171 C170,155 188,157 196,170"/>
 <path class="fc-crease" d="M105,161 C113,151 131,149 139,158"/>
 <path class="fc-crease" d="M161,158 C169,149 187,151 195,161"/>
 <path class="fc-nose" d="M151,180 C150,196 148,208 147,216"/>
 <path class="fc-nose" d="M139,224 C144,230 156,230 161,224"/>
 <path class="fc-nose" d="M139,224 C133,220 134,212 140,210"/>
 <path class="fc-nose" d="M161,224 C167,220 166,212 160,210"/>
 <path class="fc-lip" d="M125,257 C134,246 144,244 150,250 C156,244 166,246 175,257
  C165,276 135,276 125,257 Z"/>
 <path class="fc-lipline" d="M125,257 C134,246 144,244 150,250 C156,244 166,246 175,257"/>
 <path class="fc-chin" d="M142,300 C146,303 154,303 158,300"/>
</g>
<g class="fc-iris"><circle cx="120" cy="169" r="6.6"/><circle cx="180" cy="169" r="6.6"/></g>
<g class="fc-pupil">
 <circle cx="120" cy="169" r="2.8"/><circle cx="180" cy="169" r="2.8"/>
 <circle class="fc-glint" cx="122.4" cy="166.6" r="1.7"/><circle class="fc-glint" cx="182.4" cy="166.6" r="1.7"/>
</g>
<g class="fc-lash">
 <path d="M104,170 C105,174 106,177 107,179"/><path d="M110,176 C111,180 112,182 113,184"/>
 <path d="M196,170 C195,174 194,177 193,179"/><path d="M190,176 C189,180 188,182 187,184"/>
</g>
"""

def face_svg(width=250, marks=None, cls='facesvg', aria='rosto feminino em vista frontal',
             vw=300, dx=0, leader=False, lx_l=112, lx_r=288):
    """marks: (x, y, cor, label, lado). lado 'L'/'R' com leader até as colunas de rótulo."""
    m = ''
    if marks:
        for mk in marks:
            if leader:
                x, y, c, label, side = mk; x += dx
                if side == 'R':
                    m += (f'<line x1="{x+10}" y1="{y}" x2="{lx_r-5}" y2="{y}" class="fc-ld"/>'
                          f'<text x="{lx_r}" y="{y+4}" class="fc-lb" text-anchor="start">{html.escape(label)}</text>')
                else:
                    m += (f'<line x1="{lx_l+5}" y1="{y}" x2="{x-10}" y2="{y}" class="fc-ld"/>'
                          f'<text x="{lx_l}" y="{y+4}" class="fc-lb" text-anchor="end">{html.escape(label)}</text>')
            else:
                x, y, c, label, anch = mk; x += dx
                if label:
                    lxx = x + (12 if anch == 'start' else -12)
                    m += (f'<line x1="{x}" y1="{y}" x2="{lxx}" y2="{y}" class="fc-ld"/>'
                          f'<text x="{lxx + (4 if anch == "start" else -4)}" y="{y + 3.5}" class="fc-lb" '
                          f'text-anchor="{anch}">{html.escape(label)}</text>')
            m += (f'<circle cx="{x}" cy="{y}" r="12" fill="{CHIP[c]}" class="fc-halo"/>'
                  f'<circle cx="{x}" cy="{y}" r="7.5" fill="{CHIP[c]}" class="fc-dot"/>')
    g0 = f'<g transform="translate({dx},0)">' if dx else ''
    g1 = '</g>' if dx else ''
    return (f'<svg class="{cls}" viewBox="0 0 {vw} 400" role="img" aria-label="{aria}" '
            f'style="max-width:{width}px">{g0}{FACE_ART}{g1}{m}</svg>')

def gel_icons():
    return {
    'gota': '<svg viewBox="0 0 90 90" class="gelico"><path d="M45,10 C45,10 20,42 20,58 a25,25 0 0 0 50,0 C70,42 45,10 45,10 Z" fill="var(--fam-a)" fill-opacity=".25" stroke="var(--fam-a)" stroke-width="2.5"/><ellipse cx="45" cy="80" rx="20" ry="4" fill="var(--fam-a)" fill-opacity=".35"/></svg>',
    'mel': '<svg viewBox="0 0 90 90" class="gelico"><path d="M40,8 C40,26 34,30 34,44 C34,58 46,58 46,44 C46,34 42,30 42,20" fill="none" stroke="var(--fam-m)" stroke-width="7" stroke-linecap="round"/><path d="M20,72 q12,-10 25,0 t25,0" fill="none" stroke="var(--fam-m)" stroke-width="7" stroke-linecap="round"/><path d="M24,82 q10,-7 21,0 t21,0" fill="none" stroke="var(--fam-m)" stroke-width="5" stroke-linecap="round" opacity=".6"/></svg>',
    'rigido': '<svg viewBox="0 0 90 90" class="gelico"><path d="M20,70 L26,34 Q45,22 64,34 L70,70 Z" fill="var(--fam-r)" fill-opacity=".25" stroke="var(--fam-r)" stroke-width="2.5" stroke-linejoin="round"/><path d="M38,38 L34,68 M52,36 L58,68 M27,52 L63,50" stroke="var(--fam-r)" stroke-width="2" opacity=".65"/></svg>',
    }

def box_qr(titulo, texto, qr, url, kind='pratica', ilus=None, ilus_cap=''):
    """Box no padrão dos eBooks do autor: imagem ilustrativa | texto | QR."""
    head = 'NA PRÁTICA' if kind == 'pratica' else 'SAIBA MAIS'
    img = (f'<figure class="bx-ilus"><img src="{ilus}" alt="{html.escape(ilus_cap or titulo)}" loading="lazy">'
           + (f'<figcaption>{html.escape(ilus_cap)}</figcaption>' if ilus_cap else '') + '</figure>') if ilus else ''
    return (f'<aside class="qrbox {kind}"><div class="bx-head">{head}</div><div class="bx-body">{img}'
            f'<div class="bx-txt"><h4>{html.escape(titulo)}</h4><p>{texto}</p>'
            f'<p class="bx-url"><a href="{html.escape(url)}">{html.escape(url)}</a></p></div>'
            f'<div class="bx-qrwrap"><img class="bx-qr" src="{qr}" alt="QR code — {html.escape(titulo)}" width="122" height="122">'
            f'<span>aponte a câmera</span></div></div></aside>')
def box_pratica(titulo, texto, qr, url, ilus=None, ilus_cap=''):
    return box_qr(titulo, texto, qr, url, 'pratica', ilus, ilus_cap)

def figura(num, ilus, legenda, alt='', cls=''):
    return (f'<figure class="figura-img {cls}"><img src="{ilus}" alt="{html.escape(alt or legenda[:80])}" loading="lazy">'
            f'<figcaption><b>Figura {num}.</b> {legenda}</figcaption></figure>')

# ---------------- card ----------------
def card(p):
    k=p['k']; d=DATA[k]; g=grp(p); G=GRUPOS[g]; fam=G['fam']
    g1,g2v,eta = d['G1_0.7Hz'], d['G2_0.7Hz'], d['eta_0.7Hz']; td=td_of(k)
    flags=p.get('fl',[])
    fh = '<p class="flags">'+' · '.join(html.escape(FLAGTXT[x]) for x in flags)+'</p>' if flags else ''
    ind=''.join(f'<span class="pill {NIVEL[n][1]}">{html.escape(r)}<i>{NIVEL[n][0]}</i></span>' for r,n in p['ind'])
    ev=' · '.join(html.escape(e) for e in p['ev'])
    lote = d['lote'] if d['lote'] not in ('','N/D') else 'em revisão'
    tech = f'<p class="tech"><span class="lbl">Fabricante*</span>{html.escape(p["t"].rstrip("*"))}</p>' if p.get('t') and p['t'] not in ('—*',) else ''
    return f'''<article class="card fam-{fam}" id="{slug(k)}">
<header><div class="c-title"><h4>{html.escape(k)}</h4></div>
<div class="c-right"><span class="marca">{html.escape(p['m'])}</span><span class="famtag" style="color:var(--fam-{fam})">G{G['num']} · {G['nome']}</span></div></header>
{sigdots(k)}
{assin_badge(k)}
<div class="vis">{radar(k,fam)}
<div class="vis-col"><div class="sig"><span>G′ <b>{br(g1)}</b> Pa</span><span>G″ <b>{br(g2v)}</b> Pa</span><span>tan δ <b>{br(td)}</b></span><span>η* <b>{br(eta)}</b> Pa·s</span></div>
{regua(k,fam)}<span class="lote">lote {html.escape(lote)}</span></div></div>
<p class="comp">{html.escape(p['comp'])}</p>
<p class="mp"><span class="lbl">Melhor para</span>{html.escape(p['mp'])}</p>
<div class="indwrap"><span class="lbl">Indicações</span><div class="pills">{ind}</div></div>
<p class="evite"><span class="lbl lbl-ev">Evite / não priorize</span>{ev}</p>
<p class="escolha" style="border-color:var(--fam-{fam})">{html.escape(p['esc'])}</p>
<p class="alts"><span class="lbl">Alternativas</span>{html.escape(p['alt'])}</p>
{tech}{fh}</article>'''

# ---------------- gráficos (3 famílias de cor = 1ª cor) ----------------
def famcolor(p):
    return {'G1':'a','G2':'a','G3':'m','G4':'r','G5':'r'}[grp(p)]
LEG3 = ('<div class="legend"><span><i style="background:var(--fam-a)"></i>Baixo G′ — grupos 1–2 (34)</span>'
        '<span><i style="background:var(--fam-m)"></i>Intermediário — grupo 3 (14)</span>'
        '<span><i style="background:var(--fam-r)"></i>Alto G′ — grupos 4–5 (28)</span></div>')

def dot(x,y,fam,k,val):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" class="dot" fill="var(--fam-{fam})" '
            f'data-n="{html.escape(k,quote=True)}" data-v="{html.escape(val,quote=True)}">'
            f'<title>{html.escape(k)} — {html.escape(val)}</title></circle>')

def scatter_main():
    W,H,mL,mB,mT,mR=860,470,52,40,16,120; pw,ph=W-mL-mR,H-mT-mB
    def Y(t): return mT+ph-t/0.78*ph
    s=[f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="Mapa da Reologia">']
    for a,b,cls in [(30,200,'za'),(200,300,'zm'),(300,1000,'zr')]:
        x1,x2=mL+xg(a,pw),mL+xg(b,pw)
        s.append(f'<rect x="{x1:.1f}" y="{mT}" width="{x2-x1:.1f}" height="{ph}" class="{cls}"/>')
    for gv in (50,100,200,300,500,1000):
        x=mL+xg(gv,pw); s.append(f'<line x1="{x:.1f}" y1="{mT}" x2="{x:.1f}" y2="{mT+ph}" class="grid"/><text x="{x:.1f}" y="{H-14}" class="ax" text-anchor="middle">{gv}</text>')
    for tv in [i/10 for i in range(8)]:
        s.append(f'<line x1="{mL}" y1="{Y(tv):.1f}" x2="{mL+pw}" y2="{Y(tv):.1f}" class="grid"/><text x="{mL-8}" y="{Y(tv)+3.5:.1f}" class="ax" text-anchor="end">{br(tv,1)}</text>')
    s.append(f'<text x="{mL+pw/2}" y="{H-1}" class="axt" text-anchor="middle">G′ a 0,7 Hz (Pa · escala log)</text>')
    s.append(f'<text x="14" y="{mT+ph/2}" class="axt" text-anchor="middle" transform="rotate(-90 14 {mT+ph/2})">tan δ a 0,7 Hz</text>')
    s.append(f'<text x="{mL+xg(80,pw):.1f}" y="{mT+14}" class="zlb">BAIXO G′ · espalha/integra</text>')
    s.append(f'<text x="{mL+xg(244,pw):.1f}" y="{mT+14}" class="zlb" text-anchor="middle">INTERMEDIÁRIO</text>')
    s.append(f'<text x="{mL+xg(560,pw):.1f}" y="{mT+14}" class="zlb" text-anchor="middle">ALTO G′ · sustenta/projeta</text>')
    seen={}; pts=[]
    for p in ed.PRODUTOS:
        k=p['k']; g1,td=DATA[k]['G1_0.7Hz'],td_of(k)
        key=(round(g1,2),round(td,2)); off=seen.get(key,0); seen[key]=off+1
        pts.append((mL+xg(g1,pw)+off*5, Y(td), p, g1, td))
    for x,y,p,g1,td in pts: s.append(dot(x,y,famcolor(p),p['k'],f'G′ {br(g1)} Pa · tan δ {br(td)}'))
    LB={'Belotero Balance Lido':('Balance',0,-9,'middle'),'Juvéderm Skinvive':('Skinvive',0,-9,'middle'),
        'Restylane Refyne Lido':('Refyne',0,-9,'middle'),'Restylane Kysse Lido':('Kysse',0,15,'middle'),
        'Juvéderm Volux':('Volux',0,15,'middle'),'Restylane Shaype Lido':('Shaype',0,-9,'middle'),
        'Hyafilia V Plus Lido':('Hyafilia V',-9,3.5,'end'),'Restylane Lyft Lido':('Lyft',0,-9,'middle'),
        'Yvoire Contour+ Lido':('Yvoire Contour+',9,3.5,'start'),'Rennova Lips Plus Lido':('Lips Plus',0,-9,'middle'),
        'Restylane Lido (lote 27003)':('Restylane (27003)',9,3.5,'start'),'Restylane Skinbooster Lido':('Skinbooster',-9,3.5,'end')}
    for x,y,p,g1,td in pts:
        if p['k'] in LB:
            t,dx,dy,anc=LB[p['k']]
            s.append(f'<text x="{x+dx:.1f}" y="{y+dy:.1f}" class="dlb" text-anchor="{anc}">{html.escape(t)}</text>')
    s.append('</svg>'); return ''.join(s)

def scatter_gg():
    W,H,mL,mB,mT,mR=860,470,56,40,16,24; pw,ph=W-mL-mR,H-mT-mB
    YA,YB=math.log10(10),math.log10(260)
    def X(g): return mL+xg(g,pw)
    def Y(g2): return mT+ph-(math.log10(g2)-YA)/(YB-YA)*ph
    s=[f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="G duplo-prima por G prima">']
    for gv in (50,100,200,300,500,1000):
        s.append(f'<line x1="{X(gv):.1f}" y1="{mT}" x2="{X(gv):.1f}" y2="{mT+ph}" class="grid"/><text x="{X(gv):.1f}" y="{H-14}" class="ax" text-anchor="middle">{gv}</text>')
    for gv in (10,20,50,100,200):
        s.append(f'<line x1="{mL}" y1="{Y(gv):.1f}" x2="{mL+pw}" y2="{Y(gv):.1f}" class="grid"/><text x="{mL-8}" y="{Y(gv)+3.5:.1f}" class="ax" text-anchor="end">{gv}</text>')
    for t in (0.07,0.1,0.2,0.4,0.7):
        g2a,g2b=t*30,t*1000; xa,ya=X(30),Y(max(g2a,10))
        if g2a<10: xa=X(10/t); ya=Y(10)
        xb,yb=X(1000),Y(min(g2b,260))
        if g2b>260: xb=X(260/t); yb=Y(260)
        s.append(f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" class="iso"/>')
        anch='start' if xb<mL+pw-4 else 'end'
        s.append(f'<text x="{xb+(4 if anch=="start" else -3):.1f}" y="{yb-4:.1f}" class="isolb" text-anchor="{anch}">tan δ {br(t,2)}</text>')
    s.append(f'<text x="{mL+pw/2}" y="{H-1}" class="axt" text-anchor="middle">G′ a 0,7 Hz (Pa · log)</text>')
    s.append(f'<text x="14" y="{mT+ph/2}" class="axt" text-anchor="middle" transform="rotate(-90 14 {mT+ph/2})">G″ a 0,7 Hz (Pa · log)</text>')
    for p in ed.PRODUTOS:
        k=p['k']; g1,g2v=DATA[k]['G1_0.7Hz'],DATA[k]['G2_0.7Hz']
        s.append(dot(X(g1),Y(g2v),famcolor(p),k,f'G′ {br(g1)} · G″ {br(g2v)} · tan δ {br(td_of(k))}'))
    for k,t,dx,dy,anc in [('Restylane Lido (lote 27003)','Restylane (27003)',-9,3.5,'end'),('Restylane Skinbooster Lido','Skinbooster',-9,3.5,'end'),
                          ('Juvéderm Volux','Volux',0,15,'middle'),('Restylane Defyne Lido','Defyne',0,15,'middle'),
                          ('Belotero Balance Lido','Balance',9,3.5,'start'),('Restylane Shaype Lido','Shaype',0,-9,'middle'),
                          ('Rennova Lift Plus Lido','Lift Plus',0,15,'middle'),('Juvéderm Skinvive','Skinvive',0,-9,'middle')]:
        g1,g2v=DATA[k]['G1_0.7Hz'],DATA[k]['G2_0.7Hz']
        s.append(f'<text x="{X(g1)+dx:.1f}" y="{Y(g2v)+dy:.1f}" class="dlb" text-anchor="{anc}">{t}</text>')
    s.append('</svg>'); return ''.join(s)

def scatter_eta():
    W,H,mL,mB,mT,mR=860,470,64,40,16,24; pw,ph=W-mL-mR,H-mT-mB
    YA,YB=math.log10(140),math.log10(13000)
    def X(g): return mL+xg(g,pw)
    def Y(e): return mT+ph-(math.log10(e)-YA)/(YB-YA)*ph
    s=[f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="Viscosidade em repouso por G prima">']
    for gv in (50,100,200,300,500,1000):
        s.append(f'<line x1="{X(gv):.1f}" y1="{mT}" x2="{X(gv):.1f}" y2="{mT+ph}" class="grid"/><text x="{X(gv):.1f}" y="{H-14}" class="ax" text-anchor="middle">{gv}</text>')
    for ev in (200,500,1000,2000,5000,10000):
        s.append(f'<line x1="{mL}" y1="{Y(ev):.1f}" x2="{mL+pw}" y2="{Y(ev):.1f}" class="grid"/><text x="{mL-8}" y="{Y(ev)+3.5:.1f}" class="ax" text-anchor="end">{br0(ev)}</text>')
    s.append(f'<text x="{mL+pw/2}" y="{H-1}" class="axt" text-anchor="middle">G′ a 0,7 Hz (Pa · log)</text>')
    s.append(f'<text x="14" y="{mT+ph/2}" class="axt" text-anchor="middle" transform="rotate(-90 14 {mT+ph/2})">η* em repouso (Pa·s · log)</text>')
    for p in ed.PRODUTOS:
        k=p['k']; g1,e=DATA[k]['G1_0.7Hz'],DATA[k]['eta_0.01Hz']
        s.append(dot(X(g1),Y(e),famcolor(p),k,f'G′ {br(g1)} Pa · η* repouso {br0(e)} Pa·s'))
    for k,t,dx,dy,anc in [('Restylane Shaype Lido','Shaype',0,-9,'middle'),('Hyafilia V Plus Lido','Hyafilia V',-9,3.5,'end'),
                          ('Belotero Balance Lido','Balance',9,3.5,'start'),('Juvéderm Skinvive','Skinvive',9,3.5,'start'),
                          ('Restylane Lyft Lido','Lyft',9,3.5,'start'),('Juvéderm Volux','Volux',-9,3.5,'end'),
                          ('Neuramis Lido','Neuramis',0,-9,'middle')]:
        g1,e=DATA[k]['G1_0.7Hz'],DATA[k]['eta_0.01Hz']
        s.append(f'<text x="{X(g1)+dx:.1f}" y="{Y(e)+dy:.1f}" class="dlb" text-anchor="{anc}">{t}</text>')
    s.append('</svg>'); return ''.join(s)

def ranking(metric,title_axis,maxv,fmt,grids):
    rows=sorted(ed.PRODUTOS,key=lambda p:(DATA[p['k']]['G1_0.7Hz'] if metric=='g1' else td_of(p['k'])),reverse=True)
    rh,gap,mT,mB,mL,mR=13,2.6,8,30,196,58; W=860; ph=len(rows)*(rh+gap); H=mT+ph+mB; pw=W-mL-mR
    def val(p): return DATA[p['k']]['G1_0.7Hz'] if metric=='g1' else td_of(p['k'])
    s=[f'<svg class="chart chart-rank" viewBox="0 0 {W} {H}" role="img" aria-label="ranking">']
    for gv in grids:
        x=mL+gv/maxv*pw
        s.append(f'<line x1="{x:.1f}" y1="{mT}" x2="{x:.1f}" y2="{mT+ph}" class="grid"/><text x="{x:.1f}" y="{H-12}" class="ax" text-anchor="middle">{fmt(gv)}</text>')
    y=mT
    for p in rows:
        k=p['k']; v=val(p); bw=v/maxv*pw; fam=famcolor(p)
        s.append(f'<text x="{mL-6}" y="{y+rh-3}" class="bn" text-anchor="end">{html.escape(short(k))}</text>')
        s.append(f'<rect x="{mL}" y="{y}" width="{max(bw,2):.1f}" height="{rh}" rx="3.5" fill="var(--fam-{fam})" class="bar"><title>{html.escape(k)} — {fmt(v)}</title></rect>')
        s.append(f'<text x="{mL+bw+5:.1f}" y="{y+rh-3}" class="bv">{fmt(v)}</text>')
        y+=rh+gap
    s.append(f'<text x="{mL+pw/2}" y="{H-1}" class="axt" text-anchor="middle">{title_axis}</text></svg>')
    return ''.join(s)

def emblema(size=200):
    c=size/2; R=c-16; polys=[]
    for k,fam in [('Belotero Balance Lido','a'),('Saypha Volume Lido','m'),('Juvéderm Volux','r'),('Restylane Lido (lote 22647)','v')]:
        v=RK[k]; pts=[]
        for met,ang in [('g1',-90),('g2',0),('td',90),('eta',180)]:
            rad=6+v[met]*(R-6); a=math.radians(ang)
            pts.append(f'{c+rad*math.cos(a):.1f},{c+rad*math.sin(a):.1f}')
        polys.append(f'<polygon points="{" ".join(pts)}" fill="var(--fam-{fam})" fill-opacity=".17" stroke="var(--fam-{fam})" stroke-width="2.2" stroke-linejoin="round"/>')
    grid=''.join(f'<polygon points="{" ".join(f"{c+r*math.cos(math.radians(a)):.1f},{c+r*math.sin(math.radians(a)):.1f}" for a in (-90,0,90,180))}" class="rd-grid"/>' for r in (6+(R-6)/3,6+2*(R-6)/3,R))
    axes=f'<line x1="{c}" y1="{c-R}" x2="{c}" y2="{c+R}" class="rd-ax"/><line x1="{c-R}" y1="{c}" x2="{c+R}" y2="{c}" class="rd-ax"/>'
    lbl=(f'<text x="{c}" y="11" class="rd-lb" text-anchor="middle">G′</text><text x="{size-3}" y="{c+3.5}" class="rd-lb" text-anchor="end">G″</text>'
         f'<text x="{c}" y="{size-3}" class="rd-lb" text-anchor="middle">tan δ</text><text x="3" y="{c+3.5}" class="rd-lb">η*</text>')
    return f'<svg class="capa-emb" viewBox="0 0 {size} {size}" role="img" aria-label="assinaturas reológicas">{grid}{axes}{"".join(polys)}{lbl}</svg>'


# ---------------- rankings temáticos (recalculados do banco, 76 ensaios) --------
def top(metric, n=10, maior=True, filtro=None, cor='g1'):
    """Ranking temático direto do banco canônico — nunca de tabela transcrita."""
    def v(r):
        return {'g1': r['G1_0.7Hz'], 'g2': r['G2_0.7Hz'],
                'td': ERR_TD.get(r['produto'], r['tand_0.7Hz']),
                'eta': r['eta_0.7Hz']}[metric]
    rs = [r for r in DATA.values() if v(r) is not None and (filtro(r) if filtro else True)]
    rs.sort(key=v, reverse=maior)
    return rs[:n]

def podio(rows, metric, titulo, nota='', fmt=None):
    fmt = fmt or (lambda x: br(x, 2) if metric == 'td' else br(x, 2))
    def v(r):
        return {'g1': r['G1_0.7Hz'], 'g2': r['G2_0.7Hz'],
                'td': ERR_TD.get(r['produto'], r['tand_0.7Hz']),
                'eta': r['eta_0.7Hz']}[metric]
    tr = ''
    for i, r in enumerate(rows, 1):
        k = r['produto']
        g1 = r['G1_0.7Hz']; td = ERR_TD.get(k, r['tand_0.7Hz'])
        fam = c_g1(g1)
        comp = (f'tan δ {br(td,2)}' if metric == 'g1'
                else (f'G′ {br(g1,2)} Pa' if metric == 'td'
                      else f'G′ {br(g1,2)} · tan δ {br(td,2)}'))
        tr += (f'<tr><td class="pd-n">{i}</td>'
               f'<td class="pd-p">{dotchip(fam,10)} {html.escape(short(k))}'
               f'<span class="pd-as">{assinatura(k)[0]}</span></td>'
               f'<td class="pd-v">{fmt(v(r))}</td>'
               f'<td class="pd-x">{comp}</td></tr>')
    un = {'g1': 'G′ (Pa)', 'g2': 'G″ (Pa)', 'td': 'tan δ', 'eta': 'η* (Pa·s)'}[metric]
    n = f'<p class="pd-nota">{nota}</p>' if nota else ''
    hx = {'g1': 'tan δ', 'td': 'G′'}.get(metric, 'Perfil')
    return (f'<div class="podio"><h4>{titulo}</h4><table><thead><tr><th></th><th>Produto</th>'
            f'<th>{un}</th><th>{hx}</th></tr></thead><tbody>{tr}</tbody></table>{n}</div>')

OUTRAS_FONTES = [('Belotero Balance Lido', '128', '0,64', 'lit', 'Literatura publicada'), ('Belotero Intense Lido', '255', '0,43', 'lit', 'Literatura publicada'), ('Belotero Volume + Lido', '438', '0,23', 'lit', 'Literatura publicada'), ('e.p.t.q S 100 Lido', '36', '0,46', 'fab', 'Fabricante (Anton Paar MCR302 · 0,1 Hz)'), ('e.p.t.q S 300 Lido', '144', '0,19', 'fab', 'Fabricante (Anton Paar MCR302 · 0,1 Hz)'), ('e.p.t.q S 500 Lido', '232', '0,14', 'fab', 'Fabricante (Anton Paar MCR302 · 0,1 Hz)'), ('Yvoire Classic+ Lido', '286', '0,36', 'lit', 'Estudo comparativo de linha'), ('Yvoire Volume+ Lido', '253', '0,29', 'lit', 'Estudo comparativo de linha'), ('Yvoire Contour+ Lido', '484', '0,32', 'lit', 'Estudo comparativo de linha')]

_ROWS_FONTES = ''
for _p, _g, _t, _kind, _fonte in OUTRAS_FONTES:
    _r = DATA[_p]; _td = ERR_TD.get(_p, _r['tand_0.7Hz'])
    _ddir = '↑' if float(_g.replace(',', '.')) > _r['G1_0.7Hz'] else '↓'
    _ROWS_FONTES += (f'<tr><td><b>{html.escape(short(_p))}</b></td>'
        f'<td class="med">G′ {br(_r["G1_0.7Hz"],2)}<br>tan δ {br(_td,2)}</td>'
        f'<td class="out">G′ {_g} {_ddir}<br>tan δ {_t}</td>'
        f'<td>{_fonte}</td></tr>')


# ---------------- mapa anatômico: regiões faciais por grupo ----------------
FACE_CLIP = ("M150,344 C174,341 193,326 205,305 C216,287 223,262 225,231 C227,201 226,171 222,147 C218,120 202,102 181,94 C171,90 161,88 150,88 C139,88 129,90 119,94 C98,102 82,120 78,147 C74,171 73,201 75,231 C77,262 84,287 95,305 C107,326 126,341 150,344 Z")

# lado esquerdo do observador; as bilaterais são espelhadas por transform
REG = {
 'fronte':      ('c', 'M91,133 C93,103 119,95 150,95 C181,95 207,103 209,133 '
                      'C180,140 120,140 91,133 Z'),
 'temporal':    ('b', 'M96,122 C94,142 93,162 95,182 L75,188 C69,168 67,144 71,124 Z'),
 'supercilio':  ('b', 'M97,157 C109,143 131,141 143,150 L141,160 C130,152 111,153 100,164 Z'),
 'infraorb':    ('b', 'M101,182 C110,177 130,178 139,184 C134,199 112,202 102,192 Z'),
 'zigoma':      ('b', 'M78,193 C92,187 112,192 126,203 C124,212 118,216 110,212 '
                      'C98,206 86,203 77,203 Z'),
 'bochecha':    ('b', 'M88,222 C101,217 118,222 127,232 C125,249 107,258 91,249 Z'),
 'auricular':   ('b', 'M80,204 C80,222 82,240 86,258 L62,266 C56,250 52,230 50,200 Z'),
 'nariz':       ('c', 'M144,162 C147,158 153,158 156,162 C157,186 158,204 160,214 '
                      'C158,225 142,225 140,214 C142,204 143,186 144,162 Z'),
 'nasolabial':  ('b', 'M132,217 C124,229 118,246 120,266 L131,268 C129,250 132,234 140,224 Z'),
 'labios':      ('c', 'M125,257 C134,246 144,244 150,250 C156,244 166,246 175,257 '
                      'C165,276 135,276 125,257 Z'),
 'perioral':    ('c', 'M117,252 C126,239 141,241 150,245 C159,241 174,239 183,252 '
                      'C181,270 169,285 150,287 C131,285 119,270 117,252 Z'
                      'M125,257 C135,276 165,276 175,257 C166,246 156,244 150,250 '
                      'C144,244 134,246 125,257 Z'),
 'labiomentual':('c', 'M132,281 C140,275 160,275 168,281 C161,291 139,291 132,281 Z'),
 'mento':       ('c', 'M129,295 C139,290 161,290 171,295 C172,316 163,331 150,336 '
                      'C137,331 128,316 129,295 Z'),
 'mandibula':   ('b', 'M78,228 C82,266 96,300 124,326 L116,350 C74,326 46,290 38,234 Z'),
 'prejowl':     ('b', 'M108,298 C118,293 130,298 135,307 C128,320 112,320 105,311 Z'),
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

FACE_FEATS = FACE_ART[FACE_ART.index('<g class="fc-feat">'):]

def face_regioes(g, width=196, cls='facereg'):
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
    return (f'<svg class="{cls}" viewBox="0 0 300 400" role="img" '
            f'style="width:{width}px;--rg-f:{fill};--rg-s:{stroke}" '
            f'aria-label="regiões faciais do grupo {g["n"]}: {html.escape(g["txt"])}">'
            f'<defs><clipPath id="{uid}"><path d="{FACE_CLIP}"/></clipPath></defs>'
            f'{FACE_ART}<g clip-path="url(#{uid})">{shapes}</g>'
            f'<path d="{FACE_CLIP}" class="fc-edge"/>{FACE_FEATS}</svg>')

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


# ---------------- capítulo da forma: eixos e famílias ----------------
def faixa_banco(campo):
    vs = [r[campo] for r in DATA.values() if r[campo] is not None]
    return min(vs), max(vs)

EIXOS = [
 ('g1', 'G′', 'cima', 'Módulo elástico', 'a',
  'A mola: energia que o gel devolve. É o que sustenta forma sob carga.',
  [('a', 'menos de 200 Pa'), ('m', '200 a 300 Pa'), ('r', 'mais de 300 Pa')], 'G1_0.7Hz', 'Pa'),
 ('g2', 'G″', 'direita', 'Módulo viscoso', 'a',
  'O amortecedor: energia dissipada. Só significa alguma coisa lido em relação ao G′.',
  [('a', 'menos de 50 Pa'), ('m', '50 a 100 Pa'), ('r', 'mais de 100 Pa')], 'G2_0.7Hz', 'Pa'),
 ('td', 'tan δ', 'baixo', 'Balanço viscoelástico', 'r',
  'A razão G″/G′ — qual dos dois comportamentos manda. É uma proporção, nunca uma força.',
  [('r', 'até 0,15 · elástico'), ('v', '0,15 a 0,20 · maleável'), ('p', 'acima de 0,20 · dinâmico')],
  'tand_0.7Hz', ''),
 ('eta', 'η*', 'esquerda', 'Viscosidade complexa', 'a',
  'Resistência global ao escoamento. Proxy de permanência — dispara em repouso.',
  [('a', 'menos de 50 Pa·s'), ('m', '50 a 100 Pa·s'), ('r', 'mais de 100 Pa·s')], 'eta_0.7Hz', 'Pa·s'),
]

def eixos_cards():
    out = ''
    for met, simb, pos, nome, _c, desc, cortes, campo, un in EIXOS:
        lo, hi = faixa_banco(campo)
        nd = 2 if met == 'td' else 1
        chips = ''.join(f'<li>{dotchip(c, 11)} {t}</li>' for c, t in cortes)
        out += (f'<div class="eixo eixo-{met}"><span class="ex-pos">{pos}</span>'
                f'<b class="ex-s">{simb}</b><span class="ex-n">{nome}</span>'
                f'<p>{desc}</p><ul class="ex-cut">{chips}</ul>'
                f'<span class="ex-faixa">no banco: {br(lo, nd)} a {br(hi, nd)} {un}</span></div>')
    return f'<div class="eixos">{out}</div>'

FAMILIAS_FORMA = [
 ('1', 'BAIXO G′', ['a', 'p'], 'Belotero Balance Lido',
  'Azul preenchendo, rosa no contorno. Pouca estrutura e tan δ alto: a forma cai para baixo.'),
 ('2', 'BAIXO G′ VOLUMIZADOR', ['a', 'm', 'p'], 'Belotero Intense Lido',
  'Azul no G′, amarelo no G″, rosa no tan δ. Mesma família, com corpo: a forma abre para a direita.'),
 ('3', 'MÉDIO G′', ['m'], 'Belotero Volume + Lido',
  'Amarelo preenchendo — a cor do vale. A forma se centra: preenche e equilibra sem impor '
  'projeção. O contorno rosa lembra que a família é amarela, mas este exemplar mediu tan δ 0,23.'),
 ('4', 'ALTO G′', ['r'], 'Restylane Shaype Lido',
  'Roxo nos quatro eixos — o roxo completo do grupo 4. A forma aponta para cima e para a '
  'esquerda: estrutura e permanência.'),
]

def familias_forma():
    out = ''
    for n, nome, cores, k, txt in FAMILIAS_FORMA:
        chips = ''.join(dotchip(c, 13) for c in cores)
        nomes = ' + '.join(CNAME[c] for c in cores)
        d = DATA[k]
        out += (f'<figure class="ffam">'
                f'<figcaption><span class="ff-n">{n}</span><span class="ff-t">{nome}</span></figcaption>'
                f'<div class="ff-chips">{chips}<span>{nomes}</span></div>'
                f'{radar(k, None, 140, "radar radar-lg")}'
                f'<p class="ff-p"><b>{html.escape(short(k))}</b> · {assinatura(k)[0]}</p>'
                f'<p class="ff-v">G′ {br(d["G1_0.7Hz"])} · G″ {br(d["G2_0.7Hz"])} · '
                f'tan δ {br(td_of(k), 2)} · η* {br(d["eta_0.7Hz"])}</p>'
                f'<p class="ff-d">{txt}</p></figure>')
    return f'<div class="ffams">{out}</div>'


# ---------------- capítulo 1: diagramas nativos ----------------
def figura_nat(num, conteudo, legenda):
    """Figura nativa — mesma moldura das pranchas, conteúdo em SVG/HTML."""
    return (f'<figure class="figura-nat"><div class="fn-in">{conteudo}</div>'
            f'<figcaption><b>Figura {num}.</b> {legenda}</figcaption></figure>')

MEDIDOS = [
 ('G′', 'Módulo elástico', 'cima', ['a', 'm', 'r'], ['200', '300'], 'Pa',
  'Quanto o gel devolve de energia — o que sustenta forma.'),
 ('G″', 'Módulo viscoso', 'direita', ['a', 'm', 'r'], ['50', '100'], 'Pa',
  'Quanto dissipa. Só significa algo lido em relação ao G′.'),
 ('tan δ', 'Balanço', 'baixo', ['r', 'v', 'p'], ['0,15', '0,20'], '',
  'A razão G″/G′ — qual comportamento manda.'),
 ('η*', 'Viscosidade complexa', 'esquerda', ['a', 'm', 'r'], ['50', '100'], 'Pa·s',
  'Resistência global ao escoamento.'),
]

NAO_MEDIDOS = [
 ('Swelling factor', 'Quanto o gel incha ao captar água. Governa edema e previsibilidade.'),
 ('Coesividade', 'Capacidade de se manter unido no tecido, sem se fragmentar.'),
 ('Força de extrusão', 'Quanto esforço a injeção exige na seringa e na agulha.'),
 ('Strain / amplitude', 'Até onde o gel deforma antes de romper a estrutura.'),
]

def painel_medidas():
    med = ''
    for simb, nome, pos, cores, cortes, un, desc in MEDIDOS:
        segs = ''.join(f'<span style="background:{CHIP[c]}"></span>' for c in cores)
        marks = ''.join(f'<i>{v}</i>' for v in cortes)
        med += (f'<div class="medc"><div class="mc-h"><b>{simb}</b>'
                f'<span class="mc-pos">{pos}</span></div>'
                f'<span class="mc-n">{nome}</span><p>{desc}</p>'
                f'<div class="mc-bar">{segs}</div><div class="mc-cut">{marks}'
                f'<em>{un}</em></div></div>')
    nao = ''.join(f'<div class="nmedc"><b>💧 {n}</b><p>{d}</p></div>' for n, d in NAO_MEDIDOS)
    return (f'<div class="medpanel">'
            f'<div class="mp-lado mp-sim"><h4>Medido neste estudo</h4>'
            f'<p class="mp-sub">Quatro números por produto, a 0,7 Hz, com lote identificado. '
            f'São eles — e só eles — que geram cor, grupo, assinatura e ranking.</p>'
            f'<div class="medgrid">{med}</div></div>'
            f'<div class="mp-lado mp-nao"><h4>Não medido nesta rodada</h4>'
            f'<p class="mp-sub">Aparecem sempre marcados com 💧. São citados quando o fabricante '
            f'ou a literatura os declara — e <b>nunca deduzidos</b> a partir dos quatro medidos.</p>'
            f'<div class="nmedgrid">{nao}</div></div></div>')

PASSOS4 = [
 ('1', '1ª COR', 'G′ — quanto o gel estrutura',
  [('a', 'baixo', 'espalha e integra'), ('m', 'intermediário', 'preenche e equilibra'),
   ('r', 'alto', 'sustenta e projeta')],
  'Define a <b>família</b> do gel.'),
 ('2', '2ª COR', 'tan δ — como essa estrutura se comporta',
  [('r', 'elástico', 'até 0,15'), ('v', 'maleável', '0,15 a 0,20'),
   ('p', 'dinâmico', 'acima de 0,20')],
  'Define o <b>modificador</b> da família.'),
]

def esquema_passos():
    cols = ''
    for n, tit, sub, linhas, nota in PASSOS4:
        li = ''.join(f'<li>{dotchip(c, 12)}<b>{lab}</b><span class="p4-d">{txt}</span></li>'
                     for c, lab, txt in linhas)
        cols += (f'<div class="p4"><span class="p4-n">{n}</span>'
                 f'<h5>{tit}</h5><p class="p4-s">{sub}</p>'
                 f'<ul class="p4-l">{li}</ul><p class="p4-nota">{nota}</p></div>')
    # passo 3: a soma
    ex = ('<div class="p4"><span class="p4-n">3</span><h5>ASSINATURA</h5>'
          '<p class="p4-s">1ª cor + 2ª cor = o nome oficial do perfil</p>'
          '<div class="p4-soma">'
          f'<span>{dotchip("a", 15)}</span><em>+</em><span>{dotchip("p", 15)}</span>'
          '<em>=</em><b>INTEGRATIVO<br>DINÂMICO</b></div>'
          '<p class="p4-nota">Três famílias × três comportamentos = <b>nove assinaturas</b>. '
          'Quando o tan δ é baixo, a estrutura fala mais alto e o nome fica puro: '
          '<b>ESPALHA</b>, <b>PREENCHE</b>, <b>PROJETA</b>.</p></div>')
    q = ('<div class="p4"><span class="p4-n">4</span><h5>LEITURA CLÍNICA</h5>'
         '<p class="p4-s">A assinatura responde três perguntas</p>'
         '<ol class="p4-q"><li>O que eu quero fazer aqui — espalhar, preencher ou projetar?</li>'
         '<li>Esse tecido se move muito?</li>'
         '<li>Preciso moldar e distribuir o produto?</li></ol>'
         '<p class="p4-nota">A região entra depois, no capítulo 5; a forma dos quatro números, '
         'no capítulo 6.</p></div>')
    return f'<div class="passos4">{cols}{ex}{q}</div>'

ROTEIRO = [
 ('1', 'Como ler este guia', 'a'), ('2–3', 'A molécula, a rede e a viscoelasticidade', 'a'),
 ('4', 'Os quatro números', 'm'), ('5', 'O mapa: três famílias sobre a face', 'm'),
 ('6', 'A forma do gel', 'm'), ('7', 'Textura visual', 'm'),
 ('8', 'Atlas de gráficos', 'r'), ('9–14', 'As famílias em seis grupos, produto a produto', 'r'),
 ('15', 'Rankings completos', 'r'), ('16', 'Quando as fontes discordam', 's'),
 ('17', 'Guia rápido por região', 's'),
]

def roteiro():
    it = ''.join(f'<li class="rt-{c}"><b>{n}</b><span>{t}</span></li>' for n, t, c in ROTEIRO)
    return f'<ol class="roteiro">{it}</ol>'


# ---------------- AS TRÊS FAMÍLIAS (estrutura principal do livro) ----------------
REG_AZUL = ['perioral', 'labios', 'temporal', 'fronte', 'supercilio', 'nasolabial', 'labiomentual']
REG_AMAR = ['labiomentual', 'nasolabial', 'prejowl', 'bochecha', 'auricular', 'mandibula']
REG_ROXO = ['mento', 'nariz', 'zigoma', 'mandibula', 'temporal', 'infraorb']

FAMILIAS = [
 dict(n='1', nome='BAIXO G′', cor='a', grupos='grupos 1 e 2', regs=REG_AZUL,
      sub=[('azul + rosa', ['a', 'p']), ('azul + amarelo + rosa', ['a', 'm', 'p'])],
      lead='Integra, acompanha o movimento e cria pouco relevo próprio.',
      regs_txt='Região oral e perioral · lábio · têmpora, fronte e supercílio · '
               'sulco nasolabial · sulco labiomentual.',
      nota='<b>As duas assinaturas atendem as mesmas regiões.</b> A diferença entre '
           'azul + rosa e azul + amarelo + rosa é <i>quanto</i> cada uma valoriza — '
           'a segunda entrega um pouco mais de volume. A indicação não muda.'),
 dict(n='2', nome='MODERADO G′', cor='m', grupos='grupo 3', regs=REG_AMAR,
      sub=[('amarelo', ['m'])],
      lead='Preenche e equilibra: corpo sem impor projeção.',
      regs_txt='Sulco labiomentual e sulco nasolabial · pré-jowl · bochecha · '
               'região auricular anterior · valorização de mandíbula.',
      nota='A família de transição — a cor do vale. Uma assinatura só, sem subclasse: '
           'é o produto que preenche onde não se quer nem espalhar nem projetar.'),
 dict(n='3', nome='ALTO G′', cor='r', grupos='grupos 4 e 5', regs=REG_ROXO,
      sub=[('roxo puro', ['r']), ('roxo + 2ª cor', ['r', 'v']), ('na olheira 💧', ['r', 's'])],
      lead='Sustenta. Conforme a segunda cor, projeta ou volumiza.',
      regs_txt='Mento · nariz · arco zigomático · mandíbula · têmpora (crown lift) · '
               'e, no uso preciso, a região infraorbitária.',
      nota='<b>Três usos, não um.</b> O <b>roxo puro</b> projeta — é o vértice. '
           'O <b>roxo com segunda cor</b> volumiza, com menos projeção. E o mesmo alto G′, '
           'quando tem baixo swelling factor, é o que se usa na <b>olheira</b>.'),
]

USOS_ROXO = [
 ('PROJEÇÃO', ['r'], ['mento', 'nariz', 'zigoma', 'mandibula'],
  'Roxo puro: tan δ baixo, estrutura sem modificador. Mantém o vértice onde foi colocado.'),
 ('VOLUMIZAÇÃO', ['r', 'v'], ['mandibula', 'zigoma', 'temporal', 'nasolabial', 'mento'],
  'Roxo com segunda cor: sustenta com mais curva e mais corpo. Volume estrutural, '
  'não projeção focal.'),
 ('OLHEIRA', ['r', 's'], ['infraorb'],
  'Alto G′ de <b>baixo swelling factor</b> — baixa concentração de AH e partículas grandes. '
  'É a exceção que a família comporta: estrutura numa região que não tolera inchaço. 💧'),
]

def face_fam(f, width=210, cls='facereg'):
    g = dict(n=f['n'], regs=f['regs'], cores=[f['cor'], f['sub'][-1][1][-1]], txt=f['regs_txt'])
    return face_regioes(g, width, cls)

def mapa_familias():
    cards = ''
    for f in FAMILIAS:
        subs = ''.join(
            f'<span class="fm-sub">{"".join(dotchip(c, 11) for c in cores)}<em>{nome}</em></span>'
            for nome, cores in f['sub'])
        cards += (f'<figure class="famcard fc-{f["cor"]}">'
                  f'<figcaption><span class="fm-n">{f["n"]}</span>'
                  f'<span class="fm-t">{f["nome"]}</span>'
                  f'<span class="fm-g">{f["grupos"]}</span></figcaption>'
                  f'<p class="fm-lead">{f["lead"]}</p>'
                  f'<div class="fm-subs">{subs}</div>'
                  f'{face_fam(f)}'
                  f'<p class="fm-regs">{f["regs_txt"]}</p>'
                  f'<p class="fm-nota">{f["nota"]}</p></figure>')
    return f'<div class="mapafam">{cards}</div>'

def usos_roxo():
    out = ''
    for nome, cores, regs, txt in USOS_ROXO:
        g = dict(n='3', regs=regs, cores=cores, txt=nome)
        chips = ''.join(dotchip(c, 12) for c in cores)
        out += (f'<figure class="usocard"><figcaption>{chips}<b>{nome}</b></figcaption>'
                f'{face_regioes(g, 150)}<p>{txt}</p></figure>')
    return f'<div class="usos">{out}</div>'



# ---------------- arte da capa: varredura de frequência + rede molecular ----------------
CAPA_CURVAS = [('Restylane Shaype Lido', 'c-r'), ('Belotero Volume + Lido', 'c-m'),
               ('Belotero Balance Lido', 'c-a')]
CAPA_FRQ = [(0.01, '0.01Hz'), (0.1, '0.1Hz'), (0.7, '0.7Hz'), (1.0, '1Hz'), (5.0, '5Hz'), (10.0, '10Hz')]

def _suave(pts):
    """Catmull-Rom convertida em bézier: curva contínua pelos pontos medidos."""
    if len(pts) < 3:
        return 'M' + ' L'.join(f'{x},{y}' for x, y in pts)
    d = f'M{pts[0][0]},{pts[0][1]}'
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i else pts[0]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f' C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]},{p2[1]}'
    return d

def _hexring(cx, cy, r, rot=0):
    return [(round(cx + r * math.cos(math.radians(a + rot)), 1),
             round(cy + r * math.sin(math.radians(a + rot)), 1)) for a in range(30, 390, 60)]

def capa_arte():
    """Arte central da capa, nativa e auditável: as curvas são G′ medido a
    0,01–10 Hz de um produto de cada família — não são traço decorativo."""
    gx0, gx1, gy0, gy1 = 104, 556, 44, 424
    LX0, LX1 = -2.0, 2.0
    LY0, LY1 = math.log10(7), math.log10(1500)
    def px(f): return round(gx0 + (math.log10(f) - LX0) / (LX1 - LX0) * (gx1 - gx0), 1)
    def py(v): return round(gy1 - (math.log10(v) - LY0) / (LY1 - LY0) * (gy1 - gy0), 1)

    # ondas decorativas ao fundo — o gel escoando sob solicitação
    ondas = ''
    for i in range(9):
        amp = 34 - i * 2.2
        yb = 96 + i * 21
        ph = i * 33.0
        op = round(.34 - i * .030, 3)
        pts = [(round(x, 1),
                round(yb - amp * math.sin((x + ph - 40) / 190)
                      - amp * .42 * math.sin((x + ph * 1.7 - 40) / 71)
                      - amp * .18 * math.sin((x - ph - 40) / 38), 1))
               for x in range(20, 1011, 22)]
        ondas += f'<path d="{_suave(pts)}" class="cp-onda" opacity="{op}"/>'

    # eixos e escala logarítmica
    eixos = (f'<path d="M{gx0},{gy0 - 6} L{gx0},{gy1} L{gx1 + 16},{gy1}" class="cp-eixo"/>')
    for e in range(-2, 3):
        x = px(10 ** e)
        sup = {-2: '⁻²', -1: '⁻¹', 0: '⁰', 1: '¹', 2: '²'}[e]
        eixos += (f'<path d="M{x},{gy1} L{x},{gy1 + 7}" class="cp-eixo"/>'
                  f'<text x="{x}" y="{gy1 + 26}" class="cp-tick" text-anchor="middle">10{sup}</text>')
    for v in (10, 100, 1000):
        y = py(v)
        eixos += (f'<path d="M{gx0 - 6},{y} L{gx0},{y}" class="cp-eixo"/>'
                  f'<path d="M{gx0},{y} L{gx1 + 16},{y}" class="cp-grade"/>')
    eixos += (f'<text x="{gx0 - 18}" y="{(gy0 + gy1) / 2}" class="cp-ax" text-anchor="middle" '
              f'transform="rotate(-90 {gx0 - 18} {(gy0 + gy1) / 2})">G′, G″ (Pa)</text>'
              f'<text x="{(gx0 + gx1) / 2}" y="{gy1 + 50}" class="cp-ax" text-anchor="middle">Frequência (Hz)</text>')

    # curvas medidas: G′ de um produto por família, com as contas nos pontos reais
    curvas = ''
    for k, cls in CAPA_CURVAS:
        r = DATA[k]
        pts = [(px(f), py(r[f'G1_{fk}'])) for f, fk in CAPA_FRQ]
        curvas += f'<path d="{_suave(pts)}" class="cp-linha {cls}"/>'
        curvas += ''.join(f'<circle cx="{x}" cy="{y}" r="3.1" class="cp-pt {cls}"/>' for x, y in pts)
    # G″ do estrutural, tracejado — o contraponto viscoso
    kr = CAPA_CURVAS[0][0]
    ptsg2 = [(px(f), py(DATA[kr][f'G2_{fk}'])) for f, fk in CAPA_FRQ]
    curvas += f'<path d="{_suave(ptsg2)}" class="cp-linha cp-g2"/>'

    # rede molecular: anéis fundidos em bola-e-bastão, pendentes ancorados
    bonds, atoms = '', {}
    CEN = [(752, 248, 64), (860, 184, 64), (868, 318, 64)]
    rings = [_hexring(cx, cy, r) for cx, cy, r in CEN]
    for ring in rings:
        for i, p in enumerate(ring):
            q = ring[(i + 1) % 6]
            bonds += f'<line x1="{p[0]}" y1="{p[1]}" x2="{q[0]}" y2="{q[1]}" class="cp-bond"/>'
            atoms[p] = 15.5
    # ramos externos: partem de um vértice real, na direção que sai do anel
    for ri, vi, ln, rr in ((0, 3, 48, 11.5), (1, 1, 46, 11.0), (2, 5, 50, 11.5), (0, 4, 42, 10.0)):
        cx, cy, _ = CEN[ri]
        vx, vy = rings[ri][vi]
        dx, dy = vx - cx, vy - cy
        n = math.hypot(dx, dy) or 1
        ex, ey = round(vx + dx / n * ln, 1), round(vy + dy / n * ln, 1)
        bonds += f'<line x1="{vx}" y1="{vy}" x2="{ex}" y2="{ey}" class="cp-bond"/>'
        atoms.setdefault((ex, ey), rr)
    spheres = ''
    for (x, y), r2 in sorted(atoms.items(), key=lambda kv: kv[0][1]):
        spheres += (f'<circle cx="{x}" cy="{y}" r="{r2}" class="cp-sph"/>'
                    f'<circle cx="{round(x - r2 * .32, 1)}" cy="{round(y - r2 * .36, 1)}" '
                    f'r="{round(r2 * .34, 1)}" class="cp-sph-hi"/>')
    mol = f'<g class="cp-mol">{bonds}{spheres}</g>'

    return (f'<svg class="capa-arte" viewBox="0 0 1000 500" role="img" '
            f'aria-label="Varredura de frequência de 0,01 a 10 Hz: curvas de G′ medidas de um produto '
            f'de cada família reológica, sobre a representação da rede molecular do ácido hialurônico">'
            f'<g class="cp-ondas">{ondas}</g>{mol}{eixos}{curvas}</svg>')

def capa_orn():
    """Losango floral dourado — divisor da capa."""
    pet = ''
    for a in (0, 90, 180, 270):
        pet += (f'<path d="M0,0 C7,-8 7,-19 0,-27 C-7,-19 -7,-8 0,0 Z" class="co-p" '
                f'transform="rotate({a})"/>')
    for a in (45, 135, 225, 315):
        pet += (f'<path d="M0,0 C4.4,-5 4.4,-12 0,-17 C-4.4,-12 -4.4,-5 0,0 Z" class="co-p2" '
                f'transform="rotate({a})"/>')
    return ('<svg class="capa-orn" viewBox="-42 -42 84 84" role="presentation" aria-hidden="true">'
            f'<g>{pet}</g><circle r="4.2" class="co-c"/>'
            '<path d="M-40,0 L-27,0 M40,0 L27,0" class="co-l"/></svg>')

# ---------------- seções de grupos ----------------
FAM_DE = {'G1': 'FAMÍLIA AZUL', 'G2': 'FAMÍLIA AZUL', 'G3': 'FAMÍLIA AMARELA', 'G4': 'FAMÍLIA ROXA', 'G5': 'FAMÍLIA ROXA'}
fam_secs=[]; CH0=9
for gi,g in enumerate(['G1','G2','G3','G4','G5']):
    G=GRUPOS[g]; prods=[p for p in ed.PRODUTOS if grp(p)==g]
    prods.sort(key=lambda p:DATA[p['k']]['G1_0.7Hz'])
    cards='\n'.join(card(p) for p in prods)
    gmin,gmax=DATA[prods[0]['k']]['G1_0.7Hz'],DATA[prods[-1]['k']]['G1_0.7Hz']
    extra=''
    if g=='G5':
        extra='<p class="famdesc" style="margin-top:.3rem">Caso de borda com curadoria oficial: Restylane Defyne (292,62 Pa) permanece neste grupo, com o G′ marcado em roxo por decisão do mapa.</p>'
    fam_secs.append(f'''<section class="famsec folha" id="grupo-{G['num']}">
<div class="fambanner bn-{G['fam']}"><div><p class="fam-eyebrow"><b class="fam-de">{FAM_DE[g]}</b> · CAPÍTULO {CH0+gi} · GRUPO {G['num']} · {html.escape(G['tec'])}</p><h2>{G['nome']}</h2>
<p class="famchave">“{html.escape(G['chave'])}”</p></div>
<div><p class="famdesc"><b>Faixas do grupo:</b> {G['bandas']}<br><b>Melhores contextos:</b> {html.escape(G['ctx'])} · <b>Produto-exemplo:</b> {html.escape(G['ex'])}</p>{extra}
<p class="famdesc" style="margin-top:.3rem"><b>{len(prods)} produtos</b> · G′ de {br(gmin)} a {br(gmax)} Pa</p></div></div>
<div class="grid2">{cards}</div></section>''')

SF=[('Yvoire Contour+ Lido','1ª escolha do autor para olheiras: G′ alto (580 Pa) com baixa expansão declarada — "projeção com precisão volumétrica". Plano subcutâneo superficial na técnica do autor.'),
 ('Perfectha Subskin','Precisão + projeção + baixa expansão. Bifásico com partícula grande; previsibilidade volumétrica infraorbitária.'),
 ('Restylane Lyft Lido','Projeção com pouco volume e precisão (NASHA). Corrige a olheira estrutural sem depender de hidratação do gel.'),
 ('Juvéderm Voluma Lido','Citado no grupo: convexidade com precisão em pacientes selecionados (Vycross, 20 mg/mL).'),
 ('Up Contour Lido','Membro complementar citado: contorno de precisão em plano profundo.')]
sf_cards=''.join(f'''<article class="sfcard"><header>{dotchip('s',12)}<h4>{html.escape(k)}</h4><span class="marca">{html.escape(next(q for q in ed.PRODUTOS if q['k']==k)['m'])}</span></header>
<div class="sfnum"><span>G′ <b>{br(DATA[k]['G1_0.7Hz'])}</b> Pa</span><span>tan δ <b>{br(td_of(k))}</b></span>{radar(k, GRUPOS[grp(next(q for q in ed.PRODUTOS if q['k']==k))]['fam'],72,'radar radar-sm')}</div>
<p>{html.escape(why)}</p><a class="sflink" href="#{slug(k)}">ver ficha completa ↓</a></article>''' for k,why in SF)
sf_sec=f'''<section class="famsec folha" id="grupo-6">
<div class="fambanner bn-s"><div><p class="fam-eyebrow"><b class="fam-de">FAMÍLIA ROXA · USO NA OLHEIRA</b> · CAPÍTULO 14 · GRUPO 6 · critério funcional transversal · 💧</p><h2>PRECISOS — BAIXO SWELLING FACTOR</h2>
<p class="famchave">“Alta projeção + baixa expansão + mais precisão + melhor controle de edema.”</p></div>
<div><p class="famdesc"><b>Padrão funcional:</b> alto G′ + AH em baixa concentração (20–22 mg/mL) + partículas grandes + maior estabilidade química. <b>Melhores contextos:</b> olheiras e áreas em que o controle de expansão é determinante. Regra do autor: <i>nunca escolher olheira pelo G′</i> — “o tamanho da partícula ajuda a explicar; o SF medido é o que confirma”.</p>
<p class="famdesc" style="margin-top:.3rem"><b>⚠ SF ainda não foi medido em nenhum produto</b> — prioridade da 2ª rodada laboratorial. Até lá, grupo clínico-declarativo (💧); sem SF confiável, não existe “ranking definitivo” para olheiras.</p></div></div>
<div class="grid3">{sf_cards}</div></section>'''

def radar_demo(k,cap):
    p=next(q for q in ed.PRODUTOS if q['k']==k)
    return f'<figure class="rdemo">{radar(k,GRUPOS[grp(p)]["fam"],150,"radar radar-lg")}<figcaption><b>{html.escape(short(k))}</b><br>{cap}</figcaption></figure>'

GEL=gel_icons()
reg_rows=''.join(f'<tr><td><b>{html.escape(r)}</b></td><td>{html.escape(c)}</td><td>{html.escape(pr)}</td><td class="obs">{html.escape(o)}</td></tr>' for r,c,pr,o in ed.REGIOES)
marcas={}
for p in ed.PRODUTOS: marcas.setdefault(p['m'].split('·')[0].strip(),[]).append(p)
idx=''.join('<div class="ixm"><b>'+html.escape(m)+'</b>'+''.join(
    f'<a href="#{slug(q["k"])}"><span class="chip" style="width:9px;height:9px;background:{CHIP[famcolor(q)]}"></span>{html.escape(short(q["k"]))}</a>'
    for q in sorted(ps,key=lambda q:DATA[q['k']]['G1_0.7Hz']))+'</div>' for m,ps in sorted(marcas.items()))


A9_ORDEM = [('a','r'),('a','v'),('a','p'),('m','r'),('m','v'),('m','p'),('r','r'),('r','v'),('r','p')]
from collections import Counter as _C
_a9c = _C(assinatura(p['k'])[0] for p in ed.PRODUTOS)
a9_cards = ''.join(
    f'<div class="a9c"><div class="a9dots"><i style="background:{CHIP[b]}"></i>'
    + ('' if m=='r' else f'<span>+</span><i style="background:{CHIP[m]}"></i>')
    + f'</div><span class="a9n">{ASSIN[(b,m)]}</span><span class="a9q">{_a9c.get(ASSIN[(b,m)],0)} produto{"" if _a9c.get(ASSIN[(b,m)],0)==1 else "s"}</span></div>'
    for b,m in A9_ORDEM)

FACE_CAPA = face_svg(196, marks=[
    (150,128,'a','','start'), (124,192,'s','','start'), (200,216,'v','','start'),
    (172,246,'m','','start'), (150,310,'r','','start')],
    cls='facesvg capa-face', aria='rosto com os pontos das famílias do Mapa')

FACE_GEO = face_svg(620, marks=[
    (108,207,'m','CURVA · malar','L'),
    (132,233,'r','SUPORTE · profundo','L'),
    (134,260,'a','LINHA · perioral','L'),
    (172,246,'m','VALE · sulco nasolabial','R'),
    (152,311,'r','VÉRTICE · mento','R')],
    cls='facesvg facegeo', aria='tarefas geométricas do preenchimento sobre a face',
    vw=520, dx=110, leader=True, lx_l=150, lx_r=370)

page=f'''<title>eBook Reology Map</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&family=JetBrains+Mono:wght@400;600;700&display=swap">
<style>
:root {{
 /* identidade dos eBooks: navy profundo + dourado metálico */
 --navy:#0A3557; --navy-2:#10486F; --navy-3:#2A6C9C; --navy-ink:#092C48;
 --gold:#C08A2E; --gold-2:#E0A64B; --gold-3:#F5CE7B; --gold-soft:rgba(224,166,75,.13);
 --bg:#FBF9F6; --card:#FFFFFF; --ink:#15293C; --ink2:#4C5C6B; --ink3:#8494A1;
 --line:#E4DFD6; --linesoft:#F0EBE3; --accent:var(--navy-2); --accent-ink:#0E4269; --accent-soft:#EAF1F7;
 --fam-a:#2E7DBF; --fam-m:#8F6D12; --fam-r:#7C3AED; --fam-v:#3E9B6E;
 --chip-rosa:#C4557F; --sf:#0F7480; --sf-soft:rgba(15,116,128,.09);
 --warn:#A8501F; --flag:#B23B3B;
 --za:rgba(46,125,191,.05); --zm:rgba(143,109,18,.06); --zr:rgba(124,58,237,.045);
 --title-ink:#10486F; --gold-ink:#10486F; --face-line:#7C6A61; --face-fill:#FBEDE2; --face-hi:#FFF8F1; --face-sh:#F0DACA; --hair-1:#4A3428; --hair-2:#6B4A37; --hair-line:#3A281E; --blush:#E9B6A4; --lip:#D89A94; --lip-line:#B4726C; --eye-white:#FFFDFB; --iris:#7B5B43; --pupil:#2B1D14; --lash:#3A281E;
 --n1bg:#10486F; --n1ink:#FFFFFF; --n2bg:#DCE8F1; --n2ink:#0E4269; --n3bd:#A9BFD1; --n3ink:#31536E; --n4ink:#7A8794;
 --tint:12%; --book-bg:#EDE7DD;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
 --navy:#071F33; --navy-2:#0C2A42; --navy-3:#2A6C9C; --navy-ink:#DCE8F1;
 --gold:#D6A048; --gold-2:#E9B968; --gold-3:#F7DA96; --gold-soft:rgba(233,185,104,.14);
 --bg:#071F33; --card:#0C2A42; --ink:#E8EEF4; --ink2:#A9BCCB; --ink3:#728A9C;
 --line:#1B3E5A; --linesoft:#16344C; --accent:#4E97D0; --accent-ink:#8CC0E8; --accent-soft:#123650;
 --fam-a:#3F87C4; --fam-m:#AC831F; --fam-r:#8E68D8; --fam-v:#43A076;
 --chip-rosa:#C96B92; --sf:#3DA0AC; --sf-soft:rgba(61,160,172,.15);
 --warn:#D08A5E; --flag:#DC7E7E;
 --za:rgba(63,135,196,.10); --zm:rgba(172,131,31,.12); --zr:rgba(142,104,216,.10);
 --title-ink:#E8EEF4; --gold-ink:#E9B968; --face-line:#A08C80; --face-fill:#E6CDBB; --face-hi:#F2DECF; --face-sh:#D2B29B; --hair-1:#3A281E; --hair-2:#573D2C; --hair-line:#2A1C14; --blush:#D99A86; --lip:#C8867F; --lip-line:#9E5F59; --eye-white:#FBF6F1; --iris:#8A6A50; --pupil:#221610; --lash:#2A1C14;
 --n1bg:#2A6C9C; --n1ink:#08192A; --n2bg:#173F5C; --n2ink:#A9D2EE; --n3bd:#2F5B7C; --n3ink:#8CC0E8; --n4ink:#7A93A6;
 --tint:22%; --book-bg:#04141F;
}} }}
:root[data-theme="dark"] {{
 --navy:#071F33; --navy-2:#0C2A42; --navy-3:#2A6C9C; --navy-ink:#DCE8F1;
 --gold:#D6A048; --gold-2:#E9B968; --gold-3:#F7DA96; --gold-soft:rgba(233,185,104,.14);
 --bg:#071F33; --card:#0C2A42; --ink:#E8EEF4; --ink2:#A9BCCB; --ink3:#728A9C;
 --line:#1B3E5A; --linesoft:#16344C; --accent:#4E97D0; --accent-ink:#8CC0E8; --accent-soft:#123650;
 --fam-a:#3F87C4; --fam-m:#AC831F; --fam-r:#8E68D8; --fam-v:#43A076;
 --chip-rosa:#C96B92; --sf:#3DA0AC; --sf-soft:rgba(61,160,172,.15);
 --warn:#D08A5E; --flag:#DC7E7E;
 --za:rgba(63,135,196,.10); --zm:rgba(172,131,31,.12); --zr:rgba(142,104,216,.10);
 --title-ink:#E8EEF4; --gold-ink:#E9B968; --face-line:#A08C80; --face-fill:#E6CDBB; --face-hi:#F2DECF; --face-sh:#D2B29B; --hair-1:#3A281E; --hair-2:#573D2C; --hair-line:#2A1C14; --blush:#D99A86; --lip:#C8867F; --lip-line:#9E5F59; --eye-white:#FBF6F1; --iris:#8A6A50; --pupil:#221610; --lash:#2A1C14;
 --n1bg:#2A6C9C; --n1ink:#08192A; --n2bg:#173F5C; --n2ink:#A9D2EE; --n3bd:#2F5B7C; --n3ink:#8CC0E8; --n4ink:#7A93A6;
 --tint:22%; --book-bg:#04141F;
}}
*{{box-sizing:border-box}} html{{scroll-behavior:smooth}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:'Source Serif 4',Georgia,serif;font-size:16px;line-height:1.62}}
.pill,.lbl,.marca,.legend,.stat span,.famdesc,.fam-eyebrow,.sflink,.evite,.alts,.tech,.flags,.sfnum,.sigdots,.bx-url,.bx-qrwrap span,.a9q{{font-family:'Barlow',system-ui,sans-serif}}
h1,h2,h3,h4,.famtag,.capa-brand,.bx-head{{font-family:'Barlow Condensed','Barlow',sans-serif}}
h2,h3{{text-transform:uppercase;letter-spacing:.015em}}
.cap-eyebrow{{font-family:'Barlow',sans-serif;font-size:.72rem;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:var(--gold);margin:0 0 .2rem}}
.cap-eyebrow::before{{content:"";display:inline-block;width:26px;height:2px;background:var(--gold);vertical-align:.28em;margin-right:.55rem}}
main{{max-width:78rem;margin:0 auto;padding:2rem 1.2rem 5rem}}
a{{color:var(--accent-ink)}} a:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.chip{{display:inline-block;border-radius:50%;border:1.5px solid rgba(0,0,0,.16);margin-right:4px;vertical-align:-1px}}
h1,h2,h3,h4{{font-family:'Barlow Condensed','Barlow',sans-serif;text-wrap:balance;line-height:1.06}}
.capa{{padding:0;margin-bottom:1.6rem;border:none;background:none;border-radius:0}}
.capa-in{{background:linear-gradient(160deg,#0B2647 0%,#0A2141 38%,#0C2B50 72%,#0A1E3B 100%);
 padding:clamp(.9rem,2.6vw,1.7rem);position:relative;overflow:hidden}}
.capa-in::before{{content:"";position:absolute;inset:0;pointer-events:none;
 background:radial-gradient(ellipse at 72% 18%,rgba(88,150,214,.20),transparent 58%),
 radial-gradient(ellipse at 20% 88%,rgba(60,110,170,.14),transparent 62%)}}
.capa-spine{{position:absolute;left:0;top:0;bottom:0;width:clamp(10px,1.5vw,20px);pointer-events:none;
 background:linear-gradient(90deg,rgba(0,0,0,.55),rgba(0,0,0,.22) 45%,transparent);
 border-right:1px solid rgba(224,166,75,.16)}}
.capa-frame{{border:1px solid rgba(224,166,75,.62);padding:clamp(1.5rem,3.6vw,2.6rem) clamp(1rem,3vw,2.4rem) clamp(1.2rem,3vw,2rem);
 text-align:center;position:relative}}
.capa-frame p{{max-width:none}}
.capa-brand{{font-family:'Barlow',sans-serif;font-size:clamp(.6rem,1.5vw,.78rem);font-weight:600;
 letter-spacing:.30em;text-transform:uppercase;color:var(--gold-2);margin:0}}
.capa-dot{{display:block;width:5px;height:5px;background:var(--gold-2);margin:.9rem auto 1.1rem;
 transform:rotate(45deg)}}
.capa h1{{margin:0;font-family:'Source Serif 4',Georgia,serif;font-weight:600;text-transform:uppercase;
 line-height:.98;letter-spacing:.012em}}
.capa h1 .t1,.capa h1 .t3{{display:block;
 background:linear-gradient(176deg,#F3D69A 2%,#E3B063 34%,#C89237 70%,#EFCB84 100%);
 -webkit-background-clip:text;background-clip:text;color:#E0A64B;-webkit-text-fill-color:transparent}}
@supports not (-webkit-background-clip:text){{.capa h1 .t1,.capa h1 .t3{{-webkit-text-fill-color:#E0A64B;color:#E0A64B}}}}
.capa h1 .t1{{font-size:clamp(2.1rem,8.4vw,5.1rem)}}
.capa h1 .t3{{font-size:clamp(1.6rem,6.3vw,3.85rem)}}
.capa h1 .t2{{display:flex;align-items:center;justify-content:center;gap:clamp(.7rem,2.4vw,1.5rem);
 font-size:clamp(.92rem,2.9vw,1.75rem);font-weight:400;letter-spacing:.34em;color:var(--gold-3);
 margin:.18em 0 .1em}}
.capa h1 .t2 i{{height:1px;width:clamp(28px,7vw,86px);background:rgba(224,166,75,.55)}}
.capa-sub{{font-family:'Barlow',sans-serif;font-size:clamp(.8rem,2.15vw,1.24rem);font-weight:400;
 color:rgba(238,245,251,.94);margin:clamp(.9rem,2.4vw,1.5rem) 0 0;letter-spacing:.012em}}
.capa-autor{{font-family:'Source Serif 4',Georgia,serif;font-size:clamp(1.3rem,4vw,2.35rem);
 font-weight:600;color:var(--gold-2);margin:0;letter-spacing:.01em}}
.capa-ed{{font-family:'Barlow',sans-serif;font-size:clamp(.56rem,1.4vw,.74rem);letter-spacing:.26em;
 text-transform:uppercase;color:var(--gold-3);opacity:.82;margin:.85rem 0 0}}
.capa-band{{height:8px;background:linear-gradient(90deg,var(--fam-a) 0 33.33%,var(--fam-m) 33.33% 66.66%,var(--fam-r) 66.66% 100%)}}
/* arte nativa da capa: varredura de frequência real + rede molecular */
.capa-arte{{display:block;width:100%;max-width:760px;height:auto;margin:clamp(1rem,2.8vw,1.9rem) auto 0;overflow:visible}}
.cp-onda{{fill:none;stroke:#8FC0EC;stroke-width:1.1}}
.cp-eixo{{fill:none;stroke:rgba(214,232,247,.55);stroke-width:1.1}}
.cp-grade{{fill:none;stroke:rgba(214,232,247,.13);stroke-width:1;stroke-dasharray:3 6}}
.cp-tick,.cp-ax{{fill:rgba(214,232,247,.72);font-family:'Barlow',sans-serif;font-size:15px}}
.cp-ax{{font-size:16px;fill:rgba(214,232,247,.8)}}
.cp-linha{{fill:none;stroke-width:2.1;stroke-linecap:round}}
.cp-pt{{stroke:rgba(10,33,65,.85);stroke-width:1}}
.c-a{{stroke:#7FB6E8}} circle.c-a{{fill:#7FB6E8}}
.c-m{{stroke:#E8C577}} circle.c-m{{fill:#E8C577}}
.c-r{{stroke:#B79BEA}} circle.c-r{{fill:#B79BEA}}
.cp-g2{{stroke:rgba(190,214,238,.62);stroke-dasharray:5 5;stroke-width:1.6}}
.cp-bond{{stroke:#3E7BB4;stroke-width:2.6;opacity:.62;stroke-linecap:round}}
.cp-sph{{fill:#1D4E80;stroke:#4A88C0;stroke-width:1.2;opacity:.88}}
.cp-sph-hi{{fill:#8CBEE8;opacity:.55}}
.cp-mol{{opacity:.8}}
.capa-orn{{display:block;width:clamp(52px,9vw,76px);height:auto;margin:clamp(.9rem,2.6vw,1.5rem) auto clamp(.7rem,2vw,1.1rem);overflow:visible}}
.co-p{{fill:none;stroke:var(--gold-2);stroke-width:1.5}}
.co-p2{{fill:none;stroke:var(--gold-2);stroke-width:1.1;opacity:.6}}
.co-c{{fill:var(--gold-2)}}
.co-l{{stroke:var(--gold-2);stroke-width:1;opacity:.6}}
@media (max-width:640px){{.capa-arte{{max-width:none}} .cp-tick{{font-size:19px}} .cp-ax{{font-size:20px}}}}

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
 background:url("data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%27%20viewBox%3D%270%200%20152%2020%27%20width%3D%27152%27%20height%3D%2720%27%3E%3Cpath%20d%3D%27M3.0%2C10.0%20L7.87%2C6.11%20L12.73%2C4.6%20L17.6%2C6.41%20L22.47%2C10.42%20L27.33%2C14.17%20L32.2%2C15.36%20L37.07%2C13.27%20L41.93%2C9.17%20L46.8%2C5.58%20L51.67%2C4.7%20L56.53%2C7.07%20L61.4%2C11.24%20L66.27%2C14.65%20L71.13%2C15.2%20L76.0%2C12.57%20L80.87%2C8.36%20L85.73%2C5.16%20L90.6%2C4.92%20L95.47%2C7.8%20L100.33%2C12.03%20L105.2%2C15.01%20L110.07%2C14.92%20L114.93%2C11.81%20L119.8%2C7.59%20L124.67%2C4.85%20L129.53%2C5.27%20L134.4%2C8.59%20L139.27%2C12.78%20L144.13%2C15.26%20L149.0%2C14.52%27%20fill%3D%27none%27%20stroke%3D%27%23C08A2E%27%20stroke-width%3D%271%27%20opacity%3D%27.42%27%2F%3E%3Ccircle%20cx%3D%223.0%22%20cy%3D%2210.0%22%20r%3D%221.7%22%20fill%3D%22%23C08A2E%22%20opacity%3D%220.3%22%2F%3E%3Ccircle%20cx%3D%2212.73%22%20cy%3D%224.6%22%20r%3D%222.2%22%20fill%3D%22%23C08A2E%22%20opacity%3D%220.57%22%2F%3E%3Ccircle%20cx%3D%2222.47%22%20cy%3D%2210.42%22%20r%3D%222.5%22%20fill%3D%22%23C08A2E%22%20opacity%3D%220.71%22%2F%3E%3Ccircle%20cx%3D%2232.2%22%20cy%3D%2215.36%22%20r%3D%222.73%22%20fill%3D%22%23C08A2E%22%20opacity%3D%220.81%22%2F%3E%3Ccircle%20cx%3D%2241.93%22%20cy%3D%229.17%22%20r%3D%222.92%22%20fill%3D%22%23C08A2E%22%20opacity%3D%220.89%22%2F%3E%3Ccircle%20cx%3D%2251.67%22%20cy%3D%224.7%22%20r%3D%223.06%22%20fill%3D%22%23C08A2E%22%20opacity%3D%220.94%22%2F%3E%3Ccircle%20cx%3D%2261.4%22%20cy%3D%2211.24%22%20r%3D%223.15%22%20fill%3D%22%23C08A2E%22%20opacity%3D%220.98%22%2F%3E%3Ccircle%20cx%3D%2271.13%22%20cy%3D%2215.2%22%20r%3D%223.19%22%20fill%3D%22%23C08A2E%22%20opacity%3D%221.0%22%2F%3E%3Ccircle%20cx%3D%2280.87%22%20cy%3D%228.36%22%20r%3D%223.19%22%20fill%3D%22%23C08A2E%22%20opacity%3D%221.0%22%2F%3E%3Ccircle%20cx%3D%2290.6%22%20cy%3D%224.92%22%20r%3D%223.15%22%20fill%3D%22%23C08A2E%22%20opacity%3D%220.98%22%2F%3E%3Ccircle%20cx%3D%22100.33%22%20cy%3D%2212.03%22%20r%3D%223.06%22%20fill%3D%22%23C08A2E%22%20opacity%3D%220.94%22%2F%3E%3Ccircle%20cx%3D%22110.07%22%20cy%3D%2214.92%22%20r%3D%222.92%22%20fill%3D%22%23C08A2E%22%20opacity%3D%220.89%22%2F%3E%3Ccircle%20cx%3D%22119.8%22%20cy%3D%227.59%22%20r%3D%222.73%22%20fill%3D%22%23C08A2E%22%20opacity%3D%220.81%22%2F%3E%3Ccircle%20cx%3D%22129.53%22%20cy%3D%225.27%22%20r%3D%222.5%22%20fill%3D%22%23C08A2E%22%20opacity%3D%220.71%22%2F%3E%3Ccircle%20cx%3D%22139.27%22%20cy%3D%2212.78%22%20r%3D%222.2%22%20fill%3D%22%23C08A2E%22%20opacity%3D%220.57%22%2F%3E%3Ccircle%20cx%3D%22149.0%22%20cy%3D%2214.52%22%20r%3D%221.7%22%20fill%3D%22%23C08A2E%22%20opacity%3D%220.3%22%2F%3E%3C%2Fsvg%3E") no-repeat center .95rem;background-size:132px 18px;
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
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]) .folha::after{{background-image:url("data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%27%20viewBox%3D%270%200%20152%2020%27%20width%3D%27152%27%20height%3D%2720%27%3E%3Cpath%20d%3D%27M3.0%2C10.0%20L7.87%2C6.11%20L12.73%2C4.6%20L17.6%2C6.41%20L22.47%2C10.42%20L27.33%2C14.17%20L32.2%2C15.36%20L37.07%2C13.27%20L41.93%2C9.17%20L46.8%2C5.58%20L51.67%2C4.7%20L56.53%2C7.07%20L61.4%2C11.24%20L66.27%2C14.65%20L71.13%2C15.2%20L76.0%2C12.57%20L80.87%2C8.36%20L85.73%2C5.16%20L90.6%2C4.92%20L95.47%2C7.8%20L100.33%2C12.03%20L105.2%2C15.01%20L110.07%2C14.92%20L114.93%2C11.81%20L119.8%2C7.59%20L124.67%2C4.85%20L129.53%2C5.27%20L134.4%2C8.59%20L139.27%2C12.78%20L144.13%2C15.26%20L149.0%2C14.52%27%20fill%3D%27none%27%20stroke%3D%27%23D6A048%27%20stroke-width%3D%271%27%20opacity%3D%27.42%27%2F%3E%3Ccircle%20cx%3D%223.0%22%20cy%3D%2210.0%22%20r%3D%221.7%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.3%22%2F%3E%3Ccircle%20cx%3D%2212.73%22%20cy%3D%224.6%22%20r%3D%222.2%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.57%22%2F%3E%3Ccircle%20cx%3D%2222.47%22%20cy%3D%2210.42%22%20r%3D%222.5%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.71%22%2F%3E%3Ccircle%20cx%3D%2232.2%22%20cy%3D%2215.36%22%20r%3D%222.73%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.81%22%2F%3E%3Ccircle%20cx%3D%2241.93%22%20cy%3D%229.17%22%20r%3D%222.92%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.89%22%2F%3E%3Ccircle%20cx%3D%2251.67%22%20cy%3D%224.7%22%20r%3D%223.06%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.94%22%2F%3E%3Ccircle%20cx%3D%2261.4%22%20cy%3D%2211.24%22%20r%3D%223.15%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.98%22%2F%3E%3Ccircle%20cx%3D%2271.13%22%20cy%3D%2215.2%22%20r%3D%223.19%22%20fill%3D%22%23D6A048%22%20opacity%3D%221.0%22%2F%3E%3Ccircle%20cx%3D%2280.87%22%20cy%3D%228.36%22%20r%3D%223.19%22%20fill%3D%22%23D6A048%22%20opacity%3D%221.0%22%2F%3E%3Ccircle%20cx%3D%2290.6%22%20cy%3D%224.92%22%20r%3D%223.15%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.98%22%2F%3E%3Ccircle%20cx%3D%22100.33%22%20cy%3D%2212.03%22%20r%3D%223.06%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.94%22%2F%3E%3Ccircle%20cx%3D%22110.07%22%20cy%3D%2214.92%22%20r%3D%222.92%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.89%22%2F%3E%3Ccircle%20cx%3D%22119.8%22%20cy%3D%227.59%22%20r%3D%222.73%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.81%22%2F%3E%3Ccircle%20cx%3D%22129.53%22%20cy%3D%225.27%22%20r%3D%222.5%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.71%22%2F%3E%3Ccircle%20cx%3D%22139.27%22%20cy%3D%2212.78%22%20r%3D%222.2%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.57%22%2F%3E%3Ccircle%20cx%3D%22149.0%22%20cy%3D%2214.52%22%20r%3D%221.7%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.3%22%2F%3E%3C%2Fsvg%3E")}}}}
:root[data-theme="dark"] .folha::after{{background-image:url("data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%27%20viewBox%3D%270%200%20152%2020%27%20width%3D%27152%27%20height%3D%2720%27%3E%3Cpath%20d%3D%27M3.0%2C10.0%20L7.87%2C6.11%20L12.73%2C4.6%20L17.6%2C6.41%20L22.47%2C10.42%20L27.33%2C14.17%20L32.2%2C15.36%20L37.07%2C13.27%20L41.93%2C9.17%20L46.8%2C5.58%20L51.67%2C4.7%20L56.53%2C7.07%20L61.4%2C11.24%20L66.27%2C14.65%20L71.13%2C15.2%20L76.0%2C12.57%20L80.87%2C8.36%20L85.73%2C5.16%20L90.6%2C4.92%20L95.47%2C7.8%20L100.33%2C12.03%20L105.2%2C15.01%20L110.07%2C14.92%20L114.93%2C11.81%20L119.8%2C7.59%20L124.67%2C4.85%20L129.53%2C5.27%20L134.4%2C8.59%20L139.27%2C12.78%20L144.13%2C15.26%20L149.0%2C14.52%27%20fill%3D%27none%27%20stroke%3D%27%23D6A048%27%20stroke-width%3D%271%27%20opacity%3D%27.42%27%2F%3E%3Ccircle%20cx%3D%223.0%22%20cy%3D%2210.0%22%20r%3D%221.7%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.3%22%2F%3E%3Ccircle%20cx%3D%2212.73%22%20cy%3D%224.6%22%20r%3D%222.2%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.57%22%2F%3E%3Ccircle%20cx%3D%2222.47%22%20cy%3D%2210.42%22%20r%3D%222.5%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.71%22%2F%3E%3Ccircle%20cx%3D%2232.2%22%20cy%3D%2215.36%22%20r%3D%222.73%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.81%22%2F%3E%3Ccircle%20cx%3D%2241.93%22%20cy%3D%229.17%22%20r%3D%222.92%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.89%22%2F%3E%3Ccircle%20cx%3D%2251.67%22%20cy%3D%224.7%22%20r%3D%223.06%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.94%22%2F%3E%3Ccircle%20cx%3D%2261.4%22%20cy%3D%2211.24%22%20r%3D%223.15%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.98%22%2F%3E%3Ccircle%20cx%3D%2271.13%22%20cy%3D%2215.2%22%20r%3D%223.19%22%20fill%3D%22%23D6A048%22%20opacity%3D%221.0%22%2F%3E%3Ccircle%20cx%3D%2280.87%22%20cy%3D%228.36%22%20r%3D%223.19%22%20fill%3D%22%23D6A048%22%20opacity%3D%221.0%22%2F%3E%3Ccircle%20cx%3D%2290.6%22%20cy%3D%224.92%22%20r%3D%223.15%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.98%22%2F%3E%3Ccircle%20cx%3D%22100.33%22%20cy%3D%2212.03%22%20r%3D%223.06%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.94%22%2F%3E%3Ccircle%20cx%3D%22110.07%22%20cy%3D%2214.92%22%20r%3D%222.92%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.89%22%2F%3E%3Ccircle%20cx%3D%22119.8%22%20cy%3D%227.59%22%20r%3D%222.73%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.81%22%2F%3E%3Ccircle%20cx%3D%22129.53%22%20cy%3D%225.27%22%20r%3D%222.5%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.71%22%2F%3E%3Ccircle%20cx%3D%22139.27%22%20cy%3D%2212.78%22%20r%3D%222.2%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.57%22%2F%3E%3Ccircle%20cx%3D%22149.0%22%20cy%3D%2214.52%22%20r%3D%221.7%22%20fill%3D%22%23D6A048%22%20opacity%3D%220.3%22%2F%3E%3C%2Fsvg%3E")}}

/* pódios (rankings temáticos) */
.podios{{display:grid;grid-template-columns:repeat(auto-fit,minmax(390px,1fr));gap:1.1rem;margin:1.1rem 0}}
.podio{{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:.9rem 1rem 1rem}}
.podio h4{{margin:0 0 .55rem;font-size:1.06rem;color:var(--title-ink);letter-spacing:.02em}}
.podio table{{width:100%;border-collapse:collapse;font-family:'Barlow',sans-serif;font-size:.86rem}}
.podio th{{text-align:left;font-size:.66rem;letter-spacing:.14em;text-transform:uppercase;
 color:var(--ink3);font-weight:700;border-bottom:1px solid var(--line);padding:0 .3rem .3rem}}
.podio td{{padding:.3rem .3rem;border-bottom:1px solid var(--linesoft);vertical-align:baseline}}
.podio tr:last-child td{{border-bottom:none}}
.pd-n{{font-family:'Barlow Condensed',sans-serif;font-weight:700;color:var(--gold);width:1.7rem;font-size:1rem}}
.pd-p{{font-weight:600;color:var(--ink)}}
.pd-as{{display:block;font-size:.63rem;letter-spacing:.1em;text-transform:uppercase;color:var(--ink3);font-weight:600}}
.pd-v{{font-family:'JetBrains Mono',monospace;font-weight:700;text-align:right;white-space:nowrap;color:var(--accent-ink)}}
.pd-x{{font-size:.74rem;color:var(--ink2);white-space:nowrap;text-align:right}}
.pd-nota{{font-family:'Barlow',sans-serif;font-size:.76rem;color:var(--ink2);margin:.6rem 0 0;line-height:1.45}}
@media (max-width:560px){{.pd-x{{display:none}}}}
/* tabela de camadas de evidência */
.fontes{{overflow-x:auto;margin:1rem 0}}
.fontes table{{width:100%;min-width:640px;border-collapse:collapse;font-family:'Barlow',sans-serif;font-size:.85rem}}
.fontes th{{background:var(--accent-soft);color:var(--accent-ink);text-align:left;padding:.5rem .6rem;
 font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;font-weight:700;border-bottom:1px solid var(--line)}}
.fontes td{{padding:.45rem .6rem;border-bottom:1px solid var(--linesoft);vertical-align:top}}
.fontes .med{{font-family:'JetBrains Mono',monospace;font-weight:700;color:var(--accent-ink);white-space:nowrap}}
.fontes .out{{font-family:'JetBrains Mono',monospace;color:var(--warn);white-space:nowrap}}
.fontes tr:nth-child(even) td{{background:color-mix(in srgb,var(--linesoft) 42%,transparent)}}
.camadas{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:.8rem;margin:1rem 0}}
.camada{{border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:3px;
 background:var(--card);padding:.7rem .85rem}}
.camada>b{{font-family:'Barlow Condensed',sans-serif;font-size:1.02rem;letter-spacing:.05em;
 text-transform:uppercase;color:var(--title-ink);display:block}}
.camada p{{margin:.25rem 0 0;font-family:'Barlow',sans-serif;font-size:.8rem;color:var(--ink2);line-height:1.45}}
.camada.c2{{border-left-color:var(--gold)}} .camada.c3{{border-left-color:var(--fam-v)}}
.camada.c4{{border-left-color:var(--fam-r)}}
/* errata */
.errata{{background:var(--gold-soft);border:1px solid var(--gold-2);border-radius:4px;padding:1rem 1.2rem;margin:1.2rem 0}}
.errata h4{{margin:0 0 .5rem;color:var(--gold-ink);font-size:1.1rem;letter-spacing:.04em}}
.errata ul{{margin:.3rem 0 0;padding-left:1.1rem;font-family:'Barlow',sans-serif;font-size:.87rem;line-height:1.6}}
.errata li{{margin-bottom:.4rem}}
.errata code{{font-family:'JetBrains Mono',monospace;font-size:.82em;background:var(--card);
 padding:.05rem .3rem;border-radius:2px;border:1px solid var(--line)}}
.de{{color:var(--flag);text-decoration:line-through}} .para{{color:var(--fam-v);font-weight:700}}
/* equações */
.eqs{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:.85rem;margin:1rem 0}}
.eq{{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:.85rem 1rem;text-align:center}}
.eq .f{{font-family:'JetBrains Mono',monospace;font-size:1.16rem;font-weight:700;color:var(--accent-ink);display:block}}
.eq .t{{font-family:'Barlow Condensed',sans-serif;font-size:.95rem;letter-spacing:.08em;text-transform:uppercase;
 color:var(--gold-ink);display:block;margin-bottom:.3rem}}
.eq p{{margin:.35rem 0 0;font-family:'Barlow',sans-serif;font-size:.79rem;color:var(--ink2);line-height:1.4}}
/* modelos reológicos */
.mods{{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:.85rem;margin:1rem 0}}
.mod{{background:var(--card);border:1px solid var(--line);border-top:3px solid var(--gold-2);
 border-radius:3px;padding:.8rem .95rem}}
.mod>b{{font-family:'Barlow Condensed',sans-serif;font-size:1.05rem;letter-spacing:.04em;
 text-transform:uppercase;color:var(--title-ink);display:block;margin-bottom:.25rem}}
.mod p{{margin:0;font-family:'Barlow',sans-serif;font-size:.82rem;color:var(--ink2);line-height:1.5}}
/* etapas numeradas (química) */
.etapas{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:.85rem;margin:1rem 0}}
.etapa{{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:.85rem 1rem;position:relative}}
.etapa .n{{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:.9rem;color:#fff;
 background:var(--accent);width:1.55rem;height:1.55rem;border-radius:50%;display:flex;
 align-items:center;justify-content:center;margin-bottom:.45rem}}
.etapa>b{{font-family:'Barlow Condensed',sans-serif;font-size:1.02rem;letter-spacing:.04em;
 text-transform:uppercase;color:var(--title-ink);display:block;margin-bottom:.2rem}}
.etapa p{{margin:0;font-family:'Barlow',sans-serif;font-size:.82rem;color:var(--ink2);line-height:1.5}}
.etapa p b,.mod p b,.camada p b,.podio p b,.pd-nota b{{display:inline;font-family:inherit;font-size:inherit;letter-spacing:normal;text-transform:none;color:var(--ink);font-weight:700}}
.etapa code{{font-family:'JetBrains Mono',monospace;font-size:.78em;color:var(--accent-ink)}}

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
.facereg .rg{{fill:var(--rg-f);fill-opacity:.30;stroke:var(--rg-s);stroke-width:1.7;
 stroke-linejoin:round}}
.facereg .fc-edge{{fill:none;stroke:var(--face-line);stroke-width:2.2;opacity:.9}}
.rc-reg{{font-family:'Barlow',sans-serif;font-size:.82rem;color:var(--ink);
 margin:.1rem 0 .35rem;line-height:1.45;text-align:left;font-weight:600}}
.rc-leg{{font-family:'Barlow',sans-serif;font-size:.76rem;color:var(--ink2);
 margin:0;line-height:1.45;text-align:left}}

/* capítulo da forma: eixos e famílias */
.eixos{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:.9rem;margin:1.1rem 0 1.4rem}}
.eixo{{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:.85rem 1rem;
 border-top:3px solid var(--fam-a);position:relative}}
.eixo-td{{border-top-color:var(--fam-r)}}
.ex-pos{{position:absolute;top:.6rem;right:.9rem;font-family:'Barlow',sans-serif;font-size:.62rem;
 letter-spacing:.16em;text-transform:uppercase;color:var(--ink3);font-weight:700}}
.ex-s{{font-family:'JetBrains Mono',monospace;font-size:1.5rem;font-weight:700;color:var(--accent-ink);
 display:block;line-height:1.1}}
.ex-n{{font-family:'Barlow Condensed',sans-serif;font-size:1rem;letter-spacing:.04em;
 text-transform:uppercase;color:var(--title-ink);display:block;margin-bottom:.3rem}}
.eixo p{{margin:0 0 .5rem;font-family:'Barlow',sans-serif;font-size:.82rem;color:var(--ink2);line-height:1.45}}
.ex-cut{{list-style:none;margin:0 0 .5rem;padding:0;font-family:'Barlow',sans-serif;font-size:.79rem}}
.ex-cut li{{margin:.12rem 0;color:var(--ink)}}
.ex-faixa{{font-family:'Barlow',sans-serif;font-size:.72rem;color:var(--ink3);
 border-top:1px solid var(--linesoft);padding-top:.4rem;display:block}}
.ffams{{display:grid;grid-template-columns:repeat(auto-fit,minmax(232px,1fr));gap:1rem;margin:1.1rem 0}}
.ffam{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:4px;
 padding:.6rem .85rem 1rem;text-align:center;display:flex;flex-direction:column}}
.ffam figcaption{{display:flex;align-items:center;gap:.5rem;text-align:left;
 border-bottom:1px solid var(--linesoft);padding-bottom:.4rem}}
.ff-n{{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:1.45rem;
 line-height:1;color:var(--gold)}}
.ff-t{{font-family:'Barlow Condensed',sans-serif;font-size:.98rem;font-weight:600;letter-spacing:.04em;
 text-transform:uppercase;color:var(--title-ink);line-height:1.05}}
.ff-chips{{display:flex;align-items:center;justify-content:center;gap:.3rem;margin:.5rem 0 .1rem}}
.ff-chips span{{font-family:'Barlow',sans-serif;font-size:.72rem;letter-spacing:.08em;
 text-transform:uppercase;color:var(--ink3);font-weight:600;margin-left:.2rem}}
.ffam .radar-lg{{margin:.1rem auto .2rem}}
.ff-p{{font-family:'Barlow',sans-serif;font-size:.8rem;color:var(--ink);margin:.1rem 0 .1rem;line-height:1.35}}
.ff-p b{{color:var(--title-ink)}}
.ff-v{{font-family:'JetBrains Mono',monospace;font-size:.68rem;color:var(--ink2);margin:.1rem 0 .45rem;line-height:1.4}}
.ff-d{{font-family:'Barlow',sans-serif;font-size:.79rem;color:var(--ink2);margin:0;
 line-height:1.45;text-align:left}}

/* capítulo 1: figuras nativas */
.figura-nat{{margin:1.4rem 0;background:var(--card);border:1px solid var(--line);border-radius:4px;padding:.7rem}}
.figura-nat .fn-in{{border:2px solid var(--gold-2);border-radius:2px;padding:1.1rem 1rem;background:var(--bg)}}
.figura-nat figcaption{{font-family:'Barlow',sans-serif;font-size:.86rem;color:var(--ink2);
 padding:.7rem .3rem .1rem;line-height:1.5}}
.figura-nat figcaption b{{color:var(--gold-ink);font-weight:700}}
/* painel medido / não medido */
.medpanel{{display:grid;grid-template-columns:1.55fr 1fr;gap:1.1rem}}
@media (max-width:760px){{.medpanel{{grid-template-columns:1fr}}}}
.mp-lado h4{{margin:0 0 .2rem;font-size:1.06rem;letter-spacing:.05em;color:var(--title-ink)}}
.mp-sim h4::before{{content:"";display:inline-block;width:10px;height:10px;border-radius:50%;
 background:var(--fam-v);margin-right:.45rem;vertical-align:.05em}}
.mp-nao h4::before{{content:"";display:inline-block;width:10px;height:10px;border-radius:50%;
 background:var(--sf);margin-right:.45rem;vertical-align:.05em}}
.mp-sub{{font-family:'Barlow',sans-serif;font-size:.79rem;color:var(--ink2);margin:0 0 .7rem;line-height:1.45}}
.medgrid{{display:grid;grid-template-columns:1fr 1fr;gap:.7rem}}
.medc{{background:var(--card);border:1px solid var(--line);border-radius:3px;padding:.6rem .7rem}}
.mc-h{{display:flex;align-items:baseline;justify-content:space-between}}
.mc-h b{{font-family:'JetBrains Mono',monospace;font-size:1.15rem;color:var(--accent-ink)}}
.mc-pos{{font-family:'Barlow',sans-serif;font-size:.58rem;letter-spacing:.14em;text-transform:uppercase;
 color:var(--ink3);font-weight:700}}
.mc-n{{font-family:'Barlow Condensed',sans-serif;font-size:.9rem;letter-spacing:.04em;
 text-transform:uppercase;color:var(--title-ink);display:block}}
.medc p{{margin:.2rem 0 .5rem;font-family:'Barlow',sans-serif;font-size:.75rem;color:var(--ink2);line-height:1.4}}
.mc-bar{{display:flex;height:7px;border-radius:4px;overflow:hidden}}
.mc-bar span{{flex:1}}
.mc-cut{{display:grid;grid-template-columns:1fr 1fr 1fr;margin-top:.15rem;align-items:baseline}}
.mc-cut i{{text-align:right;transform:translateX(50%)}}
.mc-cut em{{text-align:right}}
.mc-cut i{{font-family:'JetBrains Mono',monospace;font-size:.6rem;color:var(--ink3);font-style:normal;display:block}}
.mc-cut em{{font-family:'Barlow',sans-serif;font-size:.6rem;color:var(--ink3);font-style:normal;display:block}}
.nmedgrid{{display:grid;gap:.5rem}}
.nmedc{{background:var(--sf-soft);border:1px dashed var(--sf);border-radius:3px;padding:.5rem .7rem}}
.nmedc b{{font-family:'Barlow Condensed',sans-serif;font-size:.94rem;letter-spacing:.03em;
 text-transform:uppercase;color:var(--sf);display:block}}
.nmedc p{{margin:.1rem 0 0;font-family:'Barlow',sans-serif;font-size:.74rem;color:var(--ink2);line-height:1.4}}
/* esquema em quatro passos */
.passos4{{display:grid;grid-template-columns:repeat(auto-fit,minmax(202px,1fr));gap:.85rem}}
.p4{{background:var(--card);border:1px solid var(--line);border-top:3px solid var(--gold-2);
 border-radius:3px;padding:.75rem .85rem;position:relative;display:flex;flex-direction:column}}
.p4-n{{position:absolute;top:-13px;right:.8rem;width:24px;height:24px;border-radius:50%;
 background:var(--gold-2);color:#3A2708;font-family:'Barlow Condensed',sans-serif;font-weight:700;
 font-size:.92rem;display:flex;align-items:center;justify-content:center}}
.p4 h5{{margin:.1rem 0 .1rem;font-family:'Barlow Condensed',sans-serif;font-size:1.02rem;
 letter-spacing:.09em;text-transform:uppercase;color:var(--title-ink)}}
.p4-s{{font-family:'Barlow',sans-serif;font-size:.76rem;color:var(--ink2);margin:0 0 .5rem;line-height:1.4}}
.p4-l{{list-style:none;margin:0 0 .5rem;padding:0}}
.p4-l li{{display:flex;align-items:baseline;gap:.3rem;flex-wrap:wrap;margin:.2rem 0;
 font-family:'Barlow',sans-serif;font-size:.78rem}}
.p4-l b{{color:var(--ink);font-weight:700}}
.p4-l .p4-d{{color:var(--ink3);font-size:.72rem;flex:1 0 100%;padding-left:1.15rem;margin-top:-.1rem}}
.p4-soma{{display:flex;align-items:center;justify-content:center;gap:.35rem;margin:.5rem 0 .6rem;
 flex-wrap:wrap}}
.p4-soma em{{font-family:'Barlow',sans-serif;font-style:normal;color:var(--ink3);font-weight:700}}
.p4-soma b{{font-family:'Barlow Condensed',sans-serif;font-size:.84rem;letter-spacing:.05em;
 color:var(--title-ink);text-align:center;line-height:1.1}}
.p4-q{{margin:0 0 .5rem;padding-left:1.05rem;font-family:'Barlow',sans-serif;font-size:.78rem;
 color:var(--ink);line-height:1.45}}
.p4-q li{{margin:.2rem 0}}
.p4-nota{{margin:auto 0 0;font-family:'Barlow',sans-serif;font-size:.72rem;color:var(--ink2);
 line-height:1.42;border-top:1px solid var(--linesoft);padding-top:.4rem}}
/* roteiro do livro */
.roteiro{{list-style:none;margin:.8rem 0 0;padding:0;display:grid;
 grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:.35rem .9rem;counter-reset:none}}
.roteiro li{{display:flex;align-items:baseline;gap:.5rem;font-family:'Barlow',sans-serif;
 font-size:.82rem;padding:.22rem 0;border-bottom:1px solid var(--linesoft)}}
.roteiro b{{font-family:'Barlow Condensed',sans-serif;font-size:.95rem;min-width:2.6rem;
 color:var(--gold);letter-spacing:.02em}}
.roteiro span{{color:var(--ink2)}}
.rt-a b{{color:var(--fam-a)}} .rt-m b{{color:var(--fam-m)}} .rt-r b{{color:var(--fam-r)}}
.rt-s b{{color:var(--sf)}}

/* as três famílias */
.mapafam{{display:grid;grid-template-columns:repeat(auto-fit,minmax(268px,1fr));gap:1.1rem;margin:1.2rem 0}}
.famcard{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:4px;
 padding:.65rem .95rem 1.1rem;display:flex;flex-direction:column;border-top:4px solid var(--fam-a)}}
.famcard.fc-m{{border-top-color:var(--fam-m)}} .famcard.fc-r{{border-top-color:var(--fam-r)}}
.famcard figcaption{{display:flex;align-items:baseline;gap:.5rem;flex-wrap:wrap;
 border-bottom:1px solid var(--linesoft);padding-bottom:.4rem;text-align:left}}
.fm-n{{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:1.7rem;
 line-height:1;color:var(--gold)}}
.fm-t{{font-family:'Barlow Condensed',sans-serif;font-size:1.2rem;font-weight:700;letter-spacing:.05em;
 text-transform:uppercase;color:var(--title-ink);flex:1}}
.fm-g{{font-family:'Barlow',sans-serif;font-size:.64rem;letter-spacing:.12em;text-transform:uppercase;
 color:var(--ink3);font-weight:700}}
.fm-lead{{font-family:'Barlow',sans-serif;font-size:.85rem;color:var(--ink);margin:.45rem 0 .5rem;
 line-height:1.45;text-align:left;font-weight:600}}
.fm-subs{{display:flex;flex-direction:column;gap:.22rem;margin-bottom:.3rem}}
.fm-sub{{display:flex;align-items:center;gap:.18rem}}
.fm-sub em{{font-family:'Barlow',sans-serif;font-style:normal;font-size:.74rem;color:var(--ink2);
 margin-left:.3rem;letter-spacing:.02em}}
.famcard .facereg{{margin:.3rem auto .5rem}}
.fm-regs{{font-family:'Barlow',sans-serif;font-size:.81rem;color:var(--ink);margin:0 0 .45rem;
 line-height:1.45;text-align:left;font-weight:600}}
.fm-nota{{font-family:'Barlow',sans-serif;font-size:.78rem;color:var(--ink2);margin:auto 0 0;
 line-height:1.5;text-align:left;border-top:1px solid var(--linesoft);padding-top:.45rem}}
/* os três usos do alto G' */
.usos{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:.9rem;margin:1rem 0}}
.usocard{{margin:0;background:var(--card);border:1px solid var(--line);border-left:3px solid var(--fam-r);
 border-radius:3px;padding:.55rem .8rem .9rem;text-align:center}}
.usocard figcaption{{display:flex;align-items:center;justify-content:center;gap:.25rem;
 padding-bottom:.35rem;border-bottom:1px solid var(--linesoft)}}
.usocard figcaption b{{font-family:'Barlow Condensed',sans-serif;font-size:1rem;letter-spacing:.07em;
 text-transform:uppercase;color:var(--title-ink);margin-left:.3rem}}
.usocard p{{font-family:'Barlow',sans-serif;font-size:.78rem;color:var(--ink2);margin:.2rem 0 0;
 line-height:1.45;text-align:left}}

.capa-face .rg{{fill-opacity:.72;stroke-width:2.4}}

.fam3{{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:.85rem;margin:1rem 0}}
.f3{{background:var(--card);border:1px solid var(--line);border-left:5px solid var(--fam-a);
 border-radius:3px;padding:.75rem .9rem}}
.f3-m{{border-left-color:var(--fam-m)}} .f3-r{{border-left-color:var(--fam-r)}}
.f3 b{{font-family:'Barlow Condensed',sans-serif;font-size:1.12rem;letter-spacing:.05em;
 text-transform:uppercase;color:var(--title-ink);display:block;line-height:1.1}}
.f3 span{{font-family:'Barlow',sans-serif;font-size:.68rem;letter-spacing:.18em;text-transform:uppercase;
 font-weight:700;display:block;margin-bottom:.35rem}}
.f3-a span{{color:var(--fam-a)}} .f3-m span{{color:var(--fam-m)}} .f3-r span{{color:var(--fam-r)}}
.f3 p{{margin:0;font-family:'Barlow',sans-serif;font-size:.81rem;color:var(--ink2);line-height:1.5}}
.stat.st-a{{border-top:3px solid var(--fam-a)}} .stat.st-m{{border-top:3px solid var(--fam-m)}}
.stat.st-r{{border-top:3px solid var(--fam-r)}} .stat.st-s{{border-top:3px solid var(--sf)}}
.fam-de{{color:var(--gold-3);letter-spacing:.16em}}
/* figuras e ilustrações com moldura dourada */
.figura-img{{margin:1.4rem 0;background:var(--card);border:1px solid var(--line);border-radius:4px;padding:.7rem}}
.figura-img>img{{display:block;width:100%;height:auto;border:2px solid var(--gold-2)}}
.figura-img figcaption{{font-family:'Barlow',sans-serif;font-size:.86rem;color:var(--ink2);padding:.7rem .3rem .1rem;line-height:1.5}}
.figura-img figcaption b{{color:var(--gold-ink);font-weight:700}}
.figura-img.sci>img{{background:#FBF9F6;padding:.5rem;border:2px solid var(--gold-2);border-radius:2px}}
.figura-img.sci{{background:var(--card)}}
/* box QR no padrão do autor */
.qrbox{{margin:1.6rem 0;border:1px solid var(--line);border-left:4px solid var(--gold-2);background:var(--card);border-radius:4px;overflow:hidden}}
.bx-head{{font-size:.9rem;font-weight:700;letter-spacing:.24em;text-transform:uppercase;padding:.5rem 1.2rem;color:var(--gold-3);background:linear-gradient(100deg,var(--navy) 0%,var(--navy-2) 70%,var(--navy-3) 130%)}}
.saibamais .bx-head{{background:linear-gradient(100deg,#08343A 0%,#0F7480 120%)}}
.bx-body{{display:flex;gap:1.1rem;padding:1.1rem 1.2rem;align-items:center;flex-wrap:wrap}}
.bx-ilus{{margin:0;flex:0 0 218px;max-width:100%}}
.bx-ilus img{{display:block;width:100%;height:auto;border:2px solid var(--gold-2)}}
.bx-ilus figcaption{{font-family:'Barlow',sans-serif;font-size:.72rem;color:var(--ink3);padding-top:.35rem;line-height:1.4}}
.bx-txt{{flex:1;min-width:210px}}
.bx-body h4{{margin:0 0 .35rem;font-size:1.16rem;font-weight:600;text-transform:uppercase;letter-spacing:.01em;color:var(--gold-ink)}}
.bx-body p{{margin:.2rem 0;font-size:.93rem;max-width:56ch}}
.bx-qrwrap{{flex:none;text-align:center}}
.bx-qr{{border:2px solid var(--gold-2);background:#fff;padding:5px;display:block}}
.bx-qrwrap span{{display:block;font-size:.66rem;letter-spacing:.16em;text-transform:uppercase;color:var(--ink3);margin-top:.35rem}}
.bx-url a{{font-size:.76rem;word-break:break-all;color:var(--ink3)}}
.fichatec{{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:1rem 1.3rem;margin-bottom:.4rem}}
.fichatec .meta{{display:flex;flex-wrap:wrap;gap:.4rem 1.8rem;color:var(--ink2);font-size:.92rem;margin:0}}
.fichatec .meta b{{color:var(--ink)}}
.stats{{display:flex;flex-wrap:wrap;gap:1rem;margin-top:.9rem}}
.stat{{background:var(--card);border:1px solid var(--line);border-top:4px solid var(--accent);border-radius:4px;padding:.7rem 1.1rem;min-width:8.5rem}}
.stat:nth-child(1){{border-top-color:var(--fam-a)}} .stat:nth-child(2){{border-top-color:var(--fam-m)}}
.stat:nth-child(3){{border-top-color:var(--fam-r)}} .stat:nth-child(4){{border-top-color:var(--sf)}}
.stat b{{display:block;font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:1.75rem;line-height:1.05;color:var(--gold-ink)}}
.stat span{{font-size:.8rem;color:var(--ink2)}}
section{{margin-top:2.8rem}}
h2{{font-size:1.9rem;font-weight:700;margin:0 0 .8rem;color:var(--title-ink)}}
.fambanner h2{{font-size:2.05rem}}
h3{{font-size:1.28rem;font-weight:600;margin:1.6rem 0 .5rem;color:var(--title-ink);border-bottom:1px solid var(--line);padding-bottom:.3rem}}
p{{max-width:76ch}} .lead{{color:var(--ink2)}}
.box{{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:1.1rem 1.3rem}}
.qt{{border-left:4px solid var(--gold-2);background:var(--gold-soft);border-radius:0 4px 4px 0;padding:.85rem 1.15rem;font-family:'Source Serif 4',serif;font-style:italic;font-size:1.08rem;margin:1.1rem 0;max-width:70ch}}
.fund{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:.9rem}}
.fund .box{{border-top:4px solid var(--accent)}}
.fund .box:nth-child(1){{border-top-color:var(--fam-r)}} .fund .box:nth-child(2){{border-top-color:var(--fam-a)}}
.fund .box:nth-child(3){{border-top-color:var(--chip-rosa)}} .fund .box:nth-child(4){{border-top-color:var(--fam-v)}}
.fund .box b.t{{font-family:'JetBrains Mono',monospace;color:var(--accent-ink);font-size:1.02rem}}
.fund .box p{{margin:.35rem 0 0;font-size:.92rem;color:var(--ink2)}}
.freq{{width:100%;border-collapse:collapse;font-size:.9rem;margin-top:.8rem}}
.freq th,.freq td{{border-bottom:1px solid var(--linesoft);padding:.45rem .6rem;text-align:left}}
.anti{{columns:2;column-gap:2rem;font-size:.92rem;margin:.4rem 0 0;padding-left:1.1rem}}
.anti li{{margin:.25rem 0;break-inside:avoid}} @media(max-width:46rem){{.anti{{columns:1}}}}
.g33{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.9rem;margin:.8rem 0}}
.passos{{counter-reset:passo}}
.passo{{position:relative;padding-left:2.6rem}}
.passo::before{{counter-increment:passo;content:counter(passo);position:absolute;left:.7rem;top:1rem;width:1.35rem;height:1.35rem;border-radius:50%;background:var(--accent);color:#fff;font:700 .85rem 'Source Sans 3',sans-serif;display:flex;align-items:center;justify-content:center}}
.chart{{width:100%;height:auto;background:var(--card);border:1px solid var(--line);border-radius:4px;margin-top:.6rem}}
.grid{{stroke:var(--linesoft);stroke-width:1}} .za{{fill:var(--za)}} .zm{{fill:var(--zm)}} .zr{{fill:var(--zr)}}
.ax{{fill:var(--ink3);font:11px 'JetBrains Mono',monospace}}
.axt{{fill:var(--ink2);font:600 12px 'Source Sans 3',sans-serif}}
.zlb{{fill:var(--ink3);font:700 10.5px 'Source Sans 3',sans-serif;letter-spacing:.04em}}
.iso{{stroke:var(--ink3);stroke-width:1;stroke-dasharray:5 4;opacity:.6}}
.isolb{{fill:var(--ink3);font:600 10px 'JetBrains Mono',monospace}}
.dot{{stroke:var(--card);stroke-width:2;cursor:pointer}} .dot:hover{{r:8}}
.dlb{{fill:var(--ink2);font:600 10.5px 'Source Sans 3',sans-serif;paint-order:stroke;stroke:var(--card);stroke-width:3px;stroke-linejoin:round}}
.bn{{fill:var(--ink2);font:600 10.5px 'Source Sans 3',sans-serif}}
.bv{{fill:var(--ink3);font:9.5px 'JetBrains Mono',monospace}}
.bar:hover{{opacity:.8}}
.legend{{display:flex;flex-wrap:wrap;gap:.4rem 1.4rem;margin:.7rem 0 0;font-size:.9rem;color:var(--ink2)}}
.legend span{{display:inline-flex;align-items:center;gap:.4rem}}
.legend i{{width:11px;height:11px;border-radius:50%;display:inline-block}}
#tip{{position:fixed;pointer-events:none;background:var(--ink);color:var(--bg);padding:.35rem .6rem;border-radius:8px;font-size:.8rem;opacity:0;transition:opacity .1s;z-index:9;max-width:280px}}
.radar{{flex:none;width:96px;height:96px}} .radar-sm{{width:72px;height:72px}} .radar-lg{{width:150px;height:150px}}
.rd-grid{{fill:none;stroke:var(--linesoft);stroke-width:1}} .rd-ax{{stroke:var(--linesoft);stroke-width:1}}
.rd-lb{{fill:var(--ink3);font:600 8.5px 'JetBrains Mono',monospace}} .radar-lg .rd-lb{{font-size:10px}}
.rdemos{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:1rem;margin:.8rem 0}}
.rdemo{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:4px;padding:.9rem;text-align:center}}
.rdemo figcaption{{font-size:.82rem;color:var(--ink2);margin-top:.4rem}} .rdemo b{{color:var(--ink)}}
/* face / figuras */
.fc-face{{fill:url(#fcSkin);stroke:var(--face-line);stroke-width:1.6;stroke-linejoin:round}}
.fc-neck{{fill:var(--face-sh);stroke:var(--face-line);stroke-width:1.3;opacity:.92}}
.fc-sh{{fill:var(--face-fill);stroke:var(--face-line);stroke-width:1.2;opacity:.75}}
.fc-hairb{{fill:url(#fcHair);stroke:var(--hair-line);stroke-width:1.3;stroke-linejoin:round}}
.fc-hairf{{fill:url(#fcHair);stroke:var(--hair-line);stroke-width:1.2;stroke-linejoin:round}}
.fc-blush ellipse{{fill:var(--blush);opacity:.5}}
.fc-feat path{{fill:none;stroke:var(--face-line);stroke-width:1.35;stroke-linecap:round;stroke-linejoin:round}}
.fc-eye{{fill:var(--eye-white);stroke:var(--face-line);stroke-width:1.35}}
.fc-lid{{stroke:var(--lash);stroke-width:2.1}}
.fc-brow{{stroke:var(--hair-1);stroke-width:3.4;stroke-linecap:round}}
.fc-crease{{stroke:var(--face-line);stroke-width:.9;opacity:.55}}
.fc-nose{{stroke-width:1.2;opacity:.8}}
.fc-lip{{fill:var(--lip);stroke:var(--lip-line);stroke-width:1.1}}
.fc-lipline{{stroke:var(--lip-line);stroke-width:1.2}}
.fc-chin{{stroke-width:1;opacity:.5}}
.fc-iris circle{{fill:var(--iris)}}
.fc-pupil circle{{fill:var(--pupil)}}
.fc-glint{{fill:#fff;opacity:.9}}
.fc-lash path{{fill:none;stroke:var(--lash);stroke-width:1.5;stroke-linecap:round}}
.fc-dot{{stroke:var(--card);stroke-width:2.2}}
.fc-halo{{opacity:.17}}
.fc-ld{{stroke:var(--ink3);stroke-width:1;stroke-dasharray:2 3}}
.fc-lb{{fill:var(--ink2);font:600 11.5px 'Barlow',sans-serif;letter-spacing:.02em}}
.capa-face .fc-face{{fill:rgba(255,255,255,.14);stroke:rgba(255,255,255,.78)}}
.capa-face .fc-hairb,.capa-face .fc-hairf{{fill:rgba(255,255,255,.07);stroke:rgba(255,255,255,.42)}}
.capa-face .fc-neck,.capa-face .fc-sh{{fill:rgba(255,255,255,.05);stroke:rgba(255,255,255,.4)}}
.capa-face .fc-feat path{{stroke:rgba(255,255,255,.62)}}
.capa-face .fc-eye{{fill:rgba(255,255,255,.22)}}
.capa-face .fc-lip{{fill:rgba(255,255,255,.18);stroke:rgba(255,255,255,.55)}}
.capa-face .fc-blush ellipse{{opacity:.18}}
.capa-face .fc-iris circle{{fill:rgba(255,255,255,.55)}}
.capa-face .fc-pupil circle{{fill:rgba(10,53,87,.8)}}
.capa-face .fc-brow{{stroke:rgba(255,255,255,.55)}}
.capa-face .fc-dot{{stroke:rgba(10,53,87,.9)}}
figure.figura{{margin:1.2rem 0;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1rem 1.2rem;text-align:center}}
figure.figura figcaption{{text-align:left;font-size:.85rem;color:var(--ink2);border-top:1px solid var(--linesoft);margin-top:.8rem;padding-top:.6rem}}
figure.figura figcaption b{{color:var(--ink)}}
.gelrow{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:1rem;margin:1rem 0}}
.gelcard{{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:1rem;text-align:center}}
.gelico{{width:88px;height:88px}}
.gelcard h4{{margin:.4rem 0 .2rem;font-size:1.12rem;font-weight:600;text-transform:uppercase;color:var(--title-ink)}}
.gelcard p{{font-size:.88rem;color:var(--ink2);margin:.2rem 0}}
.gelcard .gelsub{{font-family:'JetBrains Mono',monospace;font-size:.68rem;letter-spacing:.14em;color:var(--ink3)}}
/* boxes estilo aprovado */
.pratica,.saibamais{{margin:1.4rem 0;border:1px solid var(--line);border-radius:10px;overflow:hidden;background:var(--card)}}
.bx-head{{font-family:'JetBrains Mono',monospace;font-size:.72rem;letter-spacing:.26em;padding:.45rem 1.1rem;color:#fff;background:var(--accent)}}
.saibamais .bx-head{{background:var(--sf)}}
.bx-body{{display:flex;gap:1.2rem;padding:1rem 1.2rem;align-items:center;flex-wrap:wrap}}
.bx-body h4{{margin:0 0 .3rem;font-size:1.16rem}}
.bx-body p{{margin:.2rem 0;font-size:.92rem;max-width:58ch}}
.bx-body>div{{flex:1;min-width:230px}}
.bx-qr{{border:1px solid var(--line);border-radius:8px;background:#fff;padding:4px;flex:none}}
.bx-url a{{font-size:.78rem;word-break:break-all;color:var(--ink3)}}
/* bandeiras */
.fambanner{{display:flex;flex-wrap:wrap;gap:.6rem 2.5rem;align-items:center;justify-content:space-between;border-radius:10px;padding:1.15rem 1.4rem;margin-bottom:1.1rem;border:1px solid var(--line)}}
.fambanner{{border-radius:4px;color:#fff;border:none;position:relative}}
.fambanner::after{{content:"";position:absolute;left:0;right:0;bottom:0;height:4px}}
.bn-a{{background:linear-gradient(112deg,var(--navy) 0%,var(--navy-2) 62%,#2E76A8 128%)}}
.bn-a::after{{background:var(--fam-a)}}
.bn-m{{background:linear-gradient(112deg,var(--navy) 0%,var(--navy-2) 62%,#2E76A8 128%)}}
.bn-m::after{{background:var(--fam-m)}}
.bn-r{{background:linear-gradient(112deg,var(--navy) 0%,var(--navy-2) 62%,#2E76A8 128%)}}
.bn-r::after{{background:var(--fam-r)}}
.bn-s{{background:linear-gradient(112deg,#062A30 0%,#0A4A53 66%,#0F7480 130%)}}
.bn-s::after{{background:var(--sf)}}
.fambanner .fam-eyebrow{{color:var(--gold-3)}}
.fambanner h2{{color:#fff}}
.fambanner .famchave{{color:rgba(255,255,255,.9)}}
.fambanner .famdesc{{color:rgba(255,255,255,.82)}}
.fambanner .famdesc b{{color:var(--gold-3)}}
.fambanner .chip{{border-color:rgba(255,255,255,.35)}}
.fam-eyebrow{{font-family:'JetBrains Mono',monospace;font-size:.7rem;letter-spacing:.14em;color:var(--ink2);margin:0 0 .25rem}}
.fambanner h2{{margin:0;font-size:1.7rem}}
.famchave{{font-family:'Source Serif 4',serif;font-style:italic;font-size:1.04rem;color:var(--ink2);margin:.4rem 0 0;max-width:46ch}}
.famdesc{{margin:0;color:var(--ink2);font-size:.92rem;max-width:38rem}}
.grid2{{display:grid;grid-template-columns:repeat(auto-fill,minmax(350px,1fr));gap:1rem}}
.grid3{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1rem}}
/* cards */
.card{{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:0 1.1rem 1rem;display:flex;flex-direction:column;gap:.5rem;break-inside:avoid;border-left-width:6px;border-left-style:solid}}
.card.fam-a{{border-left-color:var(--fam-a)}} .card.fam-m{{border-left-color:var(--fam-m)}} .card.fam-r{{border-left-color:var(--fam-r)}}
.card header{{display:flex;justify-content:space-between;gap:.6rem;align-items:flex-start;margin:0 -1.1rem;padding:.7rem 1.1rem .5rem}}
.card.fam-a header{{background:linear-gradient(90deg,color-mix(in srgb,var(--fam-a) var(--tint),transparent),transparent 75%)}}
.card.fam-m header{{background:linear-gradient(90deg,color-mix(in srgb,var(--fam-m) var(--tint),transparent),transparent 75%)}}
.card.fam-r header{{background:linear-gradient(90deg,color-mix(in srgb,var(--fam-r) var(--tint),transparent),transparent 75%)}}
.card h4{{font-size:1.2rem;font-weight:600;margin:0;line-height:1.12;text-transform:uppercase;letter-spacing:.005em;color:var(--title-ink)}}
.c-right{{display:flex;flex-direction:column;align-items:flex-end;gap:.1rem}}
.marca{{font-size:.72rem;color:var(--ink3);white-space:nowrap;letter-spacing:.03em}}
.famtag{{font-size:.76rem;font-weight:700;letter-spacing:.07em;white-space:nowrap;text-transform:uppercase}}
.sigdots{{display:flex;gap:.9rem;font-size:.72rem;color:var(--ink3);padding-bottom:.3rem}}
.assin{{margin:0 0 .1rem;display:flex;flex-direction:column;gap:.1rem;border-bottom:1px solid var(--linesoft);padding-bottom:.45rem}}
.assin-lbl{{font-family:'Source Sans 3',sans-serif;font-size:.62rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--ink3)}}
.assin-v{{display:flex;align-items:center;gap:.3rem;font-family:'Barlow Condensed',sans-serif;font-size:1rem;font-weight:700;letter-spacing:.02em}}
.assin-v i{{width:13px;height:13px;border-radius:50%;display:inline-block;border:1.5px solid rgba(0,0,0,.16)}}
.assin-v .plus{{color:var(--ink3);font-size:.7rem}}
.assin-v b{{color:var(--ink);font-weight:700}}
.ico{{flex:none}}
.logo{{height:auto}}
.lg-e{{stroke:var(--accent-ink);stroke-width:1.6;opacity:.5}}
.lg-n{{fill:var(--accent-ink)}}
.gram{{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:.9rem;margin:.9rem 0}}
.gramc{{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:1rem;display:flex;gap:.8rem;align-items:flex-start}}
.gramc h4{{margin:0 0 .1rem;font-size:1.14rem;font-weight:600;text-transform:uppercase;color:var(--title-ink)}}
.gramc .verbo{{font-family:'JetBrains Mono',monospace;font-size:.68rem;letter-spacing:.1em;display:block;margin-bottom:.25rem}}
.gramc p{{margin:0;font-size:.85rem;color:var(--ink2)}}
.a9{{display:grid;grid-template-columns:repeat(auto-fit,minmax(168px,1fr));gap:.6rem;margin:.9rem 0}}
.a9c{{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:.65rem .8rem;text-align:center}}
.a9dots{{display:flex;align-items:center;justify-content:center;gap:.25rem;margin-bottom:.35rem}}
.a9dots i{{width:16px;height:16px;border-radius:50%;display:inline-block;border:1.5px solid rgba(0,0,0,.16)}}
.a9dots span{{color:var(--ink3);font-size:.8rem}}
.a9n{{font-family:'Barlow Condensed',sans-serif;font-size:.92rem;font-weight:700;letter-spacing:.03em;line-height:1.15;display:block;color:var(--title-ink)}}
.a9q{{font-size:.72rem;color:var(--ink3);display:block;margin-top:.2rem}}
.sd{{display:inline-flex;align-items:center;gap:.3rem}}
.sd i{{width:12px;height:12px;border-radius:50%;display:inline-block;border:1.5px solid rgba(0,0,0,.16)}}
.vis{{display:flex;gap:.9rem;align-items:center;border-bottom:1px solid var(--linesoft);padding-bottom:.55rem}}
.vis-col{{flex:1;display:flex;flex-direction:column;gap:.3rem;min-width:0}}
.sig{{display:grid;grid-template-columns:1fr 1fr;gap:.15rem .8rem;font-family:'JetBrains Mono',monospace;font-size:.78rem;color:var(--ink2)}}
.sig b{{color:var(--ink);font-weight:700}}
.lote{{color:var(--ink3);font-size:.7rem;font-family:'JetBrains Mono',monospace}}
.rg{{width:100%;max-width:260px;height:auto}}
.rg-tr{{stroke:var(--line);stroke-width:2;stroke-linecap:round}} .rg-tick{{stroke:var(--ink3);stroke-width:1}}
.rg-dot{{stroke:var(--card);stroke-width:1.5}} .rg-lb{{fill:var(--ink2);font:600 9.5px 'JetBrains Mono',monospace}}
.comp{{margin:0;font-size:.93rem}}
.lbl{{display:block;font-size:.68rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--ink3);margin-bottom:.15rem}}
.mp{{margin:0;font-weight:600;font-size:.93rem}}
.pills{{display:flex;flex-wrap:wrap;gap:.3rem}}
.pill{{font-size:.78rem;padding:.16rem .55rem;border-radius:999px;line-height:1.25}}
.pill i{{font-style:normal;font-size:.66rem;opacity:.85;margin-left:.35rem;letter-spacing:.04em}}
.n1{{background:var(--n1bg);color:var(--n1ink);font-weight:600}} .n2{{background:var(--n2bg);color:var(--n2ink);font-weight:600}}
.n3{{border:1.5px solid var(--n3bd);color:var(--n3ink)}} .n4{{border:1.5px dashed var(--line);color:var(--n4ink)}}
.evite{{margin:0;font-size:.85rem;color:var(--ink2)}} .lbl-ev{{color:var(--warn)}}
.escolha{{margin:0;border-left:3px solid var(--gold-2);background:var(--gold-soft);padding:.5rem .7rem;border-radius:0 4px 4px 0;font-size:.92rem;font-style:italic}}
.alts,.tech{{margin:0;font-size:.82rem;color:var(--ink2)}}
.flags{{margin:0;font-size:.76rem;color:var(--flag);font-weight:600}}
.sfcard{{background:var(--card);border:1px solid var(--line);border-left:6px solid var(--sf);border-radius:4px;padding:.9rem 1rem;display:flex;flex-direction:column;gap:.45rem;break-inside:avoid}}
.sfcard header{{display:flex;align-items:baseline;gap:.3rem;flex-wrap:wrap}}
.sfcard h4{{font-size:1.1rem;font-weight:600;text-transform:uppercase;margin:0;color:var(--title-ink)}}
.sfcard .marca{{margin-left:auto}}
.sfnum{{display:flex;align-items:center;gap:1rem;font-family:'JetBrains Mono',monospace;font-size:.8rem;color:var(--ink2);background:var(--sf-soft);border-radius:10px;padding:.35rem .7rem}}
.sfnum b{{color:var(--ink)}} .sfnum .radar-sm{{margin-left:auto}}
.sfcard p{{margin:0;font-size:.88rem}}
.sflink{{font-size:.8rem;text-decoration:none;font-weight:600;color:var(--sf)}}
.sflink:hover{{text-decoration:underline}}
.regtab{{overflow-x:auto;border:1px solid var(--line);border-radius:4px;background:var(--card)}}
.regtab table{{border-collapse:collapse;width:100%;font-size:.88rem;min-width:720px}}
.regtab th,.regtab td{{padding:.5rem .7rem;border-bottom:1px solid var(--linesoft);text-align:left;vertical-align:top}}
.regtab th{{font-family:'Barlow',sans-serif;font-size:.76rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#fff;background:var(--navy-2)}}
.regtab .obs{{color:var(--ink3);font-size:.8rem}}
.ix{{columns:3;column-gap:2rem}} @media(max-width:56rem){{.ix{{columns:2}}}} @media(max-width:38rem){{.ix{{columns:1}}}}
.ixm{{break-inside:avoid;margin-bottom:.9rem;font-size:.88rem}}
.ixm b{{display:block;font-family:'Barlow Condensed',sans-serif;font-size:1.06rem;font-weight:700;text-transform:uppercase;color:var(--gold-ink);margin-bottom:.15rem;border-bottom:1px solid var(--linesoft)}}
.ixm a{{display:block;text-decoration:none;color:var(--ink2);padding:.06rem 0}}
.ixm a:hover{{color:var(--accent-ink);text-decoration:underline}}
.rodape{{margin-top:3rem;border-top:1px solid var(--line);padding-top:1rem;color:var(--ink3);font-size:.82rem}}
@media print{{ body{{background:#fff;font-size:10.5px}} .famsec,#rankings,#regioes,#textura,#atlas{{break-before:page}}
 .card,.sfcard,.rdemo,.qrbox,.figura-img,.gelcard,.gramc{{break-inside:avoid}} #tip{{display:none}}
 .capa-in{{-webkit-print-color-adjust:exact;print-color-adjust:exact}} .fambanner,.bx-head,.regtab th{{-webkit-print-color-adjust:exact;print-color-adjust:exact}} }}
@media(max-width:30rem){{.vis{{flex-direction:column;align-items:flex-start}}}}

/* ================= impressão: livro em página real ================= */
@media print{{
 @page{{size:210mm 280mm;margin:15mm 14mm 16mm}}
 html,body{{background:#fff}}
 main{{padding:0;background:#fff}}
 .folha{{max-width:none;margin:0;border:none;box-shadow:none;padding:0 0 6mm;
  break-after:page;page-break-after:always}}
 .folha:last-child{{break-after:auto;page-break-after:auto}}
 .folha::before{{display:none}}
 .folha::after{{margin:8mm 0 0;padding-top:9mm;background-size:110px 15px}}
 .cap-abre{{break-after:avoid;page-break-after:avoid}}
 h2,h3,h4{{break-after:avoid;page-break-after:avoid}}
 .box,.gelcard,.card,figure,table{{break-inside:avoid;page-break-inside:avoid}}
 .capa{{break-after:page;page-break-after:always}}
 a[href^="http"]::after{{content:""}}
}}
</style>
<main>
<header class="capa">
<div class="capa-in">
<div class="capa-spine"></div>
<div class="capa-frame">
<p class="capa-brand">Reology Map · Ciência que guia escolhas</p>
<span class="capa-dot"></span>
<h1><span class="t1">Reologia</span><span class="t2"><i></i>dos<i></i></span><span class="t1">Géis de</span><span class="t3">Ácido Hialurônico</span></h1>
<p class="capa-sub">Fundamentos, Classificação e Aplicações Clínicas</p>
{capa_arte()}
{capa_orn()}
<p class="capa-autor">Dr. João Pithon</p>
<p class="capa-ed">Primeira edição · São Paulo · 2026</p>
</div>
</div>
<div class="capa-band"></div>
</header>

<div class="fichatec">
<p class="meta"><span>Estudo <b>Reológico Pithon Napoli (2026)</b> — 76 ensaios · 75 produtos canônicos sob protocolo único</span><span>Ensaio <b>reômetro rotacional TA Instruments AR-1500ex</b> · 25&nbsp;°C · placas Ø20&nbsp;mm · gap 500&nbsp;µm · varredura 10&nbsp;→&nbsp;0,01&nbsp;Hz</span><span>Frequência de referência <b>0,7&nbsp;Hz</b></span></p>
<div class="stats"><div class="stat st-a"><b>34</b><span>família azul · baixo G′</span></div><div class="stat st-m"><b>14</b><span>família amarela · moderado G′</span></div><div class="stat st-r"><b>28</b><span>família roxa · alto G′</span></div><div class="stat st-s"><b>💧</b><span>baixo swelling factor: uso na olheira</span></div></div>
<p class="qt" style="margin:1rem 0 .2rem">“Não existe o melhor preenchedor. Existe a propriedade reológica mais adequada para o comportamento que queremos produzir em cada região.”</p>
</div>


<section class="folha" id="molecula">
{cap_head('Capítulo 2','A molécula e a rede — de onde vem o G′',
 'Antes de qualquer número existe química. Três desenhos explicam por que um gel de ácido hialurônico resiste, escoa e um dia desaparece.')}
<h3>2.1 &nbsp;A molécula: um dissacarídeo repetido milhares de vezes</h3>
<p class="lead">O ácido hialurônico é um <b>glicosaminoglicano linear</b> formado pela repetição de uma única unidade dissacarídica: <b>ácido D-glicurônico</b> (GlcA, C<sub>6</sub>H<sub>10</sub>O<sub>7</sub>) e <b>N-acetil-D-glicosamina</b> (GlcNAc, C<sub>8</sub>H<sub>15</sub>NO<sub>6</sub>). As duas unidades se unem alternadamente por ligações <b>β(1→3)</b> e <b>β(1→4)</b>, e uma única cadeia pode conter de <b>2.000 a mais de 25.000</b> dessas unidades.</p>
{figura('1', ILU2['conc_molecula'], 'Arquitetura molecular do ácido hialurônico: as duas unidades monossacarídicas em projeção de Haworth e modelo tridimensional, com as ligações glicosídicas alternadas β(1→3) e β(1→4). Os grupos que aparecem na cadeia — carboxila (COO<sup>−</sup>), hidroxila (OH) e acetamido (NH-COCH<sub>3</sub>) — são os que dão ao HA sua avidez por água e, no passo seguinte, os pontos onde a reticulação acontece.', 'estrutura molecular do ácido hialurônico', cls='sci')}
<div class="box"><p style="margin:0"><b>O que distingue o HA dos outros glicosaminoglicanos:</b> ele <b>não possui grupamentos sulfatados</b> e <b>não está ligado covalentemente a proteínas</b>. É por isso que o HA nativo é solúvel, altamente hidratado e rapidamente degradado — e é justamente por isso que, para virar preenchedor, ele precisa ser <b>reticulado</b>.</p></div>

{filete('cadeia', 160)}
<h3>2.2 &nbsp;Da solução ao hidrogel: a reticulação</h3>
<p class="lead">Uma solução de HA não sustenta nada: as cadeias deslizam livremente umas sobre as outras. O que transforma solução em <b>gel</b> é a criação de pontes covalentes entre cadeias — a reticulação. Este é o passo que faz nascer o G′.</p>
<div class="etapas">
<div class="etapa"><div class="n">1</div><b>Solução de HA</b><p>Cadeias lineares de ácido hialurônico dispersas em solução aquosa, sem ligação entre si.</p></div>
<div class="etapa"><div class="n">2</div><b>Agente reticulante</b><p>Molécula com grupos reativos nas duas pontas. O mais usado é o <b>BDDE</b> — <code>1,4-butanodiol diglicidil éter</code> —, cujos grupos epóxi são os sítios reativos.</p></div>
<div class="etapa"><div class="n">3</div><b>Reação de reticulação</b><p>Os grupos epóxi reagem com as <b>hidroxilas (−OH)</b> das cadeias de HA formando <b>ligações éter covalentes</b>, estáveis.</p></div>
<div class="etapa"><div class="n">4</div><b>Rede tridimensional</b><p>Múltiplas ligações cruzadas formam uma rede 3D que <b>aprisiona grande quantidade de água</b>. É esse conjunto — rede + água — que chamamos de hidrogel.</p></div>
</div>
{figura('2', ILU2['conc_hidrogel'], 'Formação do hidrogel de ácido hialurônico em quatro etapas: solução, agente reticulante (BDDE), reação com as hidroxilas formando ligações éter e a rede tridimensional que retém água. O detalhe mostra a ligação éter no ponto de reticulação. <b>É deste desenho que vem o ornamento das cadeias em contas usado nos rodapés deste livro</b> — a identidade visual do Reology Map nasce da própria molécula.', 'formação do hidrogel de ácido hialurônico por reticulação', cls='sci')}
<p><b>Reticulantes descritos na literatura:</b> BDDE (1,4-butanodiol diglicidil éter) · DVS (divinil sulfona) · EGDE (etilenoglicol diglicidil éter) · PEGDGE (polietilenoglicol diglicidil éter).</p>
<div class="box"><p style="margin-top:0"><b>O grau de reticulação governa três propriedades ao mesmo tempo</b> — e é aqui que a química encontra a reologia:</p>
<div class="g33 passos" style="margin-top:.6rem">
<div class="box passo"><b style="color:var(--fam-a)">Baixo grau de reticulação</b><p style="margin:.3rem 0 0;font-size:.9rem;color:var(--ink2)">Gel mais macio · maior inchamento · degradação mais rápida.</p></div>
<div class="box passo"><b style="color:var(--fam-r)">Alto grau de reticulação</b><p style="margin:.3rem 0 0;font-size:.9rem;color:var(--ink2)">Gel mais firme · menor inchamento · degradação mais lenta.</p></div>
<div class="box passo"><b style="color:var(--gold-ink)">O que isso mede</b><p style="margin:.3rem 0 0;font-size:.9rem;color:var(--ink2)">Firmeza é <b>G′</b>. Inchamento é <b>swelling factor</b> — que este estudo <b>não mediu</b> (💧).</p></div>
</div></div>
<p class="qt">Cuidado com o atalho: a reticulação <i>explica</i> o G′, mas a <b>tecnologia declarada não prevê a faixa de G′</b>. No banco deste livro, DVS não significa alto G′ e NASHA não significa alto G′. A química é a causa; o reômetro é a medida.</p>

{filete('cadeia', 160)}
<h3>2.3 &nbsp;A rede desfeita: hialuronidase</h3>
<p class="lead">A mesma ligação que constrói a cadeia é a que permite desfazê-la. A <b>hialuronidase</b> cliva especificamente a ligação <b>β(1→4)</b> entre o GlcA e a GlcNAc — e só essa. É a base bioquímica da reversão de um preenchimento.</p>
{figura('3', ILU2['conc_hialuron'], 'Degradação do gel de ácido hialurônico pela hialuronidase: o sítio de clivagem na ligação β(1→4), o mecanismo catalítico em quatro passos (reconhecimento, posicionamento da água no sítio ativo, clivagem hidrolítica e liberação dos oligossacarídeos) e o efeito progressivo sobre o gel.', 'ação da hialuronidase sobre o gel de ácido hialurônico', cls='sci')}
<div class="etapas">
<div class="etapa"><div class="n">1</div><b>Gel íntegro</b><p>Alta viscosidade · rede tridimensional estável · capacidade plena de sustentação.</p></div>
<div class="etapa"><div class="n">2</div><b>Degradação parcial</b><p>Viscosidade reduzida · perda parcial da sustentação · formação de cadeias menores.</p></div>
<div class="etapa"><div class="n">3</div><b>Degradação completa</b><p>Solução fluida · perda total da estrutura de gel · eliminação natural dos fragmentos.</p></div>
</div>
<div class="box"><p style="margin:0"><b>Condições de atividade:</b> a enzima tem atividade ótima em <b>pH 5,0–7,0</b> e à <b>temperatura corporal (37&nbsp;°C)</b>, e é <b>específica</b> para a ligação β(1→4) entre GlcA e GlcNAc. <b>Honestidade de fonte:</b> este capítulo é química de literatura — o estudo reológico deste livro <b>não mediu degradação enzimática</b> de nenhum produto. Nenhum número de resistência à hialuronidase é atribuído aqui a nenhum gel.</p></div>
</section>

<section class="folha" id="viscoelast">
{cap_head('Capítulo 3','Por que o gel é viscoelástico',
 'Um preenchedor não é sólido nem líquido: é os dois ao mesmo tempo. Entender isso é entender por que existem G′, G″ e tan δ — e por que a frequência muda o resultado.')}
<div class="eqs">
<div class="eq"><span class="t">Material elástico</span><span class="f">F = k · x</span><p>A <b>mola</b>. Deforma sob força e <b>retorna inteiramente</b> à forma original quando a força cessa. A deformação é proporcional à força (Lei de Hooke).</p></div>
<div class="eq"><span class="t">Material viscoso</span><span class="f">τ = η · γ̇</span><p>O <b>mel</b>. <b>Escoa</b> sob tensão e não retorna. A tensão de cisalhamento é proporcional à taxa de deformação; η é a viscosidade.</p></div>
<div class="eq"><span class="t">Hidrogel</span><span class="f">G* = G′ + iG″</span><p>O <b>gel de ácido hialurônico</b>. Deforma, escoa lentamente até um platô e <b>recupera parte</b> da deformação — nunca toda.</p></div>
</div>
{figura('4', ILU2['conc_viscoel'], 'Viscoelasticidade da base ao gel: elasticidade (mola, Lei de Hooke), viscosidade (mel, τ = η·γ̇), a distinção entre fluido e sólido elástico sob tensão constante, o hidrogel como caso intermediário e os três modelos reológicos clássicos — Maxwell, Kelvin-Voigt e Burgers — aplicados aos preenchedores.', 'capítulo de viscoelasticidade: elasticidade, viscosidade e modelos reológicos', cls='sci')}
<h3>Os três modelos clássicos</h3>
<div class="mods">
<div class="mod"><b>Maxwell</b><p>Mola e amortecedor <b>em série</b>. Responde instantaneamente e depois escoa sem limite. Descreve bem a <b>relaxação</b> de tensão.</p></div>
<div class="mod"><b>Kelvin-Voigt</b><p>Mola e amortecedor <b>em paralelo</b>. Deforma progressivamente até um platô e recupera. Descreve bem a <b>fluência</b> (creep).</p></div>
<div class="mod"><b>Burgers</b><p>Combinação dos dois. É o que mais se aproxima do comportamento real de um hidrogel de HA: deformação instantânea, fluência e recuperação parcial.</p></div>
</div>
<div class="box"><p style="margin-top:0"><b>É daqui que saem os quatro números do capítulo seguinte.</b> Num ensaio oscilatório, a resposta do gel se decompõe em duas partes: a que está <b>em fase</b> com a deformação — a energia armazenada e devolvida, <b>G′</b> — e a que está <b>defasada em 90°</b> — a energia dissipada como escoamento, <b>G″</b>. A razão entre elas, <b>tan δ = G″/G′</b>, diz qual dos dois comportamentos domina.</p>
<p style="margin-bottom:0">E como o gel é viscoelástico, <b>a resposta depende da velocidade da solicitação</b>. Não existe “o G′ do produto”: existe o G′ àquela frequência. Por isso todo este livro é lido a <b>0,7 Hz</b> — a frequência da mímica habitual — e por isso o mesmo Belotero Balance aparece com G′ 78 Pa e tan δ 0,90 a 10 Hz, 34 Pa e 0,69 a 0,7 Hz, e vira praticamente líquido a 0,01 Hz.</p></div>
</section>

<section class="folha" id="fundamentos">
{cap_head('Capítulo 4','Os quatro números em 60 segundos')}
<div class="fund">
<div class="box"><b class="t">G′ — módulo elástico</b><p>A “mola”: energia devolvida. Sustentação, projeção, manutenção de forma. No banco: 33,6 a 935,9 Pa.</p></div>
<div class="box"><b class="t">G″ — módulo viscoso</b><p>O “amortecedor”: energia dissipada. Acomodação ao movimento. Ler sempre em relação ao G′.</p></div>
<div class="box"><b class="t">tan δ = G″/G′</b><p>O balanço. &lt;1 = gel; &gt;1 = líquido. Banco: 0,07 (Volux) a 0,69 (Balance). É uma relação, não uma força.</p></div>
<div class="box"><b class="t">η* — viscosidade complexa</b><p>Resistência global ao fluxo; explode em repouso (0,01 Hz: 164 → 11.451 Pa·s). Proxy de permanência.</p></div>
</div>
<h3>Frequência é movimento facial</h3>
<div class="box" style="padding:.4rem 1rem">
<table class="freq"><thead><tr><th>Frequência</th><th>Equivalente clínico</th><th>Exemplo do banco (G′ / tan δ)</th></tr></thead><tbody>
<tr><td>10–5 Hz</td><td>gestos rápidos (fala, mastigação vigorosa)</td><td>Balance 78/0,90 — parece um filler comum</td></tr>
<tr><td><b>0,7 Hz</b></td><td><b>mímica habitual — referência do guia</b></td><td>Balance 34/0,69 · Volux 669/0,07</td></tr>
<tr><td>0,01 Hz</td><td>repouso (carga estática)</td><td>Skinvive tan δ <b>1,54</b> → líquido em repouso: espalha e hidrata, não sustenta</td></tr>
</tbody></table></div>
{box_pratica('Aulas de reologia do autor (FEP)',
 'Acesse as aulas do Dr. João Pithon sobre reologia aplicada ao preenchimento — fundamentos, leitura dos parâmetros e escolha do produto na prática clínica. Escaneie o QR Code com a câmera do celular para abrir a pasta de aulas.',
 QR['aulas'], 'https://drive.google.com/drive/folders/1ztwjgguHK3VdDHG-j2E5CL4ViGglwpv-',
 ilus=ILU['g3b'], ilus_cap='Leitura de grupo na aula: os valores a 0,7 Hz na linguagem de cores.')}
<h3>O que um número NÃO diz (anti-inferências)</h3>
<div class="box"><ul class="anti">
<li>G′ ≠ coesividade · G′ ≠ volumização · G′ ≠ lifting</li>
<li>G′ não define plano de injeção</li>
<li><b>G′ não é segurança vascular</b></li>
<li>tan δ ≠ fluidez; G″ alto ≠ gel dinâmico (Hyafilia V: G″ 123 e é estrutural)</li>
<li>Concentração ≠ reologia (Hyafilia 20 mg/mL: 284 → 526 → 841 Pa)</li>
<li>Partícula ≠ G′ (Sofiderm Derm Plus: 2ª maior partícula, MENOR G′ da linha)</li>
<li>Tecnologia/reticulante ≠ faixa de G′ (DVS ≠ alto G′; NASHA ≠ alto G′)</li>
<li>Nome comercial ≠ reologia (“SOFT NÃO É AZUL” — Hyafilia Soft 284 Pa)</li>
<li>Swelling do gel ≠ edema clínico; baixo G′ ≠ baixo SF</li>
<li>Mesmo G′ ≠ mesmo gel (Refyne × Rennova Fine Lines: 81,6 Pa ambos; tan δ 0,29 × 0,53)</li>
</ul></div>
<p class="qt">Sequência decisória: <b>ANATOMIA → DEFEITO → OBJETIVO → PLANO → PRODUTO → VOLUME → TÉCNICA</b>. O produto é a 5ª decisão — e “RESULTADO = PRODUTO × VOLUME × PLANO × TÉCNICA × TECIDO”.</p>
</section>

<section class="folha" id="mapasec">
{cap_head('Capítulo 5','O Mapa da Reologia — três famílias sobre a face',
 'Três cores organizam o livro inteiro: azul integra, amarelo preenche, roxo sustenta. As subclasses refinam — não criam famílias novas.')}
<p class="lead">Cada ponto é um ensaio (0,7&nbsp;Hz). As faixas coloridas são as três famílias da 1ª cor (cortes 200 e 300&nbsp;Pa); a altura é o caráter dinâmico (tan δ). Passe o mouse/toque para identificar.</p>
{scatter_main()}
{LEG3}
<p class="lead" style="font-size:.9rem">Achados: apenas <b>2 dos 76 ensaios</b> são “roxo completo” (grupo 4); os pares sobrepostos (Volift=Voluma, Belotero Volume+=Neauvia Intense, Stimulate=Singderm) estão em re-verificação; famílias comerciais inteiras vivem numa mesma zona — a cor classifica, o número posiciona.</p>
<h3 style="margin-top:1.6rem">Mapa anatômico — as três famílias sobre a face</h3>
<p class="lead">Este é o mapa central do livro. <b>Três famílias</b>, definidas pelo G′ e reconhecidas pela cor: <b style="color:var(--fam-a)">azul</b> quando o gel integra, <b style="color:var(--fam-m)">amarelo</b> quando preenche, <b style="color:var(--fam-r)">roxo</b> quando sustenta. Tudo o mais no livro — as nove assinaturas, os seis grupos, as fichas — é detalhamento destas três.</p>
{mapa_familias()}
<p class="lead" style="font-size:.92rem"><b>Como ler cada face:</b> o preenchimento traz a cor da família (a 1ª cor, o G′) e o contorno traz a segunda cor da assinatura. As regiões se repetem entre famílias de propósito — <b>a mesma mandíbula</b> aparece no amarelo (valorizar o contorno), no roxo puro (projetar o ângulo) e no roxo modulado (volumizar). O que muda não é a região: é a tarefa.</p>

<div class="box"><p style="margin-top:0"><b>A subclasse do baixo G′ — duas assinaturas, uma indicação.</b> Dentro do azul existem dois perfis: <b>azul + rosa</b> {dotchip('a',11)}{dotchip('p',11)} e <b>azul + amarelo + rosa</b> {dotchip('a',11)}{dotchip('m',11)}{dotchip('p',11)}. A diferença entre eles é <i>quanto valorizam</i> — o segundo entrega um pouco mais de volume, porque tem G″ intermediário. <b>As regiões são as mesmas.</b> Não existe uma indicação para um e outra para o outro: onde vai o azul + rosa, vai também o azul + amarelo + rosa, e a escolha entre os dois é de quanto corpo se quer naquele mesmo lugar.</p>
<p style="margin-bottom:0"><b>O moderado se mantém.</b> A família amarela tem uma assinatura só e não se subdivide: é o produto de transição, o que preenche o vale sem espalhar nem projetar.</p></div>

{filete('cadeia', 160)}
<h4 style="margin-bottom:.2rem">Os três usos do alto G′</h4>
<p class="lead">A família roxa é a única com três destinos clínicos distintos — e é por isso que ela concentra mais produtos que qualquer outra no banco.</p>
{usos_roxo()}
<div class="box"><p style="margin:0"><b>O terceiro uso merece atenção.</b> A região infraorbitária não tolera inchaço: ali um gel que capte muita água produz edema visível e resultado imprevisível. A resposta não é usar um gel fraco — é usar um gel de <b>alto G′ com baixo swelling factor</b>, tipicamente de baixa concentração de ácido hialurônico e partículas grandes. É a família roxa entrando numa região que, à primeira vista, pediria a azul. <b>💧 O swelling factor não foi medido neste estudo</b>: os produtos deste uso são identificados por declaração de fabricante e pela experiência clínica do autor, nunca por dedução a partir do G′.</p></div>
<p class="qt">A regra que atravessa o mapa: <b>o gel é escolhido para a tarefa, não para a região</b>. Um sulco nasolabial raso e um sulco nasolabial muito profundo estão em famílias diferentes — azul e roxa — apesar de terem o mesmo nome anatômico.</p>
</section>

<section class="folha" id="forma">
{cap_head('Capítulo 6','A forma do gel — os quatro conceitos que a desenham',
 'O radar não é enfeite: é a única figura do livro em que as quatro medidas aparecem juntas, na mesma escala e nas cores da gramática oficial.')}
<h3>6.1 &nbsp;Os quatro conceitos medidos</h3>
<p class="lead">Tudo o que este estudo mediu cabe em quatro números, um por eixo. Cada um tem sua posição fixa na figura e seus próprios cortes de cor — os mesmos cortes usados em todas as fichas do livro.</p>
{eixos_cards()}
<div class="box"><p style="margin:0"><b>Por que percentil e não valor absoluto.</b> Os quatro parâmetros vivem em escalas incomparáveis: o G′ vai a centenas de Pa, o tan δ não passa de 0,7. Se a figura usasse valor absoluto, o G′ esmagaria os outros três eixos e toda forma seria a mesma seta. Cada eixo do radar é então a <b>posição do produto dentro do banco</b> (percentil entre os 76 ensaios a 0,7 Hz). A forma compara géis entre si — não substitui os números, que estão sempre impressos ao lado.</p></div>

{filete('cadeia', 160)}
<h3>6.2 &nbsp;A forma geométrica e as cores da assinatura</h3>
<p class="lead">Ligando os quatro percentis nasce um quadrilátero — a impressão digital reológica do gel. E a figura é colorida pela mesma gramática do resto do livro: o <b>preenchimento traz a 1ª cor</b> (a família de G′), o <b>contorno traz a 2ª cor</b> (o comportamento em tan δ) e <b>cada vértice recebe a cor da sua própria métrica</b>. Um produto cujos quatro vértices são da mesma cor é um gel “completo” naquela família.</p>
{familias_forma()}
<p class="lead" style="font-size:.92rem"><b>As quatro famílias em uma linha:</b> <span style="color:var(--fam-a)"><b>baixo G′</b></span> é azul com rosa · <span style="color:var(--fam-a)"><b>baixo G′ volumizador</b></span> é azul, amarelo e rosa · <span style="color:var(--fam-m)"><b>médio G′</b></span> é amarelo · <span style="color:var(--fam-r)"><b>alto G′</b></span> é roxo — puro no grupo 4, e com uma segunda cor associada no grupo 5.</p>
<div class="box"><p style="margin-top:0"><b>Como ler a silhueta:</b></p>
<ul class="anti" style="margin-bottom:0">
<li><b>Pipa para baixo</b> — o tan δ domina: gel dissipativo, espalha e acompanha o movimento.</li>
<li><b>Seta para cima e para a esquerda</b> — G′ e η* altos com tan δ baixo: estrutura e permanência.</li>
<li><b>Abertura para a direita</b> — G″ proporcionalmente alto: o gel tem corpo, trabalha a superfície.</li>
<li><b>Losango cheio</b> — alto em tudo: magnitude com equilíbrio viscoelástico, estrutura que ainda se molda.</li>
<li><b>Forma pequena e centrada</b> — gel leve em todas as dimensões.</li>
</ul></div>
<p class="qt">A forma diz <i>como</i> o gel se comporta; ela não diz onde aplicar, quanto volume usar nem em que plano. Duas formas parecidas podem ter magnitudes muito diferentes — por isso o percentil vem sempre acompanhado do número medido.</p>
</section>

<section class="folha" id="textura">
{cap_head('Capítulo 7','Textura visual do gel — o que os olhos antecipam')}
<p class="lead">Antes do reômetro, o gel já conta parte da história ao ser extrudado: existe um padrão visual nos tipos de géis. Uns escorrem <b>em gota</b>; outros vertem densos, <b>como mel</b>; outros saem <b>rígidos</b>, em cordão que se quebra — o aspecto <b>fraturado</b>. Além do escoamento, observa-se a aparência: gel <b>translúcido</b> e contínuo ou opalescente e particulado.</p>
<div class="gelrow">
<div class="gelcard">{GEL['gota']}<h4>Em gota — fluido</h4><p class="gelsub">TÍPICO DOS GRUPOS 1–2</p><p>Escorre e se espalha; vence a própria forma. Antecipa integração alta e baixo relevo.</p></div>
<div class="gelcard">{GEL['mel']}<h4>Como mel — viscoso denso</h4><p class="gelsub">TÍPICO DO GRUPO 3</p><p>Verte em fita contínua e lenta; segura a forma por instantes. Antecipa corpo e equilíbrio.</p></div>
<div class="gelcard">{GEL['rigido']}<h4>Rígido / fraturado — estrutural</h4><p class="gelsub">TÍPICO DOS GRUPOS 4–5</p><p>Sai em cordão firme que mantém geometria — e, nos mais coesos, fratura em blocos em vez de escorrer.</p></div>
</div>
<p class="lead" style="font-size:.92rem"><b>Regra de honestidade:</b> a textura visual <i>sugere</i>; o reômetro <i>confirma</i>. Aparência translúcida ou particulada não prevê G′ (“nome, cor e aspecto não são reologia”) — por isso cada impressão visual deste capítulo remete à ficha numérica do produto.</p>
{box_pratica('Vídeos e imagens de textura — galeria oficial',
 'Assista aos vídeos ilustrativos de extrusão e textura dos géis (em gota, como mel, rígido/fraturado) e veja as imagens comparativas da galeria do Reology Map. O acervo é atualizado continuamente pelo autor — os vídeos de cada grupo entram nesta mesma pasta.',
 QR['galeria'], 'https://drive.google.com/drive/folders/1xcyZVRcnvkHyYFCXOlZf9pWmq-CVwlm1',
 ilus=ILU['g1b'], ilus_cap='Da textura ao número: o grupo mais fluido do banco e seus valores medidos.')}
</section>

<section class="folha" id="atlas">
{cap_head('Capítulo 8 (gráficos) · Capítulos 9–14 (grupos)','Atlas de gráficos — todas as variáveis')}
<h3>G″ × G′ — a dissipação em magnitude (tan δ vira inclinação)</h3>
<p class="lead">Nas escalas log, as retas tracejadas são valores constantes de tan δ: produtos sobre a mesma reta têm a mesma <i>proporção</i> dissipativa, ainda que magnitudes muito diferentes.</p>
{scatter_gg()}
{LEG3}
<h3>Permanência em repouso — η* a 0,01 Hz × G′ a 0,7 Hz</h3>
<p class="lead">O quanto o gel resiste a fluir quando a face está parada. A tendência acompanha o G′ — e os desvios contam histórias: Skinvive despenca (vira líquido em repouso); os NASHA de G″ alto ficam acima da vizinhança.</p>
{scatter_eta()}
{LEG3}
</section>

{''.join(fam_secs)}
{sf_sec}

<section class="folha" id="rankings">
{cap_head('Capítulo 15','Rankings completos — os 76 ensaios lado a lado')}
<h3>G′ a 0,7 Hz (Pa) — a espinha estrutural do banco</h3>
{ranking('g1','G′ a 0,7 Hz (Pa)',960,br0,(0,200,300,500,750))}
<h3>tan δ a 0,7 Hz — o eixo do movimento</h3>
{ranking('td','tan δ a 0,7 Hz',0.72,lambda v: br(v,2),(0,0.15,0.30,0.50,0.70))}

{filete('cadeia', 160)}
<h3>Rankings temáticos — recalculados sobre os 76 ensaios</h3>
<p class="lead">Os quatro recortes que mais se pedem na prática, gerados <b>direto do banco canônico</b> e não de tabelas transcritas. Vale registrar o motivo: versões anteriores destes rankings circularam construídas sobre um subconjunto de 42 produtos, e a composição muda quando se olha o banco inteiro — o menor G′ do estudo não é o Up Fine e sim o <b>Belotero Balance</b>, e o segundo maior não é o Lyft e sim o <b>Hyafilia V Plus</b>. Os números eram certos; a lista estava incompleta.</p>
<div class="podios">
{podio(top('g1', 10, True), 'g1', 'Os 10 maiores G′', 'Maior capacidade de manter forma sob carga. Não confundir com volumização, lifting ou segurança vascular.')}
{podio(top('g1', 10, False), 'g1', 'Os 10 menores G′', 'Maior integração e menor relevo próprio. Baixo G′ <b>não</b> implica baixo swelling factor — são propriedades independentes, e o SF não foi medido (💧).')}
{podio(top('td', 10, True), 'td', 'Os 10 maiores tan δ', 'Componente viscosa relativa dominante: o gel acompanha o movimento e se distribui. tan δ é uma <b>razão</b>, não uma força — um tan δ alto num gel de G′ baixo não é o mesmo gel de um tan δ alto num G′ alto.')}
{podio(top('td', 10, True, filtro=lambda r: r['G1_0.7Hz'] and r['G1_0.7Hz'] >= 300), 'td', 'Alto G′ (≥ 300 Pa) com maior tan δ', 'O recorte mais útil e o mais mal transcrito: estrutura <b>com</b> componente dinâmica preservada — sustenta sem endurecer o movimento.')}
</div>
<div class="box"><p style="margin:0"><b>Filtro clássico, refeito:</b> o critério “G′ ≥ 200 Pa <b>e</b> tan δ ≥ 0,21” devolve <b>10 ensaios</b> no banco completo, não 7: além de Neauvia Stimulate, Singderm, Restylane Lido, Belotero Volume +, Neauvia Intense, e.p.t.q S 300 e Up Max, entram <b>Restylane Lido (lote 27003)</b>, <b>Restylane Skinbooster</b> e <b>Hyafilia S Plus</b>.</p></div>
</section>

<section class="folha" id="fontes">
{cap_head('Capítulo 16','Quando as fontes discordam',
 'O mesmo produto, medido por dois laboratórios, devolve dois números — e os dois podem estar certos. Este capítulo mostra o tamanho real dessa diferença e a regra que impede que ela contamine o livro.')}
<h3>15.1 &nbsp;As quatro camadas de evidência</h3>
<p class="lead">Todo dado deste guia carrega, explicitamente, de onde veio. Não é formalidade: é o que separa uma medida de uma impressão.</p>
<div class="camadas">
<div class="camada"><b>1 · Medido</b><p>Laudo do estudo, com lote identificado, a 0,7 Hz. É a única camada que gera cor, grupo, assinatura e ranking neste livro.</p></div>
<div class="camada c2"><b>2 · Fabricante *</b><p>Valor declarado em monografia, bula ou material técnico. Sempre marcado com asterisco e nunca comparado lado a lado com a camada 1.</p></div>
<div class="camada c3"><b>3 · Literatura</b><p>Dado publicado por terceiros, citado como tal. Útil para contexto histórico e para entender divergências — não para classificar.</p></div>
<div class="camada c4"><b>4 · Interpretação</b><p>A leitura clínica do autor sobre o número medido. É opinião fundamentada, declarada como opinião.</p></div>
</div>
<p><b>E a quinta possibilidade, que não é camada nenhuma:</b> o dado ausente. Swelling factor, coesividade quantitativa, força de extrusão e Strain X <b>não foram medidos</b> nesta rodada e aparecem marcados com 💧. Dado ausente é informação — nunca se deduz um deles a partir de outro.</p>

{filete('cadeia', 160)}
<h3>15.2 &nbsp;O tamanho real da divergência</h3>
<p class="lead">Nove produtos deste banco também têm valores publicados por outras fontes. Abaixo, os dois números lado a lado. A coluna da esquerda é o que este estudo mediu; a da direita, o que a outra fonte relata.</p>
<div class="fontes"><table>
<thead><tr><th>Produto</th><th>Este estudo · 0,7 Hz</th><th>Outra fonte</th><th>Camada e origem</th></tr></thead>
<tbody>{_ROWS_FONTES}</tbody></table></div>
<div class="box"><p style="margin-top:0"><b>Por que os números diferem — e por que isso não é erro de ninguém:</b></p>
<ul class="anti" style="margin-bottom:.4rem">
<li><b>Reômetro e geometria diferentes.</b> Este estudo: TA Instruments AR-1500ex, placas Ø 20 mm, gap 500 µm. A fonte do fabricante da linha e.p.t.q: Anton Paar MCR302, placa-placa 25 mm, gap 1.000 µm.</li>
<li><b>Frequência diferente.</b> O dado do fabricante é reportado a 0,1 Hz; este livro lê a 0,7 Hz. Num material viscoelástico, mudar a frequência muda o número por definição — não por imprecisão.</li>
<li><b>Desenho de estudo diferente.</b> O comparativo da linha Yvoire mede também tamanho de partícula (693 ± 344 a 1.258 ± 742) e força de injeção (9,8 a 19 N): é outro experimento, com outro objetivo.</li>
<li><b>Lote e geração de produto diferentes.</b> Comparar um lote de hoje com um dado de anos atrás compara também duas formulações.</li>
</ul>
<p style="margin-bottom:0"><b>A prova de que é protocolo e não desvio sistemático:</b> a divergência não tem direção única. Para a linha e.p.t.q, a outra fonte é <b>menor</b> em G′. Para a linha Belotero, é <b>maior</b>. Para a linha Yvoire, é menor em G′ e <b>muito maior</b> em tan δ. Se houvesse um erro de calibração de um lado, o desvio andaria sempre para o mesmo lado.</p></div>
<p class="qt">A regra operacional deste livro: <b>comparabilidade é interna ao protocolo</b>. Números de fontes diferentes nunca entram na mesma tabela, no mesmo gráfico ou no mesmo ranking — nem quando isso deixaria a lista mais completa.</p>

{filete('cadeia', 160)}
<h3>15.3 &nbsp;Nome comercial não é reologia: o caso Perfectha</h3>
<p class="lead">A linha Perfectha é apresentada como uma escada crescente de suporte: <b>Finelines → Derm → Deep → Subskin</b>, do refinamento superficial à sustentação estrutural. É uma narrativa clara, coerente e — na medida de G′ — invertida.</p>
<div class="podios"><div class="podio"><h4>O que a escada comercial promete × o que o reômetro mediu</h4>
<table><thead><tr><th></th><th>Produto</th><th>G′ medido (Pa)</th><th>Posição na escada</th></tr></thead><tbody>
<tr><td class="pd-n">1</td><td class="pd-p">Perfectha Derm</td><td class="pd-v">440,68</td><td class="pd-x">2º de 4 · <b>maior G′</b></td></tr>
<tr><td class="pd-n">2</td><td class="pd-p">Perfectha Deep</td><td class="pd-v">386,46</td><td class="pd-x">3º de 4</td></tr>
<tr><td class="pd-n">3</td><td class="pd-p">Perfectha Subskin</td><td class="pd-v">343,00</td><td class="pd-x">4º de 4 · <b>menor G′</b></td></tr>
</tbody></table>
<p class="pd-nota">O produto vendido como o mais estrutural da linha é o que tem <b>menor</b> módulo elástico dos três medidos. Isso não desqualifica o Subskin: ele pode ser o mais indicado para volumização profunda por coesividade, comportamento de bolus ou tolerância a grandes volumes — propriedades que este estudo <b>não mediu</b>. O que a medida desautoriza é a inferência de que “mais profundo no nome” significa “maior G′”.</p></div></div>
<p>É o mesmo fenômeno já registrado no capítulo 4 com o Hyafilia Soft (284 Pa — “soft não é azul”) e com a linha Hyafilia inteira a 20 mg/mL variando de 284 a 841 Pa. <b>O nome descreve a intenção comercial; o número descreve o gel.</b></p>

{filete('cadeia', 160)}
<h3>15.4 &nbsp;Reconciliação de nomes</h3>
<p class="lead">Materiais anteriores usam denominações que não batem com as do banco. Nenhuma delas é erro — são gerações, mercados e traduções diferentes. Registrar a correspondência evita que o mesmo gel seja contado duas vezes.</p>
<div class="fontes"><table>
<thead><tr><th>Nome em outros materiais</th><th>Nome canônico neste livro</th><th>Observação</th></tr></thead><tbody>
<tr><td>Yvoire Classic / Volume / Contour</td><td><b>Yvoire Classic+ · Volume+ · Contour+</b></td><td>A geração “+” é a medida neste estudo; os valores da geração anterior circulam na literatura.</td></tr>
<tr><td>Juvéderm Volite</td><td><b>Juvéderm Skinvive</b></td><td>Mesma proposta de skin quality, denominação distinta por mercado.</td></tr>
<tr><td>Milimetric Fino / Moderado / Profundo</td><td><b>Milimetric PRO Leve · Moderado · Intenso</b></td><td>Correspondência por posição na linha.</td></tr>
<tr><td>EVO Fine / Deep / Contour</td><td><b>Evofill Derm · Evofill Ultra Deep</b></td><td>Apenas dois ensaios desta marca entraram no banco; a linha comercial é maior.</td></tr>
<tr><td>Finafill</td><td><b>Finahfil Intense</b></td><td>Grafia divergente do mesmo produto.</td></tr>
<tr><td>Belotero Soft · Perlane · Rennova Ultradeep</td><td><b>—</b></td><td>Citados em materiais anteriores, <b>não presentes</b> neste banco: nenhum valor lhes é atribuído aqui.</td></tr>
</tbody></table></div>

{filete('cadeia', 160)}
<h3>15.5 &nbsp;Errata desta edição</h3>
<p class="lead">Esta edição corrige três valores que circularam em materiais anteriores do próprio autor. Em todos os casos o banco de laudo está certo e a transcrição estava errada — e em todos os três a própria tabela de origem contém a prova da correção.</p>
<div class="errata">
<h4>Três correções, com a demonstração de cada uma</h4>
<ul>
<li><b>e.p.t.q S 500 — tan δ:</b> <span class="de">0,23</span> → <span class="para">0,19</span>.<br>
Recálculo direto: <code>G″/G′ = 67,30 / 355,13 = 0,1895</code>. O valor 0,23 é o tan δ do <b>S 300</b>, repetido uma linha abaixo.</li>
<li><b>Perfectha Subskin — tan δ:</b> <span class="de">0,20</span> → <span class="para">0,15</span>.<br>
Recálculo direto: <code>52,00 / 343,00 = 0,1516</code>. Esta correção já vinha sinalizada com ⚑ nas fichas e agora está consolidada.</li>
<li><b>Saypha Filler — G″:</b> <span class="de">39,36 Pa</span> → <span class="para">33,52 Pa</span>.<br>
O valor 39,36 é o G″ do <b>Revanesse Ultra +</b>, linha vizinha na tabela de origem. A prova está na própria tabela: ela imprime tan δ 0,24 para o Saypha Filler, e <code>33,52 / 142,61 = 0,235</code> fecha em 0,24 — <code>39,36 / 142,61 = 0,276</code> não fecha.</li>
</ul>
</div>
<div class="box"><p style="margin-top:0"><b>Correção de escopo, não de valor — os rankings.</b> As listas de maiores e menores G′ publicadas anteriormente traziam <b>valores corretos sobre um universo incompleto</b>: foram construídas quando o banco tinha 42 produtos. Sobre os 76 ensaios atuais, a composição muda — entram Belotero Balance (o menor G′ do estudo), Milimetric PRO Leve, Rennova Fill Fine Lines, Restylane Refyne e Juvéderm Skinvive entre os menores; e Hyafilia V Plus, Restylane Lido lote 27003, Juvéderm Volux, Restylane Skinbooster e Hyafilia M Plus entre os maiores. O mesmo vale para o filtro “G′ ≥ 200 e tan δ ≥ 0,21”, que passa de 7 para 10 ensaios.</p>
<p style="margin-bottom:0"><b>Como conferir qualquer número deste livro:</b> todos os valores são gerados diretamente de <code>data/reologia_produtos_full.json</code> — o banco canônico versionado — e não de tabelas redigitadas. Nenhum número deste guia foi transcrito à mão de uma imagem.</p></div>
</section>

<section class="folha" id="regioes">
{cap_head('Capítulo 17','Guia rápido por região')}
<p class="lead">Síntese do mapeamento região → necessidade reológica → produtos citados nas monografias. Uma região pode pertencer a mais de um grupo conforme o objetivo (corpo do mento ≠ vértice do mento).</p>
<div class="regtab"><table><thead><tr><th>Região</th><th>Necessidade</th><th>Produtos (1ª escolha / fortes)</th><th>Observação</th></tr></thead><tbody>{reg_rows}</tbody></table></div>
</section>

<section class="folha" id="indice">
{cap_head('Apêndice A','Índice por marca')}
<div class="ix">{idx}</div>
</section>

<section class="folha" id="notas">
{cap_head('Apêndice B','Fontes, limitações e aviso')}
<div class="box">
<p style="margin-top:0"><b>Fonte dos números:</b> Estudo Reológico Pithon Napoli — laudo laboratorial independente, assinado, de 04/08/2026 (Anexo 2, 0,7 Hz), com lote identificado em cada ficha; 76 ensaios e 75 produtos canônicos (Restylane Lido em dois lotes, modelado como um produto com dois ensaios). Reômetro rotacional TA Instruments AR-1500ex, 25 °C, placas paralelas Ø 20 mm, gap 500 µm, varredura 10 → 0,01 Hz. Comparabilidade é <b>interna ao protocolo</b>; 25 °C in vitro ≠ comportamento in vivo. O radar usa <b>percentil do banco</b>, não valor absoluto. As cores seguem a gramática oficial do Mapa, com zonas de transição e curadoria versionada.</p>
<p><b>Não medidos nesta rodada</b> (prioridade da 2ª rodada): coesividade quantitativa, Swelling Factor, força de extrusão, Strain X/amplitude, compressão. Onde citados, são dados declarados pelo fabricante (*) ou impressão clínica do autor — dado ausente é informação, nunca inferência.</p>
<p><b>Auditoria desta edição:</b> os infográficos e tabelas anteriores do autor foram conferidos valor por valor contra o banco canônico antes de qualquer conteúdo novo entrar no livro. A tabela-mestra a 0,7 Hz conferiu em 39 dos 42 produtos; as três divergências, sua demonstração e a correção de escopo dos rankings estão no <b>capítulo 16</b>. Rankings construídos sobre universo incompleto foram refeitos a partir dos 76 ensaios. <b>Fichas com ⚑</b> aguardam errata/re-verificação laboratorial (pares idênticos, η* divergentes, tan δ do Perfectha Subskin corrigido por recálculo). <b>Fichas com ◌</b> aguardam a monografia do autor.</p>
<p style="margin-bottom:0"><b>Aviso:</b> material educacional para profissionais habilitados; não substitui julgamento clínico, bula/IFU nem treinamento anatômico. Indicações refletem a experiência e a leitura reológica do autor sobre lotes específicos; os fabricantes não participaram nem endossam o estudo. Marcas citadas pertencem aos respectivos titulares.</p>
</div>
{box_qr('Continue com o autor — aulas e atualizações',
 'As aulas de reologia da FEP e os materiais complementares do Reology Map ficam na pasta oficial do autor. Escaneie para acessar; o conteúdo é atualizado continuamente.',
 QR['aulas'], 'https://drive.google.com/drive/folders/1ztwjgguHK3VdDHG-j2E5CL4ViGglwpv-',
 kind='saibamais', ilus=ILU['g5b'], ilus_cap='Material complementar: grupos, valores e leitura clínica.')}
<p class="rodape">Reologia do Ácido Hialurônico — Guia Reology Map · Dr. João Pithon · 1ª edição (ago/2026). Gerado do banco canônico <code>data/reologia_produtos_full.json</code>. Para exportar PDF: imprimir pelo navegador (layout otimizado).</p>
</section>
</main>
<div id="tip" role="status"></div>
<script>
(function(){{
 var tip=document.getElementById('tip');
 document.querySelectorAll('.dot').forEach(function(d){{
  d.addEventListener('pointerenter',function(){{tip.textContent=d.dataset.n+' — '+d.dataset.v;tip.style.opacity=1;}});
  d.addEventListener('pointermove',function(e){{var x=Math.min(e.clientX+14,window.innerWidth-tip.offsetWidth-8);tip.style.left=x+'px';tip.style.top=(e.clientY+16)+'px';}});
  d.addEventListener('pointerleave',function(){{tip.style.opacity=0;}});
 }});
}})();
</script>
'''
out=f'{BASE}/ebook-reologia-map.html'
open(out,'w',encoding='utf-8').write(page)
counts={g:sum(1 for p in ed.PRODUTOS if grp(p)==g) for g in ['G1','G2','G3','G4','G5']}
print('OK',len(page)//1024,'KB · grupos:',counts)
assert counts=={'G1':28,'G2':6,'G3':14,'G4':2,'G5':26}, counts
