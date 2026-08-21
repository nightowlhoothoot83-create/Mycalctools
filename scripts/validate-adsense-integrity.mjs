import fs from 'node:fs';
import path from 'node:path';
const expected='google.com, pub-1904958390525375, DIRECT, f08c47fec0942fa0';
const fail=[];
const walk=p=>fs.readdirSync(p,{withFileTypes:true}).flatMap(e=>e.name==='.git'?[]:e.isDirectory()?walk(path.join(p,e.name)):e.name.endsWith('.html')?[path.join(p,e.name)]:[]);
const files=walk('.');
for(const file of files){const s=fs.readFileSync(file,'utf8');if(/href=["'][^"']*\.html/i.test(s))fail.push(`${file}: internal .html link`);if(/75\+ lenders|INSERT BROKER LEAD FORM LINK|Get a Free Finance/i.test(s))fail.push(`${file}: unfinished finance promotion`);if(/<script\b[^>]*src=["'][^"']*pagead2\.googlesyndication\.com\/pagead\/js\/adsbygoogle\.js/i.test(s))fail.push(`${file}: AdSense loads before consent`);if(/Getting a ballpark figure before speaking to a broker or accountant/i.test(s))fail.push(`${file}: repeated generic copy`);if(!/<link\b[^>]*rel=["']canonical["'][^>]*href=["']https:\/\/mycalctools\.net\//i.test(s))fail.push(`${file}: missing absolute canonical`)}
if(fs.readFileSync('ads.txt','utf8').trim()!==expected)fail.push('ads.txt: publisher line mismatch');
if(/<loc>[^<]*\.html/i.test(fs.readFileSync('sitemap.xml','utf8')))fail.push('sitemap.xml: redirected .html URL');
const consent=fs.readFileSync('cookie-consent.js','utf8');if(!/data-consent-adsense/.test(consent)||!/reopenCookiePreferences/.test(consent))fail.push('cookie-consent.js: consent gate missing');
if(fail.length){console.error(fail.join('\n'));process.exit(1)}console.log(`MyCalcTools integrity passed (${files.length} HTML files)`);
