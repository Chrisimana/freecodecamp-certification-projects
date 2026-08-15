document.addEventListener('DOMContentLoaded', function() {
    const textInput = document.getElementById('text-input');
    const checkBtn = document.getElementById('check-btn');
    const resultDiv = document.getElementById('result');
    
    // Function to clean the input string
    function cleanInputString(str) {
        // Remove all non-alphanumeric characters (punctuation, spaces, symbols)
        return str.replace(/[^a-zA-Z0-9]/g, '').toLowerCase();
    }
    
    // Function to check if a string is palindrome
    function isPalindrome(str) {
        const cleanedStr = cleanInputString(str);
        const reversedStr = cleanedStr.split('').reverse().join('');
        return cleanedStr === reversedStr;
    }
    
    // Function to display result with exact format required
    function displayResult(input, isPalindromeResult) {
        if (isPalindromeResult) {
            resultDiv.innerHTML = `<p><strong>${input}</strong> is a palindrome.</p>`;
        } else {
            resultDiv.innerHTML = `<p><strong>${input}</strong> is not a palindrome.</p>`;
        }
    }
    
    // Event listener for check button
    checkBtn.addEventListener('click', function() {
        const inputValue = textInput.value.trim();
        
        // Check if input is empty
        if (!inputValue) {
            alert('Please input a value');
            return;
        }
        
        // Check if palindrome and display result
        const palindromeCheck = isPalindrome(inputValue);
        displayResult(inputValue, palindromeCheck);
    });
    
    // Event listener for Enter key in input field
    textInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            checkBtn.click();
        }
    });
    
    // Remove the auto-check on page load to avoid interference with tests
    // textInput.value = "A man, a plan, a canal. Panama";
    // checkBtn.click();
});