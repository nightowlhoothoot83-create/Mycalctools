const {test}=require('node:test');
const assert=require('node:assert/strict');
const {calculate,csv}=require('../craft-fair-profit.js');
const base={units:40,price:20,unitCost:6,feePercent:2,feeFlat:0.2,booth:80,travel:20,other:0,hours:10,hourly:20};
test('reconciles actual example and separates labour from cash',()=>{
 const r=calculate(base); assert.equal(r.revenue,800);assert.equal(r.paymentFees,24);assert.equal(r.stockCost,240);
 assert.equal(r.cashProfit,436);assert.equal(r.economicProfit,236);assert.equal(r.cashBreakEven,8);assert.equal(r.fullBreakEven,23);assert.equal(r.cashPerHour,43.6);
});
test('zero sales loses fixed costs; zero hours has no hourly rate',()=>{const r=calculate({...base,units:0,hours:0});assert.equal(r.cashProfit,-100);assert.equal(r.cashPerHour,null)});
test('negative contribution cannot break even, even at zero fixed cost',()=>{const r=calculate({...base,price:5,booth:0,travel:0});assert.equal(r.cashBreakEven,null)});
test('break-even ceiling reaches target, previous unit fails',()=>{const r=calculate(base);for(const [n,goal] of [[r.cashBreakEven,100],[r.fullBreakEven,300]]){assert.ok(n*r.contribution>=goal);assert.ok((n-1)*r.contribution<goal)}});
test('rejects malformed inputs, blank values, fractions, and unreasonable fee',()=>{for(const bad of [{price:-1},{units:1.2},{price:Infinity},{hourly:''},{feePercent:101},{price:'no'}])assert.throws(()=>calculate({...base,...bad}))});
test('CSV quotes names and neutralises spreadsheet formulas',()=>{const c=csv([{name:'=HYPERLINK("bad")',...calculate(base)}],'AUD');assert.ok(c.includes('"\'=HYPERLINK(""bad"")"'));assert.ok(c.includes('"AUD"'));assert.ok(c.includes('"cashProfit"'))});
test('CSV neutralises whitespace and control-prefixed formulas',()=>{for(const name of [' =1+1','\n=1+1','\t=1+1'])assert.ok(csv([{name,...calculate(base)}],'AUD').includes('"\''+name+'"'))});
