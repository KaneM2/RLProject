import typing
import random
import numpy as np


class Gridworld:
    allStates: typing.List[int]

    def __init__(self, m, n, rewardDict):
        self.rewardDict = rewardDict
        self.m = m
        self.n = n
        self.grid = np.zeros((m, n))
        self.agentPosition = 0  # Sets agent  initial position to corner of grid
        self.nonTerminalStates = [i for i in range(self.m * self.n)]
        self.nonTerminalStates.remove(self.m * self.n - 1)  # Remove terminal state from set of non terminal states

        self.allStates = [i for i in range(self.m * self.n)]
        self.actionDict = {'Left': -1, 'Right': 1, 'Up': -self.m, 'Down': self.m}
        self.possibleActions = ['Left', 'Right', 'Up', 'Down']
        self.setRewardSquares(rewardDict)

    def getAgentPosition(self):
        x = self.agentPosition // self.m
        y = self.agentPosition % self.n
        return x, y

    def setRewardSquares(self, rewardDict):
        self.rewardDict = rewardDict
        rewardSquareIndicator = 2
        for square in self.rewardDict:
            x = square // self.m
            y = square % self.n
            self.grid[x][y] = rewardSquareIndicator

    def isTerminal(self, state):
        return state in self.allStates and state not in self.nonTerminalStates

    def resetStateAfterMove(self, newPosition):
        x, y = self.getAgentPosition()
        self.grid[x][y] = 0
        self.agentPosition = newPosition
        x, y = self.getAgentPosition()
        self.grid[x][y] = 1

    def isOffGridMove(self, oldState, newState):
        if newState not in self.allStates:  # If agent moves up or down when already at top or bottom of grid
            return True
        elif (
                oldState % self.m == 0 and newState % self.m == self.m - 1):  # If agent moves left when at leftmost
            # part of grid

            return True
        elif (
                oldState % self.m == self.m - 1 and newState % self.m == 0):  # If agent moves right when at
            # rightmost part of grid
            return True
        else:
            return False

    def step(self, action):
        nextState = self.agentPosition + self.actionDict[action]

        if self.isTerminal(nextState):
            reward = 0
        else:
            reward = -1
        if self.isOffGridMove(self.agentPosition, nextState):
            return self.agentPosition, reward, self.isTerminal(self.agentPosition), 'Off grid move'

        elif nextState in self.rewardDict:
            self.resetStateAfterMove(nextState)
            reward += self.rewardDict[nextState]
            return self.agentPosition, reward, self.isTerminal(self.agentPosition), 'State is now reward square'

        else:
            self.resetStateAfterMove(nextState)
            return self.agentPosition, reward, self.isTerminal(nextState), 'State is now non reward square'

    def reset(self):
        self.agentPosition = 0
        self.grid = np.zeros((self.m, self.n))
        self.setRewardSquares(self.rewardDict)
        return self.agentPosition

    def render(self):
        row_num: int = 0
        col_num = 0
        print('------------Start----------------')
        for row in self.grid:
            for col in row:
                if self.isTerminal(8 * row_num + col_num):
                    print('T', end='\t')
                if row_num == 0 and col_num == 0:
                    print('S', end='\t')
                elif col == 0:
                    print('-', end='\t')
                elif col == 1:
                    print('X', end='\t')
                elif col == 2:
                    print('R', end='\t')
                col_num += 1
            print('\n')
            col_num = 0
            row_num += 1
        print('------------End----------------')


if __name__ == '__main__':
    rDict = {
        3: -3,
        2 * 8 + 6 - 1: -10,
        4 * 8 + 2 - 1: 3,
        6 * 8 + 2 - 1: 1,
        63 - 8: 2
    }

    environment = Gridworld(8, 8, rDict)
    environment.render()
    for count in range(100):
        random_action = random.choice(list(environment.possibleActions))
        environment.step(random_action)
        environment.render()
