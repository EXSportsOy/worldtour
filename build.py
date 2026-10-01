"""Tuottaa sivuston HTML-sivut. Aja: python build.py

Rakenne on yhteinen kaikille kielille; tekstit tulevat kielikohtaisesta sanastosta (T).
Suomi on juuressa (/), muut kielet omassa kansiossaan (/en/). Uusi kieli lisätään
LANGS-taulukkoon ja sanastoon, muuta ei tarvitse muuttaa.
"""
import os

SITE = "https://worldtour.exsports.fi"
PLAY = "https://play.google.com/store/apps/details?id=fi.exsports.exsworldtour"
PAGES = ["", "nain-pelaat/", "lista/", "s/", "kayttoehdot/", "tietosuoja/", "tili/"]

LANGS = {
    "fi": {"prefix": "", "name": "Suomi", "short": "FI"},
    "en": {"prefix": "en/", "name": "English", "short": "EN"},
}

ROWS = [(1, "Riikka_fin", "BS 540 + Indy", "15 890"), (2, "Snowdog", "Etuvoltti 360 + Nose", "15 660"),
        (3, "Kaamos", "FS 540", "15 020"), (4, "Aino", "Takavoltti 360", "14 780"), (5, "Pihla", "FS 360 + Indy", "14 310"),
        (6, "Eero", "BS 360 + Weddle", "13 960"), (7, "Noora", "Shifty", "13 420"), (8, "Jussi", "BS 360", "12 980"),
        (9, "Liisa", "Suora hyppy", "12 640"), (10, "Oskari", "FS 180", "12 100"), (11, "Mea", "Etuvoltti 360", "11 870"),
        (12, "Saku", "BS 540", "11 540")]

TRICK_EN = {"Etuvoltti": "Front flip", "Takavoltti": "Back flip", "Suora hyppy": "Straight air"}

