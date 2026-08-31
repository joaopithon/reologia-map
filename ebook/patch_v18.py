# -*- coding: utf-8 -*-
"""v18 — faces humanizadas com relevo anatomico e regioes identificadas por numero.

Tres problemas resolvidos:
1. A face era chapada: uma mancha "no arco zigomatico" nao tinha relevo onde se apoiar.
   Entra uma camada de modelagem (fc-model) com as concavidades e saliencias reais.
2. As regioes nao tinham nome ligado a elas: 6 manchas roxas e uma lista de 6 nomes
   embaixo. Agora cada regiao recebe um pino numerado e a lista e numerada igual.
3. As regioes eram desenhadas por cima do cabelo. A ordem de camadas foi corrigida
   (FACE_BASE -> regioes -> FACE_TOP), so a pele recebe cor.
"""
import io, re, sys, pathlib

SRC = pathlib.Path(__file__).with_name('build_ebook.py')
s = SRC.read_text(encoding='utf-8')
orig = s

# ---------------------------------------------------------------- 1. FACE_ART
FACE_NEW = '''
FACE_BASE = """
<defs>
 <radialGradient id="fcSkin" cx="50%" cy="30%" r="80%">
  <stop offset="0%" stop-color="var(--face-hi)"/>
  <stop offset="55%" stop-color="var(--face-fill)"/>
  <stop offset="100%" stop-color="var(--face-sh)"/>
 </radialGradient>
 <linearGradient id="fcHair" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="var(--hair-2)"/>
  <stop offset="100%" stop-color="var(--hair-1)"/>
 </linearGradient>
 <filter id="fcSoft" x="-40%" y="-40%" width="180%" height="180%">
  <feGaussianBlur stdDeviation="4.2"/>
 </filter>
 <filter id="fcSoft2" x="-40%" y="-40%" width="180%" height="180%">
  <feGaussianBlur stdDeviation="2.4"/>
 </filter>
</defs>
<g class="fc-body">
 <path class="fc-neck" d="M124,322 C125,345 122,357 116,367 C99,374 80,381 67,391
  C62,395 59,398 58,400 L242,400 C241,398 238,395 233,391 C220,381 201,374 184,367
  C178,357 175,345 176,322 Z"/>
 <path class="fc-necksh" d="M126,326 C133,342 167,342 174,326 C176,344 172,357 165,364
  C156,369 144,369 135,364 C128,357 124,344 126,326 Z"/>
 <path class="fc-sh" d="M150,369 C139,369 129,367 121,363 C115,373 111,386 109,400
  L191,400 C189,386 185,373 179,363 C171,367 161,369 150,369 Z"/>
</g>
<path class="fc-hairb" d="M150,60 C205,60 241,97 243,157 C244,192 241,228 234,260
 C231,273 227,284 222,293 L208,284 C217,252 222,215 220,178 C216,130 194,100 150,100
 C106,100 84,130 80,178 C78,215 83,252 92,284 L78,293 C73,284 69,273 66,260
 C59,228 56,192 57,157 C59,97 95,60 150,60 Z"/>
<path class="fc-face" d="M150,344 C174,341 193,326 205,305 C216,287 223,262 225,231 C227,201 226,171 222,147 C218,120 202,102 181,94 C171,90 161,88 150,88 C139,88 129,90 119,94 C98,102 82,120 78,147 C74,171 73,201 75,231 C77,262 84,287 95,305 C107,326 126,341 150,344 Z"/>

<!-- relevo anatomico: e o que da apoio visual as regioes -->
<g class="fc-model" clip-path="url(#fcFaceClip)">
 <!-- fossa temporal -->
 <path class="fm-sh" d="M81,140 C91,149 97,166 96,188 C87,193 79,186 76,171
  C74,158 76,146 81,140 Z"/>
 <path class="fm-sh" d="M219,140 C209,149 203,166 204,188 C213,193 221,186 224,171
  C226,158 224,146 219,140 Z"/>
 <!-- sulco infraorbitario -->
 <path class="fm-sh2" d="M105,182 C115,179 131,181 139,187 C133,197 114,199 106,192 Z"/>
 <path class="fm-sh2" d="M195,182 C185,179 169,181 161,187 C167,197 186,199 194,192 Z"/>
 <!-- saliencia malar / arco zigomatico -->
 <ellipse class="fm-hi" cx="103" cy="204" rx="22" ry="12" transform="rotate(-14 103 204)"/>
 <ellipse class="fm-hi" cx="197" cy="204" rx="22" ry="12" transform="rotate(14 197 204)"/>
 <!-- concavidade submalar -->
 <path class="fm-sh" d="M93,217 C105,216 119,224 125,236 C117,250 100,252 91,241
  C87,232 88,223 93,217 Z"/>
 <path class="fm-sh" d="M207,217 C195,216 181,224 175,236 C183,250 200,252 209,241
  C213,232 212,223 207,217 Z"/>
 <!-- sulco nasolabial -->
 <path class="fm-ln" d="M138,223 C132,233 128,249 129,267"/>
 <path class="fm-ln" d="M162,223 C168,233 172,249 171,267"/>
 <!-- ramo e corpo da mandibula -->
 <path class="fm-ln2" d="M80,229 C84,264 97,297 123,323"/>
 <path class="fm-ln2" d="M220,229 C216,264 203,297 177,323"/>
 <!-- sulco pre-jowl -->
 <path class="fm-sh2" d="M110,299 C119,295 129,300 133,308 C127,318 113,318 108,310 Z"/>
 <path class="fm-sh2" d="M190,299 C181,295 171,300 167,308 C173,318 187,318 192,310 Z"/>
 <!-- sulco labiomentual -->
 <path class="fm-sh2" d="M133,282 C141,277 159,277 167,282 C160,290 140,290 133,282 Z"/>
 <!-- eminencia mentual -->
 <ellipse class="fm-hi" cx="150" cy="312" rx="17" ry="14"/>
 <!-- fronte: luz central e leve sombra lateral -->
 <ellipse class="fm-hi" cx="150" cy="128" rx="34" ry="20"/>
 <!-- filtro nasal -->
 <path class="fm-ln3" d="M145,232 C145,239 145,244 146,247"/>
 <path class="fm-ln3" d="M155,232 C155,239 155,244 154,247"/>
 <!-- dorso nasal: sombra de um lado, luz do outro -->
 <path class="fm-sh2" d="M143,180 C141,195 140,208 139,217 C143,219 145,218 146,216
  C146,204 146,191 147,180 Z"/>
 <ellipse class="fm-hi" cx="152" cy="215" rx="7" ry="5"/>
</g>
<g class="fc-blush"><ellipse cx="102" cy="212" rx="15" ry="9"/><ellipse cx="198" cy="212" rx="15" ry="9"/></g>
"""

FACE_TOP = """
<path class="fc-hairf" d="M87,152 C89,112 114,86 150,86 C188,86 216,109 221,152
 C213,129 197,114 177,110 C157,129 116,133 95,124 C91,132 88,141 87,152 Z"/>
<g class="fc-hairln">
 <path d="M96,126 C104,132 118,135 133,133"/>
 <path d="M176,111 C168,120 156,127 142,131"/>
 <path d="M209,132 C213,141 216,150 218,160"/>
 <path d="M84,140 C82,152 81,164 81,176"/>
</g>
<g class="fc-feat">
 <path class="fc-brow-f" d="M99,155 C106,144 121,138 134,141 C139,142 143,146 146,150
  C141,147 136,146 131,146 C120,146 107,150 100,158 Z"/>
 <path class="fc-brow-f" d="M201,155 C194,144 179,138 166,141 C161,142 157,146 154,150
  C159,147 164,146 169,146 C180,146 193,150 200,158 Z"/>
 <path class="fc-eye" d="M104,170 C110,158 126,154 134,161 C137,164 138,167 138,170
  C130,180 112,181 104,170 Z"/>
 <path class="fc-eye" d="M196,170 C190,158 174,154 166,161 C163,164 162,167 162,170
  C170,180 188,181 196,170 Z"/>
 <path class="fc-lid" d="M104,170 C110,158 126,154 134,161 C137,164 138,167 138,170"/>
 <path class="fc-lid" d="M196,170 C190,158 174,154 166,161 C163,164 162,167 162,170"/>
 <path class="fc-lidlo" d="M106,173 C113,180 128,180 137,172"/>
 <path class="fc-lidlo" d="M194,173 C187,180 172,180 163,172"/>
 <path class="fc-crease" d="M105,160 C113,150 131,148 139,157"/>
 <path class="fc-crease" d="M195,160 C187,150 169,148 161,157"/>
 <path class="fc-nose" d="M139,225 C133,221 134,212 141,210"/>
 <path class="fc-nose" d="M161,225 C167,221 166,212 159,210"/>
 <path class="fc-nose" d="M147,229 C148,232 152,232 153,229"/>
 <g class="fc-nostril"><ellipse cx="143.5" cy="225" rx="2.6" ry="1.7"/>
  <ellipse cx="156.5" cy="225" rx="2.6" ry="1.7"/></g>
 <path class="fc-lipup" d="M126,257 C133,247 143,245 150,251 C157,245 167,247 174,257
  C166,259 158,258 150,258 C142,258 134,259 126,257 Z"/>
 <path class="fc-liplo" d="M126,257 C134,258 142,259 150,259 C158,259 166,258 174,257
  C167,272 133,272 126,257 Z"/>
 <path class="fc-lipline" d="M126,257 C140,259 160,259 174,257"/>
 <ellipse class="fc-liphi" cx="150" cy="266" rx="9" ry="3"/>
</g>
<g class="fc-iris"><circle cx="120" cy="169" r="6.6"/><circle cx="180" cy="169" r="6.6"/></g>
<g class="fc-pupil">
 <circle cx="120" cy="169" r="2.8"/><circle cx="180" cy="169" r="2.8"/>
 <circle class="fc-glint" cx="122.4" cy="166.6" r="1.7"/><circle class="fc-glint" cx="182.4" cy="166.6" r="1.7"/>
</g>
<g class="fc-lash">
 <path d="M104,170 C105,174 106,177 107,179"/><path d="M110,176 C111,180 112,182 113,184"/>
 <path d="M196,170 C195,174 194,177 193,179"/><path d="M190,176 C189,180 188,182 187,184"/>
</g>
"""

FACE_ART = FACE_BASE + FACE_TOP
'''

