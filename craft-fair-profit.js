(function(root){
  'use strict';
  const fields=['units','price','unitCost','feePercent','feeFlat','booth','travel','other','hours','hourly'];
  function calculate(input){
    const v={};
    for(const key of fields){
      if(input[key]===''||input[key]===null||input[key]===undefined) throw new Error('Enter every number, using 0 where a cost does not apply.');
      const n=Number(input[key]);
      if(!Number.isFinite(n)||n<0||n>1e9) throw new Error('Use finite, non-negative numbers below one billion.');
      v[key]=n;
    }
    if(!Number.isInteger(v.units)) throw new Error('Items sold must be a whole number.');
    if(v.feePercent>100) throw new Error('Payment fee percentage cannot exceed 100.');
    const revenue=v.units*v.price;
    const paymentFees=revenue*v.feePercent/100+v.units*v.feeFlat;
    const stockCost=v.units*v.unitCost;
    const eventCosts=v.booth+v.travel+v.other;
    const contribution=v.price*(1-v.feePercent/100)-v.feeFlat-v.unitCost;
    const cashProfit=revenue-paymentFees-stockCost-eventCosts;
    const labour=v.hours*v.hourly;
    const economicProfit=cashProfit-labour;
    const breakeven=(cost)=>contribution>0?Math.ceil(cost/contribution):null;
    return {...v,revenue,paymentFees,stockCost,eventCosts,contribution,cashProfit,labour,economicProfit,
      cashBreakEven:breakeven(eventCosts),fullBreakEven:breakeven(eventCosts+labour),
      cashPerHour:v.hours>0?cashProfit/v.hours:null};
  }
  function csvCell(value){const s=String(value??'');return '"'+(/^(?:\s*[=+\-@]|[\t\r\n])/.test(s)?"'"+s:s).replaceAll('"','""')+'"';}
  function csv(rows,currency){
    const keys=['name',...fields,'revenue','paymentFees','stockCost','eventCosts','cashProfit','labour','economicProfit','cashBreakEven','fullBreakEven','cashPerHour'];
    return '\uFEFF'+[['Currency',currency],keys,...rows.map(r=>keys.map(k=>r[k]??'Not achievable'))].map(row=>row.map(csvCell).join(',')).join('\r\n');
  }
  const api={calculate,csv,fields};
  if(typeof module==='object'&&module.exports)module.exports=api;
  else root.CraftFairProfit=api;
})(typeof window==='object'?window:globalThis);
