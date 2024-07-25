from s3_splitter import S3FileSplitter
from directories import BUCKET_NAME

if __name__ == "__main__":
    splitter = S3FileSplitter(BUCKET_NAME)
    splitter.split_files()
