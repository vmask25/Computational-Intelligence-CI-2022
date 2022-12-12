# Laboratory 3 part 3: Nim

## Task

Write agents able to play Nim, with an arbitrary number of rows and an upper bound  on the number of objects that can be removed in a turn (a.k.a., subtraction game).

The player taking the last object wins.

- Task 3.4: An agent using Reinforcement Learning.

## Explanation

The code is structured in three files. 
- _nim.py_ is the library file in which the Nim class, the cook status, the various rules/strategies, possible moves and the rewards are defined.
- _lab3.py_ is the file containing the main and the evaluation phase.
- _agent.py_ is the library file in which we define the agent and the learning phase and we calculate the best action.

The training of the agent is performed through a certain number of **episodes**, during which we made the agent compete against an opponent in order to let the agent learn which moves lead to victory and which not. \
After every **episode** we perform an evaluation phase in which we made the agent play against the opponent without learning.
We thought also to save the current best agent if it performs better than its "successors", but in order to be able to train more and more (continuously) in the future we disabled it.

Ended the training phase, we evaluate again the final agent against the opponent, to test it without random_factor but making it act based on what it learned. \
To keep the agent as general as possible and not "seen states" dependent, we use _ply_ as the state, it's not really in line with the classical Reinforcement Learning agorithms, but we found better results doing that instead of using an actual "state" that could be the current board situation. Anyway in the code there are commented lines that allow to easily try to use as state (state.rows) or even (state.rows, ply)).

## Results
The trained agent is able to easily defeat various strategies, with good winning rates (100% against the easiest ones). \
Unfortunately we can not say the same against the optimal strategy, where we can't achieve any significant result, also because our agent is never able to defeat nim sum so it never receives rewards and so it doesn't learn anything. \
We also tried some generalization ideas like training the agent on multiple strategies and then comparing the obtained agent with all the strategies it learned from, and sometimes it gave 100% of win against all and other times 0% and 0.6% in some of the strategies, so we concluded that this approach is really problem specific.
Also regarding the number of rows, our training happens on a fixed number of rows and it performs not very well against a different number of rows.
If you have any suggestions or improvements feel free to open an issue to point your ideas out.

## Contributors

- [Marco Sacchet](https://github.com/saccuz)
- [Fabrizio Sulpizio](https://github.com/Xiusss)

Professor's repository took as reference: https://github.com/squillero/computational-intelligence