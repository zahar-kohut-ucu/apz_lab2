import hazelcast
import multiprocessing
import time

QUEUE_NAME = "bounded-queue"
QUEUE_SIZE = 10  
TOTAL_MESSAGES = 100  

def create_client():
    return hazelcast.HazelcastClient(cluster_name="dev")

def producer():
    client = create_client()
    queue = client.get_queue(QUEUE_NAME).blocking()
    
    for i in range(1, TOTAL_MESSAGES + 1):
        print(f"Producer: Trying to put {i}")
        queue.put(i)  
        print(f"Producer: Put {i} into queue")
    
    print("Producer: Finished")
    client.shutdown()

def consumer(consumer_id):
    client = create_client()
    queue = client.get_queue(QUEUE_NAME).blocking()

    while True:
        item = queue.take()  
        print(f"Consumer {consumer_id}: Took {item}")

    client.shutdown()

if __name__ == "__main__":
    client = create_client()
    client.shutdown()

    producer_process = multiprocessing.Process(target=producer)
    consumer_process1 = multiprocessing.Process(target=consumer, args=(1,))
    consumer_process2 = multiprocessing.Process(target=consumer, args=(2,))

    producer_process.start()
    consumer_process1.start()
    consumer_process2.start()

    producer_process.join()
    consumer_process1.terminate()
    consumer_process2.terminate()
