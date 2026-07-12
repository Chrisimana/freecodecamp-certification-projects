function telephoneCheck(str) {
  // Regular expression to validate US phone numbers
  const phoneRegex = /^(1\s?)?(\(\d{3}\)|\d{3})([\s\-]?)\d{3}([\s\-]?)\d{4}$/;
  
  // Check if the string matches the pattern
  if (!phoneRegex.test(str)) {
    return false;
  }
  
  // Count opening and closing parentheses
  const openParenCount = (str.match(/\(/g) || []).length;
  const closeParenCount = (str.match(/\)/g) || []).length;
  
  // If parentheses counts don't match, it's invalid
  if (openParenCount !== closeParenCount) {
    return false;
  }
  
  // If there are parentheses, they must be in the correct position
  if (openParenCount > 0) {
    // Check if parentheses properly enclose the area code
    const parenRegex = /^1?\s?\(\d{3}\)\s?\d{3}[-\s]?\d{4}$/;
    if (!parenRegex.test(str)) {
      return false;
    }
  }
  
  return true;
}

// Test
console.log(telephoneCheck("555-555-5555")); 
console.log(telephoneCheck("1 555-555-5555")); 
console.log(telephoneCheck("1 (555) 555-5555")); 
console.log(telephoneCheck("(555)555-5555")); 
console.log(telephoneCheck("1(555)555-5555")); 
console.log(telephoneCheck("555-5555")); 
console.log(telephoneCheck("1 555)555-5555")); 
console.log(telephoneCheck("(6054756961)"));
console.log(telephoneCheck("2 (757) 622-7382"));
console.log(telephoneCheck("(555-555-5555"));
console.log(telephoneCheck("555)-555-5555"));