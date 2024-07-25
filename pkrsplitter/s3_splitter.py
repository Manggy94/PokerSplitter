"""This module defines the FileSplitter class, which is used to split poker history files."""
import boto3
from splitter import FileSplitter


class S3FileSplitter(FileSplitter):
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
