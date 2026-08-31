# -*- coding: utf-8 -*-
"""Pranchas das regioes da cabeca e do pescoco — figura masculina.

Redesenho das pranchas de atlas anatomico (vistas anterior, lateral, dorsal e
inferior) em morfologia masculina: cranio mais quadrado, mandibula larga com
gonio marcado, arco supraorbital reto e baixo, dorso nasal reto, labio superior
longo, proeminencia laringea visivel, esternocleidomastoideo mais definido.

As figuras sao construidas a partir de um sistema de marcos proporcionais
(tercos faciais classicos, largura do olho = 1/5 da largura bizigomatica), nao
de curvas escritas a mao — assim os limites das regioes caem sobre a anatomia
em vez de flutuar sobre ela.
"""

# ============================================================ marcos e proporcoes
CX = 450.0                 # eixo de simetria

Y_VERT   =  92.0           # vertex
Y_TRIC   = 172.0           # limite frontal/parietal (cabeca raspada)
Y_BROW   = 262.0           # glabela / margem supraorbital
Y_OLHO   = 294.0           # linha das pupilas
Y_ZIG    = 306.0           # ponto mais largo (zigion)
Y_SUBN   = 374.0           # subnasal
Y_BOCA   = 424.0           # estomio
Y_SULCO  = 462.0           # sulco labiomentual
Y_GONIO  = 424.0           # angulo da mandibula
Y_MENTO  = 504.0           # menton

HW_ZIG   = 106.0           # semi-largura bizigomatica
HW_GONIO =  90.0           # semi-largura bigonial (masculina: larga)
HW_PAR   = 104.0           # semi-largura parietal
LARG_OLHO = 2 * HW_ZIG / 5  # ~42: largura do olho = 1/5 da face
HW_NARIZ = LARG_OLHO / 2    # asa do nariz = distancia intercantal
HW_BOCA  = LARG_OLHO * 0.75
X_OLHO   = CX - LARG_OLHO   # centro da orbita esquerda do observador
HW_PESC  =  64.0

# ------------------------------------------------------------------ utilitarios
def suave(pts, fechar=False, t=6.0):
    """Catmull-Rom -> bezier cubica. Curva passando por todos os pontos dados."""
    p = list(pts)
    if len(p) < 2:
        return ''
    if fechar:
        ext = [p[-1]] + p + [p[0], p[1]]
    else:
        ext = [p[0]] + p + [p[-1]]
    d = f'M{p[0][0]:.1f},{p[0][1]:.1f}'
    n = len(ext)
    for i in range(1, n - 2):
        p0, p1, p2, p3 = ext[i-1], ext[i], ext[i+1], ext[i+2]
        c1 = (p1[0] + (p2[0]-p0[0])/t, p1[1] + (p2[1]-p0[1])/t)
        c2 = (p2[0] - (p3[0]-p1[0])/t, p2[1] - (p3[1]-p1[1])/t)
        d += (f' C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} '
              f'{p2[0]:.1f},{p2[1]:.1f}')
    if fechar:
        d += ' Z'
    return d

def reta(pts, fechar=False):
    """Polilinha. Limites de ladrilhamento precisam ser retos: curva fechada
    sobre poucos vertices distantes estoura para fora do poligono."""
    d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    return d + ' Z' if fechar else d

def emenda(*ds):
    """Concatena paths trocando o M dos seguintes por L."""
    out = ds[0]
    for d in ds[1:]:
        out += ' L' + d[1:].lstrip()
    return out

def mx(pts):
    """Espelha uma lista de pontos em torno de CX."""
    return [(2*CX - x, y) for x, y in pts]

def simetrico(meia, t=6.0):
    """Contorno fechado a partir da metade esquerda (do vertex ao menton)."""
    return suave(meia + mx(meia[::-1])[1:-1], fechar=True, t=t)


# ==================================================== VISTA ANTERIOR — contorno
# metade esquerda do observador, do vertex ao menton
MEIA_CRANIO = [
 (CX,        Y_VERT),
 (CX -  34,   96),
 (CX -  62,  110),
 (CX -  84,  134),
 (CX -  97,  164),
 (CX - HW_PAR, 200),
 (CX - 105,  242),           # temporal: leve reentrancia
 (CX - HW_ZIG, Y_ZIG),       # zigion
 (CX - 103,  346),
 (CX -  97,  386),
 (CX - HW_GONIO, Y_GONIO),   # gonio
 (CX -  76,  456),
 (CX -  50,  486),
 (CX,        Y_MENTO),
]
CRANIO_A = simetrico(MEIA_CRANIO, t=6.2)

