import hazelcast
import multiprocessing
import time
def create_client():
    return hazelcast.HazelcastClient(cluster_name="dev")

def increment_map():
    print("Start incerement!")
    client = create_client()
    task5_map = client.get_map("task5_map").blocking()
    KEY = "counter"
    ITERATIONS = 10_000
    for _ in range(ITERATIONS):
        task5_map.lock(KEY)
        value = task5_map.get(KEY)  
        new_value = value + 1        
        task5_map.put(KEY, new_value)
        task5_map.unlock(KEY)
    client.shutdown()

if __name__ == "__main__":
    a = time.time()
    client = create_client()
    task5_map = client.get_map("task5_map").blocking()
    task5_map.put_if_absent("counter", 0)
    client.shutdown()

    process1 = multiprocessing.Process(target=increment_map)
    process2 = multiprocessing.Process(target=increment_map)
    process3 = multiprocessing.Process(target=increment_map)

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()

    client = create_client()
    task5_map = client.get_map("task5_map").blocking()
    final_value = task5_map.get("counter")
    b = time.time()
    print(f"Final counter value: {final_value}")
    print(f"Time taken: {b - a}s")
    client.shutdown()
