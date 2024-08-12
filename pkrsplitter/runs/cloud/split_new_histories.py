""" This script is used to split new raw histories in the S3 datalake. """
from pkrsplitter.splitters.cloud import CloudFileSplitter
from pkrsplitter.settings import BUCKET_NAME

if __name__ == "__main__":
    splitter = CloudFileSplitter(BUCKET_NAME)
    splitter.split_new_histories()
