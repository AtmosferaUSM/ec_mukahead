# to invoke    ->   arn:aws:lambda:us-west-2:825107063935:function:ec_mukaHead_toInvoke
import json
import boto3
import uuid
import time
fileName = str(uuid.uuid1())
bucket = 'ec-mukahead-temp-data'
# Create connection to S3
s3 = boto3.client('s3') 

client = boto3.client('lambda')

def lambda_handler(event, context):
	flag = True
	if 'Contents' in s3.list_objects_v2(Bucket=bucket, Prefix= fileName + '.json'):
		while (flag):
			s3.delete_object(Bucket=bucket, Key=fileName+'.json')
			time.sleep(1)
			if 'Contents' not in s3.list_objects_v2(Bucket=bucket, Prefix= fileName + '.json'):
				flag = False
				
	path = event['context']['resource-path']
	
	# users with AWS Authenticator
	if (path == '/data'):
		print(f'path: {path}')
		# prepare json data for sending to another Lambda
		inputForInvoker = {
			'start': event['params']['querystring']['start'],
			'end': event['params']['querystring']['end'], 
			'category': event['params']['querystring']['category'], 
			'fileName': fileName
		}
		# send params	
		response = client.invoke(
			FunctionName='arn:aws:lambda:us-west-2:825107063935:function:ec_mukaHead_API_data',
			InvocationType='Event', # Event | RequestResponse
			Payload=json.dumps(inputForInvoker)
			)
		# return fileName for searching the file on client side	
		return {'uuid': fileName}
		
	# internal use
	elif (path == '/usm'):
		print(f'path: {path}')
		
		inputForInvoker = {
			'start': event['params']['querystring']['start'],
			'end': event['params']['querystring']['end'],
			'data': event['params']['querystring']['data'],
			'fileName': fileName
		}
		response = client.invoke(
			FunctionName='arn:aws:lambda:us-west-2:825107063935:function:ec_mukaHead_API_usm',
			InvocationType='Event', # Event | RequestResponse
			Payload=json.dumps(inputForInvoker)
			)
		return {'uuid': fileName}
	else:
		return {
        'Success': 'false'
    	}	
    
    
