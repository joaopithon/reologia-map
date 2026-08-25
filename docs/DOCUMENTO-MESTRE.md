# REOLOGY MAP
## Documento Mestre do Projeto
### Reologia do Ácido Hialurônico Aplicada à Seleção de Preenchedores Faciais — Aplicativo + Livro

**Autor do projeto:** Dr. João Pithon · Clínica Pithon Napoli (São Paulo/SP)
**Documento consolidado em:** 25/08/2026
**Fontes analisadas:** acervo completo do Google Drive do projeto (laudo BioSmart assinado, planilha de dados, REOLOGY MAP PT 1 e PT 2, APP: REOLOGY MAP, LIVRO DE REOLOGIA, PRODUÇÃO NO CHAT, pastas de áudios por produto) + referência de mercado declarada (PensaHOF).

> **O que é este documento:** a consolidação de todo o material de estudo já produzido em uma única fonte de verdade — a ciência, o banco de dados, o sistema de classificação, a especificação do aplicativo, a estrutura do livro, o fluxo de produção e o roadmap. É o documento-ponte entre o acervo bruto e os dois produtos finais (app e livro).

---

## 0. Sumário executivo

1. **O ativo central do projeto é único no mercado:** 76 géis comerciais de ácido hialurônico do mercado brasileiro, de 21 marcas, medidos **sob protocolo único** (reômetro TA Instruments AR-1500ex, 25 °C, varredura de 10 a 0,01 Hz) pela BioSmart Nanotechnology, com lote rastreado. Nenhum aplicativo, livro ou publicação disponível oferece comparação equivalente.
2. **O sistema interpretativo já existe e está maduro:** o "Mapa da Reologia" evoluiu em três camadas coerentes — (A) 5 classes de necessidade clínica, (B) 4 fenótipos visuais de produto, (C) sistema visual final por cor-base de G′ (🔵 <200 Pa · 🟡 200–300 · 🟣 ≥300) com modificadores — sob o lema **"A COR CLASSIFICA. O NÚMERO POSICIONA."**
3. **O conteúdo por produto está ~90% produzido:** as fichas de app dos produtos 1–71 existem; as monografias longas cobrem do 1 ao 71 (com pendências pontuais listadas no §13); o método de produção (questionários + áudios) está operando.
4. **O livro tem esqueleto completo (7 partes, 23 capítulos + atlas):** capítulos 1–2 escritos, 3 semi-escrito, material bruto forte para a Parte II; as Partes IV–VI dependem diretamente do conteúdo que o app também usará.
5. **Governança de dados é o próximo passo crítico:** a auditoria feita neste documento encontrou 3 pares de produtos com valores idênticos (provável erro de transcrição do laudo), 2 erros de tan δ impresso, 8 divergências de η* (incluindo uma troca de linhas entre Belotero Intense e Volume+ a 1 Hz) e divergências internas entre listas e fichas. Nada disso compromete o projeto — mas deve ser resolvido com a BioSmart **antes da publicação**.
6. **Recomendação de sequência:** (1º) fechar o banco de dados canônico auditado → (2º) MVP do app com Mapa interativo + fichas → (3º) motor de decisão guiada → (4º) 2ª rodada laboratorial (coesividade, swelling, amplitude) → (5º) livro completo, alimentado pelo mesmo banco.

---

## 1. Visão do projeto

O projeto nasce de uma pergunta clínica simples e ainda sem resposta padronizada: **diante de um paciente real — tecido, região, plano e objetivo definidos — qual gel de ácido hialurônico é o mais adequado, com base em dados mensuráveis e comparáveis?**

Hoje a escolha do preenchedor é guiada por três fontes imperfeitas:

1. **Material promocional dos fabricantes** — cada marca mede seus géis em protocolos diferentes (frequência, geometria, temperatura), tornando os números incomparáveis entre si.
2. **Literatura científica fragmentada** — os estudos clássicos cobrem poucos produtos, quase sempre os líderes globais, e raramente os portfólios realmente disponíveis no Brasil.
3. **Experiência pessoal** — valiosa, mas não transferível nem escalável.

O Reology Map ataca o problema pela raiz: **um único laboratório, um único reômetro, um único protocolo, 76 géis do mercado brasileiro medidos lado a lado** — e, sobre essa base, três produtos derivados:

| Produto | O que é | Público |
|---|---|---|
| **Banco de dados reológico** | 76 produtos × 6 frequências × 4 parâmetros, com lote rastreado | fundação dos outros dois |
| **Aplicativo Reology Map** | ferramenta de decisão clínica: região/objetivo/tecido → fenótipo reológico → produtos ranqueados com justificativa | injetores (médicos, dentistas HOF, biomédicos) |
| **Livro "Reologia do Ácido Hialurônico"** | obra de referência: da física dos géis ao atlas produto a produto | mesmo público + pós-graduações |

A frase de abertura definida para o app e o livro resume a filosofia:

> **"Não existe o melhor preenchedor. Existe a propriedade reológica mais adequada para o comportamento que queremos produzir em cada região."**

O diferencial competitivo não é o software nem o texto: **é o dado primário proprietário.** A referência de mercado citada pelo autor (PensaHOF — plataforma de apoio à decisão em harmonização orofacial, acesso por login em pensahof.com.br) valida a categoria "app de decisão clínica para injetores"; nenhum player da categoria, porém, possui banco reológico próprio multimarcas.

---

## 2. Inventário do acervo (Google Drive, 25/08/2026)

```
APLICATIVO/
├── DESCRIÇÃO DOS PREENCHEDORES/
│   ├── REOLOGY MAP PT 1                 Google Doc — mapa das 5 classes + monografias iniciais
│   ├── REOLOGY MAP PT 2./
│   │   └── REOLOGY MAP PT 2 – 62 EM DIANTE   Google Doc — monografias 63–71 (não há nº 62; caps. 66–67 duplicados)
│   ├── APP: REOLOGY MAP                 Google Doc (~927 mil caracteres) — fichas de app dos produtos 1–71,
│   │                                    sistemas de classificação, regras editoriais
│   ├── BS_Clinica_Pithon_Napoli_04082026_assinado 4.pdf   laudo BioSmart assinado (10 págs, Anexos 1 e 2)
│   └── Reologia_Preenchedores_Pithon_Napoli.xlsx          5 abas: Resumo · Dados Completos · Ranking · ChartData · Gráficos
└── INSTRUÇÕES/
    ├── PRODUÇÃO NO CHAT                 roteiros de 6 / 8 / 25 perguntas por produto
    ├── REOLOGIA BASICA/
    │   └── LIVRO DE REOLOGIA            estrutura completa do livro + capítulos 1–3 + material bruto
    └── AUDIOS/                          20 pastas por marca, numeradas por produto (0–71)
        ├── 0. GERAL/5 CLASSES DE AH/    áudio conceitual sobre as classes
        ├── 1-3 BELOTERO · 4-7 BIOGELIS · 8-10 EPTQ · 11-13 NEURAMIS · 14-16 YVOIRE
        ├── 17-19 PERFECTHA · 20-22 SAYPHA · 23 SINGDERM · 24-30 RESTYLANE · 31-34 UP ILIKIA
        ├── 35-39 REVANESSE · 40-46 JUVEDERM · 47-49 MILIMETRIC · 50-57 RENNOVA · 58 CUTEGEL
        └── 59-60 EVO · 61-65 SOFIDERM · 66-68 STYLAGE · 69-71 HYAFILIA
             (cada subpasta contém notas de voz WhatsApp .opus — respostas do autor aos questionários)
```

**Leitura do inventário:** o projeto já tem os três pilares de matéria-prima — dado primário (laudo + planilha), sistema interpretativo (PT 1/PT 2 + APP) e método de produção em escala (questionários + áudios, cuja numeração espelha as monografias). O pipeline áudio → transcrição → monografia → ficha de app está operante.

---

## 3. A base científica proprietária (estudo BioSmart)

### 3.1 Ficha do estudo

| Campo | Valor |
|---|---|
| Solicitante | Clínica Pithon Napoli LTDA (São Paulo/SP) |
| Executor | BioSmart Nanotechnology Ltda. — Incubadora Municipal de Araraquara/SP |
| Analista / Responsável técnico | Andressa Baggio Dias / Dr. Hernane da Silva Barud — CRQ 04168330 |
| Data do laudo | 04/08/2026 |
| Equipamento | Reômetro rotacional TA Instruments AR-1500ex (New Castle, EUA) |
| Condições | 25 °C · placas paralelas Ø 20 mm · gap 500 µm · amostra 0,6 mL |
| Ensaio | Varredura de frequência 10 → 0,01 Hz, 15 pontos por década |
| Parâmetros | G′, G″, tan δ, η* |
| Frequências reportadas | 10 · 5 · 1 Hz (Anexo 1) e 0,7 · 0,1 · 0,01 Hz (Anexo 2) |
| Amostras | 76 géis comerciais com lote registrado |

### 3.2 O que o estudo mede — e o que NÃO mede

O ensaio oscilatório de varredura de frequência caracteriza a **viscoelasticidade em pequenas deformações**: quanta estrutura elástica o gel tem (G′), quanto dissipa (G″), o balanço entre os dois (tan δ) e a resistência total ao fluxo (η*) — em cada velocidade de solicitação.

Ele **não mede**: coesividade, Swelling Factor, força de extrusão, resistência a grandes deformações (Strain X / amplitude sweep), resistência à compressão, duração clínica, integração tecidual ou capacidade de projeção in vivo. Essa fronteira é a **regra editorial inegociável** do projeto (§6.4): números de G′/G″/tan δ/η* vêm exclusivamente do laudo BioSmart; dados de fabricante são sempre rotulados como tal; propriedades não mensuradas jamais são "deduzidas".

### 3.3 Cobertura do banco

76 produtos de 21 marcas/famílias:

