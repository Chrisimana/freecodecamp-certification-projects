import math
from fractions import Fraction
import sympy as sp

def solve_proportion():
    print("\nSolving Proportion (a/b = c/d)")
    try:
        a = float(input("Enter a: "))
        b = float(input("Enter b: "))
        c = float(input("Enter c: "))
        d = input("Enter d (or 'x' to solve for x): ")

        if d.lower() == 'x':
            if a == 0:
                print("Error: Division by zero")
                return
            x = (b * c) / a
            print(f"Solution: x = {x}")
        else:
            d = float(d)
            # Check if a/b equals c/d
            result = (a * d) == (b * c)
            print(f"The proportion is {'true' if result else 'false'}")
            if not result:
                print(f"Cross multiplication: {a}*{d} = {a*d} vs {b}*{c} = {b*c}")
    except ValueError:
        print("Invalid input. Please enter numbers.")

def solve_for_x():
    print("\nSolving equation for x (ax + b = c)")
    try:
        a = float(input("Enter coefficient of x (a): "))
        b = float(input("Enter constant (b): "))
        c = float(input("Enter right-hand side value (c): "))

        if a == 0:
            if b == c:
                print("Infinite solutions (identity)")
            else:
                print("No solution (contradiction)")
        else:
            x = (c - b) / a
            print(f"Solution: x = {x}")
    except ValueError:
        print("Invalid input. Please enter numbers.")

def factor_square_root():
    print("\nFactoring Square Roots (√n)")
    try:
        n = int(input("Enter a positive integer: "))
        if n < 0:
            print("Please enter a positive integer.")
            return

        largest_square = 1
        remainder = n

        # Find the largest perfect square factor
        for i in range(int(math.sqrt(n)), 0, -1):
            if n % (i*i) == 0:
                largest_square = i*i
                remainder = n // largest_square
                break

        if largest_square == 1:
            print(f"√{n} cannot be simplified further")
        else:
            print(f"√{n} = {int(math.sqrt(largest_square))}√{remainder}")
    except ValueError:
        print("Invalid input. Please enter an integer.")

def convert_decimal():
    print("\nConverting Decimal to Fraction and Percentage")
    try:
        decimal = float(input("Enter a decimal number: "))

        # Convert to fraction
        fraction = Fraction(decimal).limit_denominator()
        print(f"Fraction: {fraction.numerator}/{fraction.denominator}")

        # Convert to percentage
        percentage = decimal * 100
        print(f"Percentage: {percentage}%")
    except ValueError:
        print("Invalid input. Please enter a number.")

def convert_fraction():
    print("\nConverting Fraction to Decimal and Percentage")
    try:
        numerator = float(input("Enter numerator: "))
        denominator = float(input("Enter denominator: "))

        if denominator == 0:
            print("Error: Denominator cannot be zero")
            return

        decimal = numerator / denominator
        percentage = decimal * 100

        print(f"Decimal: {decimal}")
        print(f"Percentage: {percentage}%")
    except ValueError:
        print("Invalid input. Please enter numbers.")

def convert_percentage():
    print("\nConverting Percentage to Decimal and Fraction")
    try:
        percentage = float(input("Enter percentage (without % sign): "))

        decimal = percentage / 100
        fraction = Fraction(decimal).limit_denominator()

        print(f"Decimal: {decimal}")
        print(f"Fraction: {fraction.numerator}/{fraction.denominator}")
    except ValueError:
        print("Invalid input. Please enter a number.")

def main():
    print("Multi-Function Calculator")
    print("=======================")

    while True:
        print("\nSelect operation:")
        print("1. Solve proportion")
        print("2. Solve for x in equation")
        print("3. Factor square roots")
        print("4. Convert decimal to fraction and percentage")
        print("5. Convert fraction to decimal and percentage")
        print("6. Convert percentage to decimal and fraction")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            solve_proportion()
        elif choice == '2':
            solve_for_x()
        elif choice == '3':
            factor_square_root()
        elif choice == '4':
            convert_decimal()
        elif choice == '5':
            convert_fraction()
        elif choice == '6':
            convert_percentage()
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()