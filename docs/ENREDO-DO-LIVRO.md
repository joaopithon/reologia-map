# O enredo do livro

**Livro:** *Reologia do Ácido Hialurônico — Guia dos preenchedores do mercado brasileiro*
**Autor:** Dr. João Pithon · **Gerador:** `ebook/build_ebook.py` + `ebook/ebook_data.py`

Este documento é o **contrato narrativo** do livro: a promessa, o eixo, as subclasses, a cadeia
capítulo a capítulo, as dívidas em aberto e a definição operacional de "informação completa".
É a única referência contra a qual a revisão editorial é feita — quando o texto do livro e este
documento discordam, um dos dois está errado e a revisão precisa dizer qual.

---

## 1. A promessa, em uma frase

> Ensinar o injetor a **escolher o gel pela tarefa**, usando quatro números medidos sob um
> protocolo único, num mercado onde cada fabricante mede como quer.

Três consequências que o livro inteiro precisa honrar:

1. **A tarefa vem antes da região.** Um sulco nasolabial raso e um profundo pedem famílias
   diferentes apesar do mesmo nome anatômico.
2. **O produto é a 5ª decisão, não a 1ª:** ANATOMIA → DEFEITO → OBJETIVO → PLANO → PRODUTO →
   (DISTRIBUIÇÃO) → VOLUME → TÉCNICA.
3. **O número tem dono.** Todo valor reológico do livro vem do ensaio BioSmart a 0,7 Hz;
   todo dado declarado por fabricante leva asterisco; o que não foi medido leva marcador.

---

## 2. Escopo declarado × escopo medido

O livro se propõe a descrever **todos os tipos de preenchedor disponíveis hoje no Brasil**,
tendo o ácido hialurônico como eixo. Hoje ele entrega, com número primário, apenas o AH
reticulado ensaiado. Essa distância é legítima — **desde que declarada no texto**. O que não é
aceitável é o título prometer o mercado e o corpo entregar só uma classe, em silêncio.

| Classe de preenchedor | Presença no mercado brasileiro | Status no livro | Como o texto deve tratar hoje |
|---|---|---|---|
| **AH reticulado** (BDDE, DVS, PEG) | dominante | ✅ 76 ensaios, números primários | corpo do livro |
| **AH não reticulado / skinboosters** | crescente | 🟡 parcial — Skinvive e Restylane Skinbooster estão no banco; Profhilo não | declarar que a classe existe e que só os ensaiados aparecem com número |
| **AH de marcas não ensaiadas** (MaiLi, Teosyal, Fillmed, SoftFil…) | presente | ❌ fora do banco | nomear como candidatas à 2ª rodada, sem número |
| **CaHA** (hidroxiapatita de cálcio) | presente | ❌ | capítulo/seção declarando a classe, seu mecanismo e por que não tem número aqui |
| **PLLA** (ácido polilático) | presente | ❌ | idem |
| **PCL** (policaprolactona) | presente | ❌ | idem |
| **PMMA** | presente, com restrição regulatória e de indicação | ❌ | idem, com a nota regulatória |
| **Colágeno e autólogos** | histórico / nicho | 🟡 aparece na história (cap. 1) | manter como história, não como opção comparável |

**Regra de fronteira:** enquanto uma classe não tiver ensaio próprio, ela entra no livro como
**classe descrita sem número** — nunca comparada em Pa com o AH ensaiado, e nunca omitida.

---

## 3. O eixo: três famílias de G′

Três cores organizam o livro inteiro. A **1ª cor é o G′** e define a família.

| # | Família | Cor | Faixa de G′ a 0,7 Hz | Verbo | N | Grupos |
|---|---|---|---|---|--:|---|
| 1 | **BAIXO G′** | 🔵 azul | < 200 Pa | integra, espalha, acompanha | 34 | 1 e 2 |
| 2 | **MODERADO G′** | 🟡 amarelo | 200 – 299,99 Pa | preenche, equilibra | 14 | 3 |
| 3 | **ALTO G′** | 🟣 roxo | ≥ 300 Pa | sustenta — projeta ou volumiza | 28 | 4, 5 e 6 |

Total: **76 ensaios** (75 produtos; Restylane Lido aparece em dois lotes).

Três regras de leitura que o texto não pode contradizer:

- **A COR CLASSIFICA. O NÚMERO POSICIONA.** Mesma cor não significa mesma intensidade —
  Stylage XL (305 Pa) e Restylane Shaype (936 Pa) são ambos roxos.
- **O espectro é contínuo. A cor simplifica.** Os cortes 200 e 300 Pa são operacionais deste
  banco a 0,7 Hz, não constantes universais.
- **Nome comercial ≠ reologia.** "Soft" não é azul (Hyafilia Soft: 283,77 Pa); "Contour" e
  "Plus" não significam mais G′.

---

## 4. As subclasses — refinam, não criam sistema paralelo

