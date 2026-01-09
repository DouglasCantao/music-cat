import boto3
import urllib.parse
import logging
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def s3_file_handler(event, context):
    """
    Handles S3 events, reads the file, and logs its content.
    """
    logger.info(f"Received event: {event}")

    # Safely extract bucket and key from the event
    bucket = event.get('detail', {}).get('bucket', {})
    bucket_name = bucket.get('name')
    
    obj = event.get('detail', {}).get('object', {})
    file_key = obj.get('key')

    if not bucket_name or not file_key:
        logger.error("Could not retrieve bucket name or file key from the event.")
        return {'statusCode': 400, 'body': 'Missing bucket name or file key in the event.'}

    # The key from the event is URL-encoded
    file_key = urllib.parse.unquote_plus(file_key)

    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        file_content_bytes = response['Body'].read()
        
        try:
            # Decode file content assuming UTF-8
            file_content = file_content_bytes.decode('utf-8')
            logger.info(f"Success! Read file {file_key}. Content starts with: {file_content[:200]}")
            
            return {
                'statusCode': 200,
                'body': file_content
            }
        except UnicodeDecodeError:
            logger.warning(f"File {file_key} is not UTF-8 encoded. Treating as binary.")
            # Handle binary file, for now just log a success message
            logger.info(f"Success! Read binary file {file_key}. Size: {len(file_content_bytes)} bytes.")
            return {
                'statusCode': 200,
                'body': 'Successfully read binary file.'
            }

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code")
        if error_code == 'NoSuchKey':
            logger.error(f"File {file_key} not found in bucket {bucket_name}.")
        else:
            logger.error(f"An unexpected error occurred: {e}")
        raise e
    except Exception as e:
        logger.error(f"An unexpected error occurred when processing {file_key}: {e}")
        raise e