# pescoco e cintura escapular
PESCOCO_A = suave([
 (CX - HW_PESC + 6, 470), (CX - HW_PESC, 520), (CX - HW_PESC - 4, 572),
 (CX - 104, 606), (CX - 168, 636), (CX - 208, 664),
], t=6.0)
PESCOCO_A_D = suave(mx([
 (CX - HW_PESC + 6, 470), (CX - HW_PESC, 520), (CX - HW_PESC - 4, 572),
 (CX - 104, 606), (CX - 168, 636), (CX - 208, 664),
]), t=6.0)
_BUSTO_MEIA = [(CX - 58, 470), (CX - HW_PESC, 516), (CX - HW_PESC - 4, 566),
               (CX - 100, 602), (CX - 164, 634), (CX - 206, 664), (CX - 210, 674)]
BUSTO_A = emenda(suave(_BUSTO_MEIA, t=6.5),
                 f'M{CX+210:.0f},674',
                 suave(mx(_BUSTO_MEIA)[::-1], t=6.5)[1:] if False else
                 suave(mx(_BUSTO_MEIA[::-1]), t=6.5)) + ' Z'

# ---- orelha: entre a linha supraorbital e o subnasal, encostada no cranio
def orelha(lado=-1):
    """Pavilhao entre a linha supraorbital e o subnasal, nascendo na borda do cranio."""
    s = lado
    contorno = [(CX + s*102, Y_BROW + 8), (CX + s*112, 284), (CX + s*116, 310),
                (CX + s*113, 338), (CX + s*106, 358), (CX + s*100, Y_SUBN - 8)]
    helice   = [(CX + s*104, 288), (CX + s*109, 308), (CX + s*107, 330),
                (CX + s*102, 346)]
    tragus   = [(CX + s*100, 314), (CX + s*104, 320), (CX + s*101, 328)]
    return suave(contorno, t=5.0), suave(helice, t=5.0), suave(tragus, t=5.0)

# ---- feicoes (metade esquerda; espelhadas na montagem)
SOBRANC = suave([
 (X_OLHO - 26, Y_BROW + 14), (X_OLHO - 8, Y_BROW - 2), (X_OLHO + 14, Y_BROW - 6),
 (X_OLHO + 30, Y_BROW + 1), (X_OLHO + 28, Y_BROW + 8), (X_OLHO + 12, Y_BROW + 4),
 (X_OLHO - 8, Y_BROW + 7), (X_OLHO - 24, Y_BROW + 20),
], fechar=True, t=5.0)

OLHO = suave([
 (X_OLHO - 21, Y_OLHO + 1), (X_OLHO - 8, Y_OLHO - 9), (X_OLHO + 8, Y_OLHO - 10),
 (X_OLHO + 21, Y_OLHO - 1), (X_OLHO + 8, Y_OLHO + 10), (X_OLHO - 8, Y_OLHO + 9),
], fechar=True, t=5.0)
PALP_SUP = suave([(X_OLHO - 21, Y_OLHO + 1), (X_OLHO - 8, Y_OLHO - 9),
                  (X_OLHO + 8, Y_OLHO - 10), (X_OLHO + 21, Y_OLHO - 1)], t=5.0)
SULCO_PALP = suave([(X_OLHO - 19, Y_OLHO - 10), (X_OLHO - 4, Y_OLHO - 19),
                    (X_OLHO + 14, Y_OLHO - 18), (X_OLHO + 22, Y_OLHO - 10)], t=5.0)

