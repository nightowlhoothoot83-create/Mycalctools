from pathlib import Path
import sys

APPROVED_LOGO = 'https://www.mycalendartools.net/assets/perf/ascension-digital.webp'
LEGACY_LOGOS = [
    '/assets/perf/ascension-digital-logo.webp',
    '/ascension-digital-logo.jpg',
    'logo-ascension-digital.png',
]

errors = []
html_files = [p for p in Path('.').rglob('*.html') if '.git' not in p.parts]
for p in html_files:
    text = p.read_text(encoding='utf-8', errors='ignore').lower()
    checks = {
        'brand-strip': 'id="brand-strip"' in text or "id='brand-strip'" in text,
        'nav': 'id="nav"' in text or "id='nav'" in text,
        'site-footer': 'id="site-footer"' in text or "id='site-footer'" in text,
        'group-footer': 'id="group-footer"' in text or "id='group-footer'" in text,
        'script.js': '/script.js' in text,
    }
    missing = [name for name, ok in checks.items() if not ok]
    if missing:
        errors.append(f"{p}: missing {', '.join(missing)}")
    raw = p.read_text(encoding='utf-8', errors='ignore')
    for legacy in LEGACY_LOGOS:
        if legacy in raw:
            errors.append(f"{p}: legacy Ascension logo reference {legacy}")

script = Path('script.js').read_text(encoding='utf-8', errors='ignore')
if APPROVED_LOGO not in script:
    errors.append('script.js: approved MyCalendarTools Ascension logo URL missing')

style = Path('style.css').read_text(encoding='cp1252', errors='ignore')
if 'ADG FINAL ADSENSE POLISH 2026-08-30' not in style:
    errors.append('style.css: final card/button/mobile polish marker missing')

print(f'Checked {len(html_files)} HTML files')
if errors:
    print('\n'.join(errors))
    sys.exit(1)
print('PASS: every HTML page has shared header/footer mounts and /script.js; approved Ascension logo and final card/mobile styling are present.')
