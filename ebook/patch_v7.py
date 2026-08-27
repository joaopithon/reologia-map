# -*- coding: utf-8 -*-
"""v7 — conteúdo auditado: dois capítulos de fundamentos (molécula, rede,
hialuronidase, viscoelasticidade), rankings temáticos refeitos sobre os 76
ensaios e o capítulo 'Quando as fontes discordam' com a errata da edição."""
P = '/tmp/claude-0/-home-user-reologia-map/cd216e96-b088-57d1-abe3-2409c365400d/scratchpad/build_ebook.py'
src = open(P, encoding='utf-8').read()

# ------------------------------------------------------- carregar ilustrações novas
src = src.replace("ILU = json.load(open(f'{BASE}/ilustracoes.json'))",
                  "ILU = json.load(open(f'{BASE}/ilustracoes.json'))\n"
                  "ILU2 = json.load(open(f'{BASE}/ilustracoes2.json'))", 1)

# ------------------------------------------------------- helper: ranking temático
HELP = '''
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
        tr += (f'<tr><td class="pd-n">{i}</td>'
               f'<td class="pd-p">{dotchip(fam,10)} {html.escape(short(k))}'
               f'<span class="pd-as">{assinatura(k)}</span></td>'
               f'<td class="pd-v">{fmt(v(r))}</td>'
               f'<td class="pd-x">G′ {br(g1,2)} · tan δ {br(td,2)}</td></tr>')
    un = {'g1': 'G′ (Pa)', 'g2': 'G″ (Pa)', 'td': 'tan δ', 'eta': 'η* (Pa·s)'}[metric]
    n = f'<p class="pd-nota">{nota}</p>' if nota else ''
    return (f'<div class="podio"><h4>{titulo}</h4><table><thead><tr><th></th><th>Produto</th>'
            f'<th>{un}</th><th>Perfil a 0,7 Hz</th></tr></thead><tbody>{tr}</tbody></table>{n}</div>')

'''
anchor = '# ---------------- seções de grupos ----------------'
assert anchor in src
src = src.replace(anchor, HELP + anchor, 1)

# errata central (tan δ do Perfectha Subskin recalculado)
src = src.replace("def td_of(k): return 0.15 if k == 'Perfectha Subskin' else DATA[k]['tand_0.7Hz']",
 "ERR_TD = {'Perfectha Subskin': 0.15}   # errata: G″/G′ = 52,00/343,00 = 0,1516\n"
 "def td_of(k): return ERR_TD.get(k, DATA[k]['tand_0.7Hz'])", 1)

# ------------------------------------------------------- CSS dos novos blocos
CSS = '''
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
.camada b{{font-family:'Barlow Condensed',sans-serif;font-size:1.02rem;letter-spacing:.05em;
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
.mod b{{font-family:'Barlow Condensed',sans-serif;font-size:1.05rem;letter-spacing:.04em;
 text-transform:uppercase;color:var(--title-ink);display:block;margin-bottom:.25rem}}
.mod p{{margin:0;font-family:'Barlow',sans-serif;font-size:.82rem;color:var(--ink2);line-height:1.5}}
/* etapas numeradas (química) */
.etapas{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:.85rem;margin:1rem 0}}
.etapa{{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:.85rem 1rem;position:relative}}
.etapa .n{{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:.9rem;color:#fff;
 background:var(--accent);width:1.55rem;height:1.55rem;border-radius:50%;display:flex;
 align-items:center;justify-content:center;margin-bottom:.45rem}}
.etapa b{{font-family:'Barlow Condensed',sans-serif;font-size:1.02rem;letter-spacing:.04em;
 text-transform:uppercase;color:var(--title-ink);display:block;margin-bottom:.2rem}}
.etapa p{{margin:0;font-family:'Barlow',sans-serif;font-size:.82rem;color:var(--ink2);line-height:1.5}}
.etapa code{{font-family:'JetBrains Mono',monospace;font-size:.78em;color:var(--accent-ink)}}
'''
mark = '/* figuras e ilustrações com moldura dourada */'
src = src.replace(mark, CSS + mark, 1)

