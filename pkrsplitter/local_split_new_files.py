from local_splitter import LocalFileSplitter
from directories import DATA_DIR

if __name__ == "__main__":
    splitter = LocalFileSplitter(DATA_DIR)
    splitter.split_new_files()
