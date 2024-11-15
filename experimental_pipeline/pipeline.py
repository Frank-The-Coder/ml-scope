# experimental_pipeline/pipeline.py
import sys
import os
# Add the parent directory to sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
import itertools
from multiprocessing.managers import BaseManager
from multiprocessing import Event
from forecasting_model.rl_training import continuous_train_rl_with_forecast
from forecasting_model.forecast_training import generate_prediction
from experimental_pipeline.resilience_testing import rapid_prediction_generation


# Connect to the queue server
class QueueManager(BaseManager):
    pass

QueueManager.register('get_queue')

def connect_to_queue():
    manager = QueueManager(address=('localhost', 50000), authkey=b'queuepassword')
    manager.connect()
    return manager.get_queue()

def run_experiments():
    # Define hyperparameter ranges
    learning_rates = [0.01, 0.1, 0.5]
    exploration_rates = [1.0, 0.8, 0.5]
    discount_factors = [0.9, 0.95, 0.99]

    # Connect to the queue
    prediction_queue = connect_to_queue()

    # Store results for analysis
    results = []

    # Loop over all combinations of hyperparameters
    for lr, er, df in itertools.product(learning_rates, exploration_rates, discount_factors):
        print(f"\nTesting with learning_rate={lr}, exploration_rate={er}, discount_factor={df}")

        # Create a fresh stop_event for each experiment
        stop_event = Event()

        # Run resilience test to generate rapid predictions
        rapid_prediction_generation(n_predictions=10, delay=0.1)
        try:
            # Run RL training in a separate process to allow resilience testing
            total_reward = continuous_train_rl_with_forecast(
                prediction_queue,
                stop_event,
                learning_rate=lr,
                exploration_rate=er,
                discount_factor=df
            )


            # Record the results for this hyperparameter set
            results.append((lr, er, df, total_reward))
            print(f"Total Reward for (learning_rate={lr}, exploration_rate={er}, discount_factor={df}): {total_reward}")

            # Stop the current training session
            stop_event.set()

        except KeyboardInterrupt:
            print("Experiment interrupted, moving to the next configuration.")
            stop_event.set()  # Ensure the current training session exits cleanly
            continue  # Proceed to the next parameter set

    # Print out all results for comparison
    print("\n--- Experiment Results ---")
    for lr, er, df, total_reward in results:
        print(f"learning_rate={lr}, exploration_rate={er}, discount_factor={df} => Total Reward: {total_reward}")

if __name__ == "__main__":
    run_experiments()
