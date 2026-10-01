// Kopioi linkki -nappi suorituksen sivulla. Ei muuta ajonaikaista toimintaa.
document.querySelectorAll('[data-copy]').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var box = btn.closest('.exs-panel').querySelector('.linkbox');
    if (!box || !navigator.clipboard) return;
    navigator.clipboard.writeText('https://' + box.textContent.trim()).then(function () {
      var span = btn.querySelector('span'); var old = span.textContent;
      span.textContent = 'Kopioitu'; setTimeout(function () { span.textContent = old; }, 1500);
    });
  });
});
