# -*- coding: utf-8 -*-
"""Auditor: confere valores alegados nas imagens contra o banco canônico."""
import json, sys, unicodedata, re

BASE = '/tmp/claude-0/-home-user-reologia-map/cd216e96-b088-57d1-abe3-2409c365400d/scratchpad'
DATA = {r['produto']: r for r in json.load(open(f'{BASE}/produtos_full.json'))}

def norm(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    s = re.sub(r'\b(lido|lidocaine|lidocaina)\b', '', s)
    s = re.sub(r'[^a-z0-9+]+', ' ', s)
    return ' '.join(s.split())

NORM = {norm(k): k for k in DATA}

ALIAS = {
    'belotero volume': 'Belotero Volume + Lido',
    'restylane': 'Restylane Lido (lote 22647)',
    'restylane classico': 'Restylane Lido (lote 22647)',
    'cutegel max': 'Cutegel Lidocaine CL-Max',
    'cutegel cl max': 'Cutegel Lidocaine CL-Max',
    'cl max': 'Cutegel Lidocaine CL-Max',
    'e p t q s100': 'e.p.t.q S 100 Lido', 'eptq s100': 'e.p.t.q S 100 Lido',
    'e p t q s300': 'e.p.t.q S 300 Lido', 'eptq s300': 'e.p.t.q S 300 Lido',
    'e p t q s500': 'e.p.t.q S 500 Lido', 'eptq s500': 'e.p.t.q S 500 Lido',
    'hyafilia soft': 'Hyafilia S Plus Lido', 'hyafilia mold': 'Hyafilia M Plus Lido',
    'hyafilia volume': 'Hyafilia V Plus Lido',
    'hyafilia s plus': 'Hyafilia S Plus Lido', 'hyafilia m plus': 'Hyafilia M Plus Lido',
    'hyafilia v plus': 'Hyafilia V Plus Lido',
    'yvoire classic': 'Yvoire Classic+ Lido', 'yvoire volume': 'Yvoire Volume+ Lido',
    'yvoire contour': 'Yvoire Contour+ Lido',
    'stylage lips': 'Stylage Lips Lido', 'stylage special lips': 'Stylage Lips Lido',
    'stylage l': 'Stylage L Lido', 'stylage xl': 'Stylage XL Lido',
    'rennova fine lines': 'Rennova Fill Fine Lines Lido',
    'rennova eyes lines': 'Rennova Fill Eyes Lines Lido',
    'rennova deep line': 'Rennova Deep Line Lido',
    'rennova lift plus': 'Rennova Lift Plus Lido',
    'rennova lips plus': 'Rennova Lips Plus Lido',
    'rennova ultra volume': 'Rennova Ultra Volume Lido',
    'milimetric leve': 'Milimetric PRO Leve Lido',
    'milimetric moderado': 'Milimetric PRO Moderado Lido',
    'milimetric intenso': 'Milimetric PRO Intenso Lido',
    'milimetric pro leve': 'Milimetric PRO Leve Lido',
    'milimetric pro moderado': 'Milimetric PRO Moderado Lido',
    'milimetric pro intenso': 'Milimetric PRO Intenso Lido',
    'juvederm ultra': 'Juvéderm Ultra XC Lido',
    'juvederm ultra plus': 'Juvéderm Ultra Plus XC Lido',
    'juvederm volbella': 'Juvéderm Volbella Lido',
    'juvederm volift': 'Juvéderm Volift Lido',
    'juvederm voluma': 'Juvéderm Voluma Lido',
    'juvederm skinvive': 'Juvéderm Skinvive',
    'skinvive': 'Juvéderm Skinvive', 'volux': 'Juvéderm Volux',
    'voluma': 'Juvéderm Voluma Lido', 'volift': 'Juvéderm Volift Lido',
    'volbella': 'Juvéderm Volbella Lido',
    'restylane lyft': 'Restylane Lyft Lido', 'lyft': 'Restylane Lyft Lido',
    'restylane shaype': 'Restylane Shaype Lido', 'shaype': 'Restylane Shaype Lido',
    'restylane refyne': 'Restylane Refyne Lido', 'refyne': 'Restylane Refyne Lido',
    'restylane defyne': 'Restylane Defyne Lido', 'defyne': 'Restylane Defyne Lido',
    'restylane kysse': 'Restylane Kysse Lido', 'kysse': 'Restylane Kysse Lido',
    'restylane volyme': 'Restylane Volyme Lido', 'volyme': 'Restylane Volyme Lido',
    'restylane skinbooster': 'Restylane Skinbooster Lido',
    'biogelis fine lines': 'Biogelis Fine lines',
    'biogelis global': 'Biogelis Global Lido',
    'biogelis volume': 'Biogelis Volume Lido',
    'biogelis volumax': 'Biogelis Volumax Lido',
    'neuramis': 'Neuramis Lido', 'neuramis deep': 'Neuramis Deep Lido',
    'saypha filler': 'Saypha Filler Lido', 'saypha volume': 'Saypha Volume Lido',
    'saypha volume plus': 'Saypha Volume Plus Lido',
    'revanesse kiss': 'Revanesse Kiss Lido',
    'revanesse contour': 'Revanesse Contour + Lido',
    'revanesse contour+': 'Revanesse Contour + Lido',
    'revanesse outline+': 'Revanesse Outline+ Lido',
    'revanesse shape+': 'Revanesse Shape + Lido',
    'revanesse ultra+': 'Revanesse Ultra + Lido',
    'up fine': 'Up Fine Lido', 'up deep': 'Up Deep Lido',
    'up contour': 'Up Contour Lido', 'up max': 'Up Max Lido',
    'belotero balance': 'Belotero Balance Lido',
    'belotero intense': 'Belotero Intense Lido',
    'evofill derm': 'Evofill Derm', 'evofill ultra deep': 'Evofill Ultra Deep',
    'perfectha derm': 'Perfectha Derm', 'perfectha deep': 'Perfectha Deep',
    'perfectha subskin': 'Perfectha Subskin',
    'sofiderm derm': 'Sofiderm Derm', 'sofiderm deep': 'Sofiderm Deep',
    'sofiderm fine lines': 'Sofiderm Fine Lines',
    'sofiderm derm plus': 'Sofiderm Derm Plus',
    'sofiderm sub skin': 'Sofiderm Derm Sub-Skin',
    'sofiderm derm sub skin': 'Sofiderm Derm Sub-Skin',
    'singderm': 'Singderm Lido', 'finahfil intense': 'Finahfil Intense',
    'neauvia intense': 'Neauvia Intense', 'neauvia stimulate': 'Neauvia Stimulate',
    'rennova fill': 'Rennova Fill', 'rennova lift': 'Rennova Lift',
}

def resolve(name):
    n = norm(name)
    if n in NORM: return NORM[n]
    if n in ALIAS: return ALIAS[n]
    cands = [k for kn, k in NORM.items() if n and (n in kn or kn in n)]
    if len(cands) == 1: return cands[0]
    return None

FIELD = {'g1': 'G1_0.7Hz', "g'": 'G1_0.7Hz', 'g2': 'G2_0.7Hz', "g''": 'G2_0.7Hz',
         'td': 'tand_0.7Hz', 'tan': 'tand_0.7Hz', 'eta': 'eta_0.7Hz'}
ERRATA = {('Perfectha Subskin', 'tand_0.7Hz'): 0.15}   # recálculo G″/G′

def check(name, field, claimed, tol=0.02):
    """Retorna (status, correto, produto_resolvido)."""
    p = resolve(name)
    if not p: return ('PRODUTO_NAO_ENCONTRADO', None, None)
    f = FIELD.get(field.lower().strip())
    if not f: return ('CAMPO_INVALIDO', None, p)
    real = ERRATA.get((p, f), DATA[p][f])
    if real is None: return ('SEM_DADO', None, p)
    d = abs(real - claimed)
    ok = d <= (tol if f == 'tand_0.7Hz' else max(0.6, real * 0.004))
    return ('OK' if ok else 'DIVERGENTE', real, p)

def ficha(name):
    p = resolve(name)
    if not p: return f'{name}: NÃO ENCONTRADO'
    d = DATA[p]; td = ERRATA.get((p, 'tand_0.7Hz'), d['tand_0.7Hz'])
    return (f"{p} | G′ {d['G1_0.7Hz']:.2f} · G″ {d['G2_0.7Hz']:.2f} · "
            f"tan δ {td:.2f} · η* {d['eta_0.7Hz']:.2f} | lote {d['lote']}")

if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print('uso: auditor.py "Produto"  |  auditor.py "Produto" g1 123.4')
        sys.exit(0)
    if len(args) == 1:
        print(ficha(args[0]))
    else:
        st, real, p = check(args[0], args[1], float(args[2].replace(',', '.')))
        print(f'{st} | alegado {args[2]} | banco {real} | produto {p}')
