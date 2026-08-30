from pathlib import Path
import re

p = Path('script.js')
s = p.read_text(encoding='utf-8')

approved = 'https://raw.githubusercontent.com/nightowlhoothoot83-create/Mycalendartools/main/assets/perf/ascension-digital.webp?rev=20260830c'

# Force the group-footer Ascension artwork to the exact current CalendarTools source asset.
s = re.sub(
    r'<img\s+src="[^"]*ascension-digital[^"]*"\s+alt="Ascension Digital"\s+class="ascension-logo"[^>]*>',
    f'<img src="{approved}" alt="Ascension Digital" class="ascension-logo" width="440" height="440" loading="lazy" decoding="async" style="width:280px;max-width:78vw;height:auto;border-radius:12px;margin:0 auto 20px;display:block;filter:drop-shadow(0 0 16px rgba(6,214,255,0.3))">',
    s,
    count=1,
    flags=re.I,
)

if approved not in s:
    raise SystemExit('approved Ascension asset not written')
if 'style="width:280px;max-width:78vw;' not in s:
    raise SystemExit('final Ascension sizing not written')

p.write_text(s, encoding='utf-8')
