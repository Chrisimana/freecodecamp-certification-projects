def add_time(start, duration, start_day=None):
    # Parse the start time
    time_part, period = start.split()
    hours, minutes = map(int, time_part.split(':'))
    
    # Convert to 24-hour format for easier calculation
    if period == 'PM' and hours != 12:
        hours += 12
    elif period == 'AM' and hours == 12:
        hours = 0
    
    # Parse the duration
    dur_hours, dur_minutes = map(int, duration.split(':'))
    
    # Add the duration
    total_minutes = minutes + dur_minutes
    total_hours = hours + dur_hours + total_minutes // 60
    final_minutes = total_minutes % 60
    
    # Calculate days passed
    days_passed = total_hours // 24
    final_hours_24 = total_hours % 24
    
    # Convert back to 12-hour format
    if final_hours_24 == 0:
        final_hours_12 = 12
        final_period = 'AM'
    elif final_hours_24 == 12:
        final_hours_12 = 12
        final_period = 'PM'
    elif final_hours_24 > 12:
        final_hours_12 = final_hours_24 - 12
        final_period = 'PM'
    else:
        final_hours_12 = final_hours_24
        final_period = 'AM'
    
    # Format minutes with leading zero if needed
    final_minutes_str = f"{final_minutes:02d}"
    
    # Build the result string
    result = f"{final_hours_12}:{final_minutes_str} {final_period}"
    
    # Handle day of week if provided
    if start_day:
        days_of_week = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        start_day_index = days_of_week.index(start_day.lower())
        final_day_index = (start_day_index + days_passed) % 7
        final_day = days_of_week[final_day_index].capitalize()
        result += f", {final_day}"
    
    # Add day information
    if days_passed == 1:
        result += " (next day)"
    elif days_passed > 1:
        result += f" ({days_passed} days later)"
    
    return result


# Test Cases
def run_tests():
    print("Running tests...\n")
    
    # Test 1
    result1 = add_time('3:30 PM', '2:12')
    expected1 = '5:42 PM'
    print(f"Test 1: {result1} - {'PASS' if result1 == expected1 else 'FAIL'}")
    
    # Test 2
    result2 = add_time('11:55 AM', '3:12')
    expected2 = '3:07 PM'
    print(f"Test 2: {result2} - {'PASS' if result2 == expected2 else 'FAIL'}")
    
    # Test 3 - Next day
    result3 = add_time('10:10 PM', '3:30')
    expected3 = '1:40 AM (next day)'
    print(f"Test 3: {result3} - {'PASS' if result3 == expected3 else 'FAIL'}")
    
    # Test 4 - AM to PM change at 12:00
    result4 = add_time('11:43 AM', '00:20')
    expected4 = '12:03 PM'
    print(f"Test 4: {result4} - {'PASS' if result4 == expected4 else 'FAIL'}")
    
    # Test 5 - 24 hours later
    result5 = add_time('2:59 AM', '24:00')
    expected5 = '2:59 AM (next day)'
    print(f"Test 5: {result5} - {'PASS' if result5 == expected5 else 'FAIL'}")
    
    # Test 6 - Multiple days later
    result6 = add_time('11:59 PM', '24:05')
    expected6 = '12:04 AM (2 days later)'
    print(f"Test 6: {result6} - {'PASS' if result6 == expected6 else 'FAIL'}")
    
    # Test 7 - Many days later
    result7 = add_time('8:16 PM', '466:02')
    expected7 = '6:18 AM (20 days later)'
    print(f"Test 7: {result7} - {'PASS' if result7 == expected7 else 'FAIL'}")
    
    # Test 8 - Adding 0:00
    result8 = add_time('3:30 PM', '0:00')
    expected8 = '3:30 PM'
    print(f"Test 8: {result8} - {'PASS' if result8 == expected8 else 'FAIL'}")
    
    # Test 9 - With day of week (same day)
    result9 = add_time('3:30 PM', '2:12', 'Monday')
    expected9 = '5:42 PM, Monday'
    print(f"Test 9: {result9} - {'PASS' if result9 == expected9 else 'FAIL'}")
    
    # Test 10 - With day of week (next day)
    result10 = add_time('2:59 AM', '24:00', 'saturDay')
    expected10 = '2:59 AM, Sunday (next day)'
    print(f"Test 10: {result10} - {'PASS' if result10 == expected10 else 'FAIL'}")
    
    # Test 11 - With day of week (multiple days)
    result11 = add_time('11:59 PM', '24:05', 'Wednesday')
    expected11 = '12:04 AM, Friday (2 days later)'
    print(f"Test 11: {result11} - {'PASS' if result11 == expected11 else 'FAIL'}")
    
    # Test 12 - With day of week (many days)
    result12 = add_time('8:16 PM', '466:02', 'tuesday')
    expected12 = '6:18 AM, Monday (20 days later)'
    print(f"Test 12: {result12} - {'PASS' if result12 == expected12 else 'FAIL'}")


# Run all tests
if __name__ == "__main__":
    run_tests()
