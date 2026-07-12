function palindrome(str) {
  // Remove all non-alphanumeric characters and convert to lowercase
  const cleanedStr = str.toLowerCase().replace(/[\W_]/g, '');
  
  // Create the reversed string
  const reversedStr = cleanedStr.split('').reverse().join('');
  
  // Check if they are equal
  return cleanedStr === reversedStr;
}

// Test with the given examples
console.log(palindrome("eye"));
console.log(palindrome("_eye"));
console.log(palindrome("race car"));
console.log(palindrome("not a palindrome"));
console.log(palindrome("A man, a plan, a canal. Panama"));
console.log(palindrome("never odd or even"));
console.log(palindrome("nope"));
console.log(palindrome("almostomla"));
console.log(palindrome("My age is 0, 0 si ega ym."));
console.log(palindrome("1 eye for of 1 eye."));
console.log(palindrome("0_0 (: /-\ :) 0-0"));
console.log(palindrome("five|\_/|four"));