import logging
from botocore.exceptions import ClientError
import os
import sys
import boto3


bucket = 'ec-mukahead-visualization'
resultFolder = '/var/www/html/site/images/visualization/'


# Delete from s3
def delete_from_s3(bucket, file_name):
    try:
        s3.delete_object(Bucket=bucket, Key=file_name)
        print(f'{file_name} deleted successfully!')
        return True
    except Exception as ex:
        print(str(ex))
        return False


# Create connection to S3
s3 = boto3.client('s3') 
try:
    Contents = s3.list_objects(Bucket=bucket)['Contents']
except:
    sys.exit(None)

for my_bucket_object in Contents:
    print(my_bucket_object)
    print(my_bucket_object['Key'])
    # print(my_bucket_object['Key']) <- file name
    s3.download_file(bucket, my_bucket_object['Key'], resultFolder + my_bucket_object['Key'])
    delete_from_s3(bucket, my_bucket_object['Key'])
    print('success')