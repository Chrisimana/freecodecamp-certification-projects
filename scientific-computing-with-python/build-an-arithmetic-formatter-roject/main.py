def arithmetic_arranger(problems, show_answers=False):
    if len(problems) > 5:
        return 'Error: Too many problems.'
    
    first_line = []
    second_line = []
    dash_line = []
    answer_line = []
    
    for problem in problems:
        parts = problem.split()
        
        # Check if the problem has exactly 3 parts
        if len(parts) != 3:
            return 'Error: Invalid problem format.'
        
        num1, operator, num2 = parts
        
        # Check if operator is valid
        if operator not in ['+', '-']:
            return "Error: Operator must be '+' or '-'."
        
        # Check if numbers contain only digits
        if not num1.isdigit() or not num2.isdigit():
            return 'Error: Numbers must only contain digits.'
        
        # Check if numbers have more than 4 digits
        if len(num1) > 4 or len(num2) > 4:
            return 'Error: Numbers cannot be more than four digits.'
        
        # Calculate the width needed for this problem
        width = max(len(num1), len(num2)) + 2
        
        # Format the first line (right aligned)
        first_line.append(num1.rjust(width))
        
        # Format the second line (operator + space + number)
        second_line.append(operator + ' ' + num2.rjust(width - 2))
        
        # Format the dash line
        dash_line.append('-' * width)
        
        # Calculate and format answer if needed
        if show_answers:
            if operator == '+':
                answer = str(int(num1) + int(num2))
            else:
                answer = str(int(num1) - int(num2))
            answer_line.append(answer.rjust(width))
    
    # Combine all lines with 4 spaces between problems
    arranged_problems = '    '.join(first_line) + '\n'
    arranged_problems += '    '.join(second_line) + '\n'
    arranged_problems += '    '.join(dash_line)
    
    # Add answers if requested
    if show_answers:
        arranged_problems += '\n' + '    '.join(answer_line)
    
    return arranged_problems


# Test all
if __name__ == "__main__":
    print("ARITHMETIC ARRANGER - ALL TEST CASES")
    
    # Test Case 1
    print("\nTest Case 1:")
    print("Input: arithmetic_arranger(['3801 - 2', '123 + 49'])")
    print("Expected:   3801      123\n-    2    +  49\n------    -----")
    print("\nActual Output:")
    result1 = arithmetic_arranger(["3801 - 2", "123 + 49"])
    print(result1)
    
    # Test Case 2
    print("\nTest Case 2:")
    print("Input: arithmetic_arranger(['1 + 2', '1 - 9380'])")
    print("Expected:   1         1\n+ 2    - 9380\n---    ------")
    print("\nActual Output:")
    result2 = arithmetic_arranger(["1 + 2", "1 - 9380"])
    print(result2)
    
    # Test Case 3
    print("\nTest Case 3:")
    print("Input: arithmetic_arranger(['3 + 855', '3801 - 2', '45 + 43', '123 + 49'])")
    print("Expected:    3      3801      45      123\n+ 855    -    2    + 43    +  49\n-----    ------    ----    -----")
    print("\nActual Output:")
    result3 = arithmetic_arranger(["3 + 855", "3801 - 2", "45 + 43", "123 + 49"])
    print(result3)
    
    # Test Case 4
    print("\nTest Case 4:")
    print("Input: arithmetic_arranger(['11 + 4', '3801 - 2999', '1 + 2', '123 + 49', '1 - 9380'])")
    print("Expected:   11      3801      1      123         1\n+  4    - 2999    + 2    +  49    - 9380\n----    ------    ---    -----    ------")
    print("\nActual Output:")
    result4 = arithmetic_arranger(["11 + 4", "3801 - 2999", "1 + 2", "123 + 49", "1 - 9380"])
    print(result4)
    print("-" * 50)
    
    # Test Case 5
    print("\nTest Case 5:")
    print("Input: arithmetic_arranger(['44 + 815', '909 - 2', '45 + 43', '123 + 49', '888 + 40', '653 + 87'])")
    print("Expected: Error: Too many problems.")
    print("\nActual Output:")
    result5 = arithmetic_arranger(["44 + 815", "909 - 2", "45 + 43", "123 + 49", "888 + 40", "653 + 87"])
    print(result5)
    
    # Test Case 6
    print("\nTest Case 6:")
    print("Input: arithmetic_arranger(['3 / 855', '3801 - 2', '45 + 43', '123 + 49'])")
    print("Expected: Error: Operator must be '+' or '-'.")
    print("\nActual Output:")
    result6 = arithmetic_arranger(["3 / 855", "3801 - 2", "45 + 43", "123 + 49"])
    print(result6)
    
    # Test Case 7
    print("\nTest Case 7:")
    print("Input: arithmetic_arranger(['24 + 85215', '3801 - 2', '45 + 43', '123 + 49'])")
    print("Expected: Error: Numbers cannot be more than four digits.")
    print("\nActual Output:")
    result7 = arithmetic_arranger(["24 + 85215", "3801 - 2", "45 + 43", "123 + 49"])
    print(result7)
    
    # Test Case 8
    print("\nTest Case 8:")
    print("Input: arithmetic_arranger(['98 + 3g5', '3801 - 2', '45 + 43', '123 + 49'])")
    print("Expected: Error: Numbers must only contain digits.")
    print("\nActual Output:")
    result8 = arithmetic_arranger(["98 + 3g5", "3801 - 2", "45 + 43", "123 + 49"])
    print(result8)
    
    # Test Case 9
    print("\nTest Case 9:")
    print("Input: arithmetic_arranger(['3 + 855', '988 + 40'], True)")
    print("Expected:    3      988\n+ 855    +  40\n-----    -----\n  858     1028")
    print("\nActual Output:")
    result9 = arithmetic_arranger(["3 + 855", "988 + 40"], True)
    print(result9)
    
    # Test Case 10
    print("\nTest Case 10:")
    print("Input: arithmetic_arranger(['32 - 698', '1 - 3801', '45 + 43', '123 + 49', '988 + 40'], True)")
    print("Expected:   32         1      45      123      988\n- 698    - 3801    + 43    +  49    +  40\n-----    ------    ----    -----    -----\n -666     -3800      88      172     1028")
    print("\nActual Output:")
    result10 = arithmetic_arranger(["32 - 698", "1 - 3801", "45 + 43", "123 + 49", "988 + 40"], True)
    print(result10)