# nariz: dorso reto e alto (masculino), sombra de um lado so
NARIZ_SOMBRA = suave([
 (CX - 20, Y_SUBN - 6), (CX - 16, Y_SUBN - 20), (CX - 6, Y_SUBN - 26),
 (CX + 6, Y_SUBN - 26), (CX + 16, Y_SUBN - 20), (CX + 20, Y_SUBN - 6),
 (CX + 10, Y_SUBN - 2), (CX, Y_SUBN - 1), (CX - 10, Y_SUBN - 2),
], fechar=True, t=5.5)
NARIZ_ASA = suave([(CX - HW_NARIZ + 3, Y_SUBN + 2), (CX - HW_NARIZ - 3, Y_SUBN - 8),
                   (CX - HW_NARIZ + 2, Y_SUBN - 18), (CX - 12, Y_SUBN - 20)], t=5.0)
NARIZ_NARINA = suave([(CX - 16, Y_SUBN + 3), (CX - 11, Y_SUBN + 6),
                      (CX - 5, Y_SUBN + 5)], t=5.0)
NARIZ_PONTA = suave([(CX - 14, Y_SUBN - 8), (CX - 6, Y_SUBN - 14), (CX, Y_SUBN - 15),
                     (CX + 6, Y_SUBN - 14), (CX + 14, Y_SUBN - 8)], t=5.0)
FILTRO = suave([(CX - 6, Y_SUBN + 8), (CX - 6, Y_BOCA - 14), (CX - 5, Y_BOCA - 8)], t=6.0)

# boca: labio superior longo, labios finos (masculino)
LABIO_SUP = suave([
 (CX - HW_BOCA, Y_BOCA), (CX - 20, Y_BOCA - 9), (CX - 8, Y_BOCA - 12),
 (CX, Y_BOCA - 9), (CX + 8, Y_BOCA - 12), (CX + 20, Y_BOCA - 9),
 (CX + HW_BOCA, Y_BOCA), (CX + 14, Y_BOCA + 3), (CX, Y_BOCA + 3),
 (CX - 14, Y_BOCA + 3),
], fechar=True, t=5.5)
LABIO_INF = suave([
 (CX - HW_BOCA, Y_BOCA), (CX - 14, Y_BOCA + 3), (CX, Y_BOCA + 3),
 (CX + 14, Y_BOCA + 3), (CX + HW_BOCA, Y_BOCA),
 (CX + 16, Y_BOCA + 18), (CX, Y_BOCA + 20), (CX - 16, Y_BOCA + 18),
], fechar=True, t=5.5)
COMISSURA = suave([(CX - HW_BOCA - 2, Y_BOCA + 1), (CX - HW_BOCA + 6, Y_BOCA + 2)], t=6.0)

# proeminencia laringea (masculina)
LARINGE = suave([(CX - 11, 552), (CX, 544), (CX + 11, 552)], t=5.0)


# ---- espelhos das feicoes (recalculados dos pontos, nao do path)
def _pts_sobranc(s=-1):
    o = CX + s*LARG_OLHO
    return [(o - s*26, Y_BROW + 14), (o - s*8, Y_BROW - 2), (o + s*14, Y_BROW - 6),
            (o + s*30, Y_BROW + 1), (o + s*28, Y_BROW + 8), (o + s*12, Y_BROW + 4),
            (o - s*8, Y_BROW + 7), (o - s*24, Y_BROW + 20)]
def _pts_olho(s=-1):
    o = CX + s*LARG_OLHO
    return [(o - s*21, Y_OLHO + 1), (o - s*8, Y_OLHO - 9), (o + s*8, Y_OLHO - 10),
            (o + s*21, Y_OLHO - 1), (o + s*8, Y_OLHO + 10), (o - s*8, Y_OLHO + 9)]
def _pts_palp(s=-1):
    o = CX + s*LARG_OLHO
    return [(o - s*21, Y_OLHO + 1), (o - s*8, Y_OLHO - 9),
            (o + s*8, Y_OLHO - 10), (o + s*21, Y_OLHO - 1)]
def _pts_sulcop(s=-1):
    o = CX + s*LARG_OLHO
    return [(o - s*19, Y_OLHO - 10), (o - s*4, Y_OLHO - 19),
            (o + s*14, Y_OLHO - 18), (o + s*22, Y_OLHO - 10)]

