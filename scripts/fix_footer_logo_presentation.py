from pathlib import Path

p = Path('script.js')
s = p.read_text(encoding='utf-8')
old = '<img src="https://www.mycalendartools.net/assets/perf/ascension-digital.webp" alt="Ascension Digital" class="ascension-logo" loading="lazy" decoding="async" width="315" height="129">'
new = '<img src="https://www.mycalendartools.net/assets/perf/ascension-digital.webp" alt="Ascension Digital" class="ascension-logo" width="440" height="440" loading="lazy" decoding="async" style="width:220px;height:auto;border-radius:12px;margin:0 auto 20px;display:block;filter:drop-shadow(0 0 16px rgba(6,214,255,0.3))">'
if old not in s:
    raise SystemExit('MyCalc Ascension footer target not found')
s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')

out = p.read_text(encoding='utf-8')
assert new in out
assert 'width="315" height="129"' not in out
print('MyCalc footer logo presentation now matches MyCalendarTools')
