# -*- coding: utf-8 -*-
"""v20 — rotulos com margem suficiente, lados fixos e nomes acentuados.

v19 cortava os rotulos longos nas bordas do quadro ("ular anterior") e deixava
as linhas de chamada cruzarem a face inteira. Aqui: margem lateral real,
bilateral sempre a esquerda / central sempre a direita (nao ha cruzamento entre
colunas), nomes curtos e acentuados, e ancoragem na borda da mancha em vez do
centro, o que encurta a linha.
"""
import pathlib
SRC = pathlib.Path(__file__).with_name('build_ebook.py')
s = SRC.read_text(encoding='utf-8'); orig = s

# ------------------------------------------------------- nomes curtos, com acento
NOMES = """REG_NOME = {
 'fronte': 'fronte', 'temporal': 'têmpora', 'supercilio': 'supercílio',
 'infraorb': 'infraorbitária', 'zigoma': 'zigomático',
 'bochecha': 'bochecha', 'auricular': 'pré-auricular',
 'nariz': 'nariz', 'nasolabial': 'nasolabial', 'labios': 'lábio',
 'perioral': 'perioral', 'labiomentual': 'labiomentual',
 'mento': 'mento', 'mandibula': 'mandíbula', 'prejowl': 'pré-jowl',
}"""
i0 = s.index('REG_NOME = {')
i1 = s.index('}', s.index("'mento': 'mento'", i0)) + 1
s = s[:i0] + NOMES + s[i1:]

# ----------------------------------------------- layout dos rotulos e da figura
NEW = '''
MARG_L, MARG_R = 132, 122          # espaco reservado a cada coluna de rotulo

def _rotulos(regs):
    """Bilaterais rotulam a esquerda, centrais a direita — colunas nunca se cruzam.

    Devolve (esquerda, direita) com [ancora_x, ancora_y, nome, y_do_rotulo].
    """
    esq = [[px, py, REG_NOME.get(r, r)] for r in regs
           for lado, d, px, py in [REG[r]] if lado == 'b']
    dire = [[px, py, REG_NOME.get(r, r)] for r in regs
            for lado, d, px, py in [REG[r]] if lado == 'c']
    for col in (esq, dire):
        col.sort(key=lambda t: t[1])
        y = 40.0
        for t in col:
            t.append(max(t[1], y))
            y = t[3] + 26
        sobra = (col[-1][3] if col else 0) - 366
        if sobra > 0:
            for t in col:
                t[3] -= sobra
    return esq, dire

def face_regioes(g, width=196, cls='facereg', rotulos=True):
    """Face frontal com as regioes demarcadas e nomeadas na propria figura.

    Camadas: FACE_BASE (pele + relevo anatomico) recebe a cor da regiao e
    FACE_TOP (cabelo da frente, olhos, boca) volta por cima — a mancha nunca
    cai sobre o cabelo nem apaga uma feicao.
    """
    uid = f'fr{g["n"]}{abs(hash(tuple(g["regs"]))) % 9973}'
    fill = CORREG[g['cores'][0]]
    stroke = CORREG[g['cores'][-1]] if len(g['cores']) > 1 else fill
    DX = MARG_L if rotulos else 0
    VW = (MARG_L + 300 + MARG_R) if rotulos else 300
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
        esq, dire = _rotulos(g['regs'])
        for px, py, nome, ly in esq:
            ax, tx = px + DX, DX - 46
            lbl += (f'<path class="rgld" d="M{ax - 5},{py} L{DX - 18},{py} '
                    f'L{DX - 30},{ly:.0f} L{tx + 4},{ly:.0f}"/>'
                    f'<circle class="rgan" cx="{ax}" cy="{py}" r="2.8"/>'
                    f'<text class="rglb" x="{tx}" y="{ly:.0f}" dy="3.5" '
                    f'text-anchor="end">{html.escape(nome)}</text>')
        for px, py, nome, ly in dire:
            ax, tx = px + DX, DX + 300 + 46
            lbl += (f'<path class="rgld" d="M{ax + 5},{py} L{DX + 318},{py} '
                    f'L{DX + 330},{ly:.0f} L{tx - 4},{ly:.0f}"/>'
                    f'<circle class="rgan" cx="{ax}" cy="{py}" r="2.8"/>'
                    f'<text class="rglb" x="{tx}" y="{ly:.0f}" dy="3.5" '
                    f'text-anchor="start">{html.escape(nome)}</text>')
    gopen = f'<g transform="translate({DX},0)">' if DX else ''
    gclose = '</g>' if DX else ''
    return (f'<svg class="{cls}" viewBox="0 0 {VW} 400" role="img" '
            f'style="width:{width}px;--rg-f:{fill};--rg-s:{stroke}" '
            f'aria-label="regiões faciais do grupo {g["n"]}: {html.escape(g["txt"])}">'
            f'{FACE_DEFS}'
            f'<defs><clipPath id="{uid}"><path d="{FACE_CLIP}"/></clipPath></defs>'
            f'{gopen}{FACE_BASE}<g clip-path="url(#{uid})">{shapes}</g>'
            f'<path d="{FACE_CLIP}" class="fc-edge"/>{FACE_TOP}{gclose}{lbl}</svg>')
'''
i0 = s.index('MARG_L, MARG_R') if 'MARG_L' in s else s.index('def _rotulos(')
i1 = s.index('def mapa_regioes():')
s = s[:i0] + NEW.strip() + '\n\n' + s[i1:]

