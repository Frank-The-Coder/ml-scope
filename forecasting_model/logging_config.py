# logging_config.py
import logging
import os

# Ensure the logs directory exists
os.makedirs('logs', exist_ok=True)

# Configure the base logger for general logs
logging.basicConfig(
    filename='logs/base.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configure the queue processing logger
queue_logger = logging.getLogger('QueueLogger')
queue_handler = logging.FileHandler('logs/queue_processing.log')
queue_handler.setLevel(logging.INFO)
queue_formatter = logging.Formatter('%(asctime)s - %(message)s')
queue_handler.setFormatter(queue_formatter)
queue_logger.addHandler(queue_handler)
queue_logger.propagate = False  # Prevent logs from propagating to the base logger

# Configure the rl training logger
rl_logger = logging.getLogger('RLLogger')
rl_logger.setLevel(logging.INFO)
rl_handler = logging.FileHandler('logs/rl_training.log')
rl_handler.setLevel(logging.INFO)
rl_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
rl_handler.setFormatter(rl_formatter)
rl_logger.addHandler(rl_handler)
