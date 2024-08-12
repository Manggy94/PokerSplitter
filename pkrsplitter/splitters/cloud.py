"""This module defines the FileSplitter class, which is used to split poker history files."""
import boto3
from .abstract import AbstractFileSplitter


class CloudFileSplitter(AbstractFileSplitter):
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

    def list_raw_histories_keys(self) -> list:
        """
        Lists all the history files in the bucket and returns a list of their keys

        Returns:
            list: A list of the keys of the history files
        """
        paginator = self.s3.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=self.bucket_name, Prefix=self.prefix)
        keys = [obj["Key"] for page in pages for obj in page.get("Contents", [])]
        return keys

    def check_split_dir_exists(self, raw_key: str) -> bool:
        """
        Checks if the split directory for the history file already exists
        Args:
            raw_key: The full key of the history file

        Returns:
            split_dir_exists (bool): True if the split directory already exists, False otherwise
        """
        destination_dir = self.get_destination_dir(raw_key)
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=destination_dir)
        split_dir_exists = bool(response.get("Contents"))
        return split_dir_exists

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

    def write_hand_text(self, hand_text: str, destination_path: str):
        self.s3.put_object(Bucket=self.bucket_name, Key=destination_path, Body=hand_text.encode('utf-8'))

    def write_new_split_files(self, raw_key: str):
        destination_dir = self.get_destination_dir(raw_key)
        print(f"Splitting {raw_key} to {destination_dir}")
        for destination_key, hand_text in self.get_separated_hands_info(raw_key):
            destination_response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=destination_key)
            destination_exists = bool(destination_response.get("Contents"))
            if hand_text and not destination_exists:
                self.write_hand_text(hand_text=hand_text, destination_path=destination_key)
                print(f"Created {destination_key} from {raw_key}")
