# -*- coding: utf-8 -*-
"""Auditoria formal do lote 1 (14 imagens) contra o banco canônico."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-reologia-map/cd216e96-b088-57d1-abe3-2409c365400d/scratchpad')
from auditor import check, ficha, resolve, DATA

# ---------------------------------------------------------------- 16_43_38
# TABELA SIMPLIFICADA 0,7 Hz — 42 produtos × (G', G", tan δ)
TAB = [
 ('Belotero Intense Lido',        186.11, 60.69, 0.33),
 ('Belotero Volume + Lido',       252.61, 57.31, 0.23),
 ('Biogelis Volumax Lido',        385.93, 71.79, 0.19),
 ('Biogelis Volume Lido',         251.51, 48.87, 0.19),
 ('Cutegel Lidocaine CL-Max',     282.48, 56.87, 0.20),
 ('E.p.t.q S100 Lido',             70.35, 39.28, 0.56),
 ('E.p.t.q S300 Lido',            226.00, 53.09, 0.23),
 ('E.p.t.q S500 Lido',            355.13, 67.30, 0.23),
 ('Neauvia Intense',              252.61, 57.31, 0.23),
 ('Neauvia Stimulate',            285.83, 78.16, 0.27),
 ('Neuramis Deep Lido',           164.47, 43.84, 0.27),
 ('Neuramis Lido',                 89.70, 34.31, 0.38),
 ('Neuramis Volume',              314.05, 48.17, 0.15),
 ('Perfectha Deep',               386.46, 46.88, 0.12),
 ('Perfectha Derm',               440.68, 50.10, 0.11),
 ('Perfectha Subskin',            343.00, 52.00, 0.20),
 ('Rennova Deep Line Lido',       183.33, 31.85, 0.17),
 ('Restylane Defyne Lido',        292.62, 24.28, 0.08),
 ('Restylane Kysse Lido',         178.82, 24.53, 0.14),
 ('Restylane Lido',               617.71, 162.40, 0.26),
 ('Restylane Lyft Lido',          718.22, 128.63, 0.18),
 ('Restylane Shaype Lido',        935.94, 141.80, 0.15),
 ('Restylane Volyme Lido',        137.69, 22.68, 0.16),
 ('Revanesse Contour + Lido',     142.29, 39.24, 0.28),
 ('Revanesse Kiss Lido',          131.06, 50.83, 0.39),
 ('Revanesse Outline+ Lido',      148.24, 32.83, 0.22),
 ('Revanesse Shape + Lido',       172.61, 30.79, 0.18),
 ('Revanesse Ultra + Lido',       127.76, 39.36, 0.31),
 ('Saypha Filler Lido',           142.61, 39.36, 0.24),
 ('Saypha Volume Lido',           251.93, 29.52, 0.12),
 ('Saypha Volume Plus Lido',      488.91, 35.54, 0.07),
 ('Singderm Lido',                285.83, 78.16, 0.27),
 ('Stylage L Lido',               260.15, 41.82, 0.16),
 ('Stylage Lips Lido',            167.01, 34.95, 0.21),
 ('Stylage XL Lido',              305.08, 46.59, 0.15),
 ('Up Contour Lido',              328.48, 47.92, 0.15),
 ('Up Deep Lido',                 172.67, 31.94, 0.18),
 ('Up Fine Lido',                  33.66, 12.28, 0.36),
 ('Up Max Lido',                  351.32, 72.19, 0.21),
 ('Yvoire Classic+ Lido',         319.88, 45.65, 0.14),
 ('Yvoire Contour+ Lido',         579.90, 60.64, 0.10),
 ('Yvoire Volume+ Lido',          358.50, 55.99, 0.16),
]

# ---------------------------------------------------------------- rankings
TOP_MENOR = [('Up Fine Lido',33.66),('E.p.t.q S100 Lido',70.35),('Neuramis Lido',89.70),
 ('Revanesse Ultra + Lido',127.76),('Revanesse Kiss Lido',131.06),('Restylane Volyme Lido',137.69),
 ('Revanesse Contour + Lido',142.29),('Saypha Filler Lido',142.61),('Revanesse Outline+ Lido',148.24),
 ('Neuramis Deep Lido',164.47)]

TOP_MAIOR = [('Restylane Shaype Lido',935.94),('Restylane Lyft Lido',718.22),('Restylane Lido',617.71),
 ('Yvoire Contour+ Lido',579.90),('Saypha Volume Plus Lido',488.91),('Perfectha Derm',440.68),
 ('Perfectha Deep',386.46),('Biogelis Volumax Lido',385.93),('Yvoire Volume+ Lido',358.50),
 ('E.p.t.q S500 Lido',355.13)]

FILTRO = [('Neauvia Stimulate',285.83,0.27),('Singderm Lido',285.83,0.27),('Restylane Lido',617.71,0.26),
 ('Belotero Volume + Lido',252.61,0.23),('Neauvia Intense',252.61,0.23),('E.p.t.q S300 Lido',226.00,0.23),
 ('Up Max Lido',351.32,0.21)]

# ---------------------------------------------------------------- Yvoire (literatura/fabricante)
YV_LIT = [('Yvoire Classic+ Lido',286,103,0.3624),('Yvoire Volume+ Lido',253,73,0.2910),
          ('Yvoire Contour+ Lido',484,157,0.3245)]
YV_FREQ = [('Yvoire Classic+ Lido',325,40,0.15),('Yvoire Volume+ Lido',253,73,0.29),
           ('Yvoire Contour+ Lido',600,60,0.10)]

def bloco(titulo, linhas):
    print(f'\n{"="*78}\n{titulo}\n{"="*78}')
    div = 0
    for l in linhas:
        nome = l[0]
        p = resolve(nome)
        if not p:
            print(f'  ✗ {nome:30s} PRODUTO NÃO ENCONTRADO NO BANCO'); div += 1; continue
        campos = [('g1', l[1])]
        if len(l) > 2: campos.append(('g2', l[2]))
        if len(l) > 3: campos.append(('td', l[3]))
        if len(l) == 3 and isinstance(l[2], float) and l[2] < 1.5:  # (nome, g1, td)
            campos = [('g1', l[1]), ('td', l[2])]
        bad = []
        for f, v in campos:
            st, real, _ = check(nome, f, v)
            if st != 'OK':
                bad.append(f'{f}: alegado {v} · banco {real}')
        if bad:
            div += 1
            print(f'  ✗ {nome:30s} ' + ' | '.join(bad))
        else:
            print(f'  ✓ {nome:30s} ok')
    print(f'\n  → {len(linhas)-div}/{len(linhas)} produtos conferem · {div} divergência(s)')
    return div

t = 0
t += bloco('16_43_38 — TABELA SIMPLIFICADA 0,7 Hz (42 produtos × G′/G″/tan δ)', TAB)
t += bloco('16_50_54 — TOP 10 MENORES G′', TOP_MENOR)
t += bloco('16_48_00 — TOP 10 MAIORES G′', TOP_MAIOR)
t += bloco('18_56_20 — FILTRO G′≥200 & tan δ≥0,21 (G′ + tan δ)', FILTRO)
t += bloco('15_48_38 / 15_44_31_2 — YVOIRE (valores de literatura/fabricante)', YV_LIT)
t += bloco('15_44_31_3 — YVOIRE (curvas de frequência)', YV_FREQ)

print(f'\n{"#"*78}\nTOTAL DE PRODUTOS COM DIVERGÊNCIA: {t}\n{"#"*78}')

# ---------------------------------------------------------------- ordenação
print('\nVERIFICAÇÃO DE ORDENAÇÃO (monotonicidade dos rankings)')
for nm, lst, rev in [('TOP 10 MENORES G′', TOP_MENOR, False), ('TOP 10 MAIORES G′', TOP_MAIOR, True)]:
    vals = [v for _, v in lst]
    ok = all(vals[i] <= vals[i+1] for i in range(len(vals)-1)) if not rev else \
         all(vals[i] >= vals[i+1] for i in range(len(vals)-1))
    print(f'  {"✓" if ok else "✗"} {nm}: {"monotônico" if ok else "FORA DE ORDEM"}')

# o TOP 10 é realmente o top 10 do banco?
print('\nO TOP 10 corresponde ao banco?')
todos = sorted(((r['G1_0.7Hz'], r['produto']) for r in DATA.values() if r['G1_0.7Hz']), key=lambda x: x[0])
print('  10 menores no banco:')
for v, p in todos[:10]: print(f'    {v:8.2f}  {p}')
print('  10 maiores no banco:')
for v, p in reversed(todos[-10:]): print(f'    {v:8.2f}  {p}')

# filtro reproduzível?
print('\nFiltro G′≥200 & tan δ≥0,21 recalculado no banco:')
from auditor import ERRATA
sel = []
for r in DATA.values():
    g, td = r['G1_0.7Hz'], ERRATA.get((r['produto'],'tand_0.7Hz'), r['tand_0.7Hz'])
    if g and td and g >= 200 and td >= 0.21: sel.append((td, g, r['produto']))
for td, g, p in sorted(sel, reverse=True): print(f'    tan δ {td:.2f} · G′ {g:7.2f}  {p}')
print(f'  → {len(sel)} produtos (a imagem afirma 7)')
