# -*- coding: utf-8 -*-
"""v12 — Capítulo 1 revisado: as duas figuras rasterizadas viram diagramas
nativos na identidade do livro, com o conceito atualizado — o painel do que
o estudo mede e o que não mede, e o Esquema de Descrição em quatro passos."""
P = 'build_ebook.py'
src = open(P, encoding='utf-8').read()

FUNCS = '''
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
        li = ''.join(f'<li>{dotchip(c, 12)}<b>{lab}</b><span>{txt}</span></li>'
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
 ('4', 'Os quatro números', 'm'), ('5', 'O mapa e as regiões da face', 'm'),
 ('6', 'A forma do gel', 'm'), ('7', 'Textura visual', 'm'),
 ('8', 'Atlas de gráficos', 'r'), ('9–14', 'Os seis grupos, produto a produto', 'r'),
 ('15', 'Rankings completos', 'r'), ('16', 'Quando as fontes discordam', 's'),
 ('17', 'Guia rápido por região', 's'),
]

def roteiro():
    it = ''.join(f'<li class="rt-{c}"><b>{n}</b><span>{t}</span></li>' for n, t, c in ROTEIRO)
    return f'<ol class="roteiro">{it}</ol>'

'''
anchor = '# ---------------- seções de grupos ----------------'
assert anchor in src
src = src.replace(anchor, FUNCS + anchor, 1)

CSS = '''
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
.mc-cut{{display:flex;justify-content:space-between;margin-top:.15rem;position:relative}}
.mc-cut i{{font-family:'JetBrains Mono',monospace;font-size:.6rem;color:var(--ink3);font-style:normal}}
.mc-cut em{{font-family:'Barlow',sans-serif;font-size:.6rem;color:var(--ink3);font-style:normal}}
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
.p4-l span{{color:var(--ink3);font-size:.72rem}}
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
'''
mark = '/* figuras e ilustrações com moldura dourada */'
src = src.replace(CSS.__class__() or mark, mark, 1)   # no-op guard
src = src.replace(mark, CSS + mark, 1)