# troca o bloco FACE_ART = """...""" inteiro
i0 = s.index('FACE_ART = """')
i1 = s.index('def face_svg(', i0)
s = s[:i0] + FACE_NEW.strip() + '\n\n' + s[i1:]

# o clip do relevo precisa existir no documento; injeta um defs global no face_svg/face_regioes
s = s.replace(
 'return (f\'<svg class="{cls}" viewBox="0 0 {vw} 400" role="img" aria-label="{aria}" \'\n'
 '            f\'style="max-width:{width}px">{g0}{FACE_ART}{g1}{m}</svg>\')',
 'return (f\'<svg class="{cls}" viewBox="0 0 {vw} 400" role="img" aria-label="{aria}" \'\n'
 '            f\'style="max-width:{width}px">{FACE_DEFS}{g0}{FACE_ART}{g1}{m}</svg>\')')

# ------------------------------------------------------- 2. REG com anatomia + pino
REG_NEW = '''
FACE_DEFS = ('<defs><clipPath id="fcFaceClip"><path d="' + FACE_CLIP + '"/></clipPath></defs>')

# (lado, path, pino_x, pino_y) — lado 'b' = bilateral (espelhada), 'c' = central
# o pino marca a regiao com o numero da legenda; nas bilaterais fica num lado so
REG = {
 'fronte':      ('c', 'M92,132 C95,105 120,97 150,97 C180,97 205,105 208,132 '
                      'C196,140 172,143 150,143 C128,143 104,140 92,132 Z', 150, 120),
 'temporal':    ('b', 'M97,124 C95,144 94,164 96,186 C86,191 78,184 75,170 '
                      'C72,154 74,137 80,124 Z', 85, 155),
 'supercilio':  ('b', 'M97,158 C108,144 129,138 145,147 L143,159 C130,151 110,155 '
                      '100,167 Z', 119, 150),
 'infraorb':    ('b', 'M103,181 C113,177 132,179 141,186 C135,199 112,202 104,193 Z',
                 121, 190),
 'zigoma':      ('b', 'M79,192 C93,185 113,190 128,202 C126,213 119,218 110,214 '
                      'C99,207 87,203 78,202 Z', 101, 202),
 'bochecha':    ('b', 'M90,219 C103,215 119,223 127,235 C121,251 101,255 91,243 '
                      'C87,234 87,225 90,219 Z', 107, 235),
 'auricular':   ('b', 'M79,203 C79,222 81,241 85,259 L63,266 C57,249 53,229 51,201 Z',
                 67, 232),
 'nariz':       ('c', 'M144,166 C147,161 153,161 156,166 C157,188 158,205 160,215 '
                      'C158,227 142,227 140,215 C142,205 143,188 144,166 Z', 150, 193),
 'nasolabial':  ('b', 'M134,219 C126,231 121,248 122,268 L133,269 C132,251 136,236 '
                      '143,226 Z', 127, 245),
 'labios':      ('c', 'M124,257 C133,245 144,243 150,249 C156,243 167,245 176,257 '
                      'C167,277 133,277 124,257 Z', 150, 262),
 'perioral':    ('c', 'M116,252 C126,238 141,240 150,244 C159,240 174,238 184,252 '
                      'C182,271 169,287 150,289 C131,287 118,271 116,252 Z'
                      'M124,257 C133,277 167,277 176,257 C167,245 156,243 150,249 '
                      'C144,243 133,245 124,257 Z', 122, 271),
 'labiomentual':('c', 'M131,280 C140,274 160,274 169,280 C161,292 139,292 131,280 Z',
                 150, 286),
 'mento':       ('c', 'M128,294 C139,289 161,289 172,294 C173,317 163,332 150,337 '
                      'C137,332 127,317 128,294 Z', 150, 316),
 'mandibula':   ('b', 'M78,227 C82,265 96,299 124,326 L115,349 C73,325 45,289 37,233 Z',
                 92, 291),
 'prejowl':     ('b', 'M107,297 C118,292 131,297 136,307 C129,321 112,321 104,311 Z',
                 118, 307),
}
'''
i0 = s.index('# lado esquerdo do observador')
i1 = s.index('GRUPOS_REG = [')
s = s[:i0] + '# lado esquerdo do observador; as bilaterais sao espelhadas por transform\n' \
   + REG_NEW.strip() + '\n\n' + s[i1:]

