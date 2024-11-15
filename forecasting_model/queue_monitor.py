import time
import logging
import _queue  # Import _queue to catch Empty specifically for managed queues
from multiprocessing import Event

counter = 0

# Set up logging configuration
logging.basicConfig(filename='logs/queue_processing.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def log_enqueue(queue, item):
    # Record the current time and enqueue the item as a tuple (prediction, enqueue_time)
    enqueue_time = time.time()
    queue.put((item, enqueue_time))
    logging.info(f"Enqueued prediction with value {item} at {enqueue_time}")

def log_dequeue(queue, stop_event=None):
    counter = 0
    while not stop_event.is_set():
        try:
            item, enqueue_time = queue.get(timeout=0.5)  # Set a short timeout to allow checking stop_event
            dequeue_time = time.time()
            processing_time = dequeue_time - enqueue_time
            logging.info(f"Dequeued prediction with value {item} after {processing_time:.4f} seconds")
            counter = 0  # Reset the counter if an item is successfully dequeued
            return item
        except _queue.Empty:  # Use _queue.Empty to catch the exception
            if counter == 0:
                logging.warning("Queue is empty - waiting for item.")
            counter += 1
    logging.info("Exiting dequeue due to stop event.")
    return None