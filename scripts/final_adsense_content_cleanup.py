from pathlib import Path
import re

ROOT = Path('.')
changed = []

STATIC_SEO_RE = re.compile(
    r'\n?<section class="static-content-section container" data-static-seo="true">.*?</section>\s*',
    re.S,
)

for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    original = text

    # Remove the old generic SEO block from source entirely. It was previously
    # hidden/rewritten at response time, which left stale boilerplate in GitHub.
    text = STATIC_SEO_RE.sub('\n', text)

    # Keep visible maintenance signals current.
    text = text.replace('&copy; 2025 MyCalcTools', '&copy; 2026 MyCalcTools')
    text = text.replace('© 2025 MyCalcTools', '© 2026 MyCalcTools')

    if path.name == 'etsy-calculator.html':
        text = text.replace(
            'Calculate Etsy fees, net profit and profit margin for any listing. Updated for 2024 Etsy fee structure.',
            'Estimate marketplace fees, net profit and profit margin for a product listing. Fee settings are simplified and should be checked against the platform before relying on the result.'
        )
        text = text.replace('Etsy Fees 2024', 'Fee Estimate')
        text = text.replace(
            '<option value="etsy">Etsy (6.5% + $0.20 listing)</option>',
            '<option value="etsy">Etsy estimate (transaction + listing + payment fees)</option>'
        )
        text = text.replace(
            '<div class="info-card"><h3>About</h3><p>Calculate your Etsy fees, net profit and profit margin for any product listing.</p></div>',
            '<div class="info-card"><h3>Important</h3><p>This is a simplified fee estimate. Etsy listing, transaction, payment-processing, advertising and tax charges can vary by country, currency and seller account.</p></div>'
        )

    if path.name == 'sitemap.html':
        # Repair malformed nested list items in the kitchen section.
        text = text.replace(
            '<li><a href="/boiled-egg-calculator">Boiled Egg Calculator</a><li><a href="/recipe-scaling-calculator">Recipe Scaling Calculator</a></li><li><a href="/cups-grams-calculator">Cups to Grams Converter</a></li><li><a href="/pan-size-converter">Pan Size Converter</a></li></li>',
            '<li><a href="/boiled-egg-calculator">Boiled Egg Calculator</a></li>\n<li><a href="/recipe-scaling-calculator">Recipe Scaling Calculator</a></li>\n<li><a href="/cups-grams-calculator">Cups to Grams Converter</a></li>\n<li><a href="/pan-size-converter">Pan Size Converter</a></li>'
        )

    if text != original:
        path.write_text(text, encoding='utf-8')
        changed.append(str(path))

print(f'Updated {len(changed)} HTML files')
for item in changed:
    print(item)
