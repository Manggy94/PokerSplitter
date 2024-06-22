"""This module defines the main entry point for the pkrsplitter package."""
from pkrsplitter.directories import RAW_HISTORY_DIR, SPLIT_HISTORY_DIR
from pkrsplitter.splitter import FileSplitter

if __name__ == "__main__":
    splitter = FileSplitter(
        raw_histories_directory=RAW_HISTORY_DIR,
        split_histories_directory=SPLIT_HISTORY_DIR
    )
    splitter.split_files(check_dir_exists=False, check_file_exists=True)

