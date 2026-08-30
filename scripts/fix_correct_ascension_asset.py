from pathlib import Path
p = Path('script.js')
s = p.read_text(encoding='utf-8')
old = 'https://www.mycalendartools.net/assets/perf/ascension-digital.webp'
new = 'https://mycalendartools.net/assets/perf/ascension-digital.webp?v=20260830'
if old not in s:
    raise SystemExit('Expected old Ascension asset URL not found')
s = s.replace(old, new)
p.write_text(s, encoding='utf-8')
out = p.read_text(encoding='utf-8')
assert old not in out
assert new in out
print('MyCalc now references the exact non-www Calendar Ascension asset with cache-busting version')
