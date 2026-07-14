def hanoi_solver(n):
    # Initialize the three rods
    rods = [
        list(range(n, 0, -1)), 
        [],                     
        []                      
    ]
    
    # List to store all states as strings
    states = []
    
    # Add initial state
    states.append(format_rods(rods))
    
    # Recursive helper function to solve the puzzle
    def move_disks(num_disks, source, target, auxiliary):
        if num_disks == 1:
            # Move one disk from source to target
            disk = rods[source].pop()
            rods[target].append(disk)
            states.append(format_rods(rods))
        else:
            # Move top n-1 disks from source to auxiliary using target as buffer
            move_disks(num_disks - 1, source, auxiliary, target)
            
            # Move the largest disk from source to target
            disk = rods[source].pop()
            rods[target].append(disk)
            states.append(format_rods(rods))
            
            # Move the n-1 disks from auxiliary to target using source as buffer
            move_disks(num_disks - 1, auxiliary, target, source)
    
    # Start solving: move n disks from rod 0 to rod 2 using rod 1 as auxiliary
    move_disks(n, 0, 2, 1)
    
    # Join all states with newlines
    return '\n'.join(states)


def format_rods(rods):
    """
    Format the three rods into the required string representation.
    Each rod is represented as a list of integers, with smallest disk = 1.
    """
    return f"{rods[0]} {rods[1]} {rods[2]}"


# Test the implementation
if __name__ == "__main__":
    # Test with 2 disks
    print("Testing with 2 disks:")
    print(hanoi_solver(2))
    print()
    
    # Test with 3 disks
    print("Testing with 3 disks:")
    print(hanoi_solver(3))
    print()
    
    # Test with 4 disks
    print("Testing with 4 disks:")
    print(hanoi_solver(4))
    print()
    
    # Verify move count: 2^n - 1
    for n in range(1, 6):
        moves = hanoi_solver(n).count('\n') + 1  # Count states
        expected = 2 ** n - 1 + 1  # +1 for initial state
        print(f"n={n}: moves={moves}, expected={expected} {'O' if moves == expected else 'X'}")