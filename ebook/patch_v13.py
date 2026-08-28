# -*- coding: utf-8 -*-
"""v13 — face humanizada: mesmos marcos anatômicos (para as regiões seguirem
válidas), traço muito mais humano — olhos amendoados com íris e cílios, lábios
com arco do cupido, nariz suave, cabelo que emoldura, pescoço e ombros, e
sombreado macio para dar dimensão."""
P = 'build_ebook.py'
src = open(P, encoding='utf-8').read()

NOVA_ART = '''FACE_ART = """
<defs>
 <radialGradient id="fcSkin" cx="50%" cy="34%" r="76%">
  <stop offset="0%" stop-color="var(--face-hi)"/>
  <stop offset="62%" stop-color="var(--face-fill)"/>
  <stop offset="100%" stop-color="var(--face-sh)"/>
 </radialGradient>
 <linearGradient id="fcHair" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="var(--hair-2)"/>
  <stop offset="100%" stop-color="var(--hair-1)"/>
 </linearGradient>
</defs>
<g class="fc-body">
 <path class="fc-neck" d="M121,320 C122,344 119,357 113,367 C95,374 76,381 63,391
  C58,395 55,398 54,400 L246,400 C245,398 242,395 237,391 C224,381 205,374 187,367
  C181,357 178,344 179,320 Z"/>
 <path class="fc-sh" d="M150,368 C138,368 127,366 118,362 C112,372 108,386 106,400
  L194,400 C192,386 188,372 182,362 C173,366 162,368 150,368 Z"/>
</g>
<path class="fc-hairb" d="M150,64 C206,64 243,101 245,159 C246,192 243,227 236,258
 C233,271 229,281 225,289 L212,280 C221,249 226,214 224,180 C220,135 196,104 150,104
 C104,104 80,135 76,180 C74,214 79,249 88,280 L75,289 C71,281 67,271 64,258
 C57,227 54,192 55,159 C57,101 94,64 150,64 Z"/>
<path class="fc-face" d="M150,344 C176,342 197,327 211,305 C223,287 230,261 232,229
 C234,198 233,169 229,145 C225,119 208,101 186,93 C174,89 162,87 150,87
 C138,87 126,89 114,93 C92,101 75,119 71,145 C67,169 66,198 68,229
 C70,261 77,287 89,305 C103,327 124,342 150,344 Z"/>
<path class="fc-hairf" d="M150,86 C190,86 217,109 222,150 C216,129 200,114 179,108
 C167,121 137,126 118,116 C104,124 95,136 90,152 C92,112 114,86 150,86 Z"/>
<g class="fc-blush"><ellipse cx="99" cy="207" rx="17" ry="11"/><ellipse cx="201" cy="207" rx="17" ry="11"/></g>
<g class="fc-feat">
 <path class="fc-brow" d="M99,153 C110,143 130,141 142,149"/>
 <path class="fc-brow" d="M158,149 C170,141 190,143 201,153"/>
 <path class="fc-lid" d="M102,170 C110,159 129,157 138,169"/>
 <path class="fc-lid" d="M162,169 C171,157 190,159 198,170"/>
 <path class="fc-eye" d="M102,170 C110,159 129,157 138,169 C130,179 111,180 102,170 Z"/>
 <path class="fc-eye" d="M162,169 C171,157 190,159 198,170 C189,180 170,181 162,170 Z"/>
 <path class="fc-crease" d="M104,162 C112,154 128,152 137,160"/>
 <path class="fc-crease" d="M163,160 C172,152 188,154 196,162"/>
 <path class="fc-nose" d="M151,180 C150,196 148,208 146,217"/>
 <path class="fc-nose" d="M138,223 C143,228 157,228 162,223"/>
 <path class="fc-nose" d="M138,223 C133,219 135,213 139,212"/>
 <path class="fc-nose" d="M162,223 C167,219 165,213 161,212"/>
 <path class="fc-lipline" d="M129,258 C137,249 145,247 150,252 C155,247 163,249 171,258"/>
 <path class="fc-lip" d="M129,258 C137,249 145,247 150,252 C155,247 163,249 171,258
  C162,274 138,274 129,258 Z"/>
 <path class="fc-chin" d="M142,300 C146,303 154,303 158,300"/>
</g>
<g class="fc-iris">
 <circle cx="120" cy="169" r="5.6"/><circle cx="180" cy="169" r="5.6"/>
</g>
<g class="fc-pupil">
 <circle cx="120" cy="169" r="2.4"/><circle cx="180" cy="169" r="2.4"/>
 <circle class="fc-glint" cx="122" cy="167" r="1.5"/><circle class="fc-glint" cx="182" cy="167" r="1.5"/>
</g>
<g class="fc-lash">
 <path d="M102,170 C104,174 105,176 106,178"/><path d="M108,175 C109,179 110,181 111,183"/>
 <path d="M198,170 C196,174 195,176 194,178"/><path d="M192,175 C191,179 190,181 189,183"/>
</g>
"""
'''
i = src.index('FACE_ART = """')
j = src.index('"""', src.index('"""', i) + 3) + 3
src = src[:i] + NOVA_ART.strip() + src[j:]

