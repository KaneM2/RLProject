from Game.snakeCore import *
import time

if __name__ == '__main__':
    env = Environment(20, 500, 10, 10,10)
    finished = False
    offGridStarts = 0

    for i in range(1000):
        action = env.reset()
        totalReward = 0
        if env.isOffGrid():
            action = env.reset()

        if env.isOffGrid():
            print(env.snake.blocks)
            offGridStarts += 1
        finished = False
        time.sleep(1)
        while not finished:
            time.sleep(0.08)
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

            state, stepReward, finished, info = env.step(action)
            env.render()

            totalReward += stepReward
        if i % 100 == 0:
            print('Game', i)
    print('Fraction of off grid starts', offGridStarts / 10000)
    pygame.quit()
