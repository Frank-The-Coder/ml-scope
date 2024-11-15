# experimental_pipeline/resilience_testing.py
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from forecasting_model.forecast_training import generate_prediction
from multiprocessing.managers import BaseManager

# Connect to the queue server
class QueueManager(BaseManager):
    pass

QueueManager.register('get_queue')

def connect_to_queue():
    manager = QueueManager(address=('localhost', 50000), authkey=b'queuepassword')
    manager.connect()
    return manager.get_queue()

def rapid_prediction_generation(n_predictions, delay=0.2):
    prediction_queue = connect_to_queue()
    for _ in range(n_predictions):
        generate_prediction(prediction_queue)
        time.sleep(delay)

if __name__ == "__main__":
    rapid_prediction_generation(10, delay=0.1)  # Example: 10 predictions, 0.1s delay
