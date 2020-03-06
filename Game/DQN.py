import os
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Activation, Flatten
from keras.models import Sequential
from keras.optimizers import Adam
from Game.snakeCore import *
import matplotlib.pyplot as plt
from tensorflow.python.client import device_lib
import tensorflow as tf

tf.debugging.set_log_device_placement(True)

MODEL_NAME = "DQN Model"
DISCOUNT = 1
TARGET_LAG = 5
MIN_MEM_SIZE = 1000
MIN_EPSILON = 0.01


class DQNetwork:
    def __init__(self, input_shape, num_actions, learning_rate):
        # Parameters
        self.input_shape = input_shape
        self.num_actions = num_actions
        self.learning_rate = learning_rate

        # Model
        self.model = self.create_model()

        # Target Model
        self.target_model = self.create_model()
        self.target_model.set_weights(self.model.get_weights())

    def create_model(self):
        model = Sequential()
        model.add(Conv2D(16, (3, 3), strides=1, input_shape=(20, 20, 8)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D((2, 2)))

        model.add(Conv2D(32, (5, 5)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D((2, 2), strides=1))

        model.add(Flatten())
        model.add(Dense(128))
        model.add(Dense(64))
        model.add(Dense(self.num_actions, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(self.learning_rate))
        return model


class Agent:
    def __init__(self, memory_size, input_shape, num_actions, learning_rate):
        self.DQN = DQNetwork(input_shape, num_actions, learning_rate)
        self.memory = deque(maxlen=memory_size)
        self.target_counter = 0
        self.num_actions = num_actions
        self.input_shape = input_shape

    def updateMemory(self, new_transition):
        self.memory.append(new_transition)

    def getQ(self, state, step):
        return self.DQN.model.predict(state)

    def train(self, terminal_state, step, batch_size):
        if len(self.memory) < MIN_MEM_SIZE:
            return

        minibatch = random.sample(self.memory, batch_size)

        current_states = np.concatenate([transition[0] for transition in minibatch])
        current_qs_list = self.DQN.model.predict(current_states, batch_size)

        new_current_states = np.concatenate([transition[3] for transition in minibatch])
        future_qs_list = self.DQN.target_model.predict(new_current_states, batch_size)

        X = []
        Y = []

        for index, (current_state, action, reward, new_current_state, done) in enumerate(minibatch):
            if not done:
                max_future_q = np.max(future_qs_list[index])
                new_q = reward + DISCOUNT * max_future_q
            else:
                new_q = reward

            current_qs = current_qs_list[index]
            current_qs[action] = new_q
            X.append(current_state)
            Y.append(current_qs)

        X = np.vstack(X)
        Y = np.vstack(Y)

        self.DQN.model.fit(X, Y, batch_size=batch_size, verbose=False)

        if terminal_state:
            self.target_counter += 1

        if self.target_counter > TARGET_LAG:
            self.DQN.target_model.set_weights((self.DQN.model.get_weights()))
            self.target_counter = 0


def main():
    print(device_lib.list_local_devices())
    if not os.path.isdir('models'):
        os.makedirs('models')
    n_games = 50000
    epsilon = 1
    step = 1
    env = Environment(20, 500, 10, 10, 10)
    agent = Agent(50000, (20, 20, 8), 4, 0.01)
    epRewards = []
    count = 0
    for _ in range(n_games):
        finished = False
        epReward = 0
        step = 1
        count += 1
        action, currentState = env.reset()
        while not finished:
            if np.random.random() > epsilon:
                action = np.argmax(agent.getQ(currentState, step))

            else:
                action = np.random.randint(0, agent.num_actions)

            new_state, reward, finished, info = env.step(action)

            epReward += reward

            agent.updateMemory((currentState, action, reward, new_state, finished))
            agent.train(finished, step, 32)
            currentState = new_state
            step += 1
            render()
        if count % 100 == 0:
            print('Episode ', count)
            print('Epsilon', epsilon)
            print('Last Reward', epReward)

        epRewards.append(epReward)
        if epsilon > MIN_EPSILON:
            epsilon *= 0.9997
            epsilon = max(MIN_EPSILON, epsilon)
    plt.plot(epRewards)
    plt.show()


main()
