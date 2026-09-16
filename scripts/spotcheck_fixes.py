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
    if old not in text:
        raise SystemExit(f'Missing expected worker text: {old[:80]}')
    text = text.replace(old, new)
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

# Correct Concrete copy: the current calculator does not have a waste-allowance input.
concrete = Path('concrete-calculator.html')
text = concrete.read_text(encoding='utf-8')
old1 = 'Concrete is ordered by volume, so the calculator converts the dimensions of the selected slab, footing or hole into cubic metres and then applies the waste allowance you choose. For a simple rectangular slab the core calculation is length × width × thickness, after converting all dimensions to consistent units.'
new1 = 'Concrete is ordered by volume, so the calculator converts the dimensions of the selected slab, strip footing or round post hole into cubic metres and then shows approximate premix bag counts from that volume. For a simple rectangular slab or strip footing the core calculation is length × width × depth. Round post holes use the cylinder-volume formula.'
old2 = 'Excavations are rarely perfectly square, ground levels vary and some concrete remains in chutes, pumps or tools. A modest allowance can prevent a pour from finishing short, but the right margin depends on the site and job. Measure the actual excavation in several places if dimensions vary. For structural slabs, footings or engineered work, use the dimensions and concrete specification on the approved drawings and confirm the order quantity with the builder, engineer or concrete supplier before the pour.'
new2 = 'Excavations are rarely perfectly square, ground levels vary and some concrete remains in chutes, pumps or tools. This calculator does not automatically add a waste allowance, so treat the raw volume and bag count as a starting estimate. The displayed dollar figure also uses a simple $250 per cubic metre planning assumption and may differ substantially from local supplier quotes. For structural slabs, footings or engineered work, use the dimensions and concrete specification on the approved drawings and confirm the final order quantity with the builder, engineer or concrete supplier before the pour.'
if old1 not in text or old2 not in text:
    raise SystemExit('Expected Concrete explanatory text not found')
text = text.replace(old1, new1).replace(old2, new2)
concrete.write_text(text, encoding='utf-8')

print('Applied final spot-check fixes')
