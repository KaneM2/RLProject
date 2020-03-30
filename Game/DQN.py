import datetime
import os
import tensorflow as tf
from keras.callbacks import TensorBoard
from keras.layers import Dense, Conv2D, Activation, Flatten
from keras.models import Sequential
from keras.optimizers import Adam
from tensorflow.python.client import device_lib
from Game.GridSnake import *

tf.debugging.set_log_device_placement(True)
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
log_dir = "logdir" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
summary_writer = tf.summary.create_file_writer(log_dir)

tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=0)

MODEL_NAME = "DQN Model"
DISCOUNT = 0.99
TARGET_LAG = 2000
MIN_MEM_SIZE = 10000
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
        model.add(Conv2D(32, (3, 3), strides=1, input_shape=self.input_shape, data_format='channels_first'))
        model.add(Activation('relu'))
        model.add(Conv2D(32, (3, 3), data_format='channels_first'))
        model.add(Activation('relu'))
        model.add(Flatten(data_format='channels_first'))
        model.add(Dense(256))
        model.add(Dense(self.num_actions, activation='relu'))
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

    def getQ(self, state):
        return self.DQN.model.predict_on_batch(state)

    def train(self, batch_size):
        if len(self.memory) < MIN_MEM_SIZE:
            return

        minibatch = random.sample(self.memory, batch_size)
        current_states = np.zeros((batch_size, 4, 20, 20))
        for j, transition in enumerate(minibatch):
            current_states[j] = transition[0]

        current_qs_list = self.DQN.model.predict_on_batch(current_states)
        new_current_states = np.zeros((batch_size, 4, 20, 20))
        for j, transition in enumerate(minibatch):
            new_current_states[j] = transition[3]
        future_qs_list = self.DQN.target_model.predict_on_batch(new_current_states)

        Xs = []
        Qs = []

        for index, (current_state, act, reward, new_current_state, done) in enumerate(minibatch):
            if not done:
                max_future_q = np.max(future_qs_list[index])
                new_q = reward + DISCOUNT * max_future_q
            else:
                new_q = reward

            current_qs = current_qs_list[index]
            current_qs[act] = new_q
            Xs.append(current_state)
            Qs.append(current_qs)
        x = np.zeros(((batch_size,) + self.input_shape))
        y = np.zeros((batch_size, self.num_actions))
        for j, state in enumerate(Xs):
            x[j] = Xs[j]
            y[j] = Qs[j]

        self.DQN.model.train_on_batch(x, y)
        self.target_counter += 1

        if self.target_counter > TARGET_LAG:
            self.DQN.target_model.set_weights((self.DQN.model.get_weights()))
            self.target_counter = 0


if __name__ == '__main__':
    print(device_lib.list_local_devices())
    if not os.path.isdir('models'):
        os.makedirs('models')
    n_games = 70000
    epsilon = 1
    step = 1
    env = Environment(20, 500, 10, 10, 0)
    agent = Agent(500000, (4, 20, 20), 4, 0.0001)
    epRewards = []
    count = 0

    for i in range(n_games):
        finished = False
        epReward = 0
        step = 1
        count += 1
        action, currentState = env.reset()
        while not finished:
            if np.random.random() > epsilon:
                action = np.argmax(agent.getQ(currentState))


            else:
                action = np.random.randint(0, agent.num_actions)

            new_state, reward, finished, info = env.step(action)

            epReward += reward

            agent.updateMemory((currentState, action, reward, new_state, finished))
            agent.train(32)
            currentState = new_state
            step += 1
            # render()
        epRewards.append(epReward)
        avg_rewards = sum(epRewards[max(0, i - 100):(i + 1)]) / (len(epRewards[max(0, i - 100):(i + 1)]) + 1)

        with summary_writer.as_default():
            tf.summary.scalar('Episode reward', epReward, step=i)
            tf.summary.scalar('Average reward', avg_rewards, step=i)
            tf.summary.scalar('Epsilon', epsilon, step=i)

        if count % 1000 == 0:
            print('Episode ', count)
            print('Epsilon', epsilon)
            print('Last Reward', epReward)
            model_json = agent.DQN.model.to_json()
            with open("model.json", "w") as json_file:
                json_file.write(model_json)
            # serialize weights to HDF5
            agent.DQN.model.save_weights("model.h5")
            print("Saved model to disk")
            print('epsilon', epsilon)
        if epsilon > 0.01:
            epsilon *= 0.9997
        else:
            epsilon = 0.01