SOBRANC     = suave(_pts_sobranc(-1), fechar=True, t=5.0)
SOBRANC_D   = suave(_pts_sobranc(+1), fechar=True, t=5.0)
OLHO        = suave(_pts_olho(-1), fechar=True, t=5.0)
OLHO_D      = suave(_pts_olho(+1), fechar=True, t=5.0)
PALP_SUP    = suave(_pts_palp(-1), t=5.0)
PALP_SUP_D  = suave(_pts_palp(+1), t=5.0)
SULCO_PALP  = suave(_pts_sulcop(-1), t=5.0)
SULCO_PALP_D= suave(_pts_sulcop(+1), t=5.0)

_asa  = [(CX - HW_NARIZ + 3, Y_SUBN + 2), (CX - HW_NARIZ - 3, Y_SUBN - 8),
         (CX - HW_NARIZ + 2, Y_SUBN - 18), (CX - 12, Y_SUBN - 20)]
_nari = [(CX - 16, Y_SUBN + 3), (CX - 11, Y_SUBN + 6), (CX - 5, Y_SUBN + 5)]
_filt = [(CX - 6, Y_SUBN + 12), (CX - 6, Y_BOCA - 16), (CX - 5, Y_BOCA - 11)]
_com  = [(CX - HW_BOCA - 2, Y_BOCA + 1), (CX - HW_BOCA + 6, Y_BOCA + 2)]
NARIZ_ASA      = suave(_asa, t=5.0);   NARIZ_ASA_D      = suave(mx(_asa), t=5.0)
NARIZ_NARINA   = suave(_nari, t=5.0);  NARIZ_NARINA_D   = suave(mx(_nari), t=5.0)
FILTRO         = suave(_filt, t=6.0);  FILTRO_D         = suave(mx(_filt), t=6.0)
COMISSURA      = suave(_com, t=6.0);   COMISSURA_D      = suave(mx(_com), t=6.0)

# ============================== VISTA ANTERIOR — limites das regioes
# tipo: 'c' central (nao espelha) · 'b' bilateral (espelha)
# ancora do rotulo e o lado da coluna
# vertices compartilhados entre regioes vizinhas — garantem ladrilhamento sem cruzar
P_ARCO   = (CX - 100, 302)   # arco zigomatico, a frente da orelha
P_RIMLAT = (CX -  64, 316)   # rebordo orbital lateral
P_MED    = (CX -  26, 300)   # borda medial, junto ao nariz
P_MEDINF = (CX -  30, 354)   # limite inferior medial da infraorbital
P_TRI    = (CX -  78, 358)   # trifurcacao zigomatica / infraorbital / bucal
P_BORDA  = (CX -  98, 356)   # borda do cranio, sob o arco
P_MAND   = (CX -  82, 432)   # sobre o corpo da mandibula
P_COMIS  = (CX -  52, 446)   # lateral a regiao oral (comissura)
P_ANG    = (CX -  70, 470)   # angulo da mandibula

