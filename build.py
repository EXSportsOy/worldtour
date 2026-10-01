import os
SITE="https://worldtour.exsports.fi"
def page(path,title,desc,body,current,og=None):
    url=SITE+path
    def nav(href,label):
        cur=' aria-current="page"' if href==current else ''
        return f'<a href="{href}"{cur}>{label}</a>'
    head=f'''<!doctype html>
<html lang="fi" data-theme="viimeinen-valo">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="EXS World Tour">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0c1426">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; font-src 'self'; script-src 'self'; connect-src 'self'; base-uri 'self'; form-action 'self'">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/BarlowCondensed-ExtraBoldItalic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/tokens.css">
<link rel="stylesheet" href="/assets/css/bundle.css">
<link rel="stylesheet" href="/assets/css/site.css">
<script src="/assets/js/site.js" defer></script>
</head>
<body class="exs">
<a class="skip" href="#sisalto">Siirry sisältöön</a>
<header class="site-header"><div class="wrap">
<a class="brand" href="/" aria-label="EXS World Tour, etusivu"><span class="brand__exs">EXS</span><span class="brand__bar"></span><span class="brand__wt">World Tour</span></a>
<nav class="site-nav" aria-label="Päävalikko">{nav("/nain-pelaat/","Näin pelaat")}{nav("/lista/","Maailmanlista")}<a class="exs-btn exs-btn--sm" href="https://play.google.com/store/apps/details?id=fi.exsports.exsworldtour"><span>Hae Playsta</span></a></nav>
</div></header>
<main id="sisalto">
'''
    foot='''</main>
<footer class="site-footer"><div class="wrap">
<div class="stack" style="gap: 12px"><a href="https://www.exsports.fi/" aria-label="EXSports Oy"><img class="site-footer__logo" src="/assets/img/exsports-wordmark.png" alt="EXSports Oy"></a><span>EXS World Tour on EXSports Oy:n peli Androidille. S- ja M-rinteet ovat ilmaisia, L-rinne maksaa 1,95 €.</span></div>
<nav aria-label="Alatunniste"><a href="/kayttoehdot/">Käyttöehdot</a><a href="/tietosuoja/">Tietosuoja</a><a href="/tili/">Tilin poisto</a><a href="mailto:info@exsports.fi">info@exsports.fi</a></nav>
</div></footer>
</body>
</html>
'''
    os.makedirs(os.path.dirname("."+path+"index.html") or ".",exist_ok=True)
    open("."+path+"index.html","w").write(head+body+foot)

def row(rank,name,trick,score,podium=False,me=False):
    cls="exs-row"+(" exs-row--podium" if podium else "")+(" exs-row--me" if me else "")
    btn=f'<a class="exs-btn exs-btn--sm" href="/s/?id=esimerkki"><span>Katso</span></a>' if podium else f'<a class="more" href="/s/?id=esimerkki">Katso</a>'
    return f'<li class="{cls}"><span class="exs-row__rank">{rank}</span><span><span class="exs-row__name">{name}</span><span class="exs-row__trick">{trick}</span></span><span class="row-actions"><span class="exs-row__score">{score}</span>{btn}</span></li>'

ROWS=[(1,"Riikka_fin","BS 540 + Indy","15 890"),(2,"Snowdog","Etuvoltti 360 + Nose","15 660"),(3,"Kaamos","FS 540","15 020"),(4,"Aino","Takavoltti 360","14 780"),(5,"Pihla","FS 360 + Indy","14 310"),(6,"Eero","BS 360 + Weddle","13 960"),(7,"Noora","Shifty","13 420"),(8,"Jussi","BS 360","12 980"),(9,"Liisa","Suora hyppy","12 640"),(10,"Oskari","FS 180","12 100"),(11,"Mea","Etuvoltti 360","11 870"),(12,"Saku","BS 540","11 540")]
NB=lambda: '<span class="exs-badge">Esimerkkidata</span>'
PLAY="https://play.google.com/store/apps/details?id=fi.exsports.exsworldtour"

