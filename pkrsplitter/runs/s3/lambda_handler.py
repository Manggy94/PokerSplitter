""" This module defines a lambda handler that splits a single raw history file in an S3 bucket."""

from pkrsplitter.splitters.s3 import S3FileSplitter


def lambda_handler(event, context):
    """
    Splits a single raw history file in an S3 bucket
    Args:
        event:
        context:

    Returns:

    """
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