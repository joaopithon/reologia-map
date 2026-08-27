# -*- coding: utf-8 -*-
"""Patch v5 — layout no padrão dos eBooks aprovados: navy + dourado, tipografia
condensada, molduras douradas, ilustrações oficiais e box QR com imagem ao lado."""
P = '/tmp/claude-0/-home-user-reologia-map/cd216e96-b088-57d1-abe3-2409c365400d/scratchpad/build_ebook.py'
src = open(P, encoding='utf-8').read()

# ---------------------------------------------------------------- 1. ilustrações
src = src.replace(
"QR = json.load(open(f'{BASE}/qrs.json'))",
"QR = json.load(open(f'{BASE}/qrs.json'))\nILU = json.load(open(f'{BASE}/ilustracoes.json'))", 1)

# ---------------------------------------------------------------- 2. box com imagem + QR
OLD_BOX = """def box_pratica(titulo, texto, qr, url):
    return (f'<aside class="pratica"><div class="bx-head">NA PRÁTICA</div><div class="bx-body"><div>'
            f'<h4>{html.escape(titulo)}</h4><p>{texto}</p>'
            f'<p class="bx-url"><a href="{html.escape(url)}">{html.escape(url)}</a></p></div>'
            f'<img class="bx-qr" src="{qr}" alt="QR code — {html.escape(titulo)}" width="118" height="118"></div></aside>')"""
NEW_BOX = '''def box_qr(titulo, texto, qr, url, kind='pratica', ilus=None, ilus_cap=''):
    """Box no padrão dos eBooks do autor: imagem ilustrativa | texto | QR."""
    head = 'NA PRÁTICA' if kind == 'pratica' else 'SAIBA MAIS'
    img = (f'<figure class="bx-ilus"><img src="{ilus}" alt="{html.escape(ilus_cap or titulo)}" loading="lazy">'
           + (f'<figcaption>{html.escape(ilus_cap)}</figcaption>' if ilus_cap else '') + '</figure>') if ilus else ''
    return (f'<aside class="qrbox {kind}"><div class="bx-head">{head}</div><div class="bx-body">{img}'
            f'<div class="bx-txt"><h4>{html.escape(titulo)}</h4><p>{texto}</p>'
            f'<p class="bx-url"><a href="{html.escape(url)}">{html.escape(url)}</a></p></div>'
            f'<div class="bx-qrwrap"><img class="bx-qr" src="{qr}" alt="QR code — {html.escape(titulo)}" width="122" height="122">'
            f'<span>aponte a câmera</span></div></div></aside>')
def box_pratica(titulo, texto, qr, url, ilus=None, ilus_cap=''):
    return box_qr(titulo, texto, qr, url, 'pratica', ilus, ilus_cap)

def figura(num, ilus, legenda, alt=''):
    return (f'<figure class="figura-img"><img src="{ilus}" alt="{html.escape(alt or legenda[:80])}" loading="lazy">'
            f'<figcaption><b>Figura {num}.</b> {legenda}</figcaption></figure>')'''
assert OLD_BOX in src
src = src.replace(OLD_BOX, NEW_BOX, 1)

# ---------------------------------------------------------------- 3. fontes
src = src.replace(
'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700;9..144,900&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;600;700&display=swap">',
'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&family=JetBrains+Mono:wght@400;600;700&display=swap">', 1)

