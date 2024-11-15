# forecasting_model/forecast_training.py
import torch
import torch.nn as nn
import torch.quantization
import numpy as np
from multiprocessing.managers import BaseManager
from forecasting_model.queue_monitor import log_enqueue
from config.logging_config import setup_logger
from config.device_config import device

logger = setup_logger("forecast_training")
logger.info(f"Using device: {device}")

# Sample LSTM Model
class ForecastingLSTM(nn.Module):
    def __init__(self, input_size=1, hidden_size=50, output_size=1):
        super(ForecastingLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])  # Use the last output for prediction
        return out

# Data generation
def generate_sample_data(seq_length=50):
    X = np.random.randn(seq_length, 1).astype(np.float32)
    return torch.tensor([X]).to(device)

def generate_prediction(prediction_queue):
    X = generate_sample_data()
    if device.type == "cuda":
        model = ForecastingLSTM().to(device)
        print(f"Non-quantized model on {device}.")
    else:
        model = ForecastingLSTM()
        model = torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
        print("Quantized model for CPU.")


    # Generate a single prediction
    with torch.no_grad():
        prediction = model(X).item()

    # Enqueue with logging
    if prediction_queue.full():
        prediction_queue.get()  # Remove the oldest prediction if queue is full
    log_enqueue(prediction_queue, prediction)
    print(f"Generated Prediction: {prediction}")

# Connect to the queue server
class QueueManager(BaseManager):
    pass

QueueManager.register('get_queue')

def connect_to_queue():
    manager = QueueManager(address=('localhost', 50000), authkey=b'queuepassword')
    manager.connect()
    return manager.get_queue()

if __name__ == "__main__":
    prediction_queue = connect_to_queue()  # Get the shared queue
    generate_prediction(prediction_queue)
