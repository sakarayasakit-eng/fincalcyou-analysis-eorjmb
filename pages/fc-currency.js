/* fin·calc — shared currency helper for /pages/ landing calculators.
   Reads/writes the SAME localStorage key ('fincalc_cur') the homepage uses,
   so a currency chosen here syncs with the main app and vice-versa.
   Exposes window.FCCUR = { code(), cur(), sym(), money(v) }.
   Also injects a currency picker into the first .fc-embed and swaps the
   input "$" prefixes to the visitor's currency symbol. No dependencies. */
(function () {
  var CURRENCIES = [
    { sym: '₨', code: 'PKR', name: 'Pakistani Rupee', flag: '🇵🇰' },
    { sym: '৳', code: 'BDT', name: 'Bangladeshi Taka', flag: '🇧🇩' },
    { sym: '$', code: 'USD', name: 'US Dollar', flag: '🇺🇸' },
    { sym: '€', code: 'EUR', name: 'Euro', flag: '🇪🇺' },
    { sym: '£', code: 'GBP', name: 'British Pound', flag: '🇬🇧' },
    { sym: '₹', code: 'INR', name: 'Indian Rupee', flag: '🇮🇳' },
    { sym: '¥', code: 'JPY', name: 'Japanese Yen', flag: '🇯🇵' },
    { sym: '¥', code: 'CNY', name: 'Chinese Yuan', flag: '🇨🇳' },
    { sym: 'د.إ', code: 'AED', name: 'UAE Dirham', flag: '🇦🇪' },
    { sym: 'ر.س', code: 'SAR', name: 'Saudi Riyal', flag: '🇸🇦' },
    { sym: 'ر.ق', code: 'QAR', name: 'Qatari Riyal', flag: '🇶🇦' },
    { sym: 'د.ك', code: 'KWD', name: 'Kuwaiti Dinar', flag: '🇰🇼' },
    { sym: 'ر.ع', code: 'OMR', name: 'Omani Rial', flag: '🇴🇲' },
    { sym: '.د.ب', code: 'BHD', name: 'Bahraini Dinar', flag: '🇧🇭' },
    { sym: 'د.أ', code: 'JOD', name: 'Jordanian Dinar', flag: '🇯🇴' },
    { sym: 'ل.ل', code: 'LBP', name: 'Lebanese Pound', flag: '🇱🇧' },
    { sym: 'ج.م', code: 'EGP', name: 'Egyptian Pound', flag: '🇪🇬' },
    { sym: '₺', code: 'TRY', name: 'Turkish Lira', flag: '🇹🇷' },
    { sym: 'NPR', code: 'NPR', name: 'Nepalese Rupee', flag: '🇳🇵' },
    { sym: '₨', code: 'LKR', name: 'Sri Lankan Rupee', flag: '🇱🇰' },
    { sym: '؋', code: 'AFN', name: 'Afghan Afghani', flag: '🇦🇫' },
    { sym: '﷼', code: 'IRR', name: 'Iranian Rial', flag: '🇮🇷' },
    { sym: 'RM', code: 'MYR', name: 'Malaysian Ringgit', flag: '🇲🇾' },
    { sym: 'S$', code: 'SGD', name: 'Singapore Dollar', flag: '🇸🇬' },
    { sym: 'Rp', code: 'IDR', name: 'Indonesian Rupiah', flag: '🇮🇩' },
    { sym: '฿', code: 'THB', name: 'Thai Baht', flag: '🇹🇭' },
    { sym: '₱', code: 'PHP', name: 'Philippine Peso', flag: '🇵🇭' },
    { sym: '₫', code: 'VND', name: 'Vietnamese Dong', flag: '🇻🇳' },
    { sym: '₩', code: 'KRW', name: 'South Korean Won', flag: '🇰🇷' },
    { sym: 'NT$', code: 'TWD', name: 'Taiwan Dollar', flag: '🇹🇼' },
    { sym: 'HK$', code: 'HKD', name: 'Hong Kong Dollar', flag: '🇭🇰' },
    { sym: 'A$', code: 'AUD', name: 'Australian Dollar', flag: '🇦🇺' },
    { sym: 'C$', code: 'CAD', name: 'Canadian Dollar', flag: '🇨🇦' },
    { sym: 'NZ$', code: 'NZD', name: 'New Zealand Dollar', flag: '🇳🇿' },
    { sym: 'Fr', code: 'CHF', name: 'Swiss Franc', flag: '🇨🇭' },
    { sym: 'kr', code: 'SEK', name: 'Swedish Krona', flag: '🇸🇪' },
    { sym: 'kr', code: 'NOK', name: 'Norwegian Krone', flag: '🇳🇴' },
    { sym: 'kr', code: 'DKK', name: 'Danish Krone', flag: '🇩🇰' },
    { sym: 'zł', code: 'PLN', name: 'Polish Zloty', flag: '🇵🇱' },
    { sym: 'Kč', code: 'CZK', name: 'Czech Koruna', flag: '🇨🇿' },
    { sym: '₴', code: 'UAH', name: 'Ukrainian Hryvnia', flag: '🇺🇦' },
    { sym: '₽', code: 'RUB', name: 'Russian Ruble', flag: '🇷🇺' },
    { sym: 'R$', code: 'BRL', name: 'Brazilian Real', flag: '🇧🇷' },
    { sym: 'MX$', code: 'MXN', name: 'Mexican Peso', flag: '🇲🇽' },
    { sym: 'AR$', code: 'ARS', name: 'Argentine Peso', flag: '🇦🇷' },
    { sym: '₦', code: 'NGN', name: 'Nigerian Naira', flag: '🇳🇬' },
    { sym: 'KSh', code: 'KES', name: 'Kenyan Shilling', flag: '🇰🇪' },
    { sym: 'R', code: 'ZAR', name: 'South African Rand', flag: '🇿🇦' },
    { sym: 'GH₵', code: 'GHS', name: 'Ghanaian Cedi', flag: '🇬🇭' },
    { sym: 'TSh', code: 'TZS', name: 'Tanzanian Shilling', flag: '🇹🇿' },
    { sym: 'UGX', code: 'UGX', name: 'Ugandan Shilling', flag: '🇺🇬' }
  ];
  var byCode = {};
  CURRENCIES.forEach(function (c) { byCode[c.code] = c; });

  function code() {
    try {
      var c = localStorage.getItem('fincalc_cur');
      if (c) { c = c.toUpperCase(); if (byCode[c]) return c; }
    } catch (e) {}
    return 'USD';
  }
  function cur() { return byCode[code()] || byCode.USD; }
  function sym() { return cur().sym; }

  var grp = new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 });
  function money(v) { return sym() + grp.format(Math.round(v || 0)); }

  window.FCCUR = { CURRENCIES: CURRENCIES, code: code, cur: cur, sym: sym, money: money };

  function applySymbols() {
    try {
      var spans = document.querySelectorAll('.fc-embed .fc-in span');
      Array.prototype.forEach.call(spans, function (s) {
        var t = s.textContent.trim();
        if (t === '$' || s.getAttribute('data-fcsym') === '1') {
          s.textContent = sym();
          s.setAttribute('data-fcsym', '1');
        }
      });
    } catch (e) {}
  }

  function injectSelector() {
    var embed = document.querySelector('.fc-embed');
    if (!embed || document.getElementById('fc-cur-sel')) return;
    var wrap = document.createElement('div');
    wrap.style.cssText = 'display:flex;justify-content:flex-end;align-items:center;gap:6px;margin:-2px 0 12px;font-size:12px;color:#5c6b7a;';
    var lbl = document.createElement('label');
    lbl.textContent = 'Currency';
    lbl.setAttribute('for', 'fc-cur-sel');
    var sel = document.createElement('select');
    sel.id = 'fc-cur-sel';
    sel.setAttribute('aria-label', 'Display currency');
    sel.style.cssText = 'background:#f4f6f7;border:1px solid #e3e8ee;border-radius:8px;padding:5px 8px;font-size:13px;color:#1a2733;font-family:inherit;font-weight:600;cursor:pointer;max-width:200px;';
    var cc = code();
    sel.innerHTML = CURRENCIES.map(function (c) {
      return '<option value="' + c.code + '"' + (c.code === cc ? ' selected' : '') + '>' + c.flag + ' ' + c.code + ' (' + c.sym + ')</option>';
    }).join('');
    sel.addEventListener('change', function () {
      try { localStorage.setItem('fincalc_cur', sel.value); } catch (e) {}
      location.reload();
    });
    wrap.appendChild(lbl);
    wrap.appendChild(sel);
    embed.insertBefore(wrap, embed.firstChild);
  }

  function init() { injectSelector(); applySymbols(); }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
