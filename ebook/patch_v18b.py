# -*- coding: utf-8 -*-
"""v18b — estilos das novas camadas de relevo, feicoes e pinos numerados."""
import pathlib
SRC = pathlib.Path(__file__).with_name('build_ebook.py')
s = SRC.read_text(encoding='utf-8'); orig = s

CSS = """
/* relevo anatomico: da apoio visual as regioes marcadas */
.fc-model{{pointer-events:none}}
.fc-model .fm-sh{{fill:var(--face-sh);opacity:.62;filter:url(#fcSoft)}}
.fc-model .fm-sh2{{fill:var(--face-sh);opacity:.5;filter:url(#fcSoft2)}}
.fc-model .fm-hi{{fill:var(--face-hi);opacity:.66;filter:url(#fcSoft)}}
.fc-model .fm-ln{{fill:none;stroke:var(--face-line);stroke-width:1.5;opacity:.28;
 stroke-linecap:round;filter:url(#fcSoft2)}}
.fc-model .fm-ln2{{fill:none;stroke:var(--face-line);stroke-width:2;opacity:.2;
 stroke-linecap:round;filter:url(#fcSoft)}}
.fc-model .fm-ln3{{fill:none;stroke:var(--face-line);stroke-width:1;opacity:.22;
 stroke-linecap:round}}
.fc-necksh{{fill:var(--face-sh);opacity:.55;filter:url(#fcSoft)}}
.fc-hairln path{{fill:none;stroke:var(--hair-line);stroke-width:1.1;opacity:.35;
 stroke-linecap:round}}
.fc-brow-f{{fill:var(--hair-1);stroke:none;opacity:.92}}
.fc-lidlo{{stroke:var(--face-line);stroke-width:1.1;opacity:.55}}
.fc-nostril ellipse{{fill:var(--face-line);opacity:.42;stroke:none}}
.fc-lipup{{fill:var(--lip);stroke:var(--lip-line);stroke-width:1.05;opacity:.94}}
.fc-liplo{{fill:var(--lip);stroke:var(--lip-line);stroke-width:1.05}}
.fc-liphi{{fill:#fff;opacity:.2;stroke:none}}
/* pinos numerados: ligam a mancha ao nome na legenda */
.rgpin circle{{fill:var(--rg-s);stroke:#fff;stroke-width:1.9}}
.rgpin text{{fill:#fff;font-family:'Barlow',sans-serif;font-size:10.5px;
 font-weight:700;text-anchor:middle}}
/* legenda numerada das regioes */
.rglist{{display:flex;flex-wrap:wrap;gap:.18rem .6rem;margin:.1rem 0 .4rem;
 font-family:'Barlow',sans-serif;font-size:.8rem;text-align:left}}
.rgli{{display:inline-flex;align-items:center;gap:.28rem;color:var(--ink);
 font-weight:600;white-space:nowrap}}
.rgli i{{flex:0 0 auto;width:14px;height:14px;border-radius:50%;
 background:var(--rg-s,var(--ink3));color:#fff;font-style:normal;font-weight:700;
 font-size:.62rem;line-height:14px;text-align:center}}
"""

anchor = ".fc-lash path{{fill:none;stroke:var(--lash);stroke-width:1.5;stroke-linecap:round}}"
assert anchor in s, 'ancora do CSS nao encontrada'
s = s.replace(anchor, anchor + CSS.rstrip(), 1)

SRC.write_text(s, encoding='utf-8')
print('patch v18b aplicado' if s != orig else 'nada mudou')
