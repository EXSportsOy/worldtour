const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { test } = require('node:test');

const root = path.join(__dirname, '..');
const languages = fs.readdirSync(path.join(root, 'i18n')).map(file => file.replace('.json', ''));
const source = fs.readFileSync(path.join(root, 'assets/js/language.js'), 'utf8');
function visit({ url = '/', browser = ['en-US'], saved = null, page = '', lang = 'fi', blocked = false } = {}) {
  const redirects = [];
  const storage = {
    getItem() { if (blocked) throw Error('Storage blocked'); return saved; },
    setItem(key, value) { if (blocked) throw Error('Storage blocked'); saved = value; }
  };
  vm.runInNewContext(source, {
    document: { documentElement: { lang, dataset: { languages: languages.join(' '), page } } },
    window: { location: { href: 'https://worldtour.exsports.fi' + url, replace: url => redirects.push(url) } },
    navigator: { languages: browser, language: browser[0] }, localStorage: storage, URL
  });
  return { redirects, saved };
}

for (const lang of languages) {
  test('browser preference: ' + lang, () => {
    assert.deepEqual(visit({ browser: [lang + '-XX'] }).redirects, lang === 'fi' ? [] : ['/' + lang + '/']);
  });
  if (lang !== 'fi') test('explicit URL wins: ' + lang, () => {
    assert.deepEqual(visit({ url: '/' + lang + '/lista/', lang, page: 'lista/', saved: 'fi' }).redirects, []);
  });
}
test('unsupported, absent and corrupt preferences fall back to English', () => {
  for (const browser of [['ja-JP'], ['ru', 'zh-CN'], [], ['']]) {
    assert.deepEqual(visit({ browser, saved: 'invalid' }).redirects, ['/en/']);
  }
});
test('first supported browser preference wins, including regional variants', () => {
  assert.deepEqual(visit({ browser: ['ja', 'pt-BR', 'en'] }).redirects, ['/pt/']);
  assert.deepEqual(visit({ browser: ['SV-fi', 'de'] }).redirects, ['/sv/']);
  for (const browser of [['nb-NO'], ['nn-NO'], ['no-NO']]) {
    assert.deepEqual(visit({ browser }).redirects, ['/no/']);
  }
});
test('saved choice wins over browser preference', () => {
  assert.deepEqual(visit({ saved: 'de', browser: ['fi'] }).redirects, ['/de/']);
  assert.deepEqual(visit({ saved: 'fi', browser: ['en'] }).redirects, []);
});
test('explicit Finnish works even with storage blocked', () => {
  for (const blocked of [false, true]) {
    assert.deepEqual(visit({ url: '/?lang=fi', saved: 'de', blocked }).redirects, []);
  }
  assert.equal(visit({ url: '/?lang=fi', saved: 'de' }).saved, 'fi');
  assert.deepEqual(visit({ blocked: true, browser: ['ja'] }).redirects, ['/en/']);
});
test('deep links retain query parameters and fragment', () => {
  assert.deepEqual(visit({ url: '/s/?id=abc#video', page: 's/', browser: ['de'] }).redirects, ['/de/s/?id=abc#video']);
  assert.deepEqual(visit({ url: '/lista/index.html?rinne=m', page: 'lista/', browser: ['en'] }).redirects, ['/en/lista/?rinne=m']);
});
test('404 uses requested path language, otherwise preferences, without loops', () => {
  assert.deepEqual(visit({ url: '/de/missing', page: '404', browser: ['fi'] }).redirects, ['/de/404.html']);
  assert.deepEqual(visit({ url: '/missing', page: '404', browser: ['ja'] }).redirects, ['/en/404.html']);
  assert.deepEqual(visit({ url: '/en/404.html', page: '404', lang: 'en' }).redirects, []);
  assert.deepEqual(visit({ url: '/missing', page: '404', browser: ['fi'] }).redirects, []);
});
test('language menu keeps run, slope and fragment and remembers the choice', () => {
  const links = languages.map(lang => ({
    href: 'https://worldtour.exsports.fi/' + (lang === 'fi' ? '' : lang + '/') + 'lista/',
    dataset: { language: lang }, addEventListener(event, handler) { this.click = handler; }
  }));
  let choice;
  vm.runInNewContext(fs.readFileSync(path.join(root, 'assets/js/site.js'), 'utf8'), {
    document: { querySelectorAll: selector => selector === '[data-language]' ? links : [] },
    window: { location: { href: 'https://worldtour.exsports.fi/de/lista/?rinne=m&id=abc#omat' } },
    localStorage: { setItem: (key, value) => { choice = value; } }, URL
  });
  for (const link of links) {
    const url = new URL(link.href);
    assert.equal(url.searchParams.get('rinne'), 'm');
    assert.equal(url.searchParams.get('id'), 'abc');
    assert.equal(url.hash, '#omat');
    assert.equal(url.searchParams.get('lang'), link.dataset.language === 'fi' ? 'fi' : null);
    link.click();
    assert.equal(choice, link.dataset.language);
  }
});
