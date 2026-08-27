# -*- coding: utf-8 -*-
"""eBook Reology Map v3 — 6 grupos oficiais, assinatura de cores por métrica,
ilustrações face+gel, textura visual com QR (NA PRÁTICA / SAIBA MAIS)."""
import json, math, html, re, unicodedata, importlib.util

BASE = '/tmp/claude-0/-home-user-reologia-map/cd216e96-b088-57d1-abe3-2409c365400d/scratchpad'
spec = importlib.util.spec_from_file_location('ebook_data', f'{BASE}/ebook_data.py')
ed = importlib.util.module_from_spec(spec); spec.loader.exec_module(ed)
DATA = {r['produto']: r for r in json.load(open(f'{BASE}/produtos_full.json'))}
QR = json.load(open(f'{BASE}/qrs.json'))
assert len(ed.PRODUTOS) == 76

def td_of(k): return 0.15 if k == 'Perfectha Subskin' else DATA[k]['tand_0.7Hz']
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

# ---------------- radar ----------------
def radar(k, fam, size=96, cls='radar'):
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
    return (f'<svg class="{cls}" viewBox="0 0 {size} {size}" role="img" aria-label="forma reológica"><title>{html.escape(tip)}</title>'
            f'{grid}{axes}<polygon points="{poly}" fill="var(--fam-{fam})" fill-opacity=".22" stroke="var(--fam-{fam})" stroke-width="2" stroke-linejoin="round"/>'
            + ''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.4" fill="var(--fam-{fam})"/>' for x,y in pts) + lbl + '</svg>')

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
FACE_PATH = ('M96,34 C142,16 190,34 202,86 C208,112 202,126 195,138 C191,145 191,150 197,155 '
             'C209,167 219,183 219,196 C219,204 212,208 205,208 C200,213 201,219 208,222 '
             'C215,227 215,235 206,239 C214,245 214,254 204,259 C197,263 195,269 199,275 '
             'C209,283 211,299 200,312 C186,330 158,340 130,340 C107,340 90,330 82,312')
def face_svg(width=250, marks=None, cls='facesvg', aria='perfil facial', vw=300, dx=0, leader=False):
    m=''
    if marks:
        for mk in marks:
            if leader:
                x,y,c,label,side = mk; x+=dx
                lx = (vw-6) if side=='R' else 6
                tx = lx - 4 if side=='R' else lx + 4
                ex = x+10 if side=='R' else x-10
                m += (f'<line x1="{ex}" y1="{y}" x2="{lx - (52 if side=="R" else -52)*0 - (0)}" y2="{y}" class="fc-ld" style="display:none"/>')
                lend = lx - (4 if side=='R' else -4)
                m += (f'<line x1="{ex}" y1="{y}" x2="{lx}" y2="{y}" class="fc-ld"/>'
                      f'<circle cx="{x}" cy="{y}" r="6.5" fill="{CHIP[c]}" class="fc-dot"/>'
                      f'<text x="{tx}" y="{y-4}" class="fc-lb" text-anchor="{"end" if side=="R" else "start"}">{html.escape(label)}</text>')
            else:
                x,y,c,label,anch = mk; x+=dx
                lx = x + (12 if anch=='start' else -12)
                if label:
                    m += (f'<line x1="{x}" y1="{y}" x2="{lx}" y2="{y}" class="fc-ld"/>'
                          f'<text x="{lx + (4 if anch=="start" else -4)}" y="{y+3.5}" class="fc-lb" text-anchor="{anch}">{html.escape(label)}</text>')
                m += f'<circle cx="{x}" cy="{y}" r="6.5" fill="{CHIP[c]}" class="fc-dot"/>'
    g0=f'<g transform="translate({dx},0)">' if dx else ''
    g1='</g>' if dx else ''
    return (f'<svg class="{cls}" viewBox="0 0 {vw} 380" role="img" aria-label="{aria}" style="width:{width}px">{g0}'
            f'<path d="{FACE_PATH}" class="fc-line"/>'
            f'<path d="M100,178 C88,172 80,182 84,196 C87,208 96,214 104,210" class="fc-line fc-thin"/>'
            f'<path d="M168,132 C176,128 186,128 192,131" class="fc-line fc-thin"/>'
            f'<path d="M170,152 C176,148 184,148 189,151" class="fc-thin fc-line"/>'
            f'<path d="M130,340 C136,354 146,362 158,368" class="fc-line fc-thin"/>{g1}{m}</svg>')

def gel_icons():
    return {
    'gota': '<svg viewBox="0 0 90 90" class="gelico"><path d="M45,10 C45,10 20,42 20,58 a25,25 0 0 0 50,0 C70,42 45,10 45,10 Z" fill="var(--fam-a)" fill-opacity=".25" stroke="var(--fam-a)" stroke-width="2.5"/><ellipse cx="45" cy="80" rx="20" ry="4" fill="var(--fam-a)" fill-opacity=".35"/></svg>',
    'mel': '<svg viewBox="0 0 90 90" class="gelico"><path d="M40,8 C40,26 34,30 34,44 C34,58 46,58 46,44 C46,34 42,30 42,20" fill="none" stroke="var(--fam-m)" stroke-width="7" stroke-linecap="round"/><path d="M20,72 q12,-10 25,0 t25,0" fill="none" stroke="var(--fam-m)" stroke-width="7" stroke-linecap="round"/><path d="M24,82 q10,-7 21,0 t21,0" fill="none" stroke="var(--fam-m)" stroke-width="5" stroke-linecap="round" opacity=".6"/></svg>',
    'rigido': '<svg viewBox="0 0 90 90" class="gelico"><path d="M20,70 L26,34 Q45,22 64,34 L70,70 Z" fill="var(--fam-r)" fill-opacity=".25" stroke="var(--fam-r)" stroke-width="2.5" stroke-linejoin="round"/><path d="M38,38 L34,68 M52,36 L58,68 M27,52 L63,50" stroke="var(--fam-r)" stroke-width="2" opacity=".65"/></svg>',
    }

def box_pratica(titulo, texto, qr, url):
    return (f'<aside class="pratica"><div class="bx-head">NA PRÁTICA</div><div class="bx-body"><div>'
            f'<h4>{html.escape(titulo)}</h4><p>{texto}</p>'
            f'<p class="bx-url"><a href="{html.escape(url)}">{html.escape(url)}</a></p></div>'
            f'<img class="bx-qr" src="{qr}" alt="QR code — {html.escape(titulo)}" width="118" height="118"></div></aside>')

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

# ---------------- seções de grupos ----------------
fam_secs=[]; CH0=6
for gi,g in enumerate(['G1','G2','G3','G4','G5']):
    G=GRUPOS[g]; prods=[p for p in ed.PRODUTOS if grp(p)==g]
    prods.sort(key=lambda p:DATA[p['k']]['G1_0.7Hz'])
    cards='\n'.join(card(p) for p in prods)
    gmin,gmax=DATA[prods[0]['k']]['G1_0.7Hz'],DATA[prods[-1]['k']]['G1_0.7Hz']
    extra=''
    if g=='G5':
        extra='<p class="famdesc" style="margin-top:.3rem">Caso de borda com curadoria oficial: Restylane Defyne (292,62 Pa) permanece neste grupo, com o G′ marcado em roxo por decisão do mapa.</p>'
    fam_secs.append(f'''<section class="famsec" id="grupo-{G['num']}">
<div class="fambanner bn-{G['fam']}"><div><p class="fam-eyebrow">CAPÍTULO {CH0+gi} · GRUPO {G['num']} · {html.escape(G['tec'])}</p><h2>{G['nome']}</h2>
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
sf_sec=f'''<section class="famsec" id="grupo-6">
<div class="fambanner bn-s"><div><p class="fam-eyebrow">CAPÍTULO 11 · GRUPO 6 · critério funcional transversal · 💧</p><h2>PRECISOS — BAIXO SWELLING FACTOR</h2>
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

FACE_CAPA = face_svg(200, marks=[(150,74,'a','','start'),(168,163,'s','','start'),
    (176,224,'m','','start'),(146,208,'v','','end'),(203,298,'r','','start')], cls='facesvg capa-face', aria='perfil facial com pontos das famílias do mapa')

FACE_GEO = face_svg(300, marks=[(196,268,'a','LINHA · perioral','R'),(178,222,'m','VALE · sulco nasolabial','R'),
    (144,204,'m','CURVA · malar','L'),(160,242,'r','SUPORTE · profundo','L'),(202,300,'r','VÉRTICE · mento','R')],
    cls='facesvg', aria='tarefas geométricas na face', vw=390, dx=45, leader=True)

page=f'''<title>eBook Reology Map</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700;9..144,900&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;600;700&display=swap">
<style>
:root {{
 --bg:#FAF9FC; --card:#FFFFFF; --ink:#1D1A23; --ink2:#554E63; --ink3:#8B849B;
 --line:#E5E1EE; --linesoft:#EFECF6; --accent:#6D3FB4; --accent-ink:#5A2F9E; --accent-soft:#F1EAFB;
 --fam-a:#2E7DBF; --fam-m:#A6801C; --fam-r:#7C3AED; --fam-v:#3E9B6E;
 --chip-rosa:#CE6E9E; --sf:#17808F; --sf-soft:rgba(23,128,143,.10);
 --warn:#B4572F; --flag:#C64F4F;
 --za:rgba(46,125,191,.055); --zm:rgba(166,128,28,.06); --zr:rgba(124,58,237,.05);
 --n1bg:#6D3FB4; --n1ink:#FFFFFF; --n2bg:#E8DDF8; --n2ink:#4A2B86; --n3bd:#B9A3DE; --n3ink:#5A3F94; --n4ink:#7A7290;
 --tint:14%;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
 --bg:#161320; --card:#1E1A2A; --ink:#ECE9F3; --ink2:#B3ACC6; --ink3:#7E7692;
 --line:#332D44; --linesoft:#2A2439; --accent:#A98BE0; --accent-ink:#BCA3EA; --accent-soft:#2A2140;
 --fam-a:#3F87C4; --fam-m:#B18927; --fam-r:#8E68D8; --fam-v:#43A076;
 --chip-rosa:#C4789F; --sf:#4FB3C4; --sf-soft:rgba(79,179,196,.13);
 --warn:#D08A5E; --flag:#DC7E7E;
 --za:rgba(63,135,196,.10); --zm:rgba(177,137,39,.10); --zr:rgba(142,104,216,.10);
 --n1bg:#8E68D8; --n1ink:#14101E; --n2bg:#332756; --n2ink:#CBB6F2; --n3bd:#6B549E; --n3ink:#B49BE6; --n4ink:#8F86A8;
 --tint:20%;
}} }}
:root[data-theme="dark"] {{
 --bg:#161320; --card:#1E1A2A; --ink:#ECE9F3; --ink2:#B3ACC6; --ink3:#7E7692;
 --line:#332D44; --linesoft:#2A2439; --accent:#A98BE0; --accent-ink:#BCA3EA; --accent-soft:#2A2140;
 --fam-a:#3F87C4; --fam-m:#B18927; --fam-r:#8E68D8; --fam-v:#43A076;
 --chip-rosa:#C4789F; --sf:#4FB3C4; --sf-soft:rgba(79,179,196,.13);
 --warn:#D08A5E; --flag:#DC7E7E;
 --za:rgba(63,135,196,.10); --zm:rgba(177,137,39,.10); --zr:rgba(142,104,216,.10);
 --n1bg:#8E68D8; --n1ink:#14101E; --n2bg:#332756; --n2ink:#CBB6F2; --n3bd:#6B549E; --n3ink:#B49BE6; --n4ink:#8F86A8;
 --tint:20%;
}}
*{{box-sizing:border-box}} html{{scroll-behavior:smooth}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:'Source Serif 4',Georgia,serif;font-size:15.5px;line-height:1.6}}
.pill,.lbl,.marca,.legend,.stat span,.famdesc,.fam-eyebrow,.sflink,.evite,.alts,.tech,.flags,.sfnum,.sigdots,.bx-url{{font-family:'Source Sans 3',system-ui,sans-serif}}
.cap-eyebrow{{font-family:'JetBrains Mono',monospace;font-size:.68rem;letter-spacing:.24em;text-transform:uppercase;color:var(--accent-ink);margin:0 0 .25rem}}
main{{max-width:78rem;margin:0 auto;padding:2rem 1.2rem 5rem}}
a{{color:var(--accent-ink)}} a:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.chip{{display:inline-block;border-radius:50%;border:1.5px solid rgba(0,0,0,.16);margin-right:4px;vertical-align:-1px}}
h1,h2,h3{{font-family:'Fraunces',Georgia,serif;text-wrap:balance;line-height:1.08}}
.capa{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1.4rem;margin-bottom:1.4rem}}
.capa-frame{{position:relative;border:2px solid var(--ink);padding:2.6rem 1.6rem 2rem;text-align:center}}
.capa-frame::after{{content:"";position:absolute;inset:7px;border:1px solid color-mix(in srgb,var(--ink) 45%,transparent);pointer-events:none}}
.capa-frame p{{max-width:none}}
.capa-top{{font-family:'JetBrains Mono',monospace;font-size:.72rem;letter-spacing:.3em;text-transform:uppercase;color:var(--ink2);margin:0}}
.capa-tag{{font-family:'Source Sans 3',sans-serif;font-size:.8rem;letter-spacing:.24em;text-transform:uppercase;color:var(--accent-ink);margin:.4rem 0 0}}
.capa-rule{{border:0;border-top:1px solid var(--ink3);width:130px;margin:1.1rem auto}}
.capa-rule.sm{{width:70px;margin:.9rem auto}}
.capa h1{{font-size:clamp(2.3rem,5.6vw,3.7rem);font-weight:900;margin:.2rem 0 .7rem;letter-spacing:-.01em}}
.capa .sub{{font-family:'Fraunces',serif;font-style:italic;font-size:clamp(1rem,2.2vw,1.25rem);color:var(--ink2);margin:0 auto 1.3rem;max-width:40ch}}
.capa-visual{{display:flex;justify-content:center;align-items:center;gap:2.5rem;flex-wrap:wrap}}
.capa-emb{{width:min(190px,48vw);height:auto}}
.capa-face{{max-width:44vw}}
.capa-autor{{font-family:'Fraunces',serif;font-weight:600;font-size:1.35rem;margin:1.2rem 0 0}}
.capa-imprint{{font-family:'Source Sans 3',sans-serif;font-size:.82rem;letter-spacing:.18em;text-transform:uppercase;color:var(--ink2);margin:.4rem 0 0}}
.capa-band{{height:9px;margin-top:1.4rem;background:linear-gradient(90deg,var(--fam-a) 0 25%,var(--fam-m) 25% 50%,var(--fam-r) 50% 75%,var(--fam-v) 75% 100%)}}
.fichatec{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1rem 1.3rem;margin-bottom:.4rem}}
.fichatec .meta{{display:flex;flex-wrap:wrap;gap:.4rem 1.8rem;color:var(--ink2);font-size:.92rem;margin:0}}
.fichatec .meta b{{color:var(--ink)}}
.stats{{display:flex;flex-wrap:wrap;gap:1rem;margin-top:.9rem}}
.stat{{background:var(--card);border:1px solid var(--line);border-top:4px solid var(--accent);border-radius:8px;padding:.7rem 1.1rem;min-width:8.5rem}}
.stat:nth-child(1){{border-top-color:var(--fam-a)}} .stat:nth-child(2){{border-top-color:var(--fam-m)}}
.stat:nth-child(3){{border-top-color:var(--fam-r)}} .stat:nth-child(4){{border-top-color:var(--sf)}}
.stat b{{display:block;font-family:'JetBrains Mono',monospace;font-size:1.35rem;color:var(--accent-ink)}}
.stat span{{font-size:.8rem;color:var(--ink2)}}
section{{margin-top:2.8rem}}
h2{{font-size:1.65rem;font-weight:700;margin:0 0 .8rem}}
h3{{font-size:1.15rem;margin:1.4rem 0 .5rem}}
p{{max-width:76ch}} .lead{{color:var(--ink2)}}
.box{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1.1rem 1.3rem}}
.qt{{border-left:3px solid var(--accent);background:var(--accent-soft);border-radius:0 10px 10px 0;padding:.8rem 1.1rem;font-family:'Fraunces',serif;font-size:1.06rem;margin:1rem 0;max-width:70ch}}
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
.chart{{width:100%;height:auto;background:var(--card);border:1px solid var(--line);border-radius:10px;margin-top:.6rem}}
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
.rdemo{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:.9rem;text-align:center}}
.rdemo figcaption{{font-size:.82rem;color:var(--ink2);margin-top:.4rem}} .rdemo b{{color:var(--ink)}}
/* face / figuras */
.fc-line{{fill:none;stroke:var(--ink2);stroke-width:2.6;stroke-linecap:round}}
.fc-thin{{stroke-width:1.8;opacity:.75}}
.fc-dot{{stroke:var(--card);stroke-width:2}}
.fc-ld{{stroke:var(--ink3);stroke-width:1;stroke-dasharray:2 3}}
.fc-lb{{fill:var(--ink2);font:600 11px 'Source Sans 3',sans-serif}}
figure.figura{{margin:1.2rem 0;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1rem 1.2rem;text-align:center}}
figure.figura figcaption{{text-align:left;font-size:.85rem;color:var(--ink2);border-top:1px solid var(--linesoft);margin-top:.8rem;padding-top:.6rem}}
figure.figura figcaption b{{color:var(--ink)}}
.gelrow{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:1rem;margin:1rem 0}}
.gelcard{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1rem;text-align:center}}
.gelico{{width:88px;height:88px}}
.gelcard h4{{font-family:'Fraunces',serif;margin:.4rem 0 .2rem}}
.gelcard p{{font-size:.88rem;color:var(--ink2);margin:.2rem 0}}
.gelcard .gelsub{{font-family:'JetBrains Mono',monospace;font-size:.68rem;letter-spacing:.14em;color:var(--ink3)}}
/* boxes estilo aprovado */
.pratica,.saibamais{{margin:1.4rem 0;border:1px solid var(--line);border-radius:10px;overflow:hidden;background:var(--card)}}
.bx-head{{font-family:'JetBrains Mono',monospace;font-size:.72rem;letter-spacing:.26em;padding:.45rem 1.1rem;color:#fff;background:var(--accent)}}
.saibamais .bx-head{{background:var(--sf)}}
.bx-body{{display:flex;gap:1.2rem;padding:1rem 1.2rem;align-items:center;flex-wrap:wrap}}
.bx-body h4{{font-family:'Fraunces',serif;margin:0 0 .3rem;font-size:1.05rem}}
.bx-body p{{margin:.2rem 0;font-size:.92rem;max-width:58ch}}
.bx-body>div{{flex:1;min-width:230px}}
.bx-qr{{border:1px solid var(--line);border-radius:8px;background:#fff;padding:4px;flex:none}}
.bx-url a{{font-size:.78rem;word-break:break-all;color:var(--ink3)}}
/* bandeiras */
.fambanner{{display:flex;flex-wrap:wrap;gap:.6rem 2.5rem;align-items:center;justify-content:space-between;border-radius:10px;padding:1.15rem 1.4rem;margin-bottom:1.1rem;border:1px solid var(--line)}}
.bn-a{{background:linear-gradient(120deg,color-mix(in srgb,var(--fam-a) var(--tint),var(--card)),var(--card) 78%);border-left:8px solid var(--fam-a)}}
.bn-m{{background:linear-gradient(120deg,color-mix(in srgb,var(--fam-m) var(--tint),var(--card)),var(--card) 78%);border-left:8px solid var(--fam-m)}}
.bn-r{{background:linear-gradient(120deg,color-mix(in srgb,var(--fam-r) var(--tint),var(--card)),color-mix(in srgb,var(--fam-v) 8%,var(--card)));border-left:8px solid var(--fam-r)}}
.bn-s{{background:linear-gradient(120deg,var(--sf-soft),var(--card) 78%);border-left:8px solid var(--sf)}}
.fam-eyebrow{{font-family:'JetBrains Mono',monospace;font-size:.7rem;letter-spacing:.14em;color:var(--ink2);margin:0 0 .25rem}}
.fambanner h2{{margin:0;font-size:1.7rem}}
.famchave{{font-family:'Fraunces',serif;font-style:italic;color:var(--ink2);margin:.35rem 0 0;max-width:44ch}}
.famdesc{{margin:0;color:var(--ink2);font-size:.92rem;max-width:38rem}}
.grid2{{display:grid;grid-template-columns:repeat(auto-fill,minmax(350px,1fr));gap:1rem}}
.grid3{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1rem}}
/* cards */
.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:0 1.1rem 1rem;display:flex;flex-direction:column;gap:.5rem;break-inside:avoid;border-left-width:6px;border-left-style:solid}}
.card.fam-a{{border-left-color:var(--fam-a)}} .card.fam-m{{border-left-color:var(--fam-m)}} .card.fam-r{{border-left-color:var(--fam-r)}}
.card header{{display:flex;justify-content:space-between;gap:.6rem;align-items:flex-start;margin:0 -1.1rem;padding:.7rem 1.1rem .5rem}}
.card.fam-a header{{background:linear-gradient(90deg,color-mix(in srgb,var(--fam-a) var(--tint),transparent),transparent 75%)}}
.card.fam-m header{{background:linear-gradient(90deg,color-mix(in srgb,var(--fam-m) var(--tint),transparent),transparent 75%)}}
.card.fam-r header{{background:linear-gradient(90deg,color-mix(in srgb,var(--fam-r) var(--tint),transparent),transparent 75%)}}
.card h4{{font-family:'Fraunces',serif;font-size:1.1rem;margin:0;line-height:1.15}}
.c-right{{display:flex;flex-direction:column;align-items:flex-end;gap:.1rem}}
.marca{{font-size:.72rem;color:var(--ink3);white-space:nowrap;letter-spacing:.03em}}
.famtag{{font-family:'JetBrains Mono',monospace;font-size:.58rem;font-weight:700;letter-spacing:.09em;white-space:nowrap}}
.sigdots{{display:flex;gap:.9rem;font-size:.72rem;color:var(--ink3);padding-bottom:.3rem}}
.assin{{margin:0 0 .1rem;display:flex;flex-direction:column;gap:.1rem;border-bottom:1px solid var(--linesoft);padding-bottom:.45rem}}
.assin-lbl{{font-family:'Source Sans 3',sans-serif;font-size:.62rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--ink3)}}
.assin-v{{display:flex;align-items:center;gap:.3rem;font-family:'JetBrains Mono',monospace;font-size:.74rem;letter-spacing:.02em}}
.assin-v i{{width:13px;height:13px;border-radius:50%;display:inline-block;border:1.5px solid rgba(0,0,0,.16)}}
.assin-v .plus{{color:var(--ink3);font-size:.7rem}}
.assin-v b{{color:var(--ink);font-weight:700}}
.ico{{flex:none}}
.logo{{height:auto}}
.lg-e{{stroke:var(--accent-ink);stroke-width:1.6;opacity:.5}}
.lg-n{{fill:var(--accent-ink)}}
.gram{{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:.9rem;margin:.9rem 0}}
.gramc{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1rem;display:flex;gap:.8rem;align-items:flex-start}}
.gramc h4{{font-family:'Fraunces',serif;margin:0 0 .1rem;font-size:1.02rem}}
.gramc .verbo{{font-family:'JetBrains Mono',monospace;font-size:.68rem;letter-spacing:.1em;display:block;margin-bottom:.25rem}}
.gramc p{{margin:0;font-size:.85rem;color:var(--ink2)}}
.a9{{display:grid;grid-template-columns:repeat(auto-fit,minmax(168px,1fr));gap:.6rem;margin:.9rem 0}}
.a9c{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:.65rem .8rem;text-align:center}}
.a9dots{{display:flex;align-items:center;justify-content:center;gap:.25rem;margin-bottom:.35rem}}
.a9dots i{{width:16px;height:16px;border-radius:50%;display:inline-block;border:1.5px solid rgba(0,0,0,.16)}}
.a9dots span{{color:var(--ink3);font-size:.8rem}}
.a9n{{font-family:'JetBrains Mono',monospace;font-size:.68rem;font-weight:700;letter-spacing:.04em;line-height:1.3;display:block}}
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
.escolha{{margin:0;border-left:3px solid var(--accent);background:color-mix(in srgb,var(--accent-soft) 70%,transparent);padding:.5rem .7rem;border-radius:0 8px 8px 0;font-size:.9rem;font-style:italic}}
.alts,.tech{{margin:0;font-size:.82rem;color:var(--ink2)}}
.flags{{margin:0;font-size:.76rem;color:var(--flag);font-weight:600}}
.sfcard{{background:var(--card);border:1px solid var(--line);border-left:6px solid var(--sf);border-radius:10px;padding:.9rem 1rem;display:flex;flex-direction:column;gap:.45rem;break-inside:avoid}}
.sfcard header{{display:flex;align-items:baseline;gap:.3rem;flex-wrap:wrap}}
.sfcard h4{{font-family:'Fraunces',serif;font-size:1.02rem;margin:0}}
.sfcard .marca{{margin-left:auto}}
.sfnum{{display:flex;align-items:center;gap:1rem;font-family:'JetBrains Mono',monospace;font-size:.8rem;color:var(--ink2);background:var(--sf-soft);border-radius:10px;padding:.35rem .7rem}}
.sfnum b{{color:var(--ink)}} .sfnum .radar-sm{{margin-left:auto}}
.sfcard p{{margin:0;font-size:.88rem}}
.sflink{{font-size:.8rem;text-decoration:none;font-weight:600;color:var(--sf)}}
.sflink:hover{{text-decoration:underline}}
.regtab{{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--card)}}
.regtab table{{border-collapse:collapse;width:100%;font-size:.88rem;min-width:720px}}
.regtab th,.regtab td{{padding:.5rem .7rem;border-bottom:1px solid var(--linesoft);text-align:left;vertical-align:top}}
.regtab th{{font-size:.74rem;letter-spacing:.06em;text-transform:uppercase;color:var(--ink3)}}
.regtab .obs{{color:var(--ink3);font-size:.8rem}}
.ix{{columns:3;column-gap:2rem}} @media(max-width:56rem){{.ix{{columns:2}}}} @media(max-width:38rem){{.ix{{columns:1}}}}
.ixm{{break-inside:avoid;margin-bottom:.9rem;font-size:.88rem}}
.ixm b{{display:block;font-family:'Fraunces',serif;margin-bottom:.15rem}}
.ixm a{{display:block;text-decoration:none;color:var(--ink2);padding:.06rem 0}}
.ixm a:hover{{color:var(--accent-ink);text-decoration:underline}}
.rodape{{margin-top:3rem;border-top:1px solid var(--line);padding-top:1rem;color:var(--ink3);font-size:.82rem}}
@media print{{ body{{background:#fff;font-size:11px}} .famsec,#rankings,#regioes,#textura{{break-before:page}}
 .card,.sfcard,.rdemo,.pratica,.saibamais{{break-inside:avoid;border-color:#ccc}} #tip{{display:none}} .capa{{border:none}} }}
@media(max-width:30rem){{.vis{{flex-direction:column;align-items:flex-start}}}}
</style>
<main>
<header class="capa">
<div class="capa-frame">
{logo(74)}
<p class="capa-top">Reology Map</p>
<p class="capa-tag">Ciência que guia escolhas</p>
<hr class="capa-rule">
<h1>Reologia do<br>Ácido Hialurônico</h1>
<p class="sub">Guia Reológico dos Preenchedores do Mercado Brasileiro — 75 produtos canônicos · 76 ensaios</p>
<div class="capa-visual">{FACE_CAPA}{emblema()}</div>
<p class="capa-autor">Dr. João Pithon</p>
<hr class="capa-rule sm">
<p class="capa-imprint">Primeira edição · São Paulo · 2026</p>
</div>
<div class="capa-band"></div>
</header>

<div class="fichatec">
<p class="meta"><span>Estudo <b>Reológico Pithon Napoli (2026)</b> — 76 ensaios · 75 produtos canônicos sob protocolo único</span><span>Ensaio <b>reômetro rotacional TA Instruments AR-1500ex</b> · 25&nbsp;°C · placas Ø20&nbsp;mm · gap 500&nbsp;µm · varredura 10&nbsp;→&nbsp;0,01&nbsp;Hz</span><span>Frequência de referência <b>0,7&nbsp;Hz</b></span></p>
<div class="stats"><div class="stat"><b>34</b><span>baixo G′ — grupos 1–2</span></div><div class="stat"><b>14</b><span>intermediário — grupo 3</span></div><div class="stat"><b>28</b><span>alto G′ — grupos 4–5</span></div><div class="stat"><b>💧 6º</b><span>grupo funcional: baixo SF</span></div></div>
<p class="qt" style="margin:1rem 0 .2rem">“Não existe o melhor preenchedor. Existe a propriedade reológica mais adequada para o comportamento que queremos produzir em cada região.”</p>
</div>

<section id="comoler">
<p class="cap-eyebrow">Capítulo 1</p><h2>Como ler este guia</h2>
<div class="box">
<p style="margin-top:0">Os preenchedores estão organizados nos <b>seis grupos oficiais do Mapa da Reologia</b>: <b style="color:var(--fam-a)">G1 Fluidos Dinâmicos</b> · <b style="color:var(--fam-a)">G2 Fluidos com Corpo</b> · <b style="color:var(--fam-m)">G3 Equilibrados</b> · <b style="color:var(--fam-r)">G4 Projetores Puros</b> · <b style="color:var(--fam-r)">G5 Estruturais Moldáveis</b> · <b style="color:var(--sf)">G6 Precisos (Baixo SF)</b>, o grupo funcional transversal. <i>“A primeira cor mostra quanto o gel estrutura. As demais cores mostram como essa estrutura se comporta.”</i></p>
<h3 style="margin-top:1.2rem">A gramática das cores — 1ª cor, 2ª cor, assinatura</h3>
<p style="margin-top:.2rem"><b>A 1ª cor mostra quanto o gel estrutura</b> (o G′):</p>
<div class="gram">
<div class="gramc">{ico('ondas')}<div><h4>Baixo G′</h4><span class="verbo" style="color:var(--fam-a)">ESPALHA / INTEGRA</span><p>Menor relevo e menor capacidade estrutural.<br><i>Ex.: glabela, fronte, têmpora, supercílio.</i></p></div></div>
<div class="gramc">{ico('balanca')}<div><h4>G′ intermediário</h4><span class="verbo" style="color:var(--fam-m)">PREENCHE / EQUILIBRA</span><p>Equilíbrio entre preenchimento e sustentação.<br><i>Ex.: sulcos, malar, transições.</i></p></div></div>
<div class="gramc">{ico('coluna')}<div><h4>Alto G′</h4><span class="verbo" style="color:var(--fam-r)">SUSTENTA / PROJETA</span><p>Maior manutenção de forma e estrutura.<br><i>Ex.: nariz, mento, mandíbula, arco zigomático.</i></p></div></div>
</div>
<p><b>A 2ª cor mostra como essa estrutura se comporta</b> (o tan δ):</p>
<div class="gram">
<div class="gramc">{ico('dinamico')}<div><h4>Dinâmico</h4><span class="verbo" style="color:var(--chip-rosa)">ACOMPANHA O MOVIMENTO</span><p>Maior componente viscosa relativa: acompanha melhor o movimento do tecido.</p></div></div>
<div class="gramc">{ico('maleavel')}<div><h4>Maleável</h4><span class="verbo" style="color:var(--fam-v)">MOLDÁVEL / INTEGRATIVO</span><p>Boa adaptação e distribuição tecidual: molda e distribui.</p></div></div>
</div>
<p><b>Somando as duas cores nascem as nove assinaturas reológicas</b> — o nome oficial de cada perfil no Reology Map:</p>
<div class="a9">{a9_cards}</div>
<p style="font-size:.9rem;color:var(--ink2)">Nas fichas, cada produto exibe sua assinatura logo abaixo do nome. As três assinaturas "puras" (ESPALHA, PREENCHE, PROJETA) são os perfis de tan δ baixo, em que a estrutura fala mais alto que o comportamento.</p>
<p><b>Assinatura de cores por métrica</b> — cada ficha traz 4 pontos coloridos, um por parâmetro (0,7 Hz): G′ e η* em <span class="chip" style="width:11px;height:11px;background:var(--fam-a)"></span>azul (baixo) / <span class="chip" style="width:11px;height:11px;background:var(--fam-m)"></span>amarelo (intermediário) / <span class="chip" style="width:11px;height:11px;background:var(--fam-r)"></span>roxo (alto); G″ idem; tan δ em <span class="chip" style="width:11px;height:11px;background:var(--fam-r)"></span>roxo (baixo, elástico) / <span class="chip" style="width:11px;height:11px;background:var(--fam-v)"></span>verde (intermediário, maleável) / <span class="chip" style="width:11px;height:11px;background:var(--chip-rosa)"></span>rosa (alto, dinâmico). Cortes: G′ 200/300 Pa · G″ 50/100 Pa · tan δ 0,15/0,20 · η* 50/100 Pa·s — com zonas de transição e curadoria (ex.: Defyne).</p>
<div class="g33 passos">
<div class="box passo"><b>O que eu quero fazer?</b><p style="margin:.3rem 0 0;font-size:.9rem;color:var(--ink2)">Espalhar → grupos 1–2 · Preencher → grupo 3 · Projetar → grupos 4–5.</p></div>
<div class="box passo"><b>Esse tecido se move muito?</b><p style="margin:.3rem 0 0;font-size:.9rem;color:var(--ink2)">Se sim, procure perfil <b style="color:var(--chip-rosa)">DINÂMICO</b> (tan δ rosa): acompanha o movimento.</p></div>
<div class="box passo"><b>Preciso moldar e distribuir?</b><p style="margin:.3rem 0 0;font-size:.9rem;color:var(--ink2)">Se sim, procure perfil <b style="color:var(--fam-v)">MALEÁVEL</b> (tan δ verde): adapta e distribui.</p></div>
</div>
<p><b>Níveis de indicação:</b> <span class="pill n1">região<i>1ª escolha</i></span> <span class="pill n2">região<i>forte</i></span> <span class="pill n3">região<i>boa</i></span> <span class="pill n4">região<i>seletiva</i></span></p>
<p style="margin-bottom:0"><b>Regra das quatro camadas:</b> MEDIDO (laudo do estudo, com lote) · FABRICANTE (*) · LITERATURA (citada) · INTERPRETAÇÃO (Reology Map). <b>SF, coesividade, extrusão e Strain X não foram medidos</b> (💧) e nunca são deduzidos — dado ausente é informação. <b>Sinalizações:</b> <span style="color:var(--flag);font-weight:600">⚑ dado em re-verificação</span> · ◌ monografia pendente · ※ contraindicação de bula. <b>Segurança:</b> reologia não é segurança vascular.</p>
</div>
</section>

<section id="fundamentos">
<p class="cap-eyebrow">Capítulo 2</p><h2>Os quatro números em 60 segundos</h2>
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
 'Acesse as aulas do Dr. João Pithon sobre reologia aplicada ao preenchimento — fundamentos, leitura de parâmetros e escolha do produto na prática clínica. Escaneie o QR Code com a câmera do celular para abrir a pasta de aulas no Drive.',
 QR['aulas'], 'https://drive.google.com/drive/folders/1ztwjgguHK3VdDHG-j2E5CL4ViGglwpv-')}
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

<section id="mapasec">
<p class="cap-eyebrow">Capítulo 3</p><h2>O Mapa da Reologia — todos os géis em um plano</h2>
<p class="lead">Cada ponto é um ensaio (0,7&nbsp;Hz). As faixas coloridas são as três famílias da 1ª cor (cortes 200 e 300&nbsp;Pa); a altura é o caráter dinâmico (tan δ). Passe o mouse/toque para identificar.</p>
{scatter_main()}
{LEG3}
<p class="lead" style="font-size:.9rem">Achados: apenas <b>2 dos 76 ensaios</b> são “roxo completo” (grupo 4); os pares sobrepostos (Volift=Voluma, Belotero Volume+=Neauvia Intense, Stimulate=Singderm) estão em re-verificação; famílias comerciais inteiras vivem numa mesma zona — a cor classifica, o número posiciona.</p>
<figure class="figura">{FACE_GEO}
<figcaption><b>Figura 1.</b> As cinco tarefas geométricas do preenchimento sobre a face: <b>LINHA</b> (microdepressão superficial — perioral), <b>VALE</b> (depressão — sulco nasolabial, pré-jowl), <b>CURVA</b> (convexidade difusa — malar/bochecha), <b>SUPORTE</b> (sustentação profunda — fossa piriforme, supraperiostal) e <b>VÉRTICE</b> (projeção focal — mento, ângulo, zigoma). A cor de cada ponto indica a família de G′ tipicamente exigida; o gel é escolhido para a tarefa, não para a região inteira.</figcaption></figure>
</section>

<section id="forma">
<p class="cap-eyebrow">Capítulo 4</p><h2>A forma do gel — o radar de 4 eixos</h2>
<p class="lead">Cada produto tem uma <b>forma geométrica</b> construída com as 4 características medidas: <b>G′</b> (cima), <b>G″</b> (direita), <b>tan δ</b> (baixo) e <b>η*</b> (esquerda), em percentil do banco a 0,7 Hz. A forma é a impressão digital reológica do gel.</p>
<div class="rdemos">
{radar_demo('Belotero Balance Lido','Pipa para BAIXO: tan δ domina — gel dissipativo, espalha e acompanha.')}
{radar_demo('Juvéderm Skinvive','Baixo + direita: dissipação com G″ proporcional alto — trata a superfície.')}
{radar_demo('Juvéderm Volux','Seta para CIMA-ESQUERDA: G′ e η* máximos com tan δ mínimo — vértice puro.')}
{radar_demo('Restylane Lido (lote 22647)','Losango CHEIO: alto em tudo — estrutura com dissipação (moldável).')}
</div>
<p class="lead" style="font-size:.92rem">Como ler: <b>seta para cima-esquerda</b> = estrutura e permanência · <b>pipa para baixo</b> = integração e movimento · <b>losango largo</b> = magnitude com equilíbrio viscoelástico · <b>forma pequena</b> = gel leve em todas as dimensões.</p>
</section>

<section id="textura">
<p class="cap-eyebrow">Capítulo 5</p><h2>Textura visual do gel — o que os olhos antecipam</h2>
<p class="lead">Antes do reômetro, o gel já conta parte da história ao ser extrudado: existe um padrão visual nos tipos de géis. Uns escorrem <b>em gota</b>; outros vertem densos, <b>como mel</b>; outros saem <b>rígidos</b>, em cordão que se quebra — o aspecto <b>fraturado</b>. Além do escoamento, observa-se a aparência: gel <b>translúcido</b> e contínuo ou opalescente e particulado.</p>
<div class="gelrow">
<div class="gelcard">{GEL['gota']}<h4>Em gota — fluido</h4><p class="gelsub">TÍPICO DOS GRUPOS 1–2</p><p>Escorre e se espalha; vence a própria forma. Antecipa integração alta e baixo relevo.</p></div>
<div class="gelcard">{GEL['mel']}<h4>Como mel — viscoso denso</h4><p class="gelsub">TÍPICO DO GRUPO 3</p><p>Verte em fita contínua e lenta; segura a forma por instantes. Antecipa corpo e equilíbrio.</p></div>
<div class="gelcard">{GEL['rigido']}<h4>Rígido / fraturado — estrutural</h4><p class="gelsub">TÍPICO DOS GRUPOS 4–5</p><p>Sai em cordão firme que mantém geometria — e, nos mais coesos, fratura em blocos em vez de escorrer.</p></div>
</div>
<p class="lead" style="font-size:.92rem"><b>Regra de honestidade:</b> a textura visual <i>sugere</i>; o reômetro <i>confirma</i>. Aparência translúcida ou particulada não prevê G′ (“nome, cor e aspecto não são reologia”) — por isso cada impressão visual deste capítulo remete à ficha numérica do produto.</p>
{box_pratica('Vídeos e imagens de textura — galeria oficial do estudo',
 'Assista aos vídeos ilustrativos de extrusão e textura dos géis (em gota, como mel, rígido/fraturado) e veja as imagens comparativas da galeria do Reology Map. O acervo é atualizado continuamente pelo autor — os vídeos de cada grupo entram nesta mesma pasta.',
 QR['galeria'], 'https://drive.google.com/drive/folders/1xcyZVRcnvkHyYFCXOlZf9pWmq-CVwlm1')}
</section>

<section id="atlas">
<p class="cap-eyebrow">Capítulo 6 (gráficos) · Capítulos 7–11 (grupos)</p><h2>Atlas de gráficos — todas as variáveis</h2>
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

<section id="rankings">
<p class="cap-eyebrow">Capítulo 12</p><h2>Rankings completos — os 76 ensaios lado a lado</h2>
<h3>G′ a 0,7 Hz (Pa) — a espinha estrutural do banco</h3>
{ranking('g1','G′ a 0,7 Hz (Pa)',960,br0,(0,200,300,500,750))}
<h3>tan δ a 0,7 Hz — o eixo do movimento</h3>
{ranking('td','tan δ a 0,7 Hz',0.72,lambda v: br(v,2),(0,0.15,0.30,0.50,0.70))}
</section>

<section id="regioes">
<p class="cap-eyebrow">Capítulo 13</p><h2>Guia rápido por região</h2>
<p class="lead">Síntese do mapeamento região → necessidade reológica → produtos citados nas monografias. Uma região pode pertencer a mais de um grupo conforme o objetivo (corpo do mento ≠ vértice do mento).</p>
<div class="regtab"><table><thead><tr><th>Região</th><th>Necessidade</th><th>Produtos (1ª escolha / fortes)</th><th>Observação</th></tr></thead><tbody>{reg_rows}</tbody></table></div>
</section>

<section id="indice">
<p class="cap-eyebrow">Apêndice A</p><h2>Índice por marca</h2>
<div class="ix">{idx}</div>
</section>

<section id="notas">
<p class="cap-eyebrow">Apêndice B</p><h2>Fontes, limitações e aviso</h2>
<div class="box">
<p style="margin-top:0"><b>Fonte dos números:</b> Estudo Reológico Pithon Napoli — laudo laboratorial independente, assinado, de 04/08/2026 (Anexo 2, 0,7 Hz), com lote identificado em cada ficha; 76 ensaios e 75 produtos canônicos (Restylane Lido em dois lotes, modelado como um produto com dois ensaios). Reômetro rotacional TA Instruments AR-1500ex, 25 °C, placas paralelas Ø 20 mm, gap 500 µm, varredura 10 → 0,01 Hz. Comparabilidade é <b>interna ao protocolo</b>; 25 °C in vitro ≠ comportamento in vivo. O radar usa <b>percentil do banco</b>, não valor absoluto. As cores seguem a gramática oficial do Mapa, com zonas de transição e curadoria versionada.</p>
<p><b>Não medidos nesta rodada</b> (prioridade da 2ª rodada): coesividade quantitativa, Swelling Factor, força de extrusão, Strain X/amplitude, compressão. Onde citados, são dados declarados pelo fabricante (*) ou impressão clínica do autor — dado ausente é informação, nunca inferência.</p>
<p><b>Fichas com ⚑</b> aguardam errata/re-verificação laboratorial (pares idênticos, η* divergentes, tan δ do Perfectha Subskin corrigido por recálculo). <b>Fichas com ◌</b> aguardam a monografia do autor.</p>
<p style="margin-bottom:0"><b>Aviso:</b> material educacional para profissionais habilitados; não substitui julgamento clínico, bula/IFU nem treinamento anatômico. Indicações refletem a experiência e a leitura reológica do autor sobre lotes específicos; os fabricantes não participaram nem endossam o estudo. Marcas citadas pertencem aos respectivos titulares.</p>
</div>
{box_pratica('Continue com o autor — aulas e atualizações',
 'As aulas de reologia da FEP e os materiais complementares do Reology Map ficam na pasta oficial do autor. Escaneie para acessar; o conteúdo é atualizado continuamente.',
 QR['aulas'], 'https://drive.google.com/drive/folders/1ztwjgguHK3VdDHG-j2E5CL4ViGglwpv-')}
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