Restylane (9) · Rennova (8) · Juvéderm (7) · Revanesse (5) · Sofiderm (5) · Biogelis (4) · UP/Ilikia (4) · Belotero (3) · e.p.t.q (3) · Hyafilia (3) · Milimetric (3) · Neuramis (3) · Perfectha (3) · Saypha (3) · Stylage (3) · Yvoire (3) · Evofill (2) · Neauvia (2) · Cutegel (1) · Finahfil (1) · Singderm (1)

Inclui **dois lotes distintos de Restylane Lido** (22647 e 27003) — decisão metodologicamente rica, pois documenta variabilidade inter-lote real (§6.2).

---

## 4. Fundamentos: os quatro números e o que significam na face

*(Versão condensada do que o livro desenvolve nas Partes I–II.)*

### 4.1 G′ — módulo de armazenamento (elástico)
Energia que o gel **armazena e devolve** quando deformado; a "mola". Clinicamente: capacidade de manter forma sob carga — sustentação, projeção, definição. No banco (0,7 Hz): de **33,64 Pa** (Belotero Balance) a **935,94 Pa** (Restylane Shaype) — amplitude de **28×** dentro do mesmo rótulo "preenchedor de AH". Unidade: Pascal (1 Pa = 1 N/m²).

### 4.2 G″ — módulo de perda (viscoso)
Energia que o gel **dissipa** como atrito interno; o "amortecedor". Participa da acomodação ao movimento e da sensação de escoamento. Deve sempre ser lido **em relação ao G′** — G″ alto em valor absoluto não significa gel "dinâmico" (Hyafilia V tem G″ 122,77 Pa e é o segundo gel mais estrutural do banco).

### 4.3 tan δ = G″/G′ — o balanço
- tan δ < 1: caráter predominantemente elástico (gel) · tan δ > 1: predominantemente viscoso (líquido).
- No banco a 0,7 Hz: de **0,07** (Volux, Rennova Lift Plus, Saypha Volume Plus) a **0,69** (Belotero Balance). Quartis: 0,15 · 0,20 · 0,27.
- Distinção-chave do projeto: **predominância elástica ≠ magnitude elástica** (Defyne: tan δ 0,08 com G′ 293 Pa; Volux: tan δ 0,07 com G′ 669 Pa — mesma predominância, capacidades estruturais muito diferentes).

### 4.4 η* — viscosidade complexa
Resistência global ao fluxo oscilatório; cresce dramaticamente em baixa frequência. A 0,01 Hz vai de ~164 Pa·s (Balance) a ~11.451 Pa·s (Shaype) — proxy de "o quanto o gel permanece onde foi colocado" dentro dos limites do ensaio (não substitui coesividade).

### 4.5 Frequência é movimento facial — a chave de leitura clínica

| Frequência | Analogia clínica |
|---|---|
| 10–5 Hz | gestos rápidos: fala rápida, mastigação vigorosa, sorriso explosivo |
| 1–0,7 Hz | mímica habitual — **0,7 Hz é a frequência de referência editorial do projeto** |
| 0,1 Hz | expressões lentas, transições |
| 0,01 Hz | repouso — o gel "parado" sob carga estática |

Exemplos reais do banco (G′ Pa / tan δ):

| Produto | 10 Hz | 1 Hz | 0,7 Hz | 0,01 Hz | Leitura |
|---|---|---|---|---|---|
| Belotero Balance | 78 / 0,90 | 38 / 0,70 | 34 / 0,69 | 9 / 0,50 | quase líquido em qualquer regime → integração máxima |
| Juvéderm Skinvive | 178 / 0,28 | 110 / 0,51 | 102 / 0,54 | 17 / **1,54** | único gel do banco que cruza para líquido em repouso → espalha e hidrata, não sustenta |
| Restylane Refyne | 129 / 0,50 | 86 / 0,31 | 82 / 0,29 | 52 / 0,19 | flexível no movimento, estável no repouso |
| Juvéderm Voluma | 383 / 0,13 | 367 / 0,09 | 363 / 0,09 | 270 / 0,17 | elástico e estável em todos os regimes |
| Juvéderm Volux | 748 / 0,08 | 676 / 0,07 | 669 / 0,07 | 522 / 0,16 | máxima predominância elástica prática |
| Restylane Shaype | 1146 / 0,12 | 961 / 0,15 | 936 / 0,15 | 709 / 0,17 | o teto estrutural do banco |

O caso Skinvive (tan δ > 1 em repouso) demonstra por que **um único número não descreve um gel**: a 10 Hz parece um filler comum (G′ 178 Pa); a 0,01 Hz revela-se um líquido hidratante — exatamente o comportamento desejado de um skinbooster, e exatamente o que o desqualifica para sustentação. É a "fotografia × filme": *"Enquanto o G′ em uma frequência isolada mostra uma fotografia do comportamento do gel, o sweep de frequência mostra o filme."*

---

## 5. O banco de dados: retrato do mercado brasileiro em números

### 5.1 Panorama estatístico (0,7 Hz)
- **G′:** mín 33,64 · P25 147,9 · mediana 251,7 · P75 352,3 · P90 544,6 · máx 935,94 Pa
- **tan δ:** mín 0,07 · P25 0,15 · mediana 0,20 · P75 0,27 · máx 0,69
- **η*:** ~8,8 a ~205 Pa·s a 0,7 Hz; ~164 a ~11.451 Pa·s a 0,01 Hz
- Classificação de 3 níveis da planilha: 60 "Muito elástico (sustentação)" · 10 "Moderadamente elástico" · 6 "Predomínio viscoso (fluido)"

### 5.2 Leituras que só um banco unificado permite
1. **Amplitude de ~28× em G′**: "preenchedor de AH" designa materiais tão diferentes quanto um sérum viscoso e uma borracha densa.
2. **G′ e tan δ são eixos independentes**: Restylane Volyme (137,7 Pa / 0,16) é pouco rígido porém francamente elástico; Hyafilia V (840,5 Pa / 0,15) é rígido com a mesma proporção. O par informa mais que qualquer número isolado.
3. **Famílias comerciais têm escada interna visível e verificável**: Milimetric PRO Leve → Moderado → Intenso (56 → 72 → 170 Pa); e.p.t.q S100 → S300 → S500 (70 → 226 → 355 Pa); Saypha Filler → Volume → Volume Plus (143 → 252 → 489 Pa, com tan δ 0,24 → 0,12 → 0,07); Stylage Lips → L → XL (167 → 260 → 305 Pa); Hyafilia Soft → Mold → Volume (284 → 526 → 841 Pa — mesma concentração de 20 mg/mL, três magnitudes: "MESMA CONCENTRAÇÃO. TRÊS MAGNITUDES MECÂNICAS COMPLETAMENTE DIFERENTES").
4. **A escada nem sempre segue o marketing**: Sofiderm Derm Plus tem a 2ª maior partícula declarada da família (1500 µm) e o **menor** G′ da família (122 Pa) — "PARTÍCULA MAIOR NÃO SIGNIFICA MAIOR ELASTICIDADE".
5. **Posicionamentos idênticos escondem físicas diferentes**: os "volumizadores" variam de 252 Pa (Belotero Volume+) a 936 Pa (Shaype) — quase 4×. E assinaturas quase idênticas aparecem em produtos de propostas distintas (Hyafilia Soft 283,77/59,07/0,21 × Cutegel CL-Max 282,48/56,87/0,20 — G′ difere <0,5%): "MESMA ASSINATURA NÃO SIGNIFICA MESMO PRODUTO", pois coesividade, SF, arquitetura e partícula podem diferir.

### 5.3 Extremos do banco (0,7 Hz)

| Posição | Produtos | Valores |
|---|---|---|
| Mais fluidos (menor G′) | Belotero Balance · Up Fine · Milimetric PRO Leve | 33,6 · 33,7 · 56,3 Pa |
| Mais estruturados (maior G′) | Restylane Shaype · Hyafilia V Plus · Restylane Lido (27003) | 935,9 · 840,5 · 800,1 Pa |
| Mais elásticos (menor tan δ) | Juvéderm Volux · Rennova Lift Plus · Saypha Volume Plus | 0,07 |
| Mais dissipativos (maior tan δ) | Belotero Balance · Milimetric PRO Leve · e.p.t.q S100 | 0,69 · 0,57 · 0,56 |

A tabela completa dos 76 produtos está no **Anexo A**; os dados canônicos legíveis por máquina estão em `data/reologia_produtos_full.json` e `data/reologia_produtos_07hz.csv` neste repositório.

---

## 6. Governança e integridade de dados

A credibilidade do projeto depende de tratar o próprio dado com o rigor que se cobra dos fabricantes. Auditoria completa realizada sobre laudo + planilha (76 produtos × 6 frequências = 456 medições):

### 6.1 Três pares com assinaturas idênticas (re-verificar com a BioSmart)

| Par | Evidência | Hipótese |
|---|---|---|
| Juvéderm Volift × Juvéderm Voluma | valores idênticos em **todas** as 6 frequências (lotes distintos: 1003113042 × 1003471713) | erro de transcrição (24 valores idênticos por coincidência é improvável) |
| Belotero Volume+ × Neauvia Intense | idênticos a 0,7 Hz (252,61/57,31/0,23); a 1 Hz diferem levemente | duplicação parcial de linhas no Anexo 2 |
| Neauvia Stimulate × Singderm | idênticos a 0,7 e 10 Hz (285,83/78,16/0,27) | idem |

### 6.2 Dois lotes de Restylane Lido — variabilidade inter-lote real
Lote 22647: G′ 617,71 Pa · lote 27003: G′ 800,09 Pa (0,7 Hz) — **~30% de diferença no mesmo produto.** Em vez de fragilidade, é um achado editorial: nenhum concorrente documenta variabilidade de lote. Tratamento: reportar ambos com lote explícito e usar como argumento da cultura "número com lote e protocolo, ou não é número".

### 6.3 Auditoria aritmética interna (feita neste documento)
- **tan δ impresso × G″/G′ recalculado** — 2 divergências em 456 medições:
  - Perfectha Subskin @ 0,7 Hz: impresso 0,20 · calculado **0,152** (provável erro tipográfico; corrigir para ~0,15 — muda a leitura do produto de "borderline verde" para francamente elástico);
  - Restylane Lido 22647 @ 10 Hz: impresso 0,30 · calculado 0,253.
