import random
from nim import Nim, Strategy
import nim
from copy import deepcopy
import time

NIM_SIZE=8

def evaluation(state: Nim) -> int:
    if not state:
        return -1
    else:
        return 0

def generate_possible_moves(state : Nim):
    possible_moves = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]
    return possible_moves
    

def minMax(state: Nim, dict_of_states: dict()):
    val = evaluation(state)
    if val != 0:
        return None, val

    # Check if the moves for this states are already available
    if state.rows not in dict_of_states and state:
        dict_of_states[state.rows] = list()
        moves = generate_possible_moves(state)
        for move in moves:
            if move not in dict_of_states[state.rows]:
                dict_of_states[state.rows].append((move,-1))
    # Otherwise recover them from the dictionary
    else:
        return max(dict_of_states[state.rows], key=lambda x: x[1])

    results = list()

    for ply in moves:
        tmp_state = deepcopy(state)
        _ , val = minMax(tmp_state.nimming(ply), dict_of_states)
        results.append((ply, -val))
        if -val == 1:
            dict_of_states[state.rows] = [(ply,-val)]
            break

    return max(results, key=lambda x: x[1])

#idea: salvarci nel dict già la mossa (ply) migliore

if __name__ == "__main__":
    start = time.time()
    board = Nim(NIM_SIZE)
    dict_of_states = dict()
    i = 1#random.randint(0,1)
    player2 = nim.opponent_strategy()
    while board:
        if i % 2 != 0:
            ply, _ = minMax(board, dict_of_states)
            player = 0
        else:
            opponent = player2.move()
            ply = opponent(board)
            player = 1
        board.nimming(ply)
        i+=1
    if player == 1:
        print("YOU LOSE")
    else:
        print("YOU WIN")
    
    sum = 0
    for _ in dict_of_states.values():
        sum += len(_)
    print(sum)
    print(len(dict_of_states.keys()))

    end = time.time()
    print(f"Computational time: {(end - start)//60} mins and {(end-start)-(((end - start)//60)*60)} secs")