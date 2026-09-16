from pathlib import Path
import re

ROOT = Path('.')
changed = []

STATIC_SEO_RE = re.compile(
    r'\n?<section class="static-content-section container" data-static-seo="true">.*?</section>\s*',
    re.S,
)
SOURCE_DEPTH_RE = re.compile(
    r'\n?<section class="static-content-section container" data-adg-source-depth="true">.*?</section>\s*',
    re.S,
)

# These are deliberately page-specific. They replace the old repeated SEO filler
# with useful explanatory material that exists in the static HTML before the
# Cloudflare worker adds its separate tool-specific guidance.
SOURCE_DEPTH = {
'pregnancy-calculator.html': '''<h2>How pregnancy weeks are estimated</h2>
<p>This calculator counts from the first day of the last menstrual period, the conventional starting point for pregnancy dating. A typical estimated due date is about 40 weeks from that date, even though conception usually happens later. The result is therefore a calendar estimate, not a measurement of fetal development.</p>
<h2>When the estimate can change</h2>
<p>Irregular cycles, uncertain period dates and later ovulation can shift an LMP-based estimate. A dating ultrasound may give your healthcare team better information and your recorded due date can be revised. Pregnancy, Birth and Baby explains both LMP and ultrasound dating at <a href="https://www.pregnancybirthbaby.org.au/working-out-your-due-date" target="_blank" rel="noopener">Working out your due date</a>. Use this tool for planning appointments and milestones, not to decide whether symptoms or pregnancy progress are normal.</p>''',
'ovulation-calculator.html': '''<h2>What the fertile-window estimate assumes</h2>
<p>The calculator estimates ovulation from the start of the last period and the usual cycle length. Calendar methods commonly place ovulation around the latter part of a cycle, but real cycles are not clockwork. Stress, illness, travel, breastfeeding, perimenopause and hormonal changes can move ovulation earlier or later.</p>
<h2>Using the result sensibly</h2>
<p>Treat the displayed fertile window as a planning range rather than confirmation that ovulation occurred on a particular day. People trying to identify ovulation more closely may combine calendar estimates with cervical mucus changes, basal-body-temperature tracking or ovulation tests. This calculator is not a contraceptive method and should not be relied on by itself to prevent pregnancy. If cycles are persistently irregular or fertility is a concern, a clinician can assess factors a date calculator cannot see.</p>''',
'due-date-calculator.html': '''<h2>Why a due date is an estimate</h2>
<p>Pregnancy is conventionally dated from the first day of the last menstrual period, with an estimated due date about 40 weeks later. If a conception date is known, the calculator can use that instead. Either method gives a planning date rather than a prediction of the exact day labour will begin.</p>
<h2>LMP dates, cycle length and ultrasound</h2>
<p>An LMP estimate works best when the period date is known and cycles are reasonably regular. Pregnancy, Birth and Baby notes that ultrasound can also be used to estimate gestational age and that most babies are born across a range of weeks, not on one exact date. See <a href="https://www.pregnancybirthbaby.org.au/working-out-your-due-date" target="_blank" rel="noopener">Working out your due date</a>. Use the result for calendars and appointment planning, and use the due date recorded by your maternity care team for clinical decisions.</p>''',
'sleep-cycle-calculator.html': '''<h2>What the suggested times mean</h2>
<p>This tool works backwards or forwards in repeated sleep-cycle blocks to produce several possible bedtimes or wake-up times. The options are useful for planning, but they do not measure your personal sleep stages. Real sleep cycles vary between people and across the same night.</p>
<h2>Allow for time to fall asleep</h2>
<p>A calculated bedtime is not the same as the moment sleep begins. If you usually need 10, 20 or 30 minutes to settle, allow for that before the suggested sleep time. Noise, light, alcohol, caffeine, stress, illness and sleep disorders can also affect sleep quality even when total time in bed looks adequate. The calculator is best used to compare schedules and protect enough sleep opportunity, not to promise that waking at the end of a calculated cycle will prevent tiredness.</p>''',
'mortgage-calculator.html': '''<h2>What changes a mortgage repayment</h2>
<p>The repayment estimate is driven by the amount borrowed, interest rate, repayment frequency and loan term. Extending the term usually lowers each scheduled repayment but can increase total interest, while a larger deposit reduces the amount financed. Small rate changes can have a large effect over a long mortgage.</p>
<h2>Costs this calculator does not know</h2>
<p>A real home loan can also involve application or package fees, lenders mortgage insurance, offset balances, redraw, changing variable rates and different interest-calculation conventions. Stamp duty and other property-purchase costs are separate from the loan repayment itself. Use this tool to compare scenarios on the same assumptions, then confirm a product's actual repayment schedule and fees with the lender before making a borrowing decision.</p>''',
'tax-calculator.html': '''<h2>Why country and tax year matter</h2>
<p>Income tax is not one universal percentage. Thresholds, allowances, deductions and social or health levies differ between Australia, the United Kingdom and the United States and they can change from one tax year to the next. This multi-country calculator is intended as a broad comparison tool rather than a tax-return calculation.</p>
<h2>What to verify before relying on a result</h2>
<p>Residency, filing status, offsets, state or local taxes, student-loan repayments, deductions and investment income can materially change the amount actually payable. For an Australian estimate using the site's current resident brackets, use the dedicated Australian Tax Calculator. For filing or a financial commitment, check the relevant revenue authority or a qualified tax professional. The most useful role for this page is comparing rough gross-to-net scenarios while keeping the same assumptions.</p>''',
'pay-calculator.html': '''<h2>How pay periods are converted</h2>
<p>This calculator annualises the amount you enter and then converts that annual figure into the other displayed pay periods. That makes it useful when one job advert quotes an hourly rate and another quotes weekly, fortnightly or annual pay. The conversion assumes a consistent work pattern rather than predicting a payslip.</p>
<h2>Gross pay is not take-home pay</h2>
<p>Overtime, penalty rates, unpaid breaks, casual loading, bonuses, leave, tax withholding and superannuation can all change what you actually receive. If you enter an hourly rate, check that the hours-per-week assumption matches the job you are comparing. Use the converted figures to put offers on a common basis, then use a tax calculator or payroll information when you need an estimate of net income.</p>''',
'superannuation-calculator.html': '''<h2>How the projection works</h2>
<p>The calculator grows the current balance using the return rate you enter and adds estimated employer contributions over the years to retirement. It is a compound-growth scenario, not a forecast of what a super fund will actually earn. Changing the assumed return by even one or two percentage points can produce a very different long-term balance.</p>
<h2>Australian super assumptions to check</h2>
<p>The Australian super guarantee rate is 12% in 2026–27, but contribution rules, caps, fees, insurance premiums and tax inside the fund can affect real outcomes. From July 2026, Payday Super also changes when many employer contributions are paid. The projection does not model every fee, tax rule, market fall or salary change. Use it to compare contribution and return assumptions, then check current rules with the <a href="https://www.ato.gov.au/super" target="_blank" rel="noopener">Australian Taxation Office</a> and your fund.</p>''',
'airfryer-calculator.html': '''<h2>Why air-fryer conversions are approximate</h2>
<p>An air fryer moves hot air rapidly around a relatively small cooking chamber, so food often browns faster than in a conventional oven. The calculator reduces the original oven settings to give an earlier checking point, but there is no single conversion that suits every machine, food thickness or basket load.</p>
<h2>Check the food, not only the timer</h2>
<p>Start checking before the suggested finish time, especially for small portions or a powerful preheated appliance. A crowded basket can take longer because air cannot circulate as freely. Turning or shaking food part-way through can improve even cooking. For meat, poultry and other foods where internal temperature matters, use appropriate food-safety guidance and a thermometer rather than judging doneness from colour or this timing estimate alone.</p>''',
'boiled-egg-calculator.html': '''<h2>What changes an egg's cooking time</h2>
<p>Egg size, starting temperature and the preferred centre all matter. A large refrigerator-cold egg needs a different approach from a smaller egg already near room temperature. The calculator combines those choices into a practical starting time so you can reproduce a style you like.</p>
<h2>Kitchen conditions still matter</h2>
<p>Pan size, the number of eggs, burner strength, water volume and altitude can shift the result. Decide whether your timing begins when the egg enters already-boiling water or while the water is heating, and use the same method each time if you want repeatable results. Cooling cooked eggs promptly in cold or iced water helps stop carry-over cooking. If the first batch is a little soft or firm for your preference, adjust the next run by 30 to 60 seconds rather than treating the displayed time as exact.</p>''',
'recipe-scaling-calculator.html': '''<h2>What scales cleanly and what may not</h2>
<p>Most ingredient quantities can be multiplied by the ratio between the original serving count and the new serving count. That is the arithmetic this tool performs. A recipe for four scaled to six, for example, uses a factor of 1.5 for each entered ingredient.</p>
<h2>Cooking behaviour does not always scale linearly</h2>
<p>Seasoning, chilli, raising agents and thickeners may need judgement rather than a perfectly proportional increase. Doubling ingredients also does not automatically mean doubling baking or simmering time. Pan size, food depth and appliance capacity can alter cooking performance. Use the calculated quantities as the ingredient plan, then check texture, seasoning and doneness during cooking. For very large batches, splitting the mixture between suitable pans can give a result closer to the original recipe.</p>''',
'cups-grams-calculator.html': '''<h2>Why cups and grams need an ingredient</h2>
<p>A cup is a volume measurement while a gram is a mass measurement. The same cup volume can hold very different weights of flour, sugar, butter, cocoa or another ingredient because their densities differ. That is why this converter asks what ingredient you are measuring instead of using one universal cups-to-grams factor.</p>
<h2>Expect small recipe differences</h2>
<p>Published cup standards and the way an ingredient is packed can vary. Scooped and compressed flour, for example, may weigh more than flour lightly spooned into a cup. Use a kitchen scale when precision matters, especially for baking, and treat density-based conversions as practical approximations. If a recipe author supplies both volume and weight, their stated gram amount is usually the better reference for that particular recipe.</p>''',
'pan-size-converter.html': '''<h2>Why pan area is the useful comparison</h2>
<p>This converter compares the surface area of the original pan with the surface area of the replacement pan. The resulting ratio tells you approximately how much batter or mixture is needed to keep a similar depth. It also helps when moving between round, square and rectangular pans where simply comparing widths is misleading.</p>
<h2>Depth and bake time still need judgement</h2>
<p>Two pans can have similar surface area but different wall height, material or heat conduction. A deeper layer of batter can take longer to bake and may need a lower temperature to cook evenly; a shallower layer may finish sooner. Leave enough headroom for cakes that rise, and avoid overfilling a pan just because the area calculation says the volume is close. Use the multiplier for ingredient planning and check doneness earlier when the final batter depth differs from the original recipe.</p>''',
'date-calculator.html': '''<h2>Calendar days are not all the same length on a schedule</h2>
<p>The date calculator adds, subtracts or compares calendar dates using the values you enter. It handles changing month lengths and leap years, which is more reliable than assuming every month contains 30 days. It is useful for ordinary countdowns, elapsed-time checks and planning dates a fixed number of days apart.</p>
<h2>Business-day rules are separate</h2>
<p>A result based on calendar days does not automatically exclude weekends, public holidays or organisation-specific closure days. Legal deadlines, payment terms, visa dates and workplace schedules can also define whether the first or last day is counted. For those uses, check the governing rule rather than treating a general date difference as authoritative. This tool is best for plain calendar arithmetic where every date on the calendar counts.</p>''',
'concrete-calculator.html': '''<h2>From dimensions to concrete volume</h2>
<p>Concrete is ordered by volume, so the calculator converts the dimensions of the selected slab, footing or hole into cubic metres and then applies the waste allowance you choose. For a simple rectangular slab the core calculation is length × width × thickness, after converting all dimensions to consistent units.</p>
<h2>Why a waste allowance matters</h2>
<p>Excavations are rarely perfectly square, ground levels vary and some concrete remains in chutes, pumps or tools. A modest allowance can prevent a pour from finishing short, but the right margin depends on the site and job. Measure the actual excavation in several places if dimensions vary. For structural slabs, footings or engineered work, use the dimensions and concrete specification on the approved drawings and confirm the order quantity with the builder, engineer or concrete supplier before the pour.</p>''',
'percentage-calculator.html': '''<h2>Choose the percentage question first</h2>
<p>“What is 20% of 80?”, “80 is what percent of 100?” and “what is the percentage increase from 80 to 100?” use different formulas even though they contain similar numbers. The calculator separates these common question types so the inputs are less likely to be swapped.</p>
<h2>Percentage points are different from percent change</h2>
<p>If a rate moves from 10% to 12%, it has increased by 2 percentage points but by 20% relative to its original value. That distinction matters when comparing interest rates, survey results and margins. For discounts and mark-ups, also check what value is being used as the base. Use the labelled result to confirm the calculator answered the question you intended rather than copying a number without its context.</p>''',
'etsy-calculator.html': '''<h2>What the fee estimate includes</h2>
<p>This tool combines the entered sale price and shipping charge with a simplified marketplace-fee model, then subtracts product or labour cost to estimate profit and margin. It is useful for testing whether a price still leaves room for costs before publishing a listing.</p>
<h2>Why the real Etsy amount can differ</h2>
<p>Etsy charges can vary with seller country, currency conversion, payment processing, Offsite Ads, taxes and other account-specific settings. Fee schedules also change. The calculator therefore labels the Etsy option as an estimate rather than claiming to reproduce every current invoice. Before setting final prices, compare the assumptions shown here with the fees that apply to your own shop and location. For bookkeeping or tax reporting, use the actual transaction records rather than this planning estimate.</p>''',
'digital-product-calculator.html': '''<h2>Separate revenue from profit</h2>
<p>A digital product may have almost no physical production cost, but that does not make every sale pure profit. Payment processing, marketplace commissions, advertising, refunds, software and delivery services can all reduce the amount retained. This calculator lets you enter those assumptions and see the net result per sale.</p>
<h2>Use scenarios instead of one perfect forecast</h2>
<p>Test a low, expected and high sales volume rather than relying on one target. You can also compare a higher price with fewer sales against a lower price with more sales. The calculation does not predict traffic or conversion rate, so it is most useful after you supply realistic inputs from your own audience or previous launches. Revisit the assumptions when platform fees, ad costs or refund rates change.</p>''',
'rainwater-calculator.html': '''<h2>How roof catchment becomes litres</h2>
<p>A useful rule of thumb is that one millimetre of rain falling on one square metre of roof represents about one litre of water before losses. The calculator combines roof area and rainfall with a collection-efficiency assumption to estimate how much may reach the tank.</p>
<h2>Real systems lose some water</h2>
<p>First-flush devices, gutter overflow, wind, roof wetting, leaks and a full tank can all reduce usable capture. Annual rainfall also says little about how long dry periods last, so total yearly collection should not be confused with guaranteed water security. For tank sizing, compare capture with household demand and local rainfall timing. For drinking-water systems, follow appropriate tank, roof, filtration and water-quality guidance for your location.</p>''',
'food-forest-calculator.html': '''<h2>Plant count is only the first design step</h2>
<p>The calculator turns usable area and spacing into an approximate number of planting positions. That is helpful for budgeting plants and comparing loose layout options, but a food forest is not a uniform grid once trees and shrubs mature.</p>
<h2>Leave room for the system you are building</h2>
<p>Paths, access, water lines, slope, fire considerations, shade and mature canopy spread can reduce the number of sensible planting locations. Different layers also occupy space differently: a canopy tree, understory tree, shrub and groundcover may share an area without using the same spacing rule. Use the estimate to test density, then adjust the plan for species size, climate, water availability and maintenance access. A slightly lower plant count with workable access and enough mature space can be more useful than filling every calculated position.</p>''',
}

