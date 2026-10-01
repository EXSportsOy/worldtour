"""Tuottaa sivuston HTML-sivut. Aja: python build.py

Rakenne on yhteinen kaikille kielille; markkinointitekstit tulevat sanastosta (T).
Oikeudelliset tekstit luetaan legal/fi- ja legal/en-lähteistä (legal_content.py).
Suomi on juuressa (/), muut kielet omassa kansiossaan (/en/). Uusi kieli lisätään
LANGS-taulukkoon ja sanastoon, muuta ei tarvitse muuttaa.
"""
import os
from html import escape
from legal_content import LEGAL_SLUGS, footer_links, legal_language, render_document

SITE = "https://worldtour.exsports.fi"
PLAY = "https://play.google.com/store/apps/details?id=fi.exsports.exsworldtour"
PAGES = ["", "nain-pelaat/", "lista/", "s/"] + [f"{slug}/" for slug in LEGAL_SLUGS]

# Kielet julkaisujärjestyksessä: suomi juuressa, muut omassa kansiossaan.
LANG_ORDER = ["fi", "en", "sv", "no", "da", "de", "nl", "fr", "es", "it", "pt", "pl", "et", "lv", "lt"]

ROWS = [(1, "Riikka_fin", "BS 540 + Indy", "15 890"), (2, "Snowdog", "Etuvoltti 360 + Nose", "15 660"),
        (3, "Kaamos", "FS 540", "15 020"), (4, "Aino", "Takavoltti 360", "14 780"), (5, "Pihla", "FS 360 + Indy", "14 310"),
        (6, "Eero", "BS 360 + Weddle", "13 960"), (7, "Noora", "Shifty", "13 420"), (8, "Jussi", "BS 360", "12 980"),
        (9, "Liisa", "Suora hyppy", "12 640"), (10, "Oskari", "FS 180", "12 100"), (11, "Mea", "Etuvoltti 360", "11 870"),
        (12, "Saku", "BS 540", "11 540")]

# ---------------------------------------------------------------- sanasto (i18n/<kieli>.json)
import json
T = {}
LANGS = {}
for _lang in LANG_ORDER:
    _path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "i18n", f"{_lang}.json")
    if not os.path.exists(_path):
        raise FileNotFoundError(f"Missing translation: {_path}")
    with open(_path, encoding="utf-8") as _f:
        _d = json.load(_f)
    _d["lang"] = _lang
    T[_lang] = _d
    LANGS[_lang] = {"prefix": "" if _lang == "fi" else f"{_lang}/", "name": _d["meta"]["name"], "short": _d["meta"]["short"]}


def trick(name, lang):
    for fi, tr in T[lang]["meta"].get("tricks", {}).items():
        name = name.replace(fi, tr)
    return name


def local_link(lang, rel):
    """Keep Finnish explicit because unprefixed entry URLs detect the language."""
    url = f'/{LANGS[lang]["prefix"]}{rel}'
    if lang == "fi":
        url += ("&" if "?" in url else "?") + "lang=fi"
    return escape(url, quote=True)


