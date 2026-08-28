# -*- coding: utf-8 -*-
"""v16 — capítulo 5 passa a liderar pelas três famílias; o mapa de seis
grupos dá lugar ao mapa das famílias mais os três usos do alto G′."""
P = 'build_ebook.py'
src = open(P, encoding='utf-8').read()

i = src.index('<h3 style="margin-top:1.6rem">Mapa anatômico — que região pede qual assinatura</h3>')
j = src.index('</section>', i)
NOVO = """<h3 style="margin-top:1.6rem">Mapa anatômico — as três famílias sobre a face</h3>
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
"""
src = src[:i] + NOVO + src[j:]

# o capítulo passa a se chamar pelo que faz
src = src.replace("cap_head('Capítulo 5','O Mapa da Reologia — todos os géis em um plano')",
                  "cap_head('Capítulo 5','O Mapa da Reologia — três famílias sobre a face',"
                  "\n 'Três cores organizam o livro inteiro: azul integra, amarelo preenche, roxo sustenta. "
                  "As subclasses refinam — não criam famílias novas.')", 1)

open(P, 'w', encoding='utf-8').write(src)
print('v16: capítulo 5 lidera pelas três famílias')
