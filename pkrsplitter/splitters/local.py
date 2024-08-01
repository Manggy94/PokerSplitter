"""This module defines the FileSplitter class, which is used to split poker history files."""
import os
from .abstract import AbstractFileSplitter


class LocalFileSplitter(AbstractFileSplitter):
    """
    A class to split poker history files
    """

    def __init__(self, data_dir: str):
        """

        """
        self.data_dir = data_dir
        self.raw_directory = os.path.join(data_dir, "histories", "raw")

    def list_raw_histories_keys(self) -> list:
        """
        Lists all the history files in the raw directory and returns a list of their root, and file names

        Returns:
            list: A list of dictionaries containing the root and filename of the history files
        """
        histories_list = [os.path.join(root, file)
                          for root, _, files in os.walk(self.raw_directory)
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

    def get_raw_text(self, raw_key: str) -> str:
        """
        Returns the text of a raw history file
        Args:
            raw_key (str): The full path of the history file

        Returns:
            raw_text (str): The raw text of the history file

        """
        with open(raw_key, "r", encoding="latin-1") as file:
            try:
                raw_text = file.read()
            except UnicodeDecodeError:
                #Try to read the file with a different encoding
                # with open(raw_key, "r", encoding="latin-1") as file:
                #     raw_text = file.read()
                #
                # print(raw_text)
                raise UnicodeDecodeError
        return raw_text

    def write_hand_text(self, hand_text: str, destination_key: str):
        destination_dir = os.path.dirname(destination_key)
        os.makedirs(destination_dir, exist_ok=True)
        with open(destination_key, "w", encoding="latin-1") as file:
            file.write(hand_text)

    def write_new_split_files(self, raw_key: str):
        for destination_key, hand_text in self.get_separated_hands_info(raw_key):
            if hand_text and not os.path.exists(destination_key):
                print(f"Creating {destination_key} from {raw_key} ")
                self.write_hand_text(hand_text=hand_text, destination_key=destination_key)
