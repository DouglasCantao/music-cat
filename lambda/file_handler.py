import boto3
import urllib.parse

s3 = boto3.client('s3')

def s3_file_handler(event, context):
    # Log the event for debugging
    print(f"Received event: {event}")

    # Extract bucket and key from the EventBridge 'detail' section
    bucket_name = event['detail']['bucket']['name']
    file_key = urllib.parse.unquote_plus(event['detail']['object']['key'])

    try:
        # Get the object from S3
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        
        # Example: Read the first 100 characters of the file
        file_content = response['Body'].read().decode('utf-8')
        print(f"Success! Read file {file_key}. Content starts with: {file_content[:100]}")
        
        return {
            'statusCode': 200,
            'body': file_content
        }
    except Exception as e:
        print(f"Error getting object {file_key} from bucket {bucket_name}: {e}")
        raise e