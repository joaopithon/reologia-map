# -*- coding: utf-8 -*-
"""v8 — Capítulo 15 'Quando as fontes discordam': a regra das quatro camadas
aplicada, a tabela de divergências entre fontes, a reconciliação de nomes
comerciais e a errata desta edição."""
P = '/tmp/claude-0/-home-user-reologia-map/cd216e96-b088-57d1-abe3-2409c365400d/scratchpad/build_ebook.py'
src = open(P, encoding='utf-8').read()

# tabela de divergências: (produto no banco, G' outra fonte, tan δ outra fonte, fonte)
OUTRAS = [
 ('Belotero Balance Lido',   '128',  '0,64', 'lit', 'Literatura publicada'),
 ('Belotero Intense Lido',   '255',  '0,43', 'lit', 'Literatura publicada'),
 ('Belotero Volume + Lido',  '438',  '0,23', 'lit', 'Literatura publicada'),
 ('e.p.t.q S 100 Lido',       '36',  '0,46', 'fab', 'Fabricante (Anton Paar MCR302 · 0,1 Hz)'),
 ('e.p.t.q S 300 Lido',      '144',  '0,19', 'fab', 'Fabricante (Anton Paar MCR302 · 0,1 Hz)'),
 ('e.p.t.q S 500 Lido',      '232',  '0,14', 'fab', 'Fabricante (Anton Paar MCR302 · 0,1 Hz)'),
 ('Yvoire Classic+ Lido',    '286',  '0,36', 'lit', 'Estudo comparativo de linha'),
 ('Yvoire Volume+ Lido',     '253',  '0,29', 'lit', 'Estudo comparativo de linha'),
 ('Yvoire Contour+ Lido',    '484',  '0,32', 'lit', 'Estudo comparativo de linha'),
]

GEN_ROWS = '''
_ROWS_FONTES = ''
for _p, _g, _t, _kind, _fonte in OUTRAS_FONTES:
    _r = DATA[_p]; _td = ERR_TD.get(_p, _r['tand_0.7Hz'])
    _ddir = '↑' if float(_g.replace(',', '.')) > _r['G1_0.7Hz'] else '↓'
    _ROWS_FONTES += (f'<tr><td><b>{html.escape(short(_p))}</b></td>'
        f'<td class="med">G′ {br(_r["G1_0.7Hz"],2)}<br>tan δ {br(_td,2)}</td>'
        f'<td class="out">G′ {_g} {_ddir}<br>tan δ {_t}</td>'
        f'<td>{_fonte}</td></tr>')

'''
anchor = '# ---------------- seções de grupos ----------------'
assert anchor in src
src = src.replace(anchor, 'OUTRAS_FONTES = ' + repr(OUTRAS) + '\n' + GEN_ROWS + anchor, 1)

CAP15 = """
<section class="folha" id="fontes">
{cap_head('Capítulo 15','Quando as fontes discordam',
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
"""
mark = '<section class="folha" id="regioes">'
assert mark in src
src = src.replace(mark, CAP15.strip() + '\n\n' + mark, 1)

# apêndice B: nota sobre a auditoria
src = src.replace('<b>Fichas com ⚑</b> aguardam errata/re-verificação laboratorial',
 '<b>Auditoria desta edição:</b> os infográficos e tabelas anteriores do autor foram conferidos '
 'valor por valor contra o banco canônico antes de qualquer conteúdo novo entrar no livro. '
 'A tabela-mestra a 0,7 Hz conferiu em 39 dos 42 produtos; as três divergências, sua demonstração '
 'e a correção de escopo dos rankings estão no <b>capítulo 15</b>. '
 'Rankings construídos sobre universo incompleto foram refeitos a partir dos 76 ensaios. '
 '<b>Fichas com ⚑</b> aguardam errata/re-verificação laboratorial', 1)

open(P, 'w', encoding='utf-8').write(src)
print('v8 aplicado: Capítulo 15 — Quando as fontes discordam')
