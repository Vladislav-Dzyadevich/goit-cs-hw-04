import os
import time
import threading

def search_in_files(files, keyword, result_dict):
    results = []
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line_number, line in enumerate(file, start=1):
                    if keyword in line:
                        results.append((file_path, line_number))
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
    result_dict[keyword] = results

def process_files(files, keywords):
    result_dict = {}
    threads = []
    for keyword in keywords:
        thread = threading.Thread(target=search_in_files, args=(files, keyword, result_dict))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    return result_dict

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
