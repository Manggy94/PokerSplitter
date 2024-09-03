"""This module defines the AbstractFileSplitter class, which is used to split poker history files."""
import re
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from pkrsplitter.patterns.winamax import NEW_HAND_PATTERN, HAND_ID_PATTERN


class AbstractFileSplitter(ABC):
    """
    A class to split poker history files

    Methods:
        list_raw_histories_keys: Lists all the history files in the raw directory and returns a list of their key
        get_destination_dir: Returns the directory where the split files will be stored
        check_split_file_exists: Checks if the split files already exist
        check_split_dir_exists: Checks if the split directory for the history file already exists
        get_raw_text: Returns the text of a raw history file
        split_raw_text: Splits a history file into separate hands
        get_split_texts: Returns a list of the separate hand texts in a history file
        get_hand_id: Extracts the hand id from a hand text
        get_id_list: Returns a list of the hand ids in a history file
        get_separated_hands_info: Returns a list of tuples containing the destination key and the text of each hand
        write_split_files: Writes the split files to the destination key of the bucket
        write_new_split_files: Writes the split files that do not already exist
        write_new_split_histories: Writes the split files for raw files that have never been split
        split_files: Splits all the history files in the raw directory
        split_new_files: Splits all the history files that have not already been split
        split_new_histories: Splits the raw history files for raw files that have never been split
    Examples:
        splitter = LocalFileSplitter(DATA_DIR)
        splitter.split_files()

        splitter = CloudFileSplitter(BUCKET_NAME)
        splitter.split_new_files()

    See Also:
        pkrsplitter.splitters.local.LocalFileSplitter
        pkrsplitter.splitters.s3.S3FileSplitter
    """

    data_dir: str
    raw_dir: str
    correction_raw_keys_file_key: str
    correction_split_keys_file_key: str

    @abstractmethod
    def list_raw_histories_keys(self, directory_key: str = None) -> list:
        """
         Lists all the history files in the raw directory and returns a list of their key
        Returns:
            list: A list of dictionaries containing the root and filename of the history files
        """
        pass

    @staticmethod
    def get_destination_dir(raw_key: str) -> str:
        """
        Returns the directory where the split files will be stored
        Args:
            raw_key (str): The full path of the history file

        Returns:
            destination_dir (str): The directory where the split files will be stored

        """
        destination_dir = raw_key.replace("raw", "split").replace(".txt", "")
        return destination_dir

    @abstractmethod
    def check_split_dir_exists(self, raw_key: str) -> bool:
        """
        Checks if the split directory for the history file already exists
        Args:
            raw_key: The full key of the history file

        Returns:
            split_dir_exists (bool): True if the split directory already exists, False otherwise
        """
        pass

    @abstractmethod
    def get_file_content(self, file_key: str) -> str:
        """
        Returns the text of a file
        Args:
            file_key (str): The file key

        Returns:
            content (str): The content text

        """
        pass

    @abstractmethod
    def write_file(self, file_key: str, content: str) -> None:
        """
        """
        pass

    @abstractmethod
    def write_file_from_list(self, file_key: str, content: list) -> None:
        """
        """
        pass

    @staticmethod
    def split_raw_text(raw_text: str) -> list:
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

    def get_split_texts(self, raw_key: str) -> list:
        """
        Returns a list of the separate hand texts in a history file
        Args:
            raw_key (str): The raw_key of the history file

        Returns:
            split_texts (list): A list of the separate hand texts in the history file
        """

        raw_text = self.get_file_content(raw_key)
        split_texts = self.split_raw_text(raw_text)
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

    def get_id_list(self, raw_key: str) -> list:
        """
        Returns a list of the hand ids in a history file
        Args:
            raw_key (str): The key of the raw history file

        Returns:
            id_list (list): A list of the hand ids in the history file
        """
        split_texts = self.get_split_texts(raw_key)
        id_list = [self.get_hand_id(hand) for hand in split_texts]
        return id_list
        # try:
        #    pass
        # except Exception:
        #     print(f"Error in get_id_list for {raw_key}")

    def get_separated_hands_info(self, raw_key: str) -> list:
        """
        Returns a list of tuples containing the destination key and the text of each hand
        Args:
            raw_key (str): The path of the history file

        Returns:
            separated_hands_info (list): A list of tuples containing the destination path and the text of each hand
        """
        id_list = self.get_id_list(raw_key)
        split_texts = self.get_split_texts(raw_key)
        destination_dir = self.get_destination_dir(raw_key)
        try:
            destination_key_list = [f"{destination_dir}/{hand_id}.txt" for hand_id in id_list]
            separated_hands_info = list(zip(destination_key_list, split_texts))
            return separated_hands_info
        except TypeError:
            print(f"Error in get_separated_hands_info for {raw_key}")
            print(len(id_list))
            print(len(split_texts))
            raise TypeError

    def write_split_files(self, raw_key: str):
        """
        Writes the split files to the split directory
        Args:
            raw_key (str): The path of the history file
        """
        destination_dir = self.get_destination_dir(raw_key)
        print(f"Splitting {raw_key} to {destination_dir}")
        for destination_key, hand_text in self.get_separated_hands_info(raw_key):
            if hand_text:
                self.write_file(file_key=destination_key, content=hand_text)

    @abstractmethod
    def write_new_split_files(self, raw_key: str):
        """
        Writes the split files that do not already exist
        Args:
            raw_key:
        """
        pass

    def write_new_split_histories(self, raw_key: str):
        """
        Writes the split files for raw files that have never been split
        Args:
            raw_key: The key of the raw history file
        """
        if not self.check_split_dir_exists(raw_key):
            self.write_split_files(raw_key)

    def split_files(self):
        """
        Splits all the history files in the raw directory
        """
        print(f"Splitting history files from {self.raw_dir}...\n")
        history_keys = self.list_raw_histories_keys()[::-1]
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.write_split_files, raw_key) for raw_key in history_keys}
            for future in as_completed(futures):
                future.result()

    def split_new_files(self):
        """
        Splits all the history files that have not already been split
        """
        history_keys = self.list_raw_histories_keys()[::-1]
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.write_new_split_files, raw_key) for raw_key in history_keys}
            for future in as_completed(futures):
                future.result()

    def split_new_histories(self):
        """
        Splits the raw history files for raw files that have never been split
        """
        history_keys = self.list_raw_histories_keys()[::-1]
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.write_new_split_histories, raw_key) for raw_key in history_keys}
            for future in as_completed(futures):
                future.result()

    def split_correction_files(self):
        """
        Split the history files to correct.
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
            futures = {executor.submit(self.write_new_split_files, raw_key) for raw_key in raw_keys}
            for future in as_completed(futures):
                future.result()
        self.write_file(self.correction_raw_keys_file_key, "")
        print("Raw history files to correct have been split.")
