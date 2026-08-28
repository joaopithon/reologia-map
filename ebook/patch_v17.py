# -*- coding: utf-8 -*-
"""v17 — capítulo 1 lidera pelas três famílias e a capa passa a carregá-las.
A capa deixa de usar os quatro cards rasterizados e ganha o trio nativo."""
P = 'build_ebook.py'
src = open(P, encoding='utf-8').read()

# face_regioes aceita classe (para a variante da capa)
src = src.replace("def face_regioes(g, width=196):", "def face_regioes(g, width=196, cls='facereg'):", 1)
src = src.replace("""    return (f'<svg class="facereg" viewBox="0 0 300 400" role="img" '""",
                  """    return (f'<svg class="{cls}" viewBox="0 0 300 400" role="img" '""", 1)
src = src.replace("def face_fam(f, width=210):\n"
                  "    g = dict(n=f['n'], regs=f['regs'], cores=[f['cor'], f['sub'][-1][1][-1]], txt=f['regs_txt'])\n"
                  "    return face_regioes(g, width)",
                  "def face_fam(f, width=210, cls='facereg'):\n"
                  "    g = dict(n=f['n'], regs=f['regs'], cores=[f['cor'], f['sub'][-1][1][-1]], txt=f['regs_txt'])\n"
                  "    return face_regioes(g, width, cls)", 1)

# gota no chip da olheira, para não confundir verde com turquesa
src = src.replace("('na olheira', ['r', 's'])", "('na olheira 💧', ['r', 's'])", 1)

# ------------------------------------------------------------------ capa nativa
CAPA_FN = '''
def capa_familias():
    """Trio da capa: as três famílias em traço claro sobre o navy."""
    out = ''
    for f in FAMILIAS:
        out += (f'<figure class="cf"><span class="cf-t">{f["nome"]}</span>'
                f'{face_fam(f, 168, "facereg capa-face")}</figure>')
    return f'<div class="capa-trio">{out}</div>'

'''
anchor = '# ---------------- seções de grupos ----------------'
src = src.replace(anchor, CAPA_FN + anchor, 1)

i = src.index('<div class="capa-grid">')
j = src.index('</div>', src.index("ILU['g6a']", i)) + 6
src = src[:i] + '{capa_familias()}' + src[j:]

CSS = '''
.capa-trio{{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(.4rem,1.6vw,1.1rem);
 margin:clamp(1rem,3vw,1.7rem) auto;max-width:600px}}
.capa-trio .cf{{margin:0;border:1px solid var(--gold-2);padding:.5rem .3rem .2rem;
 background:rgba(255,255,255,.04);display:flex;flex-direction:column;align-items:center}}
.cf-t{{font-family:'Barlow Condensed',sans-serif;font-size:clamp(.62rem,1.7vw,.86rem);
 font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--gold-3);
 margin-bottom:.15rem;text-align:center}}
.capa-trio .facereg{{width:100%;height:auto;max-width:168px}}
.capa-face .rg{{fill-opacity:.5;stroke-width:2.2}}
'''
mark = '/* figuras e ilustrações com moldura dourada */'
src = src.replace(mark, CSS + mark, 1)

# ------------------------------------------------------------------ capítulo 1: seção 1.3
i = src.index('<h3>1.3 &nbsp;Os seis grupos e as três perguntas</h3>')
j = src.index('{filete(\'cadeia\', 160)}\n<h3>1.4', i)
NOVO13 = """<h3>1.3 &nbsp;As três famílias — o eixo do livro</h3>
<p class="lead">Toda a organização deste guia repousa em <b>três famílias</b>, definidas pelo G′ e reconhecidas pela cor. É o que se deve levar daqui: <b style="color:var(--fam-a)">azul integra</b>, <b style="color:var(--fam-m)">amarelo preenche</b>, <b style="color:var(--fam-r)">roxo sustenta</b>.</p>
<div class="fam3">
<div class="f3 f3-a"><b>1 · BAIXO G′</b><span>azul</span><p>Espalha e integra, com pouco relevo próprio. Tem <b>duas assinaturas</b> — azul + rosa e azul + amarelo + rosa — que <b>atendem as mesmas regiões</b>: a segunda apenas valoriza um pouco mais.</p></div>
<div class="f3 f3-m"><b>2 · MODERADO G′</b><span>amarelo</span><p>Preenche e equilibra. <b>Uma assinatura só</b>, sem subclasse — a família de transição, a cor do vale.</p></div>
<div class="f3 f3-r"><b>3 · ALTO G′</b><span>roxo</span><p>Sustenta. <b>Roxo puro</b> projeta; <b>roxo com segunda cor</b> volumiza com menos projeção; e o alto G′ de <b>baixo swelling factor</b> é o que se usa na olheira. 💧</p></div>
</div>
<p>Os <b>seis grupos</b> dos capítulos 9 a 14 e as <b>nove assinaturas</b> não são um segundo sistema: são o detalhamento destas três famílias. A correspondência é direta — família azul = grupos 1 e 2 · família amarela = grupo 3 · família roxa = grupos 4 e 5, mais o critério funcional de baixo swelling factor.</p>
<div class="g33 passos">
<div class="box passo"><b>O que eu quero fazer?</b><p style="margin:.3rem 0 0;font-size:.9rem;color:var(--ink2)">Espalhar → <b style="color:var(--fam-a)">azul</b> · Preencher → <b style="color:var(--fam-m)">amarelo</b> · Sustentar → <b style="color:var(--fam-r)">roxo</b>.</p></div>
<div class="box passo"><b>Esse tecido se move muito?</b><p style="margin:.3rem 0 0;font-size:.9rem;color:var(--ink2)">Se sim, procure a segunda cor <b style="color:var(--chip-rosa)">rosa</b> — o perfil dinâmico acompanha o movimento.</p></div>
<div class="box passo"><b>Preciso moldar e distribuir?</b><p style="margin:.3rem 0 0;font-size:.9rem;color:var(--ink2)">Se sim, procure a segunda cor <b style="color:var(--fam-v)">verde</b> — o perfil maleável adapta e distribui.</p></div>
</div>
<p style="margin-bottom:.2rem"><b>Níveis de indicação nas fichas:</b> <span class="pill n1">região<i>1ª escolha</i></span> <span class="pill n2">região<i>forte</i></span> <span class="pill n3">região<i>boa</i></span> <span class="pill n4">região<i>seletiva</i></span></p>
<p class="qt">A sequência decisória do Reology Map: <b>ANATOMIA → DEFEITO → OBJETIVO → PLANO → PRODUTO → VOLUME → TÉCNICA</b>. O produto é a <b>quinta</b> decisão, não a primeira.</p>

"""
src = src[:i] + NOVO13 + src[j:]

CSS2 = '''
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
'''
src = src.replace(mark, CSS2 + mark, 1)

open(P, 'w', encoding='utf-8').write(src)
print('v17: capítulo 1 e capa nas três famílias')
