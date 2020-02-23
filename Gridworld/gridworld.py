import typing

import numpy as np
import matplotlib as plt


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
        for squareIndexList in self.rewardDict:
            x = sum(squareIndexList) // self.m
            y = sum(squareIndexList) % self.n
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
                oldState % self.m == self.m - 1 and newState % self.m == 0):  # If agent moves right when at rightmost part of grid
            return True
        else:
            return False

 