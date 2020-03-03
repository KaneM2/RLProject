from Game.snakeCore import *
import time

if __name__ == '__main__':
    env = Environment(20, 500, 10, 10)
    finished = False
    action = env.snake.direction

    while not finished:
        time.sleep(0.08)  # Make the game slow down
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