**Nove assinaturas = 3 famílias × 3 comportamentos.** A assinatura é 1ª cor + 2ª cor.
Assinaturas e grupos são **detalhamento das três famílias**; todo capítulo de grupo declara
a que família pertence.

### 4.1 Baixo G′ 🔵 — duas assinaturas, **uma indicação**

| Assinatura | Grupo | Nome | N | O que muda |
|---|---|---|--:|---|
| azul + rosa | 1 · FLUIDOS DINÂMICOS | integrativo dinâmico | 28 | máxima integração, relevo quase nulo |
| azul + amarelo + rosa | 2 · FLUIDOS COM CORPO | integrativo volumizador | 6 | G″ intermediário: mesma integração, mais corpo |

> **As regiões são as mesmas.** A diferença é *quanto* cada assinatura valoriza, não *onde* se
> aplica: onde vai uma, vai a outra. Dar listas de regiões distintas para os grupos 1 e 2 é erro
> conceitual — foi o erro corrigido na reestruturação em três famílias.

### 4.2 Moderado G′ 🟡 — uma assinatura, sem subclasse

Grupo 3 · EQUILIBRADOS · 14 produtos. O produto de transição: preenche o vale sem espalhar nem
projetar. *"O amarelo é a cor do vale."* Critério de "equilibrado": G′ ≥ 200 **e** tan δ ≥ 0,21.

### 4.3 Alto G′ 🟣 — **três usos, não um**

| Uso | Assinatura | Grupo | N | Tarefa |
|---|---|---|--:|---|
| **Projeção** | roxo puro | 4 · PROJETORES PUROS | 2 | vértice: mento, mandíbula, arco zigomático (nariz: só racional — risco vascular) |
| **Volumização** | roxo + 2ª cor | 5 · ESTRUTURAIS MOLDÁVEIS | 26 | sustenta com curva e corpo; volume estrutural, não projeção focal |
| **Olheira** | roxo + 💧 baixo SF | 6 · PRECISOS | transversal | estrutura numa região que não tolera inchaço |

O grupo 6 **não é uma sexta família**: é o terceiro uso da família roxa, critério funcional
transversal, e é **declarativo** — o Swelling Factor não foi medido em nenhum produto.
Regra do autor: *nunca escolher olheira pelo G′.*

Caso de borda com curadoria oficial: Restylane Defyne (292,62 Pa) permanece no grupo 5, com o
G′ marcado em roxo por decisão do mapa — e o texto declara essa decisão em vez de esconder.

---

## 5. A cadeia — o que cada capítulo entrega e o que promete

Um capítulo só está completo quando entrega o seu e **paga o que os anteriores prometeram**.

| Cap. | Entrega | Promete adiante | Onde paga |
|---|---|---|---|
| 1 | Como ler o guia: cores, assinatura, régua, ficha | "a região entra no cap. 5"; "a forma no cap. 6" | 5 e 6 |
| 2 | A molécula e a rede — de onde vem o G′ | que reticulação explica faixa de G′ | 3, e a anti-inferência em 4 |
| 3 | Por que o gel é viscoelástico | os quatro números | 4 |
| 4 | Os quatro números em 60 s: G′, G″, tan δ, η* | que frequência é movimento facial | 4.5 e 7 |
| 5 | **O Mapa: três famílias sobre a face** (capítulo-eixo) | os grupos como detalhamento; os três usos do roxo | 9–14 |
| 6 | A forma do gel — os quatro conceitos que a desenham | coesividade e SF como dado declarado | 12 e grupo 6 |
| 7 | Textura visual do gel | — | — |
| 8 | Atlas de gráficos — todas as variáveis | leitura par 0,7 Hz + 0,01 Hz | 15 |
| 9–13 | Grupos 1 a 5 + fichas de produto | cada ficha: composição, momento-para, indicações com nível, evitar, escolha, alternativas | fichas |
| 14 | Grupo 6 — alto G′ com baixo SF | 2ª rodada laboratorial | dívida aberta (§6) |
| 15 | Rankings completos — 76 ensaios lado a lado | — | — |
| 16 | Quando as fontes discordam: erratas, pares idênticos, lotes | re-verificação BioSmart | dívida aberta (§6) |
| 17 | Guia rápido por região | que reologia não substitui IFU | notas finais |

**Progressão-mãe do livro:** INTEGRA → INTEGRA + DÁ CORPO → PREENCHE → MODELA / SUSTENTA /
VOLUMIZA → PROJETA.

---

## 6. Dívidas do enredo — promessas em aberto

Nenhuma delas é defeito, desde que **marcada no ponto onde o leitor poderia se enganar**.

