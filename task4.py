import hazelcast
import multiprocessing

def create_client():
    return hazelcast.HazelcastClient(cluster_name="dev")

def increment_map():
    print("Start incerement!")
    client = create_client()
    task4_map = client.get_map("task4_map").blocking()
    KEY = "counter"
    ITERATIONS = 10_000

    for _ in range(ITERATIONS):
        value = task4_map.get(KEY)  
        new_value = value + 1        
        task4_map.put(KEY, new_value)
    client.shutdown()

if __name__ == "__main__":
    client = create_client()
    task4_map = client.get_map("task4_map").blocking()
    task4_map.put_if_absent("counter", 0)
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
    task4_map = client.get_map("task4_map").blocking()
    final_value = task4_map.get("counter")
    print(f"Final counter value: {final_value}")
    client.shutdown()
