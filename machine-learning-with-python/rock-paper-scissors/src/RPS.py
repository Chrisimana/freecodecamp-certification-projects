import random
from collections import Counter, defaultdict

# Variabel global untuk menyimpan state
opponent_history = []
my_history = []
play_order = defaultdict(int)
last_ten_moves = []
opponent_type = None
move_count = 0

def player(prev_play, opponent_history_param=None):
    global opponent_history, my_history, play_order, last_ten_moves, opponent_type, move_count
    
    # Reset state untuk game pertama
    if prev_play == "":
        opponent_history = []
        my_history = []
        play_order = defaultdict(int)
        last_ten_moves = []
        opponent_type = None
        move_count = 0
        
        # Mulai dengan move random
        my_move = random.choice(['R', 'P', 'S'])
        my_history.append(my_move)
        move_count += 1
        return my_move
    
    # Simpan move lawan
    opponent_history.append(prev_play)
    
    # Update last ten moves
    last_ten_moves.append(prev_play)
    if len(last_ten_moves) > 10:
        last_ten_moves.pop(0)
    
    # Identifikasi tipe lawan setelah beberapa move
    if opponent_type is None and len(opponent_history) >= 15:
        opponent_type = identify_opponent()
    
    # Tentukan strategi berdasarkan lawan
    if opponent_type == "quincy":
        my_move = counter_quincy()
    elif opponent_type == "mrugesh":
        my_move = counter_mrugesh()
    elif opponent_type == "kris":
        my_move = counter_kris()
    elif opponent_type == "abbey":
        my_move = counter_abbey()
    else:
        # Gunakan strategi adaptive untuk lawan yang belum teridentifikasi
        my_move = adaptive_strategy()
    
    # Tambahkan sedikit randomness untuk menghindari pattern yang mudah ditebak
    if len(my_history) > 5 and random.random() < 0.05:
        my_move = random.choice(['R', 'P', 'S'])
    
    # Simpan move saya
    my_history.append(my_move)
    
    # Update play order untuk pattern recognition
    if len(my_history) >= 2:
        last_two = ''.join(my_history[-2:])
        play_order[last_two] += 1
    
    move_count += 1
    return my_move

def identify_opponent():
    
    if len(opponent_history) < 10:
        return None
    
    # Cek Quincy (pattern tetap: R, R, P, P, S)
    quincy_pattern = ['R', 'R', 'P', 'P', 'S']
    quincy_score = 0
    for i in range(min(15, len(opponent_history))):
        if opponent_history[i] == quincy_pattern[i % 5]:
            quincy_score += 1
    
    if quincy_score >= 12:  # 80% match
        return "quincy"
    
    # Cek Kris (selalu counter last move kita)
    kris_score = 0
    if len(my_history) >= 10:
        for i in range(1, min(10, len(opponent_history))):
            if i < len(my_history):
                my_last_move = my_history[i-1]
                if my_last_move == 'R' and opponent_history[i] == 'P':
                    kris_score += 1
                elif my_last_move == 'P' and opponent_history[i] == 'S':
                    kris_score += 1
                elif my_last_move == 'S' and opponent_history[i] == 'R':
                    kris_score += 1
        
        if kris_score >= 6:  # 60% match
            return "kris"
    
    # Mrugesh akan counter move kita yang paling sering muncul
    mrugesh_score = 0
    if len(my_history) >= 11:
        for i in range(10, min(15, len(opponent_history))):
            if i < len(my_history):
                last_ten_my_moves = my_history[i-10:i]
                if last_ten_my_moves:
                    most_freq = Counter(last_ten_my_moves).most_common(1)[0][0]
                    expected_counter = {'R': 'P', 'P': 'S', 'S': 'R'}[most_freq]
                    if opponent_history[i] == expected_counter:
                        mrugesh_score += 1
        
        if mrugesh_score >= 3:  # Pattern detection untuk sample kecil
            return "mrugesh"
    
    # Default: Abbey (menggunakan pattern dari 2 move terakhir kita)
    return "abbey"

