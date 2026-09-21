(function () {
  var overlay = document.getElementById('loadingOverlay');
  if (!overlay) return;
  function show() { overlay.classList.add('show'); }
  function hide() { overlay.classList.remove('show'); }
  window.addEventListener('pageshow', hide);
  document.addEventListener('submit', function () { show(); }, true);
  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    var href = a.getAttribute('href');
    if (!href || href.charAt(0) === '#' || href.indexOf('javascript:') === 0) return;
    if (a.target === '_blank' || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    try {
      if (new URL(a.href, window.location.href).origin !== window.location.origin) return;
    } catch (err) { return; }
    show();
  }, true);
})();