# ---------- Etusivu
page("/","EXS World Tour – lumilautapeli, jossa puhtaus ratkaisee","Big Air -lumilautapeli Androidille. Opi temput, katso maailman parhaat suoritukset ja tavoittele omaa paikkaa maailmanlistalla.",f'''
<section class="exs-hero" style="background-image: url('/assets/img/backdrop-menu.webp')">
<div class="exs-hero__inner">
<p class="exs-hero__kicker">Big Air · World Tour</p>
<h1 class="exs-hero__title">EXS</h1>
<p class="exs-hero__sub">World Tour</p>
<p class="exs-hero__lead">Mitä puhtaampi suoritus, sitä enemmän pisteitä. Lumilautapeli, jossa temppu lasketaan pisteiksi liikkeestä, ei napin painalluksesta.</p>
<div class="exs-hero__actions"><a class="exs-btn exs-btn--lg" href="{PLAY}"><span>Hae Playsta</span></a><a class="exs-btn exs-btn--secondary" href="/nain-pelaat/"><span>Näin pelaat</span></a></div>
</div>
</section>
<a href="/lista/" class="exs-ticker" style="text-decoration: none" aria-label="Maailmanlistan kärki, Pieni S">
<span class="exs-ticker__title">Maailmanlista · Pieni S</span>
<span class="exs-ticker__item">1 Riikka_fin 15 890</span><span class="exs-ticker__dot">·</span>
<span class="exs-ticker__item">2 Snowdog 15 660</span><span class="exs-ticker__dot">·</span>
<span class="exs-ticker__item">3 Kaamos 15 020</span><span class="exs-ticker__dot">·</span>
<span class="exs-ticker__item">4 Aino 14 780</span><span class="exs-ticker__dot">·</span>
<span class="exs-ticker__item">5 Pihla 14 310</span>
</a>
<section class="section"><div class="wrap">
<div class="section__head"><h2 class="h2">Näin se toimii</h2><a class="more" href="/nain-pelaat/">Koko ohje</a></div>
<div class="grid-3">
<article class="exs-panel exs-panel--quiet"><div class="exs-panel__meta">1 · Vauhdinotto</div><h3 class="exs-panel__title">Ponnista lipistä</h3><p class="prose" style="margin:0">Kyykkyyn vauhdinotossa, ponnistus lipin kohdalla. Ajoitus ratkaisee korkeuden, ja korkeus antaa aikaa tempulle.</p></article>
<article class="exs-panel exs-panel--quiet"><div class="exs-panel__meta">2 · Lento</div><h3 class="exs-panel__title">Kierrä ja ota ote</h3><p class="prose" style="margin:0">Kierre ja voltti omilla säätimillään, ote napista: Nose, Tail, Indy tai Weddle. Pidä ote vähintään 0,2 sekuntia ja irrota ennen lunta.</p></article>
<article class="exs-panel exs-panel--quiet"><div class="exs-panel__meta">3 · Alastulo</div><h3 class="exs-panel__title">Laskeudu puhtaasti</h3><p class="prose" style="margin:0">Lauta suoraan ja kierto valmiina ennen lunta. Clean-alastulo kertoo pisteet, kaatuminen nollaa ne.</p></article>
</div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap grid-main">
<div class="exs-panel pad-shadow">
<div class="row-between" style="margin-bottom: 24px"><div><div class="exs-panel__meta">Kausi 1 · Pieni S</div><h2 class="exs-panel__title" style="margin: 4px 0 0">Kärki juuri nyt</h2></div>{NB()}</div>
<ol class="exs-board">{row(*ROWS[0],podium=True)}{row(*ROWS[1],podium=True)}{row(*ROWS[2],podium=True)}</ol>
<div style="margin-top: 24px; display: flex; flex-wrap: wrap; gap: 16px"><a class="exs-btn" href="/lista/"><span>Koko maailmanlista</span></a><a class="exs-btn exs-btn--secondary" href="/s/?id=esimerkki"><span>Katso ykkössuoritus</span></a></div>
</div>
<div class="stack">
<div class="exs-panel exs-panel--quiet"><h3 class="exs-panel__title">Kolme rinnettä</h3>
<div class="stack" style="gap: 12px; font-size: 14px; line-height: 20px; color: var(--text-soft)">
<div class="row-between"><span class="display-xs" style="text-transform: uppercase; color: var(--text)">Pieni S</span><span>Ilmainen</span></div>
<div class="row-between"><span class="display-xs" style="text-transform: uppercase; color: var(--text)">Keski M</span><span>Ilmainen</span></div>
<div class="row-between"><span class="display-xs" style="text-transform: uppercase; color: var(--text)">Iso L</span><span>Kertaosto 1,95 €</span></div>
</div></div>
<div class="exs-panel exs-panel--quiet"><h3 class="exs-panel__title">Reilu lista</h3><p class="prose" style="margin:0; font-size: 14px; line-height: 20px">Jokainen tulos lasketaan uudelleen palvelimella pelaajan syötteistä. Pelin näyttämä luku ei riitä, ja jokainen listasuoritus on katsottavissa.</p></div>
</div>
</div></section>
''',"/")

