from copy import deepcopy
import nim
from nim import Nim

NIM_SIZE=4

def evaluation(state: Nim) -> int:
    if not state:
        return -1
    else:
        return 0

def generate_possible_moves(board : Nim, state: dict()) -> None:
    if board not in state:
        state[board] = list()

    possible_moves = [(r, o) for r, c in enumerate(board.rows) for o in range(1, c + 1)]

    for ply in possible_moves:
        tmp = deepcopy(board)
        if ply not in state.values():
            state[board].append(ply)
            generate_possible_moves(tmp.nimming(ply),state)

def minMax(state: Nim, dict_of_states:dict(), player:int):
    val = evaluation(state)
    if val != 0:
        return None, val

    moves = dict_of_states[state]
    results = list()
    
    for ply in moves:
        tmp = deepcopy(state)
        _ , val = minMax(tmp.nimming(ply), dict_of_states, 1-player)
        results.append((ply, -val))
        
    return max(results, key=lambda x: x[1])

if __name__ == "__main__":
    board = Nim(NIM_SIZE)
    dict_of_states = dict()
    generate_possible_moves(board, dict_of_states)
    sum = 0
    for _ in dict_of_states.values():
        if len(_) != 0:
            sum = sum+1
    print(sum)
    print(len(dict_of_states.keys()))
    #i = 1#random.randint(0,1)
    #player2 = nim.opponent_strategy()
    #while board:
    #    if i % 2 != 0:
    #        ply, _ = minMax(board, dict_of_states, 1)
    #        player = 0
    #    else:
    #        opponent = player2.move()
    #        ply = opponent(board)
    #        player = 1
    #    board.nimming(ply)
    #    i+=1
    #if player == 1:
    #    print("YOU LOSE")
    #else:
    #    print("YOU WIN")


