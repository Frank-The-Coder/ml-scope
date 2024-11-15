# experimental_pipeline/pipeline.py
import itertools
from multiprocessing.managers import BaseManager
from multiprocessing import Event
from forecasting_model.rl_training import continuous_train_rl_with_forecast
from experimental_pipeline.resilience_testing import rapid_prediction_generation
from config.logging_config import rl_logger

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

    # Clear the RL-specific log
    with open('logs/rl_training.log', 'w') as rl_log:
        rl_log.write('')

    # Loop over all combinations of hyperparameters
    for lr, er, df in itertools.product(learning_rates, exploration_rates, discount_factors):
        rl_logger.info(f"Testing configuration: learning_rate={lr}, exploration_rate={er}, discount_factor={df}")

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
                discount_factor=df,
                test=True
            )

            # Record the results for this hyperparameter set
            rl_logger.info(f"Configuration: lr={lr}, er={er}, df={df} - Total Reward: {total_reward}")

            results.append((lr, er, df, total_reward))
            # Stop the current training session
            stop_event.set()

        except KeyboardInterrupt as e:
            rl_logger.error(f"Experiment failed with configuration lr={lr}, er={er}, df={df} due to {e}")
            stop_event.set()  # Ensure the current training session exits cleanly
            continue  # Proceed to the next parameter set

    # Log and display best configuration based on total reward
    best_config = max(results, key=lambda x: x[3])  # Find config with the highest total reward
    rl_logger.info(f"Best Configuration: lr={best_config[0]}, er={best_config[1]}, df={best_config[2]} with Reward: {best_config[3]}")

if __name__ == "__main__":
    run_experiments()
