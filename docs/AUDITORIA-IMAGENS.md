# Auditoria das 53 imagens novas — antes da integração ao livro

**Data:** 27/08/2026 · **Fonte de verdade:** `data/reologia_produtos_full.json` (76 ensaios, 75 produtos canônicos, 0,7 Hz)
**Ferramenta:** `ebook/auditor.py` + `ebook/audit_lote1.py` + `ebook/audit_lote4.py`
**Instrução do autor:** *"pode se inspirar nessas imagens para adicionar no decorrer do livro, apenas revisar os dados e corrigi-los antes de colocar as imagens."*

Nenhum número deste livro é transcrito de imagem. Todos são gerados do banco canônico. Esta auditoria existe para decidir **quais imagens podem entrar** e **o que precisa ser corrigido antes**.

---

## 1. Resultado por lote

| Lote | Imagens | Valores conferidos | Conferem | Veredito |
|---|---|---|---|---|
| 1 | 14 (13 únicas) | 79 | 76 (96%) | Tabela-mestra e rankings aproveitáveis; 3 erratas; Yvoire é outra fonte |
| 2 | 13 | 22 | 0 dos 22 numéricos | Conceituais **aprovadas**; produtos são literatura/fabricante |
| 3 | 13 | 49 | **49 (100%)** | Aprovado integralmente — estudo do próprio autor |
| 4 | 13 (12 legíveis) | 23 | **0 (0%)** | **Rejeitado**: valores e ordenações inconsistentes |

---

## 2. As três erratas (banco correto, transcrição errada)

Cada uma se demonstra pela própria tabela de origem:

| Produto | Campo | Impresso | **Correto** | Demonstração |
|---|---|---|---|---|
| e.p.t.q S 500 | tan δ | 0,23 | **0,19** | `67,30 / 355,13 = 0,1895`. O 0,23 é o tan δ do **S 300**, repetido uma linha abaixo |
| Perfectha Subskin | tan δ | 0,20 | **0,15** | `52,00 / 343,00 = 0,1516` |
| Saypha Filler | G″ | 39,36 Pa | **33,52 Pa** | 39,36 é o G″ do **Revanesse Ultra +** (linha vizinha). A tabela imprime tan δ 0,24, e só `33,52/142,61 = 0,235` fecha em 0,24 — `39,36/142,61 = 0,276` não |

Consolidadas em `ERR_TD` no gerador e documentadas no **capítulo 16** do livro.

---

## 3. Correção de escopo — os rankings

Os rankings anteriores tinham **valores corretos sobre universo incompleto** (42 produtos, não 76). Sobre o banco inteiro a composição muda:

- **Menor G′ do estudo** não é Up Fine (33,66) e sim **Belotero Balance (33,64)**.
- **Segundo maior G′** não é Restylane Lyft e sim **Hyafilia V Plus (840,54)**.
- Entram entre os 10 menores: Milimetric PRO Leve, Milimetric PRO Moderado, Rennova Fill Fine Lines, Restylane Refyne, Rennova Fill Eyes Lines, Juvéderm Skinvive.
- Entram entre os 10 maiores: Hyafilia V Plus, Restylane Lido (lote 27003), Juvéderm Volux, Restylane Skinbooster, Hyafilia M Plus.
- Filtro "G′ ≥ 200 **e** tan δ ≥ 0,21": **10 ensaios**, não 7 (entram Restylane Lido lote 27003, Restylane Skinbooster, Hyafilia S Plus).

Os quatro rankings temáticos foram **refeitos nativamente** a partir do banco (capítulo 15).

---

## 4. Divergências que NÃO são erro — outras fontes

Nove produtos têm valores publicados por outras fontes. As diferenças vêm de protocolo, não de imprecisão:

| Produto | Este estudo (0,7 Hz) | Outra fonte | Origem |
|---|---|---|---|
| Belotero Balance | G′ 33,64 · tan δ 0,69 | G′ 128 · 0,64 | Literatura publicada |
| Belotero Intense | G′ 186,11 · tan δ 0,33 | G′ 255 · 0,43 | Literatura publicada |
| Belotero Volume + | G′ 252,61 · tan δ 0,23 | G′ 438 · 0,23 | Literatura publicada |
| e.p.t.q S 100 | G′ 70,35 · tan δ 0,56 | G′ 36 · 0,46 | Fabricante · Anton Paar MCR302 · 0,1 Hz |
| e.p.t.q S 300 | G′ 226,00 · tan δ 0,23 | G′ 144 · 0,19 | idem |
| e.p.t.q S 500 | G′ 355,13 · tan δ 0,19 | G′ 232 · 0,14 | idem |
| Yvoire Classic + | G′ 319,88 · tan δ 0,14 | G′ 286 · 0,36 | Estudo comparativo de linha |
| Yvoire Volume + | G′ 358,50 · tan δ 0,16 | G′ 253 · 0,29 | idem |
| Yvoire Contour + | G′ 579,90 · tan δ 0,10 | G′ 484 · 0,32 | idem |

**Causas:** reômetro e geometria distintos (TA AR-1500ex, Ø20 mm, gap 500 µm × Anton Paar MCR302, 25 mm, gap 1.000 µm); frequência distinta (0,7 Hz × 0,1 Hz); desenho de estudo distinto (o comparativo Yvoire mede também partícula 693±344 a 1.258±742 e força de injeção 9,8 a 19 N); lote e geração distintos.