# ---------------------------------------------------------------- runko
def page(lang, rel, title, desc, body, current):
    is404 = rel == "404"
    is_legal = rel in [f"{slug}/" for slug in LEGAL_SLUGS]
    script = '' if is_legal else '<script src="/assets/js/site.js" defer></script>'
    language_script = '' if is_legal else '<script src="/assets/js/language.js"></script>'
    t = T[lang]
    footer_text = "EXS World Tour · EXSports Oy" if is_legal else t["foot_text"]
    p = LANGS[lang]["prefix"]
    rel = "" if rel == "404" else rel  # GitHub Pages näyttää vain juuren 404.html:n; sen linkit osoittavat etusivulle
    url = f"{SITE}/{p}{rel}"
    L = lambda r: local_link(lang, r)

    def nav(href, label):
        cur = ' aria-current="page"' if href == current else ""
        return f'<a href="{href}"{cur}>{label}</a>'

    alternates = "".join(f'<link rel="alternate" hreflang="{l}" href="{SITE}/{LANGS[l]["prefix"]}{rel}">\n' for l in LANGS)
    alternates += f'<link rel="alternate" hreflang="x-default" href="{SITE}/en/{rel}">\n'
    if is404:
        alternates = '<meta name="robots" content="noindex">\n'
    switch = ""
    for l in LANGS:
        cur = ' aria-current="true"' if l == lang else ""
        switch += f'<li><a href="{local_link(l, rel)}" data-language="{l}" hreflang="{l}" lang="{l}"{cur}>{LANGS[l]["name"]}</a></li>'

    head = f'''<!doctype html>
<html lang="{lang}" data-theme="viimeinen-valo" data-languages="{' '.join(LANGS)}" data-page="{'404' if is404 else rel}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc, quote=True)}">
<link rel="canonical" href="{url}">
{alternates}<meta property="og:type" content="website">
<meta property="og:site_name" content="EXS World Tour">
<meta property="og:title" content="{escape(title, quote=True)}">
<meta property="og:description" content="{escape(desc, quote=True)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/og-image.jpg">
<meta property="og:locale" content="{t["meta"]["locale"]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0c1426">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; font-src 'self'; script-src 'self'; connect-src 'self'; base-uri 'self'; form-action 'self'">
{language_script}
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/BarlowCondensed-ExtraBoldItalic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/tokens.css">
<link rel="stylesheet" href="/assets/css/bundle.css">
<link rel="stylesheet" href="/assets/css/site.css">
{script}
</head>
<body class="exs{' legal-page' if is_legal else ''}">
<a class="skip" href="#sisalto">{t["skip"]}</a>
<header class="site-header"><div class="wrap">
<a class="brand" href="{L("")}" aria-label="{t["brand_aria"]}"><span class="brand__exs">EXS</span><span class="brand__bar"></span><span class="brand__wt">World Tour</span></a>
<nav class="site-nav" aria-label="{t["nav_aria"]}">{nav(L("nain-pelaat/"), t["nav_how"])}{nav(L("lista/"), t["nav_list"])}<a class="exs-btn exs-btn--sm" href="{PLAY}"><span>{t["nav_play"]}</span></a><details class="lang-switch"><summary aria-label="{t["lang_aria"]}: {LANGS[lang]["name"]}"><span lang="{lang}">{LANGS[lang]["short"]}</span></summary><ul>{switch}</ul></details></nav>
</div></header>
<main id="sisalto">
'''
    foot = f'''</main>
<footer class="site-footer"><div class="wrap">
<div class="stack" style="gap: 12px"><a href="https://www.exsports.fi/" aria-label="EXSports Oy"><img class="site-footer__logo" src="/assets/img/exsports-wordmark.png" alt="EXSports Oy"></a><span>{footer_text}</span></div>
<nav aria-label="{t["foot_aria"]}"><span class="footer-legal-links" lang="{legal_language(lang)}">{footer_links(lang, p)}</span><a href="mailto:info@exsports.fi">info@exsports.fi</a></nav>
</div></footer>
</body>
</html>
'''
    out = f"{p}404.html" if is404 else f"{p}{rel}index.html"
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(head + body + foot)


def row(lang, rank, name, tr, score, podium=False, me=False, L=None):
    t = T[lang]
    cls = "exs-row" + (" exs-row--podium" if podium else "") + (" exs-row--me" if me else "")
    href = L("s/?id=esimerkki")
    btn = f'<a class="exs-btn exs-btn--sm" href="{href}"><span>{t["watch"]}</span></a>' if podium else f'<a class="more" href="{href}">{t["watch"]}</a>'
    return (f'<li class="{cls}"><span class="exs-row__rank">{rank}</span><span><span class="exs-row__name">{name}</span>'
            f'<span class="exs-row__trick">{trick(tr, lang)}</span></span><span class="row-actions"><span class="exs-row__score">{score}</span>{btn}</span></li>')


