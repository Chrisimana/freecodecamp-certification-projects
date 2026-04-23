import RPS
import RPS_game

def play(player1, player2, num_games, verbose=False):
    
    p1_prev_play = ""
    p2_prev_play = ""
    results = {"p1": 0, "p2": 0, "tie": 0}
    
    for i in range(num_games):
        p1_play = player1(p2_prev_play)
        p2_play = player2(p1_prev_play)
        
        if p1_play == p2_play:
            results["tie"] += 1
            winner = "Tie."
        elif (p1_play == "P" and p2_play == "R") or \
             (p1_play == "R" and p2_play == "S") or \
             (p1_play == "S" and p2_play == "P"):
            results["p1"] += 1
            winner = "Player 1 wins."
        else:
            results["p2"] += 1
            winner = "Player 2 wins."
        
        if verbose:
            print(f"Game {i+1}: Player 1: {p1_play} | Player 2: {p2_play} | {winner}")
        
        p1_prev_play = p1_play
        p2_prev_play = p2_play
    
    # Hitung win rate
    games_won = results["p1"] + results["p2"]
    if games_won == 0:
        win_rate = 0
    else:
        win_rate = results["p1"] / games_won * 100
    
    print(f"\n{'='*50}")
    print(f"MATCH RESULTS")
    print(f"{'='*50}")
    print(f"Games played: {num_games}")
    print(f"Player 1 wins: {results['p1']}")
    print(f"Player 2 wins: {results['p2']}")
    print(f"Ties: {results['tie']}")
    print(f"Player 1 win rate: {win_rate:.2f}%")
    
    if win_rate >= 60:
        print(f"✓ SUCCESS: Player 1 meets the 60% win rate requirement!")
    else:
        print(f"✗ FAIL: Player 1 does NOT meet the 60% win rate requirement.")
    
    print(f"{'='*50}")
    
    return win_rate

def run_all_tests():
    
    print("\n" + "="*60)
    print("ROCK PAPER SCISSORS CHALLENGE")
    print("="*60)
    
    bots = [
        ("Quincy", RPS_game.quincy),
        ("Mrugesh", RPS_game.mrugesh),
        ("Kris", RPS_game.kris),
        ("Abbey", RPS_game.abbey)
    ]
    
    results = []
    
    for bot_name, bot_function in bots:
        print(f"\n\nTesting against {bot_name}...")
        print("-"*40)
        
        win_rate = play(RPS.player, bot_function, 1000, verbose=False)
        results.append((bot_name, win_rate))
    
    # Summary
    print("\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)
    
    all_passed = True
    for bot_name, win_rate in results:
        passed = win_rate >= 60
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{bot_name}: {win_rate:.2f}% - {status}")
        
        if not passed:
            all_passed = False
    
    print(f"\nOverall result: {'ALL TESTS PASSED!' if all_passed else 'SOME TESTS FAILED'}")
    print("="*60)

if __name__ == "__main__":
    run_all_tests()