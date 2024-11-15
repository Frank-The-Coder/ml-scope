# forecasting_model/rl_utils.py
import numpy as np
import gym
from gym import spaces
from forecasting_model.queue_monitor import log_dequeue

# Define the custom environment
class SimpleEnv(gym.Env):
    def __init__(self, prediction_queue, fade_steps=100):
        super(SimpleEnv, self).__init__()
        self.action_space = spaces.Discrete(4)  # Example action space
        self.observation_space = spaces.Box(low=0, high=1, shape=(8,), dtype=np.float32)
        self.prediction_queue = prediction_queue
        self.fade_steps = fade_steps

    def reset(self):
        return self.observation_space.sample()

    def step(self, action, stop_event):
        next_state = self.observation_space.sample()

        reward = 0
        prediction = log_dequeue(self.prediction_queue, stop_event)  # Read and remove the latest prediction
        # Action-based reward scaling
        if action == 0:
            reward = prediction * 0.2  # Lower weight, example
        elif action == 1:
            reward = prediction * 0.5
        elif action == 2:
            reward = prediction  # Direct reward, unscaled
        else:
            reward = -0.1  # Penalize non-action, example

        return next_state, reward, False, {}  # No "done" condition to make it continuous

class QLearningAgent:
    def __init__(self, observation_space, action_space, bins=10):
        self.action_space = action_space
        self.bins = bins
        self.observation_space = observation_space
        self.q_table = np.zeros((self.bins,) * observation_space.shape[0] + (action_space.n,))

    def discretize_state(self, state):
        discretized = []
        for i in range(len(state)):
            scaling = (state[i] - self.observation_space.low[i]) / (self.observation_space.high[i] - self.observation_space.low[i])
            new_obs = int(round((self.bins - 1) * scaling))
            new_obs = min(self.bins - 1, max(0, new_obs))
            discretized.append(new_obs)
        return tuple(discretized)

    def choose_action(self, state, exploration_rate):
        discretized_state = self.discretize_state(state)
        if np.random.rand() < exploration_rate:
            return np.random.choice(self.action_space.n)
        else:
            return np.argmax(self.q_table[discretized_state])
