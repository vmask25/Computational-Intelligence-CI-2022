import logging
import random
from copy import copy
import random
import platform
from collections import Counter
from gx_utils import *

def problem(N, seed=None):
    """Creates an instance of the problem"""

    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]

def dijkstra(N, all_lists):
    """Vanilla Dijkstra's algorithm"""

    GOAL = set(range(N))
    all_lists = tuple(set(tuple(_) for _ in all_lists))
    frontier = PriorityQueue()
    nodes = 0

    def state_to_set(state):
        return set(sum((e for e in state), start=()))

    def goal_test(state):
        return state_to_set(state) == GOAL

    def possible_steps(state):
        current = state_to_set(state)
        return [l for l in all_lists if not set(l) <= current]

    def w(state):
        cnt = Counter()
        cnt.update(sum((e for e in state), start=()))
        return sum(cnt[c] - 1 for c in cnt if cnt[c] > 1), -sum(cnt[c] == 1 for c in cnt)

    state = tuple()
    while state is not None and not goal_test(state):
        nodes += 1
        for s in possible_steps(state):
            frontier.push((*state, s), p=w((*state, s)))
        state = frontier.pop()

    logging.debug(f"dijkstra: SOLVED! nodes={nodes:,}; w={sum(len(_) for _ in state):,}; iw={w(state)})")
    return state

logging.getLogger().setLevel(logging.DEBUG)

# it founds the solution 'till 20 (the optimal one) and then it fails to find a solution (for 50, 100, 500, 1000 ...)
for N in [5, 10, 20, 23]:
    solution = dijkstra(N, problem(N, seed=42))
    logging.info(
        f" Solution for N={N:,}: "
        + f"w={sum(len(_) for _ in solution):,} "
        + f"(bloat={(sum(len(_) for _ in solution)-N)/N*100:.0f}%)"
    )