# ---------- Näin pelaat
lessons=[("1","S","Lasku ja alastulo","Paina Lähde ja seuraa hyppyä valmiilla lähtöasetuksilla."),("2","S","Ponnistus","Paina Ponnista lähellä reunaa ja vapauta ohjeen mukaan."),("3","S","Ote","Pidä Indy ilmassa ja irrota ennen maata."),("4","S","Hyppy + Indy","Yhdistä ajoitettu ponnistus ja Indy-ote."),("5","M","Etuvoltti + Nose","Säädä etuvoltti; pidä Nose ilmassa ja irrota ennen maata."),("6","M","FS 360 + Indy","Säädä FS 360; pidä Indy ja irrota ennen maata."),("7","M","FS 180 + Indy","Tee puoli kierrosta FS-suuntaan, pidä Indy ja suuntaa alastulo pienellä vastakierteellä.")]
lrows="".join(f"<tr><td>{a}</td><td>{b}</td><td style='color:var(--text)'>{c}</td><td>{d}</td></tr>" for a,b,c,d in lessons)
page("/nain-pelaat/","Näin pelaat – EXS World Tour","Aloittaminen, ohjaimet, ponnistus, otteet ja alastulo. Tutoriaalin seitsemän vaihetta ja rataura.",f'''
<section class="section"><div class="wrap">
<div class="kicker">Ohje</div>
<h1 class="h1" style="margin: 8px 0 24px">Näin pelaat</h1>
<div class="grid-main">
<div class="prose">
<p>Peli alkaa tutoriaalista, joka opettaa laskun, ponnistuksen, otteen ja ensimmäiset temput seitsemässä vaiheessa. Tutoriaali käyttää S- ja M-hyppyreitä, ja sen jälkeen avautuu rataura.</p>
<h2>Aloittaminen</h2>
<ol>
<li>Valitse päävalikosta <strong>Tutoriaali</strong>.</li>
<li>Valitse vuorossa oleva harjoitus ja lue <strong>Tee näin</strong> sekä <strong>Miksi?</strong>.</li>
<li><strong>Katso esimerkki</strong> näyttää saman tehtävän syötteet. Katselu ei anna suorituksia.</li>
<li>Aloita harjoitus ja paina rinteessä <strong>Lähde</strong>. Vaiheissa 5–7 säädä voltti tai kierre ennen lähtöä.</li>
<li>Onnistuminen tallentuu ennen seuraavaa tehtävää. Valmiita tehtäviä voi kerrata.</li>
</ol>
<h2>Ohjaimet</h2>
<ul>
<li><strong>Kyykky</strong> vauhdinotossa: säädin vasemmalla, täyttö kertoo painuman.</li>
<li><strong>Ponnista</strong> lähellä lippiä. Ajoitus näkyy lennossa palautteena, täydellinen ponnistus on PERFECT.</li>
<li><strong>Kierre ja voltti</strong> omilla säätimillään. Suunta FS tai BS, määrä 180° askelin.</li>
<li><strong>Otteet</strong> Nose, Tail, Indy ja Weddle ovat nappeja lennon aikana. Ote tarvitsee vähintään 0,2 sekunnin pidon, ja pitoaika vaikuttaa pyörimiseen.</li>
<li><strong>Alastulo</strong> on Clean, Sketchy tai kaatuminen. Irrota ote ennen lunta.</li>
</ul>
<p>Pelaa-tilassa jokainen hyppy alkaa nollatuilla säädöillä. Hahmo lähtee liikkeelle heti, kun kosketat mitä tahansa lähtönäkymän säädintä.</p>
<h2>Tutoriaalin seitsemän vaihetta</h2>
</div>
<div class="stack">
<div class="exs-panel exs-panel--quiet"><h2 class="exs-panel__title">Rataura</h2><p class="prose" style="margin:0 0 12px; font-size:14px; line-height:20px">Tutoriaalin jälkeen <strong>Pelaa</strong> avaa uran. S-rinteen neljä tehtävää avaavat M-rinteen, ja M-rinteen kuusi tehtävää avaavat L-rinteen tehtävät.</p><div class="stack" style="gap: 8px; font-size: 14px; line-height: 20px; color: var(--text-soft)"><div class="row-between"><span class="display-xs" style="text-transform:uppercase;color:var(--text)">Pieni S</span><span>4 tehtävää · ilmainen</span></div><div class="row-between"><span class="display-xs" style="text-transform:uppercase;color:var(--text)">Keski M</span><span>6 tehtävää · ilmainen</span></div><div class="row-between"><span class="display-xs" style="text-transform:uppercase;color:var(--text)">Iso L</span><span>10 tehtävää · 1,95 €</span></div></div></div>
<div class="exs-panel exs-panel--quiet"><h2 class="exs-panel__title">Maailmanlista</h2><p class="prose" style="margin:0; font-size:14px; line-height:20px">Kun tulos on sinusta valmis listalle, lähetä se pelin tuloskortista. Palvelin laskee pisteet uudelleen syötteistäsi, ja varmennettu tulos näkyy <a href="/lista/">maailmanlistalla</a> nimimerkilläsi.</p></div>
</div>
</div>
<div class="exs-panel pad-shadow" style="margin-top: 32px; overflow-x: auto">
<table class="lessons"><thead><tr><th>#</th><th>Hyppyri</th><th>Harjoitus</th><th>Tee näin</th></tr></thead><tbody>{lrows}</tbody></table>
</div>
</div></section>
''',"/nain-pelaat/")