# ---------------------------------------------------------------- 4. tokens de cor
i0 = src.index(':root {{'); i1 = src.index('*{{box-sizing:border-box}}')
NEW_TOKENS = """:root {{
 /* identidade dos eBooks: navy profundo + dourado metálico */
 --navy:#0A3557; --navy-2:#10486F; --navy-3:#2A6C9C; --navy-ink:#092C48;
 --gold:#C08A2E; --gold-2:#E0A64B; --gold-3:#F5CE7B; --gold-soft:rgba(224,166,75,.13);
 --bg:#FBF9F6; --card:#FFFFFF; --ink:#15293C; --ink2:#4C5C6B; --ink3:#8494A1;
 --line:#E4DFD6; --linesoft:#F0EBE3; --accent:var(--navy-2); --accent-ink:#0E4269; --accent-soft:#EAF1F7;
 --fam-a:#2E7DBF; --fam-m:#8F6D12; --fam-r:#7C3AED; --fam-v:#3E9B6E;
 --chip-rosa:#C4557F; --sf:#0F7480; --sf-soft:rgba(15,116,128,.09);
 --warn:#A8501F; --flag:#B23B3B;
 --za:rgba(46,125,191,.05); --zm:rgba(143,109,18,.06); --zr:rgba(124,58,237,.045);
 --n1bg:#10486F; --n1ink:#FFFFFF; --n2bg:#DCE8F1; --n2ink:#0E4269; --n3bd:#A9BFD1; --n3ink:#31536E; --n4ink:#7A8794;
 --tint:12%;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
 --navy:#071F33; --navy-2:#0C2A42; --navy-3:#2A6C9C; --navy-ink:#DCE8F1;
 --gold:#D6A048; --gold-2:#E9B968; --gold-3:#F7DA96; --gold-soft:rgba(233,185,104,.14);
 --bg:#071F33; --card:#0C2A42; --ink:#E8EEF4; --ink2:#A9BCCB; --ink3:#728A9C;
 --line:#1B3E5A; --linesoft:#16344C; --accent:#4E97D0; --accent-ink:#8CC0E8; --accent-soft:#123category;
 --fam-a:#3F87C4; --fam-m:#AC831F; --fam-r:#8E68D8; --fam-v:#43A076;
 --chip-rosa:#C96B92; --sf:#3DA0AC; --sf-soft:rgba(61,160,172,.15);
 --warn:#D08A5E; --flag:#DC7E7E;
 --za:rgba(63,135,196,.10); --zm:rgba(172,131,31,.12); --zr:rgba(142,104,216,.10);
 --n1bg:#2A6C9C; --n1ink:#08192A; --n2bg:#173F5C; --n2ink:#A9D2EE; --n3bd:#2F5B7C; --n3ink:#8CC0E8; --n4ink:#7A93A6;
 --tint:22%;
}} }}
:root[data-theme="dark"] {{
 --navy:#071F33; --navy-2:#0C2A42; --navy-3:#2A6C9C; --navy-ink:#DCE8F1;
 --gold:#D6A048; --gold-2:#E9B968; --gold-3:#F7DA96; --gold-soft:rgba(233,185,104,.14);
 --bg:#071F33; --card:#0C2A42; --ink:#E8EEF4; --ink2:#A9BCCB; --ink3:#728A9C;
 --line:#1B3E5A; --linesoft:#16344C; --accent:#4E97D0; --accent-ink:#8CC0E8; --accent-soft:#123650;
 --fam-a:#3F87C4; --fam-m:#AC831F; --fam-r:#8E68D8; --fam-v:#43A076;
 --chip-rosa:#C96B92; --sf:#3DA0AC; --sf-soft:rgba(61,160,172,.15);
 --warn:#D08A5E; --flag:#DC7E7E;
 --za:rgba(63,135,196,.10); --zm:rgba(172,131,31,.12); --zr:rgba(142,104,216,.10);
 --n1bg:#2A6C9C; --n1ink:#08192A; --n2bg:#173F5C; --n2ink:#A9D2EE; --n3bd:#2F5B7C; --n3ink:#8CC0E8; --n4ink:#7A93A6;
 --tint:22%;
}}
"""
src = src[:i0] + NEW_TOKENS + src[i1:]
src = src.replace('--accent-soft:#123category;', '--accent-soft:#123650;')

# ---------------------------------------------------------------- 5. tipografia base
src = src.replace(
"""body{{margin:0;background:var(--bg);color:var(--ink);font-family:'Source Serif 4',Georgia,serif;font-size:15.5px;line-height:1.6}}
.pill,.lbl,.marca,.legend,.stat span,.famdesc,.fam-eyebrow,.sflink,.evite,.alts,.tech,.flags,.sfnum,.sigdots,.bx-url{{font-family:'Source Sans 3',system-ui,sans-serif}}
.cap-eyebrow{{font-family:'JetBrains Mono',monospace;font-size:.68rem;letter-spacing:.24em;text-transform:uppercase;color:var(--accent-ink);margin:0 0 .25rem}}""",
"""body{{margin:0;background:var(--bg);color:var(--ink);font-family:'Source Serif 4',Georgia,serif;font-size:16px;line-height:1.62}}
.pill,.lbl,.marca,.legend,.stat span,.famdesc,.fam-eyebrow,.sflink,.evite,.alts,.tech,.flags,.sfnum,.sigdots,.bx-url,.bx-qrwrap span,.a9q{{font-family:'Barlow',system-ui,sans-serif}}
h1,h2,h3,h4,.famtag,.capa-brand,.bx-head{{font-family:'Barlow Condensed','Barlow',sans-serif}}
h2,h3{{text-transform:uppercase;letter-spacing:.015em}}
.cap-eyebrow{{font-family:'Barlow',sans-serif;font-size:.72rem;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:var(--gold);margin:0 0 .2rem}}
.cap-eyebrow::before{{content:"";display:inline-block;width:26px;height:2px;background:var(--gold);vertical-align:.28em;margin-right:.55rem}}""", 1)

