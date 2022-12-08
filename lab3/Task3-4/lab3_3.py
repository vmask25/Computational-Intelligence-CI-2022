import random
from nim import Nim, Strategy
import nim
from copy import deepcopy
import time

NIM_SIZE=10

# TODO: fix the code to be able to play whatever NIM_SIZE (even if it plays badly)

def evaluation(state: Nim) -> int:
    if not state:
        return -1
    else:
        return 0

def generate_possible_moves(state : Nim):
    possible_moves = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]
    return possible_moves
    

def minMax(state: Nim, dict_of_states: dict(), current_dict_size: int):
    val = evaluation(state)
    if val != 0:
        return None, val

    # Depth limiting if the current state is not already known and stable (nim sum evaluation)
    if state and current_dict_size >= 100000:
        if state.rows not in dict_of_states:
            return random.choice(generate_possible_moves(state)), 1
        else: 
            return max(dict_of_states[state.rows], key=lambda x: x[1])

    results = list()

    if state.rows not in dict_of_states and state:
        dict_of_states[state.rows] = list()
        current_dict_size+=1
        if current_dict_size >= 100000:
            print("CIAOOO")
            return (0,1), 1
        for ply in [(len(state.rows)-1-r, o) for r, c in enumerate(reversed(state.rows)) for o in range(1, c + 1)]: #used "list comprehension" for optimization
            dict_of_states[state.rows].append((ply,-1))
            tmp_state = deepcopy(state)
            _ , val = minMax(tmp_state.nimming(ply), dict_of_states, current_dict_size)
            results.append((ply, -val))
            if -val == 1:
                dict_of_states[state.rows] = [(ply,-val)]
                break
    else:
        return max(dict_of_states[state.rows], key=lambda x: x[1])  
        
    ## Check if the moves for this states are already available
    #if state.rows not in dict_of_states and state:
    #    dict_of_states[state.rows] = list()
    #    current_dict_size+=1
    #    moves = generate_possible_moves(state)
    #    for move in moves:
    #        if move not in dict_of_states[state.rows]:
    #            dict_of_states[state.rows].append((move,-1))
    ## Otherwise recover them from the dictionary
    #else:
    #    return max(dict_of_states[state.rows], key=lambda x: x[1])
#
    #results = list()
#
    #for ply in moves:
    #    tmp_state = deepcopy(state)
    #    _ , val = minMax(tmp_state.nimming(ply), dict_of_states, current_dict_size)
    #    results.append((ply, -val))
    #    if -val == 1:
    #        dict_of_states[state.rows] = [(ply,-val)]
    #        break

    return max(results, key=lambda x: x[1])

if __name__ == "__main__":
    start = time.time()
    try:
        current_dict_size = 0
        count_moves = 0
        board = Nim(NIM_SIZE)
        dict_of_states = dict()
        i = 1#random.randint(0,1)
        player2 = nim.opponent_strategy()
        while board:
            if i % 2 != 0:
                ply, _ = minMax(board, dict_of_states, current_dict_size)
                if current_dict_size >= 100000:
                    count_moves += 2
                    if count_moves == 6:
                        current_dict_size = 0
                        count_moves = 0
                player = 0
            else:
                opponent = player2.move()
                ply = opponent(board)
                player = 1
            board.nimming(ply)
            print(board)
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
    except KeyboardInterrupt:
        sum = 0
        for _ in dict_of_states.values():
            sum = sum + len(_)
        print(len(dict_of_states.keys()))
        end = time.time()
        print(f"Computational time: {(end - start)//60} mins and {(end-start)-(((end - start)//60)*60)} secs")