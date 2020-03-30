import time
from Game.DQN import *
from keras.models import model_from_json

def main():
    print('abc')

    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")

    # evaluate loaded model on test data
    loaded_model.compile(loss='mse', optimizer=Adam(0.01))
    env = Environment(20, 500, 10, 10, 0)
    agent = Agent(50000, (4, 20, 20), 4, 0.01)
    agent.DQN.model = loaded_model
    step = 0
    epReward = 0

    for i in range(100):
        finished = False
        action, currentState = env.reset()
        while not finished:
            time.sleep(0.08)
            action = np.argmax(agent.getQ(currentState))
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


            env.draw()
            new_state, reward, finished, info = env.step(action)
            epReward += reward
            currentState = new_state
            step += 1
            render()


main()
