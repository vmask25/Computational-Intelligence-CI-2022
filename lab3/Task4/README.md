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
During the training phase we keep trak of the best agent, based on the evaluation.

Ended the training phase, we evaluate the best agent against the opponent, to test the best player obtained from the algorithm. \
To keep the agent as general as possible, we use _ply_ as the state, it's not really in line with the classical Reinforcement Learning agorithms, but we found better results doing that.

## Results
The trained agent is able to easily defeat various strategies, with good winning rates (100% against the easiest). \
Unfortunately we can not say the same against the optimal strategy, where we can't achieve any significant result.
If you have any suggestions or improvements feel free to open an issue to point your ideas out.

## Contributors

- [Marco Sacchet](https://github.com/saccuz)
- [Fabrizio Sulpizio](https://github.com/Xiusss)

Professor's repository took as reference: https://github.com/squillero/computational-intelligence