- **η* × |G*|/ω recalculado** — 8 divergências >15%, destacando-se:
  - **Belotero Intense × Belotero Volume+ @ 1 Hz: valores de η* trocados entre si** (42,96 ↔ 33,09) — troca de linha evidente;
  - Neuramis Lido @ 5 Hz (16,36 vs ~4,73) e Restylane Volyme @ 5 Hz (22,87 vs ~5,61 — o valor de 1 Hz aparece duplicado na coluna de 5 Hz);
  - Up Fine, Up Deep e Up Max @ 0,7 Hz: todos ~29% acima do esperado, **mesmo fator sistemático** (~1,293) — sugere ponto de frequência ou coluna deslocada só nesses três.
- **Ação:** solicitar à BioSmart os arquivos brutos do reômetro dessas amostras e emitir errata do laudo antes de qualquer publicação. Até lá, essas linhas carregam flag `verificar_dado` no banco.

### 6.4 Regra das três fontes (norma editorial permanente)
1. **BioSmart (dado primário):** G′, G″, tan δ, η*, lote, protocolo — única fonte de números reológicos. Números de fabricantes ou artigos medidos em outros protocolos **não entram no banco** (regra repetida em todas as monografias).
2. **Fabricante/distribuidor (dado declarado, sempre com asterisco):** concentração, partícula, crosslinker, tecnologia (MCLPE, IPN-Like, CHA-HEART, Vycross, NASHA…), apresentações, indicações de bula, duração comercial, aderência, força de injeção.
3. **Não mensurado (proibido deduzir):** coesividade, swelling, extrusão, strain, compressão, duração real, integração — entram apenas como camada qualitativa declarada/opinião do autor, com marcador 💧 "SF NÃO MEDIDO" e congêneres.

