"""This module defines the FileSplitter class, which is used to split poker history files."""
import re
import boto3
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed
from patterns import FILENAME_PATTERN, NEW_HAND_PATTERN, HAND_ID_PATTERN


class S3FileSplitter:
    """
    A class to split poker history files
    """

    def __init__(self, bucket_name: str):
        """
        Initializes the FileSplitter class
        Args:
            bucket_name: The name of the S3 bucket
        """
        self.bucket_name = bucket_name
        self.s3 = boto3.client("s3")
        self.prefix = "data/histories/raw"

    def list_histories_keys(self) -> list:
        """
        Lists all the history files in the bucket and returns a list of their keys

        Returns:
            list: A list of the keys of the history files
        """
        paginator = self.s3.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=self.bucket_name, Prefix=self.prefix)
        keys = [obj["Key"] for page in pages for obj in page.get("Contents", [])]
        return keys

    def get_destination_dir(self, raw_key: str) -> str:
        """
        Returns the directory where the split files will be stored
        Args:
            raw_key (str): The full path of the history file

        Returns:
            destination_dir (str): The directory where the split files will be stored

        """
        destination_dir = raw_key.replace("histories/raw", "histories/split").replace(".txt", "")
        return destination_dir

    def check_split_file_exists(self, raw_key: str) -> bool:
        """
        Checks if the split files already exist
        Args:
            raw_key: The full key of the history file

        Returns:
            split_file_exists (bool): True if the split files already exist, False otherwise
        """
        destination_dir = self.get_destination_dir(raw_key)
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=destination_dir)
        split_file_exists = bool(response.get("Contents"))
        return split_file_exists

    def get_raw_text(self, raw_key: str) -> str:
        """
        Returns the text of a raw history file
        Args:
            raw_key (str): The full path of the history file

        Returns:
            raw_text (str): The raw text of the history file

        """
        response = self.s3.get_object(Bucket=self.bucket_name, Key=raw_key)
        raw_text = response["Body"].read().decode("utf-8")
        return raw_text

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
        print(raw_hands)
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

        raw_text = self.get_raw_text(raw_key)
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
        try:
            split_texts = self.get_split_texts(raw_key)
            id_list = [self.get_hand_id(hand) for hand in split_texts]
            return id_list
        except Exception:
            print(f"Error in get_id_list for {raw_key}")

    def get_separated_hands_info(self, raw_key: str) -> list:
        """
        Returns a list of tuples containing the destination key and the text of each hand
        Args:
            raw_key (str): The path of the history file

        Returns:
            separated_hands_info (list): A list of tuples containing the destination path and the text of each hand
        """
        destination_dir = self.get_destination_dir(raw_key)
        destination_path_list = [f"{destination_dir}/{hand_id}.txt" for hand_id in self.get_id_list(raw_key)]
        split_texts = self.get_split_texts(raw_key)
        separated_hands_info = list(zip(destination_path_list, split_texts))
        return separated_hands_info

    def write_hand_text(self, hand_text: str, destination_path: str):
        self.s3.put_object(Bucket=self.bucket_name, Key=destination_path, Body=hand_text.encode('utf-8'))

    def write_split_files(self, raw_key: str):
        """
        Writes the split files to the destination key of the bucket
        Args:
            raw_key (str): The path of the history file
        """
        destination_dir = self.get_destination_dir(raw_key)
        print(f"Splitting {raw_key} to {destination_dir}")
        for destination_path, hand_text in self.get_separated_hands_info(raw_key):
            if hand_text:
                self.write_hand_text(hand_text=hand_text, destination_path=destination_path)

    def write_new_split_files(self, raw_key: str):
        """
        Writes the split files to the destination key of the bucket if they do not already exist
        Args:
            raw_key:
        """
        if not self.check_split_file_exists(raw_key):
            self.write_split_files(raw_key)

    def split_files(self, check_dir_exists: bool = False, check_file_exists: bool = True):
        """
        Splits all the history files in the raw directory
        Args:
            check_dir_exists (bool): If True, checks if the split files directory already exist before writing
            check_file_exists (bool): If True, checks if the split files already exist before writing

        Examples:
            splitter = S3FileSplitter(bucket_name)
            splitter.split_files(check_dir_exists=False, check_file_exists=True)

        """
        history_keys = self.list_histories_keys()
        with(ThreadPoolExecutor(max_workers=10)) as executor:
            futures = [executor.submit(self.write_split_files, raw_key) for raw_key in history_keys]
            for future in as_completed(futures):
                future.result()



def lambda_handler(event, context):
    print(f"Received event: {event}")
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print(f"Splitting file {key}")
    try:
        splitter = S3FileSplitter(bucket_name)
        splitter.write_split_files(key)
        return {
            'statusCode': 200,
            'body': f'File {key} processed successfully as split hands to {splitter.get_destination_dir(key)}'
        }
    except Exception as e:
        print(f"Error in lambda_handler: {e}")
        return {
            'statusCode': 500,
            'body': f'Error processing file {key}: {e}'
        }


