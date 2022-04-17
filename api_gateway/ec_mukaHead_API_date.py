# Give Lambda Function Access to the DynamoDB Table
import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    print(event)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ec_mukaHead')
    
    # First day    
    response = table.query(ScanIndexForward=True ,KeyConditionExpression= Key('station').eq('mukahead'),Limit = 1)
    body = []
    for item in response['Items']:
        body.append({'start': item['dateTime']})
        
    # Last day
    response = table.query(ScanIndexForward=False ,KeyConditionExpression= Key('station').eq('mukahead'),Limit = 1)
    for item in response['Items']:
        body.append({'end': item['dateTime']})
    
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': body
    }