### 6.5 Divergências internas listas × fichas (resolver na consolidação do banco)
O documento do app contém, em alguns produtos, valores diferentes entre a lista inicial de classes e a ficha individual: Belotero Balance (tan δ 0,69 na lista × 0,37 na ficha), Biogelis Global (177,40/0,19 × 166,98/0,25), Restylane Kysse (178,82/0,14 × 230,00/0,26), Yvoire Classic+ (319,88/0,14 × 392,35/0,19), Yvoire Volume+ (358,50/0,16 × 524,61/0,17). **Fonte da verdade = planilha/laudo Anexo 2 a 0,7 Hz** (colunas conferidas nesta auditoria): Balance 33,64/23,23/**0,69** · Biogelis Global **177,40/33,77/0,19** · Kysse **178,82/24,53/0,14** · Yvoire Classic+ **319,88/45,65/0,14** · Yvoire Volume+ **358,50/55,99/0,16**. As fichas divergentes provavelmente absorveram valores de outra frequência (ex.: Kysse a 10 Hz = 230,00/60,65/0,26; Yvoire Classic+ a 10 Hz = 392,35/75,78/0,19) — corrigir todas para o Anexo 2 @ 0,7 Hz.

### 6.6 Erros menores a corrigir
- Lote do Juvéderm Skinvive gravado como notação científica ("1,00309E+11") — recuperar o literal da caixa.
- Rennova Fill e Rennova Fill Eyes Lines com o mesmo lote (YLA25503), padrão de lote típico e.p.t.q/Jetema — conferir contra as caixas físicas.
- Yvoire Volume+ presente nos Anexos com dados, mas ausente da Tabela 1 do laudo e sem lote ("N/D") — pedir errata.
- Grafia oficial "Restylane Shaype™" (produto novo, NASHA HD) — manter, não "Shape".
- Concentração do Rennova Lift Plus divergente entre fontes oficiais (24 × 25 mg/mL; lido 0,3 × 0,32%) — fixar pela IFU do lote ensaiado.
- Documento PT 2: não existe monografia nº 62 e os caps. 66–67 são duplicatas verbatim (Stylage Special Lips) — renumerar.
- Produtos citados sem ensaio BioSmart (não atribuir números): Evofill Fine Lines, Rennova Fill Soft Lips, Cutegel CL-S/CL-N/CL-Max 1400.

### 6.7 Frequência de referência — decisão formalizada
- As monografias e o app adotam **0,7 Hz (Anexo 2)** como frequência comparativa exclusiva: *"0,7 Hz É A NOSSA REFERÊNCIA PADRONIZADA DE COMPARAÇÃO, NÃO UM 'G′ UNIVERSAL' DO PRODUTO."*
- A aba Resumo da planilha usa 1 Hz nos rankings ("Top 15") — **reprocessar os rankings para 0,7 Hz** e manter 1 Hz apenas como coluna de compatibilidade com a literatura.
- Recomendação adicional: nas fichas do app, exibir sempre o par **0,7 Hz (movimento) + 0,01 Hz (repouso)** — diferencia produtos que um único ponto esconde (caso Skinvive).

---

## 7. O Mapa da Reologia — o sistema de classificação

O coração intelectual do projeto. O sistema evoluiu em **três camadas complementares** (não versões rivais — o app usa as três):

### 7.1 Camada A — As 5 classes de necessidade clínica ("espinha dorsal")
Classifica **o que a região/tarefa pede**, não o produto:

| Classe | O que buscamos | Função clínica | Regiões típicas | Frase de decisão |
|---|---|---|---|---|
| 1. 🔵 Baixo G′ | menor módulo elástico | espalhamento, integração, baixo relevo | fronte, glabela, têmporas, supercílio | "quando queremos preencher sem criar relevo" |
| 2. ⚫ Alto G′ | maior módulo elástico | estrutura, projeção, manutenção de forma | nariz, mento, mandíbula, arco zigomático | "quando precisamos construir e manter estrutura" |
| 3. 🟡 Baixo Swelling Factor | baixa expansão pós-hidratação | previsibilidade volumétrica | **olheiras** | "quando poucos décimos de mL de expansão mudam o resultado" |
| 4. 🔴 Alto tan δ | maior componente dissipativa | adaptação a deformação e movimento | lábios e perioral | "quando o produto precisa acompanhar grande dinâmica" |
| 5. 🟢 Alta coesividade + volumização | gel que permanece íntegro como massa | reposição volumétrica integrada | sulco nasolabial, labiomentoniano, crown lifting, bochecha | "preencher e manter volume" |

Regras: a classe 5 não depende de um único número; **uma região pode pertencer a mais de uma classe conforme o objetivo** (bochecha volumétrica ≠ zigoma projetivo; corpo do mento ≠ vértice do mento).

### 7.2 Camada B — Fenótipos visuais dos produtos
Classifica **os 76 produtos** pelo comportamento medido. Das 9 combinações teóricas de cores, o banco real ocupa apenas 4 famílias:

| Fenótipo | Nome | Frase-verbo | N | % |
|---|---|---|---|--:|
| 🔵🌸 baixo G′ + dinâmico | INTEGRATIVO DINÂMICO | **ESPALHA + ACOMPANHA** | 34 | 44,7% |
| 🟡 G′ intermediário | PREENCHEDOR | **PREENCHE** | 14 | 18,4% |
| 🟣 alto G′ | ESTRUTURAL | **SUSTENTA / PROJETA** | 18 | 23,7% |
| 🟣🟢 alto G′ + maleável | ESTRUTURAL MALEÁVEL | **SUSTENTA + MOLDA** | 10 | 13,2% |

Na 1ª iteração (REOLOGY MAP PT 1) o grupo azul era subdividido em 🔵🌸 puro (28 produtos) e 🔵🟡🌸 "com mais corpo" (6: Skinvive, Revanesse Kiss, Evofill Derm, Up Deep, Belotero Intense, Evofill Ultra Deep) — os **dois fenótipos labiais** (natural/integrador × dinâmico com mais corpo). A consolidação em 4 famílias foi decisão posterior de simplificação para o app; a nuance labial permanece nas fichas.

Achado conceitual do fenótipo 🟣🟢: **"ALTO G′ NÃO SIGNIFICA NECESSARIAMENTE UM GEL EXCLUSIVAMENTE PROJETOR"** — existe estrutura modelável (Lyft, Restylane clássico, Restylane Skinbooster, Hyafilia M, e.p.t.q S500, Biogelis Volumax, Perfectha Subskin, UP Max, Yvoire Volume+).

Composição completa das 4 famílias (0,7 Hz, G′ Pa · tan δ):

**🔵🌸 Integrativo dinâmico (34):** Belotero Balance 33,64·0,69 · Up Fine 33,66·0,36 · Milimetric PRO Leve 56,26·0,57 · e.p.t.q S100 70,35·0,56 · Milimetric PRO Moderado 72,44·0,48 · Rennova Fill Fine Lines 81,53·0,53 · Restylane Refyne 81,57·0,29 · Rennova Fill Eyes Lines 87,38·0,52 · Neuramis 89,70·0,38 · Juvéderm Skinvive 102,26·0,54 · Juvéderm Ultra XC 110,75·0,34 · Rennova Fill 118,08·0,35 · Sofiderm Derm Plus 122,17·0,25 · Revanesse Ultra+ 127,76·0,31 · Revanesse Kiss 131,06·0,39 · Restylane Volyme 137,69·0,16 · Revanesse Contour+ 142,29·0,28 · Saypha Filler 142,61·0,24 · Sofiderm Derm 146,72·0,21 · Revanesse Outline+ 148,24·0,22 · Sofiderm Fine Lines 151,88·0,25 · Juvéderm Ultra Plus XC 161,39·0,24 · Evofill Derm 162,47·0,35 · Neuramis Deep 164,47·0,27 · Stylage Lips 167,01·0,21 · Milimetric PRO Intenso 170,32·0,27 · Revanesse Shape+ 172,61·0,18 · Up Deep 172,67·0,18 · Biogelis Fine Lines 176,94·0,20 · Biogelis Global 177,40·0,19 · Restylane Kysse 178,82·0,14 · Rennova Deep Line 183,33·0,17 · Belotero Intense 186,11·0,33 · Evofill Ultra Deep 199,67·0,29

**🟡 Preenchedor intermediário (14):** Rennova Ultra Volume 221,87·0,15 · Sofiderm Deep 223,11·0,19 · e.p.t.q S300 226,00·0,23 · Biogelis Volume 251,51·0,19 · Saypha Volume 251,93·0,12 · Juvéderm Volbella 252,50·0,16 · Belotero Volume+ 252,61·0,23 · Neauvia Intense 252,61·0,23 · Rennova Lift 253,59·0,11 · Stylage L 260,15·0,16 · Cutegel CL-Max 282,48·0,20 · Hyafilia S Plus (Soft) 283,77·0,21 · Neauvia Stimulate 285,83·0,27 · Singderm 285,83·0,27

**🟣 Estrutural (18):** Restylane Defyne 292,62·0,08 · Stylage XL 305,08·0,15 · Neuramis Volume 314,05·0,15 · Yvoire Classic+ 319,88·0,14 · UP Contour 328,48·0,15 · Sofiderm Derm Sub-Skin 330,84·0,14 · Finahfil Intense 338,51·0,11 · Juvéderm Volift 362,97·0,09 · Juvéderm Voluma 362,97·0,09 · Perfectha Deep 386,46·0,12 · Rennova Lips Plus 401,97·0,18 · Perfectha Derm 440,68·0,11 · Rennova Lift Plus 475,85·0,07 · Saypha Volume Plus 488,91·0,07 · Yvoire Contour+ 579,90·0,10 · Juvéderm Volux 669,12·0,07 · Hyafilia V Plus (Volume) 840,54·0,15 · Restylane Shaype 935,94·0,15

**🟣🟢 Estrutural maleável (10):** Perfectha Subskin 343,00·0,15* · UP Max 351,32·0,21 · e.p.t.q S500 355,13·0,19 · Yvoire Volume+ 358,50·0,16 · Biogelis Volumax 385,93·0,19 · Hyafilia M Plus (Mold) 526,31·0,16 · Restylane Skinbooster 562,82·0,26 · Restylane Lido 22647 617,71·0,26 · Restylane Lyft 718,22·0,18 · Restylane Lido 27003 800,09·0,26
*(tan δ do Perfectha Subskin corrigido pela auditoria §6.3.)*

### 7.3 Camada C — Sistema visual final ("A COR CLASSIFICA. O NÚMERO POSICIONA.")
Consolidado nas monografias mais recentes:

- **Cor-base = faixa de G′ a 0,7 Hz** (cortes operacionais internos do banco, não universais):
  - 🔵 **< 200 Pa** → INTEGRA (espalha, menor relevo)
  - 🟡 **200–299,99 Pa** → PREENCHE (*"o amarelo é a cor do vale"*)
  - 🟣 **≥ 300 Pa** → SUSTENTA / PROJETA
- **Modificadores:**
  - 🌸 rosa = participação dissipativa relativa destacada (na prática do banco, tan δ ≳ 0,26; 0,15–0,21 explicitamente NÃO recebe rosa)
  - 🟢 verde = maleabilidade/coesividade — **somente como dado clínico-tecnológico declarado, com asterisco; nunca derivado do frequency sweep**
  - 💧/🟠 = **Swelling Factor não medido** (marcador obrigatório de honestidade)
- Regras de leitura: "MESMA COR NÃO SIGNIFICA MESMA INTENSIDADE" (Stylage XL 305 Pa e Shaype 936 Pa são ambos roxos — "STYLAGE XL É ROXO, MAS ESTÁ NO INÍCIO DO TERRITÓRIO ROXO"); "O ESPECTRO É CONTÍNUO. A COR SIMPLIFICA."; critério de produto "equilibrado": G′ ≥ 200 + tan δ ≥ 0,21.

### 7.4 A gramática de tarefas geométricas
Cada depósito tem uma tarefa tridimensional — a camada que conecta o mapa à técnica:

| Tarefa | Descrição | Cor típica |
|---|---|---|
| **LINHA** | microdepressão superficial | 🔵 |
| **VALE** | depressão (sulco, pré-jowl, marionete) | 🟡 |
| **CURVA** | convexidade difusa (malar, bochecha, têmpora) | 🟡/🟣 |
| **SUPORTE** | sustentação profunda (fossa piriforme, supraperiostal) | 🟣 |
| **VÉRTICE** | projeção focal (ponta do mento, zigoma, ângulo mandibular) | 🟣 |

No corpo: DEPRESSÃO / TRANSIÇÃO / CURVA / RELEVO / VÉRTICE. Dicotomias estruturantes: **volumizar ≠ projetar** ("ULTRA VOLUME VOLUMIZA. LIFT PLUS PROJETA."), **curva ≠ vértice**, **sustentar ≠ projetar**.

### 7.5 Sequência decisória canônica

> **ANATOMIA → DEFEITO → OBJETIVO → PLANO → PRODUTO → VOLUME → TÉCNICA**

O produto é a 5ª decisão, não a 1ª. O app impõe essa ordem na jornada de decisão guiada.

### 7.6 As anti-inferências (o "código de honestidade" do sistema)
O que um número NÃO diz — regras repetidas monografia a monografia:

- G′ ≠ coesividade · G′ ≠ volumização · G′ ≠ lifting · G′ ≠ força de extrusão · G′ não define plano · **G′ não é segurança vascular**
- tan δ ≠ fluidez/espalhamento · G″ alto ≠ gel dinâmico (ler sempre em relação ao G′)
- baixo G′ ≠ baixo SF · alto G′ ≠ alto SF · **swelling do gel ≠ edema clínico**
- concentração ≠ reologia · partícula ≠ G′ · tecnologia/reticulante ≠ faixa de G′ (NASHA ≠ alto G′; DVS ≠ alto G′)
- **nome comercial ≠ reologia** ("SOFT NÃO É AZUL" — Hyafilia Soft 283,77 Pa; "'Contour' não significa alto G′"; "'Plus' não significa mais G′")
- evidência clínica ≠ causalidade reológica · indicação comercial ≠ adequação reológica · registro de estudo ≠ resultado publicado
- correlação intramarca ≠ causalidade universal · "reologia ajuda a escolher a ferramenta; não calcula os mililitros necessários"

---

## 8. Reologia clínica: região × exigência × produtos

Síntese do mapeamento região → classe de necessidade → produtos nomeados nas monografias (níveis: **1ª escolha → forte → boa → seletiva → não priorizar → não indicar quando a IFU contraindica**). Sempre sob a regra: **reologia não substitui IFU nem segurança anatômica.**

| Região | Necessidade | 1ªs escolhas e fortes (das monografias) |
|---|---|---|
| Fronte / glabela / supercílio | 🔵 baixo relevo | Neuramis Lido (1ª fronte), Restylane Refyne (1ª reológica), Biogelis Fine Lines, UP Fine — glabela sempre com alerta vascular máximo |
| Têmporas | 🔵/🟡 + coesividade | Belotero Volume+ (1ª), Refyne (fanning SC), Volyme, Voluma, Stylage XL |
| Olheiras | 🟡 baixo SF + precisão volumétrica | Yvoire Contour+ (1ª), Perfectha Subskin (1ª), Restylane Lyft (projeção + precisão), Rennova Fill Eyes Lines (1ª da linha) — concentração ideal ~20 mg/mL; **nunca escolher pelo G′**; "o tamanho da partícula ajuda a explicar; o SF medido é o que confirma" |
| Lábios — dinâmica/integração | 🔴 alto tan δ | Restylane Kysse (1ª), Neuramis Deep (1ª da linha), Revanesse Kiss (1ª), e.p.t.q S100 (delicado), Belotero Intense (1ª), Stylage Special Lips, Evofill Derm, Juvéderm Ultra XC |
| Lábios — estrutura/contorno | 🟣 seletivo | Rennova Lips Plus (contorno/arco/projeção), Volbella (precisão elástica) — "FILLER LABIAL PODE SER AZUL OU ROXO"; "NÃO EXISTE UM ÚNICO tan δ 'LABIAL'" (banco labial: tan δ 0,14 a 0,39) |
| Sulco nasolabial | 🟢 vale + coesividade | Biogelis Volume (1ª), Rennova Deep Line (1ª), Rennova Lift (1ª), Stylage L (1ª — RCT NICE de não-inferioridade vs Juvéderm Ultra 3), Cutegel CL-Max (1ª), Sofiderm Derm (1ª), Defyne, Singderm, S300; alternativa estratégica: tratar o suporte adjacente (fossa piriforme/terço médio) |
| Marionete / labiomentoniano | 🟡/🟢 adaptação | S300, Saypha Filler, Singderm, Deep Line, Fill, Outline+, Milimetric Moderado/Intenso |
| Malar / bochecha (volume difuso) | 🟢 curva | Volyme (1ª), Voluma (1ª), Belotero Volume+, Biogelis Volume, Saypha Volume, UP Max, Sofiderm Deep, Stylage XL |
| Zigoma (projeção focal) | ⚫ vértice | Lyft (1ª), Volumax, S500, Neuramis Volume, Saypha Volume Plus, UP Contour, Yvoire Volume+, Volux, Hyafilia V |
| Mento | ⚫ corpo × vértice | vértice: Volux, Shaype (indicação oficial), Lift Plus, Saypha Volume Plus, Hyafilia V, Lyft · corpo: Ultra Volume, Sofiderm Deep, Stylage XL, Hyafilia Mold ("MOLD = MENTO MODELADO; VOLUME = MENTO PROJETADO") |
| Mandíbula / ângulo | ⚫ linha + vértice | Lyft (1ª), Volux (1ª — indicação oficial), Lift Plus, UP Contour, Hyafilia V/Mold, Stylage XL |
| Pré-jowl | vale × linha | preencher o vale: Deep Line, Fill, Sofiderm Derm · construir a linha: Lift Plus, Volux, UP Contour |
| Fossa piriforme | 🟣 suporte profundo | Volumax, S500, Neuramis Volume, Saypha Volume/Plus, Sofiderm Deep, Hyafilia Mold — com alerta vascular |
| Nariz | ⚫ projeção | **nunca 1ª escolha automática** — racional reológico (Volux, Shaype, Lift Plus, S500) sempre subordinado a risco vascular e treinamento: "G′ NÃO É SEGURANÇA VASCULAR" |
| Qualidade de pele | integrar | Skinvive (1ª — microdepósitos intradérmicos; a "terceira função" do AH: PROJETAR / VOLUMIZAR / **INTEGRAR** — "TRATAR O TECIDO, NÃO CRIAR UMA NOVA PROJEÇÃO") |
| Corporal | adaptação × estrutura | Sofiderm Derm Plus (pós-lipo, cicatrizes, marcação abdominal, precisão) × Sub-Skin (glúteos, hip dips, contorno estrutural) — "NÃO EXISTE UMA ÚNICA REOLOGIA DO PREENCHEDOR CORPORAL" |

Este quadro se funde com o **Mapa Reológico Facial** do livro (§10.2) — que adiciona os eixos coesividade/swelling/integração — numa única **matriz canônica**, a "tabela-mãe" do motor de recomendação do app.

---

## 9. O aplicativo Reology Map — especificação funcional

### 9.1 Conceito
O profissional descreve **região, objetivo, plano e tecido do paciente** e recebe **produtos ranqueados com justificativa reológica transparente** — cada recomendação mostra os números que a sustentam e a fonte de cada informação. Público: médicos, cirurgiões-dentistas (HOF), biomédicos e farmacêuticos habilitados; pós-graduandos. Tom: científico-visual, "aprende enquanto decide".

### 9.2 Os dois modos de uso
1. **DECIDIR** (wizard na sequência canônica §7.5): região → defeito/objetivo → plano → tecido ⇒ ranking com "por quê".
2. **EXPLORAR** (mapa vivo): scatter interativo **G′ × tan δ** com as cores do Mapa; alternador de frequência (0,7 Hz padrão · 0,01 Hz repouso); filtros por marca, classe, faixa de G′ e "meu armário".

### 9.3 A ficha de produto (estrutura padrão — já definida e aplicada aos produtos 1–71)
1. Nome + fabricante/tecnologia/concentração (fonte: fabricante, com asterisco)
2. **DESCRIÇÃO** e **MELHOR PARA**
3. **PRINCIPAL DIFERENCIAL**
4. **PERFIL REOLÓGICO 0,7 Hz** — G′ / G″ / tan δ + tags (+ curva das 6 frequências)
5. **INTERPRETAÇÃO** ("o que os números mostram")
6. **COMPORTAMENTO CLÍNICO** — escala visual ●●● / ●●○ / ●○○ (integração, maleabilidade, sustentação, projeção, volumização; coesividade* e maleabilidade* com asterisco quando declaradas)
7. **OBJETIVOS CLÍNICOS** (tags)
8. **APLICAÇÕES POR REGIÃO** com grau de indicação e justificativa
9. **PLANO DE APLICAÇÃO** ("G′ NÃO DEFINE PLANO" — IFU e anatomia prevalecem)
10. **EVITE / NÃO PRIORIZE QUANDO** (⚠)
11. **ESCOLHA QUANDO…** e **ESCOLHA OUTRO PRODUTO QUANDO…** (frases de decisão)
12. **CLASSE REOLOGY MAP** (cor/fenótipo) + **ASSINATURA REOLOGY MAP** (fórmula em caixa alta, ex.: "PRECISÃO + PROJEÇÃO + BAIXA EXPANSÃO")
13. **RESUMO CURTO PARA O CARD** + **DADOS TÉCNICOS** (tabela) + **CONCEITO-CHAVE** (lição didática do produto)
14. **COMPARAÇÕES** — escada da própria linha + pares multimarcas (mesmo G′/assinatura diferente etc.)
15. Rodapé de rastreabilidade: lote ensaiado, protocolo, o que não foi medido (💧), fontes comerciais

As **"lógicas de linha"** já definidas viram navegação didática: e.p.t.q (S100 MOVIMENTO → S300 INTEGRAÇÃO+SUPORTE → S500 ESTRUTURA) · Neuramis (ESPALHAR → INTEGRAR → ESTRUTURAR) · Yvoire (SUSTENTAR → ESTRUTURAR → CORRIGIR COM PRECISÃO) · Perfectha (refinar → integrar → sustentar → precisão/baixo SF) · Saypha (INTEGRAÇÃO → SUSTENTAÇÃO → ESTRUTURA) · Rennova (LINHA → DEPRESSÃO → SULCO → CONVEXIDADE → SUSTENTAR → GEOMETRIA/VÉRTICE) · Milimetric (ADAPTAR → PREENCHER → SUSTENTAR) · Sofiderm (REFINAR → PREENCHER → PREENCHER+SUSTENTAR; corporal: ADAPTAR × ESTRUTURAR) · Stylage (🔵 INTEGRA → 🟡 PREENCHE → 🟣 SUSTENTA — "exemplo quase perfeito do sistema") · Hyafilia (🟡 REFINA → 🟣 MODELA → 🟣 PROJETA) · Juvéderm (ULTRA adapta → ULTRA PLUS sustenta; VOLUMA volumiza-sustenta → VOLUX projeta-define; SKINVIVE integra).

### 9.4 Modelo de dados

```
Marca(id, nome, fabricante, país)
Produto(id, marca_id, nome, numero_atlas, lidocaína,
        concentracao_mg_ml*, particula_um*, tecnologia*, crosslinker*,
        apresentacoes*, indicacao_bula*, duracao_comercial*)        * fonte=fabricante
Medida(produto_id, lote, freq_hz, g1_pa, g2_pa, tan_delta, eta_pas,
       fonte='biosmart', flag_verificar)                            # 456 linhas hoje
Classe(id, cor, nome, criterio, frase_verbo, leitura_clinica)
ProdutoClasse(produto_id, classe_id, versao_mapa)
Regiao(id, nome, classes_necessidade[], exigencia:{g1_faixa, tand_faixa,
       eta_repouso, coesividade†, swelling†, integracao†})          † qualitativo, fonte=autor
IndicacaoRegional(produto_id, regiao_id, nivel: 1a|forte|boa|seletiva|nao_priorizar|nao_indicar,
                  plano[], justificativa, fonte='autor')
FraseDecisao(produto_id, escolha_quando, escolha_outro_quando)
Similaridade(produto_a, produto_b, tipo: semelhante|mais_estrutura|mais_integracao|concorrente_direto)
```

Os arquivos `data/reologia_produtos_full.json` e `data/reologia_produtos_07hz.csv` deste repositório são a semente da tabela `Medida`.

### 9.5 Motor de seleção (algoritmo explicável, v1)

```
ENTRADA: região R, objetivo O, plano P, tecido T
1. VETOR-ALVO = exigência(R) ⊕ ajuste(O) ⊕ ajuste(P)
   ex.: lábio+naturalidade → G′ 80–190 Pa · tan δ ≥ 0,25 · família 🔵🌸
        mandíbula+definição+supraperiostal → G′ ≥ 400 Pa · tan δ ≤ 0,15 · 🟣
2. FILTRO DURO: remove nivel=nao_indicar/nao_priorizar para R
   e famílias incompatíveis com o alvo; respeita IFU sempre.
3. SCORE (0–100):
   45% proximidade reológica (distância normalizada da assinatura 0,7 Hz ao alvo;
       η* 0,01 Hz entra quando O = sustentação/projeção)
   35% camada clínica do autor (1ª escolha=100 · forte=80 · boa=60 · seletiva=35)
   20% modificadores de tecido (pele fina → penaliza G′ alto em plano superficial;
       região móvel → bonifica tan δ maior; sensível a edema → exige SF† favorável
       declarado e sinaliza 💧 quando não medido)
4. SAÍDA: top N com "POR QUÊ" (assinatura vs alvo + frase "escolha quando…" +
   fonte de cada dado) + atalhos "quero MAIS estrutura" / "quero MAIS integração"
   (arestas do grafo Similaridade — geradas pela pergunta 21 do questionário-mestre).
```

Princípios: **nenhuma recomendação sem justificativa visível**; empates mostrados como empates; linhas com `flag_verificar` exibem selo "dado em re-verificação"; coesividade/SF nunca aparecem como medidos; regiões de alto risco vascular (nariz, glabela) sempre exibem o alerta "reologia não é segurança vascular", independentemente do ranking.

### 9.6 Roadmap de produto

| Versão | Escopo |
|---|---|
| **MVP (v0.9)** | banco auditado (76 produtos, 6 freq) · Mapa interativo · fichas completas · busca · "Sobre o estudo" com metodologia e limitações. Sem login; conteúdo estático versionado. **Recomendação: PWA/web-app** (distribuição por link/QR em cursos, sem lojas). |
| **v1.0** | Decisão guiada (wizard + motor §9.5) · páginas-região · comparador 2–3 produtos · frases de decisão completas |
| **v1.1** | grafo de similares navegável · "meu armário" · modo aula (biblioteca do livro) |
| **v2.0** | 2ª rodada laboratorial (coesividade, swelling, extrusão, amplitude/Strain X) · novas marcas (MaiLi, Teosyal, Profhilo, Fillmed, SoftFil…) · casos clínicos com ultrassom · contas/assinatura · EN |

### 9.7 Decisões de produto em aberto (para o autor)
1. **Plataforma:** PWA primeiro (recomendado) vs nativo.
2. **Monetização:** assinatura individual · licença para pós-graduações · gratuito como funil de livro/cursos (benchmark PensaHOF é assinatura).
3. **Marca:** "Reology Map" — avaliar registro (INPI) e domínio.
4. **Idiomas:** PT-BR no MVP; EN na v2.

---

## 10. O livro — "REOLOGIA DO ÁCIDO HIALURÔNICO: Ciência dos Géis Aplicada ao Preenchimento Facial"

### 10.1 Estrutura completa e status

**PARTE I — Fundamentos dos Biomateriais**

| Cap. | Tema | Status |
|---|---|---|
| 1 | História: Zyderm/Zyplast (anos 1980, FDA) → colágeno humano → AH (Meyer & Palmer, 1934) → NASHA (Q-Med, 1996; FDA 2003) | ✅ escrito (faltam "bioestimuladores" e "próximas gerações") |
| 2 | Química do AH: GAG não sulfatado; ~15 g no corpo (metade na pele); GlcA+GlcNAc; β(1→3)/β(1→4); >6 MDa; fermentação de *S. equi* subsp. *zooepidemicus*; purificação; esterilização | ✅ escrito |
| 3 | Da molécula ao gel: -OH/-COOH/-NHCOCH₃; entanglement (analogia do espaguete); meia-vida do AH nativo 24–48 h; crosslink; 11 etapas industriais; arquitetura mono/bifásica | 🟡 semi-escrito (3.6 reticulantes e 3.7 hidrogel em esboço) |

**PARTE II — Físico-química dos Géis** ("o coração do livro")

| Cap. | Tema | Status |
|---|---|---|
| 4 | Viscoelasticidade (Maxwell, Kelvin-Voigt, Burgers) | 🟡 material bruto |
| 5 | G′ (~30 págs; escala 40/100/200/300/500/700 Pa; frequência; unidade; strain/LVR) | 🟡 material bruto forte |
| 6 | G″ ("quase ninguém explica direito") | 🟡 seção avulsa escrita |
| 7 | tan δ ("talvez o capítulo mais bonito" — gel parado → sorrindo → mastigando → falando) | ❌ |
| 8 | Módulo complexo G* | ❌ |
| 9 | Viscosidade zero shear / high shear | ❌ |
| 10 | Coesividade ("talvez o capítulo mais importante" — argila × areia úmida) | 🟡 trechos |
| 11 | Extrudabilidade | ❌ |
| 12 | Swelling Factor (com fotos; olheira) | 🟡 trechos + seção de durabilidade |
| 13 | Integração tecidual ("praticamente ninguém ensina") | ❌ |

**PARTE III — Engenharia dos Preenchedores:** 14 Tecnologias (CPM, NASHA, OBT, Vycross, Hylacross, XpresHAn, SMART, SHAPE, Preserved Network — "cada uma em um desenho") · 15 Monofásico × bifásico · 16 Concentração (20–30 mg/mL) · 17 Peso molecular · 18 Crosslink (BDDE, DVS, PEG). Status: ❌/🟡 fragmentos.

**PARTE IV — Reologia Clínica** ("agora entra sua contribuição"): 19 Como escolher o produto · 20 Por plano (superficial → SMAS → profundo → supraperiostal) · 21 Por região (olheira, nariz, lábios, malar, mandíbula, têmpora, testa, queixo, pré-jowl, pescoço, mãos) · 22 Por técnica (bolus, retro, leque, cross-hatching, microbolus, wash, skinbooster) · 23 Full Face ("praticamente sua técnica"). Status: ❌ — **mas o conteúdo do app (§8, fichas 1–71) É a matéria-prima destes capítulos.**

**PARTE V — Atlas dos Preenchedores** ("um diferencial absurdo — cada laboratório, mesmo padrão"): as monografias PT 1/PT 2 são o Atlas em produção (≈71/76 produzidas em alguma versão). Marcas previstas além do banco atual: MaiLi, Teosyal, Profhilo, SoftFil, Fillmed — candidatas à 2ª rodada de ensaios.

**PARTE VI — Casos Clínicos:** fluxo padronizado paciente → análise → escolha → por quê → plano → resultado → follow-up → **ultrassom**. ❌ a produzir.

**PARTE VII — Futuro:** IA, biomateriais inteligentes, hidrogéis responsivos, nanotecnologia, impressão 3D, géis personalizados. ❌ bullets.

### 10.2 O Mapa Reológico Facial (conceito-assinatura do livro)

> "Em vez de ensinar apenas regiões anatômicas, você ensina a 'ler' a face pela necessidade reológica."

| Região | G′ | Coesividade | tan δ | Swelling | Integração |
|---|---|---|---|---|---|
| Olheira | ↓ | ↓ | ↑ | ↓↓↓ | ↑↑↑ |
| Lábio | ↓ | média | ↑↑ | ↓ | ↑↑ |
| Nariz | ↑↑↑ | ↑↑↑ | ↓ | ↓ | média |
| Zigoma | ↑↑ | ↑↑ | ↓ | ↓ | média |
| Mandíbula | ↑↑↑ | ↑↑ | ↓ | ↓ | baixa |
| Têmpora | média | alta | média | ↓ | alta |
| Mento | ↑↑↑ | ↑↑ | ↓ | ↓ | média |

A completar: testa, pré-jowl, pescoço, mãos (listadas no Cap. 21). Esta tabela é também a espinha dorsal do motor de recomendação do app (§9.5).

### 10.3 Validação cruzada literatura × estudo próprio (material já produzido)
O livro já contém a comparação sistemática BioSmart × literatura internacional:
- **Tese confirmada:** *"os valores absolutos mudam, mas a tendência reológica geral é parecida"* — a **hierarquia** entre géis se preserva entre protocolos (S100 < S300 < S500; Lyft/Restylane no topo; Yvoire Contour > Volume > Classic), o que legitima comparar produtos **dentro do mesmo protocolo**.
- **Concordância pontual notável:** e.p.t.q S300 a 0,1 Hz — literatura 172,87 Pa × estudo 174,18 Pa.
- **Divergências a investigar no texto:** Cutegel Max/CL-Max (701 × 282 Pa — possivelmente formulações distintas sob nomes parecidos) e e.p.t.q S100 (tan δ 0,50 × 0,22).

### 10.4 Recursos didáticos definidos
Analogias oficiais: mola (G′), líquido espesso (G″), espaguete cozido (entanglement), argila × areia úmida (coesividade), fotografia × filme (ponto único × sweep). Sequências ilustradas: tan δ em movimento; coesividade em 5 estágios; swelling em olheira; fluxograma industrial em 11 etapas; modelos mecânicos. **Escala interpretativa do G′ ancorada em produtos reais do banco:** 40 ≈ Balance/Up Fine · 100 ≈ Skinvive/Ultra XC · 200 ≈ Evofill Ultra Deep · 300 ≈ Stylage XL · 500 ≈ Hyafilia Mold · 700+ ≈ Lyft/Volux/Shaype.

---

## 11. Fluxo de produção editorial (já definido e operante)

### 11.1 Três roteiros calibrados

| Roteiro | Uso | Gera |
|---|---|---|
| **6 perguntas** (áudio curto) | gravação rápida por produto | definição/diferencial · reologia na prática · 3 melhores indicações · paciente/tecido/plano · quando NÃO usar · concorrentes |
| **8 perguntas essenciais** | padrão universal; cada resposta → um campo do app | Descrição, Diferencial, "Melhor para", Aplicações por região, Plano, "Evite quando", Semelhantes, "Escolha quando…" |
| **Questionário-mestre (25 perguntas)** | monografia completa (livro/Atlas) | + interpretação de cada parâmetro, SF, coesividade, Strain X, limitação, armadilhas dos números (P18), experiência pessoal, rede de similares (P21), custo-benefício, classificação no Mapa |

### 11.2 Pipeline por produto

```
Áudio WhatsApp (autor responde ao roteiro)
  → transcrição
  → monografia no template padrão (PT 1/PT 2)
  → conferência dos números contra o laudo (Anexo 2, 0,7 Hz)
  → separação de fontes (BioSmart × fabricante × opinião do autor)
  → extração dos campos estruturados do app (ficha + frases + rankings por região)
  → revisão final e entrada no banco de conteúdo
```

### 11.3 Forças e riscos
- **Força:** perguntas idênticas ⇒ fichas comparáveis; a P21 ("qual produto no lugar dele se quiser MAIS estrutura / MAIS integração?") gera organicamente o **grafo de navegação** do app; a P18 ("quando os números enganam?") cria a camada anti-dogmática que diferencia o projeto de uma tabela fria.
- **Risco 1:** opinião clínica misturada a dado laboratorial sem marcação → resolver com rótulos de fonte na UI e no livro (§6.4).
- **Risco 2:** 76 produtos × 25 respostas presos em texto corrido → extrair cada resposta para campos estruturados (JSON/planilha/CMS) desde já.
- **Risco 3:** áudios sem transcrição confiável já causaram lacunas (citados: Juvéderm Ultra XC, Cutegel) → padronizar transcrição com revisão.

---

## 12. Ética, conformidade e posicionamento regulatório

1. **Natureza da ferramenta:** apoio educacional à decisão do profissional habilitado — não prescreve, não substitui julgamento clínico, não se destina a leigos. Disclaimer permanente no app e no livro.
2. **Segurança anatômica acima da reologia:** regiões de risco vascular (nariz, glabela, fronte, fossa piriforme) sempre com alerta, independentemente do ranking — "REOLOGIA NÃO TORNA UMA REGIÃO ANATOMICAMENTE ARRISCADA MAIS SEGURA".
3. **IFU prevalece:** onde a bula contraindica (ex.: Stylage L em lábios/periorbital; Volux em lábios/glabela), o app marca "NÃO INDICAR", mesmo que a reologia "combinasse". Indicações off-label refletem opinião do autor e são sinalizadas.
4. **Dados de pacientes:** o MVP não coleta dado de paciente. Versões futuras com casos clínicos/fotos: LGPD, consentimento, anonimização.
5. **Marcas de terceiros:** nomes de produtos são marcas registradas dos fabricantes; uso nominativo/comparativo com dado laboratorial próprio e fontes atribuídas; tom descritivo, nunca depreciativo; nota permanente "os fabricantes não participaram nem endossam o estudo".
6. **Variabilidade e limites:** resultados referem-se a **lotes específicos, a 25 °C, in vitro**; comportamento in vivo difere; lote a lote pode variar ~30% (§6.2). Esta honestidade é ativo, não passivo.
7. **Conflito de interesse:** declarar financiamento do estudo (clínica do autor) e ausência de patrocínio de fabricantes.

---

## 13. Roadmap consolidado — próximos passos priorizados

### Fase 0 — Fechar o banco canônico (1–2 semanas de trabalho focado)
1. Enviar à BioSmart a lista de re-verificação (§6.1 e §6.3: Volift/Voluma, Belotero Volume+/Neauvia Intense, Stimulate/Singderm, η* trocados, tan δ do Perfectha Subskin, UP a 0,7 Hz, Yvoire Volume+ sem lote) e obter errata/dados brutos.
2. Consolidar **uma única fonte de verdade** (JSON/planilha versionada — semente já em `data/` neste repositório) e corrigir as fichas divergentes (§6.5).
3. Reprocessar os rankings da planilha para 0,7 Hz; padronizar o par de exibição 0,7 + 0,01 Hz.
4. Completar fichas com números pendentes (todos já existem no laudo): Biogelis Fine Lines (G″ 35,31 · tan δ 0,20), e.p.t.q S500 (355,13/67,30/0,19), Neuramis Lido (89,70/34,31/0,38), Neuramis Deep (164,47/43,84/0,27), Neuramis Volume (314,05/48,17/0,15), Perfectha Deep (386,46/46,88/0,12), Perfectha Derm (440,68/50,10/0,11), Perfectha Subskin (343,00/52,00/0,15*), Yvoire Contour+ (579,90/60,64/0,10).

### Fase 1 — MVP do app (4–8 semanas)
5. PWA com Mapa interativo (scatter G′ × tan δ, cores das famílias), fichas 1–76, busca, "Sobre o estudo".
6. Renumerar/deduplicar monografias (não há nº 62; caps. 66–67 duplicados; completar rodapé truncado do 71 — Hyafilia Volume).
7. Produzir as ~5 fichas ainda sem monografia dedicada (Neauvia Intense, Neauvia Stimulate, Finahfil Intense, Restylane Skinbooster, Restylane lote 27003).

### Fase 2 — Decisão guiada (v1.0)
8. Fundir §8 + §10.2 na matriz canônica região × exigência; implementar o motor §9.5; validar com casos reais do autor.

### Fase 3 — 2ª rodada laboratorial (destrava a metade "não medida" do sistema)
9. Coesividade quantitativa, Swelling Factor, força de extrusão e amplitude sweep (Strain X) — prioridades citadas nas monografias: Yvoire Contour+, Perfectha Subskin, Rennova Eyes Lines, Milimetric Leve/Moderado, linha Sofiderm completa, Stylage, Hyafilia, UP Max/Contour, Evofill. Isso transforma os marcadores 💧 em dados e habilita a classe 3 (olheiras) com evidência própria.
10. Incluir marcas faltantes do Atlas: MaiLi, Teosyal, Profhilo, SoftFil, Fillmed.

### Fase 4 — Livro
11. Escrever Parte II reaproveitando §4 + material bruto já existente; Parte IV nasce das páginas-região do app; Parte V (Atlas) é a coleção de monografias revisadas; Parte VI com casos + ultrassom.
12. Converter o material em "voz de consultoria" (dirigido a "João") para prosa de livro; montar bibliografia formal (hoje links soltos PMC/ScienceDirect/Dove).

---

## Anexo A — Tabela mestre: 76 produtos a 0,7 Hz (ordenada por G′)

| # | Produto | Lote | G′ (Pa) | G″ (Pa) | tan δ | η* (Pa·s) | Classificação (planilha) |
|--:|---|---|--:|--:|--:|--:|---|
| 1 | Belotero Balance Lido | B0053230 | 33,64 | 23,23 | 0,69 | 8,84 | Predomínio viscoso (fluido) |
| 2 | Up Fine Lido | S2N724010 | 33,66 | 12,28 | 0,36 | 10,54 | Moderadamente elástico |
| 3 | Milimetric PRO Leve Lido | MLFN2410A | 56,26 | 32,04 | 0,57 | 14,01 | Predomínio viscoso (fluido) |
| 4 | e.p.t.q S 100 Lido | YLA25002 | 70,35 | 39,28 | 0,56 | 17,43 | Predomínio viscoso (fluido) |
| 5 | Milimetric PRO Moderado Lido | MLM1N2503A | 72,44 | 34,84 | 0,48 | 17,39 | Moderadamente elástico |
| 6 | Rennova Fill Fine Lines Lido | 406018 | 81,53 | 43,56 | 0,53 | 20,00 | Predomínio viscoso (fluido) |
| 7 | Restylane Refyne Lido | 23768 | 81,57 | 23,87 | 0,29 | 18,39 | Moderadamente elástico |
| 8 | Rennova Fill Eyes Lines Lido | YLA25503 | 87,38 | 45,38 | 0,52 | 21,30 | Predomínio viscoso (fluido) |
| 9 | Neuramis Lido | C024007A | 89,70 | 34,31 | 0,38 | 20,78 | Moderadamente elástico |
| 10 | Juvéderm Skinvive | (recuperar lote) | 102,26 | 54,75 | 0,54 | 25,10 | Predomínio viscoso (fluido) |
| 11 | Juvéderm Ultra XC Lido | 1003801607 | 110,75 | 37,44 | 0,34 | 25,29 | Moderadamente elástico |
| 12 | Rennova Fill | YLA25503 | 118,08 | 40,86 | 0,35 | 27,03 | Moderadamente elástico |
| 13 | Sofiderm Derm Plus | 250917-2 | 122,17 | 30,11 | 0,25 | 27,22 | Muito elástico (sustentação) |
| 14 | Revanesse Ultra + Lido | 250714 | 127,76 | 39,36 | 0,31 | 28,92 | Moderadamente elástico |
| 15 | Revanesse Kiss Lido | 250407 | 131,06 | 50,83 | 0,39 | 30,41 | Moderadamente elástico |
| 16 | Restylane Volyme Lido | S2231860020 | 137,69 | 22,68 | 0,16 | 30,19 | Muito elástico (sustentação) |
| 17 | Revanesse Contour + Lido | 25C053 | 142,29 | 39,24 | 0,28 | 31,93 | Muito elástico (sustentação) |
| 18 | Saypha Filler Lido | 905018 | 142,61 | 33,52 | 0,24 | 31,69 | Muito elástico (sustentação) |
| 19 | Sofiderm Derm | 251105-2 | 146,72 | 31,23 | 0,21 | 32,45 | Muito elástico (sustentação) |
| 20 | Revanesse Outline+ Lido | 24K091 | 148,24 | 32,83 | 0,22 | 32,85 | Muito elástico (sustentação) |
| 21 | Sofiderm Fine Lines | 240510-3 | 151,88 | 37,27 | 0,25 | 33,83 | Muito elástico (sustentação) |
| 22 | Juvéderm Ultra Plus XC Lido | 1003698142 | 161,39 | 38,10 | 0,24 | 35,88 | Muito elástico (sustentação) |
| 23 | Evofill Derm | EVMD1CLX2603A | 162,47 | 57,14 | 0,35 | 37,26 | Moderadamente elástico |
| 24 | Neuramis Deep Lido | B625027A | 164,47 | 43,84 | 0,27 | 36,82 | Muito elástico (sustentação) |
| 25 | Stylage Lips Lido | 233351202 | 167,01 | 34,95 | 0,21 | 36,92 | Muito elástico (sustentação) |
| 26 | Milimetric PRO Intenso Lido | MLV1N2602H | 170,32 | 46,24 | 0,27 | 38,18 | Muito elástico (sustentação) |
| 27 | Revanesse Shape + Lido | 250618 | 172,61 | 30,79 | 0,18 | 37,93 | Muito elástico (sustentação) |
| 28 | Up Deep Lido | S2N725007 | 172,67 | 31,94 | 0,18 | 51,64⚑ | Muito elástico (sustentação) |
| 29 | Biogelis Fine lines | 2509FL065C1E | 176,94 | 35,31 | 0,20 | 39,03 | Muito elástico (sustentação) |
| 30 | Biogelis Global Lido | 2602GL009A2E | 177,40 | 33,77 | 0,19 | 39,07 | Muito elástico (sustentação) |
| 31 | Restylane Kysse Lido | 22620-1 | 178,82 | 24,53 | 0,14 | 39,05 | Muito elástico (sustentação) |
| 32 | Rennova Deep Line Lido | V04407 | 183,33 | 31,85 | 0,17 | 40,26 | Muito elástico (sustentação) |
| 33 | Belotero Intense Lido | B00060100 | 186,11 | 60,69 | 0,33 | 42,35 | Moderadamente elástico |
| 34 | Evofill Ultra Deep | EVVO1CLX2604A | 199,67 | 57,16 | 0,29 | 44,93 | Muito elástico (sustentação) |
| 35 | Rennova Ultra Volume Lido | V05519 | 221,87 | 32,38 | 0,15 | 48,51 | Muito elástico (sustentação) |
| 36 | Sofiderm Deep | 251029-2 | 223,11 | 42,59 | 0,19 | 49,14 | Muito elástico (sustentação) |
| 37 | e.p.t.q S 300 Lido | YLB25514 | 226,00 | 53,09 | 0,23 | 50,23 | Muito elástico (sustentação) |
| 38 | Biogelis Volume Lido | 2504VL10322B | 251,51 | 48,87 | 0,19 | 55,43 | Muito elástico (sustentação) |
| 39 | Saypha Volume Lido | 106033 | 251,93 | 29,13 | 0,12 | 54,87 | Muito elástico (sustentação) |
| 40 | Juvéderm Volbella Lido | 1003875837 | 252,50 | 40,40 | 0,16 | 55,32 | Muito elástico (sustentação) |
| 41 | Belotero Volume + Lido | B0005990 | 252,61 | 57,31 | 0,23 | 56,04⚑ | Muito elástico (sustentação) |
| 42 | Neauvia Intense | HA2250906 | 252,61 | 57,31 | 0,23 | 56,04⚑ | Muito elástico (sustentação) |
| 43 | Rennova Lift | 705069 | 253,59 | 28,77 | 0,11 | 55,22 | Muito elástico (sustentação) |
| 44 | Stylage L Lido | 232651104 | 260,15 | 41,82 | 0,16 | 57,01 | Muito elástico (sustentação) |
| 45 | Cutegel Lidocaine CL-Max | BLM2401 | 282,48 | 56,87 | 0,20 | 62,34 | Muito elástico (sustentação) |
| 46 | Hyafilia S Plus Lido | LBP24001 | 283,77 | 59,07 | 0,21 | 62,71 | Muito elástico (sustentação) |
| 47 | Neauvia Stimulate | HA1250901 | 285,83 | 78,16 | 0,27 | 64,11⚑ | Muito elástico (sustentação) |
| 48 | Singderm Lido | H240729B11D | 285,83 | 78,16 | 0,27 | 64,11⚑ | Muito elástico (sustentação) |
| 49 | Restylane Defyne Lido | 22910 | 292,62 | 24,28 | 0,08 | 63,53 | Muito elástico (sustentação) |
| 50 | Stylage XL Lido | 232641104 | 305,08 | 46,59 | 0,15 | 66,77 | Muito elástico (sustentação) |
| 51 | Neuramis Volume | C424040A | 314,05 | 48,17 | 0,15 | 68,74 | Muito elástico (sustentação) |
| 52 | Yvoire Classic+ Lido | ICK24008 | 319,88 | 45,65 | 0,14 | 69,91 | Muito elástico (sustentação) |
| 53 | Up Contour Lido | S2N725009 | 328,48 | 47,92 | 0,15 | 71,82 | Muito elástico (sustentação) |
| 54 | Sofiderm Derm Sub-Skin | 241007-2 | 330,84 | 46,88 | 0,14 | 72,29 | Muito elástico (sustentação) |
| 55 | Finahfil Intense | A260120L2-1B | 338,51 | 37,90 | 0,11 | 73,69 | Muito elástico (sustentação) |
| 56 | Perfectha Subskin | 241118-1 | 343,00 | 52,00 | 0,20⚑ | 75,01 | Muito elástico (sustentação) |
| 57 | Up Max Lido | S2N725010 | 351,32 | 72,19 | 0,21 | 105,48⚑ | Muito elástico (sustentação) |
| 58 | e.p.t.q S 500 Lido | YLC25511 | 355,13 | 67,30 | 0,19 | 78,20 | Muito elástico (sustentação) |
| 59 | Yvoire Volume+ Lido | N/D⚑ | 358,50 | 55,99 | 0,16 | 78,50 | Muito elástico (sustentação) |
| 60 | Juvéderm Volift Lido | 1003113042 | 362,97 | 32,29 | 0,09 | 78,84⚑ | Muito elástico (sustentação) |
| 61 | Juvéderm Voluma Lido | 1003471713 | 362,97 | 32,29 | 0,09 | 78,84⚑ | Muito elástico (sustentação) |
| 62 | Biogelis Volumax Lido | 2502VX10092B | 385,93 | 71,79 | 0,19 | 84,93 | Muito elástico (sustentação) |
| 63 | Perfectha Deep | 250217-2 | 386,46 | 46,88 | 0,12 | 84,22 | Muito elástico (sustentação) |
| 64 | Rennova Lips Plus Lido | YLC25515 | 401,97 | 71,66 | 0,18 | 88,34 | Muito elástico (sustentação) |
| 65 | Perfectha Derm | 250217-1 | 440,68 | 50,10 | 0,11 | 95,96 | Muito elástico (sustentação) |
| 66 | Rennova Lift Plus Lido | 206031 | 475,85 | 34,33 | 0,07 | 103,22 | Muito elástico (sustentação) |
| 67 | Saypha Volume Plus Lido | 206020 | 488,91 | 35,54 | 0,07 | 106,06 | Muito elástico (sustentação) |
| 68 | Hyafilia M Plus Lido | A11092601 | 526,31 | 83,47 | 0,16 | 115,29 | Muito elástico (sustentação) |
| 69 | Restylane Skinbooster Lido | 23887 | 562,82 | 148,26 | 0,26 | 125,92 | Muito elástico (sustentação) |
| 70 | Yvoire Contour+ Lido | IVK25002 | 579,90 | 60,64 | 0,10 | 126,15 | Muito elástico (sustentação) |
| 71 | Restylane Lido (lote 22647) | 22647 | 617,71 | 162,40 | 0,26 | 138,18 | Muito elástico (sustentação) |
| 72 | Juvéderm Volux | 1003958774 | 669,12 | 49,46 | 0,07 | 145,16 | Muito elástico (sustentação) |
| 73 | Restylane Lyft Lido | 21046-1 | 718,22 | 128,63 | 0,18 | 157,86 | Muito elástico (sustentação) |
| 74 | Restylane Lido (lote 27003) | 27003 | 800,09 | 206,05 | 0,26 | 178,75 | Muito elástico (sustentação) |
| 75 | Hyafilia V Plus Lido | A11102505 | 840,54 | 122,77 | 0,15 | 183,78 | Muito elástico (sustentação) |
| 76 | Restylane Shaype Lido | 23047 | 935,94 | 141,80 | 0,15 | 204,80 | Muito elástico (sustentação) |

⚑ = linha com flag `verificar_dado` (auditoria §6.1/§6.3).

## Anexo B — Comportamento por frequência (6 produtos-exemplo, G′ Pa / tan δ)

| Produto | 10 Hz | 5 Hz | 1 Hz | 0,7 Hz | 0,1 Hz | 0,01 Hz |
|---|---|---|---|---|---|---|
| Belotero Balance | 78/0,90 | 67/0,80 | 38/0,70 | 34/0,69 | 17/0,60 | 9/0,50 |
| Juvéderm Skinvive | 178/0,28 | 162/0,31 | 110/0,51 | 102/0,54 | 48/0,88 | 17/**1,54** |
| Restylane Refyne | 129/0,50 | 115/0,43 | 86/0,31 | 82/0,29 | 63/0,22 | 52/0,19 |
| Juvéderm Voluma | 383/0,13 | 391/0,10 | 367/0,09 | 363/0,09 | 324/0,13 | 270/0,17 |
| Juvéderm Volux | 748/0,08 | 717/0,08 | 676/0,07 | 669/0,07 | 611/0,11 | 522/0,16 |
| Restylane Shaype | 1146/0,12 | 1099/0,13 | 961/0,15 | 936/0,15 | 788/0,17 | 709/0,17 |

## Anexo C — Glossário essencial

| Termo | Definição operacional do projeto |
|---|---|
| Reologia | Ciência da deformação e do fluxo da matéria sob força. |
| Ensaio oscilatório | Deformação senoidal pequena; mede resposta em fase (elástica) e fora de fase (viscosa). |
| G′ (módulo de armazenamento) | Componente elástica — energia devolvida; "a mola". Pa (1 Pa = 1 N/m²). |
| G″ (módulo de perda) | Componente viscosa — energia dissipada; "o amortecedor". |
| tan δ | G″/G′. <1 = caráter de gel; >1 = caráter de líquido. |
| G* | Módulo complexo — rigidez total. |
| η* (viscosidade complexa) | Resistência global ao fluxo oscilatório; explode em baixa frequência nos géis estruturados. |
| Varredura de frequência | Módulos em várias velocidades — o "filme" do gel (10 Hz = movimento rápido; 0,01 Hz = repouso). |
| Varredura de amplitude / Strain X | Até quanta deformação a rede aguenta (LVR) — **não realizada nesta rodada**. |
| Coesividade | Resistência à desagregação — ensaio próprio; **não medida aqui** ("argila × areia úmida"). |
| Swelling Factor (SF) | Expansão por absorção de água; crítico em olheira; **não medido aqui** (💧). |
| Extrudabilidade | Força para injetar no conjunto seringa-agulha real; **não medida aqui**. |
| Crosslink / BDDE | Reticulação covalente entre cadeias; BDDE = 1,4-butanodiol diglicidil éter. |
| Monofásico / bifásico | Matriz homogênea contínua × partículas suspensas em fase carreadora (ex.: NASHA). |
| NASHA | Non-Animal Stabilized Hyaluronic Acid (Q-Med, 1996) — fermentação + BDDE. |
| Fenótipo reológico | Família visual de comportamento (🔵🌸/🟡/🟣/🟣🟢) — unidade básica do Reology Map. |
| Assinatura reológica | O trio G′/G″/tan δ a 0,7 Hz (ex.: Voluma = 363/32/0,09) + fórmula-síntese em caixa alta. |

## Anexo D — Rastreabilidade das fontes deste documento

| Fonte | O que forneceu |
|---|---|
| `BS_Clinica_Pithon_Napoli_04082026_assinado 4.pdf` | metodologia, lotes, Anexos 1–2 (dados completos) |
| `Reologia_Preenchedores_Pithon_Napoli.xlsx` | dados tabulados nas 6 frequências, classificação 3 níveis, rankings |
| Google Doc "APP: REOLOGY MAP" (~927 mil caracteres) | fichas 1–71, sistemas de classificação, regras editoriais, mapeamento por região |
| Google Doc "REOLOGY MAP PT 1" | 1ª iteração do mapa (5 grupos) e monografias iniciais |
| Google Doc "REOLOGY MAP PT 2 – 62 EM DIANTE" | monografias 63–71 (template maduro, evidência clínica, comparações) |
| Google Doc "LIVRO DE REOLOGIA" | estrutura do livro, capítulos 1–3, Mapa Reológico Facial, validação vs literatura |
| Google Doc "PRODUÇÃO NO CHAT" | roteiros de 6/8/25 perguntas |
| Pastas AUDIOS/ (notas .opus por produto) | matéria-prima do pipeline editorial (não transcritas nesta análise) |
| pensahof.com.br | benchmark declarado (conteúdo interno não acessado — site atrás de login) |

---

*Documento gerado a partir da análise integral do acervo do projeto. Todos os valores reológicos citados provêm do laudo BioSmart (Anexo 2, 0,7 Hz, salvo indicação); dados de fabricantes estão sempre atribuídos; linhas com ⚑ aguardam re-verificação laboratorial (§6).*
