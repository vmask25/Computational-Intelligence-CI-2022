# Laboratory 3 part 1: Nim

## Task

Write agents able to play Nim, with an arbitrary number of rows and an upper bound  on the number of objects that can be removed in a turn (a.k.a., subtraction game).

The player taking the last object wins.

Task3.1: An agent using fixed rules based on nim-sum (i.e., an expert system)
Task3.2: An agent using evolved rules

The current code is actually the one to solve the Task3.2 because the 3.1 is simply a "static" version of the 3.2 (static meant as not evolving the strategies/rules, but the initial fixed rules were the same 7 we used in the evolutionary one).

## Explanation

The code is structured in two files. \
"nim.py" is the library file in which the Nim class, the cook status and the various rules/strategies are defined. \
"lab3.py" is the file containing the main.
We make the evolution of the strategies/rules in a three turns way. \
In the first turn our genome competes against "pure_random" agent, then, in the second, with "gabriele" agent (because we found out that it works not so bad with respect to random) and in the third turn it competes with the Professor's "optimal_strategy" that uses the nim sum to represent the expert user. *In these way we expect to have a learning slope that is not too steep*. \
Our genome is composed by a *list of probabilities* and each probability represents the probability to use that positional strategy/rule (also an indicator of the goodness/effectiveness of the strategy/rule). The strategies/rules are 7 so in this case the genome is initially a list of 7 elements with 0.5 as values, and during the evolution these values are incremented/decremented to increment/decrement the probability to pick the more winning strategies in the next individuals and to pick the best couple in the end.
For each one of these three turns, 100 generations are made, and for each generation an indivudal is generated picking TWO of the 7 strategies/rules we decided to use.
We make this individual compete against the opponent of the turn (e.g. pure_random in the first 100 generations) and if the results are better than the current champion couple of rules we reassign this individual as champion couple (champion strategy). 
Ended the 100 rounds of this individual competing with the opponent, the genome is evolved, so if the results are good the probabilities of the two selected strategies are incremented, and the others are decremented (the decrmenet step is half the incrment in order not to penalize too much the strategies not selected for this individual). 
At the end of each turn it's printed the champion strategy formed by the couple of rules/strategies (maybe it could be expanded making also the number of picked rules an evolving parameter). \
After these three turns some statistics are provided (mean and victory, we just used those to understand how the algorithm was doing) and the "Evolved genome: " presents the couple of rules/strategies that represent the winning strategy, having the highest evolved probabilities.
This strategy is then competed with the last winning champion and the best strategy between the two is so presented in the end.

## Contributors

- [Marco Sacchet](https://github.com/saccuz)
- [Fabrizio Sulpicio](https://github.com/Xiusss)

## OLD_tries
In the OLD_tries folder are present other old mid-attempts done throughout the process (you can ignore the folder, it's just to keep saves of previous/initial versions). \
Professor's repository took as reference: https://github.com/squillero/computational-intelligence