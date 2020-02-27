from Gridworld.gridworld import *





if __name__ == '__main__':
    n_games = 20000
    ALPHA = 0.01
    count = 1
    epsilon = 0.01

    totalRewards = np.zeros(n_games)
    rDict = {
        3: 600,
        21: -300,
        33: -50,
        49: -300,
        55: -100
    }

    environment = Gridworld(8, 8, rDict)

    Q_est = {}

    for state in environment.allStates:
        for action in environment.possibleActions:
            Q_est[state, action] = 0

    totalSarsaRewards = np.zeros(n_games)

    for i in range(n_games):
        if i % 5000 == 0:
            print('Starting Game ', i)
        obs = environment.reset()
        epRewards = 0
        finished = False

        while not finished:

            action = maxAction(Q_est, obs, environment.possibleActions) if np.random.rand() < 1 - epsilon \
                else environment.sampleRandomAction()

            observation_, reward, finished, info = environment.step(action)

            action_: object = maxAction(Q_est, obs, environment.possibleActions) if np.random.rand() < 1 - epsilon \
                else environment.sampleRandomAction()

            Q_est[obs, action] = Q_est[obs, action] + ALPHA * (
                    reward + Q_est[observation_, action_] - Q_est[obs, action])

            epRewards += reward
            obs = observation_

            if epsilon - 1 / n_games > 0:
                epsilon -= 1 / n_games
            else:
                epsilon = 0

        totalSarsaRewards[i] += epRewards
    plt.plot(totalSarsaRewards)
    plt.title('SARSA Episode Rewards')
    plt.show()
    print('Printing learned policy---------------------------')

    learnedObs = environment.reset()
    finished = False
    while not finished:
        environment.render()
        rand = np.random.rand()
        action = maxAction(Q_est, learnedObs, environment.possibleActions)
        learnedObs_: int
        learnedObs_, reward, finished, info = environment.step(action)
        learnedObs = learnedObs_

    print('Printing Episode Rewards--------------------------')

    renderPolicy(Q_est,8,8,environment.possibleActions)
