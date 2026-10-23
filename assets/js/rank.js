// World Rank -lista (/lista/). Hakee kaudet ja tulokset samasta osoitteesta /api/**-ohjauksen
// kautta (ei CORSia, ei Firebase SDK:ta, CSP connect-src 'self'). Staattinen HTML näyttää
// "avautuu"-tilan; tämä korvaa sen oikealla datalla, kun palvelu vastaa. Nimimerkit ovat
// käyttäjien sisältöä, joten ne kirjoitetaan vain textContentilla.
(function () {
  var root = document.getElementById('lista');
  if (!root || !window.fetch || !window.Promise) return;

  var PAGE = 25;            // arkiston rivit näytetään samoissa erissä kuin palvelimen sivut
  var TIMEOUT = 10000;
  var ENDED = ['finalized', 'archived'];
  var part = function (name) { return root.querySelector('[data-wr-' + name + ']'); };
  var title = part('title'), badge = part('season'), tabsBox = part('tabs'), board = part('board');
  var status = part('status'), retry = part('retry'), meta = part('meta'), more = part('more');
  var tabs = Array.prototype.slice.call(tabsBox.querySelectorAll('[data-slope]'));
  var text = function (key) { return root.dataset['t' + key] || ''; };
  var lang = document.documentElement.lang;
  var locale = lang === 'no' ? 'nb' : lang === 'en' ? 'en-GB' : lang;
  var opensAt = Date.parse(root.dataset.opens);

  var season = null, source = 'rankings', cache = {}, generation = 0, retryAction = null;
  var slope = 'S';
  try {
    var wanted = (new URL(window.location.href).searchParams.get('rinne') || root.dataset.rinne || '').toUpperCase();
    if (wanted === 'S' || wanted === 'M' || wanted === 'L') slope = wanted;
  } catch (_) {}

  function getJson(path) {
    var controller = window.AbortController ? new AbortController() : null;
    var timer = controller ? setTimeout(function () { controller.abort(); }, TIMEOUT) : 0;
    return fetch(path, { headers: { Accept: 'application/json' }, credentials: 'omit', signal: controller ? controller.signal : undefined })
      .then(function (res) {
        // Suljettu palvelu: Hostingin 404-sivu, 503 tai muu kuin JSON on aina virhe.
        if (!res.ok || !/^application\/json\b/i.test(res.headers.get('Content-Type') || '')) throw new Error('HTTP ' + res.status);
        return res.json();
      })
      .then(function (data) { clearTimeout(timer); return data; }, function (error) { clearTimeout(timer); throw error; });
  }

  function number(value) {
    try { return Number(value).toLocaleString(locale); } catch (_) { return String(value); }
  }

  function day(iso) {
    var date = new Date(iso);
    if (isNaN(date.getTime())) return '';
    try { return new Intl.DateTimeFormat(locale, { dateStyle: 'medium', timeZone: 'UTC' }).format(date); } catch (_) { return date.toISOString().slice(0, 10); }
  }

  function seasonName(id) {
    var match = /^season[-_ ]?(\d+)$/i.exec(id);
    return match ? 'Season ' + match[1] : id;
  }

  // Käynnissä oleva kausi ensin, sitten vahvistettavana oleva, sitten viimeisin päättynyt.
  function pick(list) {
    var seasons = list && Array.isArray(list.seasons) ? list.seasons.filter(function (s) {
      return s && typeof s.seasonId === 'string' && s.seasonId && typeof s.state === 'string';
    }) : [];
    function latest(states) {
      return seasons.filter(function (s) { return states.indexOf(s.state) >= 0; })
        .sort(function (a, b) { return (Date.parse(b.endUtc) || 0) - (Date.parse(a.endUtc) || 0); })[0] || null;
    }
    return latest(['open']) || latest(['closing']) || latest(ENDED);
  }

  function valid(entry) {
    return entry && typeof entry.placement === 'number' && entry.placement >= 1 && typeof entry.officialScore === 'number' && isFinite(entry.officialScore);
  }

  function base() { return '/api/seasons/' + encodeURIComponent(season.seasonId); }

  function setStatus(message, busy) {
    status.textContent = message;
    status.hidden = !message;
    root.setAttribute('aria-busy', busy ? 'true' : 'false');
  }

  function hideData() {
    board.hidden = true;
    more.hidden = true;
    retry.hidden = true;
  }

  function loading() {
    hideData();
    setStatus(text('Loading'), true);
  }

  function closed() {
    season = null;
    hideData();
    badge.hidden = true;
    tabsBox.hidden = true;
    meta.textContent = '';
    title.textContent = text('ClosedH');
    setStatus(text('ClosedP'), false);
  }

  function unavailable(action) {
    hideData();
    setStatus(text('Error'), false);
    retryAction = action;
    retry.hidden = false;
  }

  // Epäonnistunut kausihaku ennen Season 1:n alkua on suljettu palvelu, sen jälkeen häiriö.
  function failed() {
    if (Date.now() < opensAt) return closed();
    season = null;
    badge.hidden = true;
    tabsBox.hidden = true;
    meta.textContent = '';
    title.textContent = 'World Rank';
    unavailable(start);
  }

  function start() {
    var current = ++generation;
    cache = {};
    title.textContent = 'World Rank';
    loading();
    getJson('/api/seasons').then(function (list) {
      if (current !== generation) return;
      season = pick(list);
      if (!season) return failed();
      source = season.archiveVersion >= 1 && ENDED.indexOf(season.state) >= 0 ? 'archive' : 'rankings';
      if (source === 'rankings') return ready();
      return getJson(base() + '/archive').then(function (archive) {
        if (current !== generation) return;
        var slopes = archive && archive.slopes || {};
        ['S', 'M', 'L'].forEach(function (key) {
          var rows = slopes[key] && Array.isArray(slopes[key].entries) ? slopes[key].entries.filter(valid) : [];
          cache[key] = { rows: rows, shown: Math.min(PAGE, rows.length), loaded: true, done: true };
        });
        ready();
      });
    }).catch(function () {
      if (current === generation) failed();
    });
  }

  function ready() {
    var state = season.state === 'open' ? text('Open') : season.state === 'closing' ? text('Closing') : text('Final');
    badge.textContent = seasonName(season.seasonId) + ' · ' + state;
    badge.hidden = false;
    var from = day(season.startUtc), to = day(season.endUtc);
    meta.textContent = from && to ? from + '–' + to : '';
    tabsBox.hidden = false;
    select(slope, false);
  }

  function select(next, fromUser) {
    slope = next;
    tabs.forEach(function (tab) {
      var on = tab.dataset.slope === slope;
      tab.setAttribute('aria-selected', on ? 'true' : 'false');
      tab.tabIndex = on ? 0 : -1;
      if (on) {
        board.setAttribute('aria-labelledby', tab.id);
        title.textContent = tab.textContent;
      }
    });
    if (fromUser) remember();
    if (cache[slope] && cache[slope].loaded) render(); else load();
  }

  function load() {
    var key = slope, current = generation;
    var entry = cache[key] || (cache[key] = { rows: [], shown: 0, cursor: null, loaded: false, done: false });
    if (source === 'archive') {
      entry.shown = Math.min(entry.rows.length, entry.shown + PAGE);
      return render();
    }
    if (entry.busy) return;
    entry.busy = true;
    entry.failed = false;
    if (entry.loaded) more.disabled = true; else loading();
    var path = base() + '/rankings?slope=' + key + (entry.cursor ? '&cursor=' + encodeURIComponent(entry.cursor) : '');
    getJson(path).then(function (page) {
      if (!page || !Array.isArray(page.entries)) throw new Error('Unexpected response');
      entry.rows = entry.rows.concat(page.entries.filter(valid));
      entry.shown = entry.rows.length;
      entry.cursor = typeof page.nextCursor === 'string' && page.nextCursor ? page.nextCursor : null;
      entry.done = !entry.cursor;
      entry.loaded = true;
    }).catch(function () {
      entry.failed = true;
    }).then(function () {
      entry.busy = false;
      more.disabled = false;
      if (current === generation && key === slope) render();
    });
  }

  function cell(className, value) {
    var span = document.createElement('span');
    span.className = className;
    span.textContent = value;
    return span;
  }

  function row(entry) {
    var item = document.createElement('li');
    item.className = 'exs-row' + (entry.placement <= 3 ? ' exs-row--podium' : '') + (entry.self ? ' exs-row--me' : '');
    var nickname = typeof entry.nickname === 'string' && entry.nickname.trim() ? entry.nickname : null;
    var who = document.createElement('span');
    var name = cell('exs-row__name' + (nickname ? '' : ' wr-hidden'), nickname || text('Hidden'));
    if (nickname) name.dir = 'auto';
    who.appendChild(name);
    item.appendChild(cell('exs-row__rank', number(entry.placement)));
    item.appendChild(who);
    item.appendChild(cell('exs-row__score', number(entry.officialScore)));
    return item;
  }

  function render() {
    var entry = cache[slope];
    retry.hidden = true;
    if (!entry.loaded) {
      if (entry.failed) unavailable(load); else loading();
      return;
    }
    if (!entry.rows.length) {
      hideData();
      setStatus(text('Empty'), false);
      return;
    }
    var list = document.createDocumentFragment();
    entry.rows.slice(0, entry.shown).forEach(function (item) { list.appendChild(row(item)); });
    while (board.firstChild) board.removeChild(board.firstChild);
    board.appendChild(list);
    board.hidden = false;
    // Jatkosivun virhe näytetään listan alla; "Näytä lisää" yrittää samaa kursoria uudelleen.
    setStatus(entry.failed ? text('Error') : '', false);
    more.hidden = source === 'archive' ? entry.shown >= entry.rows.length : entry.done;
  }

  // Valittu rinne osoitteeseen (?rinne=m) ja kielivalikon linkkeihin, kuten site.js tekee latauksessa.
  function remember() {
    var value = slope.toLowerCase();
    try {
      var url = new URL(window.location.href);
      url.searchParams.set('rinne', value);
      window.history.replaceState(null, '', url.pathname + url.search + url.hash);
    } catch (_) {}
    document.querySelectorAll('[data-language]').forEach(function (link) {
      var target = new URL(link.href);
      target.searchParams.set('rinne', value);
      link.href = target.href;
    });
  }

  tabs.forEach(function (tab, index) {
    tab.addEventListener('click', function () {
      if (tab.dataset.slope !== slope) select(tab.dataset.slope, true);
    });
    tab.addEventListener('keydown', function (event) {
      var to = { ArrowRight: index + 1, ArrowLeft: index - 1, Home: 0, End: tabs.length - 1 }[event.key];
      if (to === undefined) return;
      event.preventDefault();
      var target = tabs[(to + tabs.length) % tabs.length];
      target.focus();
      if (target.dataset.slope !== slope) select(target.dataset.slope, true);
    });
  });
  more.addEventListener('click', function () { if (season) load(); });
  retry.addEventListener('click', function () { if (retryAction) retryAction(); });

  start();
}());