# ---------------------------------------------------------------- nova seção 1
i = src.index('<section class="folha" id="comoler">')
j = src.index('\n<section class="folha" id="molecula">')
NOVA = """<section class="folha" id="comoler">
{cap_head('Capítulo 1','Como ler este guia',
 'Este livro tem uma gramática própria: quatro números medidos, três famílias de cor, nove assinaturas. Quinze minutos aqui economizam a leitura inteira.')}
<h3>1.1 &nbsp;O que este livro mede — e o que ele não mede</h3>
<p class="lead">A primeira coisa a saber sobre um guia de reologia é onde ele para. Cinco propriedades costumam ser citadas para descrever um preenchedor; <b>este estudo mediu quatro delas</b>, sob protocolo único. As demais existem, importam clinicamente e <b>não foram medidas aqui</b> — então não recebem número, cor nem ranking neste livro.</p>
{figura_nat('1', painel_medidas(),
 'O alcance deste guia. À esquerda, os quatro parâmetros medidos a 0,7 Hz com suas faixas de cor — a barra mostra a escala e os números abaixo dela são os cortes que separam as cores. À direita, as propriedades declaradas mas não medidas nesta rodada, sempre marcadas com 💧. <b>Dado ausente é informação</b>: nenhuma delas é deduzida a partir das quatro medidas.')}
<div class="box"><p style="margin:0"><b>Por que 0,7 Hz.</b> Um gel viscoelástico responde de forma diferente conforme a velocidade da solicitação — não existe “o G′ do produto”, existe o G′ àquela frequência. Este livro lê tudo a <b>0,7 Hz</b>, a faixa da mímica facial habitual. O mesmo Belotero Balance mede G′ 78 Pa a 10 Hz, 34 Pa a 0,7 Hz e vira praticamente líquido a 0,01 Hz. Comparar produtos só faz sentido na mesma frequência — e no mesmo protocolo.</p></div>

{filete('cadeia', 160)}
<h3>1.2 &nbsp;A gramática das cores</h3>
<p class="lead">Todo produto deste livro é descrito por duas cores. <b>A primeira mostra quanto o gel estrutura</b>; <b>a segunda mostra como essa estrutura se comporta</b>. Somadas, dão o nome oficial do perfil — a assinatura.</p>
{figura_nat('2', esquema_passos(),
 'O <b>Esquema de Descrição dos Ácidos Hialurônicos</b>, a leitura completa em quatro passos: a 1ª cor (a família de G′), a 2ª cor (o comportamento em tan δ), a assinatura que nasce da soma e as três perguntas clínicas que ela responde. É a mesma gramática usada nas fichas, nos gráficos, no radar do capítulo 6 e no mapa de regiões do capítulo 5.')}
<div class="gram">
<div class="gramc">{ico('ondas')}<div><h4>Baixo G′</h4><span class="verbo" style="color:var(--fam-a)">ESPALHA / INTEGRA</span><p>Menor relevo próprio e menor capacidade estrutural: o gel se distribui e integra.</p></div></div>
<div class="gramc">{ico('balanca')}<div><h4>G′ intermediário</h4><span class="verbo" style="color:var(--fam-m)">PREENCHE / EQUILIBRA</span><p>Equilíbrio entre preencher e sustentar — a cor do vale.</p></div></div>
<div class="gramc">{ico('coluna')}<div><h4>Alto G′</h4><span class="verbo" style="color:var(--fam-r)">SUSTENTA / PROJETA</span><p>Maior manutenção de forma sob carga: o gel mantém o vértice onde foi colocado.</p></div></div>
</div>
<div class="gram">
<div class="gramc">{ico('dinamico')}<div><h4>Dinâmico</h4><span class="verbo" style="color:var(--chip-rosa)">ACOMPANHA O MOVIMENTO</span><p>Componente viscosa relativa maior: acompanha melhor o tecido em movimento.</p></div></div>
<div class="gramc">{ico('maleavel')}<div><h4>Maleável</h4><span class="verbo" style="color:var(--fam-v)">MOLDÁVEL / INTEGRATIVO</span><p>Boa adaptação e distribuição: molda e espalha sem perder corpo.</p></div></div>
</div>
<p><b>As nove assinaturas</b> — três famílias de G′ × três comportamentos de tan δ:</p>
<div class="a9">{a9_cards}</div>
<p style="font-size:.9rem;color:var(--ink2)">Nas fichas, cada produto exibe sua assinatura logo abaixo do nome. As três assinaturas puras — <b>ESPALHA</b>, <b>PREENCHE</b>, <b>PROJETA</b> — são os perfis de tan δ baixo, em que a estrutura fala mais alto que o comportamento.</p>
<div class="box"><p style="margin:0"><b>Os quatro pontos coloridos de cada ficha.</b> Além da assinatura, toda ficha traz um ponto por parâmetro medido, na cor daquela métrica: <b>G′</b>, <b>G″</b> e <b>η*</b> em {dotchip('a',11)} azul (baixo) / {dotchip('m',11)} amarelo (intermediário) / {dotchip('r',11)} roxo (alto); <b>tan δ</b> em {dotchip('r',11)} roxo (elástico) / {dotchip('v',11)} verde (maleável) / {dotchip('p',11)} rosa (dinâmico). Cortes: G′ 200 e 300 Pa · G″ 50 e 100 Pa · tan δ 0,15 e 0,20 · η* 50 e 100 Pa·s. As zonas de transição são tratadas com curadoria versionada — o Restylane Defyne, a 292,62 Pa, é lido como roxo por comportamento.</p></div>

{filete('cadeia', 160)}
<h3>1.3 &nbsp;Os seis grupos e as três perguntas</h3>
<p class="lead">Os produtos estão organizados em <b>seis grupos oficiais</b>. Os cinco primeiros são famílias de G′; o sexto é um <b>critério funcional transversal</b> — atravessa as famílias e tem cor própria.</p>
<div class="g33 passos">
<div class="box passo"><b>O que eu quero fazer?</b><p style="margin:.3rem 0 0;font-size:.9rem;color:var(--ink2)">Espalhar → <b style="color:var(--fam-a)">grupos 1–2</b> · Preencher → <b style="color:var(--fam-m)">grupo 3</b> · Projetar → <b style="color:var(--fam-r)">grupos 4–5</b>.</p></div>
<div class="box passo"><b>Esse tecido se move muito?</b><p style="margin:.3rem 0 0;font-size:.9rem;color:var(--ink2)">Se sim, procure perfil <b style="color:var(--chip-rosa)">DINÂMICO</b> (tan δ rosa): acompanha o movimento.</p></div>
<div class="box passo"><b>Preciso moldar e distribuir?</b><p style="margin:.3rem 0 0;font-size:.9rem;color:var(--ink2)">Se sim, procure perfil <b style="color:var(--fam-v)">MALEÁVEL</b> (tan δ verde): adapta e distribui.</p></div>
</div>
<p style="margin-bottom:.2rem"><b>Níveis de indicação nas fichas:</b> <span class="pill n1">região<i>1ª escolha</i></span> <span class="pill n2">região<i>forte</i></span> <span class="pill n3">região<i>boa</i></span> <span class="pill n4">região<i>seletiva</i></span></p>
<p class="qt">A sequência decisória do Reology Map: <b>ANATOMIA → DEFEITO → OBJETIVO → PLANO → PRODUTO → VOLUME → TÉCNICA</b>. O produto é a <b>quinta</b> decisão, não a primeira.</p>

{filete('cadeia', 160)}
<h3>1.4 &nbsp;De onde vem cada afirmação</h3>
<p class="lead">Toda informação deste livro carrega a sua origem. É o que separa uma medida de uma impressão — e o que permite ao leitor discordar com precisão.</p>
<div class="camadas">
<div class="camada"><b>1 · Medido</b><p>Laudo do estudo, a 0,7 Hz, com lote identificado. Única camada que gera cor, grupo, assinatura e ranking.</p></div>
<div class="camada c2"><b>2 · Fabricante *</b><p>Declarado em monografia ou material técnico. Sempre com asterisco, nunca comparado lado a lado com a camada 1.</p></div>
<div class="camada c3"><b>3 · Literatura</b><p>Publicado por terceiros e citado como tal. Serve de contexto — não classifica.</p></div>
<div class="camada c4"><b>4 · Interpretação</b><p>A leitura clínica do autor sobre o número medido. É opinião fundamentada, declarada como opinião.</p></div>
</div>
<p><b>Sinalizações que você verá nas fichas:</b> <span style="color:var(--flag);font-weight:600">⚑ dado em re-verificação laboratorial</span> · <b>◌</b> monografia do autor pendente · <b>※</b> contraindicação de bula listada · <b>💧</b> propriedade não medida nesta rodada.</p>
<div class="box" style="border-left:4px solid var(--flag)"><p style="margin:0"><b>O aviso que vale por todo o livro:</b> reologia descreve como o gel se comporta — não descreve segurança. <b>G′ não é segurança vascular</b>, G′ não define plano de injeção, e nome comercial não é reologia. O capítulo 16 mostra o caso da linha Perfectha, em que a escada comercial e a escada medida apontam para lados opostos.</p></div>

{filete('cadeia', 160)}
<h3>1.5 &nbsp;O caminho do livro</h3>
{roteiro()}
</section>

"""
src = src[:i] + NOVA + src[j:]

open(P, 'w', encoding='utf-8').write(src)
print('v12: capítulo 1 revisado — figuras nativas na identidade do livro')
