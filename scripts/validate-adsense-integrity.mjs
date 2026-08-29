import fs from 'node:fs';
import path from 'node:path';
const expected='google.com, pub-1904958390525375, DIRECT, f08c47fec0942fa0';
const fail=[];
const genericFiles=[];
const walk=p=>fs.readdirSync(p,{withFileTypes:true}).flatMap(e=>e.name==='.git'?[]:e.isDirectory()?walk(path.join(p,e.name)):e.name.endsWith('.html')?[path.join(p,e.name)]:[]);
const files=walk('.');
const stripVisible=s=>s
  .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi,' ')
  .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi,' ')
  .replace(/<footer\b[^>]*>[\s\S]*?<\/footer>/gi,' ')
  .replace(/<nav\b[^>]*>[\s\S]*?<\/nav>/gi,' ')
  .replace(/<[^>]+>/g,' ')
  .replace(/&[a-z0-9#]+;/gi,' ');
const wordCount=s=>(stripVisible(s).match(/\b[A-Za-z0-9][A-Za-z0-9'’\-]*\b/g)||[]).length;
const generic=/Enter the dates, amounts or details the calculator asks for|Pick the option that matches your specific situation|Planning ahead for an upcoming date or milestone|Working out timing for a trip, event or project|Comparing a couple of options before deciding|household planning, school or work tasks|The .*? page explains what the tool or support page provides|Enter the dates, numbers or options requested by the form on this page|Choose any unit, country, time period or setting that applies to your situation/i;
for(const file of files){
  const s=fs.readFileSync(file,'utf8');
  if(/href=["'][^"']*\.html/i.test(s))fail.push(`${file}: internal .html link`);
  if(/75\+ lenders|INSERT BROKER LEAD FORM LINK|Get a Free Finance/i.test(s))fail.push(`${file}: unfinished finance promotion`);
  if(/<script\b[^>]*src=["'][^"']*pagead2\.googlesyndication\.com\/pagead\/js\/adsbygoogle\.js/i.test(s))fail.push(`${file}: AdSense loads before consent`);
  if(/Getting a ballpark figure before speaking to a broker or accountant/i.test(s))fail.push(`${file}: repeated generic copy`);
  if(!/<link\b[^>]*rel=["']canonical["'][^>]*href=["']https:\/\/mycalctools\.net\//i.test(s))fail.push(`${file}: missing absolute canonical`);
  if(!/index\.html$/.test(file) && !s.includes('/cookie-consent.js'))fail.push(`${file}: cookie/shell bootstrap missing`);
  if(generic.test(s))genericFiles.push(file.replace(/^\.\//,''));
}
if(fs.readFileSync('ads.txt','utf8').trim()!==expected)fail.push('ads.txt: publisher line mismatch');
if(/<loc>[^<]*\.html/i.test(fs.readFileSync('sitemap.xml','utf8')))fail.push('sitemap.xml: redirected .html URL');
const redirects=fs.readFileSync('_redirects','utf8');
if(/^\/(?:bmi-calculator|calorie-calculator)\s+\/(?:bmi-calculator|calorie-calculator)\.html\s+200/m.test(redirects))fail.push('_redirects: reverse clean-route .html rewrite returned');
const consent=fs.readFileSync('cookie-consent.js','utf8');
if(!/data-consent-adsense/.test(consent)||!/reopenCookiePreferences/.test(consent))fail.push('cookie-consent.js: consent gate missing');
for(const marker of ['ensureShellMounts','site-footer','group-footer','mct-approved-shell-style','mycalendartools.net/assets/perf/ascension-digital.webp'])if(!consent.includes(marker))fail.push(`cookie-consent.js: shared shell marker missing: ${marker}`);
const shared=fs.readFileSync('script.js','utf8');
const toolEntries=(shared.match(/\{ name:/g)||[]).length;
if(toolEntries!==55)fail.push(`script.js: expected 55 searchable tools, found ${toolEntries}`);
const toolSlugs=[...shared.matchAll(/file:\s*'([^']+)'/g)].map(m=>m[1]).filter((v,i,a)=>a.indexOf(v)===i);
if(toolSlugs.length!==55)fail.push(`script.js: expected 55 unique tool slugs, found ${toolSlugs.length}`);
for(const slug of toolSlugs){
  const file=`${slug}.html`;
  if(!fs.existsSync(file)){fail.push(`${file}: searchable tool page missing`);continue;}
  const s=fs.readFileSync(file,'utf8');
  const words=wordCount(s);
  if(words<250)fail.push(`${file}: thin static tool copy (${words} visible words; minimum 250 before worker enrichment)`);
}
const requiredNew=['subscription-cancellation-savings-calculator','online-business-running-cost-calculator','advertising-budget-break-even-calculator','rainwater-days-remaining-calculator','generator-vs-solar-cost-calculator','grow-your-own-savings-calculator','mulch-coverage-cost-calculator','trees-per-acre-hectare-calculator','off-grid-battery-runtime-calculator'];
for(const slug of requiredNew){if(!fs.existsSync(`${slug}.html`))fail.push(`${slug}: page missing`);if(!shared.includes(`file: '${slug}'`))fail.push(`${slug}: missing from search list`);if(!fs.readFileSync('sitemap.xml','utf8').includes(`/${slug}</loc>`))fail.push(`${slug}: missing from XML sitemap`)}
for(const file of ['index.html','about.html','sitemap.html','script.js']){const s=fs.readFileSync(file,'utf8');if(/(?:46 free|46 tools|Search 46|includes 46)/i.test(s))fail.push(`${file}: stale 46-tool reference`)}
const worker=fs.readFileSync('_worker.js','utf8');
if(!worker.includes('endsWith(".mycalctools.pages.dev")'))fail.push('_worker.js: branch preview host allowance missing');
if(!worker.includes('isPreview?host:"mycalctools.net"'))fail.push('_worker.js: preview assets are not isolated from production');
if(!worker.includes('data-adg-unique-info="true"'))fail.push('_worker.js: unique-content marker missing');
if(!worker.includes('data-static-seo')||!worker.includes('html=html.replace(p,s)'))fail.push('_worker.js: obsolete filler removal or tool-info replacement missing');
const objectLiteral=name=>{const start=worker.indexOf(`const ${name}={`);if(start<0)return null;const open=worker.indexOf('{',start);let depth=0,quote=null,escaped=false;for(let i=open;i<worker.length;i++){const c=worker[i];if(quote){if(escaped)escaped=false;else if(c==='\\')escaped=true;else if(c===quote)quote=null;continue}if(c==='"'||c==="'"){quote=c;continue}if(c==='{')depth++;if(c==='}'&&--depth===0)return worker.slice(open,i+1)}return null};
const infoLiteral=objectLiteral('INFO'),howLiteral=objectLiteral('HOW');
if(!infoLiteral||!howLiteral)fail.push('_worker.js: unique content maps missing');
else{
  const info=Function(`return (${infoLiteral})`)(),how=Function(`return (${howLiteral})`)();
  for(const key of Object.keys(info)){if(!how[key]||how[key].length<80)fail.push(`_worker.js: specific instructions missing for ${key}`);if(!Array.isArray(info[key].use)||info[key].use.length<2)fail.push(`_worker.js: specific use cases missing for ${key}`)}
  if(Object.keys(how).some(key=>!info[key]))fail.push('_worker.js: instruction map contains an unknown tool');
  for(const file of genericFiles){const slug=file.replace(/\.html$/,'').replace(/\\/g,'/');if(!info[slug]||!how[slug])fail.push(`${file}: generic fallback exists without a server-side unique replacement`)}
}
const bmi=fs.readFileSync('bmi-calculator.html','utf8');
for(const marker of ['data-adg-enrichment="true"','How BMI is calculated','BMI range guide','Worked BMI example','role="img"'])if(!bmi.includes(marker))fail.push(`bmi-calculator.html: missing enrichment marker ${marker}`);
if(/dates, numbers or options|household planning, school or work tasks/i.test(bmi))fail.push('bmi-calculator.html: generic template copy remains');
const mulch=fs.readFileSync('mulch-coverage-cost-calculator.html','utf8');
for(const marker of ['Mulch depth at a glance','Worked example','role="img"','How do I convert mulch depth'])if(!mulch.includes(marker))fail.push(`mulch-coverage-cost-calculator.html: missing enrichment marker ${marker}`);
if((mulch.match(/class="faq-item"/g)||[]).length<4)fail.push('mulch-coverage-cost-calculator.html: expected at least four useful FAQs');
const lockedVisuals={'bmi-calculator.html':'/assets/bmi-range-guide.svg','advertising-budget-break-even-calculator.html':'/assets/advertising-budget-flow.svg','trees-per-acre-hectare-calculator.html':'/assets/trees-spacing-guide.svg','mulch-coverage-cost-calculator.html':'/assets/mulch-depth-guide.svg','generator-vs-solar-cost-calculator.html':'/assets/generator-vs-solar-cost-guide.svg','concrete-calculator.html':'/assets/concrete-volume-guide.svg','electricity-calculator.html':'/assets/electricity-running-cost-guide.svg'};
for(const [page,asset] of Object.entries(lockedVisuals)){if(!fs.existsSync(page))fail.push(`${page}: locked visual page missing`);else if(!fs.readFileSync(page,'utf8').includes(`src="${asset}"`))fail.push(`${page}: locked visual reference missing (${asset})`);const assetPath=asset.slice(1);if(!fs.existsSync(assetPath))fail.push(`${assetPath}: locked visual asset missing`)}
const home=fs.readFileSync('index.html','utf8');
if(!home.includes('ATO-aligned FY2026-27 with LITO'))fail.push('index.html: Australian Tax description must remain FY2026-27');
if(!home.includes('>ATO 2026-27</span>'))fail.push('index.html: Australian Tax tag must remain ATO 2026-27');
if(/ATO 2024-25/.test(home))fail.push('index.html: stale Australian Tax year returned');
if(!home.includes('&copy; 2026 MyCalcTools'))fail.push('index.html: homepage copyright must remain 2026');
if(fail.length){console.error(fail.join('\n'));process.exit(1)}console.log(`MyCalcTools integrity passed (${files.length} HTML files; ${toolSlugs.length} tool pages; ${genericFiles.length} obsolete fallback sections safely replaced by worker content)`);
