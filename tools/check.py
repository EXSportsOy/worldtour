"""Tarkistaa, että sivuston sisäiset linkit ja tiedostoviittaukset osoittavat olemassa oleviin tiedostoihin."""
import os, re, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bad = []
for d, _, files in os.walk(root):
    if '/.git' in d or '/.github' in d or '/node_modules' in d: continue
    for f in files:
        if not f.endswith('.html'): continue
        p = os.path.join(d, f)
        html = open(p, encoding='utf-8').read()
        for m in re.finditer(r'(?:href|src)="(/[^"#?]*)', html):
            t = m.group(1)
            fs = os.path.join(root, t.lstrip('/'))
            if t.endswith('/'): fs = os.path.join(fs, 'index.html')
            if not os.path.exists(fs): bad.append(f'{os.path.relpath(p, root)}: {t}')
        
if bad:
    print('\n'.join(bad)); sys.exit(1)
print('linkit ok')

from check_i18n import check
check()
