import hazelcast

if __name__ == "__main__":

    client = hazelcast.HazelcastClient(cluster_name="dev")
    task3_map = client.get_map("task3_map").blocking()

    for i in range(1000):
        task3_map.set(i, str(i))