# ---------------------------------------------------------------- sanasto
T = {}
T["fi"] = dict(
    lang="fi", skip="Siirry sisältöön", brand_aria="EXS World Tour, etusivu", nav_aria="Päävalikko", lang_aria="Kieli",
    nav_how="Näin pelaat", nav_list="Maailmanlista", nav_play="Hae Playsta", foot_aria="Alatunniste",
    foot_text="EXS World Tour on EXSports Oy:n peli Androidille. S- ja M-rinteet ovat ilmaisia, L-rinne maksaa 1,95 €.",
    foot_terms="Käyttöehdot", foot_privacy="Tietosuoja", foot_account="Tilin poisto",
    sample="Esimerkkidata", watch="Katso", prev="Edellinen", next="Seuraava", verified="Varmennettu",
    # etusivu
    home_title="EXS World Tour – lumilautapeli, jossa puhtaus ratkaisee",
    home_desc="Big Air -lumilautapeli Androidille. Opi temput, katso maailman parhaat suoritukset ja tavoittele omaa paikkaa maailmanlistalla.",
    hero_kicker="Big Air · World Tour", hero_sub="World Tour",
    hero_lead="Mitä puhtaampi suoritus, sitä enemmän pisteitä. Lumilautapeli, jossa temppu lasketaan pisteiksi liikkeestä, ei napin painalluksesta.",
    ticker_title="Maailmanlista · Pieni S", ticker_aria="Maailmanlistan kärki, Pieni S",
    how_h="Näin se toimii", how_all="Koko ohje",
    step1_m="1 · Vauhdinotto", step1_h="Ponnista lipistä", step1_p="Kyykkyyn vauhdinotossa, ponnistus lipin kohdalla. Ajoitus ratkaisee korkeuden, ja korkeus antaa aikaa tempulle.",
    step2_m="2 · Lento", step2_h="Kierrä ja ota ote", step2_p="Kierre ja voltti omilla säätimillään, ote napista: Nose, Tail, Indy tai Weddle. Pidä ote vähintään 0,2 sekuntia ja irrota ennen lunta.",
    step3_m="3 · Alastulo", step3_h="Laskeudu puhtaasti", step3_p="Lauta suoraan ja kierto valmiina ennen lunta. Clean-alastulo kertoo pisteet, kaatuminen nollaa ne.",
    top_meta="Kausi 1 · Pieni S", top_h="Kärki juuri nyt", top_all="Koko maailmanlista", top_first="Katso ykkössuoritus",
    slopes_h="Kolme rinnettä", slope_s="Pieni S", slope_m="Keski M", slope_l="Iso L", free="Ilmainen", paid="Kertaosto 1,95 €",
    fair_h="Reilu lista", fair_p="Jokainen tulos lasketaan uudelleen palvelimella pelaajan syötteistä. Pelin näyttämä luku ei riitä, ja jokainen listasuoritus on katsottavissa.",
    # näin pelaat
    how_title="Näin pelaat – EXS World Tour", how_desc="Aloittaminen, ohjaimet, ponnistus, otteet ja alastulo. Tutoriaalin seitsemän vaihetta ja rataura.",
    how_kicker="Ohje", how_h1="Näin pelaat",
    how_intro="Peli alkaa tutoriaalista, joka opettaa laskun, ponnistuksen, otteen ja ensimmäiset temput seitsemässä vaiheessa. Tutoriaali käyttää S- ja M-hyppyreitä, ja sen jälkeen avautuu rataura.",
    start_h="Aloittaminen",
    start_steps=["Valitse päävalikosta <strong>Tutoriaali</strong>.", "Valitse vuorossa oleva harjoitus ja lue <strong>Tee näin</strong> sekä <strong>Miksi?</strong>.",
                 "<strong>Katso esimerkki</strong> näyttää saman tehtävän syötteet. Katselu ei anna suorituksia.",
                 "Aloita harjoitus ja paina rinteessä <strong>Lähde</strong>. Vaiheissa 5–7 säädä voltti tai kierre ennen lähtöä.",
                 "Onnistuminen tallentuu ennen seuraavaa tehtävää. Valmiita tehtäviä voi kerrata."],
    controls_h="Ohjaimet",
    controls=["<strong>Kyykky</strong> vauhdinotossa: säädin vasemmalla, täyttö kertoo painuman.",
              "<strong>Ponnista</strong> lähellä lippiä. Ajoitus näkyy lennossa palautteena, täydellinen ponnistus on PERFECT.",
              "<strong>Kierre ja voltti</strong> omilla säätimillään. Suunta FS tai BS, määrä 180° askelin.",
              "<strong>Otteet</strong> Nose, Tail, Indy ja Weddle ovat nappeja lennon aikana. Ote tarvitsee vähintään 0,2 sekunnin pidon, ja pitoaika vaikuttaa pyörimiseen.",
              "<strong>Alastulo</strong> on Clean, Sketchy tai kaatuminen. Irrota ote ennen lunta."],
    controls_p="Pelaa-tilassa jokainen hyppy alkaa nollatuilla säädöillä. Hahmo lähtee liikkeelle heti, kun kosketat mitä tahansa lähtönäkymän säädintä.",
    lessons_h="Tutoriaalin seitsemän vaihetta", lessons_cols=["#", "Hyppyri", "Harjoitus", "Tee näin"],
    lessons=[("1", "S", "Lasku ja alastulo", "Paina Lähde ja seuraa hyppyä valmiilla lähtöasetuksilla."),
             ("2", "S", "Ponnistus", "Paina Ponnista lähellä reunaa ja vapauta ohjeen mukaan."),
             ("3", "S", "Ote", "Pidä Indy ilmassa ja irrota ennen maata."),
             ("4", "S", "Hyppy + Indy", "Yhdistä ajoitettu ponnistus ja Indy-ote."),
             ("5", "M", "Etuvoltti + Nose", "Säädä etuvoltti; pidä Nose ilmassa ja irrota ennen maata."),
             ("6", "M", "FS 360 + Indy", "Säädä FS 360; pidä Indy ja irrota ennen maata."),
             ("7", "M", "FS 180 + Indy", "Tee puoli kierrosta FS-suuntaan, pidä Indy ja suuntaa alastulo pienellä vastakierteellä.")],
    career_h="Rataura", career_p="Tutoriaalin jälkeen <strong>Pelaa</strong> avaa uran. S-rinteen neljä tehtävää avaavat M-rinteen, ja M-rinteen kuusi tehtävää avaavat L-rinteen tehtävät.",
    career_s="4 tehtävää · ilmainen", career_m="6 tehtävää · ilmainen", career_l="10 tehtävää · 1,95 €",
    wr_h="Maailmanlista", wr_p="Kun tulos on sinusta valmis listalle, lähetä se pelin tuloskortista. Palvelin laskee pisteet uudelleen syötteistäsi, ja varmennettu tulos näkyy <a href=\"{list}\">maailmanlistalla</a> nimimerkilläsi.",
    # lista
    list_title="Maailmanlista – EXS World Tour", list_desc="Maailman parhaat suoritukset S-, M- ja L-rinteillä. Jokainen tulos on palvelimen varmentama.",
    list_kicker="Kausi 1", list_h1="Maailmanlista", tabs_aria="Rinne", archive="Arkisto",
    list_rows="Rivit 1–12 · yksi tulos per pelaaja",
    own_meta="Omat ennätykset", own_h="Kirjaudu nähdäksesi", own_p="Kirjautuminen Google-tilillä avautuu, kun testikausi alkaa. Tulosten lähettämiseen tarvitset tilin ja nimimerkin.", own_btn="Tilistä",
    rules_h="Säännöt lyhyesti",
    rules=["Yksi paras tulos pelaajaa kohden kullakin rinteellä.", "Palvelin laskee pisteet uudelleen syötteistä. Vain varmennetut tulokset näkyvät.",
           "Vain Google Playsta asennettu Android-peli kelpaa.", "Kauden vaihtuessa lista alkaa tyhjästä ja vanha kausi siirtyy arkistoon."],
    # suoritus
    run_title="Suoritus – EXS World Tour", run_desc="Palvelimen varmentama suoritus EXS World Tourin maailmanlistalta.",
    crumbs_aria="Murupolku", crumb_rank="Sija 1",
    run_notice="Esimerkkisivu. Oikeat suoritukset avautuvat osoitteesta <strong>worldtour.exsports.fi/s/&lt;tunnus&gt;</strong>, kun testikausi alkaa.",
    video_aria="Suorituksen video", video_device="Video laitteelta", play_aria="Toista video",
    run_meta="Pieni S · kausi 1 · 3.10.2026", total="Yhteensä", rank1="Sija 1",
    score_labels=["Amplitudi", "Rotaatio", "Grab", "Tasapaino", "Tyyli", "Stomp"],
    coach="Kierre 2° vajaa · Ote koko lennon · Ponnistus täydellinen · Puhdas stomp",
    share_h="Jaa suoritus", share_p="Linkki aukeaa ilman peliä ja kirjautumista.", copy="Kopioi linkki", download="Lataa video",
    how_scored_h="Miten pisteet syntyvät", how_scored_p="Palvelin ajoi pelaajan syötteet uudelleen ja laski pisteet itse. Video on tehty pelaajan laitteella samasta hypystä.",
    report="Ilmoita suoritus", report_subject="Ilmoitus%20suorituksesta",
    # oikeudelliset
    terms_title="Käyttöehdot", terms_kicker="World Rank", terms_desc="EXS World Tourin maailmanlistan käyttöehdot.",
    terms_notice="Käyttöehdot julkaistaan tällä sivulla ennen testikauden alkua. Alla on tiivistelmä periaatteista.",
    terms=["Maailmanlistalle osallistuminen vaatii 13 vuoden iän ja Google-tilin. Pelaaminen ilman tiliä on aina mahdollista.",
           "Nimimerkki on julkinen. Loukkaava, toisena esiintyvä tai henkilötietoja sisältävä nimimerkki vaihdetaan, ja toistuva rikkomus johtaa lähetyskieltoon.",
           "Listalle kelpaa vain itse pelattu suoritus muokkaamattomalla pelillä. Palvelin laskee jokaisen tuloksen uudelleen.",
           "Testikausi päättyy pelin julkaisuun, ja listat alkavat silloin tyhjästä."],
    questions="Kysymykset",
    privacy_title="Tietosuojaseloste", privacy_kicker="Henkilötiedot", privacy_desc="EXS World Tourin tietosuojaseloste.",
    privacy_notice="Tietosuojaseloste julkaistaan tällä sivulla ennen testikauden alkua.",
    privacy_p1="Rekisterinpitäjä on EXSports Oy. Maailmanlistaa varten käsitellään Google-tilin tunniste, nimimerkki, lähetetyt suoritukset ja niiden tiedot. Tiedot tallennetaan Google Firebase -palveluun EU:n alueelle. Julkisesti näkyy vain nimimerkki ja suoritus.",
    privacy_p2="Pelitestin telemetriaa koskeva seloste on pelin hyväksyntäruudussa. Yhteys",
    account_title="Tili ja tilin poisto", account_kicker="Tili", account_desc="EXS World Tourin tilin poisto.",
    account_p="Maailmanlistan tili luodaan Google-tilillä pelissä tai tällä sivustolla, kun testikausi alkaa. Tilin voi poistaa pelin asetuksista tai tältä sivulta kirjautumalla sisään. Poisto poistaa nimimerkin, tulokset, toistot ja videot.",
    account_notice="Kirjautuminen ja tilin poisto avautuvat tähän, kun palvelu on käytössä. Siihen asti pyynnöt", account_subject="Tilin%20poisto",
    nf_title="Sivua ei löytynyt – EXS World Tour", nf_desc="Sivua ei löytynyt.", nf_h="Kaatui",
    nf_p="Sivua ei löytynyt. Palaa <a href=\"{home}\">etusivulle</a> tai <a href=\"{list}\">maailmanlistalle</a>.",
)

