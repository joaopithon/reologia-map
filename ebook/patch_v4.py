# -*- coding: utf-8 -*-
"""Patch v4: assinaturas reológicas oficiais (9), ícones das famílias, logo Reology Map."""
import re
P = '/tmp/claude-0/-home-user-reologia-map/cd216e96-b088-57d1-abe3-2409c365400d/scratchpad/build_ebook.py'
src = open(P, encoding='utf-8').read()

# ---------- 1. bloco de assinaturas + ícones + logo (inserido antes do radar) ----------
NEW_BLOCK = r'''
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
'''
anchor = '# ---------------- radar ----------------'
assert anchor in src
src = src.replace(anchor, NEW_BLOCK + '\n' + anchor, 1)

# ---------- 2. badge de assinatura no card ----------
old_card = """{sigdots(k)}
<div class="vis">{radar(k,fam)}"""
new_card = """{sigdots(k)}
{assin_badge(k)}
<div class="vis">{radar(k,fam)}"""
assert old_card in src
src = src.replace(old_card, new_card, 1)

# ---------- 3. CSS ----------
old_css = """.sigdots{{display:flex;gap:.9rem;font-size:.72rem;color:var(--ink3);border-bottom:1px solid var(--linesoft);padding-bottom:.45rem}}"""
new_css = """.sigdots{{display:flex;gap:.9rem;font-size:.72rem;color:var(--ink3);padding-bottom:.3rem}}
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
.a9q{{font-size:.72rem;color:var(--ink3);display:block;margin-top:.2rem}}"""
assert old_css in src
src = src.replace(old_css, new_css, 1)

# ---------- 4. logo na capa ----------
old_top = """<p class="capa-top">Reology Map</p>
<p class="capa-tag">Ciência que guia escolhas</p>"""
new_top = """{logo(74)}
<p class="capa-top">Reology Map</p>
<p class="capa-tag">Ciência que guia escolhas</p>"""
assert old_top in src
src = src.replace(old_top, new_top, 1)

# ---------- 5. seção da gramática visual (capítulo 1) ----------
old_sec = """<p><b>Assinatura de cores por métrica</b>"""
GRAM = """<h3 style="margin-top:1.2rem">A gramática das cores — 1ª cor, 2ª cor, assinatura</h3>
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
<p><b>Assinatura de cores por métrica</b>"""
assert old_sec in src
src = src.replace(old_sec, GRAM, 1)

# ---------- 6. gerar cards das 9 assinaturas ----------
A9_BUILDER = '''
A9_ORDEM = [('a','r'),('a','v'),('a','p'),('m','r'),('m','v'),('m','p'),('r','r'),('r','v'),('r','p')]
from collections import Counter as _C
_a9c = _C(assinatura(p['k'])[0] for p in ed.PRODUTOS)
a9_cards = ''.join(
    f'<div class="a9c"><div class="a9dots"><i style="background:{CHIP[b]}"></i>'
    + ('' if m=='r' else f'<span>+</span><i style="background:{CHIP[m]}"></i>')
    + f'</div><span class="a9n">{ASSIN[(b,m)]}</span><span class="a9q">{_a9c.get(ASSIN[(b,m)],0)} produtos</span></div>'
    for b,m in A9_ORDEM)
'''
anchor2 = "FACE_CAPA = face_svg("
assert anchor2 in src
src = src.replace(anchor2, A9_BUILDER + '\n' + anchor2, 1)

open(P,'w',encoding='utf-8').write(src)
print('patch v4 aplicado')