for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    original = text

    # Remove the old repeated SEO block and any prior copy of this new enrichment.
    text = STATIC_SEO_RE.sub('\n', text)
    text = SOURCE_DEPTH_RE.sub('\n', text)

    # Keep visible maintenance signals current.
    text = text.replace('&copy; 2025 MyCalcTools', '&copy; 2026 MyCalcTools')
    text = text.replace('© 2025 MyCalcTools', '© 2026 MyCalcTools')

    # Remove the stale year label anywhere it appears, including the homepage card.
    text = text.replace('Etsy Fees 2024', 'Fee Estimate')

    if path.name == 'etsy-calculator.html':
        text = text.replace(
            'Calculate Etsy fees, net profit and profit margin for any listing. Updated for 2024 Etsy fee structure.',
            'Estimate marketplace fees, net profit and profit margin for a product listing. Fee settings are simplified and should be checked against the platform before relying on the result.'
        )
        text = text.replace(
            '<option value="etsy">Etsy (6.5% + $0.20 listing)</option>',
            '<option value="etsy">Etsy estimate (transaction + listing + payment fees)</option>'
        )
        text = text.replace(
            '<div class="info-card"><h3>About</h3><p>Calculate your Etsy fees, net profit and profit margin for any product listing.</p></div>',
            '<div class="info-card"><h3>Important</h3><p>This is a simplified fee estimate. Etsy listing, transaction, payment-processing, advertising and tax charges can vary by country, currency and seller account.</p></div>'
        )

    if path.name == 'sitemap.html':
        text = text.replace(
            '<li><a href="/boiled-egg-calculator">Boiled Egg Calculator</a><li><a href="/recipe-scaling-calculator">Recipe Scaling Calculator</a></li><li><a href="/cups-grams-calculator">Cups to Grams Converter</a></li><li><a href="/pan-size-converter">Pan Size Converter</a></li></li>',
            '<li><a href="/boiled-egg-calculator">Boiled Egg Calculator</a></li>\n<li><a href="/recipe-scaling-calculator">Recipe Scaling Calculator</a></li>\n<li><a href="/cups-grams-calculator">Cups to Grams Converter</a></li>\n<li><a href="/pan-size-converter">Pan Size Converter</a></li>'
        )

    extra = SOURCE_DEPTH.get(path.name)
    if extra and '<footer id="static-policy-footer"' in text:
        block = '\n<section class="static-content-section container" data-adg-source-depth="true">\n' + extra + '\n</section>\n'
        text = text.replace('<footer id="static-policy-footer"', block + '<footer id="static-policy-footer"', 1)

    if text != original:
        path.write_text(text, encoding='utf-8')
        changed.append(str(path))

# The Pages worker creates the served tool-info section. The first panel repeated
# the same summary already shown immediately above the calculator, so remove that
# duplicate from the rendered response rather than asking Google to crawl it twice.
worker_path = ROOT / '_worker.js'
worker = worker_path.read_text(encoding='utf-8')
worker_original = worker
worker = worker.replace(
    ' <div class="tool-info-panel"><h2>What this tool calculates</h2><p>${esc(intro.summary)}</p></div>\n',
    ''
)
if worker != worker_original:
    worker_path.write_text(worker, encoding='utf-8')
    changed.append(str(worker_path))

print(f'Updated {len(changed)} files')
for item in changed:
    print(item)
