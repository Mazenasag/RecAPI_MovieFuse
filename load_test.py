import requests
import time
import numpy as np
import concurrent.futures
import psutil
import threading

# URL of your Flask app
URL = "http://127.0.0.1:5000/"  # change if deployed elsewhere

# Example input data (adjust movie titles based on your dataset)
FORM_DATA_LIST = [
    {"title": "Toy Story"},
    {"title": "Jumanji"},
    {"title": "Inception"},
    {"title": "Avengers: Endgame"},
    {"title": "The Dark Knight"},
]

# Number of requests and concurrency
TOTAL_REQUESTS = 100
CONCURRENCY = 10

cpu_readings = []
ram_readings = []

def monitor_system(pid):
    process = psutil.Process(pid)
    while True:
        try:
            cpu = process.cpu_percent(interval=0.5)
            ram = process.memory_percent()
            cpu_readings.append(cpu)
            ram_readings.append(ram)
        except psutil.NoSuchProcess:
            break

def send_request():
    # Pick a random title from the list
    import random
    form_data = random.choice(FORM_DATA_LIST)
    
    start = time.time()
    response = requests.post(URL, data=form_data)
    end = time.time()

    inference_time = None
    if response.status_code == 200:
        try:
            # If your Flask app returns inference_time, extract it
            data = response.json()  # optional if your app returns JSON
            inference_time = data.get("inference_time", None)
        except Exception:
            pass

    return end - start, inference_time, response.status_code

def run_load_test():
    times = []
    inference_times = []
    success = 0

    # Monitor CPU/RAM of Flask process (parent)
    pid = psutil.Process().ppid()
    monitor_thread = threading.Thread(target=monitor_system, args=(pid,), daemon=True)
    monitor_thread.start()

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        futures = [executor.submit(send_request) for _ in range(TOTAL_REQUESTS)]
        for future in concurrent.futures.as_completed(futures):
            t, inf_time, status = future.result()
            times.append(t)
            if inf_time is not None:
                inference_times.append(inf_time)
            if status == 200:
                success += 1

    times = np.array(times)
    avg_time = np.mean(times)
    median_time = np.median(times)
    throughput = TOTAL_REQUESTS / np.sum(times)

    avg_inf = np.mean(inference_times) if inference_times else None
    avg_cpu = np.mean(cpu_readings) if cpu_readings else 0
    avg_ram = np.mean(ram_readings) if ram_readings else 0

    print("\n📊 Load Test Results:")
    print(f"Total Requests: {TOTAL_REQUESTS}")
    print(f"Concurrency: {CONCURRENCY}")
    print(f"Successful Responses: {success}/{TOTAL_REQUESTS}")
    print(f"Avg. Response Time: {avg_time:.4f} s")
    print(f"Median Response Time: {median_time:.4f} s")
    print(f"Throughput: {throughput:.2f} requests/sec")
    if avg_inf:
        print(f"Avg. Inference Time: {avg_inf:.4f} s")
    print(f"Avg. CPU Utilization: {avg_cpu:.2f}%")
    print(f"Avg. RAM Utilization: {avg_ram:.2f}%")

if __name__ == "__main__":
    run_load_test()
