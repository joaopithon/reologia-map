# -*- coding: utf-8 -*-
"""v15 — reestruturação conceitual: TRÊS FAMÍLIAS como ponto principal
(baixo G′ azul · moderado G′ amarelo · alto G′ roxo), com as subclasses
subordinadas. As duas assinaturas do baixo G′ atendem as MESMAS regiões;
o alto G′ tem três usos — projeção, volumização e a olheira."""
P = 'build_ebook.py'
src = open(P, encoding='utf-8').read()

# perioral mais justo aos lábios novos
old_per = ("'M116,252 C124,236 140,242 150,245 C160,242 176,236 184,252 '\n"
           "                      'C182,274 168,288 150,290 C132,288 118,274 116,252 Z'\n"
           "                      'M129,258 C138,275 162,275 171,258 C163,249 155,247 150,252 '\n"
           "                      'C145,247 137,249 129,258 Z'")
assert old_per in src, 'perioral'
src = src.replace(old_per,
 "'M117,252 C126,239 141,241 150,245 C159,241 174,239 183,252 '\n"
 "                      'C181,270 169,285 150,287 C131,285 119,270 117,252 Z'\n"
 "                      'M125,257 C135,276 165,276 175,257 C166,246 156,244 150,250 '\n"
 "                      'C144,244 134,246 125,257 Z'", 1)
# lábios acompanham o novo desenho da boca
src = src.replace("'labios':      ('c', 'M129,258 C137,249 145,247 150,252 C155,247 163,249 171,258 '\n"
                  "                      'C162,275 138,275 129,258 Z')",
                  "'labios':      ('c', 'M125,257 C134,246 144,244 150,250 C156,244 166,246 175,257 '\n"
                  "                      'C165,276 135,276 125,257 Z')", 1)

# ------------------------------------------------------------------ famílias
FAM = '''
# ---------------- AS TRÊS FAMÍLIAS (estrutura principal do livro) ----------------
REG_AZUL = ['perioral', 'labios', 'temporal', 'fronte', 'supercilio', 'nasolabial', 'labiomentual']
REG_AMAR = ['labiomentual', 'nasolabial', 'prejowl', 'bochecha', 'auricular', 'mandibula']
REG_ROXO = ['mento', 'nariz', 'zigoma', 'mandibula', 'temporal', 'infraorb']

FAMILIAS = [
 dict(n='1', nome='BAIXO G′', cor='a', grupos='grupos 1 e 2', regs=REG_AZUL,
      sub=[('azul + rosa', ['a', 'p']), ('azul + amarelo + rosa', ['a', 'm', 'p'])],
      lead='Integra, acompanha o movimento e cria pouco relevo próprio.',
      regs_txt='Região oral e perioral · lábio · têmpora, fronte e supercílio · '
               'sulco nasolabial · sulco labiomentual.',
      nota='<b>As duas assinaturas atendem as mesmas regiões.</b> A diferença entre '
           'azul + rosa e azul + amarelo + rosa é <i>quanto</i> cada uma valoriza — '
           'a segunda entrega um pouco mais de volume. A indicação não muda.'),
 dict(n='2', nome='MODERADO G′', cor='m', grupos='grupo 3', regs=REG_AMAR,
      sub=[('amarelo', ['m'])],
      lead='Preenche e equilibra: corpo sem impor projeção.',
      regs_txt='Sulco labiomentual e sulco nasolabial · pré-jowl · bochecha · '
               'região auricular anterior · valorização de mandíbula.',
      nota='A família de transição — a cor do vale. Uma assinatura só, sem subclasse: '
           'é o produto que preenche onde não se quer nem espalhar nem projetar.'),
 dict(n='3', nome='ALTO G′', cor='r', grupos='grupos 4 e 5', regs=REG_ROXO,
      sub=[('roxo puro', ['r']), ('roxo + 2ª cor', ['r', 'v']), ('na olheira', ['r', 's'])],
      lead='Sustenta. Conforme a segunda cor, projeta ou volumiza.',
      regs_txt='Mento · nariz · arco zigomático · mandíbula · têmpora (crown lift) · '
               'e, no uso preciso, a região infraorbitária.',
      nota='<b>Três usos, não um.</b> O <b>roxo puro</b> projeta — é o vértice. '
           'O <b>roxo com segunda cor</b> volumiza, com menos projeção. E o mesmo alto G′, '
           'quando tem baixo swelling factor, é o que se usa na <b>olheira</b>.'),
]

USOS_ROXO = [
 ('PROJEÇÃO', ['r'], ['mento', 'nariz', 'zigoma', 'mandibula'],
  'Roxo puro: tan δ baixo, estrutura sem modificador. Mantém o vértice onde foi colocado.'),
 ('VOLUMIZAÇÃO', ['r', 'v'], ['mandibula', 'zigoma', 'temporal', 'nasolabial', 'mento'],
  'Roxo com segunda cor: sustenta com mais curva e mais corpo. Volume estrutural, '
  'não projeção focal.'),
 ('OLHEIRA', ['r', 's'], ['infraorb'],
  'Alto G′ de <b>baixo swelling factor</b> — baixa concentração de AH e partículas grandes. '
  'É a exceção que a família comporta: estrutura numa região que não tolera inchaço. 💧'),
]

def face_fam(f, width=210):
    g = dict(n=f['n'], regs=f['regs'], cores=[f['cor'], f['sub'][-1][1][-1]], txt=f['regs_txt'])
    return face_regioes(g, width)

def mapa_familias():
    cards = ''
    for f in FAMILIAS:
        subs = ''.join(
            f'<span class="fm-sub">{"".join(dotchip(c, 11) for c in cores)}<em>{nome}</em></span>'
            for nome, cores in f['sub'])
        cards += (f'<figure class="famcard fc-{f["cor"]}">'
                  f'<figcaption><span class="fm-n">{f["n"]}</span>'
                  f'<span class="fm-t">{f["nome"]}</span>'
                  f'<span class="fm-g">{f["grupos"]}</span></figcaption>'
                  f'<p class="fm-lead">{f["lead"]}</p>'
                  f'<div class="fm-subs">{subs}</div>'
                  f'{face_fam(f)}'
                  f'<p class="fm-regs">{f["regs_txt"]}</p>'
                  f'<p class="fm-nota">{f["nota"]}</p></figure>')
    return f'<div class="mapafam">{cards}</div>'

def usos_roxo():
    out = ''
    for nome, cores, regs, txt in USOS_ROXO:
        g = dict(n='3', regs=regs, cores=cores, txt=nome)
        chips = ''.join(dotchip(c, 12) for c in cores)
        out += (f'<figure class="usocard"><figcaption>{chips}<b>{nome}</b></figcaption>'
                f'{face_regioes(g, 150)}<p>{txt}</p></figure>')
    return f'<div class="usos">{out}</div>'

'''
anchor = '# ---------------- seções de grupos ----------------'
assert anchor in src
src = src.replace(anchor, FAM + anchor, 1)

