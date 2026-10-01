// Keep filters/run IDs when switching language, and remember an explicit choice.
document.querySelectorAll('[data-language]').forEach(function (link) {
  var target = new URL(link.href);
  var current = new URL(window.location.href);
  target.search = current.search;
  target.searchParams.delete('lang');
  if (link.dataset.language === 'fi') target.searchParams.set('lang', 'fi');
  target.hash = current.hash;
  link.href = target.href;
  link.addEventListener('click', function () {
    try { localStorage.setItem('worldtour-language', link.dataset.language); } catch (_) {}
  });
});

// Kopioi linkki -nappi suorituksen sivulla.
document.querySelectorAll('[data-copy]').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var box = btn.closest('.exs-panel').querySelector('.linkbox');
    if (!box || !navigator.clipboard) return;
    navigator.clipboard.writeText('https://' + box.textContent.trim()).then(function () {
      var span = btn.querySelector('span'); var old = span.textContent;
      span.textContent = btn.getAttribute('data-copied') || 'Kopioitu'; setTimeout(function () { span.textContent = old; }, 1500);
    });
  });
});