# ---------------------------------------------------------------- 6. CSS: capa e componentes novos
i2 = src.index('.capa{{'); i3 = src.index('.fichatec{{')
NEW_CAPA_CSS = """.capa{{padding:0;margin-bottom:1.6rem;border:none;background:none;border-radius:0}}
.capa-in{{background:linear-gradient(142deg,#0A3557 0%,#0E4269 46%,#2E76A8 100%);padding:clamp(1rem,3vw,2rem);position:relative;overflow:hidden}}
.capa-in::before{{content:"";position:absolute;inset:0;background:radial-gradient(circle at 88% 8%,rgba(255,255,255,.13),transparent 55%);pointer-events:none}}
.capa-frame{{border:1.5px solid var(--gold-2);padding:clamp(1.6rem,4vw,2.8rem) clamp(1rem,3vw,2.2rem);text-align:center;position:relative}}
.capa-frame p{{max-width:none}}
.capa-brand{{font-size:.8rem;font-weight:600;letter-spacing:.34em;text-transform:uppercase;color:var(--gold-3);margin:0 0 1.1rem}}
.capa h1{{font-size:clamp(2.4rem,7.6vw,5rem);font-weight:700;line-height:.94;letter-spacing:.005em;margin:0 0 .2rem;text-transform:uppercase}}
.capa h1 .gold{{background:linear-gradient(178deg,#F7DA96 4%,#E0A64B 42%,#C08A2E 74%,#F0C878 100%);-webkit-background-clip:text;background-clip:text;color:#E0A64B;-webkit-text-fill-color:transparent;display:block}}
@supports not (-webkit-background-clip:text){{.capa h1 .gold{{-webkit-text-fill-color:#E0A64B;color:#E0A64B}}}}
.capa h1 .wht{{color:#fff;font-weight:500;font-size:.5em;letter-spacing:.045em;display:block;margin-top:.2em}}
.capa-grid{{display:grid;grid-template-columns:1fr 1fr;gap:clamp(.5rem,1.6vw,1rem);margin:clamp(1.1rem,3vw,1.9rem) auto;max-width:660px}}
.capa-grid figure{{margin:0;border:2px solid var(--gold-2);background:#08283F;overflow:hidden}}
.capa-grid img{{display:block;width:100%;height:100%;object-fit:cover;aspect-ratio:16/9}}
.capa-sub{{border:1px solid var(--gold-2);display:inline-block;padding:.5rem 1.4rem;color:#fff;font-family:'Barlow Condensed',sans-serif;font-size:clamp(.86rem,2.1vw,1.12rem);font-weight:500;letter-spacing:.075em;text-transform:uppercase;margin:.2rem auto 1.2rem}}
.capa-autor{{font-family:'Barlow Condensed',sans-serif;font-size:clamp(1.15rem,3vw,1.6rem);font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-2);margin:0}}
.capa-ed{{font-family:'Barlow',sans-serif;font-size:.74rem;letter-spacing:.24em;text-transform:uppercase;color:rgba(255,255,255,.62);margin:.7rem 0 0}}
.capa-band{{height:7px;background:linear-gradient(90deg,var(--fam-a) 0 25%,var(--fam-m) 25% 50%,var(--fam-r) 50% 75%,var(--fam-v) 75% 100%)}}
/* figuras e ilustrações com moldura dourada */
.figura-img{{margin:1.4rem 0;background:var(--card);border:1px solid var(--line);border-radius:4px;padding:.7rem}}
.figura-img>img{{display:block;width:100%;height:auto;border:2px solid var(--gold-2)}}
.figura-img figcaption{{font-family:'Barlow',sans-serif;font-size:.86rem;color:var(--ink2);padding:.7rem .3rem .1rem;line-height:1.5}}
.figura-img figcaption b{{color:var(--navy-2);font-weight:700}}
:root[data-theme="dark"] .figura-img figcaption b, :root:not([data-theme="light"]) .figura-img figcaption b{{color:var(--gold-2)}}
.iludupla{{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:1rem}}
.iludupla .figura-img{{margin:0}}
/* box QR no padrão do autor */
.qrbox{{margin:1.6rem 0;border:1px solid var(--line);border-left:4px solid var(--gold-2);background:var(--card);border-radius:4px;overflow:hidden}}
.bx-head{{font-size:.9rem;font-weight:700;letter-spacing:.24em;text-transform:uppercase;padding:.5rem 1.2rem;color:var(--gold-3);background:linear-gradient(100deg,var(--navy) 0%,var(--navy-2) 70%,var(--navy-3) 130%)}}
.saibamais .bx-head{{background:linear-gradient(100deg,#08343A 0%,#0F7480 120%)}}
.bx-body{{display:flex;gap:1.1rem;padding:1.1rem 1.2rem;align-items:center;flex-wrap:wrap}}
.bx-ilus{{margin:0;flex:0 0 218px;max-width:100%}}
.bx-ilus img{{display:block;width:100%;height:auto;border:2px solid var(--gold-2)}}
.bx-ilus figcaption{{font-family:'Barlow',sans-serif;font-size:.72rem;color:var(--ink3);padding-top:.35rem;line-height:1.4}}
.bx-txt{{flex:1;min-width:210px}}
.bx-body h4{{margin:0 0 .35rem;font-size:1.16rem;font-weight:600;text-transform:uppercase;letter-spacing:.01em;color:var(--navy-2)}}
:root[data-theme="dark"] .bx-body h4, :root:not([data-theme="light"]) .bx-body h4{{color:var(--gold-2)}}
.bx-body p{{margin:.2rem 0;font-size:.93rem;max-width:56ch}}
.bx-qrwrap{{flex:none;text-align:center}}
.bx-qr{{border:2px solid var(--gold-2);background:#fff;padding:5px;display:block}}
.bx-qrwrap span{{display:block;font-size:.66rem;letter-spacing:.16em;text-transform:uppercase;color:var(--ink3);margin-top:.35rem}}
.bx-url a{{font-size:.76rem;word-break:break-all;color:var(--ink3)}}
.fichatec{{"""
src = src[:i2] + NEW_CAPA_CSS + src[i3+len('.fichatec{{'):]

