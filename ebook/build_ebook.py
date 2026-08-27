# -*- coding: utf-8 -*-
"""Gera o eBook de Reologia (HTML artifact) a partir do banco canônico + conteúdo editorial."""
import json, math, html, re, unicodedata
import importlib.util

BASE = '/tmp/claude-0/-home-user-reologia-map/cd216e96-b088-57d1-abe3-2409c365400d/scratchpad'
spec = importlib.util.spec_from_file_location('ebook_data', f'{BASE}/ebook_data.py')
ed = importlib.util.module_from_spec(spec); spec.loader.exec_module(ed)

DATA = {r['produto']: r for r in json.load(open(f'{BASE}/produtos_full.json'))}
assert len(ed.PRODUTOS) == 76, len(ed.PRODUTOS)
for p in ed.PRODUTOS: assert p['k'] in DATA, p['k']

def br(v, nd=2):
    return f'{v:,.{nd}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

def slug(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii','ignore').decode()
    return re.sub(r'[^a-z0-9]+','-', t.lower()).strip('-')

FAM = {
 'A':  dict(nome='Integrativo dinâmico', chips=['a','p'], verbo='ESPALHA + ACOMPANHA', var='a',
            desc='Baixo G′ (< 200 Pa) com caráter dinâmico: espalhamento, integração, baixo relevo, movimento.'),
 'M':  dict(nome='Preenchedor intermediário', chips=['m'], verbo='PREENCHE', var='m',
            desc='G′ intermediário (200–300 Pa): corpo, equilíbrio, o território do VALE.'),
 'R':  dict(nome='Estrutural', chips=['r'], verbo='SUSTENTA / PROJETA', var='r',
            desc='Alto G′ (≥ 300 Pa): estrutura, projeção, manutenção de forma — curvas fortes e vértices.'),
 'RV': dict(nome='Estrutural maleável', chips=['r','v'], verbo='SUSTENTA + MOLDA', var='v',
            desc='Alto G′ com maleabilidade/coesividade declarada: estrutura que aceita modelagem.'),
}
CHIP = dict(a='var(--fam-a)', m='var(--fam-m)', r='var(--fam-r)', v='var(--chip-verde)', p='var(--chip-rosa)')
NIVEL = {1:('1ª escolha','n1'),2:('forte','n2'),3:('boa','n3'),4:('seletiva','n4')}
FLAGTXT = {'verif':'⚑ dado em re-verificação laboratorial','pend':'◌ monografia do autor pendente','ifu':'※ contraindicações de bula listadas'}

X0, X1 = math.log10(30), math.log10(1000)
def xg(g, w): return (math.log10(g)-X0)/(X1-X0)*w
def ytd(t, h): return h - t/0.78*h

def chips_html(keys, size=12):
    return ''.join(f'<span class="chip" style="width:{size}px;height:{size}px;background:{CHIP[k]}"></span>' for k in keys)

def regua(p, fam):
    g1, td = DATA[p['k']]['G1_0.7Hz'], DATA[p['k']]['tand_0.7Hz']
    W, cx = 190, None
    cx = xg(g1, W)
    z200, z300 = xg(200, W), xg(300, W)
    s = [f'<svg class="rg" viewBox="0 0 {W+66} 30" role="img" aria-label="posição de G′ e tan δ">']
    s.append(f'<line x1="0" y1="8" x2="{W}" y2="8" class="rg-tr"/>')
    s.append(f'<line x1="{z200:.1f}" y1="4" x2="{z200:.1f}" y2="12" class="rg-tick"/><line x1="{z300:.1f}" y1="4" x2="{z300:.1f}" y2="12" class="rg-tick"/>')
    s.append(f'<circle cx="{cx:.1f}" cy="8" r="5" fill="var(--fam-{fam})" class="rg-dot"/>')
    s.append(f'<text x="{W+8}" y="11" class="rg-lb">G′ {br(g1)}</text>')
    tx = td/0.78*W
    s.append(f'<line x1="0" y1="24" x2="{W}" y2="24" class="rg-tr"/>')
    for tv in (0.15, 0.30):
        s.append(f'<line x1="{tv/0.78*W:.1f}" y1="20" x2="{tv/0.78*W:.1f}" y2="28" class="rg-tick"/>')
    s.append(f'<circle cx="{tx:.1f}" cy="24" r="5" fill="var(--fam-{fam})" class="rg-dot"/>')
    s.append(f'<text x="{W+8}" y="27" class="rg-lb">tan δ {br(td)}</text>')
    s.append('</svg>')
    return ''.join(s)

def card(p):
    d = DATA[p['k']]; f = FAM[p['c']]
    g1,g2,td,eta = d['G1_0.7Hz'], d['G2_0.7Hz'], d['tand_0.7Hz'], d['eta_0.7Hz']
    if p['k']=='Perfectha Subskin': td = 0.15  # errata da auditoria (G″/G′)
    flags = p.get('fl', [])
    fh = ''
    if flags:
        fh = '<p class="flags">' + ' · '.join(html.escape(FLAGTXT[x]) for x in flags) + '</p>'
    ind = ''.join(f'<span class="pill {NIVEL[n][1]}">{html.escape(r)}<i>{NIVEL[n][0]}</i></span>' for r,n in p['ind'])
    ev = ' · '.join(html.escape(e) for e in p['ev'])
    lote = d['lote'] if d['lote'] not in ('','N/D') else '—'
    return f'''<article class="card" id="{slug(p['k'])}">
<header><div class="c-title">{chips_html(f['chips'])}<h4>{html.escape(p['k'])}</h4></div><span class="marca">{html.escape(p['m'])}</span></header>
<div class="sig"><span class="signum">G′ <b>{br(g1)}</b> Pa</span><span class="signum">G″ <b>{br(g2)}</b> Pa</span><span class="signum">tan δ <b>{br(td)}</b></span><span class="signum">η* <b>{br(eta)}</b> Pa·s</span><span class="lote">lote {html.escape(lote)}</span></div>
{regua(p, f['var'])}
<p class="comp">{html.escape(p['comp'])}</p>
<p class="mp"><span class="lbl">Melhor para</span>{html.escape(p['mp'])}</p>
<div class="indwrap"><span class="lbl">Indicações</span><div class="pills">{ind}</div></div>
<p class="evite"><span class="lbl lbl-ev">Evite / não priorize</span>{ev}</p>
<p class="escolha">{html.escape(p['esc'])}</p>
<p class="alts"><span class="lbl">Alternativas</span>{html.escape(p['alt'])}</p>
{f'<p class="tech"><span class="lbl">Fabricante*</span>{html.escape(p["t"].rstrip("*"))}</p>' if p.get('t') and p['t'] not in ('—*',) else ''}
{fh}</article>'''

def scatter():
    W,H,mL,mB,mT,mR = 860,470,52,40,16,120
    pw,ph = W-mL-mR, H-mT-mB
    s=[f'<svg id="mapa" viewBox="0 0 {W} {H}" role="img" aria-label="Mapa da Reologia: G′ por tan δ, 76 produtos">']
    # zonas de corte (cor-base)
    for a,b,cls in [(30,200,'za'),(200,300,'zm'),(300,1000,'zr')]:
        x1,x2 = mL+xg(a,pw), mL+xg(b,pw)
        s.append(f'<rect x="{x1:.1f}" y="{mT}" width="{x2-x1:.1f}" height="{ph}" class="{cls}"/>')
    # grid + eixos
    for gv in (50,100,200,300,500,1000):
        x = mL+xg(gv,pw)
        s.append(f'<line x1="{x:.1f}" y1="{mT}" x2="{x:.1f}" y2="{mT+ph}" class="grid"/>')
        s.append(f'<text x="{x:.1f}" y="{H-14}" class="ax" text-anchor="middle">{gv}</text>')
    for tv in (0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7):
        y = mT+ytd(tv,ph)
        s.append(f'<line x1="{mL}" y1="{y:.1f}" x2="{mL+pw}" y2="{y:.1f}" class="grid"/>')
        s.append(f'<text x="{mL-8}" y="{y+3.5:.1f}" class="ax" text-anchor="end">{br(tv,1)}</text>')
    s.append(f'<text x="{mL+pw/2}" y="{H-1}" class="axt" text-anchor="middle">G′ a 0,7 Hz (Pa · escala log)</text>')
    s.append(f'<text x="14" y="{mT+ph/2}" class="axt" text-anchor="middle" transform="rotate(-90 14 {mT+ph/2})">tan δ a 0,7 Hz</text>')
    s.append(f'<text x="{mL+xg(80,pw):.1f}" y="{mT+14}" class="zlb">🔵 integra</text>')
    s.append(f'<text x="{mL+xg(244,pw):.1f}" y="{mT+14}" class="zlb" text-anchor="middle">🟡 preenche</text>')
    s.append(f'<text x="{mL+xg(560,pw):.1f}" y="{mT+14}" class="zlb" text-anchor="middle">🟣 sustenta/projeta</text>')
    # pontos (desloca duplicatas exatas)
    seen={}
    LABEL={'Belotero Balance Lido':'Balance','Juvéderm Skinvive':'Skinvive','Restylane Refyne Lido':'Refyne',
           'Restylane Kysse Lido':'Kysse','Juvéderm Volux':'Volux','Restylane Shaype Lido':'Shaype',
           'Hyafilia V Plus Lido':'Hyafilia V','Restylane Lyft Lido':'Lyft','Yvoire Contour+ Lido':'Yvoire Contour+',
           'Rennova Lips Plus Lido':'Lips Plus','Restylane Lido (lote 27003)':'Restylane (27003)','Restylane Skinbooster Lido':'Skinbooster'}
    pts=[]
    for p in ed.PRODUTOS:
        d=DATA[p['k']]; g1,td = d['G1_0.7Hz'], d['tand_0.7Hz']
        if p['k']=='Perfectha Subskin': td=0.15
        key=(round(g1,2),round(td,2)); off = seen.get(key,0); seen[key]=off+1
        x=mL+xg(g1,pw)+off*5; y=mT+ytd(td,ph)
        pts.append((x,y,p,g1,td))
    for x,y,p,g1,td in pts:
        f=FAM[p['c']]['var']
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" class="dot" fill="var(--fam-{f})" data-n="{html.escape(p["k"],quote=True)}" data-v="G′ {br(g1)} Pa · tan δ {br(td)}"><title>{html.escape(p["k"])} — G′ {br(g1)} Pa · tan δ {br(td)}</title></circle>')
    POS = {  # dx, dy, anchor — ajustes anti-colisão
      'Restylane Kysse Lido':(0,15,'middle'), 'Juvéderm Volux':(0,15,'middle'),
      'Restylane Skinbooster Lido':(-9,3.5,'end'), 'Restylane Lido (lote 27003)':(9,3.5,'start'),
      'Hyafilia V Plus Lido':(-9,3.5,'end'), 'Restylane Shaype Lido':(0,-9,'middle'),
      'Yvoire Contour+ Lido':(9,3.5,'start'), 'Restylane Lyft Lido':(0,-9,'middle'),
    }
    for x,y,p,g1,td in pts:
        lb=LABEL.get(p['k'])
        if lb:
            dx,dy,anch = POS.get(p['k'], (0,-9,'middle'))
            s.append(f'<text x="{x+dx:.1f}" y="{y+dy:.1f}" class="dlb" text-anchor="{anch}">{html.escape(lb)}</text>')
    s.append('</svg>')
    return ''.join(s)

# -------------------- montar página --------------------
fam_secs=[]
ORD=['A','M','R','RV']
for c in ORD:
    f=FAM[c]
    prods=[p for p in ed.PRODUTOS if p['c']==c]
    prods.sort(key=lambda p: DATA[p['k']]['G1_0.7Hz'])
    cards='\n'.join(card(p) for p in prods)
    gmin,gmax = DATA[prods[0]['k']]['G1_0.7Hz'], DATA[prods[-1]['k']]['G1_0.7Hz']
    fam_secs.append(f'''<section class="famsec" id="fam-{c.lower()}">
<div class="fambanner" style="border-color:var(--fam-{f['var']})"><div>{chips_html(f['chips'],16)}
<h2>{f['nome']}</h2><p class="famverbo" style="color:var(--fam-{f['var']})">{f['verbo']}</p></div>
<p class="famdesc">{f['desc']}<br><b>{len(prods)} produtos</b> · G′ de {br(gmin)} a {br(gmax)} Pa</p></div>
<div class="grid2">{cards}</div></section>''')

reg_rows=''.join(f'<tr><td><b>{html.escape(r)}</b></td><td>{html.escape(c)}</td><td>{html.escape(p)}</td><td class="obs">{html.escape(o)}</td></tr>'
                 for r,c,p,o in ed.REGIOES)

# índice por marca
marcas={}
for p in ed.PRODUTOS:
    mk = p['m'].split('·')[0].strip()
    marcas.setdefault(mk, []).append(p)
idx=''.join(f'<div class="ixm"><b>{html.escape(m)}</b>' + ''.join(
    f'<a href="#{slug(p["k"])}">{html.escape(p["k"].replace(" Lido","").replace(" lido",""))}</a>' for p in sorted(ps,key=lambda q:DATA[q['k']]['G1_0.7Hz']))
    + '</div>' for m,ps in sorted(marcas.items()))

page = f'''<title>eBook Reology Map</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700;9..144,900&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;600;700&display=swap">
<style>
:root {{
 --bg:#FAF9FC; --card:#FFFFFF; --ink:#1D1A23; --ink2:#554E63; --ink3:#8B849B;
 --line:#E5E1EE; --linesoft:#EFECF6; --accent:#6D3FB4; --accent-ink:#5A2F9E; --accent-soft:#F1EAFB;
 --fam-a:#2E7DBF; --fam-m:#A6801C; --fam-r:#7C3AED; --fam-v:#3E9B6E;
 --chip-verde:#3E9B6E; --chip-rosa:#CE6E9E;
 --warn:#B4572F; --flag:#C64F4F;
 --za:rgba(46,125,191,.055); --zm:rgba(166,128,28,.06); --zr:rgba(124,58,237,.05);
 --n1bg:#6D3FB4; --n1ink:#FFFFFF; --n2bg:#E8DDF8; --n2ink:#4A2B86; --n3bd:#B9A3DE; --n3ink:#5A3F94; --n4ink:#7A7290;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
 --bg:#161320; --card:#1E1A2A; --ink:#ECE9F3; --ink2:#B3ACC6; --ink3:#7E7692;
 --line:#332D44; --linesoft:#2A2439; --accent:#A98BE0; --accent-ink:#BCA3EA; --accent-soft:#2A2140;
 --fam-a:#3F87C4; --fam-m:#B18927; --fam-r:#8E68D8; --fam-v:#43A076;
 --chip-verde:#43A076; --chip-rosa:#C4789F;
 --warn:#D08A5E; --flag:#DC7E7E;
 --za:rgba(63,135,196,.10); --zm:rgba(177,137,39,.10); --zr:rgba(142,104,216,.10);
 --n1bg:#8E68D8; --n1ink:#14101E; --n2bg:#332756; --n2ink:#CBB6F2; --n3bd:#6B549E; --n3ink:#B49BE6; --n4ink:#8F86A8;
}} }}
:root[data-theme="dark"] {{
 --bg:#161320; --card:#1E1A2A; --ink:#ECE9F3; --ink2:#B3ACC6; --ink3:#7E7692;
 --line:#332D44; --linesoft:#2A2439; --accent:#A98BE0; --accent-ink:#BCA3EA; --accent-soft:#2A2140;
 --fam-a:#3F87C4; --fam-m:#B18927; --fam-r:#8E68D8; --fam-v:#43A076;
 --chip-verde:#43A076; --chip-rosa:#C4789F;
 --warn:#D08A5E; --flag:#DC7E7E;
 --za:rgba(63,135,196,.10); --zm:rgba(177,137,39,.10); --zr:rgba(142,104,216,.10);
 --n1bg:#8E68D8; --n1ink:#14101E; --n2bg:#332756; --n2ink:#CBB6F2; --n3bd:#6B549E; --n3ink:#B49BE6; --n4ink:#8F86A8;
}}
*{{box-sizing:border-box}} html{{scroll-behavior:smooth}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:'Source Sans 3',system-ui,sans-serif;font-size:15.5px;line-height:1.55}}
main{{max-width:78rem;margin:0 auto;padding:2rem 1.2rem 5rem}}
a{{color:var(--accent-ink)}}
a:focus-visible,circle:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.chip{{display:inline-block;border-radius:50%;border:1.5px solid rgba(0,0,0,.18);margin-right:4px;vertical-align:-1px}}
h1,h2,h3{{font-family:'Fraunces',Georgia,serif;text-wrap:balance;line-height:1.08}}
/* CAPA */
.capa{{border:1px solid var(--line);border-radius:18px;background:linear-gradient(160deg,var(--accent-soft),var(--card) 55%);padding:3rem 2.4rem;margin-bottom:2rem}}
.capa .eyebrow{{font-family:'JetBrains Mono',monospace;font-size:.72rem;letter-spacing:.24em;text-transform:uppercase;color:var(--accent-ink);margin:0 0 1rem}}
.capa h1{{font-size:clamp(2.1rem,5vw,3.4rem);font-weight:900;margin:0 0 .6rem}}
.capa .sub{{font-family:'Fraunces',serif;font-size:clamp(1.05rem,2.4vw,1.4rem);color:var(--ink2);margin:.2rem 0 1.4rem;max-width:44ch}}
.capa .meta{{display:flex;flex-wrap:wrap;gap:.5rem 1.6rem;color:var(--ink2);font-size:.92rem}}
.capa .meta b{{color:var(--ink)}}
.stats{{display:flex;flex-wrap:wrap;gap:1rem;margin-top:1.6rem}}
.stat{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:.7rem 1.1rem;min-width:8.5rem}}
.stat b{{display:block;font-family:'JetBrains Mono',monospace;font-size:1.35rem;color:var(--accent-ink)}}
.stat span{{font-size:.8rem;color:var(--ink2)}}
/* seções */
section{{margin-top:2.6rem}}
h2{{font-size:1.65rem;font-weight:700;margin:0 0 .8rem}}
h3{{font-size:1.15rem;margin:1.4rem 0 .5rem}}
p{{max-width:76ch}}
.box{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:1.1rem 1.3rem}}
.lead{{color:var(--ink2)}}
.qt{{border-left:3px solid var(--accent);background:var(--accent-soft);border-radius:0 10px 10px 0;padding:.8rem 1.1rem;font-family:'Fraunces',serif;font-size:1.06rem;margin:1rem 0;max-width:70ch}}
/* fundamentos */
.fund{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:.9rem}}
.fund .box b.t{{font-family:'JetBrains Mono',monospace;color:var(--accent-ink);font-size:1.02rem}}
.fund .box p{{margin:.35rem 0 0;font-size:.92rem;color:var(--ink2)}}
.freq{{width:100%;border-collapse:collapse;font-size:.9rem;margin-top:.8rem}}
.freq th,.freq td{{border-bottom:1px solid var(--linesoft);padding:.45rem .6rem;text-align:left}}
.freq th{{font-size:.78rem;letter-spacing:.04em}}
.anti{{columns:2;column-gap:2rem;font-size:.92rem;margin:.4rem 0 0;padding-left:1.1rem}}
.anti li{{margin:.25rem 0;break-inside:avoid}}
@media(max-width:46rem){{.anti{{columns:1}}}}
/* mapa */
#mapa{{width:100%;height:auto;background:var(--card);border:1px solid var(--line);border-radius:14px}}
.grid{{stroke:var(--linesoft);stroke-width:1}}
.za{{fill:var(--za)}} .zm{{fill:var(--zm)}} .zr{{fill:var(--zr)}}
.ax{{fill:var(--ink3);font:11px 'JetBrains Mono',monospace}}
.axt{{fill:var(--ink2);font:600 12px 'Source Sans 3',sans-serif}}
.zlb{{fill:var(--ink3);font:600 11px 'Source Sans 3',sans-serif}}
.dot{{stroke:var(--card);stroke-width:2;cursor:pointer;transition:r .12s}}
.dot:hover{{r:8}}
.dlb{{fill:var(--ink2);font:600 10.5px 'Source Sans 3',sans-serif;paint-order:stroke;stroke:var(--card);stroke-width:3px;stroke-linejoin:round}}
.legend{{display:flex;flex-wrap:wrap;gap:.4rem 1.4rem;margin:.7rem 0 0;font-size:.9rem;color:var(--ink2)}}
.legend span{{display:inline-flex;align-items:center;gap:.4rem}}
.legend i{{width:11px;height:11px;border-radius:50%;display:inline-block}}
#tip{{position:fixed;pointer-events:none;background:var(--ink);color:var(--bg);padding:.35rem .6rem;border-radius:8px;font-size:.8rem;opacity:0;transition:opacity .1s;z-index:9;max-width:260px}}
/* famílias */
.fambanner{{display:flex;flex-wrap:wrap;gap:.6rem 2rem;align-items:end;justify-content:space-between;border-left:6px solid;background:var(--card);border-top:1px solid var(--line);border-right:1px solid var(--line);border-bottom:1px solid var(--line);border-radius:12px;padding:1rem 1.3rem;margin-bottom:1rem}}
.fambanner h2{{display:inline;margin:0 0 0 .3rem;font-size:1.5rem}}
.famverbo{{font-family:'JetBrains Mono',monospace;font-weight:700;letter-spacing:.08em;margin:.3rem 0 0;font-size:.85rem}}
.famdesc{{margin:0;color:var(--ink2);font-size:.92rem;max-width:34rem}}
.grid2{{display:grid;grid-template-columns:repeat(auto-fill,minmax(345px,1fr));gap:1rem}}
/* card */
.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:1rem 1.1rem;display:flex;flex-direction:column;gap:.5rem;break-inside:avoid}}
.card header{{display:flex;justify-content:space-between;gap:.6rem;align-items:baseline}}
.c-title{{display:flex;align-items:baseline;gap:.15rem}}
.card h4{{font-family:'Fraunces',serif;font-size:1.08rem;margin:0;line-height:1.15}}
.marca{{font-size:.72rem;color:var(--ink3);white-space:nowrap;letter-spacing:.03em}}
.sig{{display:flex;flex-wrap:wrap;gap:.3rem .9rem;font-family:'JetBrains Mono',monospace;font-size:.78rem;color:var(--ink2);border-top:1px solid var(--linesoft);border-bottom:1px solid var(--linesoft);padding:.4rem 0}}
.sig b{{color:var(--ink);font-weight:700}}
.lote{{margin-left:auto;color:var(--ink3);font-size:.72rem}}
.rg{{width:100%;max-width:300px;height:auto}}
.rg-tr{{stroke:var(--line);stroke-width:2;stroke-linecap:round}}
.rg-tick{{stroke:var(--ink3);stroke-width:1}}
.rg-dot{{stroke:var(--card);stroke-width:1.5}}
.rg-lb{{fill:var(--ink2);font:600 9.5px 'JetBrains Mono',monospace}}
.comp{{margin:0;font-size:.93rem}}
.lbl{{display:block;font-size:.68rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--ink3);margin-bottom:.15rem}}
.mp{{margin:0;font-weight:600;font-size:.93rem}}
.pills{{display:flex;flex-wrap:wrap;gap:.3rem}}
.pill{{font-size:.78rem;padding:.16rem .55rem;border-radius:999px;line-height:1.25}}
.pill i{{font-style:normal;font-size:.66rem;opacity:.85;margin-left:.35rem;letter-spacing:.04em}}
.n1{{background:var(--n1bg);color:var(--n1ink);font-weight:600}}
.n2{{background:var(--n2bg);color:var(--n2ink);font-weight:600}}
.n3{{border:1.5px solid var(--n3bd);color:var(--n3ink)}}
.n4{{border:1.5px dashed var(--line);color:var(--n4ink)}}
.evite{{margin:0;font-size:.85rem;color:var(--ink2)}}
.lbl-ev{{color:var(--warn)}}
.escolha{{margin:0;border-left:3px solid var(--accent);background:var(--accent-soft);padding:.5rem .7rem;border-radius:0 8px 8px 0;font-size:.9rem;font-style:italic}}
.alts,.tech{{margin:0;font-size:.82rem;color:var(--ink2)}}
.flags{{margin:0;font-size:.76rem;color:var(--flag);font-weight:600}}
/* região */
.regtab{{overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:var(--card)}}
.regtab table{{border-collapse:collapse;width:100%;font-size:.88rem;min-width:720px}}
.regtab th,.regtab td{{padding:.5rem .7rem;border-bottom:1px solid var(--linesoft);text-align:left;vertical-align:top}}
.regtab th{{font-size:.74rem;letter-spacing:.06em;text-transform:uppercase;color:var(--ink3)}}
.regtab .obs{{color:var(--ink3);font-size:.8rem}}
/* índice */
.ix{{columns:3;column-gap:2rem}}
@media(max-width:56rem){{.ix{{columns:2}}}} @media(max-width:38rem){{.ix{{columns:1}}}}
.ixm{{break-inside:avoid;margin-bottom:.9rem;font-size:.88rem}}
.ixm b{{display:block;font-family:'Fraunces',serif;margin-bottom:.15rem}}
.ixm a{{display:block;text-decoration:none;color:var(--ink2);padding:.06rem 0}}
.ixm a:hover{{color:var(--accent-ink);text-decoration:underline}}
.rodape{{margin-top:3rem;border-top:1px solid var(--line);padding-top:1rem;color:var(--ink3);font-size:.82rem}}
/* print */
@media print{{
 body{{background:#fff;font-size:11px}}
 .famsec{{break-before:page}} .card{{break-inside:avoid;border-color:#ccc}}
 #tip{{display:none}} .capa{{border:none}}
}}
</style>
<main>
<header class="capa">
<p class="eyebrow">Reology Map · 1ª edição · dados BioSmart ago/2026</p>
<h1>Reologia do Ácido Hialurônico</h1>
<p class="sub">Guia reológico dos 76 preenchedores do mercado brasileiro — medidos sob um único protocolo, lado a lado.</p>
<div class="meta"><span>Autor <b>Dr. João Pithon</b></span><span>Laboratório <b>BioSmart Nanotechnology</b> (TA Instruments AR-1500ex · 25&nbsp;°C · placas Ø20&nbsp;mm · gap 500&nbsp;µm)</span><span>Frequência de referência <b>0,7&nbsp;Hz</b> (Anexo 2)</span></div>
<div class="stats"><div class="stat"><b>76</b><span>géis ensaiados</span></div><div class="stat"><b>21</b><span>marcas</span></div><div class="stat"><b>28×</b><span>amplitude de G′ (33,6 → 935,9 Pa)</span></div><div class="stat"><b>6</b><span>frequências (10 → 0,01 Hz)</span></div></div>
<p class="qt" style="margin-bottom:0">“Não existe o melhor preenchedor. Existe a propriedade reológica mais adequada para o comportamento que queremos produzir em cada região.”</p>
</header>

<section id="comoler">
<h2>Como ler este guia</h2>
<div class="box">
<p style="margin-top:0">Cada ficha traz a <b>assinatura reológica a 0,7&nbsp;Hz</b> (G′ / G″ / tan δ / η*) medida pelo estudo BioSmart, as <b>réguas de posição</b> do produto no banco (G′ em escala log com marcas nos cortes de 200 e 300&nbsp;Pa; tan δ com marcas em 0,15 e 0,30), a leitura clínica e as indicações do autor.</p>
<p><b>Níveis de indicação:</b> <span class="pill n1">região<i>1ª escolha</i></span> <span class="pill n2">região<i>forte</i></span> <span class="pill n3">região<i>boa</i></span> <span class="pill n4">região<i>seletiva</i></span></p>
<p><b>Cores das famílias:</b> <span class="chip" style="width:12px;height:12px;background:var(--fam-a)"></span>+<span class="chip" style="width:12px;height:12px;background:var(--chip-rosa)"></span> integrativo dinâmico · <span class="chip" style="width:12px;height:12px;background:var(--fam-m)"></span> preenchedor · <span class="chip" style="width:12px;height:12px;background:var(--fam-r)"></span> estrutural · <span class="chip" style="width:12px;height:12px;background:var(--fam-r)"></span>+<span class="chip" style="width:12px;height:12px;background:var(--chip-verde)"></span> estrutural maleável — <i>“A COR CLASSIFICA. O NÚMERO POSICIONA.”</i></p>
<p><b>Regra das três fontes:</b> números reológicos = exclusivamente do laudo BioSmart (Anexo&nbsp;2, 0,7&nbsp;Hz, lote identificado); dados marcados com <b>*</b> = declarados pelo fabricante/distribuidor; <b>coesividade, Swelling Factor, extrusão e Strain&nbsp;X não foram medidos nesta rodada</b> (💧) e nunca são deduzidos dos números.</p>
<p style="margin-bottom:0"><b>Sinalizações:</b> <span style="color:var(--flag);font-weight:600">⚑ dado em re-verificação</span> (auditoria do laudo) · ◌ monografia pendente · ※ contraindicação de bula. <b>Segurança:</b> reologia não é segurança vascular — nariz, glabela, fronte e fossa piriforme mantêm alerta máximo independentemente do produto.</p>
</div>
</section>

<section id="fundamentos">
<h2>Os quatro números em 60 segundos</h2>
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
<h2>O Mapa da Reologia — 76 produtos em um plano</h2>
<p class="lead">Cada ponto é um gel ensaiado (0,7&nbsp;Hz). O eixo horizontal posiciona a estrutura (G′, escala log, com os cortes operacionais de 200 e 300&nbsp;Pa); o vertical, o caráter dinâmico (tan δ). Passe o mouse/toque para identificar cada produto.</p>
{scatter()}
<div class="legend">
<span><i style="background:var(--fam-a)"></i>Integrativo dinâmico (34)</span>
<span><i style="background:var(--fam-m)"></i>Preenchedor (14)</span>
<span><i style="background:var(--fam-r)"></i>Estrutural (18)</span>
<span><i style="background:var(--fam-v)"></i>Estrutural maleável (10)</span>
</div>
<p class="lead" style="font-size:.9rem">Achados de leitura: apenas <b>2 dos 76</b> são “roxo completo” (Hyafilia V e Shaype); os pares sobrepostos (Volift=Voluma, Belotero Volume+=Neauvia Intense, Stimulate=Singderm) estão em re-verificação laboratorial; e famílias comerciais inteiras vivem dentro de uma mesma zona — a cor classifica, o número posiciona.</p>
</section>

{''.join(fam_secs)}

<section id="regioes">
<h2>Guia rápido por região</h2>
<p class="lead">Síntese do mapeamento região → necessidade reológica → produtos citados nas monografias. Uma região pode pertencer a mais de uma classe conforme o objetivo (corpo do mento ≠ vértice do mento).</p>
<div class="regtab"><table><thead><tr><th>Região</th><th>Necessidade</th><th>Produtos (1ª escolha / fortes)</th><th>Observação</th></tr></thead><tbody>{reg_rows}</tbody></table></div>
</section>

<section id="indice">
<h2>Índice por marca</h2>
<div class="ix">{idx}</div>
</section>

<section id="notas">
<h2>Fontes, limitações e aviso</h2>
<div class="box">
<p style="margin-top:0"><b>Fonte dos números:</b> laudo BioSmart Nanotechnology / Clínica Pithon Napoli, 04/08/2026 — Anexo 2 (0,7 Hz), lote identificado em cada ficha. Reômetro TA Instruments AR-1500ex, 25 °C, placas paralelas Ø 20 mm, gap 500 µm, varredura 10 → 0,01 Hz. Comparabilidade é <b>interna ao protocolo</b>; 25 °C in vitro ≠ comportamento in vivo.</p>
<p><b>Não medidos nesta rodada</b> (previstos para a 2ª rodada): coesividade quantitativa, Swelling Factor, força de extrusão, Strain X/amplitude, compressão. Onde citados, são dados declarados pelo fabricante (*) ou impressão clínica do autor — nunca resultado do ensaio.</p>
<p><b>Fichas com ⚑</b> aguardam errata/re-verificação da BioSmart (pares idênticos, η* divergentes, tan δ do Perfectha Subskin corrigido por recálculo). <b>Fichas com ◌</b> aguardam a monografia do autor.</p>
<p style="margin-bottom:0"><b>Aviso:</b> material educacional para profissionais habilitados; não substitui julgamento clínico, bula/IFU nem treinamento anatômico. Indicações refletem a experiência e a leitura reológica do autor sobre lotes específicos; os fabricantes não participaram nem endossam o estudo. Marcas citadas pertencem aos respectivos titulares.</p>
</div>
<p class="rodape">Reologia do Ácido Hialurônico — Guia Reology Map · Dr. João Pithon · 1ª edição (ago/2026). Gerado a partir do banco canônico <code>data/reologia_produtos_full.json</code>. Para imprimir/exportar PDF: usar a função de impressão do navegador (layout otimizado).</p>
</section>
</main>
<div id="tip" role="status"></div>
<script>
(function(){{
 var tip=document.getElementById('tip');
 document.querySelectorAll('#mapa .dot').forEach(function(d){{
  d.addEventListener('pointerenter',function(e){{tip.textContent=d.dataset.n+' — '+d.dataset.v;tip.style.opacity=1;}});
  d.addEventListener('pointermove',function(e){{var x=Math.min(e.clientX+14,window.innerWidth-tip.offsetWidth-8);tip.style.left=x+'px';tip.style.top=(e.clientY+16)+'px';}});
  d.addEventListener('pointerleave',function(){{tip.style.opacity=0;}});
 }});
}})();
</script>
'''
out=f'{BASE}/ebook-reologia-map.html'
open(out,'w',encoding='utf-8').write(page)
print('OK',out,len(page)//1024,'KB')