NOVO_CSS = '''.fc-face{{fill:url(#fcSkin);stroke:var(--face-line);stroke-width:1.6;stroke-linejoin:round}}
.fc-neck{{fill:var(--face-sh);stroke:var(--face-line);stroke-width:1.3;opacity:.92}}
.fc-sh{{fill:var(--face-fill);stroke:var(--face-line);stroke-width:1.2;opacity:.75}}
.fc-hairb{{fill:url(#fcHair);stroke:var(--hair-line);stroke-width:1.3;stroke-linejoin:round}}
.fc-hairf{{fill:url(#fcHair);stroke:var(--hair-line);stroke-width:1.2;stroke-linejoin:round}}
.fc-blush ellipse{{fill:var(--blush);opacity:.5}}
.fc-feat path{{fill:none;stroke:var(--face-line);stroke-width:1.35;stroke-linecap:round;stroke-linejoin:round}}
.fc-eye{{fill:var(--eye-white);stroke:var(--face-line);stroke-width:1.35}}
.fc-lid{{stroke:var(--lash);stroke-width:2.1}}
.fc-brow{{stroke:var(--hair-1);stroke-width:3.4;stroke-linecap:round}}
.fc-crease{{stroke:var(--face-line);stroke-width:.9;opacity:.55}}
.fc-nose{{stroke-width:1.2;opacity:.8}}
.fc-lip{{fill:var(--lip);stroke:var(--lip-line);stroke-width:1.1}}
.fc-lipline{{stroke:var(--lip-line);stroke-width:1.2}}
.fc-chin{{stroke-width:1;opacity:.5}}
.fc-iris circle{{fill:var(--iris)}}
.fc-pupil circle{{fill:var(--pupil)}}
.fc-glint{{fill:#fff;opacity:.9}}
.fc-lash path{{fill:none;stroke:var(--lash);stroke-width:1.5;stroke-linecap:round}}
.fc-dot{{stroke:var(--card);stroke-width:2.2}}
.fc-halo{{opacity:.17}}
.fc-ld{{stroke:var(--ink3);stroke-width:1;stroke-dasharray:2 3}}
.fc-lb{{fill:var(--ink2);font:600 11.5px 'Barlow',sans-serif;letter-spacing:.02em}}
.capa-face .fc-face{{fill:rgba(255,255,255,.07);stroke:rgba(255,255,255,.66)}}
.capa-face .fc-hairb,.capa-face .fc-hairf{{fill:rgba(255,255,255,.12);stroke:rgba(255,255,255,.5)}}
.capa-face .fc-neck,.capa-face .fc-sh{{fill:rgba(255,255,255,.05);stroke:rgba(255,255,255,.4)}}
.capa-face .fc-feat path{{stroke:rgba(255,255,255,.62)}}
.capa-face .fc-eye{{fill:rgba(255,255,255,.22)}}
.capa-face .fc-lip{{fill:rgba(255,255,255,.18);stroke:rgba(255,255,255,.55)}}
.capa-face .fc-blush ellipse{{opacity:.18}}
.capa-face .fc-iris circle{{fill:rgba(255,255,255,.55)}}
.capa-face .fc-pupil circle{{fill:rgba(10,53,87,.8)}}
.capa-face .fc-brow{{stroke:rgba(255,255,255,.55)}}
.capa-face .fc-dot{{stroke:rgba(10,53,87,.9)}}'''

k = src.index('.fc-face{{fill:var(--face-fill)')
m = src.index('.capa-face .fc-dot{{stroke:rgba(10,53,87,.9)}}')
src = src[:k] + NOVO_CSS + src[m + len('.capa-face .fc-dot{{stroke:rgba(10,53,87,.9)}}'):]

# tokens de pele, cabelo, lábio e olho — claro e escuro
src = src.replace(' --face-line:#5A6C7A; --face-fill:#FFFCF7;',
 ' --face-line:#7C6A61; --face-fill:#FBEDE2; --face-hi:#FFF8F1; --face-sh:#F0DACA;'
 ' --hair-1:#4A3428; --hair-2:#6B4A37; --hair-line:#3A281E; --blush:#E9B6A4;'
 ' --lip:#D89A94; --lip-line:#B4726C; --eye-white:#FFFDFB; --iris:#7B5B43;'
 ' --pupil:#2B1D14; --lash:#3A281E;', 1)
src = src.replace(' --face-line:#8CA3B5; --face-fill:rgba(255,255,255,.04);',
 ' --face-line:#A08C80; --face-fill:#E6CDBB; --face-hi:#F2DECF; --face-sh:#D2B29B;'
 ' --hair-1:#3A281E; --hair-2:#573D2C; --hair-line:#2A1C14; --blush:#D99A86;'
 ' --lip:#C8867F; --lip-line:#9E5F59; --eye-white:#FBF6F1; --iris:#8A6A50;'
 ' --pupil:#221610; --lash:#2A1C14;')

open(P, 'w', encoding='utf-8').write(src)
print('v13: face humanizada')