| Dívida | Marcação obrigatória no texto |
|---|---|
| **Swelling Factor não medido em nenhum produto** | 💧 em toda menção; grupo 6 identificado como declarativo; "sem SF confiável não existe ranking definitivo para olheiras" |
| **Três pares com assinatura idêntica** (Volift × Voluma; Belotero Volume+ × Neauvia Intense; Neauvia Stimulate × Singderm) | flag de re-verificação junto às fichas e no cap. 16 |
| **Restylane Lido em dois lotes** (617,71 × 800,09 Pa) | reportar ambos com lote explícito — é argumento, não fragilidade |
| **Três erratas de transcrição** (e.p.t.q S500 tan δ 0,19; Perfectha Subskin tan δ 0,15; Saypha Filler G″ 33,52) | valor corrigido no corpo + demonstração aritmética no cap. 16 |
| **Divergências fichas × listas** (Belotero Balance, Biogelis Global, Restylane Kysse, Yvoire Classic+, Yvoire Volume+) | fonte da verdade = laudo Anexo 2 a 0,7 Hz |
| **Coesividade, extrudabilidade, integração, duração** não medidas | camada qualitativa declarada, com asterisco; nunca deduzidas do G′ |
| **Classes de preenchedor fora do AH ensaiado** (§2) | classe descrita sem número, fronteira declarada |
| **Produtos citados sem ensaio** (Evofill Fine Lines, Rennova Fill Soft Lips, Cutegel CL-S/CL-N/CL-Max 1400) | citar sem atribuir número |

---

## 7. Regras de honestidade que o texto não pode violar

**Regra das três fontes:** (1) BioSmart = única fonte de número reológico; (2) fabricante =
dado declarado, sempre com asterisco; (3) não mensurado = proibido deduzir.

**Anti-inferências** (o código de honestidade do sistema):

- G′ ≠ coesividade · ≠ volumização · ≠ lifting · ≠ força de extrusão · não define plano ·
  **G′ não é segurança vascular**
- tan δ ≠ fluidez · G″ alto ≠ gel dinâmico (ler sempre em relação ao G′)
- baixo G′ ≠ baixo SF · alto G′ ≠ alto SF · **swelling do gel ≠ edema clínico**
- concentração ≠ reologia · partícula ≠ G′ · tecnologia/reticulante ≠ faixa de G′
  (NASHA ≠ alto G′; DVS ≠ alto G′)
- nome comercial ≠ reologia · indicação comercial ≠ adequação reológica
- evidência clínica ≠ causalidade reológica

**Três frases-fundamento:**

> "O objetivo não é mostrar o preenchedor. É fazer desaparecer a depressão."
> "Entre espalhar e projetar existe uma terceira função extremamente importante: sustentar."
> "O melhor produto utilizado na indicação errada continua sendo uma escolha errada."

**Limites declarados:** reologia não substitui IFU nem segurança anatômica ·
RESULTADO = PRODUTO × VOLUME × PLANO × TÉCNICA × TECIDO · "reologia ajuda a escolher a
ferramenta; não calcula os mililitros necessários" · 0,7 Hz é referência padronizada de
comparação, não um "G′ universal do produto".

---

## 8. O que conta como "informação completa"

Definição operacional. Um trecho do livro está **incompleto** — e a revisão precisa fechá-lo,
não apenas apontá-lo — quando:

1. **Promessa sem pagamento.** O texto anuncia ("veremos adiante", "no capítulo X") e o destino
   não existe, ou existe sem o conteúdo prometido.
2. **Referência órfã.** Aponta para figura, tabela, capítulo, produto, âncora ou QR que não existe.
3. **Termo sem primeira definição.** Jargão (LVR, strain, entanglement, bifásico, NASHA, CPM,
   supraperiostal…) usado antes de ser definido uma vez, no lugar onde aparece primeiro.
4. **Número sem procedência.** Valor reológico sem frequência, sem fonte, ou sem lote quando o
   lote importa; dado de fabricante sem asterisco; grandeza sem unidade.
5. **Classificação sem membros.** Família, grupo, assinatura ou faixa apresentada sem o N, sem
   os cortes ou sem a lista de quem pertence.
6. **Ficha truncada.** Produto sem um dos campos do padrão: composição/leitura, momento-para,
   indicações com nível (1–4), o que evitar, frase de escolha, alternativas.
7. **Região sem tarefa.** Região citada sem dizer qual tarefa geométrica ela pede
   (LINHA / VALE / CURVA / SUPORTE / VÉRTICE) e qual família responde.
8. **Assimetria entre pares.** Uma família, grupo, região ou produto tratado com profundidade
   que os equivalentes não recebem.
9. **Dívida não marcada.** Qualquer item do §6 aparecendo sem sua marcação obrigatória.
10. **Figura muda.** Ilustração, gráfico ou prancha sem legenda que diga o que ler nela, ou sem
    `alt` para leitor de tela.
11. **Afirmação sem dono.** Alegação clínica ou de mecanismo sem fonte, sem ser marcada como
    experiência do autor, e sem estar amparada por número do banco.
12. **Fronteira de escopo silenciosa.** Trecho que induz o leitor a achar que o livro cobre algo
    que ele não cobre (§2).
