from pathlib import Path

# Replace heavyweight legacy image references with existing optimized WebP assets.
replacements = {
    '/mycalctools-logo.png': '/assets/perf/mycalctools-logo.webp',
    '/mycalendartools-logo.png': '/assets/perf/mycalendartools-logo.webp',
    '/wheelnamepicker-logo.png': '/assets/perf/wheelnamepicker-logo.webp',
    '/ravensharp-logo.jpg': '/assets/perf/ravensharp-logo.webp',
    '/raven-sharp.jpg': '/assets/perf/raven-sharp.webp',
}

for path in [Path('script.js'), Path('index.html')]:
    text = path.read_text(encoding='utf-8')
    for old, new in replacements.items():
        text = text.replace(old, new)

    if path.name == 'script.js':
        text = text.replace(
            '<img src="/assets/perf/mycalctools-logo.webp" alt="MyCalcTools logo" class="nav-logo-icon">',
            '<img src="/assets/perf/mycalctools-logo.webp" alt="MyCalcTools logo" class="nav-logo-icon" width="36" height="36" decoding="async" fetchpriority="high">'
        )
    else:
        # All promotional images are below the fold: lazy-load and async-decode them.
        text = text.replace(
            '<img src="/assets/perf/mycalendartools-logo.webp" alt="MyCalendarTools logo">',
            '<img src="/assets/perf/mycalendartools-logo.webp" alt="MyCalendarTools logo" loading="lazy" decoding="async" width="72" height="72">'
        )
        text = text.replace(
            '<img src="/assets/perf/wheelnamepicker-logo.webp" alt="Wheel Name Picker logo">',
            '<img src="/assets/perf/wheelnamepicker-logo.webp" alt="Wheel Name Picker logo" loading="lazy" decoding="async" width="72" height="72">'
        )
        text = text.replace(
            '<img src="/assets/perf/ravensharp-logo.webp" alt="Raven Sharp Print on Demand logo">',
            '<img src="/assets/perf/ravensharp-logo.webp" alt="Raven Sharp Print on Demand logo" loading="lazy" decoding="async" width="72" height="72">'
        )
        text = text.replace(
            '<img src="/assets/perf/raven-sharp.webp" alt="Raven Sharp Image Optimiser logo">',
            '<img src="/assets/perf/raven-sharp.webp" alt="Raven Sharp Image Optimiser logo" loading="lazy" decoding="async" width="72" height="72">'
        )

    path.write_text(text, encoding='utf-8')

print('Mobile image references optimized.')
