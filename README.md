# Reologia Map

Projeto **Reology Map** — reologia do ácido hialurônico aplicada à seleção de preenchedores faciais.
Autor: Dr. João Pithon · Clínica Pithon Napoli.

Um banco de dados reológico proprietário (76 géis comerciais do mercado brasileiro, medidos sob protocolo único pela BioSmart Nanotechnology) que alimenta dois produtos:

1. **Aplicativo Reology Map** — ferramenta de decisão clínica para injetores (região/objetivo/tecido → produtos ranqueados com justificativa reológica);
2. **Livro "Reologia do Ácido Hialurônico — Ciência dos Géis Aplicada ao Preenchimento Facial"**.

## Conteúdo deste repositório

| Caminho | Descrição |
|---|---|
| [`docs/DOCUMENTO-MESTRE.md`](docs/DOCUMENTO-MESTRE.md) | **Documento mestre do projeto** — consolidação de todo o acervo: base científica, banco de dados, sistema de classificação (Mapa da Reologia), reologia clínica por região, especificação do aplicativo, estrutura do livro, fluxo editorial, governança de dados e roadmap |
| [`docs/ENREDO-DO-LIVRO.md`](docs/ENREDO-DO-LIVRO.md) | **Contrato narrativo do livro** — a promessa, o escopo declarado × medido, as três famílias de G′ (baixo · moderado · alto), as subclasses, a cadeia capítulo a capítulo, as dívidas em aberto e a definição operacional de "informação completa". É a referência contra a qual o livro é revisado |
| [`.claude/agents/revisora-livro.md`](.claude/agents/revisora-livro.md) | **Revisora do livro** — agente de revisão editorial-científica: lê o livro inteiro, confere o enredo contra o contrato, recalcula todo número a partir do banco canônico e fecha cada achado com texto pronto. Modos `auditar` e `corrigir` |
| [`data/reologia_produtos_full.json`](data/reologia_produtos_full.json) | Banco canônico: 76 produtos × 6 frequências (10 · 5 · 1 · 0,7 · 0,1 · 0,01 Hz) × 4 parâmetros (G′, G″, tan δ, η*), com lote e classificação |
| [`data/reologia_produtos_07hz.csv`](data/reologia_produtos_07hz.csv) | Recorte a 0,7 Hz (frequência de referência editorial), ordenado por G′ |

## Fonte dos dados

Laudo BioSmart Nanotechnology / Clínica Pithon Napoli, 04/08/2026 — reômetro TA Instruments AR-1500ex, 25 °C, placas paralelas Ø 20 mm, gap 500 µm, varredura de frequência 10 → 0,01 Hz. Números reológicos citados no projeto provêm exclusivamente desse ensaio; dados de fabricantes são sempre atribuídos como tal.

> ⚠ Linhas marcadas com flag `verificar_dado` no documento mestre aguardam re-verificação junto ao laboratório (ver §6 do documento).
