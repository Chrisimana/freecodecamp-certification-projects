import unittest
import RPS
import RPS_game

class TestRPS(unittest.TestCase):
    
    def test_player_reset(self):
        # Panggil pertama kali dengan empty string
        first_move = RPS.player("")
        self.assertIn(first_move, ['R', 'P', 'S'])
    
    def test_against_quincy(self):
        wins = 0
        total = 100
        
        # Reset player
        RPS.player("")
        
        prev_play = ""
        for _ in range(total):
            my_move = RPS.player(prev_play)
            quincy_move = RPS_game.quincy("")
            
            if (my_move == "R" and quincy_move == "S") or \
               (my_move == "P" and quincy_move == "R") or \
               (my_move == "S" and quincy_move == "P"):
                wins += 1
            
            prev_play = quincy_move
        
        win_rate = wins / total * 100
        print(f"Win rate against Quincy: {win_rate}%")
        self.assertGreaterEqual(win_rate, 50)

if __name__ == '__main__':
    unittest.main()