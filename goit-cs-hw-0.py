import os
import time
import multiprocessing
from queue import Empty

def search_in_files(files, keyword, result_queue):
    results = []
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line_number, line in enumerate(file, start=1):
                    if keyword in line:
                        results.append((file_path, line_number))
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
    result_queue.put((keyword, results))  # Put both keyword and results into the queue

def process_files(files, keywords):
    result_queue = multiprocessing.Queue()
    processes = []
    for keyword in keywords:
        process = multiprocessing.Process(target=search_in_files, args=(files, keyword, result_queue))
        processes.append(process)
        process.start()

    # Collect results from processes
    results = {}
    for process in processes:
        process.join()

    # Retrieve results from the queue
    while not result_queue.empty():
        keyword, partial_result = result_queue.get()
        if keyword not in results:
            results[keyword] = []
        results[keyword].extend(partial_result)

    return results

if __name__ == "__main__":
    files = ["b.txt"]
    keywords = ["2", "s", "3", "Альберт"]

    start_time = time.time()
    results = process_files(files, keywords)
    end_time = time.time()

    print("Search results:")
    for keyword, occurrences in results.items():
        print(f"Keyword: {keyword}")
        for file_path, line_number in occurrences:
            print(f"   Found '{keyword}' in '{file_path}' at line {line_number}")

    print(f"Time taken: {end_time - start_time} seconds")
