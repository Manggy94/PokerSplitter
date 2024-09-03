""" This module defines a lambda handler that splits a single raw history file in an S3 bucket."""
import json
from pkrsplitter.splitters.cloud import CloudFileSplitter


def lambda_handler(event, context):
    """
    Splits raw histories in a S3 bucket
    Args:
        event:
        context:

    Returns:

    """
    print(f"Event: {event} Starting lambda_handler")
    for record in event['Records']:
        body = record['body']
        body_dict = json.loads(body)
        message = body_dict["Message"]
        message_dict = json.loads(message)
        message_record = message_dict["Records"][0]
        bucket_name = message_record['s3']['bucket']['name']
        key = message_record['s3']['object']['key']
        print(f"Splitting file {key}")
        try:
            splitter = CloudFileSplitter(bucket_name)
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
