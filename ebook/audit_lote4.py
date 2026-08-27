# -*- coding: utf-8 -*-
"""Auditoria formal do lote 4 (rankings com inconsistências internas)."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-reologia-map/cd216e96-b088-57d1-abe3-2409c365400d/scratchpad')
from auditor import check, resolve, DATA, ERRATA

BLOCOS = [
 ('10_44_43 — RANKING DE ALTO G′ (Pa)', [
   ('Yvoire Contour', 484), ('Belotero Volume', 483), ('Perfectha Subskin', 421),
   ('Restylane Lyft', 411), ('Juvederm Voluma', 398), ('Juvederm Volux', 665)]),
 ('10_42_12_1 — PRINCIPAIS PREENCHEDORES DE BAIXO G′', [
   ('e.p.t.q S100', 36), ('Rennova Ultradeep', 43), ('Restylane Refyne', 116),
   ('Neuramis Deep', 127), ('Restylane Volyme', 239), ('Restylane Kysse', 236),
   ('Yvoire Classic', 286), ('Belotero Intense', 255), ('e.p.t.q S300', 144)]),
 ('10_42_14_3 — ALTO G′ E COESIVIDADE', [
   ('Neuramis Volume', 281), ('Yvoire Volume', 253), ('Belotero Volume', 438),
   ('Juvederm Ultra', 156), ('Juvederm Ultra XC', 207), ('Juvederm Ultra Plus', 214),
   ('Juvederm Ultra Plus XC', 263), ('e.p.t.q S300', 316)]),
]

tot = ok_n = 0
for titulo, linhas in BLOCOS:
    print(f'\n{"="*78}\n{titulo}\n{"="*78}')
    for nome, v in linhas:
        p = resolve(nome)
        if not p:
            print(f'  ⊘ {nome:26s} alegado {v:>6}  →  PRODUTO NÃO EXISTE NO BANCO'); tot += 1; continue
        st, real, _ = check(nome, 'g1', v)
        tot += 1
        if st == 'OK':
            ok_n += 1; print(f'  ✓ {nome:26s} alegado {v:>6}  ·  banco {real:7.2f}')
        else:
            erro = 100*(v-real)/real
            print(f'  ✗ {nome:26s} alegado {v:>6}  ·  banco {real:7.2f}   ({erro:+.0f}%)  [{p}]')

print(f'\n{"#"*78}\nLOTE 4: {ok_n}/{tot} valores conferem com o banco ({100*ok_n//tot}%)\n{"#"*78}')

# monotonicidade
print('\nCONSISTÊNCIA INTERNA (o ranking está em ordem?)')
for titulo, linhas in BLOCOS:
    vals = [v for _, v in linhas]
    cresc = all(vals[i] <= vals[i+1] for i in range(len(vals)-1))
    decr  = all(vals[i] >= vals[i+1] for i in range(len(vals)-1))
    print(f'  {"✓" if (cresc or decr) else "✗"} {titulo.split(" — ")[1][:44]:46s} '
          f'{"ordenado" if (cresc or decr) else "FORA DE ORDEM: " + str(vals)}')

# rankings corretos, reconstruídos do banco
print('\n\nRANKINGS CORRETOS RECONSTRUÍDOS DO BANCO (0,7 Hz, 76 ensaios)')
todos = sorted(((r['G1_0.7Hz'], r['produto']) for r in DATA.values() if r['G1_0.7Hz']))
print('\n  ALTO G′ — 10 maiores:')
for i, (v, p) in enumerate(reversed(todos[-10:]), 1): print(f'    {i:2d}. {p:38s} {v:7.2f} Pa')
print('\n  BAIXO G′ — 10 menores:')
for i, (v, p) in enumerate(todos[:10], 1): print(f'    {i:2d}. {p:38s} {v:7.2f} Pa')
print('\n  ALTO TAN δ — 10 maiores:')
tds = sorted(((ERRATA.get((r['produto'],'tand_0.7Hz'), r['tand_0.7Hz']), r['G1_0.7Hz'], r['produto'])
              for r in DATA.values() if r['tand_0.7Hz']), reverse=True)
for i, (td, g, p) in enumerate(tds[:10], 1): print(f'    {i:2d}. {p:38s} tan δ {td:.2f} · G′ {g:7.2f}')
print('\n  ALTO G′ (≥300) + MAIOR TAN δ — os 8 primeiros:')
mix = sorted(((ERRATA.get((r['produto'],'tand_0.7Hz'), r['tand_0.7Hz']), r['G1_0.7Hz'], r['produto'])
              for r in DATA.values() if r['G1_0.7Hz'] and r['G1_0.7Hz'] >= 300 and r['tand_0.7Hz']), reverse=True)
for i, (td, g, p) in enumerate(mix[:8], 1): print(f'    {i:2d}. {p:38s} tan δ {td:.2f} · G′ {g:7.2f}')
