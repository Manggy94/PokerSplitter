"""This module defines the directories used by the pkrsplitter package."""
import os
from dotenv import load_dotenv

load_dotenv()

SOURCE_DIR = os.environ.get("SOURCE_DIR")
HISTORY_DIR = os.path.join(SOURCE_DIR, "histories")
RAW_HISTORY_DIR = os.path.join(HISTORY_DIR, "raw")
SPLIT_HISTORY_DIR = os.path.join(HISTORY_DIR, "split")
BUCKET_NAME = os.environ.get("BUCKET_NAME")

if __name__ == "__main__":
    print(f"Source directory: {SOURCE_DIR}")
    print(f"History directory: {HISTORY_DIR}")
    print(f"Raw history directory: {RAW_HISTORY_DIR}")
    print(f"Split history directory: {SPLIT_HISTORY_DIR}")