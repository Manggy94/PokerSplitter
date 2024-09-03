"""This module tests the time needed to split a raw history file in local."""
import pandas as pd
import time
import os

from memory_profiler import profile
from pkrsplitter.settings import DATA_DIR
from pkrsplitter.splitters.local import LocalFileSplitter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
SPEED_RESULTS_PATH = os.path.join(REPORTS_DIR, "splitting_speed_results.txt")
MEMORY_RESULTS_PATH = os.path.join(REPORTS_DIR, "splitting_memory_results.log")
fp = open(MEMORY_RESULTS_PATH, "w+")

splitter = LocalFileSplitter(DATA_DIR)


@profile(stream=fp)
def get_average_time(main_function, files_list):
    last_10_files = files_list[-10:]
    print("Splitting last 10 files 10 times each")
    start = time.time()
    for _ in range(10):
        for file_key in last_10_files:
            main_function(file_key)
    end = time.time()
    total_time = end - start
    average_time = total_time / 100
    total_time_text = f"\nTotal time for 100 files: {total_time:.2f} seconds\n"
    average_time_text = f"Average time: {average_time:.2f} seconds, or {average_time*1000:.1f} milliseconds per file.\n"
    print(total_time_text)
    print(average_time_text)
    return {
        "total_time_text": total_time_text,
        "average_time_text": average_time_text,
        "average_time": average_time,
    }




def get_parameters_df(files_list, average_time):
    nb_files = len(files_list)
    batch_sizes = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
    max_functions = [2, 5, 10, 20, 50, 100, 200, 500, 1000]
    parameters_df = pd.DataFrame(columns=batch_sizes, index=max_functions)
    for batch_size in batch_sizes:
        for nb_functions in max_functions:
            time_per_batch = average_time * batch_size
            files_per_run = batch_size * nb_functions
            nb_rounds = nb_files // files_per_run + 1
            total_time = round(time_per_batch * nb_rounds, 2)
            parameters_df.loc[nb_functions, batch_size] = total_time
    return parameters_df


def get_optimal_parameters(parameters_df):
    min_time = parameters_df.min().min()
    min_idx = parameters_df.stack().idxmin()
    min_nb_functions, min_batch_size = min_idx
    optimal_parameters_text = f"Minimum time: {min_time:.2f} seconds with {min_nb_functions} concurrent functions and "\
                              f"{min_batch_size} batch size\n"
    print(optimal_parameters_text)
    return optimal_parameters_text


def write_results(average_time_text, total_time_text, optimal_parameters_text, parameters_df, results_path):
    print(f"Writing results to {results_path}")
    with open(results_path, "w") as file:
        file.write(total_time_text)
        file.write(average_time_text)
        file.write(optimal_parameters_text)
    parameters_df.to_csv(results_path.replace("txt", "csv"), mode='w')


def test_speed(main_function, files_list, results_path):
    average_time_results = get_average_time(main_function, files_list)
    average_time = average_time_results["average_time"]
    average_time_text = average_time_results["average_time_text"]
    total_time_text = average_time_results["total_time_text"]
    parameters_df = get_parameters_df(files_list, average_time)
    optimal_parameters_text = get_optimal_parameters(parameters_df)
    write_results(average_time_text, total_time_text, optimal_parameters_text, parameters_df, results_path)


if __name__ == "__main__":
    test_speed(splitter.write_split_files, splitter.list_raw_histories_keys(), SPEED_RESULTS_PATH)
