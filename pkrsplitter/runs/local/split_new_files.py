"""This script is used to split raw histories with new hands in the local file system."""
from pkrsplitter.splitters.local import LocalFileSplitter
from pkrsplitter.settings import DATA_DIR

if __name__ == "__main__":
    splitter = LocalFileSplitter(DATA_DIR)
    splitter.split_new_files()
