from Gridworld.gridworld import *

#This script contains an implementation of the TD algorithm on the GridWorld environment

# This algorithm is slightly modified to the version in the project
# The main difference is in how the state is chosen at each step


if __name__ == '__main__':
    n_games = 10000
    ALPHA = 0.1
    count = 1

    totalRewards = np.zeros(n_games)
    rDict = {                   #Dictionary containing the Reward squares for the gridworld
        3: 600,
        21: -300,
        33: -50,
        49: -300,
        55: -100
    }

    environment = Gridworld(8, 8, rDict)
    environment.render()

    v = [0 for i in range(len(environment.allStates))]  # Initialise value function to 0
    valueFunctionInstance = []

    for i in range(n_games):

        finished = False
        episodeRewards = 0
        currentObservation = environment.reset()

        if count % 1000 == 0:
            print('Episode ', count)
        num_steps = 0
        while not finished:
            obs = currentObservation
            oldValue = v[obs]
            sampledAction = environment.sampleRandomAction()
            currentObservation, sampledReward, finished, info = environment.step(sampledAction)
            episodeRewards += sampledReward
            v[obs] += ALPHA * (sampledReward + v[currentObservation] - oldValue)

        totalRewards[i] += episodeRewards
        count += 1

        valueFunctionInstance.append(v[24])

    plt.plot(totalRewards)
    plt.title('Episode Rewards for random policy')
    plt.show()

    renderValueFunction(v, 8, 8)

    plt.plot(valueFunctionInstance)
    plt.title('TD estimate of state [0,4]')
    plt.ylabel('v(s)')
    plt.xlabel('Episode')
    plt.show()


