/* cookie-consent.js — MyCalcTools */
(function () {
  'use strict';

  var CONSENT_KEY = 'cookieConsent';

  function getConsent() {
    try { return localStorage.getItem(CONSENT_KEY); } catch (e) { return null; }
  }

  function setConsent(value) {
    try { localStorage.setItem(CONSENT_KEY, value); } catch (e) {}
  }

  var ADSENSE_CLIENT = 'ca-pub-1904958390525375';

  function activateAds() {
    function fillSlots() {
      var ads = document.querySelectorAll('ins.adsbygoogle');
      ads.forEach(function (ins) {
        if (!ins.dataset.adsbygoogleStatus) {
          try { (window.adsbygoogle = window.adsbygoogle || []).push({}); } catch (e) {}
        }
      });
    }

    var existing = document.querySelector('script[data-consent-adsense]');
    if (existing) {
      if (existing.dataset.loaded === 'true') fillSlots();
      return;
    }

    var script = document.createElement('script');
    script.async = true;
    script.crossOrigin = 'anonymous';
    script.dataset.consentAdsense = 'true';
    script.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + ADSENSE_CLIENT;
    script.addEventListener('load', function () {
      script.dataset.loaded = 'true';
      fillSlots();
    });
    document.head.appendChild(script);
  }

  function buildBanner() {
    var banner = document.createElement('div');
    banner.id = 'mct-cookie-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-live', 'polite');
    banner.setAttribute('aria-label', 'Cookie consent');
    banner.style.cssText = [
      'position:fixed', 'bottom:0', 'left:0', 'right:0', 'z-index:99999',
      'background:rgba(8,8,20,0.97)', 'border-top:1px solid rgba(139,92,246,0.25)',
      'padding:16px 20px', 'display:flex', 'align-items:center',
      'justify-content:space-between', 'gap:16px', 'flex-wrap:wrap',
      'font-family:sans-serif', 'font-size:0.88rem', 'color:#cbd5e1',
      'backdrop-filter:blur(8px)'
    ].join(';');

    var msg = document.createElement('p');
    msg.style.cssText = 'margin:0;flex:1;min-width:200px;line-height:1.5';
    msg.innerHTML = 'We use cookies and local storage to remember your preferences and serve ads. ' +
      '<a href="/cookies" style="color:#a78bfa;text-decoration:underline">Cookie Policy</a> · ' +
      '<a href="/privacy" style="color:#a78bfa;text-decoration:underline">Privacy Policy</a>';

    var btns = document.createElement('div');
    btns.style.cssText = 'display:flex;gap:10px;flex-shrink:0';

    var acceptBtn = document.createElement('button');
    acceptBtn.textContent = 'Accept';
    acceptBtn.style.cssText = 'background:#8b5cf6;color:#fff;border:none;border-radius:8px;' +
      'padding:9px 18px;cursor:pointer;font-size:0.88rem;font-weight:600;white-space:nowrap';
    acceptBtn.addEventListener('click', function () {
      setConsent('granted');
      hideBanner();
      activateAds();
    });

    var declineBtn = document.createElement('button');
    declineBtn.textContent = 'Decline';
    declineBtn.style.cssText = 'background:transparent;color:#94a3b8;border:1px solid rgba(148,163,184,0.3);' +
      'border-radius:8px;padding:9px 18px;cursor:pointer;font-size:0.88rem;font-weight:600;white-space:nowrap';
    declineBtn.addEventListener('click', function () {
      setConsent('declined');
      hideBanner();
    });

    btns.appendChild(acceptBtn);
    btns.appendChild(declineBtn);
    banner.appendChild(msg);
    banner.appendChild(btns);
    return banner;
  }

  function hideBanner() {
    var b = document.getElementById('mct-cookie-banner');
    if (b) b.remove();
  }

  window.reopenCookiePreferences = function () {
    hideBanner();
    var banner = buildBanner();
    document.body.appendChild(banner);
  };

  function initConsent() {
    var consent = getConsent();
    if (consent === 'granted') {
      activateAds();
    } else if (consent !== 'declined') {
      document.body.appendChild(buildBanner());
    }
  }

  function ensureShellMounts() {
    if (!document.getElementById('brand-strip')) {
      var brand = document.createElement('div');
      brand.id = 'brand-strip';
      document.body.insertBefore(brand, document.body.firstChild);
    }
    if (!document.getElementById('nav')) {
      var nav = document.createElement('div');
      nav.id = 'nav';
      var brandStrip = document.getElementById('brand-strip');
      if (brandStrip && brandStrip.nextSibling) brandStrip.parentNode.insertBefore(nav, brandStrip.nextSibling);
      else document.body.insertBefore(nav, document.body.firstChild);
    }
    if (!document.getElementById('site-footer')) {
      var siteFooter = document.createElement('div');
      siteFooter.id = 'site-footer';
      document.body.appendChild(siteFooter);
    }
    if (!document.getElementById('group-footer')) {
      var groupFooter = document.createElement('div');
      groupFooter.id = 'group-footer';
      document.body.appendChild(groupFooter);
    }
  }

  function addApprovedVisualTreatment() {
    if (document.getElementById('mct-approved-shell-style')) return;
    var style = document.createElement('style');
    style.id = 'mct-approved-shell-style';
    style.textContent = [
      '.calc-card,.info-card,.related-card,.tool-info-panel,.card,.tool-card,.category-card,.static-content-section{background:linear-gradient(145deg,rgba(22,24,44,.96),rgba(13,15,30,.96));border-color:rgba(139,92,246,.28);box-shadow:0 10px 30px rgba(0,0,0,.2),0 0 18px rgba(6,214,255,.055)}',
      '.related-card:hover,.tool-card:hover,.category-card:hover,.info-card:hover{border-color:rgba(6,214,255,.38);box-shadow:0 12px 34px rgba(0,0,0,.24),0 0 22px rgba(139,92,246,.12)}',
      '.btn-calc,.btn-primary,.btn-finance,button[type="submit"]{box-shadow:0 0 18px rgba(139,92,246,.16)}'
    ].join('\n');
    document.head.appendChild(style);
  }

  function enforceApprovedAdgLogo() {
    var logos = document.querySelectorAll('.ascension-logo, img[alt="Ascension Digital"], img[alt="Ascension Digital Group"]');
    logos.forEach(function (img) {
      img.src = 'https://www.mycalendartools.net/assets/perf/ascension-digital.webp';
      img.style.objectFit = 'contain';
      img.style.height = 'auto';
    });
  }

  function loadSharedShell() {
    ensureShellMounts();
    addApprovedVisualTreatment();

    var staticFooter = document.getElementById('static-policy-footer');
    if (staticFooter) staticFooter.remove();

    var existing = Array.prototype.find.call(document.scripts, function (s) {
      return /(?:^|\/)script\.js(?:[?#]|$)/.test(s.getAttribute('src') || '');
    });

    if (!existing) {
      var shell = document.createElement('script');
      shell.src = '/script.js';
      shell.defer = false;
      shell.dataset.adgSharedShell = 'true';
      shell.addEventListener('load', function () {
        if (typeof window.initPage === 'function') window.initPage();
        enforceApprovedAdgLogo();
      });
      document.body.appendChild(shell);
    }

    var observer = new MutationObserver(function () { enforceApprovedAdgLogo(); });
    observer.observe(document.body, { childList: true, subtree: true });
    setTimeout(enforceApprovedAdgLogo, 0);
    setTimeout(enforceApprovedAdgLogo, 250);
  }

  function init() {
    loadSharedShell();
    initConsent();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
