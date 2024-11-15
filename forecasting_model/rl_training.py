# forecasting_model/rl_training.py
import numpy as np
import signal
from multiprocessing.managers import BaseManager
from forecasting_model.rl_utils import QLearningAgent, SimpleEnv
from multiprocessing import Event
from forecasting_model.logging_config import rl_logger


# Handler for graceful exit
def signal_handler(sig, frame, stop_event):
    if not stop_event.is_set():  # Check if stop_event is already set
        print("Termination signal received. Stopping training...")
        stop_event.set()  # Signal the stop event to end the loop

# forecasting_model/rl_training.py (updated snippet)
def continuous_train_rl_with_forecast(prediction_queue, stop_event, learning_rate=0.1, exploration_rate=1.0, discount_factor=0.99, test=False):
    # Register the signal handler locally within the function
    signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, stop_event))
    signal.signal(signal.SIGTERM, lambda sig, frame: signal_handler(sig, frame, stop_event))

    env = SimpleEnv(prediction_queue)
    agent = QLearningAgent(env.observation_space, env.action_space)

    total_reward = 0
    state = env.reset()
    while not stop_event.is_set():
        action = agent.choose_action(state, exploration_rate)
        next_state, prediction, _, _ = env.step(action, stop_event)
        if test and prediction_queue.empty():
            break
        elif not test and prediction is None:
            break  # Exit if log_dequeue returns None due to stop event
        reward = max(-1, min(1, prediction))  # Scale reward to [-1, 1]

        # RL processing as before
        total_reward += reward
        rl_logger.info(f"Action={action}, Reward={reward}, Cumulative Reward={total_reward}")

        # Q-learning update
        discretized_state = agent.discretize_state(state)
        discretized_next_state = agent.discretize_state(next_state)
        best_next_action = np.argmax(agent.q_table[discretized_next_state])
        td_target = reward + discount_factor * agent.q_table[discretized_next_state][best_next_action]
        td_error = td_target - agent.q_table[discretized_state][action]
        agent.q_table[discretized_state][action] += learning_rate * td_error

        state = next_state
        exploration_rate *= 0.995  # Decay exploration rate

    rl_logger.info(f"Final Total Reward: {total_reward}")
    return total_reward

class QueueManager(BaseManager):
    pass

QueueManager.register('get_queue')

def connect_to_queue():
    manager = QueueManager(address=('localhost', 50000), authkey=b'queuepassword')
    manager.connect()
    return manager.get_queue()

if __name__ == "__main__":
    prediction_queue = connect_to_queue()  # Get the shared queue
    local_stop_event = Event()  # Create a local stop event
    continuous_train_rl_with_forecast(prediction_queue, local_stop_event)