# ---------- Maailmanlista
page("/lista/","Maailmanlista – EXS World Tour","Maailman parhaat suoritukset S-, M- ja L-rinteillä. Jokainen tulos on palvelimen varmentama.",f'''
<section class="section" style="padding-bottom: 0"><div class="wrap" style="display:flex; flex-wrap:wrap; align-items:flex-end; justify-content:space-between; gap: 24px">
<div><div class="kicker">Kausi 1</div><h1 class="h1" style="margin: 8px 0 0">Maailmanlista</h1></div>
<div style="display:flex; align-items:center; gap: 24px; flex-wrap: wrap">
<div class="exs-tabs tabs-scroll" role="tablist" aria-label="Rinne"><a class="exs-tab" role="tab" aria-selected="true" href="/lista/?rinne=s"><span>Pieni S</span></a><a class="exs-tab" role="tab" aria-selected="false" href="/lista/?rinne=m"><span>Keski M</span></a><a class="exs-tab" role="tab" aria-selected="false" href="/lista/?rinne=l"><span>Iso L</span></a></div>
<a class="more" href="/lista/?kausi=arkisto" style="color: var(--text-soft)">Arkisto</a>
</div>
</div></section>
<section class="section"><div class="wrap grid-main">
<div>
<div class="exs-panel pad-shadow" id="lista" data-rinne="s" data-kausi="kausi-1">
<div class="row-between" style="margin-bottom: 24px"><h2 class="exs-panel__title" style="margin:0">Pieni S</h2>{NB()}</div>
<ol class="exs-board">{"".join(row(*r,podium=(r[0]<=3)) for r in ROWS)}</ol>
<div class="row-between" style="margin-top: 24px; align-items:center; flex-wrap: wrap; gap: 12px"><span class="exs-panel__meta">Rivit 1–12 · yksi tulos per pelaaja</span><div style="display:flex; gap: 8px"><a class="exs-btn exs-btn--sm exs-btn--secondary" href="/lista/?sivu=1" aria-disabled="true"><span>Edellinen</span></a><a class="exs-btn exs-btn--sm exs-btn--secondary" href="/lista/?sivu=2"><span>Seuraava</span></a></div></div>
</div>
<div class="pinned pad-shadow" id="oma-rivi" hidden>
<ol class="exs-board"><li class="exs-row exs-row--me"><span class="exs-row__rank">38</span><span><span class="exs-row__name">Sinä</span><span class="exs-row__trick">BS 360 + Weddle</span></span><span class="row-actions"><span class="exs-row__score">10 980</span><a class="more" href="/s/?id=esimerkki">Katso</a></span></li></ol>
</div>
</div>
<div class="stack">
<div class="exs-panel pad-shadow" id="omat"><div class="exs-panel__meta">Omat ennätykset</div><h2 class="exs-panel__title" style="margin-top: 4px">Kirjaudu nähdäksesi</h2><p class="prose" style="margin:0 0 16px; font-size:14px; line-height:20px">Kirjautuminen Google-tilillä avautuu, kun testikausi alkaa. Tulosten lähettämiseen tarvitset tilin ja nimimerkin.</p><a class="exs-btn exs-btn--sm exs-btn--secondary" href="/tili/"><span>Tilistä</span></a></div>
<div class="exs-panel exs-panel--quiet"><h2 class="exs-panel__title">Säännöt lyhyesti</h2>
<ul class="prose" style="margin:0; font-size:14px; line-height:20px">
<li>Yksi paras tulos pelaajaa kohden kullakin rinteellä.</li>
<li>Palvelin laskee pisteet uudelleen syötteistä. Vain varmennetut tulokset näkyvät.</li>
<li>Vain Google Playsta asennettu Android-peli kelpaa.</li>
<li>Kauden vaihtuessa lista alkaa tyhjästä ja vanha kausi siirtyy arkistoon.</li>
</ul>
<div style="margin-top: 16px"><a class="more" href="/kayttoehdot/">Käyttöehdot</a></div>
</div>
</div>
</div></section>
''',"/lista/")

