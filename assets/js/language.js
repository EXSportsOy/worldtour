// Run before rendering: explicit URL, saved choice, browser languages, English.
(function () {
  var root = document.documentElement;
  var supported = root.dataset.languages.split(' ');
  var url = new URL(window.location.href);
  var prefix = url.pathname.split('/')[1];
  var explicitPath = supported.includes(prefix) && prefix !== 'fi' ? prefix : null;
  var requested = url.searchParams.get('lang');
  if (!supported.includes(requested)) requested = null;
  var saved = null;
  try { saved = localStorage.getItem('worldtour-language'); } catch (_) {}
  if (!supported.includes(saved)) saved = null;

  function browserLanguage() {
    var languages = navigator.languages && navigator.languages.length
      ? navigator.languages : [navigator.language || ''];
    for (var i = 0; i < languages.length; i++) {
      var lang = languages[i].toLowerCase().split(/[-_]/)[0];
      if (lang === 'nb' || lang === 'nn') lang = 'no';
      if (supported.includes(lang)) return lang;
    }
    return 'en';
  }

  var lang = explicitPath || requested || saved || browserLanguage();
  if (requested && !explicitPath) {
    try { localStorage.setItem('worldtour-language', lang); } catch (_) {}
  }
  var errorPage = root.dataset.page === '404';
  var target = errorPage
    ? '/' + (lang === 'fi' ? '' : lang + '/') + '404.html'
    : '/' + (lang === 'fi' ? '' : lang + '/') + root.dataset.page;
  // Preserve the missing URL for Finnish errors; other languages have their own page.
  if (errorPage && root.lang === lang) return;
  if (!errorPage && (explicitPath || lang === 'fi')) return;
  if (target !== url.pathname) {
    url.pathname = target;
    url.searchParams.delete('lang');
    window.location.replace(url.pathname + url.search + url.hash);
  }
}());