REGIOES_A = [
 ('Região parietal', 'c', 'linha:suave',
  [(CX - 103, 202), (CX - 78, 176), (CX - 40, 164), (CX, 162),
   (CX + 40, 164), (CX + 78, 176), (CX + 103, 202)],
  (CX, 130), 'R'),

 ('Região frontal', 'b', 'linha:suave',
  [(CX - 100, 196), (CX - 95, 226), (CX - 94, 250), (CX - 96, Y_BROW + 6)],
  (CX - 46, 218), 'L'),

 ('Região temporal', 'b', 'linha:reta',
  [(CX - 104, Y_BROW), (CX - 100, 282), P_ARCO],
  (CX - 100, 244), 'R'),

 ('Região auricular', 'b', 'nada', [], (CX - 118, 316), 'L'),

 ('Região orbital', 'b', 'fechado:suave',
  [P_MED, (X_OLHO + 6, Y_BROW - 4), (X_OLHO - 24, Y_BROW + 8), P_RIMLAT,
   (CX - 58, Y_OLHO + 24), (X_OLHO - 10, Y_OLHO + 28), (X_OLHO + 18, Y_OLHO + 22)],
  (X_OLHO, Y_OLHO), 'L'),

 ('Região nasal', 'c', 'fechado:suave',
  [(CX, Y_BROW + 2), (CX - 22, Y_BROW + 12), (CX - 21, 322),
   (CX - HW_NARIZ - 5, 358), (CX - HW_NARIZ - 7, Y_SUBN + 6),
   (CX, Y_SUBN + 14), (CX + HW_NARIZ + 7, Y_SUBN + 6),
   (CX + HW_NARIZ + 5, 358), (CX + 23, 322), (CX + 22, Y_BROW + 12)],
  (CX, 338), 'R'),

 ('Região infraorbital', 'b', 'fechado:reta',
  [P_MED, (X_OLHO + 18, Y_OLHO + 22), (X_OLHO - 10, Y_OLHO + 28),
   (CX - 58, Y_OLHO + 24), P_RIMLAT, P_TRI, P_MEDINF],
  (CX - 50, 338), 'L'),

 ('Região zigomática', 'b', 'fechado:reta',
  [P_ARCO, P_RIMLAT, P_TRI, P_BORDA],
  (CX - 86, 332), 'R'),

 ('Região infratemporal', 'b', 'fechado:reta',
  [(CX - 104, 292), P_ARCO, P_BORDA, (CX - 103, 340)],
  (CX - 101, 318), 'R'),

 ('Região oral', 'c', 'fechado:suave',
  [(CX, Y_SUBN + 14), (CX - HW_NARIZ - 6, Y_SUBN + 8), (CX - 42, 400),
   P_COMIS, (CX - 34, Y_SULCO), (CX, Y_SULCO + 4),
   (CX + 34, Y_SULCO), (2*CX - P_COMIS[0], P_COMIS[1]),
   (CX + 42, 400), (CX + HW_NARIZ + 6, Y_SUBN + 8)],
  (CX, Y_BOCA + 28), 'R'),

 ('Região bucal', 'b', 'fechado:reta',
  [P_MEDINF, P_TRI, P_MAND, P_COMIS, (CX - 42, 400)],
  (CX - 62, 398), 'L'),

 ('Região parotideomassetérica', 'b', 'fechado:reta',
  [P_BORDA, P_TRI, P_MAND, P_ANG, (CX - 92, 448), (CX - 100, 404)],
  (CX - 90, 416), 'R'),

 ('Região mentual', 'c', 'fechado:suave',
  [(CX, Y_SULCO + 4), (CX - 30, Y_SULCO + 2), (CX - 38, 482),
   (CX, Y_MENTO - 2), (CX + 38, 482), (CX + 30, Y_SULCO + 2)],
  (CX, 486), 'R'),
]

REGIOES_PESC_A = [
 ('Região esternocleidomastóidea', 'b', 'linha',
  [(CX - 96, 490), (CX - 82, 528), (CX - 62, 570), (CX - 42, 618)],
  (CX - 62, 552), 'L'),
 ('Trígono muscular', 'b', 'linha',
  [(CX - 68, 486), (CX - 52, 528), (CX - 32, 572), (CX - 14, 622)],
  (CX - 20, 596), 'R'),
 ('Região cervical lateral', 'b', 'linha',
  [(CX - 100, 512), (CX - 108, 560), (CX - 122, 600), (CX - 146, 628)],
  (CX - 84, 592), 'R'),
 ('Região cervical posterior', 'b', 'nada', [], (CX - 150, 632), 'L'),
]


# ================================================================ montagem SVG
COL_L, COL_R, W_PR, H_PR = 254, 646, 900, 700

def _rotulo(nome, ax, ay, lado, ly):
    if lado == 'L':
        d, tx, an = f'M{ax:.0f},{ay:.0f} L{COL_L:.0f},{ay:.0f} L{COL_L-10:.0f},{ly:.0f}', COL_L - 16, 'end'
    else:
        d, tx, an = f'M{ax:.0f},{ay:.0f} L{COL_R:.0f},{ay:.0f} L{COL_R+10:.0f},{ly:.0f}', COL_R + 16, 'start'
    return (f'<path class="ld" d="{d}"/>'
            f'<circle class="an" cx="{ax:.0f}" cy="{ay:.0f}" r="2.4"/>'
            f'<text class="lb" x="{tx}" y="{ly:.0f}" text-anchor="{an}">{nome}</text>')

