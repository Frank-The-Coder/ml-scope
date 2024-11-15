# logging_config.py
import logging
import os

# Ensure the logs directory exists
os.makedirs('logs', exist_ok=True)


import logging
import os

def setup_logger(log_name, log_file=None, level=logging.INFO, formatter='%(asctime)s - %(levelname)s - %(message)s'):
    """
    Sets up a logger with a specified name and optional log file.
    
    Args:
        log_name (str): Name of the logger (e.g., 'rl_training', 'forecast_training').
        log_file (str): Path to the log file. If None, logs will only output to the console.
        level (int): Logging level. Default is logging.INFO.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(log_name)
    logger.setLevel(level)
    
    # Prevent duplicate handlers in case of multiple setup calls
    if not logger.handlers:
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_formatter = logging.Formatter(formatter)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # File Handler (optional)
        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)  # Ensure directory exists
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_formatter = logging.Formatter(formatter)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

    return logger


# Base Logger
base_logger = setup_logger('BaseLogger', 'logs/base.log')

# Queue Processing Logger
queue_logger = setup_logger('QueueLogger', 'logs/queue_processing.log', formatter='%(asctime)s - %(message)s')

# RL Training Logger
rl_logger = setup_logger('RLLogger', 'logs/rl_training.log')