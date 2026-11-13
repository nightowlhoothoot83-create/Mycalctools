const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { join } = require('node:path');
const vm = require('node:vm');
const html = readFileSync(join(__dirname, '..', 'solar-calculator.html'), 'utf8');
const script = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).find(s => s.includes('function calcSol()'));
function calculate(kwh, sun, days = 2, voltage = 48) {
  const elements = Object.fromEntries(['solKwh','solState','solDays','solV','solR','solRVal','solRLbl','solRGrid'].map(id => [id, {}]));
  for (const [id, value] of Object.entries({solKwh:kwh,solState:sun,solDays:days,solV:voltage})) elements[id].value=String(value);
  const context = vm.createContext({document:{getElementById:id=>elements[id]}});
  vm.runInContext(script,context); context.calcSol(); return elements;
}
test('20 kWh/day at 5 sun hours requires 17 nominal 300 W panels with the existing 25% allowance', () => {
  const result = calculate(20,5);
  assert.equal(result.solRVal.textContent,'17×300W');
  assert.match(result.solRGrid.innerHTML,/1042Ah @ 48V/);
  assert.match(result.solRGrid.innerHTML,/50\.0 kWh/);
});
test('fractional panel requirements always round upward', () => {
  assert.equal(calculate(1,5).solRVal.textContent,'1×300W');
  assert.equal(calculate(10,5).solRVal.textContent,'9×300W');
});
