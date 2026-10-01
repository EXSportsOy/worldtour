"""Legal metadata and rendering; terms exist in all site languages, other prose in FI/EN."""
from html import escape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEGAL_SLUGS = ("kayttoehdot", "tietosuoja", "tili", "ostot", "saannot", "evasteet")
from legal_ui import UI, TITLES, NOTICES


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


def legal_language(lang, slug=None):
    # All UI labels and terms are translated; remaining document bodies use FI/EN.
    if slug is None or slug == "kayttoehdot":
        return lang
    return "fi" if lang == "fi" else "en"


def footer_links(lang, prefix):
    labels = TITLES[legal_language(lang)]
    links = "".join(f'<a href="/{prefix}{slug}/">{escape(label)}</a>' for slug, label in zip(LEGAL_SLUGS, labels))
    imprint = UI[lang][4]
    return links + f'<a href="https://www.exsports.fi/legal/imprint.html">{imprint}</a>'


def render_document(lang, slug, prefix):
    content_lang = legal_language(lang, slug)
    title = TITLES[content_lang][LEGAL_SLUGS.index(slug)]
    fragment = (ROOT / "legal" / content_lang / f"{slug}.html").read_text(encoding="utf-8")
    fragment = fragment.replace("{{prefix}}", "/" if content_lang == "fi" else f"/{content_lang}/")
    headings = Headings()
    headings.feed(fragment)
    if not headings.headings:
        raise ValueError(f"No legal sections in {content_lang}/{slug}")
    fi = content_lang == "fi"
    documents, contents, languages = UI[content_lang][1:4]
    nav = "".join(
        f'<li><a href="/{prefix}{key}/"' + (' aria-current="page"' if key == slug else "") + f'>{escape(label)}</a></li>'
        for key, label in zip(LEGAL_SLUGS, TITLES[content_lang])
    )
    toc = "".join(f'<li><a href="#{escape(anchor, quote=True)}">{escape(label.strip())}</a></li>' for anchor, label in headings.headings)
    notice = ""
    if lang != content_lang:
        notice = f'<p class="notice legal-fallback" lang="{lang}">{escape(NOTICES[lang])} <a href="/en/{slug}/" lang="en" hreflang="en">Read in English</a></p>'
    document_languages = tuple(UI) if slug == "kayttoehdot" else ("fi", "en")
    language_links = "".join(
        f'<a href="/{"" if code == "fi" else code + "/"}{slug}/" lang="{code}" hreflang="{code}">{escape(UI[code][0])}</a>'
        for code in document_languages
    )
    body = f'''<section class="section legal-section"><div class="wrap">
{notice}
<div class="legal-layout" lang="{content_lang}">
<header class="legal-heading"><div class="kicker">{documents}</div>
<h1 class="h1">{escape(title)}</h1>
<nav class="legal-languages" aria-label="{languages}">{language_links}</nav></header>
<aside class="legal-sidebar"><nav class="legal-nav" aria-label="{documents}"><p class="legal-nav-title">{documents}</p><ul>{nav}</ul></nav>
<nav class="legal-toc" aria-label="{contents}"><p class="legal-nav-title">{contents}</p><ol>{toc}</ol></nav></aside>
<article class="prose legal-document" lang="{content_lang}" data-legal-document="{slug}">{fragment}</article>
</div></div></section>'''
    if slug in ("tili", "evasteet"):
        status = "Ajantasaiset ohjeet, päivitetty 1.10.2026." if fi else "Current guidance, updated 1 October 2026."
    else:
        status = UI[content_lang][5]
    desc = f"EXS World Tour: {title}. {status}"
    return title, desc, body