# ------------------------------------------------- formas: nariz e bochecha/orelha
s = s.replace(
 "'nariz':       ('c', 'M144,166 C147,161 153,161 156,166 C157,188 158,205 160,215 '\n"
 "                      'C158,227 142,227 140,215 C142,205 143,188 144,166 Z', 150, 193),",
 "'nariz':       ('c', 'M146,168 C148,164 152,164 154,168 C155,189 156,204 158,214 '\n"
 "                      'C156,224 144,224 142,214 C144,204 145,189 146,168 Z', 150, 192),")
s = s.replace(
 "'bochecha':    ('b', 'M90,219 C103,215 119,223 127,235 C121,251 101,255 91,243 '\n"
 "                      'C87,234 87,225 90,219 Z', 107, 235),",
 "'bochecha':    ('b', 'M89,216 C102,214 117,222 125,235 C121,250 104,256 93,247 '\n"
 "                      'C87,240 85,227 89,216 Z', 104, 234),")
s = s.replace(
 "'auricular':   ('b', 'M79,203 C79,222 81,241 85,259 L63,266 C57,249 53,229 51,201 Z',\n"
 "                 67, 232),",
 "'auricular':   ('b', 'M80,201 C79,220 80,239 84,257 C74,262 66,262 62,258 '\n"
 "                      'C57,242 54,222 53,200 C62,197 72,197 80,201 Z', 68, 229),")

# --------------------------------------------------------- largura das figuras
s = s.replace("def face_fam(f, width=430, cls='facereg'):",
              "def face_fam(f, width=468, cls='facereg'):")
s = s.replace("f'{face_regioes(g, 330)}<p>{txt}</p></figure>')",
              "f'{face_regioes(g, 352)}<p>{txt}</p></figure>')")

# rotulo um pouco maior, ja que a figura cresceu
s = s.replace(".rglb{{fill:var(--ink);font-family:'Barlow',sans-serif;font-size:14px;font-weight:600}}",
              ".rglb{{fill:var(--ink);font-family:'Barlow',sans-serif;font-size:15.5px;\n"
              " font-weight:600;letter-spacing:-.1px}}")
s = s.replace(".facereg{{display:block;margin:.2rem auto .5rem;height:auto}}",
              ".facereg{{display:block;margin:.2rem auto .5rem;height:auto;max-width:100%}}")

SRC.write_text(s, encoding='utf-8')
print('patch v20 aplicado' if s != orig else 'nada mudou')
