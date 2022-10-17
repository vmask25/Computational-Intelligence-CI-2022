# Laboratory 1 : Set Covering

## Task

Given a number N and some lists of integers $P = (L_0, L_1, L_2, ..., L_n)$, determine, if possible, $S=(L_{s_0}, L_{s_1}, ..., L_{s_n})$ such that each number between 0 and N-1 appears in at least one list
$$\forall n \in [0, N-1] \ \exists i : n \in L_{s_i}$$
and that the total numbers of elements in all $L_{s_i}$ is minimum.

## Explanation

The first used algorithm is the greedy solution given by the Professor.
The second solution uses the combinations inside a loop, generating for each level all the possible combinations (without repetitions).
Once found a solution, it explores the subsequent level in order to be sure not to found another solution, and then it stops, returning the optimal solution.

| N | Processed nodes | Number of Elements (weight) |
|---|---|---|
|5      |325|5|
|10     |1275|10|
|20     |331211|23|
|100    |-|-|
|500    |-|-|
|1000   |-|-|

Given that this is an uninformed strategy, the number of processed nodes can be higher and in fact from N=50 it starts to take too long to find the optimal solution.
There is something that could minimize the number of processed nodes, such as A*.

## Contributors

- [Marco Sacchet](https://github.com/saccuz)
- [Fabrizio Sulpicio](https://github.com/Xiusss)
