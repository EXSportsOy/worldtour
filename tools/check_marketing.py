"""Check the approved price and prevent preview pages claiming live services."""
import json
import re
from pathlib import Path
from check_i18n import Page

ROOT = Path(__file__).resolve().parents[1]


def check():
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
            assert data['availability'] in html, f'{lang}/{route}: missing availability'
            assert 'play.google.com/store/apps/details' not in html, f'{lang}/{route}: premature store CTA'
            assert not any(tag == 'a' and a.get('aria-disabled') == 'true' for tag, a in parsed.tags), f'{lang}/{route}: placeholder link'
            if route in ('', 'nain-pelaat/'):
                assert data['purchase_scope'] in html, f'{lang}/{route}: missing purchase scope'
                assert data['offer'] in html, f'{lang}/{route}: missing regional price disclosure'
            if route == '':
                ticker = re.search(r'class="exs-ticker".*?</a>', html, re.S)
                assert ticker and data['sample'] in ticker.group(), f'{lang}: unlabelled sample ticker'
            if route in ('lista/', 's/'):
                assert ('meta', {'name': 'robots', 'content': 'noindex'}) in parsed.tags, f'{lang}/{route}: demo indexed'
                assert 'kausi-1' not in html and 'kausi=arkisto' not in html, f'{lang}: misleading season'
                assert 'video__play' not in html and 'exs-badge--verified' not in html, f'{lang}: fake video/verification'
                assert not any(tag == 'a' and a.get('href') == '#' for tag, a in parsed.tags), f'{lang}: dummy action'
    print('marketing ok: 15 languages; price, scope, availability and demo behaviour')


if __name__ == '__main__':
    check()
