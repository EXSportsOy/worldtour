"""Check the approved price and prevent preview pages claiming live services."""
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET
from check_i18n import Page

SITE = 'https://worldtour.exsports.fi/'
WR_OPENS = '2026-12-01T00:00:00Z'
WR_TEXT = ('wr_loading', 'wr_closed_h', 'wr_closed_p', 'wr_empty', 'wr_error', 'wr_hidden', 'wr_open', 'wr_closing', 'wr_final')
SAMPLE_NAMES = ('Riikka_fin', 'Snowdog', 'Kaamos')

ROOT = Path(__file__).resolve().parents[1]


def check_rank_script():
    # Nicknames are user content and the list and run pages must stay same-origin under connect-src 'self'.
    for name in ('rank.js', 'share.js'):
        source = (ROOT / 'assets/js' / name).read_text(encoding='utf-8')
        for sink in ('innerHTML', 'outerHTML', 'insertAdjacentHTML', 'document.write', 'eval(', 'new Function'):
            assert sink not in source, f'{name}: unsafe sink {sink}'
        assert source.count('fetch(') == 1, f'{name}: one fetch helper only'
        paths = re.findall(r"(?<!\+ )'(/[^']*)'", source)  # path literals, not suffixes after base() +
        assert paths and all(path.startswith('/api/seasons') for path in paths), f'{name}: unexpected request path {paths}'
        assert not re.search(r'https?://', source), f'{name}: absolute URL'


def check_scripts(path, parsed):
    # CSP script-src 'self': only same-origin files; inline JSON data blocks would be allowed, code is not.
    for tag, attrs in parsed.tags:
        if tag == 'script':
            src = attrs.get('src', '')
            assert src.startswith('/assets/js/') or attrs.get('type') == 'application/json', f'{path}: inline or foreign script'


def check():
    check_rank_script()
    sitemap = ET.parse(ROOT / 'sitemap.xml')
    locations = {n.text for n in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
    for path in list((ROOT / 'i18n').glob('*.json')) + list(ROOT.rglob('*.html')):
        assert not re.search(r'\b1[.,]95\b', path.read_text(encoding='utf-8')), f'{path}: obsolete price'
    for path in (ROOT / 'i18n').glob('*.json'):
        lang = path.stem
        data = json.loads(path.read_text(encoding='utf-8'))
        prefix = '' if lang == 'fi' else lang + '/'
        for key in ('foot_text', 'paid', 'career_l', 'offer'):
            assert re.search(r'2[.,]99', data[key]), f'{lang}/{key}: missing current price'
        for route in ('', 'nain-pelaat/', 'lista/', 's/'):
            html = (ROOT / prefix / route / 'index.html').read_text(encoding='utf-8')
            parsed = Page(html)
            check_scripts(f'{lang}/{route}', parsed)
            noindex = ('meta', {'name': 'robots', 'content': 'noindex'}) in parsed.tags
            assert noindex == (SITE + prefix + route not in locations), f'{lang}/{route}: robots and sitemap disagree'
            assert data['availability'] in html, f'{lang}/{route}: missing availability'
            assert 'play.google.com/store/apps/details' not in html, f'{lang}/{route}: premature store CTA'
            assert not any(tag == 'a' and a.get('aria-disabled') == 'true' for tag, a in parsed.tags), f'{lang}/{route}: placeholder link'
            if route in ('', 'nain-pelaat/'):
                assert data['purchase_scope'] in html, f'{lang}/{route}: missing purchase scope'
                assert data['offer'] in html, f'{lang}/{route}: missing regional price disclosure'
            if route == '':
                ticker = re.search(r'class="exs-ticker".*?</a>', html, re.S)
                assert ticker and data['sample'] in ticker.group(), f'{lang}: unlabelled sample ticker'
            if route == 'lista/':
                # Real rows come only from the API (assets/js/rank.js); static HTML is the honest closed state.
                assert data['sample'] not in html and not any(n in html for n in SAMPLE_NAMES), f'{lang}: sample data on the list'
                assert not any(tag == 'li' and 'exs-row' in a.get('class', '') for tag, a in parsed.tags), f'{lang}: static list rows'
                assert ('script', {'src': '/assets/js/rank.js', 'defer': None}) in parsed.tags, f'{lang}: list script missing'
                panel = next((a for tag, a in parsed.tags if a.get('id') == 'lista'), {})
                assert panel.get('data-opens') == WR_OPENS, f'{lang}: World Rank opening date'
                for key in WR_TEXT:
                    assert panel.get('data-t-' + key[3:].replace('_', '-')) == data[key], f'{lang}: list text {key}'
                status = re.search(r'<p [^>]*data-wr-status[^>]*>(.*?)</p>', html, re.S)
                assert status and status.group(1) == data['wr_closed_p'], f'{lang}: list does not show the closed state'
                assert ('meta', {'name': 'description', 'content': data['wr_closed_p']}) in parsed.tags, f'{lang}: list description'
                # Until Season 1 has verified results the page is an empty state: keep it out of search.
                assert noindex, f'{lang}/{route}: empty list indexed'
            if route == 's/':
                # Real runs come only from the API (assets/js/share.js); static HTML is the honest closed state.
                assert noindex, f'{lang}/{route}: run page indexed'
                assert data['sample'] not in html and not any(n in html for n in SAMPLE_NAMES), f'{lang}: sample data on the run page'
                assert ('script', {'src': '/assets/js/share.js', 'defer': None}) in parsed.tags, f'{lang}: run script missing'
                panel = next((a for tag, a in parsed.tags if a.get('id') == 'suoritus'), {})
                assert panel.get('data-opens') == WR_OPENS and panel.get('data-share') == SITE + prefix + 's/', f'{lang}: run page share base'
                status = re.search(r'<p [^>]*data-run-status[^>]*>(.*?)</p>', html, re.S)
                assert status and status.group(1) == data['wr_closed_p'], f'{lang}: run page does not show the closed state'
            if route in ('lista/', 's/'):
                assert 'kausi-1' not in html and 'kausi=arkisto' not in html, f'{lang}: misleading season'
                assert 'video__play' not in html and 'exs-badge--verified' not in html, f'{lang}: fake video/verification'
                assert not any(tag == 'a' and a.get('href') == '#' for tag, a in parsed.tags), f'{lang}: dummy action'
    print('marketing ok: 15 languages; price, scope, availability, honest World Rank list, scripts, robots/sitemap')


if __name__ == '__main__':
    check()
