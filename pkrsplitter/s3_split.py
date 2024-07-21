from s3_splitter import S3FileSplitter
from directories import BUCKET_NAME

if __name__ == "__main__":
    splitter = S3FileSplitter(BUCKET_NAME)
    print(f"Splitting files from '{BUCKET_NAME}'")
    # splitter.split_files()
    keys = splitter.list_histories_keys()
    for key in keys:
        print(key, splitter.get_destination_dir(key))
