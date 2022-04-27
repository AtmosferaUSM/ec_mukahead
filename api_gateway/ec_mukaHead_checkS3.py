import json
import boto3

s3 = boto3.client('s3')
bucket = 'ec-mukahead-temp-data'



def lambda_handler(event, context):
    Key = event['params']['querystring']['name'] + '.json'
    results = s3.list_objects(Bucket=bucket , Prefix=Key)
    if 'Contents' in results:
        link = s3.generate_presigned_url('get_object', Params = {'Bucket': bucket, 'Key': Key}, ExpiresIn = 900)
        # TODO implement
        return {
            'statusFile': True,
            'link': link
        }
    
    else: 
        return {
            'statusFile': False
        }
