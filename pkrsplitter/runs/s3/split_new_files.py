""" This script is used to split raw histories with new hands in the S3 datalake. """
from pkrsplitter.splitters.s3 import S3FileSplitter
from pkrsplitter.settings import BUCKET_NAME

if __name__ == "__main__":
    splitter = S3FileSplitter(BUCKET_NAME)
    splitter.split_new_files()