# ------------------------------------------------------- renumeração de capítulos
REN = [('Capítulo 2', 'Capítulo 4', 'Os quatro números em 60 segundos'),
       ('Capítulo 3', 'Capítulo 5', 'O Mapa da Reologia — todos os géis em um plano'),
       ('Capítulo 4', 'Capítulo 6', 'A forma do gel — o radar de 4 eixos'),
       ('Capítulo 5', 'Capítulo 7', 'Textura visual do gel — o que os olhos antecipam'),
       ('Capítulo 12', 'Capítulo 14', 'Rankings completos — os 76 ensaios lado a lado'),
       ('Capítulo 13', 'Capítulo 16', 'Guia rápido por região')]
for old, new, tit in REN:
    a = f"cap_head('{old}','{tit}')"
    assert a in src, a
    src = src.replace(a, f"cap_head('{new}','{tit}')", 1)
a = "cap_head('Capítulo 6 (gráficos) · Capítulos 7–11 (grupos)','Atlas de gráficos — todas as variáveis')"
assert a in src
src = src.replace(a, "cap_head('Capítulo 8 (gráficos) · Capítulos 9–13 (grupos)','Atlas de gráficos — todas as variáveis')", 1)
src = src.replace('fam_secs=[]; CH0=6', 'fam_secs=[]; CH0=8', 1)
src = src.replace("CAPÍTULO 11 · GRUPO 6", "CAPÍTULO 13 · GRUPO 6", 1)

# ------------------------------------------------------- CAPÍTULOS 2 e 3 (novos)
CAP23 = """
<section class="folha" id="molecula">
{cap_head('Capítulo 2','A molécula e a rede — de onde vem o G′',
 'Antes de qualquer número existe química. Três desenhos explicam por que um gel de ácido hialurônico resiste, escoa e um dia desaparece.')}
<h3>2.1 &nbsp;A molécula: um dissacarídeo repetido milhares de vezes</h3>
<p class="lead">O ácido hialurônico é um <b>glicosaminoglicano linear</b> formado pela repetição de uma única unidade dissacarídica: <b>ácido D-glicurônico</b> (GlcA, C<sub>6</sub>H<sub>10</sub>O<sub>7</sub>) e <b>N-acetil-D-glicosamina</b> (GlcNAc, C<sub>8</sub>H<sub>15</sub>NO<sub>6</sub>). As duas unidades se unem alternadamente por ligações <b>β(1→3)</b> e <b>β(1→4)</b>, e uma única cadeia pode conter de <b>2.000 a mais de 25.000</b> dessas unidades.</p>
{figura('3', ILU2['conc_molecula'], 'Arquitetura molecular do ácido hialurônico: as duas unidades monossacarídicas em projeção de Haworth e modelo tridimensional, com as ligações glicosídicas alternadas β(1→3) e β(1→4). Os grupos que aparecem na cadeia — carboxila (COO<sup>−</sup>), hidroxila (OH) e acetamido (NH-COCH<sub>3</sub>) — são os que dão ao HA sua avidez por água e, no passo seguinte, os pontos onde a reticulação acontece.', 'estrutura molecular do ácido hialurônico')}
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
{figura('4', ILU2['conc_hidrogel'], 'Formação do hidrogel de ácido hialurônico em quatro etapas: solução, agente reticulante (BDDE), reação com as hidroxilas formando ligações éter e a rede tridimensional que retém água. O detalhe mostra a ligação éter no ponto de reticulação. <b>É deste desenho que vem o ornamento das cadeias em contas usado nos rodapés deste livro</b> — a identidade visual do Reology Map nasce da própria molécula.', 'formação do hidrogel de ácido hialurônico por reticulação')}
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
{figura('5', ILU2['conc_hialuron'], 'Degradação do gel de ácido hialurônico pela hialuronidase: o sítio de clivagem na ligação β(1→4), o mecanismo catalítico em quatro passos (reconhecimento, posicionamento da água no sítio ativo, clivagem hidrolítica e liberação dos oligossacarídeos) e o efeito progressivo sobre o gel.', 'ação da hialuronidase sobre o gel de ácido hialurônico')}
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
{figura('6', ILU2['conc_viscoel'], 'Viscoelasticidade da base ao gel: elasticidade (mola, Lei de Hooke), viscosidade (mel, τ = η·γ̇), a distinção entre fluido e sólido elástico sob tensão constante, o hidrogel como caso intermediário e os três modelos reológicos clássicos — Maxwell, Kelvin-Voigt e Burgers — aplicados aos preenchedores.', 'capítulo de viscoelasticidade: elasticidade, viscosidade e modelos reológicos')}
<h3>Os três modelos clássicos</h3>
<div class="mods">
<div class="mod"><b>Maxwell</b><p>Mola e amortecedor <b>em série</b>. Responde instantaneamente e depois escoa sem limite. Descreve bem a <b>relaxação</b> de tensão.</p></div>
<div class="mod"><b>Kelvin-Voigt</b><p>Mola e amortecedor <b>em paralelo</b>. Deforma progressivamente até um platô e recupera. Descreve bem a <b>fluência</b> (creep).</p></div>
<div class="mod"><b>Burgers</b><p>Combinação dos dois. É o que mais se aproxima do comportamento real de um hidrogel de HA: deformação instantânea, fluência e recuperação parcial.</p></div>
</div>
<div class="box"><p style="margin-top:0"><b>É daqui que saem os quatro números do capítulo seguinte.</b> Num ensaio oscilatório, a resposta do gel se decompõe em duas partes: a que está <b>em fase</b> com a deformação — a energia armazenada e devolvida, <b>G′</b> — e a que está <b>defasada em 90°</b> — a energia dissipada como escoamento, <b>G″</b>. A razão entre elas, <b>tan δ = G″/G′</b>, diz qual dos dois comportamentos domina.</p>
<p style="margin-bottom:0">E como o gel é viscoelástico, <b>a resposta depende da velocidade da solicitação</b>. Não existe “o G′ do produto”: existe o G′ àquela frequência. Por isso todo este livro é lido a <b>0,7 Hz</b> — a frequência da mímica habitual — e por isso o mesmo Belotero Balance aparece com G′ 78 Pa e tan δ 0,90 a 10 Hz, 34 Pa e 0,69 a 0,7 Hz, e vira praticamente líquido a 0,01 Hz.</p></div>
</section>
"""
mark2 = '<section class="folha" id="fundamentos">'
assert mark2 in src
src = src.replace(mark2, CAP23.strip() + '\n\n' + mark2, 1)

