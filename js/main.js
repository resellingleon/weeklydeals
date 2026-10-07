/* Weekly Deals – kein Framework, keine externen Skripte. */
(function () {
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* Navigation */
  var burger = $('.burger'), nav = $('#nav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open);
    });
  }

  /* Countdown bis Sonntag 23:59:59 (Ortszeit des Besuchers) */
  function weekEnd() {
    var n = new Date(), d = (7 - n.getDay()) % 7; // So = 0
    var e = new Date(n.getFullYear(), n.getMonth(), n.getDate() + d, 23, 59, 59);
    return e;
  }
  var cd = $('#countdown');
  if (cd) {
    var tick = function () {
      var s = Math.max(0, Math.floor((weekEnd() - new Date()) / 1000));
      var v = [Math.floor(s / 86400), Math.floor(s % 86400 / 3600), Math.floor(s % 3600 / 60), s % 60];
      $$('b', cd).forEach(function (b, i) { b.textContent = String(v[i]).padStart(2, '0'); });
    };
    tick(); setInterval(tick, 1000);
  }

  /* Filter (Wochendeals) */
  $$('.chip').forEach(function (c) {
    c.addEventListener('click', function () {
      $$('.chip').forEach(function (x) { x.setAttribute('aria-pressed', x === c); });
      var f = c.dataset.filter;
      $$('[data-cat]').forEach(function (d) { d.hidden = f !== 'alle' && d.dataset.cat !== f; });
    });
  });

  /* Einwilligung (Opt-in). Tracking nur nach Zustimmung. */
  var KEY = 'wd-consent', banner = $('#consent');
  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  function loadAnalytics() {
    /* HIER nach Zustimmung z. B. Plausible/GA4/Meta-Pixel einbinden.
       Beispiel: var s=document.createElement('script'); s.src='…'; s.defer=true; document.head.appendChild(s); */
    window.wdAnalytics = true;
  }
  if (get() === 'all') loadAnalytics();
  if (banner && !get()) banner.classList.add('show');
  $$('[data-consent]').forEach(function (b) {
    b.addEventListener('click', function () {
      set(b.dataset.consent); banner.classList.remove('show');
      if (b.dataset.consent === 'all') loadAnalytics();
    });
  });
  var reopen = $('#consent-open');
  if (reopen) reopen.addEventListener('click', function (e) { e.preventDefault(); banner.classList.add('show'); });

  /* Ziele messen: Anrufe, WhatsApp, Formular (nur mit Einwilligung) */
  window.wdTrack = function (name) {
    if (get() !== 'all') return;
    window.dataLayer = window.dataLayer || []; window.dataLayer.push({ event: name });
  };
  $$('a[href^="tel:"]').forEach(function (a) { a.addEventListener('click', function () { wdTrack('call_click'); }); });
  $$('a[href*="wa.me"]').forEach(function (a) { a.addEventListener('click', function () { wdTrack('whatsapp_click'); }); });

  /* Karte erst nach Klick laden (kein Datenabfluss vorab) */
  var mb = $('#map-load');
  if (mb) mb.addEventListener('click', function () {
    var box = mb.closest('.map-box');
    box.innerHTML = '<iframe title="Karte" loading="lazy" referrerpolicy="no-referrer" src="' + box.dataset.src + '"></iframe>';
  });

  /* Formulare: Honeypot + Zeitsperre als Spam-Schutz. */
  var t0 = Date.now();
  $$('form[data-form]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      var hp = $('.hp input', f);
      if ((hp && hp.value) || Date.now() - t0 < 3000) { e.preventDefault(); return; }
      wdTrack('form_submit');
      /* Entwurf: solange kein echtes Backend eingetragen ist, direkt zur Danke-Seite. */
      if (/PLATZHALTER/.test(f.getAttribute('action'))) { e.preventDefault(); location.href = f.dataset.thanks; }
    });
  });

  /* Deal aus Link ins Formular übernehmen */
  var m = $('#f-msg'), q = new URLSearchParams(location.search).get('deal');
  if (m && q) m.value = 'Ich interessiere mich für: ' + q;

  var y = $('#year'); if (y) y.textContent = new Date().getFullYear();
})();
