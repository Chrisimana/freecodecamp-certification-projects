document.addEventListener('DOMContentLoaded', function() {
    const numberInput = document.getElementById('number');
    const convertBtn = document.getElementById('convert-btn');
    const output = document.getElementById('output');
    
    // Roman numeral conversion data
    const romanNumerals = [
        { value: 1000, numeral: 'M' },
        { value: 900, numeral: 'CM' },
        { value: 500, numeral: 'D' },
        { value: 400, numeral: 'CD' },
        { value: 100, numeral: 'C' },
        { value: 90, numeral: 'XC' },
        { value: 50, numeral: 'L' },
        { value: 40, numeral: 'XL' },
        { value: 10, numeral: 'X' },
        { value: 9, numeral: 'IX' },
        { value: 5, numeral: 'V' },
        { value: 4, numeral: 'IV' },
        { value: 1, numeral: 'I' }
    ];
    
    // Function to convert Arabic number to Roman numeral
    function convertToRoman(num) {
        if (num < 1 || num > 3999) return null;
        
        let result = '';
        let remaining = num;
        
        for (const { value, numeral } of romanNumerals) {
            while (remaining >= value) {
                result += numeral;
                remaining -= value;
            }
        }
        
        return result;
    }
    
    // Function to handle conversion
    function handleConversion() {
        const inputValue = numberInput.value.trim();
        const outputDisplay = output.querySelector('p');
        
        // Reset output display
        output.className = 'output-display';
        
        // Check if input is empty
        if (inputValue === '') {
            outputDisplay.textContent = 'Please enter a valid number';
            output.classList.add('error');
            return;
        }
        
        // Parse input as integer
        const number = parseInt(inputValue, 10);
        
        // Check if input is a valid number
        if (isNaN(number)) {
            outputDisplay.textContent = 'Please enter a valid number';
            output.classList.add('error');
            return;
        }
        
        // Check if number is less than 1
        if (number < 1) {
            outputDisplay.textContent = 'Please enter a number greater than or equal to 1';
            output.classList.add('error');
            return;
        }
        
        // Check if number is greater than 3999
        if (number > 3999) {
            outputDisplay.textContent = 'Please enter a number less than or equal to 3999';
            output.classList.add('error');
            return;
        }
        
        // Convert to Roman numeral
        const romanNumeral = convertToRoman(number);
        
        // Display result
        outputDisplay.textContent = romanNumeral;
        output.classList.add('success');
    }
    
    // Event listener for convert button
    convertBtn.addEventListener('click', handleConversion);
    
    // Event listener for Enter key in input field
    numberInput.addEventListener('keyup', function(event) {
        if (event.key === 'Enter') {
            handleConversion();
        }
    });
    
    // Event listener for input field to clear error state when user starts typing
    numberInput.addEventListener('input', function() {
        if (output.classList.contains('error')) {
            output.className = 'output-display';
            output.querySelector('p').textContent = 'Your result will appear here';
        }
    });
    
    // Pre-fill with an example number
    numberInput.value = '2023';
    
    // Initialize with a conversion example
    setTimeout(() => {
        handleConversion();
    }, 500);
});