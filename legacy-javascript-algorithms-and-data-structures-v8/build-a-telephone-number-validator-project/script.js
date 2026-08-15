const userInput = document.getElementById('user-input');
const checkBtn = document.getElementById('check-btn');
const clearBtn = document.getElementById('clear-btn');
const resultsDiv = document.getElementById('results-div');

const validatePhoneNumber = (phoneNumber) => {
    // Regular expression to validate US phone numbers
    const regex = /^(1\s?)?(\(\d{3}\)|\d{3})([\s\-]?)\d{3}([\s\-]?)\d{4}$/;
    
    // Remove all non-digit characters except parentheses, spaces, and hyphens
    const cleanNumber = phoneNumber.replace(/[^0-9()\s-]/g, '');
    
    // Check if it matches the US phone number pattern
    const digitsOnly = phoneNumber.replace(/\D/g, '');
    
    if (digitsOnly.length === 10) {
        // Check if it matches any valid format
        return regex.test(phoneNumber);
    } else if (digitsOnly.length === 11 && digitsOnly[0] === '1') {
        // Check if it matches any valid format with country code
        return regex.test(phoneNumber);
    }
    
    return false;
};

const checkPhoneNumber = () => {
    const inputValue = userInput.value.trim();
    
    if (inputValue === '') {
        alert('Please provide a phone number');
        return;
    }
    
    const isValid = validatePhoneNumber(inputValue);
    
    // Clear previous results
    resultsDiv.className = '';
    
    if (isValid) {
        resultsDiv.textContent = `Valid US number: ${inputValue}`;
        resultsDiv.className = 'valid';
    } else {
        resultsDiv.textContent = `Invalid US number: ${inputValue}`;
        resultsDiv.className = 'invalid';
    }
};

const clearResults = () => {
    userInput.value = '';
    resultsDiv.textContent = '';
    resultsDiv.className = 'empty';
};

// Event Listeners
checkBtn.addEventListener('click', checkPhoneNumber);

clearBtn.addEventListener('click', clearResults);

// Allow Enter key to trigger check
userInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        checkPhoneNumber();
    }
});

// Initialize empty state
resultsDiv.className = 'empty';