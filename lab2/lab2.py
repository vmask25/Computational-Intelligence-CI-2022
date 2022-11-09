import random
import logging
import numpy as np
import time

logging.basicConfig(format="%(message)s", level=logging.INFO)

NUM_GENERATIONS = 1000

POPULATION_SIZE = 30        
OFFSPRING_SIZE =  20        # Other possible values (5 and 3, 30 and 20, 70 and 70, 70 and 40, 150 and 100 and others)

# Call Counter annotation for fitness functions
__CALLS__ = dict()

def CallCounter(fn):
    """Annotation @CallCounter"""
    assert fn.__name__ not in __CALLS__, f"Function '{fn.__name__}' already listed in __CALLS__"
    __CALLS__[fn.__name__] = 0
    logging.debug(f"CallCounter: Counting __CALLS__['{fn.__name__}'] ({fn})")

    def call_count(*args, **kwargs):
        __CALLS__[fn.__name__] += 1
        return fn(*args, **kwargs)

    return call_count

# List of lists generator (old function that "bias" the random generator with the seed = 42)
#def problem(N, seed=None):
#    random.seed(seed)
#    return [
#        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
#        for n in range(random.randint(N, N * 5))
#    ]

# New Professor's version of the problem generation (it restores the initial random state (not "biased" by the seed 42))
def problem(N, seed=None):
    state = random.getstate()
    random.seed(seed)
    p = [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]
    random.setstate(state)
    return p

# Counts the number of collisions in the current solution (duplicated covered numbers)
def collisions(sol):
    check_ = np.ones(N)*(N+1) 
    collision = 0
    for el in sol:
        for i in el:
            if check_[i] == i: 
                collision += 1
            else:
                check_[i] = i
    return collision

# Translates the bitmap into the actual list of lists taken in the current solution
def bitmap_to_search_space(genome, space):
    sol = list()
    for i, _ in enumerate(genome):
        if _:
            sol.append(space[i])
    return sol

# Returns the amount of numbers covered by the current solution
def covered_numbers(sol):
    check_set = set()
    for e in sol:
        check_set |= set(e)
    return len(check_set)

# Fitness function
@CallCounter
def fitness(genome, space):
    sol = bitmap_to_search_space(genome, space)
    collisions_ = collisions(sol)
    how_many_covered = covered_numbers(sol)
    return (how_many_covered, -collisions_)

# Simple tournament function (size (tau) =2, with a greater tau it didn't seem to improve solutions)
def tournament(population, tournament_size=2):
    return max(random.choices(population, k=tournament_size), key=lambda i: fitness(i, space))

# The mutation is made by 2 bit tilts, so two lists between the current genome lists are taken/untaken.
# Improving ideas: instead of 2 bit tilts, a proportional (to the problem size (genome length)) number of bit tilts could improve the solution faster.
def mutation(g):
    point1 = random.randint(0, PROBLEM_SIZE - 1)
    # Reversing one of the 1/0 in a random point of the individual/genome
    mutated = g[:point1] + (1 - g[point1],) + g[point1 + 1 :]
    point2 = random.randint(0, PROBLEM_SIZE - 1)
    if point2 == point1:
        if point1 == PROBLEM_SIZE -1:
            point2 -= 1
        elif point1 == 0:
            point2 += 1
        else:
            point2 = point1 - 1
    # Reversing one of the 1/0 in a random point of the individual/genome
    return mutated[:point2] + (1 - mutated[point2],) + mutated[point2 + 1 :]

# The xover is a basic xover in which the result is composed by a slice of each of the two parents.
def cross_over(g1, g2):
    cut = random.randint(0, PROBLEM_SIZE)
    return g1[:cut] + g2[cut:]


########## Main

for N in [5,10,20,22,50,100,500,1000,2000,5000,10000]:
    seed = 42
    
    print (f"------------------------------------------Now trying to solve for N = {N}")

    start = time.time()

    space = list(set(tuple(sorted(set(_))) for _ in problem(N, seed)))

    PROBLEM_SIZE = len(space)
    # fitness_calls = 0 old way to count the fitness calls
    # The initial population is randomly created with bitmaps of 0's and only one "1" randomly choosen
    population = list()
    for genome in [tuple([0 for _ in range(PROBLEM_SIZE)]) for _ in range(POPULATION_SIZE)]:
        # Improving ideas: having a proportional (to the problem size (genome length)) number of initially taken lists could allow a faster optimization
        # for _ in range(int(PROBLEM_SIZE*0.1)):
        point = random.randint(0, PROBLEM_SIZE - 1)
        mutated = genome[:point] + (1,) + genome[point + 1 :]

        population.append(mutated)

    population = sorted(population, key=lambda i: fitness(i,space), reverse=True)
    # fitness_calls += len(population)  old way to count the fitness calls
    mutation_rate = 0.3
    #last_10_fittest = list()
    for g in range(NUM_GENERATIONS):
        offspring = list()
        for i in range(OFFSPRING_SIZE):
            if random.random() < mutation_rate:
                p = tournament(population)
                o = mutation(p)
            else:
                p1 = tournament(population)
                p2 = tournament(population)
                o = cross_over(p1, p2)
            offspring.append(o)
                
        population += offspring
        population = sorted(population, key=lambda i: fitness(i,space), reverse=True)[:POPULATION_SIZE]
        # fitness_calls += len(population)  old way to count the fitness calls
        fittest = fitness(population[0], space)
        if g in [NUM_GENERATIONS//4, NUM_GENERATIONS//2,NUM_GENERATIONS-NUM_GENERATIONS//4, NUM_GENERATIONS-1]:
            print(f"Status: {100 * (g+1) // NUM_GENERATIONS}%\t- Fit: {fittest}")
        # fitness_calls += 1  old way to count the fitness calls

        # This was an attempt to avoid the flatness increasing the mutation rate if the fittest individuals in the last
        # 10 generation didn't evolved anything, but it didn't make such great changes, maybe an improvable idea.
        #last_10_fittest.append(fittest)
        #if len(last_10_fittest) == 10 and not len(set(last_10_fittest)) == 1:
        #    last_10_fittest.pop(0)    
        #if len(last_10_fittest) == 10 and len(set(last_10_fittest)) == 1:
        #    last_10_fittest = list()
        #    if mutation_rate < 0.8:
        #        mutation_rate = mutation_rate + 0.1
        #print(fittest, g+1, mutation_rate)

    ############################################ STATISTICS and RESUME PRINTING
    sol = bitmap_to_search_space(population[0], space)
    collisions_ = collisions(sol)
    how_many_covered = covered_numbers(sol)

    end = time.time()

    #print(f"Best solution up to now ({NUM_GENERATIONS} generations): {sol}")
    print(f"How many covered: {how_many_covered}")
    print(f"Collisions: { collisions_}")
    print(f"Weight: {sum(len(_) for _ in sol)}")
    print(f"Population size: {POPULATION_SIZE}")
    print(f"Offspring size: {OFFSPRING_SIZE}")
    print(f"Generations: {NUM_GENERATIONS}")
    print(f"Fittness calls: {__CALLS__['fitness']}")
    print(f"Computational time: {(end - start)//60} mins and {(end-start)-(((end - start)//60)*60)} secs")
    ############################################