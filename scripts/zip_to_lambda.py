import os

from scripts.utils import create_zip_archive, make_lambda_function

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(BASE_DIR, "pkrsplitter")
DIST_DIR = os.path.join(BASE_DIR, "dist")
LAMBDA_HANDLER = "lambda.history_splitter.lambda_handler"
FUNCTION_NAME = "history_splitter"
FUNCTION_ROLE = "LambdaS3FilesManager"
RUNTIME = "python3.12"
ARCHIVE_NAME = f"{FUNCTION_NAME}.zip"
ARCHIVE_PATH = os.path.join(DIST_DIR, ARCHIVE_NAME)


def zip_and_upload():
    create_zip_archive(source_dir=SOURCE_DIR, dist_dir=DIST_DIR, archive_name=ARCHIVE_NAME, archive_path=ARCHIVE_PATH)
    make_lambda_function(function_name=FUNCTION_NAME, archive_path=ARCHIVE_PATH, runtime=RUNTIME,
                         lambda_handler=LAMBDA_HANDLER, function_role=FUNCTION_ROLE)


if __name__ == "__main__":
    zip_and_upload()