# --------------------------------------------- 3. face_regioes: pinos + camadas
FR_OLD_START = s.index("FACE_FEATS = FACE_ART[")
FR_OLD_END   = s.index("def mapa_regioes():")
FR_NEW = '''
def face_regioes(g, width=196, cls='facereg', pinos=True):
    """Face frontal com as regioes do grupo demarcadas e numeradas.

    A ordem de camadas importa: FACE_BASE (pele + relevo) recebe a cor da regiao,
    e FACE_TOP (cabelo da frente, olhos, boca) volta por cima — assim a mancha
    nunca cai sobre o cabelo nem apaga uma feicao.
    """
    uid = f'fr{g["n"]}{abs(hash(tuple(g["regs"]))) % 9973}'
    fill = CORREG[g['cores'][0]]
    stroke = CORREG[g['cores'][-1]] if len(g['cores']) > 1 else fill
    shapes, pins = '', ''
    for i, r in enumerate(g['regs'], 1):
        lado, d, px, py = REG[r]
        rule = ' fill-rule="evenodd"' if r == 'perioral' else ''
        nome = REG_NOME.get(r, r)
        shapes += f'<path d="{d}" class="rg"{rule}><title>{nome}</title></path>'
        if lado == 'b':
            shapes += (f'<g transform="translate(300,0) scale(-1,1)">'
                       f'<path d="{d}" class="rg"{rule}><title>{nome}</title></path></g>')
        if pinos:
            pins += (f'<g class="rgpin"><circle cx="{px}" cy="{py}" r="8.4"/>'
                     f'<text x="{px}" y="{py}" dy="3.1">{i}</text></g>')
    return (f'<svg class="{cls}" viewBox="0 0 300 400" role="img" '
            f'style="width:{width}px;--rg-f:{fill};--rg-s:{stroke}" '
            f'aria-label="regioes faciais do grupo {g["n"]}: {html.escape(g["txt"])}">'
            f'{FACE_DEFS}'
            f'<defs><clipPath id="{uid}"><path d="{FACE_CLIP}"/></clipPath></defs>'
            f'{FACE_BASE}<g clip-path="url(#{uid})">{shapes}</g>'
            f'<path d="{FACE_CLIP}" class="fc-edge"/>{FACE_TOP}{pins}</svg>')

def regs_numerados(regs):
    """Lista das regioes numerada na mesma ordem dos pinos da face."""
    return ''.join(f'<span class="rgli"><i>{i}</i>{REG_NOME.get(r, r)}</span>'
                   for i, r in enumerate(regs, 1))

'''
s = s[:FR_OLD_START] + FR_NEW.strip() + '\n\n' + s[FR_OLD_END:]

# nomes clinicos das regioes, para pino/legenda/tooltip
NOMES = '''
REG_NOME = {
 'fronte': 'fronte', 'temporal': 'tempora', 'supercilio': 'supercilio',
 'infraorb': 'regiao infraorbitaria', 'zigoma': 'arco zigomatico',
 'bochecha': 'bochecha', 'auricular': 'regiao auricular anterior',
 'nariz': 'nariz', 'nasolabial': 'sulco nasolabial', 'labios': 'labio',
 'perioral': 'regiao perioral', 'labiomentual': 'sulco labiomentual',
 'mento': 'mento', 'mandibula': 'mandibula', 'prejowl': 'pre-jowl',
}
'''
s = s.replace("GRUPOS_REG = [", NOMES.strip() + "\n\nGRUPOS_REG = [", 1)

SRC.write_text(s, encoding='utf-8')
print('patch v18 aplicado' if s != orig else 'nada mudou')
