import numpy as np
from collections import deque
import pygame
import time
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Snake:
    actions = [np.array([-1, 0]), np.array([1, 0]), np.array([0, -1]), np.array([0, 1])]

    def __init__(self, start_position, start_direction_idx):
        """

        :type start_position: 2x1 numpy Array
        """
        self.startPosition = None
        self.alive = True
        self.direction = start_direction_idx
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
            # noinspection PyUnusedLocal
            action = self.direction

        else:
            self.direction = action

        self.currentPosition += self.actions[self.direction]
        self.blocks.append(self.currentPosition.copy())
        self.blockAtEndofTail = self.blocks.popleft()

    def eat(self):
        self.blocks.appendleft(self.blockAtEndofTail)  # If current position is an apple eat

    def die(self):
        pass

    def draw(self, screen, blockDim):

        for i, block in enumerate(self.blocks):
            pygame.draw.rect(screen, GREEN, (blockDim * block[0], blockDim * block[1], blockDim, blockDim))


class Environment:
    def __init__(self, rows, screenSize, startX, startY):
        self.rows = rows
        self.screenSize = screenSize

        pygame.init()
        self.gameDisplay = pygame.display.set_mode((screenSize, screenSize))
        pygame.display.set_caption('Snake')

        self.blockSize = screenSize / rows

        self.stateSet = set([tuple([i, j]) for i in range(rows) for j in range(rows)])
        self.snake = Snake(np.array([startX, startY]), 1)
        self.apple = Apple(np.array([1, 1]))

    def reset(self):
        pass

    def render(self):
        self.gameDisplay.fill(BLACK)
        self.snake.draw(self.gameDisplay, self.blockSize)
        self.apple.draw(self.gameDisplay, self.blockSize)
        pygame.display.update()

    def step(self, action):
        self.snake.move(action)
        if self.snake.currentPosition[0] == self.apple.position[0] and self.snake.currentPosition[1] == \
                self.apple.position[1]:
            self.snake.eat()

            self.apple.reset(random.choice(self.getEmptySquares()))

    def isOffGrid(self):
        if self.snake.currentPosition[0] * self.blockSize < 0 or self.snake.currentPosition[0] * (
                self.blockSize) > self.screenSize - self.blockSize:
            print(self.snake.currentPosition[0] * self.screenSize, self.snake.currentPosition[1] * self.screenSize)
            return True
        if self.snake.currentPosition[1] * self.blockSize < 0 or self.snake.currentPosition[1] * (
                self.blockSize) > self.screenSize - self.blockSize:
            print(self.snake.currentPosition[0] * self.screenSize, self.snake.currentPosition[1] * self.screenSize)
            return True
        else:
            return False

    def getEmptySquares(self):
        snakeSquares = set([tuple(item) for item in self.snake.blocks.copy()])
        emptySquares = list(self.stateSet - snakeSquares)
        return emptySquares


class Apple:
    def __init__(self, position):
        self.size = 20
        self.position = position

    def draw(self, screen, blockDim):
        pygame.draw.rect(screen, RED, (blockDim * self.position[0], blockDim * self.position[1], blockDim, blockDim))

    def reset(self, newPosition):
        self.position = newPosition


class Wall:
    def __init__(self):
        pass


def main():
    env = Environment(5, 500, 2, 2)
    finished = False
    action = env.snake.direction

    while not finished:
        time.sleep(1)  # Make the game slow down
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    action = 1
                if event.key == pygame.K_LEFT:
                    action = 0
                if event.key == pygame.K_UP:
                    action = 2
                if event.key == pygame.K_DOWN:
                    action = 3
        env.step(action)
        if env.isOffGrid():
            pygame.quit()
            quit()

        env.render()


main()
