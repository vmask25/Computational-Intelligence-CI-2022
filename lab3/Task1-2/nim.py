from collections import namedtuple
from copy import deepcopy
from typing import Callable
import random
from itertools import accumulate
from operator import xor

Nimply = namedtuple("Nimply", "row, num_objects")

# Nim class
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

# Strategy class
class Strategy:
    def __init__(self, dna: list) -> None:
        self._dna = dna
        self._step = 0
    
    def move(self) -> Callable:
        next_move = self._dna[self._step]
        self._step += 1
        if self._step >= len(self._dna):
            self._step = 0
        return next_move


# Optimal function 
def nim_sum(state: Nim) -> int:
    #*_, result = accumulate(state.rows, xor)
    #return result
    result = state.rows[0]
    for row in state.rows[1:]:
        result = result ^ row
    return result

# Professor's cook_status to have all the cooked data inside a single dictionary
def cook_status(state: Nim) -> dict:
    cooked = dict()
    cooked['possible_moves'] = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state.k is None or o <= state.k]
    cooked['active_rows_number'] = sum(o > 0 for o in state.rows)
    cooked['even_object_rows'] = [x[0] for x in enumerate(state.rows) if x[1] % 2 == 0 and x[1] != 0]
    cooked['odd_object_rows'] = [x[0] for x in enumerate(state.rows) if x[1] % 2 != 0]
    cooked['shortest_row'] = min((x for x in enumerate(state.rows) if x[1] > 0), key=lambda y:y[1])[0]
    cooked['longest_row'] = max((x for x in enumerate(state.rows)), key=lambda y:y[1])[0]
    cooked['nim_sum'] = nim_sum(state)
    cooked['dumb_strategy'] = [x[0] for x in enumerate(state.rows) if x[1] > 0]

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

# This strategy simply picks only one object from a random row, this performs worse than pure_random
def dumb_strategy(state: Nim) -> Nimply:
    data = cook_status(state)
    row = random.choice(data['dumb_strategy'])
    return Nimply(row, 1)

# This rule picks a random number of objects from the shortest row
def shortest_row(state: Nim) -> Nimply:
    data = cook_status(state)
    return Nimply(data['shortest_row'], random.randint(1, state.rows[data['shortest_row']]))

# This rule picks a random number of objects from the longest row
def longest_row(state: Nim) -> Nimply:
    data = cook_status(state)
    return Nimply(data['longest_row'], random.randint(1, state.rows[data['longest_row']]))

# This rule picks one object from the longest row
def pick_one_from_max(state: Nim) -> Nimply:
    data = cook_status(state)
    return Nimply(data['longest_row'], 1)

# This rule picks one object from the shortest row
def pick_one_from_min(state: Nim) -> Nimply:
    data = cook_status(state)
    return Nimply(data['shortest_row'], 1)

# This rule picks half (+1) the objects from the even objects row that has the maximum number of objects
def pick_even_max(state: Nim) -> Nimply:
    data = cook_status(state)
    info = data['even_object_rows'] if data['even_object_rows'] != [] else data['odd_object_rows']
    row_ = max(info, key=lambda x: x)
    return Nimply(row_, (state.rows[row_]//2)+1)

# This rule picks half the objects from the odd objects row that has the maximum number of objects
def pick_odd_max(state: Nim) -> Nimply:
    data = cook_status(state)
    info = data['odd_object_rows'] if data['odd_object_rows'] != [] else data['even_object_rows']
    row_ = max(info, key=lambda x: x)
    return Nimply(row_, state.rows[row_]//2)

# Opponent strategy generator (based on the evolution turn)
def opponent_strategy(turn: int) -> Strategy:
    if turn == 3:
        return Strategy([optimal_strategy])
    elif turn == 2:
        return Strategy([gabriele])
    elif turn == 1:
        return Strategy([pure_random])
    elif turn == 0: 
        return Strategy([dumb_strategy])

# List of the chosen tactics from which the evolution will choose
tactics = [gabriele,shortest_row,longest_row,pick_one_from_max,pick_one_from_min,pick_even_max,pick_odd_max]