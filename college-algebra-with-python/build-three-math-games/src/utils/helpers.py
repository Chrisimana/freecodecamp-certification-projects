import random

def format_number(number, decimals=2):
    # Format number with specified decimals
    return f"{number:.{decimals}f}"

def random_in_range(min_val, max_val, decimals=2):
    # Generate random number within range
    return round(random.uniform(min_val, max_val), decimals)

def clean_input(text):
    # Clean input string
    return text.strip() if text else ""