# ---------------------------------------------------------------- 7. ajustes de componentes
REPL = [
 # bandeiras de capítulo: faixa navy com barra dourada
 (""".bn-a{{background:linear-gradient(120deg,color-mix(in srgb,var(--fam-a) var(--tint),var(--card)),var(--card) 78%);border-left:8px solid var(--fam-a)}}
.bn-m{{background:linear-gradient(120deg,color-mix(in srgb,var(--fam-m) var(--tint),var(--card)),var(--card) 78%);border-left:8px solid var(--fam-m)}}
.bn-r{{background:linear-gradient(120deg,color-mix(in srgb,var(--fam-r) var(--tint),var(--card)),color-mix(in srgb,var(--fam-v) 8%,var(--card)));border-left:8px solid var(--fam-r)}}
.bn-s{{background:linear-gradient(120deg,var(--sf-soft),var(--card) 78%);border-left:8px solid var(--sf)}}""",
  """.fambanner{{border-radius:4px;color:#fff;border:none;position:relative}}
.fambanner::after{{content:"";position:absolute;left:0;right:0;bottom:0;height:4px}}
.bn-a{{background:linear-gradient(112deg,var(--navy) 0%,var(--navy-2) 62%,#2E76A8 128%)}}
.bn-a::after{{background:var(--fam-a)}}
.bn-m{{background:linear-gradient(112deg,var(--navy) 0%,var(--navy-2) 62%,#2E76A8 128%)}}
.bn-m::after{{background:var(--fam-m)}}
.bn-r{{background:linear-gradient(112deg,var(--navy) 0%,var(--navy-2) 62%,#2E76A8 128%)}}
.bn-r::after{{background:var(--fam-r)}}
.bn-s{{background:linear-gradient(112deg,#062A30 0%,#0A4A53 66%,#0F7480 130%)}}
.bn-s::after{{background:var(--sf)}}
.fambanner .fam-eyebrow{{color:var(--gold-3)}}
.fambanner h2{{color:#fff}}
.fambanner .famchave{{color:rgba(255,255,255,.9)}}
.fambanner .famdesc{{color:rgba(255,255,255,.82)}}
.fambanner .famdesc b{{color:var(--gold-3)}}
.fambanner .chip{{border-color:rgba(255,255,255,.35)}}"""),
 # h2 e caixas
 ("""h2{{font-size:1.65rem;font-weight:700;margin:0 0 .8rem}}""",
  """h2{{font-size:1.9rem;font-weight:700;margin:0 0 .8rem;color:var(--navy-2)}}
:root[data-theme="dark"] h2, :root:not([data-theme="light"]) h2{{color:var(--ink)}}
.fambanner h2{{font-size:2.05rem}}"""),
 ("""h3{{font-size:1.15rem;margin:1.4rem 0 .5rem}}""",
  """h3{{font-size:1.28rem;font-weight:600;margin:1.6rem 0 .5rem;color:var(--navy-2);border-bottom:1px solid var(--line);padding-bottom:.3rem}}
:root[data-theme="dark"] h3, :root:not([data-theme="light"]) h3{{color:var(--gold-2)}}"""),
 (""".box{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1.1rem 1.3rem}}""",
  """.box{{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:1.1rem 1.3rem}}"""),
 (""".qt{{border-left:3px solid var(--accent);background:var(--accent-soft);border-radius:0 10px 10px 0;padding:.8rem 1.1rem;font-family:'Fraunces',serif;font-size:1.06rem;margin:1rem 0;max-width:70ch}}""",
  """.qt{{border-left:4px solid var(--gold-2);background:var(--gold-soft);border-radius:0 4px 4px 0;padding:.85rem 1.15rem;font-family:'Source Serif 4',serif;font-style:italic;font-size:1.08rem;margin:1.1rem 0;max-width:70ch}}"""),
 # cards
 (""".card h4{{font-family:'Fraunces',serif;font-size:1.1rem;margin:0;line-height:1.15}}""",
  """.card h4{{font-size:1.2rem;font-weight:600;margin:0;line-height:1.12;text-transform:uppercase;letter-spacing:.005em;color:var(--navy-2)}}
:root[data-theme="dark"] .card h4, :root:not([data-theme="light"]) .card h4{{color:var(--ink)}}"""),
 (""".card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:0 1.1rem 1rem;""",
  """.card{{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:0 1.1rem 1rem;"""),
 (""".escolha{{margin:0;border-left:3px solid var(--accent);background:color-mix(in srgb,var(--accent-soft) 70%,transparent);padding:.5rem .7rem;border-radius:0 8px 8px 0;font-size:.9rem;font-style:italic}}""",
  """.escolha{{margin:0;border-left:3px solid var(--gold-2);background:var(--gold-soft);padding:.5rem .7rem;border-radius:0 4px 4px 0;font-size:.92rem;font-style:italic}}"""),
 (""".sfcard h4{{font-family:'Fraunces',serif;font-size:1.02rem;margin:0}}""",
  """.sfcard h4{{font-size:1.1rem;font-weight:600;text-transform:uppercase;margin:0;color:var(--navy-2)}}
:root[data-theme="dark"] .sfcard h4, :root:not([data-theme="light"]) .sfcard h4{{color:var(--ink)}}"""),
 (""".gramc h4{{font-family:'Fraunces',serif;margin:0 0 .1rem;font-size:1.02rem}}""",
  """.gramc h4{{margin:0 0 .1rem;font-size:1.14rem;font-weight:600;text-transform:uppercase;color:var(--navy-2)}}
:root[data-theme="dark"] .gramc h4, :root:not([data-theme="light"]) .gramc h4{{color:var(--ink)}}"""),
 (""".rdemo{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:.9rem;text-align:center}}""",
  """.rdemo{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:4px;padding:.9rem;text-align:center}}"""),
 (""".chart{{width:100%;height:auto;background:var(--card);border:1px solid var(--line);border-radius:10px;margin-top:.6rem}}""",
  """.chart{{width:100%;height:auto;background:var(--card);border:1px solid var(--line);border-radius:4px;margin-top:.6rem}}"""),
 (""".stat{{background:var(--card);border:1px solid var(--line);border-top:4px solid var(--accent);border-radius:8px;padding:.7rem 1.1rem;min-width:8.5rem}}""",
  """.stat{{background:var(--card);border:1px solid var(--line);border-top:4px solid var(--accent);border-radius:4px;padding:.7rem 1.1rem;min-width:8.5rem}}"""),
 (""".stat b{{display:block;font-family:'JetBrains Mono',monospace;font-size:1.35rem;color:var(--accent-ink)}}""",
  """.stat b{{display:block;font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:1.75rem;line-height:1.05;color:var(--navy-2)}}
:root[data-theme="dark"] .stat b, :root:not([data-theme="light"]) .stat b{{color:var(--gold-2)}}"""),
 (""".fichatec{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1rem 1.3rem;margin-bottom:.4rem}}""",
  """.fichatec{{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:1rem 1.3rem;margin-bottom:.4rem}}"""),
 (""".gelcard{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1rem;text-align:center}}""",
  """.gelcard{{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:1rem;text-align:center}}"""),
 (""".gelcard h4{{font-family:'Fraunces',serif;margin:.4rem 0 .2rem}}""",
  """.gelcard h4{{margin:.4rem 0 .2rem;font-size:1.12rem;font-weight:600;text-transform:uppercase;color:var(--navy-2)}}
:root[data-theme="dark"] .gelcard h4, :root:not([data-theme="light"]) .gelcard h4{{color:var(--ink)}}"""),
 (""".ixm b{{display:block;font-family:'Fraunces',serif;margin-bottom:.15rem}}""",
  """.ixm b{{display:block;font-family:'Barlow Condensed',sans-serif;font-size:1.06rem;font-weight:700;text-transform:uppercase;color:var(--navy-2);margin-bottom:.15rem;border-bottom:1px solid var(--linesoft)}}
:root[data-theme="dark"] .ixm b, :root:not([data-theme="light"]) .ixm b{{color:var(--gold-2)}}"""),
 (""".famchave{{font-family:'Fraunces',serif;font-style:italic;color:var(--ink2);margin:.35rem 0 0;max-width:44ch}}""",
  """.famchave{{font-family:'Source Serif 4',serif;font-style:italic;font-size:1.04rem;color:var(--ink2);margin:.4rem 0 0;max-width:46ch}}"""),
 (""".sfcard{{background:var(--card);border:1px solid var(--line);border-left:6px solid var(--sf);border-radius:10px;""",
  """.sfcard{{background:var(--card);border:1px solid var(--line);border-left:6px solid var(--sf);border-radius:4px;"""),
 (""".regtab{{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--card)}}""",
  """.regtab{{overflow-x:auto;border:1px solid var(--line);border-radius:4px;background:var(--card)}}"""),
 (""".regtab th{{font-size:.74rem;letter-spacing:.06em;text-transform:uppercase;color:var(--ink3)}}""",
  """.regtab th{{font-family:'Barlow',sans-serif;font-size:.76rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#fff;background:var(--navy-2)}}"""),
 (""".a9c{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:.65rem .8rem;text-align:center}}""",
  """.a9c{{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:.65rem .8rem;text-align:center}}"""),
 (""".a9n{{font-family:'JetBrains Mono',monospace;font-size:.68rem;font-weight:700;letter-spacing:.04em;line-height:1.3;display:block}}""",
  """.a9n{{font-family:'Barlow Condensed',sans-serif;font-size:.92rem;font-weight:700;letter-spacing:.03em;line-height:1.15;display:block;color:var(--navy-2)}}
:root[data-theme="dark"] .a9n, :root:not([data-theme="light"]) .a9n{{color:var(--ink)}}"""),
 (""".gramc{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1rem;display:flex;gap:.8rem;align-items:flex-start}}""",
  """.gramc{{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:1rem;display:flex;gap:.8rem;align-items:flex-start}}"""),
 (""".assin-v{{display:flex;align-items:center;gap:.3rem;font-family:'JetBrains Mono',monospace;font-size:.74rem;letter-spacing:.02em}}""",
  """.assin-v{{display:flex;align-items:center;gap:.3rem;font-family:'Barlow Condensed',sans-serif;font-size:1rem;font-weight:700;letter-spacing:.02em}}"""),
 (""".famtag{{font-family:'JetBrains Mono',monospace;font-size:.58rem;font-weight:700;letter-spacing:.09em;white-space:nowrap}}""",
  """.famtag{{font-size:.76rem;font-weight:700;letter-spacing:.07em;white-space:nowrap;text-transform:uppercase}}"""),
 # print
 ("""@media print{{ body{{background:#fff;font-size:11px}} .famsec,#rankings,#regioes,#textura{{break-before:page}}
 .card,.sfcard,.rdemo,.pratica,.saibamais{{break-inside:avoid;border-color:#ccc}} #tip{{display:none}} .capa{{border:none}} }}""",
  """@media print{{ body{{background:#fff;font-size:10.5px}} .famsec,#rankings,#regioes,#textura,#atlas{{break-before:page}}
 .card,.sfcard,.rdemo,.qrbox,.figura-img,.gelcard,.gramc{{break-inside:avoid}} #tip{{display:none}}
 .capa-in{{-webkit-print-color-adjust:exact;print-color-adjust:exact}} .fambanner,.bx-head,.regtab th{{-webkit-print-color-adjust:exact;print-color-adjust:exact}} }}"""),
]
for a, b in REPL:
    if a not in src:
        raise SystemExit('CSS/HTML alvo não encontrado: ' + a[:80])
    src = src.replace(a, b, 1)

