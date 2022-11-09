import logging
import random
from copy import copy
import random
import platform
from collections import Counter
from gx_utils import *

def problem(N, seed=None):
    """Creates an instance of the problem"""

    state = random.getstate()
    random.seed(seed)
    p = [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]
    random.setstate(state)
    return p

# Hill Climbing is an algorithm that is not correct for sure, it's not guaranteed that it finds the optimal solution,
# neither that it finds a solution, but
# it's incredibly better than Greedy (nearer to the optimal solution) and takes a very small time with respect to others (like Dijkstra that 
# after N=20 it stops providing a solution at all)
def hc(N, all_lists):
    """Vanilla Hill Climber"""
    #print(all_lists)
    # doing this (tuple(set(_))) you cut a lot the search space, because we are not interested in duplicates
    # and doing also the SORTED allows to avoid that (1,2) and (2,1) are considered different, so you are cutting further the search space
    # (anyway this is useless when N increases because lists are getting sparser) 
    logging.debug(f"Original: {len(all_lists)}")
    all_lists = set(tuple(sorted(set(_))) for _ in all_lists)
    logging.debug(f"Optimized: {len(all_lists)}")
    # the REPRESENTATION is a set of tuples (because faster/simpler in doing set operations)
    #print(all_lists)

    def evaluate(state):
        cnt = Counter()
        cnt.update(sum((e for e in state), start=()))
        return len(cnt), -cnt.total()

    # working on this to decide how to move in the nieghborhood is up to you and leads to different solutions (maybe)
    # who is close to who is your decision, you decide the size of the neighborhood
    def tweak(solution):
        new_solution = set(solution)
        #randomly removes some random list from the solution
        while new_solution and random.random() < 0.7:
            r = random.choice(list(new_solution))
            new_solution.remove(r)
        #randomly adds some random list to the solution (excluding the ones that already was in the solution ad the beginning)
        while all_lists - solution and random.random() < 0.7:
            a = random.choice(list(all_lists - solution))
            new_solution.add(a)
        return new_solution

    current_solution = set()
    useless_steps = 0
    while useless_steps < 10_000:
        useless_steps += 1
        candidate_solution = tweak(current_solution)
        if evaluate(candidate_solution) > evaluate(current_solution):
            useless_steps = 0
            current_solution = copy(candidate_solution)
            logging.debug(f"New solution: {evaluate(current_solution)}")
    return current_solution
logging.getLogger().setLevel(logging.INFO)


# actually it does not find the optimal solution except for N=5 (maybe could be better tweaking the parameters like the 0.7 or
# maybe using MULTISTART!! Or maybe with some improvements like the SORTING allows to find the optimal solution also for N=10), 
# but we are really close to the optimal solution and we found a solution for big N like 1000.
# So it's a tradeoff between computational effort and quality of the result.
for N in [5, 10, 20, 100, 500, 1000]:
    solution = hc(N, problem(N, seed=42))
    logging.info(
        f" Solution for N={N:,}: "
        + f"w={sum(len(_) for _ in solution):,} "
        + f"(bloat={(sum(len(_) for _ in solution)-N)/N*100:.0f}%)"
    )