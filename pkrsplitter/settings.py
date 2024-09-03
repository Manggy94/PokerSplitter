"""This module defines the directories used by the pkrsplitter package."""
import os

# print all environment variables

DATA_DIR = os.environ.get("POKER_DATA_DIR")
HISTORY_DIR = os.path.join(DATA_DIR, "histories")
RAW_HISTORY_DIR = os.path.join(HISTORY_DIR, "raw")
SPLIT_HISTORY_DIR = os.path.join(HISTORY_DIR, "split")
BUCKET_NAME = os.environ.get("POKER_AWS_BUCKET_NAME")

if __name__ == "__main__":
    print(f"Source directory: {DATA_DIR}")
    print(f"History directory: {HISTORY_DIR}")
    print(f"Raw history directory: {RAW_HISTORY_DIR}")
    print(f"Split history directory: {SPLIT_HISTORY_DIR}")