def _distribui(itens, topo=118, passo=30, fundo=676):
    """itens: (nome, ax, ay, lado). Empilha por coluna sem sobreposicao."""
    out = []
    for lado in 'LR':
        col = sorted([i for i in itens if i[3] == lado], key=lambda i: i[2])
        y = topo
        linhas = []
        for nome, ax, ay, _ in col:
            ly = max(ay, y)
            linhas.append([nome, ax, ay, lado, ly])
            y = ly + passo
        sobra = (linhas[-1][4] if linhas else 0) - fundo
        if sobra > 0:
            for l in linhas:
                l[4] -= sobra
        out += linhas
    return out

def _limites(regs):
    """Desenha os limites; devolve tambem as ancoras para os rotulos."""
    corpo, anc = '', []
    for nome, tipo, forma, pts, (ax, ay), lado in regs:
        if forma != 'nada':
            base, _, modo = forma.partition(':')
            fechar = base == 'fechado'
            traco = reta if modo == 'reta' else suave
            cls = 'rg' if fechar else 'rgl'
            corpo += f'<path class="{cls}" d="{traco(pts, fechar)}"/>'
            if tipo == 'b':
                corpo += f'<path class="{cls}" d="{traco(mx(pts), fechar)}"/>'
        anc.append((nome, ax, ay, lado))
    return corpo, anc

def plate_anterior():
    o_e, he_e, tr_e = orelha(-1)
    o_d, he_d, tr_d = orelha(+1)

    pele = (f'<path class="pl" d="{BUSTO_A}"/>'
            f'<path class="orelha" d="{o_e}"/><path class="orelha" d="{o_d}"/>'
            f'<path class="pl" d="{CRANIO_A}"/>')
    det = (f'<path class="ln2" d="{he_e}"/><path class="ln2" d="{he_d}"/>'
           f'<path class="ln3" d="{tr_e}"/><path class="ln3" d="{tr_d}"/>'
           f'<path class="ln2" d="{LARINGE}"/>')

    feic = ''
    feic += f'<path class="brow" d="{SOBRANC}"/><path class="brow" d="{SOBRANC_D}"/>'
    feic += f'<path class="olho" d="{OLHO}"/><path class="olho" d="{OLHO_D}"/>'
    feic += f'<path class="lid" d="{PALP_SUP}"/><path class="lid" d="{PALP_SUP_D}"/>'
    feic += f'<path class="ln3" d="{SULCO_PALP}"/><path class="ln3" d="{SULCO_PALP_D}"/>'
    feic += f'<circle class="iris" cx="{X_OLHO:.0f}" cy="{Y_OLHO:.0f}" r="8.4"/>'
    feic += f'<circle class="iris" cx="{2*CX-X_OLHO:.0f}" cy="{Y_OLHO:.0f}" r="8.4"/>'
    feic += f'<circle class="pup" cx="{X_OLHO:.0f}" cy="{Y_OLHO:.0f}" r="3.6"/>'
    feic += f'<circle class="pup" cx="{2*CX-X_OLHO:.0f}" cy="{Y_OLHO:.0f}" r="3.6"/>'
    feic += f'<path class="sh" d="{NARIZ_SOMBRA}"/>'
    feic += f'<path class="ln2" d="{NARIZ_ASA}"/><path class="ln2" d="{NARIZ_ASA_D}"/>'
    feic += f'<path class="ln2" d="{NARIZ_NARINA}"/><path class="ln2" d="{NARIZ_NARINA_D}"/>'
    feic += f'<path class="ln3" d="{NARIZ_PONTA}"/>'
    feic += f'<path class="ln3" d="{FILTRO}"/><path class="ln3" d="{FILTRO_D}"/>'
    feic += f'<path class="lipup" d="{LABIO_SUP}"/><path class="liplo" d="{LABIO_INF}"/>'
    feic += f'<path class="ln2" d="{COMISSURA}"/><path class="ln2" d="{COMISSURA_D}"/>'

    lim, anc = _limites(REGIOES_A + REGIOES_PESC_A)
    rot = ''.join(_rotulo(*r) for r in _distribui(anc))

    return (f'<svg viewBox="0 0 {W_PR} {H_PR}" role="img" class="prancha" '
            f'aria-label="Regiões da cabeça e do pescoço em vista anterior, figura '
            f'masculina: os limites de cada região traçados sobre a anatomia e '
            f'nomeados por linha de chamada">{pele}{det}{feic}{lim}{rot}</svg>')
