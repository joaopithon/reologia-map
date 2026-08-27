# -*- coding: utf-8 -*-
"""eBook Reology Map v2 — linhas Baixa/Intermediária/Alta + Baixo SF, radar 4 eixos, atlas de gráficos."""
import json, math, html, re, unicodedata, importlib.util

BASE = '/tmp/claude-0/-home-user-reologia-map/cd216e96-b088-57d1-abe3-2409c365400d/scratchpad'
spec = importlib.util.spec_from_file_location('ebook_data', f'{BASE}/ebook_data.py')
ed = importlib.util.module_from_spec(spec); spec.loader.exec_module(ed)
DATA = {r['produto']: r for r in json.load(open(f'{BASE}/produtos_full.json'))}
assert len(ed.PRODUTOS) == 76

def td_of(k):
    return 0.15 if k == 'Perfectha Subskin' else DATA[k]['tand_0.7Hz']  # errata auditoria
def br(v, nd=2): return f'{v:,.{nd}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
def br0(v): return f'{v:,.0f}'.replace(',', '.')
def slug(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii','ignore').decode()
    return re.sub(r'[^a-z0-9]+','-', t.lower()).strip('-')
def short(k):
    s = k.replace(' Lidocaine','').replace(' Lido','').replace(' lido','')
    return s if len(s)<=26 else s[:25]+'…'

FAMVAR = {'A':'a','M':'m','R':'r','RV':'v'}
FAMTAG = {'A':'INTEGRATIVO DINÂMICO','M':'PREENCHEDOR','R':'ESTRUTURAL','RV':'ESTRUTURAL MALEÁVEL'}
FAMCHIPS = {'A':['a','p'],'M':['m'],'R':['r'],'RV':['r','v']}
CHIP = dict(a='var(--fam-a)', m='var(--fam-m)', r='var(--fam-r)', v='var(--fam-v)', p='var(--chip-rosa)', s='var(--sf)')
NIVEL = {1:('1ª escolha','n1'),2:('forte','n2'),3:('boa','n3'),4:('seletiva','n4')}
FLAGTXT = {'verif':'⚑ dado em re-verificação laboratorial','pend':'◌ monografia do autor pendente','ifu':'※ contraindicações de bula listadas'}

# percentis para o radar (posição no banco, 0–1)
def ranks(vals):
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    r = [0]*len(vals)
    for pos,i in enumerate(order): r[i] = pos/(len(vals)-1)
    return r
KEYS = [p['k'] for p in ed.PRODUTOS]
RK = {}
for met, get in [('g1', lambda k: DATA[k]['G1_0.7Hz']), ('g2', lambda k: DATA[k]['G2_0.7Hz']),
                 ('td', td_of), ('eta', lambda k: DATA[k]['eta_0.7Hz'])]:
    rr = ranks([get(k) for k in KEYS])
    for k, v in zip(KEYS, rr): RK.setdefault(k, {})[met] = v

X0, X1 = math.log10(30), math.log10(1000)
def xg(g, w): return (math.log10(g)-X0)/(X1-X0)*w

def chips_html(keys, size=13):
    return ''.join(f'<span class="chip" style="width:{size}px;height:{size}px;background:{CHIP[c]}"></span>' for c in keys)

# ---------- radar 4 eixos ----------
def radar(k, fam, size=96, cls='radar'):
    c = size/2; R = c-13
    v = RK[k]
    # eixos: G′ cima · G″ direita · tan δ baixo · η* esquerda
    pts = []
    for met, ang in [('g1',-90),('g2',0),('td',90),('eta',180)]:
        rad = 5 + v[met]*(R-5); a = math.radians(ang)
        pts.append((c+rad*math.cos(a), c+rad*math.sin(a)))
    poly = ' '.join(f'{x:.1f},{y:.1f}' for x,y in pts)
    grid = []
    for f in (1/3, 2/3, 1.0):
        r = 5 + f*(R-5)
        d = ' '.join(f'{c+r*math.cos(math.radians(a)):.1f},{c+r*math.sin(math.radians(a)):.1f}' for a in (-90,0,90,180))
        grid.append(f'<polygon points="{d}" class="rd-grid"/>')
    axes = f'<line x1="{c}" y1="{c-R}" x2="{c}" y2="{c+R}" class="rd-ax"/><line x1="{c-R}" y1="{c}" x2="{c+R}" y2="{c}" class="rd-ax"/>'
    d0 = DATA[k]
    tip = f"G′ {br(d0['G1_0.7Hz'])} · G″ {br(d0['G2_0.7Hz'])} · tan δ {br(td_of(k))} · η* {br(d0['eta_0.7Hz'])}"
    lbl = (f'<text x="{c}" y="9" class="rd-lb" text-anchor="middle">G′</text>'
           f'<text x="{size-2}" y="{c+3}" class="rd-lb" text-anchor="end">G″</text>'
           f'<text x="{c}" y="{size-2}" class="rd-lb" text-anchor="middle">tan δ</text>'
           f'<text x="2" y="{c+3}" class="rd-lb">η*</text>')
    return (f'<svg class="{cls}" viewBox="0 0 {size} {size}" role="img" aria-label="forma reológica"><title>{html.escape(tip)}</title>'
            f'{"".join(grid)}{axes}<polygon points="{poly}" fill="var(--fam-{fam})" fill-opacity=".22" stroke="var(--fam-{fam})" stroke-width="2" stroke-linejoin="round"/>'
            + ''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.4" fill="var(--fam-{fam})"/>' for x,y in pts) + lbl + '</svg>')

def regua(k, fam):
    g1, td = DATA[k]['G1_0.7Hz'], td_of(k)
    W = 168
    cx = xg(g1, W); z2, z3 = xg(200,W), xg(300,W)
    tx = td/0.78*W
    return (f'<svg class="rg" viewBox="0 0 {W+64} 30"><line x1="0" y1="8" x2="{W}" y2="8" class="rg-tr"/>'
            f'<line x1="{z2:.1f}" y1="4" x2="{z2:.1f}" y2="12" class="rg-tick"/><line x1="{z3:.1f}" y1="4" x2="{z3:.1f}" y2="12" class="rg-tick"/>'
            f'<circle cx="{cx:.1f}" cy="8" r="5" fill="var(--fam-{fam})" class="rg-dot"/><text x="{W+6}" y="11" class="rg-lb">G′ {br0(g1)}</text>'
            f'<line x1="0" y1="24" x2="{W}" y2="24" class="rg-tr"/>'
            f'<line x1="{0.15/0.78*W:.1f}" y1="20" x2="{0.15/0.78*W:.1f}" y2="28" class="rg-tick"/>'
            f'<line x1="{0.30/0.78*W:.1f}" y1="20" x2="{0.30/0.78*W:.1f}" y2="28" class="rg-tick"/>'
            f'<circle cx="{tx:.1f}" cy="24" r="5" fill="var(--fam-{fam})" class="rg-dot"/><text x="{W+6}" y="27" class="rg-lb">tanδ {br(td)}</text></svg>')

def card(p):
    k = p['k']; d = DATA[k]; fam = FAMVAR[p['c']]
    g1,g2,eta = d['G1_0.7Hz'], d['G2_0.7Hz'], d['eta_0.7Hz']; td = td_of(k)
    flags = p.get('fl', [])
    fh = '<p class="flags">' + ' · '.join(html.escape(FLAGTXT[x]) for x in flags) + '</p>' if flags else ''
    ind = ''.join(f'<span class="pill {NIVEL[n][1]}">{html.escape(r)}<i>{NIVEL[n][0]}</i></span>' for r,n in p['ind'])
    ev = ' · '.join(html.escape(e) for e in p['ev'])
    lote = d['lote'] if d['lote'] not in ('','N/D') else '—'
    tech = f'<p class="tech"><span class="lbl">Fabricante*</span>{html.escape(p["t"].rstrip("*"))}</p>' if p.get('t') and p['t'] not in ('—*',) else ''
    return f'''<article class="card fam-{fam}" id="{slug(k)}">
<header><div class="c-title">{chips_html(FAMCHIPS[p['c']])}<h4>{html.escape(k)}</h4></div>
<div class="c-right"><span class="marca">{html.escape(p['m'])}</span><span class="famtag" style="color:var(--fam-{fam})">{FAMTAG[p['c']]}</span></div></header>
<div class="vis">{radar(k, fam)}
<div class="vis-col"><div class="sig"><span>G′ <b>{br(g1)}</b> Pa</span><span>G″ <b>{br(g2)}</b> Pa</span><span>tan δ <b>{br(td)}</b></span><span>η* <b>{br(eta)}</b> Pa·s</span></div>
{regua(k, fam)}<span class="lote">lote {html.escape(lote)}</span></div></div>
<p class="comp">{html.escape(p['comp'])}</p>
<p class="mp"><span class="lbl">Melhor para</span>{html.escape(p['mp'])}</p>
<div class="indwrap"><span class="lbl">Indicações</span><div class="pills">{ind}</div></div>
<p class="evite"><span class="lbl lbl-ev">Evite / não priorize</span>{ev}</p>
<p class="escolha" style="border-color:var(--fam-{fam})">{html.escape(p['esc'])}</p>
<p class="alts"><span class="lbl">Alternativas</span>{html.escape(p['alt'])}</p>
{tech}{fh}</article>'''

# ---------- gráficos ----------
def dot(x,y,fam,k,val,extra=''):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" class="dot" fill="var(--fam-{fam})" '
            f'data-n="{html.escape(k,quote=True)}" data-v="{html.escape(val,quote=True)}"{extra}>'
            f'<title>{html.escape(k)} — {html.escape(val)}</title></circle>')

def scatter_main():
    W,H,mL,mB,mT,mR = 860,470,52,40,16,120
    pw,ph = W-mL-mR, H-mT-mB
    def Y(t): return mT + ph - t/0.78*ph
    s=[f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="Mapa da Reologia">']
    for a,b,cls in [(30,200,'za'),(200,300,'zm'),(300,1000,'zr')]:
        x1,x2 = mL+xg(a,pw), mL+xg(b,pw)
        s.append(f'<rect x="{x1:.1f}" y="{mT}" width="{x2-x1:.1f}" height="{ph}" class="{cls}"/>')
    for gv in (50,100,200,300,500,1000):
        x = mL+xg(gv,pw)
        s.append(f'<line x1="{x:.1f}" y1="{mT}" x2="{x:.1f}" y2="{mT+ph}" class="grid"/><text x="{x:.1f}" y="{H-14}" class="ax" text-anchor="middle">{gv}</text>')
    for tv in [i/10 for i in range(8)]:
        s.append(f'<line x1="{mL}" y1="{Y(tv):.1f}" x2="{mL+pw}" y2="{Y(tv):.1f}" class="grid"/><text x="{mL-8}" y="{Y(tv)+3.5:.1f}" class="ax" text-anchor="end">{br(tv,1)}</text>')
    s.append(f'<text x="{mL+pw/2}" y="{H-1}" class="axt" text-anchor="middle">G′ a 0,7 Hz (Pa · escala log)</text>')
    s.append(f'<text x="14" y="{mT+ph/2}" class="axt" text-anchor="middle" transform="rotate(-90 14 {mT+ph/2})">tan δ a 0,7 Hz</text>')
    s.append(f'<text x="{mL+xg(80,pw):.1f}" y="{mT+14}" class="zlb">LINHA BAIXA · integra</text>')
    s.append(f'<text x="{mL+xg(244,pw):.1f}" y="{mT+14}" class="zlb" text-anchor="middle">INTERMEDIÁRIA</text>')
    s.append(f'<text x="{mL+xg(560,pw):.1f}" y="{mT+14}" class="zlb" text-anchor="middle">LINHA ALTA · sustenta/projeta</text>')
    seen={}; pts=[]
    for p in ed.PRODUTOS:
        k=p['k']; g1, td = DATA[k]['G1_0.7Hz'], td_of(k)
        key=(round(g1,2),round(td,2)); off=seen.get(key,0); seen[key]=off+1
        pts.append((mL+xg(g1,pw)+off*5, Y(td), p, g1, td))
    for x,y,p,g1,td in pts:
        s.append(dot(x,y,FAMVAR[p['c']],p['k'],f'G′ {br(g1)} Pa · tan δ {br(td)}'))
    LB={'Belotero Balance Lido':('Balance',0,-9,'middle'),'Juvéderm Skinvive':('Skinvive',0,-9,'middle'),
        'Restylane Refyne Lido':('Refyne',0,-9,'middle'),'Restylane Kysse Lido':('Kysse',0,15,'middle'),
        'Juvéderm Volux':('Volux',0,15,'middle'),'Restylane Shaype Lido':('Shaype',0,-9,'middle'),
        'Hyafilia V Plus Lido':('Hyafilia V',-9,3.5,'end'),'Restylane Lyft Lido':('Lyft',0,-9,'middle'),
        'Yvoire Contour+ Lido':('Yvoire Contour+',9,3.5,'start'),'Rennova Lips Plus Lido':('Lips Plus',0,-9,'middle'),
        'Restylane Lido (lote 27003)':('Restylane (27003)',9,3.5,'start'),'Restylane Skinbooster Lido':('Skinbooster',-9,3.5,'end')}
    for x,y,p,g1,td in pts:
        if p['k'] in LB:
            t,dx,dy,anc = LB[p['k']]
            s.append(f'<text x="{x+dx:.1f}" y="{y+dy:.1f}" class="dlb" text-anchor="{anc}">{html.escape(t)}</text>')
    s.append('</svg>')
    return ''.join(s)

def scatter_gg():
    """G″ × G′ log-log com retas de tan δ constante."""
    W,H,mL,mB,mT,mR = 860,470,56,40,16,24
    pw,ph = W-mL-mR, H-mT-mB
    YA,YB = math.log10(10), math.log10(260)
    def X(g): return mL + xg(g,pw)
    def Y(g2): return mT + ph - (math.log10(g2)-YA)/(YB-YA)*ph
    s=[f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="G duplo-prima por G prima">']
    for gv in (50,100,200,300,500,1000):
        s.append(f'<line x1="{X(gv):.1f}" y1="{mT}" x2="{X(gv):.1f}" y2="{mT+ph}" class="grid"/><text x="{X(gv):.1f}" y="{H-14}" class="ax" text-anchor="middle">{gv}</text>')
    for gv in (10,20,50,100,200):
        s.append(f'<line x1="{mL}" y1="{Y(gv):.1f}" x2="{mL+pw}" y2="{Y(gv):.1f}" class="grid"/><text x="{mL-8}" y="{Y(gv)+3.5:.1f}" class="ax" text-anchor="end">{gv}</text>')
    # iso tan δ
    for t in (0.07,0.1,0.2,0.4,0.7):
        p1g, p2g = 30, 1000
        g2a, g2b = t*p1g, t*p2g
        xa,ya = X(p1g), Y(max(g2a,10))
        if g2a < 10: xa = X(10/t); ya = Y(10)
        xb,yb = X(p2g), Y(min(g2b,260))
        if g2b > 260: xb = X(260/t); yb = Y(260)
        s.append(f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" class="iso"/>')
        lx,ly = xb, yb
        anch = 'start' if lx < mL+pw-4 else 'end'
        s.append(f'<text x="{lx+(4 if anch=="start" else -3):.1f}" y="{ly-4:.1f}" class="isolb" text-anchor="{anch}">tan δ {br(t,2 if t!=0.07 else 2)}</text>')
    s.append(f'<text x="{mL+pw/2}" y="{H-1}" class="axt" text-anchor="middle">G′ a 0,7 Hz (Pa · log)</text>')
    s.append(f'<text x="14" y="{mT+ph/2}" class="axt" text-anchor="middle" transform="rotate(-90 14 {mT+ph/2})">G″ a 0,7 Hz (Pa · log)</text>')
    for p in ed.PRODUTOS:
        k=p['k']; g1,g2 = DATA[k]['G1_0.7Hz'], DATA[k]['G2_0.7Hz']
        s.append(dot(X(g1),Y(g2),FAMVAR[p['c']],k,f'G′ {br(g1)} · G″ {br(g2)} · tan δ {br(td_of(k))}'))
    for k,t,dx,dy,anc in [('Restylane Lido (lote 27003)','Restylane (27003)',-9,3.5,'end'),('Restylane Skinbooster Lido','Skinbooster',-9,3.5,'end'),
                          ('Juvéderm Volux','Volux',0,15,'middle'),('Restylane Defyne Lido','Defyne',0,15,'middle'),
                          ('Belotero Balance Lido','Balance',9,3.5,'start'),('Restylane Shaype Lido','Shaype',0,-9,'middle'),
                          ('Rennova Lift Plus Lido','Lift Plus',0,15,'middle'),('Juvéderm Skinvive','Skinvive',0,-9,'middle')]:
        g1,g2 = DATA[k]['G1_0.7Hz'], DATA[k]['G2_0.7Hz']
        s.append(f'<text x="{X(g1)+dx:.1f}" y="{Y(g2)+dy:.1f}" class="dlb" text-anchor="{anc}">{t}</text>')
    s.append('</svg>')
    return ''.join(s)

def scatter_eta():
    """η* em repouso (0,01 Hz) × G′ 0,7 Hz — permanência."""
    W,H,mL,mB,mT,mR = 860,470,64,40,16,24
    pw,ph = W-mL-mR, H-mT-mB
    YA,YB = math.log10(140), math.log10(13000)
    def X(g): return mL + xg(g,pw)
    def Y(e): return mT + ph - (math.log10(e)-YA)/(YB-YA)*ph
    s=[f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="Viscosidade em repouso por G prima">']
    for gv in (50,100,200,300,500,1000):
        s.append(f'<line x1="{X(gv):.1f}" y1="{mT}" x2="{X(gv):.1f}" y2="{mT+ph}" class="grid"/><text x="{X(gv):.1f}" y="{H-14}" class="ax" text-anchor="middle">{gv}</text>')
    for ev in (200,500,1000,2000,5000,10000):
        s.append(f'<line x1="{mL}" y1="{Y(ev):.1f}" x2="{mL+pw}" y2="{Y(ev):.1f}" class="grid"/><text x="{mL-8}" y="{Y(ev)+3.5:.1f}" class="ax" text-anchor="end">{br0(ev)}</text>')
    s.append(f'<text x="{mL+pw/2}" y="{H-1}" class="axt" text-anchor="middle">G′ a 0,7 Hz (Pa · log)</text>')
    s.append(f'<text x="14" y="{mT+ph/2}" class="axt" text-anchor="middle" transform="rotate(-90 14 {mT+ph/2})">η* em repouso (Pa·s · log)</text>')
    for p in ed.PRODUTOS:
        k=p['k']; g1,e = DATA[k]['G1_0.7Hz'], DATA[k]['eta_0.01Hz']
        s.append(dot(X(g1),Y(e),FAMVAR[p['c']],k,f'G′ {br(g1)} Pa · η* repouso {br0(e)} Pa·s'))
    for k,t,dx,dy,anc in [('Restylane Shaype Lido','Shaype',0,-9,'middle'),('Hyafilia V Plus Lido','Hyafilia V',-9,3.5,'end'),
                          ('Belotero Balance Lido','Balance',9,3.5,'start'),('Juvéderm Skinvive','Skinvive',9,3.5,'start'),
                          ('Restylane Lyft Lido','Lyft',9,3.5,'start'),('Juvéderm Volux','Volux',-9,3.5,'end'),
                          ('Neuramis Lido','Neuramis',0,-9,'middle')]:
        g1,e = DATA[k]['G1_0.7Hz'], DATA[k]['eta_0.01Hz']
        s.append(f'<text x="{X(g1)+dx:.1f}" y="{Y(e)+dy:.1f}" class="dlb" text-anchor="{anc}">{t}</text>')
    s.append('</svg>')
    return ''.join(s)

def ranking(metric, title_axis, maxv, fmt, grids, unit=''):
    rows = sorted(ed.PRODUTOS, key=lambda p: (DATA[p['k']]['G1_0.7Hz'] if metric=='g1' else td_of(p['k'])), reverse=True)
    rh, gap, mT, mB, mL, mR = 13, 2.6, 8, 30, 196, 58
    W = 860; ph = len(rows)*(rh+gap)
    H = mT + ph + mB; pw = W-mL-mR
    def val(p): return DATA[p['k']]['G1_0.7Hz'] if metric=='g1' else td_of(p['k'])
    s=[f'<svg class="chart chart-rank" viewBox="0 0 {W} {H}" role="img" aria-label="ranking">']
    for gv in grids:
        x = mL + gv/maxv*pw
        s.append(f'<line x1="{x:.1f}" y1="{mT}" x2="{x:.1f}" y2="{mT+ph}" class="grid"/><text x="{x:.1f}" y="{H-12}" class="ax" text-anchor="middle">{fmt(gv)}</text>')
    y = mT
    for p in rows:
        k=p['k']; v=val(p); bw = v/maxv*pw; fam=FAMVAR[p['c']]
        s.append(f'<text x="{mL-6}" y="{y+rh-3}" class="bn" text-anchor="end">{html.escape(short(k))}</text>')
        s.append(f'<rect x="{mL}" y="{y}" width="{max(bw,2):.1f}" height="{rh}" rx="3.5" fill="var(--fam-{fam})" class="bar"><title>{html.escape(k)} — {fmt(v)}{unit}</title></rect>')
        s.append(f'<text x="{mL+bw+5:.1f}" y="{y+rh-3}" class="bv">{fmt(v)}</text>')
        y += rh+gap
    s.append(f'<text x="{mL+pw/2}" y="{H-1}" class="axt" text-anchor="middle">{title_axis}</text></svg>')
    return ''.join(s)

# ---------- montar seções ----------
LINHAS = [
 ('baixa','A','LINHA BAIXA','a','CAPÍTULO 6 · G′ &lt; 200 Pa — ESPALHA + ACOMPANHA',
  'Integração, naturalidade, baixo relevo, movimento. É a maior linha do banco: escolha padrão para lábios dinâmicos, perioral, terço superior e depressões rasas.'),
 ('intermediaria','M','LINHA INTERMEDIÁRIA','m','CAPÍTULO 7 · G′ 200–300 Pa — PREENCHE',
  'Corpo e equilíbrio: "o amarelo é a cor do VALE". Sulcos bem marcados, volumização moderada, sustentação sem vértice.'),
 ('alta',('R','RV'),'LINHA ALTA','r','CAPÍTULO 8 · G′ ≥ 300 Pa — SUSTENTA / PROJETA / MOLDA',
  'Estrutura, projeção e manutenção de forma. Dois comportamentos convivem aqui: os ESTRUTURAIS puros (🟣) e os ESTRUTURAIS MALEÁVEIS (🟣+🟢), que aceitam modelagem. Apenas 2 dos 76 são "roxo completo".'),
]
fam_secs=[]
for anchor, cc, nome, var, sub, desc in LINHAS:
    prods = [p for p in ed.PRODUTOS if (p['c'] in cc if isinstance(cc,tuple) else p['c']==cc)]
    prods.sort(key=lambda p: DATA[p['k']]['G1_0.7Hz'])
    cards = '\n'.join(card(p) for p in prods)
    gmin,gmax = DATA[prods[0]['k']]['G1_0.7Hz'], DATA[prods[-1]['k']]['G1_0.7Hz']
    extra = ''
    if anchor=='alta':
        extra = f'<p class="famdesc" style="margin-top:.3rem"><span class="chip" style="width:11px;height:11px;background:var(--fam-r)"></span> estrutural ({sum(1 for p in prods if p["c"]=="R")}) · <span class="chip" style="width:11px;height:11px;background:var(--fam-r)"></span><span class="chip" style="width:11px;height:11px;background:var(--fam-v)"></span> estrutural maleável ({sum(1 for p in prods if p["c"]=="RV")}) · caso de borda: Restylane Defyne (292,62 Pa) mantido aqui conforme o mapa do autor</p>'
    fam_secs.append(f'''<section class="famsec" id="linha-{anchor}">
<div class="fambanner bn-{var}"><div><p class="fam-eyebrow">{sub}</p><h2>{nome}</h2></div>
<div><p class="famdesc">{desc}</p>{extra}<p class="famdesc" style="margin-top:.3rem"><b>{len(prods)} produtos</b> · G′ de {br(gmin)} a {br(gmax)} Pa</p></div></div>
<div class="grid2">{cards}</div></section>''')

# ---------- capítulo BAIXO SWELLING FACTOR ----------
SF = [
 ('Yvoire Contour+ Lido','1ª escolha do autor para olheiras: G′ alto (580 Pa) com baixa expansão declarada — "projeção com precisão volumétrica". Plano subcutâneo superficial na técnica do autor.'),
 ('Perfectha Subskin','1ª escolha da classe: precisão + projeção + baixa expansão. Bifásico com partícula grande; previsibilidade volumétrica infraorbitária.'),
 ('Restylane Lyft Lido','Projeção com pouco volume e precisão (NASHA). Corrige a olheira estrutural sem depender de hidratação do gel.'),
 ('Juvéderm Voluma Lido','Citado na classe SF do mapa: convexidade com precisão em pacientes selecionados (Vycross).'),
 ('Up Contour Lido','Membro complementar citado na classe: contorno de precisão em plano profundo.'),
 ('Rennova Fill Eyes Lines Lido','Caminho oposto na mesma região: gel dinâmico dedicado ao periorbicular (1ª da linha Rennova) — SF igualmente não medido; monitorar edema.'),
]
sf_cards=[]
for k, why in SF:
    p = next(q for q in ed.PRODUTOS if q['k']==k); fam=FAMVAR[p['c']]; d=DATA[k]
    sf_cards.append(f'''<article class="sfcard"><header>{chips_html(['s'],12)}<h4>{html.escape(k)}</h4><span class="marca">{html.escape(p['m'])}</span></header>
<div class="sfnum"><span>G′ <b>{br(d['G1_0.7Hz'])}</b> Pa</span><span>tan δ <b>{br(td_of(k))}</b></span>{radar(k,fam,72,'radar radar-sm')}</div>
<p>{html.escape(why)}</p><a class="sflink" href="#{slug(k)}">ver ficha completa ↓</a></article>''')
sf_sec = f'''<section class="famsec" id="linha-sf">
<div class="fambanner bn-s"><div><p class="fam-eyebrow">CAPÍTULO 9 · 💧 CLASSE CLÍNICA TRANSVERSAL — OLHEIRAS E PRECISÃO</p><h2>LINHA BAIXO SWELLING FACTOR</h2></div>
<div><p class="famdesc">A 3ª classe do Mapa: <b>"quando poucos décimos de mililitro de expansão podem mudar o resultado"</b>. Não é uma faixa de G′ — seus membros vêm das outras linhas e entram por comportamento hídrico declarado/clínico. Regra do autor: <i>nunca escolher olheira pelo G′</i>; concentração ideal ~20 mg/mL; "o tamanho da partícula ajuda a explicar — o SF medido é o que confirma".</p>
<p class="famdesc" style="margin-top:.3rem"><b>⚠ SF ainda NÃO foi medido em nenhum produto</b> — é a prioridade da 2ª rodada laboratorial. Até lá, esta classe é clínico-declarativa (💧).</p></div></div>
<div class="grid3">{''.join(sf_cards)}</div></section>'''

# ---------- emblema da capa (4 assinaturas sobrepostas) ----------
def emblema(size=200):
    c=size/2; R=c-16
    polys=[]
    for k,fam in [('Belotero Balance Lido','a'),('Saypha Volume Lido','m'),('Juvéderm Volux','r'),('Restylane Lido (lote 22647)','v')]:
        v=RK[k]; pts=[]
        for met,ang in [('g1',-90),('g2',0),('td',90),('eta',180)]:
            rad=6+v[met]*(R-6); a=math.radians(ang)
            pts.append(f'{c+rad*math.cos(a):.1f},{c+rad*math.sin(a):.1f}')
        polys.append(f'<polygon points="{" ".join(pts)}" fill="var(--fam-{fam})" fill-opacity=".17" stroke="var(--fam-{fam})" stroke-width="2.2" stroke-linejoin="round"/>')
    grid=''.join(f'<polygon points="{" ".join(f"{c+r*math.cos(math.radians(a)):.1f},{c+r*math.sin(math.radians(a)):.1f}" for a in (-90,0,90,180))}" class="rd-grid"/>'
                 for r in (6+(R-6)/3, 6+2*(R-6)/3, R))
    axes=f'<line x1="{c}" y1="{c-R}" x2="{c}" y2="{c+R}" class="rd-ax"/><line x1="{c-R}" y1="{c}" x2="{c+R}" y2="{c}" class="rd-ax"/>'
    lbl=(f'<text x="{c}" y="11" class="rd-lb" text-anchor="middle">G′</text>'
         f'<text x="{size-3}" y="{c+3.5}" class="rd-lb" text-anchor="end">G″</text>'
         f'<text x="{c}" y="{size-3}" class="rd-lb" text-anchor="middle">tan δ</text>'
         f'<text x="3" y="{c+3.5}" class="rd-lb">η*</text>')
    return f'<svg class="capa-emb" viewBox="0 0 {size} {size}" role="img" aria-label="assinaturas reológicas das quatro linhas">{grid}{axes}{"".join(polys)}{lbl}</svg>'

# ---------- radar didático ----------
def radar_demo(k, cap):
    p = next(q for q in ed.PRODUTOS if q['k']==k)
    return f'<figure class="rdemo">{radar(k, FAMVAR[p["c"]], 150, "radar radar-lg")}<figcaption><b>{html.escape(short(k))}</b><br>{cap}</figcaption></figure>'
radar_sec = f'''<section id="forma">
<p class="cap-eyebrow">Capítulo 4</p><h2>A forma do gel — o radar de 4 eixos</h2>
<p class="lead">Cada produto tem uma <b>forma geométrica</b> construída com as 4 características medidas: <b>G′</b> (cima), <b>G″</b> (direita), <b>tan δ</b> (baixo) e <b>η*</b> (esquerda). Cada eixo mostra a <b>posição do produto entre os 76</b> (percentil do banco, a 0,7 Hz): quanto mais longe do centro, mais alto o valor em relação aos demais. A forma é a impressão digital reológica do gel — produtos da mesma família desenham silhuetas parecidas.</p>
<div class="rdemos">
{radar_demo('Belotero Balance Lido','Pipa para BAIXO: tan δ domina — gel dissipativo, espalha e acompanha.')}
{radar_demo('Juvéderm Skinvive','Baixo + direita: dissipação com G″ proporcional alto — trata a superfície.')}
{radar_demo('Juvéderm Volux','Seta para CIMA-ESQUERDA: G′ e η* máximos com tan δ mínimo — vértice puro.')}
{radar_demo('Restylane Lido (lote 22647)','Losango CHEIO: alto em tudo — estrutura com dissipação (maleável).')}
</div>
<p class="lead" style="font-size:.92rem">Como ler: <b>seta para cima-esquerda</b> = estrutura e permanência · <b>pipa para baixo</b> = integração e movimento · <b>losango largo</b> = magnitude com equilíbrio viscoelástico · <b>forma pequena</b> = gel leve em todas as dimensões.</p>
</section>'''

reg_rows=''.join(f'<tr><td><b>{html.escape(r)}</b></td><td>{html.escape(c)}</td><td>{html.escape(p)}</td><td class="obs">{html.escape(o)}</td></tr>'
                 for r,c,p,o in ed.REGIOES)
marcas={}
for p in ed.PRODUTOS:
    marcas.setdefault(p['m'].split('·')[0].strip(), []).append(p)
idx=''.join('<div class="ixm"><b>'+html.escape(m)+'</b>'+''.join(
    f'<a href="#{slug(q["k"])}"><span class="chip" style="width:9px;height:9px;background:{CHIP[FAMVAR[q["c"]]]}"></span>{html.escape(short(q["k"]))}</a>'
    for q in sorted(ps,key=lambda q:DATA[q['k']]['G1_0.7Hz']))+'</div>' for m,ps in sorted(marcas.items()))

LEGEND = '''<div class="legend">
<span><i style="background:var(--fam-a)"></i>Linha baixa — integrativo dinâmico (34)</span>
<span><i style="background:var(--fam-m)"></i>Linha intermediária — preenchedor (14)</span>
<span><i style="background:var(--fam-r)"></i>Linha alta — estrutural (18)</span>
<span><i style="background:var(--fam-v)"></i>Linha alta — estrutural maleável (10)</span>
</div>'''

page = f'''<title>eBook Reology Map</title>
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
.pill,.lbl,.marca,.legend,.stat span,.famdesc,.fam-eyebrow,.sflink,.evite,.alts,.tech,.flags,.sfnum{{font-family:'Source Sans 3',system-ui,sans-serif}}
.cap-eyebrow{{font-family:'JetBrains Mono',monospace;font-size:.68rem;letter-spacing:.24em;text-transform:uppercase;color:var(--accent-ink);margin:0 0 .25rem}}
main{{max-width:78rem;margin:0 auto;padding:2rem 1.2rem 5rem}}
a{{color:var(--accent-ink)}} a:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.chip{{display:inline-block;border-radius:50%;border:1.5px solid rgba(0,0,0,.16);margin-right:4px;vertical-align:-1px}}
h1,h2,h3{{font-family:'Fraunces',Georgia,serif;text-wrap:balance;line-height:1.08}}
.capa{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1.4rem;margin-bottom:1.4rem}}
.capa-frame{{position:relative;border:2px solid var(--ink);padding:2.8rem 1.6rem 2rem;text-align:center}}
.capa-frame::after{{content:"";position:absolute;inset:7px;border:1px solid color-mix(in srgb,var(--ink) 45%,transparent);pointer-events:none}}
.capa-frame p{{max-width:none}}
.capa-top{{font-family:'JetBrains Mono',monospace;font-size:.72rem;letter-spacing:.3em;text-transform:uppercase;color:var(--ink2);margin:0}}
.capa-rule{{border:0;border-top:1px solid var(--ink3);width:130px;margin:1.15rem auto}}
.capa-rule.sm{{width:70px;margin:.9rem auto}}
.capa h1{{font-size:clamp(2.3rem,5.6vw,3.7rem);font-weight:900;margin:.2rem 0 .7rem;letter-spacing:-.01em}}
.capa .sub{{font-family:'Fraunces',serif;font-style:italic;font-size:clamp(1rem,2.2vw,1.25rem);color:var(--ink2);margin:0 auto 1.4rem;max-width:38ch}}
.capa-emb{{width:min(200px,52vw);height:auto;margin:0 auto;display:block}}
.capa-autor{{font-family:'Fraunces',serif;font-weight:600;font-size:1.35rem;margin:1.2rem 0 0}}
.capa-imprint{{font-family:'Source Sans 3',sans-serif;font-size:.82rem;letter-spacing:.18em;text-transform:uppercase;color:var(--ink2);margin:.4rem 0 0}}
.capa-band{{height:9px;margin-top:1.4rem;background:linear-gradient(90deg,var(--fam-a) 0 25%,var(--fam-m) 25% 50%,var(--fam-r) 50% 75%,var(--fam-v) 75% 100%)}}
.fichatec{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1rem 1.3rem;margin-bottom:.4rem}}
.fichatec .meta{{display:flex;flex-wrap:wrap;gap:.4rem 1.8rem;color:var(--ink2);font-size:.92rem;margin:0}}
.fichatec .meta b{{color:var(--ink)}}
.stats{{display:flex;flex-wrap:wrap;gap:1rem;margin-top:.9rem}}
.stat{{background:var(--card);border:1px solid var(--line);border-top:4px solid var(--accent);border-radius:8px;padding:.7rem 1.1rem;min-width:8.5rem}}
.stat:nth-child(1){{border-top-color:var(--fam-a)}} .stat:nth-child(2){{border-top-color:var(--fam-m)}}
.stat:nth-child(3){{border-top-color:var(--fam-r)}} .stat:nth-child(4){{border-top-color:var(--fam-v)}}
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
/* radar */
.radar{{flex:none;width:96px;height:96px}}
.radar-sm{{width:72px;height:72px}} .radar-lg{{width:150px;height:150px}}
.rd-grid{{fill:none;stroke:var(--linesoft);stroke-width:1}}
.rd-ax{{stroke:var(--linesoft);stroke-width:1}}
.rd-lb{{fill:var(--ink3);font:600 8.5px 'JetBrains Mono',monospace}}
.radar-lg .rd-lb{{font-size:10px}}
.rdemos{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:1rem;margin:.8rem 0}}
.rdemo{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:.9rem;text-align:center}}
.rdemo figcaption{{font-size:.82rem;color:var(--ink2);margin-top:.4rem}} .rdemo b{{color:var(--ink)}}
/* bandeiras de seção */
.fambanner{{display:flex;flex-wrap:wrap;gap:.6rem 2.5rem;align-items:center;justify-content:space-between;border-radius:10px;padding:1.15rem 1.4rem;margin-bottom:1.1rem;border:1px solid var(--line)}}
.bn-a{{background:linear-gradient(120deg,color-mix(in srgb,var(--fam-a) var(--tint),var(--card)),var(--card) 78%);border-left:8px solid var(--fam-a)}}
.bn-m{{background:linear-gradient(120deg,color-mix(in srgb,var(--fam-m) var(--tint),var(--card)),var(--card) 78%);border-left:8px solid var(--fam-m)}}
.bn-r{{background:linear-gradient(120deg,color-mix(in srgb,var(--fam-r) var(--tint),var(--card)),color-mix(in srgb,var(--fam-v) 8%,var(--card)));border-left:8px solid var(--fam-r)}}
.bn-s{{background:linear-gradient(120deg,var(--sf-soft),var(--card) 78%);border-left:8px solid var(--sf)}}
.fam-eyebrow{{font-family:'JetBrains Mono',monospace;font-size:.7rem;letter-spacing:.14em;color:var(--ink2);margin:0 0 .25rem}}
.fambanner h2{{margin:0;font-size:1.7rem}}
.famdesc{{margin:0;color:var(--ink2);font-size:.92rem;max-width:38rem}}
.grid2{{display:grid;grid-template-columns:repeat(auto-fill,minmax(350px,1fr));gap:1rem}}
.grid3{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1rem}}
/* cards */
.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:0 1.1rem 1rem;display:flex;flex-direction:column;gap:.5rem;break-inside:avoid;border-left-width:6px;border-left-style:solid}}
.card.fam-a{{border-left-color:var(--fam-a)}} .card.fam-m{{border-left-color:var(--fam-m)}} .card.fam-r{{border-left-color:var(--fam-r)}}
.card.fam-v{{border-left-color:var(--fam-v);border-image:linear-gradient(180deg,var(--fam-r) 30%,var(--fam-v) 70%) 1;border-left-width:6px}}
.card header{{display:flex;justify-content:space-between;gap:.6rem;align-items:flex-start;margin:0 -1.1rem;padding:.7rem 1.1rem .55rem;border-radius:0 12px 0 0}}
.card.fam-a header{{background:linear-gradient(90deg,color-mix(in srgb,var(--fam-a) var(--tint),transparent),transparent 75%)}}
.card.fam-m header{{background:linear-gradient(90deg,color-mix(in srgb,var(--fam-m) var(--tint),transparent),transparent 75%)}}
.card.fam-r header{{background:linear-gradient(90deg,color-mix(in srgb,var(--fam-r) var(--tint),transparent),transparent 75%)}}
.card.fam-v header{{background:linear-gradient(90deg,color-mix(in srgb,var(--fam-r) 11%,transparent),color-mix(in srgb,var(--fam-v) 11%,transparent) 60%,transparent)}}
.c-title{{display:flex;align-items:baseline;gap:.15rem}}
.card h4{{font-family:'Fraunces',serif;font-size:1.1rem;margin:0;line-height:1.15}}
.c-right{{display:flex;flex-direction:column;align-items:flex-end;gap:.1rem}}
.marca{{font-size:.72rem;color:var(--ink3);white-space:nowrap;letter-spacing:.03em}}
.famtag{{font-family:'JetBrains Mono',monospace;font-size:.6rem;font-weight:700;letter-spacing:.1em;white-space:nowrap}}
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
/* SF cards */
.sfcard{{background:var(--card);border:1px solid var(--line);border-left:6px solid var(--sf);border-radius:10px;padding:.9rem 1rem;display:flex;flex-direction:column;gap:.45rem;break-inside:avoid}}
.sfcard header{{display:flex;align-items:baseline;gap:.3rem;flex-wrap:wrap}}
.sfcard h4{{font-family:'Fraunces',serif;font-size:1.02rem;margin:0}}
.sfcard .marca{{margin-left:auto}}
.sfnum{{display:flex;align-items:center;gap:1rem;font-family:'JetBrains Mono',monospace;font-size:.8rem;color:var(--ink2);background:var(--sf-soft);border-radius:10px;padding:.35rem .7rem}}
.sfnum b{{color:var(--ink)}} .sfnum .radar-sm{{margin-left:auto}}
.sfcard p{{margin:0;font-size:.88rem}}
.sflink{{font-size:.8rem;text-decoration:none;font-weight:600;color:var(--sf)}}
.sflink:hover{{text-decoration:underline}}
/* região / índice */
.regtab{{overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:var(--card)}}
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
@media print{{ body{{background:#fff;font-size:11px}} .famsec,#rankings,#regioes{{break-before:page}}
 .card,.sfcard,.rdemo{{break-inside:avoid;border-color:#ccc}} #tip{{display:none}} .capa{{border:none}} }}
@media(max-width:30rem){{.vis{{flex-direction:column;align-items:flex-start}}}}
</style>
<main>
<header class="capa">
<div class="capa-frame">
<p class="capa-top">Reology Map</p>
<hr class="capa-rule">
<h1>Reologia do<br>Ácido Hialurônico</h1>
<p class="sub">Guia Reológico dos 76 Preenchedores do Mercado Brasileiro</p>
{emblema()}
<p class="capa-autor">Dr. João Pithon</p>
<hr class="capa-rule sm">
<p class="capa-imprint">Primeira edição · São Paulo · 2026</p>
</div>
<div class="capa-band"></div>
</header>

<div class="fichatec">
<p class="meta"><span>Estudo <b>Reológico Pithon Napoli (2026)</b> — 76 géis comerciais sob protocolo único</span><span>Ensaio <b>reômetro rotacional TA Instruments AR-1500ex</b> · 25&nbsp;°C · placas Ø20&nbsp;mm · gap 500&nbsp;µm · varredura 10&nbsp;→&nbsp;0,01&nbsp;Hz</span><span>Frequência de referência <b>0,7&nbsp;Hz</b></span></p>
<div class="stats"><div class="stat"><b>34</b><span>linha baixa (&lt;200 Pa)</span></div><div class="stat"><b>14</b><span>linha intermediária (200–300)</span></div><div class="stat"><b>28</b><span>linha alta (≥300 Pa)</span></div><div class="stat"><b>28×</b><span>amplitude de G′ no banco</span></div></div>
<p class="qt" style="margin:1rem 0 .2rem">“Não existe o melhor preenchedor. Existe a propriedade reológica mais adequada para o comportamento que queremos produzir em cada região.”</p>
</div>

<section id="comoler">
<p class="cap-eyebrow">Capítulo 1</p><h2>Como ler este guia</h2>
<div class="box">
<p style="margin-top:0">Os 76 géis estão organizados em <b>quatro linhas</b>: <b style="color:var(--fam-a)">LINHA BAIXA</b> (G′ &lt; 200 Pa), <b style="color:var(--fam-m)">LINHA INTERMEDIÁRIA</b> (200–300 Pa), <b style="color:var(--fam-r)">LINHA ALTA</b> (≥ 300 Pa — incluindo os <b style="color:var(--fam-v)">estruturais maleáveis</b>) e a classe clínica transversal <b style="color:var(--sf)">💧 BAIXO SWELLING FACTOR</b>. <i>“A COR CLASSIFICA. O NÚMERO POSICIONA.”</i></p>
<p>Cada ficha traz: a <b>forma do gel</b> (radar de 4 eixos — G′, G″, tan δ, η*, em percentil do banco), a <b>assinatura numérica a 0,7 Hz</b> (laudo do estudo) com lote, as <b>réguas de posição</b> (marcas nos cortes 200/300 Pa e tan δ 0,15/0,30), leitura clínica e indicações do autor.</p>
<p><b>Níveis de indicação:</b> <span class="pill n1">região<i>1ª escolha</i></span> <span class="pill n2">região<i>forte</i></span> <span class="pill n3">região<i>boa</i></span> <span class="pill n4">região<i>seletiva</i></span></p>
<p style="margin-bottom:0"><b>Regra das três fontes:</b> números reológicos = exclusivamente do laudo laboratorial do estudo; dados com <b>*</b> = declarados pelo fabricante; <b>coesividade, SF, extrusão e Strain X não foram medidos</b> (💧) e nunca são deduzidos. <b>Sinalizações:</b> <span style="color:var(--flag);font-weight:600">⚑ dado em re-verificação</span> · ◌ monografia pendente · ※ contraindicação de bula. <b>Segurança:</b> reologia não é segurança vascular.</p>
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
<p class="cap-eyebrow">Capítulo 3</p><h2>O Mapa da Reologia — 76 produtos em um plano</h2>
<p class="lead">Cada ponto é um gel ensaiado (0,7&nbsp;Hz). As faixas coloridas são as três linhas (cortes de 200 e 300&nbsp;Pa); a altura é o caráter dinâmico (tan δ). Passe o mouse/toque para identificar.</p>
{scatter_main()}
{LEGEND}
<p class="lead" style="font-size:.9rem">Achados: apenas <b>2 dos 76</b> são “roxo completo” (Hyafilia V e Shaype); os pares sobrepostos (Volift=Voluma, Belotero Volume+=Neauvia Intense, Stimulate=Singderm) estão em re-verificação; famílias comerciais inteiras vivem numa mesma zona — a cor classifica, o número posiciona.</p>
</section>

{radar_sec}

<section id="atlas">
<p class="cap-eyebrow">Capítulo 5</p><h2>Atlas de gráficos — todas as variáveis</h2>
<h3>G″ × G′ — a dissipação em magnitude (tan δ vira inclinação)</h3>
<p class="lead">Nas escalas log, as retas tracejadas são valores constantes de tan δ: produtos sobre a mesma reta têm a mesma <i>proporção</i> dissipativa, ainda que magnitudes muito diferentes. Veja Defyne e Volux colados na reta de 0,07–0,08, e o braço NASHA (Restylane clássico, Skinbooster) subindo à direita com G″ altíssimo.</p>
{scatter_gg()}
{LEGEND}
<h3>Permanência em repouso — η* a 0,01 Hz × G′ a 0,7 Hz</h3>
<p class="lead">O quanto o gel resiste a fluir quando a face está parada. A tendência acompanha o G′ — mas os desvios contam histórias: Skinvive despenca (vira líquido em repouso) e os NASHA de G″ alto ficam acima da vizinhança.</p>
{scatter_eta()}
{LEGEND}
</section>

{fam_secs[0]}
{fam_secs[1]}
{fam_secs[2]}
{sf_sec}

<section id="rankings">
<p class="cap-eyebrow">Capítulo 10</p><h2>Rankings completos — os 76 lado a lado</h2>
<h3>G′ a 0,7 Hz (Pa) — a espinha estrutural do banco</h3>
{ranking('g1','G′ a 0,7 Hz (Pa)',960,br0,(0,200,300,500,750),' Pa')}
<h3>tan δ a 0,7 Hz — o eixo do movimento</h3>
{ranking('td','tan δ a 0,7 Hz',0.72,lambda v: br(v,2),(0,0.15,0.30,0.50,0.70))}
</section>

<section id="regioes">
<p class="cap-eyebrow">Capítulo 11</p><h2>Guia rápido por região</h2>
<p class="lead">Síntese do mapeamento região → necessidade reológica → produtos citados nas monografias. Uma região pode pertencer a mais de uma classe conforme o objetivo (corpo do mento ≠ vértice do mento).</p>
<div class="regtab"><table><thead><tr><th>Região</th><th>Necessidade</th><th>Produtos (1ª escolha / fortes)</th><th>Observação</th></tr></thead><tbody>{reg_rows}</tbody></table></div>
</section>

<section id="indice">
<p class="cap-eyebrow">Apêndice A</p><h2>Índice por marca</h2>
<div class="ix">{idx}</div>
</section>

<section id="notas">
<p class="cap-eyebrow">Apêndice B</p><h2>Fontes, limitações e aviso</h2>
<div class="box">
<p style="margin-top:0"><b>Fonte dos números:</b> Estudo Reológico Pithon Napoli — laudo laboratorial independente, assinado, de 04/08/2026 (Anexo 2, 0,7 Hz), com lote identificado em cada ficha. Reômetro rotacional TA Instruments AR-1500ex, 25 °C, placas paralelas Ø 20 mm, gap 500 µm, varredura 10 → 0,01 Hz. Comparabilidade é <b>interna ao protocolo</b>; 25 °C in vitro ≠ comportamento in vivo. O radar usa <b>percentil do banco</b> (posição entre os 76), não valor absoluto.</p>
<p><b>Não medidos nesta rodada</b> (prioridade da 2ª rodada): coesividade quantitativa, Swelling Factor, força de extrusão, Strain X/amplitude, compressão. Onde citados, são dados declarados pelo fabricante (*) ou impressão clínica do autor — nunca resultado do ensaio. A LINHA BAIXO SF é, por ora, uma classe clínico-declarativa (💧).</p>
<p><b>Fichas com ⚑</b> aguardam errata/re-verificação laboratorial (pares idênticos, η* divergentes, tan δ do Perfectha Subskin corrigido por recálculo). <b>Fichas com ◌</b> aguardam a monografia do autor.</p>
<p style="margin-bottom:0"><b>Aviso:</b> material educacional para profissionais habilitados; não substitui julgamento clínico, bula/IFU nem treinamento anatômico. Indicações refletem a experiência e a leitura reológica do autor sobre lotes específicos; os fabricantes não participaram nem endossam o estudo. Marcas citadas pertencem aos respectivos titulares.</p>
</div>
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
print('OK',out,len(page)//1024,'KB')
