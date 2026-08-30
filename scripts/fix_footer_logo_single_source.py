from pathlib import Path

# 1) Stop cookie-consent from rewriting the footer image source.
p = Path('cookie-consent.js')
s = p.read_text()
old = """  function enforceApprovedAdgLogo() {
    var logos = document.querySelectorAll('.ascension-logo, img[alt=\"Ascension Digital\"], img[alt=\"Ascension Digital Group\"]');
    logos.forEach(function (img) {
      img.src = '/assets/perf/ascension-digital.webp';
      img.style.objectFit = 'contain';
      img.style.height = 'auto';
    });
  }
"""
new = """  function enforceApprovedAdgLogo() {
    // Presentation guard only. The logo source is owned by script.js so this
    // bootstrap cannot silently revert a footer-logo change in the browser.
    var logos = document.querySelectorAll('.ascension-logo, img[alt=\"Ascension Digital\"], img[alt=\"Ascension Digital Group\"]');
    logos.forEach(function (img) {
      img.style.objectFit = 'contain';
      img.style.height = 'auto';
    });
  }
"""
if old not in s:
    raise SystemExit('Expected cookie-consent logo rewriter block not found')
p.write_text(s.replace(old, new, 1))

# 2) Make integrity validation protect the local canonical asset instead of
# requiring the obsolete MyCalendarTools hotlink.
p = Path('scripts/validate-adsense-integrity.mjs')
s = p.read_text()
old_marker = "'mycalendartools.net/assets/perf/ascension-digital.webp'"
new_marker = "'/assets/perf/ascension-digital.webp'"
if old_marker not in s:
    raise SystemExit('Expected obsolete validator logo marker not found')
p.write_text(s.replace(old_marker, new_marker, 1))

# 3) Assert script.js remains the single source of truth for the footer image.
shell = Path('script.js').read_text()
if 'src=\"/assets/perf/ascension-digital.webp\"' not in shell:
    raise SystemExit('script.js is not using the canonical local Ascension asset')

print('Footer logo source conflict removed; validator aligned to canonical local asset.')