T["en"] = dict(
    lang="en", skip="Skip to content", brand_aria="EXS World Tour, home", nav_aria="Main menu", lang_aria="Language",
    nav_how="How to play", nav_list="World ranking", nav_play="Get it on Google Play", foot_aria="Footer",
    foot_text="EXS World Tour is a game by EXSports Oy for Android. The S and M slopes are free; the L slope is a one-time purchase of €1.95.",
    foot_terms="Terms of use", foot_privacy="Privacy", foot_account="Delete account",
    sample="Sample data", watch="Watch", prev="Previous", next="Next", verified="Verified",
    home_title="EXS World Tour – the snowboard game where clean wins",
    home_desc="A Big Air snowboard game for Android. Learn the tricks, watch the world's best runs and chase your own place on the world ranking.",
    hero_kicker="Big Air · World Tour", hero_sub="World Tour",
    hero_lead="The cleaner the run, the higher the score. A snowboard game where tricks are scored from the movement itself, not from a button press.",
    ticker_title="World ranking · Small S", ticker_aria="Top of the world ranking, Small S",
    how_h="How it works", how_all="Full guide",
    step1_m="1 · In-run", step1_h="Pop off the lip", step1_p="Crouch in the in-run, pop at the lip. Timing decides height, and height gives you time for the trick.",
    step2_m="2 · Air", step2_h="Spin and grab", step2_p="Spin and flip on their own sliders, grab with a button: Nose, Tail, Indy or Weddle. Hold the grab for at least 0.2 seconds and let go before the snow.",
    step3_m="3 · Landing", step3_h="Land it clean", step3_p="Board straight and rotation finished before the snow. A clean landing banks the points; a crash wipes them.",
    top_meta="Season 1 · Small S", top_h="Top right now", top_all="Full world ranking", top_first="Watch the #1 run",
    slopes_h="Three slopes", slope_s="Small S", slope_m="Medium M", slope_l="Large L", free="Free", paid="One-time €1.95",
    fair_h="A fair ranking", fair_p="Every result is recomputed on the server from the player's inputs. The number the game shows is not enough, and every ranked run can be watched.",
    how_title="How to play – EXS World Tour", how_desc="Getting started, controls, pop, grabs and landing. The seven tutorial steps and the career track.",
    how_kicker="Guide", how_h1="How to play",
    how_intro="The game starts with a tutorial that teaches the run, the pop, the grab and the first tricks in seven steps. The tutorial uses the S and M kickers, and the career track opens after it.",
    start_h="Getting started",
    start_steps=["Choose <strong>Tutorial</strong> from the main menu.", "Pick the current exercise and read <strong>Do this</strong> and <strong>Why?</strong>.",
                 "<strong>Watch example</strong> shows the inputs for the same task. Watching does not count as a completion.",
                 "Start the exercise and press <strong>Go</strong> on the slope. In steps 5–7, set the flip or spin before you go.",
                 "A success is saved before the next task. Completed tasks can be repeated."],
    controls_h="Controls",
    controls=["<strong>Crouch</strong> in the in-run: the slider on the left, the fill shows how deep you are.",
              "<strong>Pop</strong> near the lip. Your timing shows as feedback in the air; a perfect pop is PERFECT.",
              "<strong>Spin and flip</strong> on their own sliders. Direction FS or BS, amount in 180° steps.",
              "<strong>Grabs</strong> Nose, Tail, Indy and Weddle are buttons during the air. A grab needs a hold of at least 0.2 seconds, and the hold time affects rotation.",
              "<strong>Landing</strong> is Clean, Sketchy or a crash. Let go of the grab before the snow."],
    controls_p="In Play mode every jump starts with the sliders reset. The rider sets off as soon as you touch any control on the start screen.",
    lessons_h="The seven tutorial steps", lessons_cols=["#", "Kicker", "Exercise", "Do this"],
    lessons=[("1", "S", "Run and landing", "Press Go and follow the jump with the preset settings."),
             ("2", "S", "Pop", "Press Pop near the lip and release as instructed."),
             ("3", "S", "Grab", "Hold Indy in the air and let go before the ground."),
             ("4", "S", "Jump + Indy", "Combine a timed pop with an Indy grab."),
             ("5", "M", "Front flip + Nose", "Set a front flip; hold Nose in the air and let go before the ground."),
             ("6", "M", "FS 360 + Indy", "Set an FS 360; hold Indy and let go before the ground."),
             ("7", "M", "FS 180 + Indy", "Half a rotation frontside, hold Indy and aim the landing with a small counter-spin.")],
    career_h="Career track", career_p="After the tutorial, <strong>Play</strong> opens the career. The four S tasks unlock the M slope, and the six M tasks unlock the L tasks.",
    career_s="4 tasks · free", career_m="6 tasks · free", career_l="10 tasks · €1.95",
    wr_h="World ranking", wr_p="When a result is ready for the ranking, submit it from the result card in the game. The server recomputes the score from your inputs, and the verified result appears on the <a href=\"{list}\">world ranking</a> under your nickname.",
    list_title="World ranking – EXS World Tour", list_desc="The world's best runs on the S, M and L slopes. Every result is verified on the server.",
    list_kicker="Season 1", list_h1="World ranking", tabs_aria="Slope", archive="Archive",
    list_rows="Rows 1–12 · one result per player",
    own_meta="Your bests", own_h="Sign in to see", own_p="Sign-in with a Google account opens when the test season starts. You need an account and a nickname to submit results.", own_btn="About accounts",
    rules_h="Rules in brief",
    rules=["One best result per player on each slope.", "The server recomputes scores from the inputs. Only verified results are shown.",
           "Only the Android game installed from Google Play qualifies.", "When the season changes, the ranking starts empty and the old season moves to the archive."],
    run_title="Run – EXS World Tour", run_desc="A server-verified run from the EXS World Tour world ranking.",
    crumbs_aria="Breadcrumb", crumb_rank="Rank 1",
    run_notice="Sample page. Real runs open at <strong>worldtour.exsports.fi/s/&lt;id&gt;</strong> when the test season starts.",
    video_aria="Run video", video_device="Video from device", play_aria="Play video",
    run_meta="Small S · season 1 · 3 Oct 2026", total="Total", rank1="Rank 1",
    score_labels=["Amplitude", "Rotation", "Grab", "Balance", "Style", "Stomp"],
    coach="Spin 2° short · Grab held the whole air · Perfect pop · Clean stomp",
    share_h="Share this run", share_p="The link opens without the game or a sign-in.", copy="Copy link", download="Download video",
    how_scored_h="How the score is made", how_scored_p="The server replayed the player's inputs and computed the score itself. The video was rendered on the player's device from the same jump.",
    report="Report this run", report_subject="Run%20report",
    terms_title="Terms of use", terms_kicker="World Rank", terms_desc="Terms of use for the EXS World Tour world ranking.",
    terms_notice="The terms of use will be published on this page before the test season starts. Below is a summary of the principles.",
    terms=["Taking part in the world ranking requires being 13 or older and a Google account. Playing without an account is always possible.",
           "Nicknames are public. An offensive or impersonating nickname, or one containing personal data, is changed, and repeated violations lead to a submission ban.",
           "Only runs you played yourself on an unmodified game qualify. The server recomputes every result.",
           "The test season ends when the game launches, and the rankings start empty then."],
    questions="Questions",
    privacy_title="Privacy policy", privacy_kicker="Personal data", privacy_desc="EXS World Tour privacy policy.",
    privacy_notice="The privacy policy will be published on this page before the test season starts.",
    privacy_p1="The controller is EXSports Oy. For the world ranking we process your Google account identifier, nickname, submitted runs and their data. Data is stored in Google Firebase in the EU. Only the nickname and the run are shown publicly.",
    privacy_p2="The notice covering playtest telemetry is in the game's consent screen. Contact",
    account_title="Account and account deletion", account_kicker="Account", account_desc="Deleting your EXS World Tour account.",
    account_p="The world ranking account is created with a Google account in the game or on this site when the test season starts. You can delete the account from the game's settings or from this page after signing in. Deletion removes the nickname, results, replays and videos.",
    account_notice="Sign-in and account deletion will open here when the service is live. Until then, send requests to", account_subject="Account%20deletion",
    nf_title="Page not found – EXS World Tour", nf_desc="Page not found.", nf_h="Bailed",
    nf_p="Page not found. Go back to the <a href=\"{home}\">front page</a> or the <a href=\"{list}\">world ranking</a>.",
)


