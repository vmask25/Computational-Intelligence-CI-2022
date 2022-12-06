import logging
import random
from typing import Callable
import nim
from nim import Nim, Nimply

from collections import namedtuple
from copy import deepcopy
import random

Nimply = namedtuple("Nimply", "row, num_objects")

class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        self._k = k

    # this allow to use the while loop on the object (when all rows are zeroed this returns false)
    def __bool__(self):
        return sum(self._rows) > 0

    # representation "override"
    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)
    
    @property
    def k(self) -> int:
        return self._k

    def nimming(self, ply: Nimply) -> None:
        row, num_objects = ply
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects


# Sample (and silly) strategies

def nim_sum(state: Nim) -> int:
    result = state.rows[0]
    for row in state.rows[1:]:
        result = result ^ row
    return result

def cook_status(state: Nim) -> dict:
    cooked = dict()
    cooked['possible_moves'] = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state.k is None or o <= state.k]
    cooked['active_rows_number'] = sum(o > 0 for o in state.rows)
    cooked['even_object_rows'] = [x for x in enumerate(state.rows) if x[1] % 2 == 0]
    cooked['odd_object_rows'] = [x for x in enumerate(state.rows) if x[1] % 2 != 0]
    cooked['shortest_row'] = min((x for x in enumerate(state.rows) if x[1] > 0), key=lambda y:y[1])[0]
    cooked['longest_row'] = max((x for x in enumerate(state.rows)), key=lambda y:y[1])[0]
    cooked['nim_sum'] = nim_sum(state)

    brute_force = list()
    for m in cooked['possible_moves']:
        tmp = deepcopy(state)
        tmp.nimming(m)
        brute_force.append((m, nim_sum(tmp)))
    cooked['brute_force'] = brute_force

    return cooked

def optimal_strategy(state: Nim) -> Nimply:
    data = cook_status(state)
    #return next(m for m in data['possible_moves'] if m[1] == data['min_sum'])
    return next((bf for bf in data['brute_force'] if bf[1] == 0), random.choice(data['brute_force']))[0]

def pure_random(state: Nim) -> Nimply:
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)

def gabriele(state: Nim) -> Nimply:
    """Pick always the maximum possible number of the lowest row"""
    possible_moves = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]
    return Nimply(*max(possible_moves, key=lambda m: (-m[0], m[1])))

def shortest_row(state: Nim) -> Nimply:
    data = cook_status(state)
    return Nimply(data['shortest_row'], random.randint(1, state.rows[data['shortest_row']]))

def longest_row(state: Nim) -> Nimply:
    data = cook_status(state)
    return Nimply(data['longest_row'], random.randint(1, state.rows[data['longest_row']]))

def pick_one_from_max(state: Nim) -> Nimply:
    data = cook_status(state)
    return Nimply(data['longest_row'], 1)

def pick_one_from_min(state: Nim) -> Nimply:
    data = cook_status(state)
    return Nimply(data['shortest_row'], 1)

def pick_even_max(state: Nim) -> Nimply:
    data = cook_status(state)
    row_ = max(data['even_object_rows'], key=lambda x: x[1])
    return Nimply(row_, (state.rows[row_]//2)+1)

def pick_odd_max(state: Nim) -> Nimply:
    data = cook_status(state)
    row_ = max(data['odd_object_rows'], key=lambda x: x[1])
    return Nimply(row_, state.rows[row_]//2)

def opponent_strategy(turn: int):
    if turn % 2 == 0:
        return optimal_strategy
    else:
        return pure_random

def strategy_genome(allele: int):
    return strategies[allele]

strategies = [pure_random,gabriele,shortest_row,longest_row,pick_one_from_max,pick_one_from_min,pick_even_max,pick_odd_max]



def generate_individual(genome: list) -> list:
    dna = list()
    while len(dna) < 4:
        locus = random.randint(0,len(nim.strategies))
        if random.random() < genome[locus]:
            dna.append(locus)
    return dna

def make_strategy(genome: list) -> Callable:
    def evolvable(state: Nim) -> Nimply:
        data = nim.cook_status(state)

        if random.random() < genome['p']:
            ply = Nimply(data['shortest_row'], random.randint(1, state.rows[data['shortest_row']]))
        else:
            ply = Nimply(data['longest_row'], random.randint(1, state.rows[data['longest_row']]))

        return ply
    return evolvable

NUM_MATCHES = 100
NIM_SIZE=10

def evaluate(strategy: Callable) -> float:
    opponent = (strategy, nim.optimal_strategy)
    won = 0

    for m in range(NUM_MATCHES):
        nim = Nim(NIM_SIZE)
        player = 0
        while nim:
            ply = opponent[player](nim)
            nim.nimming(ply)
            player = 1 - player
        if player == 1:
            won += 1
    return won/NUM_MATCHES

def evaluate_with_average(strategy: Callable) -> float:
    won = 0
    for m in range(NUM_MATCHES):
        board = Nim(NIM_SIZE)
        player = 0
        i = 0
        while board:
            opponent = (strategy,nim.opponent_strategy(i))
            ply = opponent[player](board)
            board.nimming(ply)
            player = 1 - player
            i+=1
        if player == 1:
            won += 1
    return won/NUM_MATCHES


if __name__ == "__main__":

    genome = [0.5]*len(nim.strategies)
    for generation in range(100):
        individual = generate_individual(genome)
    evaluate(make_strategy({'p' : .1}))

# # (OLD) Oversimplified match

# logging.getLogger().setLevel(logging.DEBUG)

# #strategy = (pure_random, gabriele)
# strategy = (make_strategy({'p' : .1}), optimal_strategy)

# # 11 is the num of rows
# nim = Nim(11)
# logging.debug(f"status: Initial board  -> {nim}")
# player = 0
# turn = 0
# while nim:
#     ply = strategy[player](nim)
#     nim.nimming(ply)
#     turn = turn+1
#     logging.debug(f"status: After player {player} -> {nim}")
#     player = 1 - player
# winner = 1 - player


# logging.info(f"status: Player {winner} won! (At turn {turn})")