# ------------------------------------------------------- rankings temáticos (cap 14)
RANK_TEM = """
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
"""
mark3 = '<section class="folha" id="regioes">'
assert mark3 in src
src = src.replace('</section>\n\n' + mark3, RANK_TEM.rstrip() + '\n</section>\n\n' + mark3, 1)

# ------------------------------------------------------- numeração das figuras em ordem
# Fig 1 mapa geral · 2 esquema · 3 molécula · 4 hidrogel · 5 hialuronidase · 6 viscoel · 7 face
FIG1 = """{figura('1', ILU2['conc_mapa'], 'O <b>mapa geral da reologia do ácido hialurônico</b>: os cinco parâmetros que descrevem um gel injetado na face e o que cada extremo significa na clínica — <b>baixo G′</b> (flexibilidade e naturalidade), <b>alto G′</b> (suporte e projeção), <b>baixo swelling factor</b> (menor edema e maior previsibilidade), <b>alto tan δ</b> (maleabilidade e integração dinâmica) e <b>coesividade</b> (capacidade de se manter unido no tecido). Deste conjunto, este livro mede quatro; swelling factor e coesividade não foram medidos nesta rodada e aparecem sempre marcados com 💧.', 'mapa geral dos parâmetros reológicos do ácido hialurônico')}
"""
a = "{cap_head('Capítulo 1','Como ler este guia')}"
assert a in src
src = src.replace(a, a + '\n' + FIG1.strip(), 1)
src = src.replace("{figura('1', ILU['esquema']", "{figura('2', ILU['esquema']", 1)
assert '<b>Figura 2.</b> As cinco tarefas geométricas' in src
src = src.replace('<b>Figura 2.</b> As cinco tarefas geométricas',
                  '<b>Figura 7.</b> As cinco tarefas geométricas', 1)

open(P, 'w', encoding='utf-8').write(src)
print('v7 aplicado: caps 2 e 3 + rankings temáticos + renumeração + 5 figuras novas')