CSS = '''
/* as três famílias */
.mapafam{{display:grid;grid-template-columns:repeat(auto-fit,minmax(268px,1fr));gap:1.1rem;margin:1.2rem 0}}
.famcard{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:4px;
 padding:.65rem .95rem 1.1rem;display:flex;flex-direction:column;border-top:4px solid var(--fam-a)}}
.famcard.fc-m{{border-top-color:var(--fam-m)}} .famcard.fc-r{{border-top-color:var(--fam-r)}}
.famcard figcaption{{display:flex;align-items:baseline;gap:.5rem;flex-wrap:wrap;
 border-bottom:1px solid var(--linesoft);padding-bottom:.4rem;text-align:left}}
.fm-n{{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:1.7rem;
 line-height:1;color:var(--gold)}}
.fm-t{{font-family:'Barlow Condensed',sans-serif;font-size:1.2rem;font-weight:700;letter-spacing:.05em;
 text-transform:uppercase;color:var(--title-ink);flex:1}}
.fm-g{{font-family:'Barlow',sans-serif;font-size:.64rem;letter-spacing:.12em;text-transform:uppercase;
 color:var(--ink3);font-weight:700}}
.fm-lead{{font-family:'Barlow',sans-serif;font-size:.85rem;color:var(--ink);margin:.45rem 0 .5rem;
 line-height:1.45;text-align:left;font-weight:600}}
.fm-subs{{display:flex;flex-direction:column;gap:.22rem;margin-bottom:.3rem}}
.fm-sub{{display:flex;align-items:center;gap:.18rem}}
.fm-sub em{{font-family:'Barlow',sans-serif;font-style:normal;font-size:.74rem;color:var(--ink2);
 margin-left:.3rem;letter-spacing:.02em}}
.famcard .facereg{{margin:.3rem auto .5rem}}
.fm-regs{{font-family:'Barlow',sans-serif;font-size:.81rem;color:var(--ink);margin:0 0 .45rem;
 line-height:1.45;text-align:left;font-weight:600}}
.fm-nota{{font-family:'Barlow',sans-serif;font-size:.78rem;color:var(--ink2);margin:auto 0 0;
 line-height:1.5;text-align:left;border-top:1px solid var(--linesoft);padding-top:.45rem}}
/* os três usos do alto G' */
.usos{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:.9rem;margin:1rem 0}}
.usocard{{margin:0;background:var(--card);border:1px solid var(--line);border-left:3px solid var(--fam-r);
 border-radius:3px;padding:.55rem .8rem .9rem;text-align:center}}
.usocard figcaption{{display:flex;align-items:center;justify-content:center;gap:.25rem;
 padding-bottom:.35rem;border-bottom:1px solid var(--linesoft)}}
.usocard figcaption b{{font-family:'Barlow Condensed',sans-serif;font-size:1rem;letter-spacing:.07em;
 text-transform:uppercase;color:var(--title-ink);margin-left:.3rem}}
.usocard p{{font-family:'Barlow',sans-serif;font-size:.78rem;color:var(--ink2);margin:.2rem 0 0;
 line-height:1.45;text-align:left}}
'''
mark = '/* figuras e ilustrações com moldura dourada */'
src = src.replace(mark, CSS + mark, 1)

open(P, 'w', encoding='utf-8').write(src)
print('v15: estrutura das três famílias criada')