# ---------- Suoritus
cells="".join(f'<div><div class="exs-score__label">{a}</div><div class="exs-score__value">{b}</div></div>' for a,b in [("Amplitudi","6 240"),("Rotaatio","4 180"),("Grab","1 960"),("Tasapaino","1 420"),("Tyyli","1 090"),("Stomp","1 000")])
page("/s/","Suoritus – EXS World Tour","Palvelimen varmentama suoritus EXS World Tourin maailmanlistalta.",f'''
<div class="wrap"><nav class="crumbs" aria-label="Murupolku"><a href="/lista/">Maailmanlista</a><span>›</span><span>Pieni S</span><span>›</span><span style="color: var(--text)">Sija 1</span></nav></div>
<section class="section" style="padding-top: 24px"><div class="wrap grid-main">
<div class="stack">
<div class="notice">Esimerkkisivu. Oikeat suoritukset avautuvat osoitteesta <strong>worldtour.exsports.fi/s/&lt;tunnus&gt;</strong>, kun testikausi alkaa.</div>
<div class="video pad-shadow" aria-label="Suorituksen video">
<div class="video__badges"><span class="exs-badge exs-badge--verified">Varmennettu</span><span class="exs-badge">Video laitteelta</span></div>
<button type="button" class="video__play" aria-label="Toista video"><svg width="36" height="36" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4l12 8-12 8z"/></svg></button>
<div class="video__bar"><span class="label" style="text-transform:uppercase;color:var(--text-soft)">0:00 / 0:11</span><div class="video__track"><div class="video__fill"></div></div><span class="label" style="text-transform:uppercase;color:var(--text-soft)">0,5×</span></div>
</div>
<section class="exs-panel pad-shadow">
<div class="row-between" style="flex-wrap: wrap"><h1 class="exs-panel__title" style="margin:0">Riikka_fin <span style="color: var(--accent); font-size: 20px">BS 540 + Indy</span></h1><span class="exs-panel__meta">Pieni S · kausi 1 · 3.10.2026</span></div>
<div class="exs-total" style="margin-top: 16px"><span class="exs-total__label">Yhteensä</span><span class="exs-total__value">15 890</span><span class="exs-total__pb">Sija 1</span></div>
<div class="exs-score">{cells}</div>
<div class="exs-callout" style="margin-top: 24px">Kierre 2° vajaa · Ote koko lennon · Ponnistus täydellinen · Puhdas stomp</div>
</section>
</div>
<div class="stack">
<div class="exs-panel pad-shadow"><h2 class="exs-panel__title">Jaa suoritus</h2><p class="prose" style="margin:0 0 16px; font-size:14px; line-height:20px">Linkki aukeaa ilman peliä ja kirjautumista.</p><div class="linkbox">worldtour.exsports.fi/s/esimerkki</div><div style="margin-top: 16px; display:flex; gap: 12px; flex-wrap: wrap"><button type="button" class="exs-btn exs-btn--sm" data-copy><span>Kopioi linkki</span></button><a class="exs-btn exs-btn--sm exs-btn--secondary" href="#" aria-disabled="true"><span>Lataa video</span></a></div></div>
<div class="exs-panel exs-panel--quiet"><h2 class="exs-panel__title">Riikka_fin</h2><div class="stack" style="gap: 8px; font-size: 14px; line-height: 20px; color: var(--text-soft)"><div class="row-between"><span>Pieni S</span><span class="display-xs" style="color: var(--text)">1 · 15 890</span></div><div class="row-between"><span>Keski M</span><span class="display-xs" style="color: var(--text)">4 · 21 330</span></div><div class="row-between"><span>Iso L</span><span class="display-xs" style="color: var(--text)">2 · 27 110</span></div></div></div>
<div class="exs-panel exs-panel--quiet"><h2 class="exs-panel__title">Miten pisteet syntyvät</h2><p class="prose" style="margin:0; font-size:14px; line-height:20px">Palvelin ajoi pelaajan syötteet uudelleen ja laski pisteet itse. Video on tehty pelaajan laitteella samasta hypystä.</p><div style="margin-top: 16px"><a class="more" href="mailto:info@exsports.fi?subject=Ilmoitus%20suorituksesta" style="color: var(--muted)">Ilmoita suoritus</a></div></div>
</div>
</div></section>
''',"/lista/")

