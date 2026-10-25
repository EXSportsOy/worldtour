// Suorituksen sivu (/s/?season=&row=, tarkistuslista 3.5). Hakee yhden World Rank -rivin ja pelaajan muut rinteet
// samasta osoitteesta /api/**-ohjauksen kautta (ei CORSia, CSP connect-src 'self'). Jakolinkki /s/{kausi}/{rivi}
// ohjautuu Cloud Runiin, joka antaa esikatselun ja palauttaa selaimen tänne. Staattinen HTML on rehellinen tila
// ilman riviä; nimimerkit ovat käyttäjien sisältöä, joten ne kirjoitetaan vain textContentilla.
(function () {
  var root = document.getElementById('suoritus');
  if (!root || !window.fetch || !window.Promise) return;

  var TIMEOUT = 10000;
  var part = function (name) { return document.querySelector('[data-run-' + name + ']'); };
  var name = part('name'), meta = part('meta'), total = part('total'), score = part('score'), place = part('place');
  var status = part('status'), retry = part('retry'), crumb = part('crumb');
  var share = part('share'), link = part('link'), others = part('others'), othersList = part('others-list');
  var text = function (key) { return root.dataset['t' + key] || ''; };
  var lang = document.documentElement.lang;
  var locale = lang === 'no' ? 'nb' : lang === 'en' ? 'en-GB' : lang;
  var opensAt = Date.parse(root.dataset.opens);
  var SLOPES = { Small: 'S', Medium: 'M', Large: 'L' };

  var seasonId = null, rowId = null;
  try {
    var params = new URL(window.location.href).searchParams;
    seasonId = params.get('season');
    rowId = params.get('row');
  } catch (_) {}
  if (!/^[a-z0-9][a-z0-9_-]{0,63}$/.test(seasonId || '') || !/^[0-9a-f]{32}$/.test(rowId || '')) {
    // Ilman riviä: ennen Season 1:tä avautumisteksti (staattinen), sen jälkeen ohje valita suoritus listalta.
    if (Date.now() >= opensAt) status.textContent = text('Notice');
    return;
  }

  function number(value) {
    try { return Number(value).toLocaleString(locale); } catch (_) { return String(value); }
  }

  function seasonName(id) {
    var match = /^season[-_ ]?(\d+)$/i.exec(id);
    return match ? 'Season ' + match[1] : id;
  }

  function slopeName(kicker) {
    var key = SLOPES[kicker];
    return key ? root.dataset['slope' + key] || key : '';
  }

  function placeText(entry) { return text('Place').replace('{n}', number(entry.placement)); }

  function valid(entry) {
    return entry && typeof entry.placement === 'number' && entry.placement >= 1 && typeof entry.officialScore === 'number' && isFinite(entry.officialScore);
  }

  function setStatus(message, busy) {
    status.textContent = message;
    status.hidden = !message;
    root.setAttribute('aria-busy', busy ? 'true' : 'false');
  }

  // 404 JSON-vastauksena: rivi tai kausi puuttuu. Muu virhe (Hostingin 404-sivu, 503, aikakatkaisu) on häiriö.
  function fetchRow() {
    var controller = window.AbortController ? new AbortController() : null;
    var timer = controller ? setTimeout(function () { controller.abort(); }, TIMEOUT) : 0;
    var path = '/api/seasons/' + encodeURIComponent(seasonId) + '/rows/' + rowId;
    return fetch(path, { headers: { Accept: 'application/json' }, credentials: 'omit', signal: controller ? controller.signal : undefined })
      .then(function (res) {
        clearTimeout(timer);
        var json = /^application\/json\b/i.test(res.headers.get('Content-Type') || '');
        if (res.status === 404 && json) return { missing: true };
        if (!res.ok || !json) throw new Error('HTTP ' + res.status);
        return res.json();
      }, function (error) { clearTimeout(timer); throw error; });
  }

  function load() {
    retry.hidden = true;
    setStatus(text('Loading'), true);
    fetchRow().then(function (data) {
      if (data.missing || !data.entry || !valid(data.entry)) {
        setStatus(text('Missing'), false);
        return;
      }
      show(data);
    }).catch(function () {
      if (Date.now() < opensAt) return setStatus(text('ClosedP'), false);
      setStatus(text('Error'), false);
      retry.hidden = false;
    });
  }

  function show(data) {
    var entry = data.entry;
    var nickname = typeof entry.nickname === 'string' && entry.nickname.trim() ? entry.nickname : null;
    name.textContent = nickname || text('Hidden');
    if (nickname) name.dir = 'auto'; else name.classList.add('wr-hidden');
    meta.textContent = seasonName(data.seasonId) + ' · ' + slopeName(data.kicker);
    meta.hidden = false;
    score.textContent = number(entry.officialScore);
    place.textContent = placeText(entry);
    total.hidden = false;
    crumb.textContent = slopeName(data.kicker) + ' · ' + placeText(entry);
    document.title = (nickname || text('Hidden')) + ' · ' + placeText(entry) + ' – EXS World Tour';
    // site.js lisää kopioidessa laatikon tekstin eteen skeeman, joten laatikossa on osoite ilman sitä.
    link.textContent = root.dataset.share.replace(/^https:\/\//, '') + encodeURIComponent(seasonId) + '/' + rowId;
    share.hidden = false;
    while (othersList.firstChild) othersList.removeChild(othersList.firstChild);
    (Array.isArray(data.others) ? data.others : []).forEach(function (other) {
      if (!other || !valid(other.entry) || !/^[0-9a-f]{32}$/.test(other.entry.rowId || '')) return;
      var item = document.createElement('a');
      item.className = 'row-between';
      item.href = '?season=' + encodeURIComponent(seasonId) + '&row=' + other.entry.rowId;
      var label = document.createElement('span');
      label.textContent = slopeName(other.kicker);
      var value = document.createElement('span');
      value.className = 'display-xs';
      value.style.color = 'var(--text)';
      value.textContent = number(other.entry.placement) + ' · ' + number(other.entry.officialScore);
      item.appendChild(label);
      item.appendChild(value);
      othersList.appendChild(item);
    });
    others.hidden = !othersList.firstChild;
    setStatus('', false);
  }

  retry.addEventListener('click', load);
  load();
}());
