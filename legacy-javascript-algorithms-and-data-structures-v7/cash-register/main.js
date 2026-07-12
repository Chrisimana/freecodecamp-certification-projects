function checkCashRegister(price, cash, cid) {
  let changeDue = cash - price;
  
  const currencyUnits = [
    ["ONE HUNDRED", 10000],
    ["TWENTY", 2000],
    ["TEN", 1000],
    ["FIVE", 500],
    ["ONE", 100],
    ["QUARTER", 25],
    ["DIME", 10],
    ["NICKEL", 5],
    ["PENNY", 1]
  ];
  
  // Convert all amounts to cents
  let changeDueCents = Math.round(changeDue * 100);
  
  // Calculate total cash in drawer in cents
  let totalCid = 0;
  for (let i = 0; i < cid.length; i++) {
    totalCid += Math.round(cid[i][1] * 100);
  }
  
  // Not enough money in drawer
  if (totalCid < changeDueCents) {
    return {status: "INSUFFICIENT_FUNDS", change: []};
  }
  
  // Exact change equals cash in drawer
  if (totalCid === changeDueCents) {
    return {status: "CLOSED", change: cid};
  }
  
  // Prepare array for change to give
  let change = [];
  
  // Calculate change
  for (let i = 0; i < currencyUnits.length; i++) {
    const [unitName, unitValueCents] = currencyUnits[i];
    
    // Find this unit in cid array
    let cidEntry = cid.find(entry => entry[0] === unitName);
    let cidAmountCents = Math.round(cidEntry[1] * 100);
    let unitCountInDrawer = Math.floor(cidAmountCents / unitValueCents);
    
    // Calculate how many of this unit we can use
    let unitsNeeded = Math.floor(changeDueCents / unitValueCents);
    let unitsToUse = Math.min(unitsNeeded, unitCountInDrawer);
    
    if (unitsToUse > 0) {
      // Calculate amount to give from this unit
      let amountFromUnit = unitsToUse * unitValueCents / 100;
      change.push([unitName, amountFromUnit]);
      
      // Update remaining change due
      changeDueCents -= unitsToUse * unitValueCents;
      
      // Update cash in drawer for this unit
      cidAmountCents -= unitsToUse * unitValueCents;
    }
  }
  
  // Cannot return exact change
  if (changeDueCents > 0) {
    return {status: "INSUFFICIENT_FUNDS", change: []};
  }
  
  // Successfully return change
  return {status: "OPEN", change: change};
}

// Test
console.log(checkCashRegister(19.5, 20, [["PENNY", 1.01], ["NICKEL", 2.05], ["DIME", 3.1], ["QUARTER", 4.25], ["ONE", 90], ["FIVE", 55], ["TEN", 20], ["TWENTY", 60], ["ONE HUNDRED", 100]]));