# ---------------------------------------------------------------- 8. nova capa (HTML)
i4 = src.index('<header class="capa">'); i5 = src.index('<div class="fichatec">')
NEW_CAPA = """<header class="capa">
<div class="capa-in">
<div class="capa-frame">
<p class="capa-brand">Reology Map · Ciência que guia escolhas</p>
<h1><span class="gold">Reologia do<br>Ácido Hialurônico</span><span class="wht">Guia dos preenchedores do mercado brasileiro</span></h1>
<div class="capa-grid">
<figure><img src="{ILU['g1a']}" alt="Grupo 1 — fluidos dinâmicos" loading="eager"></figure>
<figure><img src="{ILU['g3a']}" alt="Grupo 3 — equilibrados" loading="eager"></figure>
<figure><img src="{ILU['g4a']}" alt="Grupo 4 — projetores puros" loading="lazy"></figure>
<figure><img src="{ILU['g6a']}" alt="Grupo 6 — baixo swelling factor" loading="lazy"></figure>
</div>
<p class="capa-sub">75 produtos canônicos · 76 ensaios · 6 grupos · 9 assinaturas</p>
<p class="capa-autor">Por Dr. João Pithon</p>
<p class="capa-ed">Primeira edição · São Paulo · 2026</p>
</div>
</div>
<div class="capa-band"></div>
</header>

<div class="fichatec">"""
src = src[:i4] + NEW_CAPA + src[i5+len('<div class="fichatec">'):]

