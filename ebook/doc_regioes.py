# -*- coding: utf-8 -*-
"""Documento das regioes da cabeca e do pescoco — figura masculina.

Monta docs/regioes/regioes-da-face.html a partir das pranchas de regioes_face.py
e do glossario abaixo. Conteudo anatomico de referencia (Terminologia Anatomica).
"""
import html, importlib.util, pathlib

_spec = importlib.util.spec_from_file_location(
    'regioes_face', pathlib.Path(__file__).with_name('regioes_face.py'))
RF = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(RF)

# ============================================================ glossario
# (nome, vistas, limites, conteudo de nota)
GRUPOS = [
 ('Crânio e face superior', [
  ('Região frontal', 'anterior · lateral',
   'Abaixo, a glabela e as margens supraorbitais; lateralmente, a linha temporal '
   'superior, que a separa da região temporal; acima, o limite convencional com a '
   'região parietal.',
   'Ventre frontal do occipitofrontal. Nas margens supraorbitais emergem os feixes '
   'supraorbital e supratroclear — o pedículo que irriga a fronte e que se anastomosa '
   'com a circulação oftálmica.'),
  ('Região parietal', 'anterior · lateral · dorsal',
   'À frente, a região frontal; atrás, a occipital; abaixo e nos lados, a temporal, '
   'pela linha temporal superior.',
   'Gálea aponeurótica sobre o osso parietal. Plano de deslizamento pouco vascularizado '
   'entre a gálea e o pericrânio.'),
  ('Região occipital', 'lateral · dorsal',
   'Abóbada posterior sobre o osso occipital, até a linha nucal superior, onde começa '
   'a região cervical posterior.',
   'Ventre occipital do occipitofrontal; nervo occipital maior e artéria occipital, '
   'que ascendem atravessando a inserção do trapézio.'),
  ('Região temporal', 'anterior · lateral · dorsal',
   'Acima, a linha temporal superior; abaixo, o arco zigomático, que a separa da '
   'região infratemporal.',
   'Músculo temporal na fossa temporal, sob a fáscia temporal. Artéria e veia temporais '
   'superficiais e nervo auriculotemporal sobem à frente do trago. A fossa é uma '
   'concavidade que se aprofunda com a idade.'),
  ('Região infratemporal', 'anterior · lateral',
   'Abaixo do arco zigomático, medialmente ao ramo da mandíbula. Na superfície, uma '
   'faixa estreita à frente do pavilhão auricular.',
   'Fossa infratemporal: músculos pterigóideos, artéria maxilar, plexo venoso '
   'pterigóideo e ramos do nervo mandibular. Região profunda, de acesso indireto.'),
  ('Região auricular', 'anterior · lateral · dorsal',
   'O pavilhão auricular e a área periauricular imediata.',
   'Cartilagem auricular; ramos da artéria auricular posterior e da temporal '
   'superficial; nervo auricular magno.'),
  ('Região mastóidea', 'lateral · dorsal',
   'Atrás do pavilhão, sobre o processo mastóideo; abaixo, a inserção do '
   'esternocleidomastóideo.',
   'Processo mastóideo — origem do esternocleidomastóideo. Ponto de reparo para a '
   'extremidade superior do músculo.'),
 ]),
 ('Face média', [
  ('Região orbital', 'anterior · lateral · inferior',
   'Acima, a margem supraorbital; abaixo, a margem infraorbital; medialmente, a raiz '
   'do nariz; lateralmente, o rebordo orbital lateral.',
   'Pálpebras e conteúdo orbital. Território da artéria oftálmica — a razão pela qual '
   'a região não tolera manobras que possam gerar fluxo retrógrado. Sulcos '
   'palpebrais e o sulco nasojugal medialmente.'),
  ('Região infraorbital', 'anterior · lateral · inferior',
   'Acima, a margem infraorbital; medialmente, a região nasal; lateralmente, a '
   'zigomática; abaixo, as regiões bucal e oral.',
   'Forame infraorbital, com o nervo e os vasos infraorbitais, cerca de um centímetro '
   'abaixo da margem orbital, na vertical da pupila. A artéria angular sobe medialmente, '
   'junto ao sulco nasojugal.'),
  ('Região nasal', 'anterior · lateral · inferior',
   'Raiz, dorso, ápice, asas e base do nariz, com as narinas.',
   'Artéria dorsal do nariz (ramo da oftálmica) e ramos nasais laterais e columelar da '
   'angular/facial — uma anastomose direta com a circulação oftálmica. Pele fina e '
   'aderente no dorso, espessa e sebácea no ápice.'),
  ('Região zigomática', 'anterior · lateral · inferior',
   'Sobre o osso e o arco zigomáticos; acima, as regiões orbital e temporal; '
   'medialmente, a infraorbital; abaixo, as regiões bucal e parotideomassetérica.',
   'Eminência malar — o ponto mais projetado do terço médio. Forames zigomaticofacial e '
   'zigomaticotemporal; a artéria transversa da face cruza a região horizontalmente.'),
 ]),
 ('Face inferior', [
  ('Região oral', 'anterior · lateral · inferior',
   'Acima, a base do nariz; lateralmente, os sulcos nasolabiais; abaixo, o sulco '
   'labiomentual.',
   'Orbicular da boca; artérias labiais superior e inferior, ramos da facial, correndo '
   'logo abaixo do vermelhão — o plano que define a profundidade segura no lábio. '
   'Colunas do filtro e arco do cupido definem o desenho.'),
  ('Região bucal', 'anterior · lateral · inferior',
   'Acima, as regiões infraorbital e zigomática; medialmente, a região oral; abaixo, a '
   'margem da mandíbula; lateralmente, a região parotideomassetérica.',
   'Bucinador e corpo adiposo da bochecha (bola de Bichat). A artéria e a veia faciais '
   'cruzam a região obliquamente; o ducto parotídeo perfura o bucinador na altura do '
   'segundo molar superior.'),
  ('Região parotideomassetérica', 'anterior · lateral · dorsal · inferior',
   'Acima, o arco zigomático; abaixo, a margem da mandíbula; atrás, o pavilhão '
   'auricular; à frente, a margem anterior do masseter.',
   'Glândula parótida e masseter. Os ramos do nervo facial emergem na margem anterior '
   'da glândula em leque; veia retromandibular e artéria transversa da face. É a região '
   'que define o contorno do ângulo mandibular.'),
  ('Região mentual', 'anterior · lateral · inferior',
   'Acima, o sulco labiomentual; lateralmente, continua-se com as regiões bucal e '
   'oral; abaixo, a margem inferior da mandíbula.',
   'Protuberância mentual, mentual e abaixador do lábio inferior. Forame mentual, com '
   'o nervo e os vasos mentuais, habitualmente abaixo do segundo pré-molar, a meia '
   'altura do corpo da mandíbula.'),
  ('Fossa retromandibular', 'lateral',
   'Entre a margem posterior do ramo da mandíbula, o processo mastóideo e a margem '
   'anterior do esternocleidomastóideo.',
   'Depressão que aloja o polo posterior da parótida e a veia retromandibular.'),
 ]),
 ('Pescoço', [
  ('Região esternocleidomastóidea', 'anterior · lateral · dorsal · inferior',
   'Sobre o músculo homônimo, do processo mastóideo e do occipital, acima, ao esterno e '
   'à clavícula, abaixo.',
   'Esternocleidomastóideo; profundamente, a bainha carotídea. A veia jugular externa '
   'cruza a face superficial do músculo obliquamente. No meio da margem posterior está '
   'o ponto nervoso do pescoço, onde emergem os ramos cutâneos do plexo cervical.'),
  ('Trígono submentual', 'lateral · inferior',
   'Entre os ventres anteriores dos digástricos e o corpo do hioide.',
   'Linfonodos submentuais; assoalho formado pelos milo-hióideos.'),
  ('Trígono submandibular', 'lateral · inferior',
   'Entre a margem inferior da mandíbula e os dois ventres do digástrico.',
   'Glândula submandibular, linfonodos, artéria facial ao emergir sob a mandíbula.'),
  ('Triângulo carótico', 'lateral · inferior',
   'Entre o esternocleidomastóideo, o ventre posterior do digástrico e o ventre '
   'superior do omo-hióideo.',
   'Bifurcação da carótida comum, veia jugular interna, nervo vago e alça cervical.'),
  ('Trígono muscular (omotraqueal)', 'anterior · lateral · inferior',
   'Entre a linha mediana do pescoço, o ventre superior do omo-hióideo e a margem '
   'anterior do esternocleidomastóideo.',
   'Músculos infra-hióideos, laringe, traqueia e glândula tireoide. A proeminência '
   'laríngea é o reparo de superfície mais evidente na morfologia masculina.'),
  ('Região cervical lateral', 'anterior · lateral · dorsal · inferior',
   'Entre a margem posterior do esternocleidomastóideo, a margem anterior do trapézio '
   'e a clavícula — o trígono posterior.',
   'Nervo acessório, ramos do plexo cervical e, na base, os troncos do plexo braquial e '
   'a artéria subclávia.'),
  ('Região cervical posterior', 'anterior · lateral · dorsal',
   'Atrás da margem anterior do trapézio, da linha nucal superior à base do pescoço — '
   'a nuca.',
   'Trapézio e musculatura nucal profunda; nervo occipital maior.'),
  ('Acidentes de superfície', 'dorsal · inferior',
   'Fossa jugular (supraesternal), fossa supraclavicular menor e maior, e a vértebra '
   'proeminente (C7).',
   'Reparos ósseos e depressões usados para orientar a descrição das regiões cervicais; '
   'a C7 é o primeiro processo espinhoso nitidamente palpável na nuca.'),
 ]),
]

