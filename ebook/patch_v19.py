# -*- coding: utf-8 -*-
"""v19 — regioes nomeadas na propria figura, com linha de chamada.

v18 colocou pinos numerados mas nao ligou o numero a nenhuma legenda: o leitor
via "3" na tempora e nada que dissesse o que era 3. E com 6 regioes os pinos
colidiam. Agora cada regiao leva o nome ao lado da face, ligado por uma linha
fina — nao ha o que consultar.
"""
import pathlib
SRC = pathlib.Path(__file__).with_name('build_ebook.py')
s = SRC.read_text(encoding='utf-8'); orig = s

NEW = '''
def _rotulos(regs):
    """Distribui os rotulos nas duas colunas laterais sem sobreposicao.

    Bilaterais rotulam a instancia da esquerda (lado do observador); centrais
    alternam de lado para equilibrar a figura.
    """
    esq, dir_ = [], []
    alterna = 0
    for r in regs:
        lado, d, px, py = REG[r]
        if lado == 'b':
            esq.append([px, py, REG_NOME.get(r, r)])
        else:
            (dir_ if alterna % 2 == 0 else esq).append([px, py, REG_NOME.get(r, r)])
            alterna += 1
    for col in (esq, dir_):
        col.sort(key=lambda t: t[1])
        # empurra para baixo garantindo espaco minimo, depois acomoda no quadro
        y = 34.0
        for t in col:
            t.append(max(t[1], y))
            y = t[3] + 25
        excesso = (col[-1][3] if col else 0) - 372
        if excesso > 0:
            for t in col:
                t[3] -= excesso
    return esq, dir_

def face_regioes(g, width=196, cls='facereg', rotulos=True):
    """Face frontal com as regioes demarcadas e nomeadas na figura.

    Camadas: FACE_BASE (pele + relevo anatomico) recebe a cor da regiao e
    FACE_TOP (cabelo da frente, olhos, boca) volta por cima — a mancha nunca
    cai sobre o cabelo nem apaga uma feicao.
    """
    uid = f'fr{g["n"]}{abs(hash(tuple(g["regs"]))) % 9973}'
    fill = CORREG[g['cores'][0]]
    stroke = CORREG[g['cores'][-1]] if len(g['cores']) > 1 else fill
    DX = 116 if rotulos else 0
    VW = 532 if rotulos else 300
    shapes = ''
    for r in g['regs']:
        lado, d, px, py = REG[r]
        rule = ' fill-rule="evenodd"' if r == 'perioral' else ''
        nome = REG_NOME.get(r, r)
        shapes += f'<path d="{d}" class="rg"{rule}><title>{nome}</title></path>'
        if lado == 'b':
            shapes += (f'<g transform="translate(300,0) scale(-1,1)">'
                       f'<path d="{d}" class="rg"{rule}><title>{nome}</title></path></g>')
    lbl = ''
    if rotulos:
        esq, dir_ = _rotulos(g['regs'])
        for px, py, nome, ly in esq:
            ax = px + DX
            lbl += (f'<path class="rgld" d="M{ax - 6},{py} L{DX - 14},{py} '
                    f'L{DX - 26},{ly:.0f} L{DX - 34},{ly:.0f}"/>'
                    f'<circle class="rgan" cx="{ax}" cy="{py}" r="2.9"/>'
                    f'<text class="rglb" x="{DX - 39}" y="{ly:.0f}" dy="3.4" '
                    f'text-anchor="end">{html.escape(nome)}</text>')
        for px, py, nome, ly in dir_:
            ax = px + DX
            # centrais: sai pela direita, contornando a face
            lbl += (f'<path class="rgld" d="M{ax + 6},{py} L{DX + 314},{py} '
                    f'L{DX + 326},{ly:.0f} L{DX + 334},{ly:.0f}"/>'
                    f'<circle class="rgan" cx="{ax}" cy="{py}" r="2.9"/>'
                    f'<text class="rglb" x="{DX + 339}" y="{ly:.0f}" dy="3.4" '
                    f'text-anchor="start">{html.escape(nome)}</text>')
    gopen = f'<g transform="translate({DX},0)">' if DX else ''
    gclose = '</g>' if DX else ''
    return (f'<svg class="{cls}" viewBox="0 0 {VW} 400" role="img" '
            f'style="width:{width}px;--rg-f:{fill};--rg-s:{stroke}" '
            f'aria-label="regioes faciais do grupo {g["n"]}: {html.escape(g["txt"])}">'
            f'{FACE_DEFS}'
            f'<defs><clipPath id="{uid}"><path d="{FACE_CLIP}"/></clipPath></defs>'
            f'{gopen}{FACE_BASE}<g clip-path="url(#{uid})">{shapes}</g>'
            f'<path d="{FACE_CLIP}" class="fc-edge"/>{FACE_TOP}{gclose}{lbl}</svg>')
'''

i0 = s.index('def face_regioes(')
i1 = s.index('def regs_numerados(')
i2 = s.index('def mapa_regioes():')
s = s[:i0] + NEW.strip() + '\n\n' + s[i2:]

# largura maior: a figura agora carrega as duas colunas de rotulo
s = s.replace("def face_fam(f, width=210, cls='facereg'):",
              "def face_fam(f, width=430, cls='facereg'):")
s = s.replace("f'{face_regioes(g, 150)}<p>{txt}</p></figure>')",
              "f'{face_regioes(g, 330)}<p>{txt}</p></figure>')")
s = s.replace("f'{face_fam(f, 168, \"facereg capa-face\")}</figure>')",
              "f'{face_fam(f, 168, \"facereg capa-face\")}</figure>')")
# capa: sem rotulos, o trio e decorativo e minusculo
s = s.replace("def face_fam(f, width=430, cls='facereg'):\n"
              "    g = dict(n=f['n'], regs=f['regs'], cores=[f['cor'], f['sub'][-1][1][-1]], txt=f['regs_txt'])\n"
              "    return face_regioes(g, width, cls)",
              "def face_fam(f, width=430, cls='facereg'):\n"
              "    g = dict(n=f['n'], regs=f['regs'], cores=[f['cor'], f['sub'][-1][1][-1]], txt=f['regs_txt'])\n"
              "    return face_regioes(g, width, cls, rotulos='capa-face' not in cls)")

CSS = """
/* rotulos das regioes na figura: nome ligado a mancha por linha de chamada */
.rgld{{fill:none;stroke:var(--rg-s);stroke-width:1.1;opacity:.62;
 stroke-linejoin:round;stroke-linecap:round}}
.rgan{{fill:var(--rg-s);stroke:#fff;stroke-width:1.1}}
.rglb{{fill:var(--ink);font-family:'Barlow',sans-serif;font-size:14px;font-weight:600}}
"""
anchor = ".rgli i{{flex:0 0 auto;width:14px;height:14px;border-radius:50%;\n background:var(--rg-s,var(--ink3));color:#fff;font-style:normal;font-weight:700;\n font-size:.62rem;line-height:14px;text-align:center}}"
if anchor in s:
    s = s.replace(anchor, anchor + CSS.rstrip(), 1)
else:
    s = s.replace(".rgpin circle{{", CSS.strip() + "\n.rgpin circle{{", 1)

SRC.write_text(s, encoding='utf-8')
print('patch v19 aplicado' if s != orig else 'nada mudou')