# ---------------------------------------------------------------- 9. ilustração oficial em cada grupo
OLD_G = """    fam_secs.append(f'''<section class="famsec" id="grupo-{G['num']}">
<div class="fambanner bn-{G['fam']}"><div><p class="fam-eyebrow">CAPÍTULO {CH0+gi} · GRUPO {G['num']} · {html.escape(G['tec'])}</p><h2>{G['nome']}</h2>
<p class="famchave">“{html.escape(G['chave'])}”</p></div>
<div><p class="famdesc"><b>Faixas do grupo:</b> {G['bandas']}<br><b>Melhores contextos:</b> {html.escape(G['ctx'])} · <b>Produto-exemplo:</b> {html.escape(G['ex'])}</p>{extra}
<p class="famdesc" style="margin-top:.3rem"><b>{len(prods)} produtos</b> · G′ de {br(gmin)} a {br(gmax)} Pa</p></div></div>
<div class="grid2">{cards}</div></section>''')"""
NEW_G = """    ilus = f'''<div class="iludupla">
{figura(f'{G["num"]}.1', ILU[f'g{G["num"]}a'], f'<b>{G["nome"]}</b> — leitura conceitual do grupo: características, leitura clínica, comportamento e mensagem-chave. Ilustração oficial do Mapa da Reologia.')}
{figura(f'{G["num"]}.2', ILU[f'g{G["num"]}b'], 'Exemplos do grupo com os valores medidos a 0,7 Hz, na linguagem de cores do Mapa. As fichas a seguir detalham cada produto.')}
</div>'''
    fam_secs.append(f'''<section class="famsec" id="grupo-{G['num']}">
<div class="fambanner bn-{G['fam']}"><div><p class="fam-eyebrow">CAPÍTULO {CH0+gi} · GRUPO {G['num']} · {html.escape(G['tec'])}</p><h2>{G['nome']}</h2>
<p class="famchave">“{html.escape(G['chave'])}”</p></div>
<div><p class="famdesc"><b>Faixas do grupo:</b> {G['bandas']}<br><b>Melhores contextos:</b> {html.escape(G['ctx'])} · <b>Produto-exemplo:</b> {html.escape(G['ex'])}</p>{extra}
<p class="famdesc" style="margin-top:.3rem"><b>{len(prods)} produtos</b> · G′ de {br(gmin)} a {br(gmax)} Pa</p></div></div>
{ilus}
<div class="grid2">{cards}</div></section>''')"""
assert OLD_G in src
src = src.replace(OLD_G, NEW_G, 1)