# ============================================================ documento
CSS = """
:root{
 --papel:#F7F5F2; --papel2:#EFEBE5; --tinta:#1E2530; --tinta2:#454E5C;
 --tinta3:#6E7683; --linha:#D8D2C9; --carmim:#8E3B46; --carmim-fr:#F0E3E2;
 --pele:#E4C3AC; --pele-sh:#CFA48B; --pele-or:#DCB9A1;
 --sobranc:#4E3B2C; --iris:#6B5236; --pupila:#1A1410;
 --labio-s:#B87B72; --labio-i:#C68C82; --esclera:#FBF7F3;
}
@media (prefers-color-scheme:dark){
 :root:not([data-theme="light"]){
  --papel:#14181F; --papel2:#1B212A; --tinta:#E6E9EE; --tinta2:#B7BEC9;
  --tinta3:#8B93A0; --linha:#2C333E; --carmim:#C9707C; --carmim-fr:#33232A;
  --pele:#C79A80; --pele-sh:#A87A62; --pele-or:#BE8E75;
  --sobranc:#3A2C21; --iris:#4E3B26; --pupila:#0D0A08;
  --labio-s:#9E635C; --labio-i:#AE746B; --esclera:#EDE6DF;
 }
}
:root[data-theme="dark"]{
 --papel:#14181F; --papel2:#1B212A; --tinta:#E6E9EE; --tinta2:#B7BEC9;
 --tinta3:#8B93A0; --linha:#2C333E; --carmim:#C9707C; --carmim-fr:#33232A;
 --pele:#C79A80; --pele-sh:#A87A62; --pele-or:#BE8E75;
 --sobranc:#3A2C21; --iris:#4E3B26; --pupila:#0D0A08;
 --labio-s:#9E635C; --labio-i:#AE746B; --esclera:#EDE6DF;
}

*{box-sizing:border-box}
body{margin:0;background:var(--papel);color:var(--tinta);
 font:400 17px/1.62 Asap,system-ui,-apple-system,sans-serif;
 -webkit-font-smoothing:antialiased}
.env{max-width:1180px;margin:0 auto;padding:56px 28px 96px}
.col{max-width:65ch;margin:0 auto}

h1{font:600 clamp(30px,4.4vw,46px)/1.1 Spectral,Georgia,serif;
 letter-spacing:-.015em;margin:0 0 14px;text-wrap:balance}
.sub{font:400 19px/1.5 Spectral,Georgia,serif;color:var(--tinta2);margin:0 0 8px}
.meta{font:600 11.5px/1.5 'Asap Condensed',Asap,sans-serif;letter-spacing:.13em;
 text-transform:uppercase;color:var(--tinta3);margin:0}
.regua{height:1px;background:var(--linha);border:0;margin:34px 0}

h2{font:600 clamp(21px,2.5vw,27px)/1.22 Spectral,Georgia,serif;
 margin:52px 0 6px;letter-spacing:-.01em}
h3{font:600 12px/1.4 'Asap Condensed',Asap,sans-serif;letter-spacing:.14em;
 text-transform:uppercase;color:var(--carmim);margin:44px 0 14px}
p{margin:0 0 15px}
strong{font-weight:600}
em{font-style:italic;color:var(--tinta2)}

figure{margin:38px 0 0}
.prancha{display:block;width:100%;height:auto}
.pr-wrap{background:var(--papel2);border:1px solid var(--linha);border-radius:3px;
 padding:14px 8px;overflow-x:auto}
figcaption{font:400 14.5px/1.5 Asap,sans-serif;color:var(--tinta2);
 margin-top:13px;max-width:70ch}
figcaption b{font:600 11.5px/1.5 'Asap Condensed',Asap,sans-serif;
 letter-spacing:.13em;text-transform:uppercase;color:var(--carmim);
 display:block;margin-bottom:4px}

/* --- figura --- */
.pl{fill:var(--pele);stroke:var(--tinta);stroke-width:1.6;stroke-linejoin:round}
.orelha{fill:var(--pele-or);stroke:var(--tinta);stroke-width:1.5;stroke-linejoin:round}
.ln2,.ln3{fill:none;stroke:var(--tinta);stroke-linecap:round}
.ln2{stroke-width:1.2;opacity:.78}
.ln3{stroke-width:1;opacity:.42}
.sh{fill:var(--pele-sh);stroke:none;opacity:.32}
.brow{fill:var(--sobranc);stroke:none}
.olho{fill:var(--esclera);stroke:var(--tinta);stroke-width:1.2}
.lid{fill:none;stroke:var(--tinta);stroke-width:2.1;stroke-linecap:round}
.iris{fill:var(--iris)}
.pup{fill:var(--pupila)}
.lipup{fill:var(--labio-s);stroke:var(--tinta);stroke-width:1.1}
.liplo{fill:var(--labio-i);stroke:var(--tinta);stroke-width:1.1}
.rg,.rgl{fill:none;stroke:var(--tinta);stroke-width:1.2;opacity:.9;stroke-linecap:round}
.ld{fill:none;stroke:var(--tinta);stroke-width:.9;opacity:.66}
.an{fill:var(--carmim);stroke:var(--papel2);stroke-width:1}
.lb{font-family:'Asap Condensed',Asap,sans-serif;font-size:15.5px;fill:var(--tinta)}

/* --- glossario --- */
.gl{display:grid;gap:0;margin:20px 0 0;border-top:1px solid var(--linha)}
.gl-it{display:grid;grid-template-columns:minmax(180px,26%) 1fr;gap:0 30px;
 padding:20px 0;border-bottom:1px solid var(--linha)}
.gl-nome{font:600 17px/1.34 Spectral,Georgia,serif;margin:0}
.gl-vis{font:600 10.5px/1.5 'Asap Condensed',Asap,sans-serif;letter-spacing:.1em;
 text-transform:uppercase;color:var(--tinta3);margin:5px 0 0}
.gl-cp>p{margin:0 0 9px;font-size:16px}
.gl-cp>p:last-child{margin:0}
.gl-rot{font:600 10.5px/1.5 'Asap Condensed',Asap,sans-serif;letter-spacing:.11em;
 text-transform:uppercase;color:var(--carmim);margin-right:7px}
@media (max-width:720px){
 .gl-it{grid-template-columns:1fr;gap:9px}
 .env{padding:40px 20px 72px}
}

.nota{background:var(--papel2);border-left:2px solid var(--carmim);
 padding:19px 22px;margin:34px 0;border-radius:0 3px 3px 0}
.nota p{font-size:16px}
.nota p:last-child{margin:0}
.rod{margin-top:60px;padding-top:22px;border-top:1px solid var(--linha);
 font-size:14.5px;color:var(--tinta3)}
"""