def counter_quincy():
    pattern = ['R', 'R', 'P', 'P', 'S']
    next_move = pattern[move_count % 5]
    
    # Counter move yang akan dimainkan Quincy
    counter_moves = {'R': 'P', 'P': 'S', 'S': 'R'}
    return counter_moves[next_move]

def counter_mrugesh():
    if len(my_history) == 0:
        return random.choice(['R', 'P', 'S'])
    
    # Mrugesh melihat 10 move terakhir kita dan counter yang paling sering
    last_ten = my_history[-10:] if len(my_history) >= 10 else my_history
    if last_ten:
        most_frequent = Counter(last_ten).most_common(1)[0][0]
        # Mrugesh akan memainkan counter untuk most_frequent kita
        mrugesh_move = {'R': 'P', 'P': 'S', 'S': 'R'}[most_frequent]
        # Kita counter move Mrugesh
        return {'R': 'P', 'P': 'S', 'S': 'R'}[mrugesh_move]
    
    return random.choice(['R', 'P', 'S'])

def counter_kris():
    if len(my_history) == 0:
        return random.choice(['R', 'P', 'S'])
    
    # Kris akan counter last move kita
    my_last_move = my_history[-1]
    kris_move = {'R': 'P', 'P': 'S', 'S': 'R'}[my_last_move]
    
    # Kita counter move Kris
    return {'R': 'P', 'P': 'S', 'S': 'R'}[kris_move]

def counter_abbey():
    if len(my_history) < 2:
        return random.choice(['R', 'P', 'S'])
    
    # Abbey melihat 2 move terakhir kita
    last_two = ''.join(my_history[-2:])
    
    # Abbey akan memprediksi berdasarkan pattern
    predictions = {
        'RR': 'R', 'RP': 'P', 'RS': 'S',
        'PR': 'R', 'PP': 'P', 'PS': 'S',
        'SR': 'R', 'SP': 'P', 'SS': 'S'
    }
    
    if last_two in predictions:
        abbey_move = predictions[last_two]
        # Abbey akan counter prediksinya sendiri
        abbey_play = {'R': 'P', 'P': 'S', 'S': 'R'}[abbey_move]
        # Kita counter move Abbey
        return {'R': 'P', 'P': 'S', 'S': 'R'}[abbey_play]
    
    return random.choice(['R', 'P', 'S'])

def adaptive_strategy():
    if len(opponent_history) < 3:
        return random.choice(['R', 'P', 'S'])
    
    # Coba cari pattern dari lawan
    last_three = opponent_history[-3:]
    
    # Jika lawan sering mengulang move yang sama
    if len(set(last_three)) == 1:
        # Lawan predictable, counter move yang diulang
        repeated_move = last_three[0]
        return {'R': 'P', 'P': 'S', 'S': 'R'}[repeated_move]
    
    # Coba prediksi berdasarkan frekuensi
    freq = Counter(opponent_history[-10:] if len(opponent_history) >= 10 else opponent_history)
    if freq:
        most_common = freq.most_common(1)[0][0]
        # Counter move yang paling sering dimainkan lawan
        return {'R': 'P', 'P': 'S', 'S': 'R'}[most_common]
    
    # Default: random dengan bias terhadap move yang belum sering dimainkan
    all_moves = ['R', 'P', 'S']
    if len(opponent_history) >= 5:
        # Kurangi kemungkinan memainkan move yang sering di-counter lawan
        opponent_counter_pattern = []
        for i in range(1, min(10, len(opponent_history))):
            if i < len(my_history):
                if opponent_history[i] == 'P' and my_history[i-1] == 'R':
                    opponent_counter_pattern.append('R')
                elif opponent_history[i] == 'S' and my_history[i-1] == 'P':
                    opponent_counter_pattern.append('P')
                elif opponent_history[i] == 'R' and my_history[i-1] == 'S':
                    opponent_counter_pattern.append('S')
        
        if opponent_counter_pattern:
            freq_counter = Counter(opponent_counter_pattern)
            least_countered = min(all_moves, key=lambda x: freq_counter.get(x, 0))
            return least_countered
    
    return random.choice(all_moves)