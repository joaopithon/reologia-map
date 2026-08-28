# -*- coding: utf-8 -*-
"""v11 — Capítulo 6 revisado: os quatro conceitos medidos e a forma geométrica
que os mede. O radar passa a carregar a gramática de cores: preenchimento na
1ª cor (família de G′), contorno na 2ª cor (tan δ) e cada vértice na cor da
sua própria métrica."""
P = 'build_ebook.py'
src = open(P, encoding='utf-8').read()

# ---------------------------------------------------------------- radar colorido pela assinatura
OLD = """    return (f'<svg class="{cls}" viewBox="0 0 {size} {size}" role="img" aria-label="forma reológica"><title>{html.escape(tip)}</title>'
            f'{grid}{axes}<polygon points="{poly}" fill="var(--fam-{fam})" fill-opacity=".22" stroke="var(--fam-{fam})" stroke-width="2" stroke-linejoin="round"/>'
            + ''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.4" fill="var(--fam-{fam})"/>' for x,y in pts) + lbl + '</svg>')"""
assert OLD in src
NEW = """    s = sig_cores(k)                      # gramática oficial: 1ª cor G′, 2ª cor tan δ
    fill, stroke = CHIP[s['g1']], CHIP[s['td']]
    dots = ''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.7" fill="{CHIP[s[m]]}" '
                   f'stroke="var(--card)" stroke-width="1"/>'
                   for (x, y), m in zip(pts, ('g1', 'g2', 'td', 'eta')))
    return (f'<svg class="{cls}" viewBox="0 0 {size} {size}" role="img" aria-label="forma reológica"><title>{html.escape(tip)}</title>'
            f'{grid}{axes}<polygon points="{poly}" fill="{fill}" fill-opacity=".20" stroke="{stroke}" stroke-width="2" stroke-linejoin="round"/>'
            + dots + lbl + '</svg>')"""
src = src.replace(OLD, NEW, 1)

# ---------------------------------------------------------------- helpers do capítulo
HELP = '''
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
  'Amarelo — a cor do vale. A forma se centra: preenche e equilibra sem impor projeção.'),
 ('4', 'ALTO G′', ['r'], 'Restylane Shaype Lido',
  'Roxo em todos os eixos. A forma aponta para cima e para a esquerda: estrutura e permanência.'),
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

'''
anchor = '# ---------------- seções de grupos ----------------'
src = src.replace(anchor, HELP + anchor, 1)

# radar() com fam opcional
src = src.replace('def radar(k, fam, size=96, cls=\'radar\'):',
                  'def radar(k, fam=None, size=96, cls=\'radar\'):', 1)

# ---------------------------------------------------------------- CSS
CSS = '''
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
'''
mark = '/* figuras e ilustrações com moldura dourada */'
src = src.replace(mark, CSS + mark, 1)

# ---------------------------------------------------------------- nova seção 6
i = src.index('<section class="folha" id="forma">')
j = src.index('</section>', i) + len('</section>')
NOVA = """<section class="folha" id="forma">
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
</section>"""
src = src[:i] + NOVA + src[j:]

open(P, 'w', encoding='utf-8').write(src)
print('v11: capítulo 6 revisado — 4 conceitos + forma na gramática de cores')
