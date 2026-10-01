"""Validate generated legal routes, source fidelity, language labels and navigation.

Run after python build.py. Uses only Python's standard library.
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from legal_content import LEGAL_SLUGS, NOTICES

LANGS = ("fi", "en", "sv", "no", "da", "de", "nl", "fr", "es", "it", "pt", "pl", "et", "lv", "lt")
errors = []


class Node:
    def __init__(self, tag="root", attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def find(self, tag=None, cls=None):
        found = []
        for child in self.children:
            if isinstance(child, Node):
                if (tag is None or child.tag == tag) and (cls is None or cls in child.attrs.get("class", "").split()):
                    found.append(child)
                found.extend(child.find(tag, cls))
        return found

    def text(self):
        return "".join(child.text() if isinstance(child, Node) else child for child in self.children)


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.root = Node()
        self.stack = [self.root]
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            self.stack.append(node)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def require(condition, path, message):
    if not condition:
        errors.append(f"{path}: {message}")


def hrefs(node):
    return {a.attrs.get("href") for a in node.find("a")}


for lang in ("fi", "en"):
    for slug in LEGAL_SLUGS:
        source = ROOT / "legal" / lang / f"{slug}.html"
        require(source.is_file(), source.relative_to(ROOT), "missing source fragment")
if errors:
    print("\n".join(errors))
    sys.exit(1)

stale = []
for lang in LANGS:
    data = json.loads((ROOT / "i18n" / f"{lang}.json").read_text(encoding="utf-8"))
    stale.extend(data.get(key, "") for key in ("terms_notice", "privacy_notice", "privacy_p1", "account_p", "account_notice"))

sitemap = ET.parse(ROOT / "sitemap.xml")
locations = {node.text for node in sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
cache = {}


def read_document(path):
    if path not in cache:
        cache[path] = Document(path.read_text(encoding="utf-8")).root
    return cache[path]


for lang in LANGS:
    prefix = "" if lang == "fi" else f"{lang}/"
    content_lang = "fi" if lang == "fi" else "en"
    for slug in LEGAL_SLUGS:
        rel = f"{prefix}{slug}/index.html"
        path = ROOT / rel
        require(path.is_file(), rel, "missing generated document")
        if not path.is_file():
            continue
        source = path.read_text(encoding="utf-8")
        doc = read_document(path)
        require(doc.find("html")[0].attrs.get("lang") == lang, rel, "wrong site language")
        require(len(doc.find("h1")) == 1, rel, "expected one page heading")
        require(not any(doc.find(tag) for tag in ("script", "form", "iframe")), rel, "legal page must remain static")
        require("{{" not in source and "}}" not in source, rel, "unresolved template placeholder")
        for old in stale:
            require(not old or old not in source, rel, "obsolete legal placeholder text survives")
        articles = doc.find("article", "legal-document")
        require(len(articles) == 1, rel, "missing legal article")
        if len(articles) != 1:
            continue
        article = articles[0]
        require(article.attrs.get("lang") == content_lang, rel, "wrong document language")
        layout = doc.find(cls="legal-layout")
        require(len(layout) == 1 and layout[0].attrs.get("lang") == content_lang, rel, "heading and navigation language missing")
        fragment = (ROOT / "legal" / content_lang / f"{slug}.html").read_text(encoding="utf-8").replace("{{prefix}}", "/" if content_lang == "fi" else "/en/")
        rendered = re.search(r'<article\b[^>]*data-legal-document="' + slug + r'"[^>]*>(.*?)</article>', source, re.S)
        require(rendered is not None and rendered.group(1) == fragment, rel, "generated body differs from its authoritative fragment")
        ids = [n.attrs["id"] for n in doc.find() if "id" in n.attrs]
        require(len(ids) == len(set(ids)), rel, "duplicate element id")
        headings = article.find("h2")
        require(len(headings) >= 2 and all(h.attrs.get("id") for h in headings), rel, "document sections need heading anchors")
        tocs = doc.find("nav", "legal-toc")
        expected_toc = [("#" + h.attrs.get("id", ""), h.text().strip()) for h in headings]
        actual_toc = [(a.attrs.get("href"), a.text().strip()) for a in tocs[0].find("a")] if tocs else []
        require(actual_toc == expected_toc, rel, "table of contents does not match sections")
        navs = doc.find("nav", "legal-nav")
        required_links = {f"/{prefix}{key}/" for key in LEGAL_SLUGS}
        require(len(navs) == 1 and required_links <= hrefs(navs[0]), rel, "incomplete document navigation")
        active = [a for a in navs[0].find("a") if a.attrs.get("aria-current") == "page"] if navs else []
        require(len(active) == 1 and active[0].attrs.get("href") == f"/{prefix}{slug}/", rel, "incorrect current document")
        languages = doc.find("nav", "legal-languages")
        require(len(languages) == 1 and {f"/{slug}/", f"/en/{slug}/"} <= hrefs(languages[0]), rel, "missing FI/EN language links")
        notices = doc.find(cls="legal-fallback")
        if lang not in ("fi", "en"):
            require(len(notices) == 1 and notices[0].attrs.get("lang") == lang and NOTICES[lang] in notices[0].text(), rel, "missing localized English-fallback notice")
            require(bool(notices) and f"/en/{slug}/" in hrefs(notices[0]), rel, "missing direct English link")
        else:
            require(not notices, rel, "unexpected fallback notice")
        require(f"https://worldtour.exsports.fi/{prefix}{slug}/" in locations, rel, "missing sitemap entry")
        for a in doc.find("a"):
            url = urlsplit(a.attrs.get("href", ""))
            if url.scheme or url.netloc or not url.fragment:
                continue
            target = ROOT / unquote(url.path).lstrip("/") if url.path else path
            if target.is_dir():
                target = target / "index.html"
            require(target.is_file(), rel, f"missing anchor target {a.attrs.get('href')}")
            if target.is_file():
                target_ids = {n.attrs.get("id") for n in read_document(target).find()}
                require(unquote(url.fragment) in target_ids, rel, f"broken anchor {a.attrs.get('href')}")

    # Footer links must be present on marketing pages as well as legal routes.
    for route in ("", "nain-pelaat/", "lista/", "s/") + tuple(f"{slug}/" for slug in LEGAL_SLUGS):
        path = ROOT / prefix / route / "index.html"
        require(path.is_file(), path.relative_to(ROOT), "missing page")
        if path.is_file():
            footers = read_document(path).find("footer", "site-footer")
            expected = {f"/{prefix}{slug}/" for slug in LEGAL_SLUGS} | {"https://www.exsports.fi/legal/imprint.html"}
            require(len(footers) == 1 and expected <= hrefs(footers[0]), path.relative_to(ROOT), "incomplete legal footer")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"legal ok: {len(LEGAL_SLUGS)} documents x {len(LANGS)} languages; source fidelity, language notices, navigation, anchors, footer and sitemap verified")
