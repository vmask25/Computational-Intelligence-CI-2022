import random
import time
import matplotlib.pyplot as plt
from tqdm import tqdm

import nim
from nim import Nim, Strategy
from agent import Agent

NIM_SIZE = 3
NUM_MATCHES_EVAL = 100
EPISODES = 5000

def evaluate(robot: Agent, player2: Strategy) -> float:
    won = 0
    for m in range(NUM_MATCHES_EVAL):
        board = Nim(NIM_SIZE)
        player = 0
        i = 1#random.randint(0,1)
        while board:
            if i % 2 != 0:
                ply = robot.choose_action(board, board.possible_moves())
                player = 0
            else:
                opponent = player2.move()
                ply = opponent(board)
                player = 1
            board.nimming(ply)
            i+=1
        if player == 0:
            won += 1
    return won/NUM_MATCHES_EVAL

if __name__ == "__main__":
    start = time.time()
    dict_of_states = dict()
    board = Nim(NIM_SIZE)
    player2 = nim.opponent_strategy()
    robot = Agent(board, alpha=0.01, random_factor=0.4)

    # Plot
    moveHistory = []
    indices = []

    for e in tqdm(range(EPISODES), desc="Playing", ascii=False):    
        i = 1#random.randint(0,1)
        # this while loop represents an EPISODE
        while board:
            if i % 2 != 0:
                player = 0
                ply = robot.choose_action(board, board.possible_moves())
                board.nimming(ply)
                reward = board.get_reward()  # get the new reward
                # update the robot memory with state and reward
                robot.update_state_history((board.rows, ply), reward)
                #robot.update_state_history(board.rows, reward)
            else:
                player = 1
                opponent = player2.move()
                ply = opponent(board)
                board.nimming(ply)
            i+=1
        robot.learn()

        #results=evaluate(robot, player2) 
        #if e % 50 == 0:
        #    moveHistory.append(results)
        #    indices.append(e)

        board = Nim(NIM_SIZE)


    #plt.plot(indices, moveHistory, "b")
    #plt.show()

    # Final evaluation
    for c in tqdm(range(500)):
        results=evaluate(robot, player2) 
        if c % 10 == 0:
            moveHistory.append(results)
            indices.append(c)
    plt.plot(indices, moveHistory, "b")
    plt.show()