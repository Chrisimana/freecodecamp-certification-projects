import copy
import random

class Hat:
    def __init__(self, **kwargs):
        self.contents = []
        for color, count in kwargs.items():
            self.contents.extend([color] * count)
    
    def draw(self, num_balls):
        if num_balls >= len(self.contents):
            drawn_balls = self.contents.copy()
            self.contents.clear()
            return drawn_balls
        
        drawn_balls = []
        for _ in range(num_balls):
            ball_index = random.randrange(len(self.contents))
            drawn_balls.append(self.contents.pop(ball_index))
        return drawn_balls

def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    success_count = 0
    
    for _ in range(num_experiments):
        # Create a deep copy of the hat for each experiment
        hat_copy = copy.deepcopy(hat)
        
        # Draw the specified number of balls
        drawn_balls = hat_copy.draw(num_balls_drawn)
        
        # Count how many of each color were drawn
        drawn_count = {}
        for ball in drawn_balls:
            drawn_count[ball] = drawn_count.get(ball, 0) + 1
        
        # Check if we got at least the expected balls
        success = True
        for color, expected_count in expected_balls.items():
            if drawn_count.get(color, 0) < expected_count:
                success = False
                break
        
        if success:
            success_count += 1
    
    return success_count / num_experiments
