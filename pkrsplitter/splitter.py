"""This module defines the FileSplitter class, which is used to split poker history files."""
import os
import re
from threading import Thread
from pkrsplitter.patterns import FILENAME_PATTERN, NEW_HAND_PATTERN, HAND_ID_PATTERN


class FileSplitter:
    """
    A class to split poker history files

    Attributes:
        raw_histories_directory (str): The directory containing the raw history files
        split_histories_directory (str): The directory to store the split history files

    Methods:
        list_histories(): Lists all the history files in the raw directory and returns a list of their root, and file names
        get_raw_path(root, filename): Returns the full path of a history file
        get_file_info(raw_path): Extracts the year, month, day, name, and tournament id of a history file
        get_destination_dir(raw_path): Returns the directory where the split files will be stored
        check_split_exists(raw_path): Checks if the split files already exist
        get_raw_text(raw_path): Returns the raw text of a history file
        split_raw_file(raw_text): Splits a history file into separate hands
        get_split_texts(raw_path): Returns a list of the separate hand texts in a history file
        get_hand_id(hand_text): Extracts the hand id from a hand text
        get_id_list(raw_path): Returns a list of the hand ids in a history file
        get_separated_hands_info(raw_path): Returns a list of tuples containing the destination path and the text of each hand
        write_split_files(raw_path, check_exists): Writes the split files to the destination directory
        write_hand_text(hand_text, destination_path): Writes the text of a hand to a file
        split_files(check_exists): Splits all the history files in the raw directory

    Examples:
        >>> splitter = FileSplitter(raw_histories_directory="raw", split_histories_directory="split")
        >>> splitter.split_files()


    """

    def __init__(self, raw_histories_directory: str, split_histories_directory: str):
        """
        Initializes the FileSplitter class
        Args:
            raw_histories_directory (str): The directory containing the raw history files
            split_histories_directory (str): The directory to store the split history files
        """
        self.raw_histories_directory = raw_histories_directory
        self.split_histories_directory = split_histories_directory

    def list_histories(self) -> list:
        """
        Lists all the history files in the raw directory and returns a list of their root, and file names

        Returns:
            list: A list of dictionaries containing the root and filename of the history files
        """
        histories_list = [{"root": root, "filename": file} for root, _, files in os.walk(self.raw_histories_directory)
                          for file in files if file.endswith(".txt")]
        return histories_list

    @staticmethod
    def get_raw_path(root: str, filename: str) -> str:
        """
        Returns the full path of a history file

        Args:
            root (str): The root directory of the history file
            filename (str): The name of the history file

        Returns:
            raw_path (str): The full path of the history file
        """
        raw_path = os.path.join(root, filename)
        return raw_path

    @property
    def raw_paths(self) -> list:
        """
        Returns a list of the full paths of all the history files
        """
        return [self.get_raw_path(history["root"], history["filename"]) for history in self.list_histories()]

    @staticmethod
    def get_file_info(raw_path: str) -> dict:
        """
        Extracts the year, month, day, name, and tournament id of a history file

        Args:
            raw_path (str): The full path of the history file

        Returns:
            file_info (dict): A dictionary containing the year, month, day, name, and tournament id of the history file
        """
        r = re.compile(FILENAME_PATTERN)
        match = r.search(raw_path)
        if match:
            file_info = {
                "year": match.group("year"),
                "month": match.group("month"),
                "day": match.group("day"),
                "name": match.group("tour_name"),
                "id": match.group("tour_id")
            }
            return file_info
        else:
            file_info = {}
            return file_info

    def get_destination_dir(self, raw_path: str) -> str:
        """
        Returns the directory where the split files will be stored
        Args:
            raw_path (str): The full path of the history file

        Returns:
            destination_dir (str): The directory where the split files will be stored

        """
        file_info = self.get_file_info(raw_path)
        if file_info:
            destination_dir = str(os.path.join(
                self.split_histories_directory,
                file_info["year"],
                file_info["month"],
                file_info["day"],
                file_info["id"])
            )
        else:
            destination_dir = ""
        return destination_dir

    def check_split_exists(self, raw_path: str) -> bool:
        """

        Args:
            raw_path (str): The full path of the history file

        Returns:
            split_exists (bool): True if the split files already exist, False otherwise
        """
        destination_dir = self.get_destination_dir(raw_path)
        split_exists = os.path.exists(destination_dir) if destination_dir else False
        return split_exists

    @staticmethod
    def get_raw_text(raw_path: str) -> str:
        """
        Returns the raw text of a history file
        Args:
            raw_path (str): The full path of the history file

        Returns:
            raw_text (str): The raw text of the history file

        """
        with open(raw_path, "r", encoding="utf-8") as file:
            raw_text = file.read()
        return raw_text

    @staticmethod
    def split_raw_file(raw_text: str) -> list:
        """
        Splits a history file into separate hands
        Args:
            raw_text (str): The raw text of the history file

        Returns:
            raw_hands (list): A list of the separate hands in the history file
        """
        raw_hands = re.split(NEW_HAND_PATTERN, raw_text)
        raw_hands.pop(0)
        return raw_hands

    def get_split_texts(self, raw_path: str) -> list:
        """
        Returns a list of the separate hand texts in a history file
        Args:
            raw_path (str): The full path of the history file

        Returns:
            split_texts (list): A list of the separate hand texts in the history file
        """
        file_info = self.get_file_info(raw_path)
        if file_info:
            raw_text = self.get_raw_text(raw_path)
            split_texts = self.split_raw_file(raw_text)
        else:
            split_texts = []
        return split_texts

    @staticmethod
    def get_hand_id(hand_text: str) -> str:
        """
        Extracts the hand id from a hand text
        Args:
            hand_text (str): The text of a hand

        Returns:
            hand_id (str): The id of the hand
        """
        r = re.compile(HAND_ID_PATTERN)
        match = r.search(hand_text)
        if match:
            hand_id = match.group("hand_id")
        else:
            hand_id = ""
        return hand_id

    def get_id_list(self, raw_path: str) -> list:
        """
        Returns a list of the hand ids in a history file
        Args:
            raw_path (str): The full path of the history file

        Returns:
            id_list (list): A list of the hand ids in the history file
        """
        file_info = self.get_file_info(raw_path)
        if file_info:
            raw_text = self.get_raw_text(raw_path)
            split_texts = self.split_raw_file(raw_text)
            id_list = [self.get_hand_id(hand) for hand in split_texts]
        else:
            id_list = []
        return id_list

    def get_separated_hands_info(self, raw_path: str) -> list:
        """
        Returns a list of tuples containing the destination path and the text of each hand
        Args:
            raw_path (str): The full path of the history file

        Returns:
            separated_hands_info (list): A list of tuples containing the destination path and the text of each hand
        """
        destination_dir = self.get_destination_dir(raw_path)
        destination_path_list = (os.path.join(destination_dir, hand_id + ".txt")
                                 for hand_id in self.get_id_list(raw_path))
        split_texts = self.get_split_texts(raw_path)
        separated_hands_info = list(zip(destination_path_list, split_texts))
        return separated_hands_info

    def write_split_files(self, raw_path: str, check_exists: bool = True):
        """
        Writes the split files to the destination directory
        Args:
            raw_path (str): The full path of the history file
            check_exists (bool): If True, checks if the split files already exist before writing
        """
        file_info = self.get_file_info(raw_path)
        split_file_exists = self.check_split_exists(raw_path)
        writing_condition = bool(file_info and not (split_file_exists and check_exists))
        if writing_condition:
            print(f"Splitting {raw_path}")
            for destination_path, hand_text in self.get_separated_hands_info(raw_path):
                self.write_hand_text(hand_text=hand_text, destination_path=destination_path)

    @staticmethod
    def write_hand_text(hand_text: str, destination_path: str):
        """
        Writes the text of a hand to a file
        Args:
            hand_text (str): The text of the hand
            destination_path (str): The full path of the destination file
        """
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        with open(destination_path, "w", encoding="utf-8") as file:
            file.write(hand_text)

    def split_files(self, check_exists: bool = True):
        """
        Splits all the history files in the raw directory
        Args:
            check_exists (bool): If True, checks if the split files already exist before writing

        Examples:
            >>> splitter = FileSplitter(raw_histories_directory="raw", split_histories_directory="split")
            >>> splitter.split_files()

        """
        threads = []
        for raw_path in self.raw_paths:
            thread = Thread(target=self.write_split_files, args=(raw_path, check_exists))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
