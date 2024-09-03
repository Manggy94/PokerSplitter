import os

from utils import create_zip_archive, make_lambda_function, create_zip_layer, publish_layer, connect_lambda_to_layer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKAGE_NAME = "pkrsplitter"
SOURCE_DIR = os.path.join(BASE_DIR, PACKAGE_NAME)
DIST_DIR = os.path.join(BASE_DIR, "dist")
LAMBDA_HANDLER = f"{PACKAGE_NAME}.lambda.history_splitter.lambda_handler"
FUNCTION_NAME = "history_splitter"
FUNCTION_ROLE = "LambdaS3FilesManager"
RUNTIME = "python3.12"
ARCHIVE_NAME = f"{PACKAGE_NAME}.zip"
ARCHIVE_PATH = os.path.join(DIST_DIR, ARCHIVE_NAME)


def zip_and_upload():
    create_zip_archive(source_dir=SOURCE_DIR, dist_dir=DIST_DIR, archive_name=ARCHIVE_NAME, archive_path=ARCHIVE_PATH,
                       package_name=PACKAGE_NAME)
    create_zip_layer(dist_dir=DIST_DIR)
    publish_layer(package_name=PACKAGE_NAME)
    make_lambda_function(function_name=FUNCTION_NAME, archive_path=ARCHIVE_PATH, runtime=RUNTIME,
                         lambda_handler=LAMBDA_HANDLER, function_role=FUNCTION_ROLE)
    connect_lambda_to_layer(function_name=FUNCTION_NAME, layer_name=f"{PACKAGE_NAME}_layer")


if __name__ == "__main__":
    zip_and_upload()