def build_lang(lang):
    t = T[lang]
    p = LANGS[lang]["prefix"]
    L = lambda r: local_link(lang, r)
    R = lambda *a, **k: row(lang, *a, L=L, **k)
    NB = f'<span class="exs-badge">{t["sample"]}</span>'
    li = lambda items: "".join(f"<li>{x}</li>" for x in items)

    # etusivu
    page(lang, "", t["home_title"], t["home_desc"], f'''
<section class="exs-hero" style="background-image: url('/assets/img/backdrop-menu.webp')">
<div class="exs-hero__inner">
<p class="exs-hero__kicker">{t["hero_kicker"]}</p>
<h1 class="exs-hero__title">EXS</h1>
<p class="exs-hero__sub">{t["hero_sub"]}</p>
<p class="exs-hero__lead">{t["hero_lead"]}</p>
<div class="exs-hero__actions"><a class="exs-btn exs-btn--lg" href="{PLAY}"><span>{t["nav_play"]}</span></a><a class="exs-btn exs-btn--secondary" href="{L("nain-pelaat/")}"><span>{t["nav_how"]}</span></a></div>
</div>
</section>
<a href="{L("lista/")}" class="exs-ticker" style="text-decoration: none" aria-label="{t["ticker_aria"]}">
<span class="exs-ticker__title">{t["ticker_title"]}</span>
{'<span class="exs-ticker__dot">·</span>'.join(f'<span class="exs-ticker__item">{r[0]} {r[1]} {r[3]}</span>' for r in ROWS[:5])}
</a>
<section class="section"><div class="wrap">
<div class="section__head"><h2 class="h2">{t["how_h"]}</h2><a class="more" href="{L("nain-pelaat/")}">{t["how_all"]}</a></div>
<div class="grid-3">
<article class="exs-panel exs-panel--quiet"><div class="exs-panel__meta">{t["step1_m"]}</div><h3 class="exs-panel__title">{t["step1_h"]}</h3><p class="prose" style="margin:0">{t["step1_p"]}</p></article>
<article class="exs-panel exs-panel--quiet"><div class="exs-panel__meta">{t["step2_m"]}</div><h3 class="exs-panel__title">{t["step2_h"]}</h3><p class="prose" style="margin:0">{t["step2_p"]}</p></article>
<article class="exs-panel exs-panel--quiet"><div class="exs-panel__meta">{t["step3_m"]}</div><h3 class="exs-panel__title">{t["step3_h"]}</h3><p class="prose" style="margin:0">{t["step3_p"]}</p></article>
</div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap grid-main">
<div class="exs-panel pad-shadow">
<div class="row-between" style="margin-bottom: 24px"><div><div class="exs-panel__meta">{t["top_meta"]}</div><h2 class="exs-panel__title" style="margin: 4px 0 0">{t["top_h"]}</h2></div>{NB}</div>
<ol class="exs-board">{R(*ROWS[0], podium=True)}{R(*ROWS[1], podium=True)}{R(*ROWS[2], podium=True)}</ol>
<div style="margin-top: 24px; display: flex; flex-wrap: wrap; gap: 16px"><a class="exs-btn" href="{L("lista/")}"><span>{t["top_all"]}</span></a><a class="exs-btn exs-btn--secondary" href="{L("s/?id=esimerkki")}"><span>{t["top_first"]}</span></a></div>
</div>
<div class="stack">
<div class="exs-panel exs-panel--quiet"><h3 class="exs-panel__title">{t["slopes_h"]}</h3>
<div class="stack" style="gap: 12px; font-size: 14px; line-height: 20px; color: var(--text-soft)">
<div class="row-between"><span class="display-xs" style="text-transform: uppercase; color: var(--text)">{t["slope_s"]}</span><span>{t["free"]}</span></div>
<div class="row-between"><span class="display-xs" style="text-transform: uppercase; color: var(--text)">{t["slope_m"]}</span><span>{t["free"]}</span></div>
<div class="row-between"><span class="display-xs" style="text-transform: uppercase; color: var(--text)">{t["slope_l"]}</span><span>{t["paid"]}</span></div>
</div></div>
<div class="exs-panel exs-panel--quiet"><h3 class="exs-panel__title">{t["fair_h"]}</h3><p class="prose" style="margin:0; font-size: 14px; line-height: 20px">{t["fair_p"]}</p></div>
</div>
</div></section>
''', L(""))

    # näin pelaat
    lrows = "".join(f"<tr><td>{a}</td><td>{b}</td><td style='color:var(--text)'>{c}</td><td>{d}</td></tr>" for a, b, c, d in t["lessons"])
    cols = "".join(f"<th>{c}</th>" for c in t["lessons_cols"])
    page(lang, "nain-pelaat/", t["how_title"], t["how_desc"], f'''
<section class="section"><div class="wrap">
<div class="kicker">{t["how_kicker"]}</div>
<h1 class="h1" style="margin: 8px 0 24px">{t["how_h1"]}</h1>
<div class="grid-main">
<div class="prose">
<p>{t["how_intro"]}</p>
<h2>{t["start_h"]}</h2>
<ol>{li(t["start_steps"])}</ol>
<h2>{t["controls_h"]}</h2>
<ul>{li(t["controls"])}</ul>
<p>{t["controls_p"]}</p>
<h2>{t["lessons_h"]}</h2>
</div>
<div class="stack">
<div class="exs-panel exs-panel--quiet"><h2 class="exs-panel__title">{t["career_h"]}</h2><p class="prose" style="margin:0 0 12px; font-size:14px; line-height:20px">{t["career_p"]}</p><div class="stack" style="gap: 8px; font-size: 14px; line-height: 20px; color: var(--text-soft)"><div class="row-between"><span class="display-xs" style="text-transform:uppercase;color:var(--text)">{t["slope_s"]}</span><span>{t["career_s"]}</span></div><div class="row-between"><span class="display-xs" style="text-transform:uppercase;color:var(--text)">{t["slope_m"]}</span><span>{t["career_m"]}</span></div><div class="row-between"><span class="display-xs" style="text-transform:uppercase;color:var(--text)">{t["slope_l"]}</span><span>{t["career_l"]}</span></div></div></div>
<div class="exs-panel exs-panel--quiet"><h2 class="exs-panel__title">{t["wr_h"]}</h2><p class="prose" style="margin:0; font-size:14px; line-height:20px">{t["wr_p"].format(list=L("lista/"))}</p></div>
</div>
</div>
<div class="exs-panel pad-shadow" style="margin-top: 32px; overflow-x: auto">
<table class="lessons"><thead><tr>{cols}</tr></thead><tbody>{lrows}</tbody></table>
</div>
</div></section>
''', L("nain-pelaat/"))

    # lista
    page(lang, "lista/", t["list_title"], t["list_desc"], f'''
<section class="section" style="padding-bottom: 0"><div class="wrap" style="display:flex; flex-wrap:wrap; align-items:flex-end; justify-content:space-between; gap: 24px">
<div><div class="kicker">{t["list_kicker"]}</div><h1 class="h1" style="margin: 8px 0 0">{t["list_h1"]}</h1></div>
<div style="display:flex; align-items:center; gap: 24px; flex-wrap: wrap">
<div class="exs-tabs tabs-scroll" role="tablist" aria-label="{t["tabs_aria"]}"><a class="exs-tab" role="tab" aria-selected="true" href="{L("lista/?rinne=s")}"><span>{t["slope_s"]}</span></a><a class="exs-tab" role="tab" aria-selected="false" href="{L("lista/?rinne=m")}"><span>{t["slope_m"]}</span></a><a class="exs-tab" role="tab" aria-selected="false" href="{L("lista/?rinne=l")}"><span>{t["slope_l"]}</span></a></div>
<a class="more" href="{L("lista/?kausi=arkisto")}" style="color: var(--text-soft)">{t["archive"]}</a>
</div>
</div></section>
<section class="section"><div class="wrap grid-main">
<div>
<div class="exs-panel pad-shadow" id="lista" data-rinne="s" data-kausi="kausi-1">
<div class="row-between" style="margin-bottom: 24px"><h2 class="exs-panel__title" style="margin:0">{t["slope_s"]}</h2>{NB}</div>
<ol class="exs-board">{"".join(R(*r, podium=(r[0] <= 3)) for r in ROWS)}</ol>
<div class="row-between" style="margin-top: 24px; align-items:center; flex-wrap: wrap; gap: 12px"><span class="exs-panel__meta">{t["list_rows"]}</span><div style="display:flex; gap: 8px"><a class="exs-btn exs-btn--sm exs-btn--secondary" href="{L("lista/?sivu=1")}" aria-disabled="true"><span>{t["prev"]}</span></a><a class="exs-btn exs-btn--sm exs-btn--secondary" href="{L("lista/?sivu=2")}"><span>{t["next"]}</span></a></div></div>
</div>
</div>
<div class="stack">
<div class="exs-panel pad-shadow" id="omat"><div class="exs-panel__meta">{t["own_meta"]}</div><h2 class="exs-panel__title" style="margin-top: 4px">{t["own_h"]}</h2><p class="prose" style="margin:0 0 16px; font-size:14px; line-height:20px">{t["own_p"]}</p><a class="exs-btn exs-btn--sm exs-btn--secondary" href="{L("tili/")}"><span>{t["own_btn"]}</span></a></div>
<div class="exs-panel exs-panel--quiet"><h2 class="exs-panel__title">{t["rules_h"]}</h2>
<ul class="prose" style="margin:0; font-size:14px; line-height:20px">{li(t["rules"])}</ul>
<div style="margin-top: 16px"><a class="more" href="{L("kayttoehdot/")}">{t["foot_terms"]}</a></div>
</div>
</div>
</div></section>
''', L("lista/"))

    # suoritus
    vals = ["6 240", "4 180", "1 960", "1 420", "1 090", "1 000"]
    cells = "".join(f'<div><div class="exs-score__label">{a}</div><div class="exs-score__value">{b}</div></div>' for a, b in zip(t["score_labels"], vals))
    page(lang, "s/", t["run_title"], t["run_desc"], f'''
<div class="wrap"><nav class="crumbs" aria-label="{t["crumbs_aria"]}"><a href="{L("lista/")}">{t["list_h1"]}</a><span>›</span><span>{t["slope_s"]}</span><span>›</span><span style="color: var(--text)">{t["crumb_rank"]}</span></nav></div>
<section class="section" style="padding-top: 24px"><div class="wrap grid-main">
<div class="stack">
<div class="notice">{t["run_notice"]}</div>
<div class="video pad-shadow" aria-label="{t["video_aria"]}">
<div class="video__badges"><span class="exs-badge exs-badge--verified">{t["verified"]}</span><span class="exs-badge">{t["video_device"]}</span></div>
<button type="button" class="video__play" aria-label="{t["play_aria"]}"><svg width="36" height="36" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4l12 8-12 8z"/></svg></button>
<div class="video__bar"><span class="label" style="text-transform:uppercase;color:var(--text-soft)">0:00 / 0:11</span><div class="video__track"><div class="video__fill"></div></div><span class="label" style="text-transform:uppercase;color:var(--text-soft)">{t["video_speed"]}</span></div>
</div>
<section class="exs-panel pad-shadow">
<div class="row-between" style="flex-wrap: wrap"><h1 class="exs-panel__title" style="margin:0">Riikka_fin <span style="color: var(--accent); font-size: 20px">BS 540 + Indy</span></h1><span class="exs-panel__meta">{t["run_meta"]}</span></div>
<div class="exs-total" style="margin-top: 16px"><span class="exs-total__label">{t["total"]}</span><span class="exs-total__value">15 890</span><span class="exs-total__pb">{t["rank1"]}</span></div>
<div class="exs-score">{cells}</div>
<div class="exs-callout" style="margin-top: 24px">{t["coach"]}</div>
</section>
</div>
<div class="stack">
<div class="exs-panel pad-shadow"><h2 class="exs-panel__title">{t["share_h"]}</h2><p class="prose" style="margin:0 0 16px; font-size:14px; line-height:20px">{t["share_p"]}</p><div class="linkbox">worldtour.exsports.fi{L("s/?id=esimerkki")}</div><div style="margin-top: 16px; display:flex; gap: 12px; flex-wrap: wrap"><button type="button" class="exs-btn exs-btn--sm" data-copy data-copied="{t["meta"]["copied"]}"><span>{t["copy"]}</span></button><a class="exs-btn exs-btn--sm exs-btn--secondary" href="#" aria-disabled="true"><span>{t["download"]}</span></a></div></div>
<div class="exs-panel exs-panel--quiet"><h2 class="exs-panel__title">Riikka_fin</h2><div class="stack" style="gap: 8px; font-size: 14px; line-height: 20px; color: var(--text-soft)"><div class="row-between"><span>{t["slope_s"]}</span><span class="display-xs" style="color: var(--text)">1 · 15 890</span></div><div class="row-between"><span>{t["slope_m"]}</span><span class="display-xs" style="color: var(--text)">4 · 21 330</span></div><div class="row-between"><span>{t["slope_l"]}</span><span class="display-xs" style="color: var(--text)">2 · 27 110</span></div></div></div>
<div class="exs-panel exs-panel--quiet"><h2 class="exs-panel__title">{t["how_scored_h"]}</h2><p class="prose" style="margin:0; font-size:14px; line-height:20px">{t["how_scored_p"]}</p><div style="margin-top: 16px"><a class="more" href="mailto:info@exsports.fi?subject={t["report_subject"]}" style="color: var(--muted)">{t["report"]}</a></div></div>
</div>
</div></section>
''', L("lista/"))

    # oikeudelliset sivut
    for slug in LEGAL_SLUGS:
        title, desc, body = render_document(lang, slug, p)
        page(lang, f"{slug}/", f"{title} – EXS World Tour", desc, body, L(f"{slug}/"))

    page(lang, "404", t["nf_title"], t["nf_desc"],
         f'''<section class="section"><div class="wrap"><div class="kicker">404</div><h1 class="h1" style="margin: 8px 0 24px">{t["nf_h"]}</h1><p class="prose">{t["nf_p"].format(home=L(""), list=L("lista/"))}</p></div></section>''', "")


def sitemap():
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for rel in PAGES:
        if rel == "s/":
            continue
        for lang in LANGS:
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{SITE}/{LANGS[l]["prefix"]}{rel}"/>' for l in LANGS)
            out.append(f'  <url><loc>{SITE}/{LANGS[lang]["prefix"]}{rel}</loc>{alts}</url>')
    out.append('</urlset>')
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for lang in LANGS:
        build_lang(lang)
    sitemap()
    print("sivut:", ", ".join(LANGS))
