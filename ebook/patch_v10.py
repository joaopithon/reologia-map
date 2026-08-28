# -*- coding: utf-8 -*-
"""v10 — geometria anatômica corrigida do mapa de regiões.
As bandas de borda (mandíbula, auricular anterior, temporal) são desenhadas
propositalmente atravessando o contorno: o clip da face as apara em faixas
que acompanham a borda. Traços do rosto passam a ser redesenhados por cima."""
import re
P = 'build_ebook.py'
src = open(P, encoding='utf-8').read()

NOVO_REG = '''REG = {
 'fronte':      ('c', 'M91,141 C93,109 119,99 150,99 C181,99 207,109 209,141 '
                      'C180,150 120,150 91,141 Z'),
 'temporal':    ('b', 'M96,130 C94,152 93,172 95,194 L74,200 C68,178 66,152 70,132 Z'),
 'supercilio':  ('b', 'M97,157 C109,143 131,141 143,150 L141,160 C130,152 111,153 100,164 Z'),
 'infraorb':    ('b', 'M101,182 C110,177 130,178 139,184 C134,199 112,202 102,192 Z'),
 'zigoma':      ('b', 'M78,193 C92,187 112,192 126,203 C124,212 118,216 110,212 '
                      'C98,206 86,203 77,203 Z'),
 'bochecha':    ('b', 'M88,222 C101,217 118,222 127,232 C125,249 107,258 91,249 Z'),
 'auricular':   ('b', 'M80,204 C80,222 82,240 86,258 L62,266 C56,250 52,230 50,200 Z'),
 'nariz':       ('c', 'M144,162 C147,158 153,158 156,162 C157,186 158,204 160,214 '
                      'C158,225 142,225 140,214 C142,204 143,186 144,162 Z'),
 'nasolabial':  ('b', 'M138,219 C130,230 124,246 126,265 L136,267 C134,250 137,236 144,226 Z'),
 'labios':      ('c', 'M129,258 C137,249 145,247 150,252 C155,247 163,249 171,258 '
                      'C162,275 138,275 129,258 Z'),
 'perioral':    ('c', 'M116,252 C124,236 140,242 150,245 C160,242 176,236 184,252 '
                      'C182,274 168,288 150,290 C132,288 118,274 116,252 Z'
                      'M129,258 C138,275 162,275 171,258 C163,249 155,247 150,252 '
                      'C145,247 137,249 129,258 Z'),
 'labiomentual':('c', 'M132,281 C140,275 160,275 168,281 C161,291 139,291 132,281 Z'),
 'mento':       ('c', 'M129,295 C139,290 161,290 171,295 C172,316 163,331 150,336 '
                      'C137,331 128,316 129,295 Z'),
 'mandibula':   ('b', 'M78,228 C82,266 96,300 124,326 L116,350 C74,326 46,290 38,234 Z'),
 'prejowl':     ('b', 'M108,298 C118,293 130,298 135,307 C128,320 112,320 105,311 Z'),
}'''
i = src.index('REG = {')
j = src.index('\n}', i) + 2
src = src[:i] + NOVO_REG + src[j:]

# traços do rosto redesenhados por cima das regiões
src = src.replace(
 "f'{FACE_ART}<g clip-path=\"url(#{uid})\">{shapes}</g>'\n"
 "            f'<path d=\"{FACE_CLIP}\" class=\"fc-edge\"/></svg>')",
 "f'{FACE_ART}<g clip-path=\"url(#{uid})\">{shapes}</g>'\n"
 "            f'<path d=\"{FACE_CLIP}\" class=\"fc-edge\"/>{FACE_FEATS}</svg>')", 1)

src = src.replace("def face_regioes(g, width=196):",
 "FACE_FEATS = FACE_ART[FACE_ART.index('<g class=\"fc-feat\">'):]\n\n"
 "def face_regioes(g, width=196):", 1)

# opacidade um pouco menor para não abafar os traços
src = src.replace('.facereg .rg{{fill:var(--rg-f);fill-opacity:.34;',
                  '.facereg .rg{{fill:var(--rg-f);fill-opacity:.30;', 1)
open(P, 'w', encoding='utf-8').write(src)
print('v10: geometria anatômica corrigida')
