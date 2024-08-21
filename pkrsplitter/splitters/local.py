"""This module defines the FileSplitter class, which is used to split poker history files."""
import os
from .abstract import AbstractFileSplitter
from concurrent.futures import ThreadPoolExecutor, as_completed


class LocalFileSplitter(AbstractFileSplitter):
    """
    A class to split poker history files
    """

    def __init__(self, data_dir: str):
        """

        """
        self.data_dir = data_dir
        self.raw_dir = os.path.join(data_dir, "histories", "raw")
        self.correction_raw_keys_file_key = os.path.join(data_dir, "correction_raw_keys.txt")
        self.correction_split_keys_file_key = os.path.join(data_dir, "correction_split_keys.txt")

    def list_raw_histories_keys(self, directory_key: str = None) -> list:
        """
        Lists all the history files in the raw directory and returns a list of their root, and file names

        Returns:
            list: A list of dictionaries containing the root and filename of the history files
        """
        directory = directory_key or self.raw_dir
        histories_list = [os.path.join(root, file)
                          for root, _, files in os.walk(directory)
                          for file in files if file.endswith(".txt")]
        return histories_list

    def check_split_dir_exists(self, raw_key: str) -> bool:
        """
        Checks if the split directory for the history file already exists
        Args:
            raw_key: The full key of the history file

        Returns:
            split_dir_exists (bool): True if the split directory already exists, False otherwise
        """
        destination_dir = self.get_destination_dir(raw_key)
        return os.path.exists(destination_dir)

    def get_file_content(self, file_key: str) -> str:
        """
        Returns the text of a raw history file
        Args:
            file_key (str): The full path of the history file

        Returns:
            raw_text (str): The raw text of the history file

        """
        with open(file_key, "r", encoding="latin-1") as file:
            try:
                content = file.read()
            except UnicodeDecodeError:
                #Try to read the file with a different encoding
                # with open(raw_key, "r", encoding="latin-1") as file:
                #     raw_text = file.read()
                # print(raw_text)
                raise UnicodeDecodeError
        return content

    def write_file(self, file_key: str, content: str) -> None:
        """
        Writes the content to a file
        Args:
            file_key (str): The file key
            content (str): The content to write
        """
        destination_dir = os.path.dirname(file_key)
        os.makedirs(destination_dir, exist_ok=True)
        with open(file_key, "w", encoding="latin-1") as file:
            file.write(content)

    def write_file_from_list(self, file_key: str, content: list) -> None:
        """
        Writes the content to a file
        Args:
            file_key (str): The file key
            content (list): The content to write
        """
        destination_dir = os.path.dirname(file_key)
        os.makedirs(destination_dir, exist_ok=True)
        with open(file_key, "w", encoding="latin-1") as file:
            for line in content:
                file.write(line + "\n")

    def write_new_split_files(self, raw_key: str):
        for destination_key, hand_text in self.get_separated_hands_info(raw_key):
            if hand_text and not os.path.exists(destination_key):
                print(f"Creating {destination_key} from {raw_key} ")
                self.write_file(content=hand_text, file_key=destination_key)

    def split_correction_files(self):
        """
        Split the history files to correct. It takes the raw keys from the correction_raw_keys.txt file and splits them.
        Returns:

        """
        print("Splitting correction files...\n")
        raw_keys_content = self.get_file_content(self.correction_raw_keys_file_key)
        raw_keys = raw_keys_content.split()
        destination_keys = [hand_info[0]
                            for raw_key in raw_keys
                            for hand_info in self.get_separated_hands_info(raw_key)]
        print(f"There are {len(raw_keys)} raw files to split.\n")
        self.write_file_from_list(self.correction_split_keys_file_key, destination_keys)
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.write_new_split_files, raw_key) for raw_key in raw_keys]
            for future in as_completed(futures):
                future.result()
        self.write_file(self.correction_raw_keys_file_key, "")
        print("Raw history files to correct have been split.")
