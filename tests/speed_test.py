"""This module tests the time needed to split a raw history file in local."""
import time
import os

from pkrsplitter.settings import DATA_DIR
from pkrsplitter.splitters.local import LocalFileSplitter

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def test_split_files():

    splitter = LocalFileSplitter(DATA_DIR)
    last_10_files = splitter.list_raw_histories_keys()[-10:]
    medium_file_size = sum([len(splitter.get_split_texts(raw_key)) for raw_key in last_10_files]) / 10
    print(f"Medium file size: {medium_file_size:.1f} hands")
    print(f"Splitting last 10 files 10 times each")
    start = time.time()
    for _ in range(10):
        for file_key in last_10_files:
            splitter.write_split_files(file_key)
    end = time.time()
    total_time = end - start
    average_time = total_time / 100
    print(f"Total time for 100 raw files splittings: {total_time:.2f} seconds")
    print(f"Average time: {average_time:.2f} seconds, or {average_time*1000:.1f} milliseconds per raw file of "
          f"{medium_file_size:.1f} hands, so {average_time*1000/medium_file_size:.1f} milliseconds per hand.")
    print(f"Writing results to {os.path.join(TEST_DIR, 'speed_results.txt')}")
    with open(os.path.join(TEST_DIR, "splitting_speed_results.txt"), "w") as file:
        file.write(f"Total time for 100 raw files splittings: {total_time:.2f} seconds\n")
        file.write(f"Average time: {average_time:.2f} seconds, or {average_time*1000:.1f} milliseconds per raw file of "
                   f"{medium_file_size:.1f} hands, so {average_time*1000/medium_file_size:.1f} milliseconds per hand\n")

if __name__ == "__main__":
    test_split_files()