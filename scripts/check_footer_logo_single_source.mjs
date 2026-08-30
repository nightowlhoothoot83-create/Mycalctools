import fs from 'node:fs';
const shell=fs.readFileSync('script.js','utf8');
const consent=fs.readFileSync('cookie-consent.js','utf8');
const validator=fs.readFileSync('scripts/validate-adsense-integrity.mjs','utf8');
const asset='/assets/perf/ascension-digital.webp';
const failures=[];
if(!shell.includes(`src=\"${asset}\"`)) failures.push('script.js does not own canonical footer logo source');
if(/img\.src\s*=\s*['\"][^'\"]*ascension-digital/.test(consent)) failures.push('cookie-consent.js still rewrites Ascension logo source');
if(!validator.includes(`'${asset}'`)) failures.push('integrity validator does not protect canonical local logo asset');
if(failures.length){console.error(failures.join('\n'));process.exit(1)}
console.log('Footer logo single-source regression check passed');
