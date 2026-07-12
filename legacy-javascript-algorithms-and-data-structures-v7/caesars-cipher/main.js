function rot13(str) {
  return str.split('')
    .map(char => {
      const code = char.charCodeAt(0);
      
      // Check if the character is an uppercase letter (A-Z)
      if (code >= 65 && code <= 90) {
        let decodedCode = code - 13;
        if (decodedCode < 65) {
          decodedCode += 26;
        }
        return String.fromCharCode(decodedCode);
      }
      
      // Return non-alphabetic characters unchanged
      return char;
    })
    .join('');
}

// Test
console.log(rot13("SERR PBQR PNZC"));
console.log(rot13("SERR CVMMN!"));
console.log(rot13("SERR YBIR?")); 
console.log(rot13("GUR DHVPX OEBJA SBK WHZCF BIRE GUR YNML QBT."));