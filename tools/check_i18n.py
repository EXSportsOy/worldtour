"""Check every translation and generated language page using only the stdlib."""
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from string import Formatter
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from legal_content import LEGAL_SLUGS
PAGES = ['', 'nain-pelaat/', 'lista/', 's/'] + [slug + '/' for slug in LEGAL_SLUGS]


def load_unique(pairs):
    result = {}
    for key, value in pairs:
        assert key not in result, f'Duplicate translation key: {key}'
        result[key] = value
    return result


def leaves(value, key=''):
    if isinstance(value, dict):
        for name, child in value.items():
            yield from leaves(child, key + '.' + name)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from leaves(child, f'{key}[{index}]')
    else:
        yield key, value


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def check():
    data = {p.stem: json.loads(p.read_text(encoding='utf-8'), object_pairs_hook=load_unique)
            for p in (ROOT / 'i18n').glob('*.json')}
    baseline = dict(leaves(data['fi']))
    count = 0
    for lang, values in data.items():
        fields = dict(leaves(values))
        comparable = lambda mapping: {k for k in mapping if not k.startswith('.meta.tricks.')}
        assert comparable(fields) == comparable(baseline), f'{lang}: missing/extra keys or list items'
        for key, value in fields.items():
            assert isinstance(value, str) and value.strip(), f'{lang}{key}: empty text'
            assert '\ufffd' not in value, f'{lang}{key}: broken Unicode'
            if key in baseline:
                placeholders = lambda text: {field for _, field, _, _ in Formatter().parse(text) if field}
                assert placeholders(value) == placeholders(baseline[key]), f'{lang}{key}: placeholders'
        if lang != 'fi':
            assert set(values['meta']['tricks']) == {'Etuvoltti', 'Takavoltti', 'Suora hyppy'}, lang
        prefix = '' if lang == 'fi' else lang + '/'
        for rel in PAGES + ['404.html']:
            file = ROOT / prefix / (rel if rel == '404.html' else rel + 'index.html')
            text = file.read_text(encoding='utf-8')
            parsed = Page(text)
            html = next(attrs for tag, attrs in parsed.tags if tag == 'html')
            assert html['lang'] == lang, file
            switches = [attrs for tag, attrs in parsed.tags if 'data-language' in attrs]
            assert {a['data-language'] for a in switches} == set(data), file
            for switch in switches:
                path = urlsplit(switch['href']).path
                target = ROOT / path.lstrip('/') / 'index.html'
                assert target.is_file(), f'{file}: {path}'
            if rel == '404.html':
                assert ('meta', {'name': 'robots', 'content': 'noindex'}) in parsed.tags, file
            else:
                alts = {a['hreflang']: a['href'] for tag, a in parsed.tags if tag == 'link' and a.get('rel') == 'alternate'}
                assert set(alts) == set(data) | {'x-default'}, file
                assert alts['x-default'] == 'https://worldtour.exsports.fi/en/' + rel, file
            if rel == 's/':
                assert 'worldtour.exsports.fi/' + prefix + 's/?id=esimerkki' in text, file
            if lang != 'fi' and rel in ['', 'lista/']:
                assert all(word not in text for word in ['Etuvoltti', 'Takavoltti', 'Suora hyppy']), file
            count += 1
    print(f'i18n ok: {len(data)} languages, {count} pages')


if __name__ == '__main__':
    check()
