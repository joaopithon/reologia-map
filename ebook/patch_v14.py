# -*- coding: utf-8 -*-
"""v14 — refino da face: oval mais delicado e alongado, olhos maiores e bem
espaçados (uma largura de olho entre eles), franja em mecha lateral no lugar
do pico, nariz definido com asas, boca mais cheia."""
P = 'build_ebook.py'
src = open(P, encoding='utf-8').read()

OVAL = ("M150,344 C174,341 193,326 205,305 C216,287 223,262 225,231 "
        "C227,201 226,171 222,147 C218,120 202,102 181,94 C171,90 161,88 150,88 "
        "C139,88 129,90 119,94 C98,102 82,120 78,147 C74,171 73,201 75,231 "
        "C77,262 84,287 95,305 C107,326 126,341 150,344 Z")

NOVA_ART = '''FACE_ART = """
<defs>
 <radialGradient id="fcSkin" cx="50%" cy="32%" r="78%">
  <stop offset="0%" stop-color="var(--face-hi)"/>
  <stop offset="60%" stop-color="var(--face-fill)"/>
  <stop offset="100%" stop-color="var(--face-sh)"/>
 </radialGradient>
 <linearGradient id="fcHair" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="var(--hair-2)"/>
  <stop offset="100%" stop-color="var(--hair-1)"/>
 </linearGradient>
</defs>
<g class="fc-body">
 <path class="fc-neck" d="M124,322 C125,345 122,357 116,367 C99,374 80,381 67,391
  C62,395 59,398 58,400 L242,400 C241,398 238,395 233,391 C220,381 201,374 184,367
  C178,357 175,345 176,322 Z"/>
 <path class="fc-sh" d="M150,369 C139,369 129,367 121,363 C115,373 111,386 109,400
  L191,400 C189,386 185,373 179,363 C171,367 161,369 150,369 Z"/>
</g>
<path class="fc-hairb" d="M150,60 C205,60 241,97 243,157 C244,192 241,228 234,260
 C231,273 227,284 222,293 L208,284 C217,252 222,215 220,178 C216,130 194,100 150,100
 C106,100 84,130 80,178 C78,215 83,252 92,284 L78,293 C73,284 69,273 66,260
 C59,228 56,192 57,157 C59,97 95,60 150,60 Z"/>
<path class="fc-face" d="OVALPATH"/>
<path class="fc-hairf" d="M87,152 C89,112 114,86 150,86 C188,86 216,109 221,152
 C213,129 197,114 177,110 C157,129 116,133 95,124 C91,132 88,141 87,152 Z"/>
<g class="fc-blush"><ellipse cx="102" cy="209" rx="15" ry="9"/><ellipse cx="198" cy="209" rx="15" ry="9"/></g>
<g class="fc-feat">
 <path class="fc-brow" d="M101,152 C112,141 132,139 143,148"/>
 <path class="fc-brow" d="M157,148 C168,139 188,141 199,152"/>
 <path class="fc-eye" d="M104,170 C112,157 130,155 136,171 C129,181 112,182 104,170 Z"/>
 <path class="fc-eye" d="M164,171 C170,155 188,157 196,170 C188,182 171,181 164,171 Z"/>
 <path class="fc-lid" d="M104,170 C112,157 130,155 136,171"/>
 <path class="fc-lid" d="M164,171 C170,155 188,157 196,170"/>
 <path class="fc-crease" d="M105,161 C113,151 131,149 139,158"/>
 <path class="fc-crease" d="M161,158 C169,149 187,151 195,161"/>
 <path class="fc-nose" d="M151,180 C150,196 148,208 147,216"/>
 <path class="fc-nose" d="M139,224 C144,230 156,230 161,224"/>
 <path class="fc-nose" d="M139,224 C133,220 134,212 140,210"/>
 <path class="fc-nose" d="M161,224 C167,220 166,212 160,210"/>
 <path class="fc-lip" d="M125,257 C134,246 144,244 150,250 C156,244 166,246 175,257
  C165,276 135,276 125,257 Z"/>
 <path class="fc-lipline" d="M125,257 C134,246 144,244 150,250 C156,244 166,246 175,257"/>
 <path class="fc-chin" d="M142,300 C146,303 154,303 158,300"/>
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
'''.replace('OVALPATH', OVAL)

i = src.index('FACE_ART = """')
j = src.index('"""', src.index('"""', i) + 3) + 3
src = src[:i] + NOVA_ART.strip() + src[j:]

# o recorte das regiões precisa acompanhar o novo oval
i = src.index('FACE_CLIP = (')
j = src.index(')\n', i) + 2
src = src[:i] + f'FACE_CLIP = ("{OVAL}")\n' + src[j:]

open(P, 'w', encoding='utf-8').write(src)
print('v14: oval refinado, olhos maiores, franja lateral')