# ---------- Käyttöehdot, tietosuoja, tili
def simple(path,title,kicker,h1,inner,desc):
    page(path,title+" – EXS World Tour",desc,f'''<section class="section"><div class="wrap"><div class="kicker">{kicker}</div><h1 class="h1" style="margin: 8px 0 24px">{h1}</h1><div class="prose">{inner}</div></div></section>''',path)
simple("/kayttoehdot/","Käyttöehdot","World Rank","Käyttöehdot",'''<div class="notice" style="margin-bottom: 24px">Käyttöehdot julkaistaan tällä sivulla ennen testikauden alkua. Alla on tiivistelmä periaatteista.</div>
<ul><li>Maailmanlistalle osallistuminen vaatii 13 vuoden iän ja Google-tilin. Pelaaminen ilman tiliä on aina mahdollista.</li><li>Nimimerkki on julkinen. Loukkaava, toisena esiintyvä tai henkilötietoja sisältävä nimimerkki vaihdetaan, ja toistuva rikkomus johtaa lähetyskieltoon.</li><li>Listalle kelpaa vain itse pelattu suoritus muokkaamattomalla pelillä. Palvelin laskee jokaisen tuloksen uudelleen.</li><li>Testikausi päättyy pelin julkaisuun, ja listat alkavat silloin tyhjästä.</li></ul>
<p>Kysymykset: <a href="mailto:info@exsports.fi">info@exsports.fi</a></p>''',"EXS World Tourin maailmanlistan käyttöehdot.")
simple("/tietosuoja/","Tietosuoja","Henkilötiedot","Tietosuojaseloste",'''<div class="notice" style="margin-bottom: 24px">Tietosuojaseloste julkaistaan tällä sivulla ennen testikauden alkua.</div>
<p>Rekisterinpitäjä on EXSports Oy. Maailmanlistaa varten käsitellään Google-tilin tunniste, nimimerkki, lähetetyt suoritukset ja niiden tiedot. Tiedot tallennetaan Google Firebase -palveluun EU:n alueelle. Julkisesti näkyy vain nimimerkki ja suoritus.</p>
<p>Pelitestin telemetriaa koskeva seloste on pelin hyväksyntäruudussa. Yhteys: <a href="mailto:info@exsports.fi">info@exsports.fi</a></p>''',"EXS World Tourin tietosuojaseloste.")
simple("/tili/","Tilin poisto","Tili","Tili ja tilin poisto",'''<p>Maailmanlistan tili luodaan Google-tilillä pelissä tai tällä sivustolla, kun testikausi alkaa. Tilin voi poistaa pelin asetuksista tai tältä sivulta kirjautumalla sisään. Poisto poistaa nimimerkin, tulokset, toistot ja videot.</p>
<div class="notice">Kirjautuminen ja tilin poisto avautuvat tähän, kun palvelu on käytössä. Siihen asti pyynnöt: <a href="mailto:info@exsports.fi?subject=Tilin%20poisto">info@exsports.fi</a></div>''',"EXS World Tourin tilin poisto.")

# 404
page("/404/","Sivua ei löytynyt – EXS World Tour","Sivua ei löytynyt.",'''<section class="section"><div class="wrap"><div class="kicker">404</div><h1 class="h1" style="margin: 8px 0 24px">Kaatui</h1><p class="prose">Sivua ei löytynyt. Palaa <a href="/">etusivulle</a> tai <a href="/lista/">maailmanlistalle</a>.</p></div></section>''',"")
os.rename("404/index.html","404.html"); os.rmdir("404")