# grupo 6 (SF)
OLD_SF = """<div class="grid3">{sf_cards}</div></section>'''"""
NEW_SF = """<div class="iludupla">
{figura('6.1', ILU['g6a'], '<b>Baixo Swelling Factor</b> — o padrão funcional: alto G′ + baixa concentração de AH + partículas grandes + estabilidade química. Ilustração oficial do Mapa da Reologia.')}
{figura('6.2', ILU['g6b'], 'Os produtos do grupo com G′ medido e a concentração declarada de AH (20–22 mg/mL). O Swelling Factor em si ainda não foi medido — é a prioridade da 2ª rodada.')}
</div>
<div class="grid3">{sf_cards}</div></section>'''"""
assert OLD_SF in src
src = src.replace(OLD_SF, NEW_SF, 1)

# ---------------------------------------------------------------- 10. esquema oficial no capítulo 1 + boxes com imagem
OLD_ESQ = """<h3 style="margin-top:1.2rem">A gramática das cores — 1ª cor, 2ª cor, assinatura</h3>"""
NEW_ESQ = """{figura('1', ILU['esquema'], 'O <b>Esquema de Descrição dos Ácidos Hialurônicos</b> — a leitura completa do perfil reológico em quatro passos: a 1ª cor (G′), a 2ª cor (comportamento), a assinatura resultante e a leitura clínica em três perguntas. Identidade oficial do Reology Map.')}
<h3 style="margin-top:1.2rem">A gramática das cores — 1ª cor, 2ª cor, assinatura</h3>"""
assert OLD_ESQ in src
src = src.replace(OLD_ESQ, NEW_ESQ, 1)