**Prova de que é protocolo e não desvio sistemático:** a divergência não tem direção única — e.p.t.q vem **menor**, Belotero vem **maior**, Yvoire vem menor em G′ e muito maior em tan δ.

---

## 5. Lote 4 — rejeitado, com motivo

Nenhum dos 23 valores conferiu, e as listas são internamente inconsistentes:

- **Ordenações quebradas:** ranking de alto G′ como `484, 483, 421, 411, 398, 665` (o 665 do Volux em 6º lugar); baixo G′ como `36, 43, 116, 127, 239, 236, 286, 255, 144`.
- **Mesmo produto com valores diferentes entre imagens:** Belotero Volume 483 × 438 × 253; Perfectha Subskin 421 × 343; e.p.t.q S 500 232 × 355 × 224.
- **Desvios grandes contra o banco:** Belotero Volume +91%; Restylane Volyme +74%; Belotero Volume (2ª imagem) +73%; Juvéderm Ultra XC +87%; e.p.t.q S 100 −49%; Restylane Lyft −43%.
- **Produtos inexistentes no banco:** "Rennova Ultradeep", "Perlane", "Belotero Soft".
- **Confusão de nomes:** Juvéderm Ultra × Ultra XC × Ultra Plus × Ultra Plus XC tratados como quatro produtos com quatro valores; o banco tem dois ensaios (Ultra XC 110,75 e Ultra Plus XC 161,39).

**Decisão:** os quatro recortes que essas imagens tentavam mostrar (alto G′, baixo G′, alto tan δ, alto G′ + maior tan δ) foram **reconstruídos nativamente** em SVG/HTML a partir do banco, no capítulo 15.

---

## 6. Reconciliação de nomenclatura

| Em outros materiais | Canônico neste livro |
|---|---|
| Yvoire Classic / Volume / Contour | Yvoire **Classic+ / Volume+ / Contour+** |
| Juvéderm Volite | **Juvéderm Skinvive** |
| Milimetric Fino / Moderado / Profundo | **Milimetric PRO Leve / Moderado / Intenso** |
| EVO Fine / Deep / Contour | **Evofill Derm / Evofill Ultra Deep** (só 2 ensaios no banco) |
| Finafill | **Finahfil Intense** |
| Belotero Soft · Perlane · Rennova Ultradeep | **não existem no banco** — nenhum valor lhes é atribuído |

---

## 7. Achado editorial: nome comercial ≠ reologia (linha Perfectha)

A escada comercial **Finelines → Derm → Deep → Subskin** é apresentada como suporte crescente. O G′ medido está invertido:

| Produto | G′ medido |
|---|---|
| Perfectha **Derm** | **440,68 Pa** |
| Perfectha Deep | 386,46 Pa |
| Perfectha **Subskin** | **343,00 Pa** |

O gel vendido como o mais estrutural tem o **menor** G′ dos três medidos. Isso não o desqualifica — coesividade, comportamento de bolus e tolerância a volume **não foram medidos** (💧). O que a medida desautoriza é a inferência "mais profundo no nome = maior G′". Está no capítulo 16.

---

## 8. Imagens integradas ao livro

Aprovadas e embutidas — todas **conceituais, sem dado de produto a auditar**:

| Imagem | Capítulo | Figura |
|---|---|---|
| Mapa geral da reologia (5 parâmetros) | 1 · Como ler este guia | 1 |
| Estrutura molecular do HA | 2 · A molécula e a rede | 3 |
| Formação do hidrogel / reticulação BDDE | 2 · A molécula e a rede | 4 |
| Degradação por hialuronidase | 2 · A molécula e a rede | 5 |
| Viscoelasticidade (Hooke, τ=η·γ̇, Maxwell/Kelvin-Voigt/Burgers) | 3 · Por que o gel é viscoelástico | 6 |

O desenho das cadeias de AH em contas (Figura 4) virou **ornamento da identidade visual**: aparece nos rodapés correntes de todas as páginas e nos filetes divisores de seção.

**Não integradas:** as 13 imagens do lote 4 (dados inconsistentes) e as tabelas de produto dos lotes 1–2 cujos números são de literatura/fabricante — estas últimas aparecem como **tabela comparativa de fontes** no capítulo 16, com a origem declarada, em vez de como imagem.

---

## 9. Duplicatas identificadas no acervo

- `16_25_23` ≡ `16_25_24` — byte-idênticas (1.621.958 bytes cada)
- `13_03_53` ≡ `12_51_45` — mesma peça Belotero em duas capturas
- `10_51_35` — variante sem dados de `10_54_53`
- `12_31_34` ≡ `12_31_35`
- `10_15_01` — não legível por OCR (PNG íntegro de 1.280.363 bytes; extração devolve vazio em 5 tentativas)

---

## 10. Pendências do banco (mantidas com ⚑)

Já sinalizadas antes desta auditoria e **confirmadas** por ela — as imagens reproduzem fielmente o banco, o que indica que a duplicação está na origem:

- Pares idênticos nas 6 frequências: Volift = Voluma · Belotero Volume + = Neauvia Intense · Neauvia Stimulate = Singderm
- η* aparentemente trocado entre Belotero Intense e Volume + a 1 Hz
- Yvoire Volume + sem lote registrado
