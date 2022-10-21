import random
from itertools import combinations
import logging

logging.basicConfig(format="%(message)s", level=logging.INFO)

# List of lists generator
def problem(N, seed=None):
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]

nodes = 0

# Professor's greedy search
def greedy_search(space, N):
    goal = set(range(N))
    covered = set()
    solution = list()
    while goal != covered:
        x = set(space.pop(0))
        if not x < covered: 
            solution.append(x)
            covered |= x 
    return solution

# Utility function to check the solution of the Breadth-First search
def check_solution(solution, N):
    if len(solution) == 0:
        return (False, solution)
    check_ = set(range(N)) # create a set with all the number of the requested solution
    sol = set()
    for e in solution:
        sol |= set(e)  # add in the set every number of the possible solution
    if sol == check_: #check if the solution is equal to the request, not a subset nor a overset
        return (True, solution)
    else:
        return (False, solution)

# Pruning, if I already found a valid solution that has N elements I cannot optimize further
def reached(solution, N):
    if not solution[0]:
        return False
    if len(solution[1]) == 0:
        return False
    # Check if the optimal number of elements has been already reached
    if sum(len(l) for l in solution[1]) == N:
        return True
    else:
        return False

# Breadth-First search
def tree_explorer_BF(space, N):
    """ Function that produce the best solution. It can be computationally too massive """
    level = 0
    nodes = []
    exit = 0
    solution = list()
    for i in range(1,N):
        nod = 0
        for e in combinations(space, i): # create every possible combination of element using i elements
            nod += 1
            isCorrect = check_solution(e, N)
            if isCorrect[0]:
                if len(solution) == 0 or sum(len(e) for e in solution[1]) > sum(len(e) for e in isCorrect[1]): # check if the solution found is better than the already existing solution
                    solution = isCorrect
                    level = i
                    if len(solution) != 0 and reached(solution, N):
                        exit = 1
                        break
        nodes.append(nod)
        if exit:
            break
        if level != 0 and level+1 <= i:
            break
    if len(solution) != 0:
        nodes.pop(-1)
        logging.info(f"Visited nodes with BF: {sum(nodes)}")
        return solution
    return (False, [])


seed = 42
    
#for N in [5,10,20,100,500,1000]:
#    space = problem(N,seed)
#    space.sort(key=len)
#    solution = greedy_search(space, N)
#    logging.info(f"Existing solution for {N}: {len(solution)} with (weight) {sum(len(e) for e in solution)} elements\n")

for N in [5, 10, 20, 21, 22, 23, 100, 500, 1000]:
    space = problem(N, seed)
    #print(len(space))
    space.sort(key=len)
    space = set(tuple(sorted(set(_))) for _ in space)
    #print(len(space))
    solution = tree_explorer_BF(space, N)
    logging.info(f"Optimal solution for {N}: {len(solution[1])} lists {solution[1]}  with (weight) {sum(len(e) for e in solution[1])} elements\n")