# box de aulas (fundamentos) ganha ilustração
OLD_B1 = """{box_pratica('Aulas de reologia do autor (FEP)',
 'Acesse as aulas do Dr. João Pithon sobre reologia aplicada ao preenchimento — fundamentos, leitura de parâmetros e escolha do produto na prática clínica. Escaneie o QR Code com a câmera do celular para abrir a pasta de aulas no Drive.',
 QR['aulas'], 'https://drive.google.com/drive/folders/1ztwjgguHK3VdDHG-j2E5CL4ViGglwpv-')}"""
NEW_B1 = """{box_pratica('Aulas de reologia do autor (FEP)',
 'Acesse as aulas do Dr. João Pithon sobre reologia aplicada ao preenchimento — fundamentos, leitura dos parâmetros e escolha do produto na prática clínica. Escaneie o QR Code com a câmera do celular para abrir a pasta de aulas.',
 QR['aulas'], 'https://drive.google.com/drive/folders/1ztwjgguHK3VdDHG-j2E5CL4ViGglwpv-',
 ilus=ILU['g3b'], ilus_cap='Leitura de grupo na aula: os valores a 0,7 Hz na linguagem de cores.')}"""
assert OLD_B1 in src
src = src.replace(OLD_B1, NEW_B1, 1)

# box de textura ganha ilustração
OLD_B2 = """{box_pratica('Vídeos e imagens de textura — galeria oficial do estudo',
 'Assista aos vídeos ilustrativos de extrusão e textura dos géis (em gota, como mel, rígido/fraturado) e veja as imagens comparativas da galeria do Reology Map. O acervo é atualizado continuamente pelo autor — os vídeos de cada grupo entram nesta mesma pasta.',
 QR['galeria'], 'https://drive.google.com/drive/folders/1xcyZVRcnvkHyYFCXOlZf9pWmq-CVwlm1')}"""
NEW_B2 = """{box_pratica('Vídeos e imagens de textura — galeria oficial',
 'Assista aos vídeos ilustrativos de extrusão e textura dos géis (em gota, como mel, rígido/fraturado) e veja as imagens comparativas da galeria do Reology Map. O acervo é atualizado continuamente pelo autor — os vídeos de cada grupo entram nesta mesma pasta.',
 QR['galeria'], 'https://drive.google.com/drive/folders/1xcyZVRcnvkHyYFCXOlZf9pWmq-CVwlm1',
 ilus=ILU['g1b'], ilus_cap='Da textura ao número: o grupo mais fluido do banco e seus valores medidos.')}"""
assert OLD_B2 in src
src = src.replace(OLD_B2, NEW_B2, 1)

# box final ganha ilustração
OLD_B3 = """{box_pratica('Continue com o autor — aulas e atualizações',
 'As aulas de reologia da FEP e os materiais complementares do Reology Map ficam na pasta oficial do autor. Escaneie para acessar; o conteúdo é atualizado continuamente.',
 QR['aulas'], 'https://drive.google.com/drive/folders/1ztwjgguHK3VdDHG-j2E5CL4ViGglwpv-')}"""
NEW_B3 = """{box_qr('Continue com o autor — aulas e atualizações',
 'As aulas de reologia da FEP e os materiais complementares do Reology Map ficam na pasta oficial do autor. Escaneie para acessar; o conteúdo é atualizado continuamente.',
 QR['aulas'], 'https://drive.google.com/drive/folders/1ztwjgguHK3VdDHG-j2E5CL4ViGglwpv-',
 kind='saibamais', ilus=ILU['g5b'], ilus_cap='Material complementar: grupos, valores e leitura clínica.')}"""
assert OLD_B3 in src
src = src.replace(OLD_B3, NEW_B3, 1)

open(P, 'w', encoding='utf-8').write(src)
print('patch v5 aplicado')
