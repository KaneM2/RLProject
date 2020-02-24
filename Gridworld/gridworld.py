import typing
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


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
        self.rewardSquareIndicator = 2
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
        for square in self.rewardDict:
            x = square // self.m
            y = square % self.n
            self.grid[x][y] = self.rewardSquareIndicator

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
        x, y = nextState // self.m, nextState % self.n
        if self.isTerminal(nextState):
            reward = 0
        else:
            reward = -1
        if self.isOffGridMove(self.agentPosition, nextState):
            return self.agentPosition, reward, self.isTerminal(self.agentPosition), 'Off grid move'

        elif self.grid[x][y] == self.rewardSquareIndicator:
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

    def sampleRandomAction(self):
        return random.choice(list(self.possibleActions))


def renderValueFunction(states, m, n):
    npList = np.asarray(states)
    valueGrid = np.reshape(npList, (m, n))
    print('-----------------------------------')
    for row in valueGrid:
        for col in row:
            print(col, end='\t')
        print('\n')
    print('-----------------------------------')
    ax=sns.heatmap(valueGrid, annot=True, fmt='7.0f')
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    plt.gca().invert_yaxis()
    plt.show()


if __name__ == '__main__':

    ALPHA = 0.05
    n_games = 75000

    rDict = {
        3: 600,
        21: -300,
        33: -50,
        49: -300,
        55: 50
    }

    environment = Gridworld(8, 8, rDict)
    environment.render()

    totalRewards = np.zeros(n_games)

    v = [0 for i in range(len(environment.allStates))]  # Initialise value function to 0

    for i in range(n_games):
        finished = False

        episodeRewards = 0
        currentObservation = environment.reset()

        while not finished:
            obs = currentObservation
            oldValue = v[currentObservation]
            sampledAction = environment.sampleRandomAction()

            currentObservation, sampledReward, finished, info = environment.step(sampledAction)
            episodeRewards += sampledReward
            v[obs] += ALPHA * (sampledReward + v[currentObservation] - oldValue)

        totalRewards[i] += episodeRewards

    plt.plot(totalRewards)
    plt.show()
    renderValueFunction(v, 8, 8)