def trick(name, lang):
    if lang == "fi":
        return name
    for fi, en in TRICK_EN.items():
        name = name.replace(fi, en)
    return name


# ---------------------------------------------------------------- runko
def page(lang, rel, title, desc, body, current):
    is404 = rel == "404"
    t = T[lang]
    p = LANGS[lang]["prefix"]
    rel = "" if rel == "404" else rel  # GitHub Pages näyttää vain juuren 404.html:n; sen linkit osoittavat etusivulle
    url = f"{SITE}/{p}{rel}"
    L = lambda r: f"/{p}{r}"

    def nav(href, label):
        cur = ' aria-current="page"' if href == current else ""
        return f'<a href="{href}"{cur}>{label}</a>'

    alternates = "".join(f'<link rel="alternate" hreflang="{l}" href="{SITE}/{LANGS[l]["prefix"]}{rel}">\n' for l in LANGS)
    alternates += f'<link rel="alternate" hreflang="x-default" href="{SITE}/{rel}">\n'
    switch = ""
    for l in LANGS:
        cur = ' aria-current="true"' if l == lang else ""
        switch += f'<a href="/{LANGS[l]["prefix"]}{rel}" hreflang="{l}" lang="{l}"{cur}>{LANGS[l]["short"]}</a>'

    head = f'''<!doctype html>
<html lang="{lang}" data-theme="viimeinen-valo">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
{alternates}<meta property="og:type" content="website">
<meta property="og:site_name" content="EXS World Tour">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/og-image.jpg">
<meta property="og:locale" content="{'fi_FI' if lang == 'fi' else 'en_US'}">
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
<a class="skip" href="#sisalto">{t["skip"]}</a>
<header class="site-header"><div class="wrap">
<a class="brand" href="{L("")}" aria-label="{t["brand_aria"]}"><span class="brand__exs">EXS</span><span class="brand__bar"></span><span class="brand__wt">World Tour</span></a>
<nav class="site-nav" aria-label="{t["nav_aria"]}">{nav(L("nain-pelaat/"), t["nav_how"])}{nav(L("lista/"), t["nav_list"])}<a class="exs-btn exs-btn--sm" href="{PLAY}"><span>{t["nav_play"]}</span></a><div class="lang-switch" role="group" aria-label="{t["lang_aria"]}">{switch}</div></nav>
</div></header>
<main id="sisalto">
'''
    foot = f'''</main>
<footer class="site-footer"><div class="wrap">
<div class="stack" style="gap: 12px"><a href="https://www.exsports.fi/" aria-label="EXSports Oy"><img class="site-footer__logo" src="/assets/img/exsports-wordmark.png" alt="EXSports Oy"></a><span>{t["foot_text"]}</span></div>
<nav aria-label="{t["foot_aria"]}"><a href="{L("kayttoehdot/")}">{t["foot_terms"]}</a><a href="{L("tietosuoja/")}">{t["foot_privacy"]}</a><a href="{L("tili/")}">{t["foot_account"]}</a><a href="mailto:info@exsports.fi">info@exsports.fi</a></nav>
</div></footer>
</body>
</html>
'''
    out = "404.html" if is404 else f"{p}{rel}index.html"
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
    L = lambda r: f"/{p}{r}"
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
<div class="video__bar"><span class="label" style="text-transform:uppercase;color:var(--text-soft)">0:00 / 0:11</span><div class="video__track"><div class="video__fill"></div></div><span class="label" style="text-transform:uppercase;color:var(--text-soft)">0,5×</span></div>
</div>
<section class="exs-panel pad-shadow">
<div class="row-between" style="flex-wrap: wrap"><h1 class="exs-panel__title" style="margin:0">Riikka_fin <span style="color: var(--accent); font-size: 20px">BS 540 + Indy</span></h1><span class="exs-panel__meta">{t["run_meta"]}</span></div>
<div class="exs-total" style="margin-top: 16px"><span class="exs-total__label">{t["total"]}</span><span class="exs-total__value">15 890</span><span class="exs-total__pb">{t["rank1"]}</span></div>
<div class="exs-score">{cells}</div>
<div class="exs-callout" style="margin-top: 24px">{t["coach"]}</div>
</section>
</div>
<div class="stack">
<div class="exs-panel pad-shadow"><h2 class="exs-panel__title">{t["share_h"]}</h2><p class="prose" style="margin:0 0 16px; font-size:14px; line-height:20px">{t["share_p"]}</p><div class="linkbox">worldtour.exsports.fi/s/esimerkki</div><div style="margin-top: 16px; display:flex; gap: 12px; flex-wrap: wrap"><button type="button" class="exs-btn exs-btn--sm" data-copy data-copied="{'Kopioitu' if lang == 'fi' else 'Copied'}"><span>{t["copy"]}</span></button><a class="exs-btn exs-btn--sm exs-btn--secondary" href="#" aria-disabled="true"><span>{t["download"]}</span></a></div></div>
<div class="exs-panel exs-panel--quiet"><h2 class="exs-panel__title">Riikka_fin</h2><div class="stack" style="gap: 8px; font-size: 14px; line-height: 20px; color: var(--text-soft)"><div class="row-between"><span>{t["slope_s"]}</span><span class="display-xs" style="color: var(--text)">1 · 15 890</span></div><div class="row-between"><span>{t["slope_m"]}</span><span class="display-xs" style="color: var(--text)">4 · 21 330</span></div><div class="row-between"><span>{t["slope_l"]}</span><span class="display-xs" style="color: var(--text)">2 · 27 110</span></div></div></div>
<div class="exs-panel exs-panel--quiet"><h2 class="exs-panel__title">{t["how_scored_h"]}</h2><p class="prose" style="margin:0; font-size:14px; line-height:20px">{t["how_scored_p"]}</p><div style="margin-top: 16px"><a class="more" href="mailto:info@exsports.fi?subject={t["report_subject"]}" style="color: var(--muted)">{t["report"]}</a></div></div>
</div>
</div></section>
''', L("lista/"))

    # oikeudelliset sivut
    def simple(rel, title, kicker, h1, inner, desc):
        page(lang, rel, f"{title} – EXS World Tour", desc, f'''<section class="section"><div class="wrap"><div class="kicker">{kicker}</div><h1 class="h1" style="margin: 8px 0 24px">{h1}</h1><div class="prose">{inner}</div></div></section>''', L(rel))

    simple("kayttoehdot/", t["terms_title"], t["terms_kicker"], t["terms_title"],
           f'<div class="notice" style="margin-bottom: 24px">{t["terms_notice"]}</div><ul>{li(t["terms"])}</ul><p>{t["questions"]}: <a href="mailto:info@exsports.fi">info@exsports.fi</a></p>', t["terms_desc"])
    simple("tietosuoja/", t["privacy_title"], t["privacy_kicker"], t["privacy_title"],
           f'<div class="notice" style="margin-bottom: 24px">{t["privacy_notice"]}</div><p>{t["privacy_p1"]}</p><p>{t["privacy_p2"]}: <a href="mailto:info@exsports.fi">info@exsports.fi</a></p>', t["privacy_desc"])
    simple("tili/", t["account_title"], t["account_kicker"], t["account_title"],
           f'<p>{t["account_p"]}</p><div class="notice">{t["account_notice"]}: <a href="mailto:info@exsports.fi?subject={t["account_subject"]}">info@exsports.fi</a></div>', t["account_desc"])

    if lang != "fi":
        return
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
