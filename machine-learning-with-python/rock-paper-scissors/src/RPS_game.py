import random

def quincy(prev_play, counter=[0]):
    counter[0] += 1
    choices = ["R", "R", "P", "P", "S"]
    return choices[counter[0] % len(choices)]

def mrugesh(prev_opponent_play, opponent_history=[]):
    opponent_history.append(prev_opponent_play)
    
    # Get last 10 plays
    last_ten = opponent_history[-10:] if len(opponent_history) >= 10 else opponent_history
    
    if not last_ten:
        most_frequent = "R"
    else:
        # Find most frequent move
        counts = {"R": 0, "P": 0, "S": 0}
        for move in last_ten:
            if move in counts:
                counts[move] += 1
        
        most_frequent = max(counts, key=counts.get)
    
    # Counter the most frequent move
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[most_frequent]

def kris(prev_opponent_play):
    if prev_opponent_play == "":
        prev_opponent_play = "R"
    
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[prev_opponent_play]

def abbey(prev_opponent_play,
          opponent_history=[],
          play_order=[{
              "RR": 0, "RP": 0, "RS": 0,
              "PR": 0, "PP": 0, "PS": 0,
              "SR": 0, "SP": 0, "SS": 0,
          }]):
    
    if not prev_opponent_play:
        prev_opponent_play = 'R'
    
    opponent_history.append(prev_opponent_play)
    
    # Update play order counts
    last_two = "".join(opponent_history[-2:])
    if len(last_two) == 2:
        play_order[0][last_two] += 1
    
    # Predict next move based on last move
    potential_plays = [
        prev_opponent_play + "R",
        prev_opponent_play + "P",
        prev_opponent_play + "S",
    ]
    
    # Get counts for potential plays
    sub_order = {
        k: play_order[0][k]
        for k in potential_plays if k in play_order[0]
    }
    
    # Predict the most likely next move
    if sub_order:
        prediction = max(sub_order, key=sub_order.get)[-1:]
    else:
        prediction = random.choice(['R', 'P', 'S'])
    
    # Counter the predicted move
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[prediction]

def random_player(prev_opponent_play):
    return random.choice(['R', 'P', 'S'])

def human(prev_opponent_play):
    play = ""
    while play not in ['R', 'P', 'S']:
        play = input("[R]ock, [P]aper, [S]cissors? ").upper()
    return play