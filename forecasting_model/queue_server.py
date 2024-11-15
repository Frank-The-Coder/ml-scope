# forecasting_model/queue_server.py
from multiprocessing.managers import BaseManager
from queue import Queue

# Define a queue server manager
class QueueManager(BaseManager):
    pass

# Register the queue with the manager
shared_queue = Queue(maxsize=100)  # Set max size to 100
QueueManager.register('get_queue', callable=lambda: shared_queue)

def start_queue_server():
    manager = QueueManager(address=('localhost', 50000), authkey=b'queuepassword')
    server = manager.get_server()
    print("Queue server is running...")
    server.serve_forever()

if __name__ == "__main__":
    start_queue_server()
