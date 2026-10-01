"""Legal document metadata and rendering; authoritative prose lives in legal/{fi,en}."""
from html import escape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEGAL_SLUGS = ("kayttoehdot", "tietosuoja", "tili", "ostot", "saannot", "evasteet")
TITLES = {
    "fi": ("Käyttöehdot", "Tietosuojaseloste", "Tietojen ja tilin poistaminen", "Ostoehdot", "World Rank -säännöt", "Evästeet ja sivuston tietosuoja"),
    "en": ("Terms of use", "Privacy notice", "Delete your data or account", "Purchase terms", "World Rank rules", "Cookies and website privacy"),
}
NOTICES = {
    "sv": "De juridiska dokumenten finns på finska och engelska. Nedan visas den engelska versionen; detta är ingen svensk översättning.",
    "no": "De juridiske dokumentene finnes på finsk og engelsk. Nedenfor vises den engelske versjonen; dette er ikke en norsk oversettelse.",
    "da": "De juridiske dokumenter findes på finsk og engelsk. Nedenfor vises den engelske version; dette er ikke en dansk oversættelse.",
    "de": "Die rechtlichen Dokumente sind auf Finnisch und Englisch verfügbar. Unten steht die englische Fassung; dies ist keine deutsche Übersetzung.",
    "nl": "De juridische documenten zijn beschikbaar in het Fins en Engels. Hieronder staat de Engelse versie; dit is geen Nederlandse vertaling.",
    "fr": "Les documents juridiques sont disponibles en finnois et en anglais. La version anglaise figure ci-dessous ; il ne s’agit pas d’une traduction française.",
    "es": "Los documentos legales están disponibles en finés e inglés. A continuación se muestra la versión inglesa; no es una traducción al español.",
    "it": "I documenti legali sono disponibili in finlandese e inglese. Di seguito è riportata la versione inglese; non si tratta di una traduzione italiana.",
    "pt": "Os documentos legais estão disponíveis em finlandês e inglês. Abaixo encontra-se a versão inglesa; não se trata de uma tradução para português.",
    "pl": "Dokumenty prawne są dostępne po fińsku i angielsku. Poniżej znajduje się wersja angielska; nie jest to polskie tłumaczenie.",
    "et": "Õigusdokumendid on saadaval soome ja inglise keeles. Allpool on ingliskeelne versioon; see ei ole eestikeelne tõlge.",
    "lv": "Juridiskie dokumenti ir pieejami somu un angļu valodā. Zemāk ir angļu valodas versija; tas nav tulkojums latviešu valodā.",
    "lt": "Teisiniai dokumentai pateikiami suomių ir anglų kalbomis. Toliau rodoma versija anglų kalba; tai nėra vertimas į lietuvių kalbą.",
}


class Headings(HTMLParser):
    def __init__(self):
        super().__init__()
        self.headings = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        if tag == "h1":
            raise ValueError("Legal fragments must not contain an h1")
        if tag == "h2":
            anchor = dict(attrs).get("id")
            if not anchor or anchor in {h[0] for h in self.headings}:
                raise ValueError("Each legal h2 needs a unique id")
            self.current = [anchor, ""]

    def handle_data(self, data):
        if self.current is not None:
            self.current[1] += data

    def handle_endtag(self, tag):
        if tag == "h2" and self.current is not None:
            self.headings.append(self.current)
            self.current = None


def legal_language(lang):
    return "fi" if lang == "fi" else "en"


def footer_links(lang, prefix):
    labels = TITLES[legal_language(lang)]
    links = "".join(f'<a href="/{prefix}{slug}/">{escape(label)}</a>' for slug, label in zip(LEGAL_SLUGS, labels))
    imprint = "Yritystiedot" if lang == "fi" else "Company information"
    return links + f'<a href="https://www.exsports.fi/legal/imprint.html">{imprint}</a>'


def render_document(lang, slug, prefix):
    content_lang = legal_language(lang)
    title = TITLES[content_lang][LEGAL_SLUGS.index(slug)]
    fragment = (ROOT / "legal" / content_lang / f"{slug}.html").read_text(encoding="utf-8")
    fragment = fragment.replace("{{prefix}}", "/" if content_lang == "fi" else "/en/")
    headings = Headings()
    headings.feed(fragment)
    if not headings.headings:
        raise ValueError(f"No legal sections in {content_lang}/{slug}")
    fi = content_lang == "fi"
    documents = "Oikeudelliset asiakirjat" if fi else "Legal documents"
    contents = "Tällä sivulla" if fi else "On this page"
    languages = "Asiakirjan kieli" if fi else "Document language"
    nav = "".join(
        f'<li><a href="/{prefix}{key}/"' + (' aria-current="page"' if key == slug else "") + f'>{escape(label)}</a></li>'
        for key, label in zip(LEGAL_SLUGS, TITLES[content_lang])
    )
    toc = "".join(f'<li><a href="#{escape(anchor, quote=True)}">{escape(label.strip())}</a></li>' for anchor, label in headings.headings)
    notice = ""
    if lang not in ("fi", "en"):
        notice = f'<p class="notice legal-fallback" lang="{lang}">{escape(NOTICES[lang])} <a href="/en/{slug}/" lang="en" hreflang="en">Read in English</a></p>'
    body = f'''<section class="section legal-section"><div class="wrap">
{notice}
<div class="legal-layout" lang="{content_lang}">
<header class="legal-heading"><div class="kicker">{documents}</div>
<h1 class="h1">{escape(title)}</h1>
<nav class="legal-languages" aria-label="{languages}"><a href="/{slug}/" lang="fi" hreflang="fi">Suomeksi</a><a href="/en/{slug}/" lang="en" hreflang="en">In English</a></nav></header>
<aside class="legal-sidebar"><nav class="legal-nav" aria-label="{documents}"><p class="legal-nav-title">{documents}</p><ul>{nav}</ul></nav>
<nav class="legal-toc" aria-label="{contents}"><p class="legal-nav-title">{contents}</p><ol>{toc}</ol></nav></aside>
<article class="prose legal-document" lang="{content_lang}" data-legal-document="{slug}">{fragment}</article>
</div></div></section>'''
    if slug in ("tili", "evasteet"):
        status = "Ajantasaiset ohjeet, päivitetty 1.10.2026." if fi else "Current guidance, updated 1 October 2026."
    else:
        status = "Tarkistettava asiakirjaluonnos, 1.10.2026." if fi else "Document draft for review, 1 October 2026."
    desc = f"EXS World Tour: {title}. {status}"
    return title, desc, body
