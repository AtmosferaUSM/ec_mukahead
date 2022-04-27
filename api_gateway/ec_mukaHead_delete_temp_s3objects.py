import json
import boto3
import datetime

print(datetime.datetime.now())
def lambda_handler(event, context):
    bucket = 'ec-mukahead-temp-data'
    
    # Create connection to S3
    s3 = boto3.client('s3') 
    for my_bucket_object in s3.list_objects(Bucket=bucket)['Contents']:
        # get file name
        file_name = my_bucket_object['Key']
        # object dateTime - LastModified
        d1 = my_bucket_object['LastModified']
        print(f"file name: {file_name}, LastModified: {d1}")
        # current time
        d2 = datetime.datetime.now(datetime.timezone.utc)
        diff = d2 - d1.replace() 
        # if object created more than 10 minutes, delete it
        if (diff > datetime.timedelta(minutes=30)):
            try:
                s3.delete_object(Bucket=bucket, Key=file_name)
                print(f'{file_name} deleted successfully!')
            except Exception as ex:
                print(str(ex))
            
    # TODO implement
    return {
        'statusCode': 200
    }