def _glossario():
    out = ''
    for titulo, itens in GRUPOS:
        out += f'<h3>{html.escape(titulo)}</h3><div class="gl">'
        for nome, vistas, limites, conteudo in itens:
            out += (f'<div class="gl-it">'
                    f'<div><p class="gl-nome">{html.escape(nome)}</p>'
                    f'<p class="gl-vis">{html.escape(vistas)}</p></div>'
                    f'<div class="gl-cp">'
                    f'<p><span class="gl-rot">Limites</span>{limites}</p>'
                    f'<p><span class="gl-rot">De nota</span>{conteudo}</p>'
                    f'</div></div>')
        out += '</div>'
    return out


def documento():
    n_reg = sum(len(i) for _, i in GRUPOS)
    return f'''<title>Regiões da Face e do Pescoço</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Spectral:wght@400;600&family=Asap:wght@400;600&family=Asap+Condensed:wght@400;600&display=swap">
<style>{CSS}</style>

<div class="env">
 <div class="col">
  <p class="meta">Reologia do Ácido Hialurônico · material de referência</p>
  <h1>Regiões da face e do pescoço</h1>
  <p class="sub">Nomenclatura anatômica de superfície, em figura masculina,
   redesenhada a partir das pranchas de regiões da cabeça e do pescoço.</p>
  <hr class="regua">
  <p>Este livro localiza cada preenchedor por região: um produto de alto G′ é
   indicado para o <em>mento</em>, um de baixo G′ para a <em>região perioral</em>.
   Essa precisão só existe se região tiver um nome único e um limite definido —
   caso contrário “bochecha” e “região bucal” passam a nomear coisas diferentes
   para autor e leitor. O que segue fixa esse vocabulário: {n_reg} regiões e
   trígonos, com seus limites e o que corre por baixo de cada um.</p>
  <p>A figura foi redesenhada em morfologia masculina. O crânio é raspado por
   necessidade descritiva: as regiões frontal, parietal e temporal só se delimitam
   com o couro cabeludo à vista.</p>
 </div>

 <figure>
  <div class="pr-wrap">{RF.plate_anterior()}</div>
  <figcaption><b>Prancha I · vista anterior</b>
   Regiões da cabeça e do pescoço em vista anterior. Os limites em traço fino são
   convencionais — separam territórios descritivos, não estruturas visíveis na pele.
   As regiões bilaterais estão traçadas nos dois lados e nomeadas uma vez.</figcaption>
 </figure>

 <div class="col">
  <h2>Glossário das regiões</h2>
  <p>Cada entrada traz os <strong>limites</strong> que definem a região e o que há
   <strong>de nota</strong> sob ela — o que importa saber antes de introduzir volume
   ali. A coluna de vistas indica em quais projeções do atlas a região aparece.</p>
  {_glossario()}

  <div class="nota">
   <p><b>Sobre a masculinização da figura</b></p>
   <p>As pranchas de origem usam uma figura feminina. O redesenho alterou o que é
    dimorfismo real e nada mais: crânio mais quadrado com abóbada menos arredondada;
    largura bigonial maior em relação à bizigomática, com ângulo mandibular marcado;
    arco supraorbital reto e mais baixo, com supercílios mais horizontais; dorso nasal
    mais alto e reto; lábio superior mais longo e vermelhão mais fino; proeminência
    laríngea visível; esternocleidomastóideo mais definido. Os
    <strong>limites das regiões não mudam com o sexo</strong> — são os mesmos da
    prancha original.</p>
  </div>

  <div class="nota">
   <p><b>O que ainda não está desenhado</b></p>
   <p>O atlas de origem traz quatro projeções. Aqui está desenhada a
    <strong>vista anterior</strong> — a que corresponde às figuras já usadas no livro.
    As vistas <strong>lateral</strong>, <strong>dorsal</strong> e
    <strong>inferior</strong> estão cobertas no glossário, incluindo as regiões que só
    nelas aparecem (occipital, mastóidea, fossa retromandibular, os trígonos cervicais
    e os acidentes de superfície), mas ainda não têm prancha própria.</p>
  </div>

  <p class="rod">Nomenclatura conforme a <em>Terminologia Anatomica</em>.
   Figura e limites redesenhados em vetor — a prancha amplia sem perda de definição.
   As referências vasculares e nervosas são reparos anatômicos de superfície, não
   orientação de técnica.</p>
 </div>
</div>'''


if __name__ == '__main__':
    saida = pathlib.Path(__file__).resolve().parents[1] / 'docs' / 'regioes'
    saida.mkdir(parents=True, exist_ok=True)
    alvo = saida / 'regioes-da-face.html'
    alvo.write_text(documento(), encoding='utf-8')
    print(f'OK {alvo}  ·  {alvo.stat().st_size//1024} KB')
