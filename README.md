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
| [`data/reologia_produtos_full.json`](data/reologia_produtos_full.json) | Banco canônico: 76 produtos × 6 frequências (10 · 5 · 1 · 0,7 · 0,1 · 0,01 Hz) × 4 parâmetros (G′, G″, tan δ, η*), com lote e classificação |
| [`data/reologia_produtos_07hz.csv`](data/reologia_produtos_07hz.csv) | Recorte a 0,7 Hz (frequência de referência editorial), ordenado por G′ |

## Fonte dos dados

Laudo BioSmart Nanotechnology / Clínica Pithon Napoli, 04/08/2026 — reômetro TA Instruments AR-1500ex, 25 °C, placas paralelas Ø 20 mm, gap 500 µm, varredura de frequência 10 → 0,01 Hz. Números reológicos citados no projeto provêm exclusivamente desse ensaio; dados de fabricantes são sempre atribuídos como tal.

> ⚠ Linhas marcadas com flag `verificar_dado` no documento mestre aguardam re-verificação junto ao laboratório (ver §6 do documento).
