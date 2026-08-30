from pathlib import Path

MARKER = "/* ADG FINAL ADSENSE POLISH 2026-08-30 */"
CSS = r'''

/* ADG FINAL ADSENSE POLISH 2026-08-30 */
:where(.calc-card,.info-card,.related-card,.tool-info-panel,.card,.tool-card,.category-card,.static-content-section,.feature-card,.planning-card){
  border-color:rgba(139,92,246,.30)!important;
  box-shadow:0 10px 30px rgba(0,0,0,.20),0 0 20px rgba(6,214,255,.07),0 0 16px rgba(139,92,246,.06);
}
:where(.calc-card,.info-card,.related-card,.tool-info-panel,.card,.tool-card,.category-card,.static-content-section,.feature-card,.planning-card):hover{
  border-color:rgba(6,214,255,.42)!important;
  box-shadow:0 12px 34px rgba(0,0,0,.24),0 0 24px rgba(6,214,255,.12),0 0 20px rgba(139,92,246,.10);
}
:where(.btn-calc,.btn-primary,.btn-finance,.btn-secondary,.toggle-btn,button[type="submit"],a[class*="btn"],button[class*="btn"]){
  box-shadow:0 0 18px rgba(139,92,246,.18),0 0 12px rgba(6,214,255,.08);
}
:where(.ascension-logo,.foot-adg-logo,img[alt="Ascension Digital"],img[alt="Ascension Digital Group"]){
  display:block!important;width:min(220px,72vw)!important;max-width:220px!important;height:auto!important;object-fit:contain!important;margin-left:auto!important;margin-right:auto!important;
}
@media(max-width:768px){
  .site-nav,.card,.calc-card,.tool-card,.info-card{backdrop-filter:none!important;-webkit-backdrop-filter:none!important}
  body::before{background-image:none!important}
  :where(.calc-card,.info-card,.related-card,.tool-info-panel,.card,.tool-card,.category-card,.static-content-section,.feature-card,.planning-card){box-shadow:0 6px 18px rgba(0,0,0,.18),0 0 10px rgba(139,92,246,.06)}
  :where(.btn-calc,.btn-primary,.btn-finance,.btn-secondary,.toggle-btn,button[type="submit"],a[class*="btn"],button[class*="btn"]){box-shadow:0 0 10px rgba(139,92,246,.12)}
}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}
'''

root = Path('.')
style = root / 'style.css'
text = style.read_text(encoding='utf-8')
if MARKER not in text:
    style.write_text(text.rstrip() + CSS + "\n", encoding='utf-8')

# Use the local optimized current ADG logo everywhere instead of legacy/cross-site assets.
replacements = {
    'https://www.mycalendartools.net/assets/perf/ascension-digital.webp': '/assets/perf/ascension-digital-logo.webp',
    '/ascension-digital-logo.jpg': '/assets/perf/ascension-digital-logo.webp',
    'ascension-digital-logo.jpg': '/assets/perf/ascension-digital-logo.webp',
    '/logo-ascension-digital.png': '/assets/perf/ascension-digital-logo.webp',
    'logo-ascension-digital.png': '/assets/perf/ascension-digital-logo.webp',
}
for p in root.rglob('*'):
    if not p.is_file() or p.suffix.lower() not in {'.html','.js','.css'} or '.git' in p.parts:
        continue
    data = p.read_text(encoding='utf-8', errors='ignore')
    new = data
    for old, rep in replacements.items():
        new = new.replace(old, rep)
    if new != data:
        p.write_text(new, encoding='utf-8')
