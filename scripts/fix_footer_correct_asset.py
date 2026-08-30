from pathlib import Path
import re

CAL='https://www.mycalendartools.net/assets/perf/ascension-digital.webp?v=20260830-final'
p=Path('script.js')
s=p.read_text()
# Replace only the large Ascension Digital footer image source; do not touch page/tool content.
pattern=r'(<img\s+src=")[^"]+("\s+alt="Ascension Digital"\s+class="ascension-logo")'
s,n=re.subn(pattern, lambda m:m.group(1)+CAL+m.group(2), s, count=1)
assert n==1, 'Ascension footer image not found'
# Keep the approved visible size consistent with Calendar/Wheel.
s=s.replace('style="width:220px;max-width:70vw;', 'style="width:280px;max-width:78vw;')
p.write_text(s)

out=p.read_text()
assert CAL in out
assert 'alt="Ascension Digital" class="ascension-logo"' in out
assert 'width:280px;max-width:78vw;' in out
print('MyCalc footer asset repair verified')
