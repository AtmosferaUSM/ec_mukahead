import json
import boto3

def bytesto(bytes, to, bsize=1024):
    a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 } 
    r = float(bytes) 
    return bytes / (bsize ** a[to])

def lambda_handler(event, context):
    client = boto3.client('dynamodb')
    # get table info
    response = client.describe_table(TableName='ec_mukaHead')
    TableSizeBytes = response['Table']['TableSizeBytes']
    ItemCount = response['Table']['ItemCount']
    
    TableSize = bytesto(TableSizeBytes, 'm')
    # TODO implement
    return {
      "schemaVersion": 1,
      "label": "DynamoDB info",
      "message": "Database Size: " + str(round(TableSize,2)) +" MB; Item Count: "+ str(ItemCount),
      "color": "informational"
    }
