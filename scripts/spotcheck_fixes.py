from pathlib import Path

# Fix semantic mismatches found during the final AdSense spot-check.
worker = Path('_worker.js')
text = worker.read_text(encoding='utf-8')
replacements = {
    '"australian-tax-calculator":"Enter Australian taxable income and applicable deductions or study-debt details, then calculate the estimated tax and net income breakdown.",':
    '"australian-tax-calculator":"Enter annual gross income, work-related deductions and any deductible personal super contribution you want included, then calculate the estimated tax and take-home breakdown.",',
    '"hecs-help-calculator":"Enter annual repayment income and select the relevant financial year, then calculate the estimated compulsory HELP repayment and remaining take-home amount.",':
    '"hecs-help-calculator":"Enter your current HECS-HELP debt balance and annual repayment income, then calculate the estimated compulsory repayment, weekly equivalent and simple payoff timeframe.",',
    '"concrete-calculator":"Choose the slab, footing or post-hole shape, enter all dimensions in matching units and add a waste allowance, then calculate volume and premix bags.",':
    '"concrete-calculator":"Choose slab or strip footing, or a round post hole, enter the dimensions in metres and the number of post holes if relevant, then calculate volume and approximate premix bag counts.",'
}
for old, new in replacements.items():
    if old in text:
        text = text.replace(old, new)
    elif new not in text:
        raise SystemExit(f'Could not locate worker instruction: {old[:80]}')
worker.write_text(text, encoding='utf-8')

# Add the five converter links that were missing from a sitemap claiming all 55 tools.
sitemap = Path('sitemap.html')
text = sitemap.read_text(encoding='utf-8')
marker = '<div class="sitemap-col"><h3>ℹ️ Pages</h3><ul>'
converter_block = '''<div class="sitemap-col"><h3>🔄 Unit Converters</h3><ul>
<li><a href="/converters/length-converter">Length &amp; Distance Converter</a></li>
<li><a href="/converters/weight-converter">Weight Converter</a></li>
<li><a href="/converters/volume-converter">Volume Converter</a></li>
<li><a href="/converters/temperature-converter">Temperature Converter</a></li>
<li><a href="/converters/speed-converter">Speed Converter</a></li>
</ul></div>
'''
if converter_block not in text:
    if marker not in text:
        raise SystemExit('Sitemap pages marker not found')
    text = text.replace(marker, converter_block + marker)
sitemap.write_text(text, encoding='utf-8')

# Make the concrete cost assumption explicit. The calculator code uses m3 * 250.
concrete = Path('concrete-calculator.html')
text = concrete.read_text(encoding='utf-8')
old = 'The cost figure is only a rough comparison based on a simple per-cubic-metre allowance, not a supplier quote.'
new = 'The cost figure is only a rough comparison using a $250 per cubic metre planning allowance, not a supplier quote.'
if old in text:
    text = text.replace(old, new)
elif new not in text:
    raise SystemExit('Concrete cost-assumption copy not found')
concrete.write_text(text, encoding='utf-8')

print('Applied final spot-check fixes')
