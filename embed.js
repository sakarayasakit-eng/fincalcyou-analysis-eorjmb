/* fin·calc embeddable calculators — https://fincalcyou.com/embed.js
   Free to use. Paste a widget block (copy from https://fincalcyou.com/pages/embed.html)
   and include this script once. Pure client-side math, no network calls, no tracking.
   Keep the "by fin·calc" attribution link in the widget. */
(function () {
  var CSS = '.fc-embed{display:block;background:#fff;border:1px solid #e3e8ee;border-radius:16px;padding:16px;margin:14px 0;color:#1a2733;font-family:Inter,-apple-system,Segoe UI,Roboto,sans-serif;max-width:520px}.fc-embed *{box-sizing:border-box}.fc-embed .fc-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}@media(max-width:560px){.fc-embed .fc-grid{grid-template-columns:1fr}}.fc-embed label{display:block;font-size:11px;color:#5c6b7a;margin-bottom:5px;text-transform:uppercase;letter-spacing:.05em}.fc-embed .fc-in{display:flex;align-items:center;gap:6px;background:#f4f6f7;border:1px solid #e3e8ee;border-radius:9px;padding:7px 9px}.fc-embed .fc-in span{color:#5c6b7a;font-size:13px}.fc-embed .fc-in input{flex:1;width:100%;background:transparent;border:0;color:#1a2733;font-size:15px;font-weight:600;outline:none}.fc-embed .fc-head{font-size:12px;color:#5c6b7a;margin-top:16px}.fc-embed .fc-head strong{display:block;font-size:30px;color:#0e7a4a;font-weight:800;line-height:1.1;margin-top:2px}.fc-embed .fc-mini{display:flex;gap:18px;margin-top:10px;font-size:12px;color:#5c6b7a;flex-wrap:wrap}.fc-embed .fc-mini b{display:block;color:#1a2733;font-size:15px}.fc-embed .fc-bar{height:12px;border-radius:7px;overflow:hidden;display:flex;border:1px solid #e3e8ee;margin-top:12px}.fc-embed .fc-bar i{display:block;height:100%}.fc-embed .fc-note{font-size:11px;color:#5c6b7a;margin-top:8px}.fc-embed .fc-note a{color:#0e7a4a}';

  function injectCSS() {
    if (document.getElementById('fc-embed-css')) return;
    var s = document.createElement('style');
    s.id = 'fc-embed-css';
    s.textContent = CSS;
    (document.head || document.documentElement).appendChild(s);
  }

  // Math — identical to the formulas used on fincalcyou.com (verified against bank examples).
  function emi(P, r, y) { var n = Math.round(y * 12), m = r / 1200, e; if (m === 0) { e = P / n; } else { var g = Math.pow(1 + m, n); e = P * m * g / (g - 1); } var t = e * n; return { headline: e, a: P, b: t - P, total: t, aPct: Math.max(2, Math.min(98, P / t * 100)) }; }
  function fd(P, r, y) { var k = 4, M = P * Math.pow(1 + r / (100 * k), k * y); return { headline: M, a: P, b: M - P, total: M, aPct: Math.max(2, Math.min(98, P / M * 100)) }; }
  function sip(M, r, y) { var i = r / 1200, n = Math.round(y * 12), inv = M * n, fv = i === 0 ? inv : M * ((Math.pow(1 + i, n) - 1) / i) * (1 + i); return { headline: fv, a: inv, b: fv - inv, total: fv, aPct: Math.max(2, Math.min(98, inv / fv * 100)) }; }
  var ENG = { emi: emi, car: emi, fd: fd, sip: sip };

  function money(cur, loc, v) {
    var nf;
    try { nf = new Intl.NumberFormat(loc, { style: 'currency', currency: cur, maximumFractionDigits: 0 }); }
    catch (e) { nf = new Intl.NumberFormat('en', { maximumFractionDigits: 0 }); }
    return nf.format(Math.round(v));
  }

  function val(el, f) { var n = el.querySelector('[data-f="' + f + '"]'); return n ? parseFloat(n.value) : NaN; }

  function hydrate(el) {
    if (el.getAttribute('data-fc-ready')) return;
    var type = el.getAttribute('data-fincalc-embed'), eng = ENG[type];
    if (!eng) return;
    el.setAttribute('data-fc-ready', '1');
    var cur = el.getAttribute('data-cur') || 'USD', loc = el.getAttribute('data-locale') || 'en-US';
    var out = function (o) { return el.querySelector('[data-o="' + o + '"]'); };
    function calc() {
      var P = val(el, 'amount'), r = val(el, 'rate'), y = val(el, 'years');
      if (!(P > 0 && r >= 0 && y > 0)) return;
      var o = eng(P, r, y);
      if (out('headline')) out('headline').textContent = money(cur, loc, o.headline);
      if (out('a')) out('a').textContent = money(cur, loc, o.a);
      if (out('b')) out('b').textContent = money(cur, loc, o.b);
      if (out('total')) out('total').textContent = money(cur, loc, o.total);
      var ba = el.querySelector('[data-bar="a"]'), bb = el.querySelector('[data-bar="b"]');
      if (ba) ba.style.width = o.aPct.toFixed(1) + '%';
      if (bb) bb.style.width = (100 - o.aPct).toFixed(1) + '%';
    }
    el.addEventListener('input', calc);
    calc();
  }

  function init() {
    injectCSS();
    var els = document.querySelectorAll('[data-fincalc-embed]');
    for (var i = 0; i < els.length; i++) hydrate(els[i]);
  }

  if (document.readyState !== 'loading') init();
  else document.addEventListener('DOMContentLoaded', init);
})();
