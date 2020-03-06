import random
from collections import deque
import numpy as np
import pygame
from Game.screenCapture import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def samplegrid(w, h, n):
    return [divmod(i, h) for i in random.sample(range(w * h), n)]


class Snake:
    actions = [np.array([-1, 0]), np.array([1, 0]), np.array([0, -1]), np.array([0, 1])]

    def __init__(self, start_position):
        """

        :type start_position: 2x1 numpy Array
        """
        self.startPosition = None
        self.direction = None
        self.length = 1
        self.currentPosition = start_position
        self.blocks = deque([start_position.copy()])
        self.blockAtEndofTail = None

    def isMovingBackwards(self, action):
        if self.direction == 0 and action == 1:
            return True
        elif self.direction == 1 and action == 0:
            return True
        elif self.direction == 2 and action == 3:
            return True
        elif self.direction == 3 and action == 2:
            return True

    def move(self, action):
        if self.isMovingBackwards(action):
            action = self.direction

        else:
            self.direction = action

        self.currentPosition += self.actions[self.direction]
        self.blocks.append(self.currentPosition.copy())
        self.blockAtEndofTail = self.blocks.popleft()

    def eat(self):
        self.blocks.appendleft(self.blockAtEndofTail)  # If current position is an apple eat
        self.length += 1

    def eatingTail(self):
        tail = self.blocks.copy()
        tail.pop()
        if any(((self.currentPosition == elem).all() for elem in tail)):
            return True
        else:
            return False

    def draw(self, screen, blockDim):

        for i, block in enumerate(self.blocks):
            pygame.draw.rect(screen, GREEN, (blockDim * block[0], blockDim * block[1], blockDim, blockDim))


def render():
    pygame.display.update()


class Environment:
    def __init__(self, rows, screenSize, startX, startY, numObstacles):
        self.rows = rows
        self.screenSize = screenSize
        self.numObstacles = numObstacles
        self.obstacles = []
        self.obstacleLocs = None
        self.gameDisplay = pygame.display.set_mode((screenSize, screenSize))
        pygame.display.set_caption('Snake')

        self.blockSize = screenSize / rows
        self.allStates = [np.array([i, j]) for i in range(rows) for j in range(rows)]
        self.stateSet = set([tuple([i, j]) for i in range(rows) for j in range(rows)])
        self.snake = Snake(np.array([startX, startY]))
        self.apple = Apple(np.array([1, 1]))
        self.frames = None

    def draw(self):
        self.gameDisplay.fill(BLACK)
        self.snake.draw(self.gameDisplay, self.blockSize)
        self.apple.draw(self.gameDisplay, self.blockSize)
        for obstacle in self.obstacles:
            obstacle.draw(self.gameDisplay, self.blockSize)

    def getState(self, currentFrame):
        if self.frames == None:
            self.frames = deque([currentFrame] * 2)
        else:
            self.frames.append(currentFrame)
            self.frames.popleft()

        dthreestate=np.concatenate((self.frames[0],self.frames[1]),axis=2)
        state=dthreestate[np.newaxis,:]
        return state

    def step(self, action):
        reward = 0
        self.draw()
        self.snake.move(action)
        display = getDisplay(self.gameDisplay, self.screenSize, self.rows)
        state = self.getState(display)
        if self.isTerminal():
            return state, reward, True, 'Reached terminal state'
        elif self.snake.currentPosition[0] == self.apple.position[0] and self.snake.currentPosition[1] == \
                self.apple.position[1]:
            self.snake.eat()
            self.apple.reset(random.choice(self.getEmptySquares()))
            reward += 1
        return state, reward, False, 'valid step'

    def isOffGrid(self):
        if self.snake.currentPosition[0] * self.blockSize < 0 or self.snake.currentPosition[0] * (
                self.blockSize) > self.screenSize - self.blockSize:
            return True
        if self.snake.currentPosition[1] * self.blockSize < 0 or self.snake.currentPosition[1] * (
                self.blockSize) > self.screenSize - self.blockSize:
            return True
        else:
            return False

    def getEmptySquares(self):

        snakeSquares = set([tuple(item) for item in self.snake.blocks])
        wallSnakeSquares = set(self.obstacleLocs) | snakeSquares
        emptySquares = list(self.stateSet - wallSnakeSquares)
        return emptySquares

    def isTerminal(self):
        if self.snake.eatingTail():
            return True
        if self.isOffGrid():
            return True
        if tuple(self.snake.currentPosition) in self.obstacleLocs:
            return True
        else:
            return False

    def reset(self):
        self.obstacles = []
        self.snake.blocks = deque([])
        self.snake.length = 1
        self.snake.direction = random.randint(0, 2)
        newPosList = samplegrid(self.rows, self.rows, 2 + self.numObstacles)

        self.snake.currentPosition = newPosList[0]
        self.snake.blocks.append(newPosList[0])

        newApplePos = newPosList[1]
        self.apple.reset(newApplePos)
        self.obstacleLocs = newPosList[2:]
        for position in self.obstacleLocs:
            self.obstacles.append(Wall(position))
        self.draw()
        display = getDisplay(self.gameDisplay, self.screenSize, self.rows)
        state = self.getState(display)
        return self.snake.direction,state


class Apple:
    def __init__(self, position):
        self.position = position

    def draw(self, screen, blockDim):
        pygame.draw.rect(screen, RED, (blockDim * self.position[0], blockDim * self.position[1], blockDim, blockDim))

    def reset(self, newPosition):
        self.position = newPosition


class Wall:
    def __init__(self, position):
        self.position = position

    def draw(self, screen, blockDim):
        pygame.draw.rect(screen, BLUE, (blockDim * self.position[0], blockDim * self.position[1], blockDim, blockDim))
