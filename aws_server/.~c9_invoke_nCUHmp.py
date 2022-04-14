# import libraries
import pandas as pd
import boto3
import sys
import time
import numpy as np

tableName = 'ec_mukaHead'

# Create connection to S3
s3 = boto3.client('s3')
bucketName = 'ec-mukahead1'

# fix dateTime
def fix_date_time(date):
    year = date.split(' ')[0]
    time = date.split(' ')[1]
    temp = []
    if "/"  in year:
        temp = year.split('/')
        if len(str(temp[0])) == 1:
            temp[0] = "0" + temp[0]
        if len(str(temp[1])) == 1:
            temp[1] = "0" + temp[1]
        year = temp[2] + "-" + temp[0] + "-" + temp[1]
        # for time 3:30 -> 03:30
        timeTemp = time.split(':')
        if len(str(timeTemp[0])) == 1:
            timeTemp[0] = "0" + timeTemp[0]
        if len(str(timeTemp[1])) == 1:
            timeTemp[1] = "0" + timeTemp[1]
        time = timeTemp[0] + ":" + timeTemp[1] 
        return year + " " + time
    return date
# check whether eddyCov database exists or not
def check_dynamodb_table_exists():
    dynamoDB = boto3.client('dynamodb')
    
    # show list of all tables in dynamoDB
    table_list = dynamoDB.list_tables()['TableNames']
    if tableName in table_list:
        print('This table already exists!')
    else:
        # create a dynamoDB table 
        table = dynamoDB.create_table(
            TableName=tableName, 
            KeySchema=[
                {
                    'AttributeName': 'station',
                    'KeyType': 'HASH' # Partition key
                },
                {
                    'AttributeName': 'dateTime', 
                    'KeyType': 'RANGE' # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'station',
                    'AttributeType': 'S' # S = String 
                }, 
                {
                    'AttributeName': 'dateTime',
                    'AttributeType': 'S'
                }
            ], BillingMode='PAY_PER_REQUEST'
            )
        print('Table is created!')
        time.sleep(20)
        print(dynamoDB.list_tables()['TableNames'])

# check whether this row stored or not (dateTime)
def check_datetime_stored(columnsName, row, _fileName):
    dynamoDB = boto3.resource('dynamodb') # connect to dynamodb
    table = dynamoDB.Table(tableName) # connect to eddyCov table
    
    # replace the nan values inside an array with -9999 
    row = ['-9999' if x is np.nan else x for x in row]
    # convert all elements of list to int python
    row = [ str(x) for x in row ]
    # fix dateTime and check whether the dateTime exists inside the dataset or not
    dateTimeValue = fix_date_time(row[-1])
    res = table.get_item(Key={'station': 'mukahead', 'dateTime': dateTimeValue}) 
    # fix dict format
    if _fileName == 'biomet':
        temp = dict(zip(columnsName[:-1], row[:-1])) # make a dict from columns name list and row values - except dateTime that is the last item in list
        # params we want to be seperated 
        keys = ['DOY', 'UNNAMED_0_0_1', 'LOGGERTEMP_0_0_1', 'VIN_1_1_1']
        others = {k:temp[k] for k in keys if k in temp} # return sub-set of temp 
        met = {k:temp[k] for k in temp if k not in keys} 
            
        temp = {
            'others': others,
            'met': met
        }
    else:
        # create the dictionary for full output file
        temp={}
        lasHeaderName = None
        for i in range(len(columnsName)-1): # exclude dateTime
            # check whether the first key exist or not
            if columnsName[i][0] in temp.keys():
                temp[lasHeaderName].update({columnsName[i][1] : row[i]})
            else:
                lasHeaderName = columnsName[i][0] 
                temp.update({columnsName[i][0]: {columnsName[i][1] : row[i]}})
    
    if 'Item' in res:
        #print('res -> ', res['Item'])
        #print('temp -> ', temp)
        
        # fix dict order - dateTime needs to be the first key 
        firstDict = {'station':res['Item']['station']} # create a dict for only Dictionary1
        secondDict = {k:v for k,v in res['Item'].items() if k!='station'} # create a dict for the rest
        fixedDictOrder = {**firstDict, **secondDict}
        
        
        
        if _fileName == 'biomet':
            
            fixedDictOrder.update({'biomet': temp})
            # update an item
            table.put_item(Item=
                fixedDictOrder # update biomet values in dict
                )
        else:
            fixedDictOrder.update({'full_output': temp})
            # update an item
            table.put_item(Item=
                fixedDictOrder # update full_output values in dict
                )
        
        print('Data has been updated successfully!')
    
    else:
        if _fileName == 'biomet':
            # add items
            table.put_item(Item={
                'station': 'mukahead',
                'dateTime': dateTimeValue,
                'biomet': temp
            })
        else:
             # insert full_output
             table.put_item(Item={
                'station': 'mukahead',
                'dateTime': dateTimeValue,
                'full_output': temp
            })
        print('Data has been stored successfully!')
    
# check the find name
def check_file(df, fileName):
    print(fileName)
    if '_biomet_' in fileName:
        print('It is a biomet file')
        df.drop(0, inplace=True) # drop first row in biomet file (symbols)
        df.reset_index(drop=True, inplace=True) # reset index
        df["dateTime"] = df["date"] + " " + df["time"] # combine date and time columns
        df.drop(['date', 'time'], axis = 1, inplace=True) # remove columns that we are not going to use
        
        for i in range(len(df)):
            columnsName = list(df)
            row =  df.iloc[i].tolist()
            check_datetime_stored(columnsName, row, 'biomet') # send list of columns name and a row
            
            
        
    elif '_full_output_' in fileName:
        print('It is a full output file')
        df.drop(df.columns[-1], axis=1, inplace=True) # NaN last column! needs to be removed
        columnsNameHeader = list(df)
        df.columns=df. iloc[0]
        df.drop([0,1], inplace=True) # drop first row in biomet file (symbols)
        df.reset_index(drop=True, inplace=True) # reset index
        df["dateTime"] = df["date"] + " " + df["time"] # combine date and time columns
        df.drop(['date', 'time'], axis = 1, inplace=True) # remove columns that we are not going to use
        columnsNameHeader = [e for e in columnsNameHeader if e not in ('Unnamed: 1', 'Unnamed: 2')] #remove date and time columns
        
        # create a single list using 2 rows of header
        columnsName = []
        index = None
        for i in range(len(columnsNameHeader)):
            #print(columnsName)
            if 'Unnamed' not in columnsNameHeader[i]:
                index = i
                columnsName.append([columnsNameHeader[index], list(df)[i]])
            else:
                columnsName.append([columnsNameHeader[index], list(df)[i]])
        columnsName.append('dateTime')
        for i in range(len(df)):
            row =  df.iloc[i].tolist()
            check_datetime_stored(columnsName, row, 'full_output') # send list of columns name and a row
            
    else:
        print('Unexpected file name')

def delete_file(fileName, bucketName):
    try:
        s3.delete_object(Bucket=bucketName, Key=fileName)
        print(f'{fileName} deleted successfully!')
        return True
    except Exception as ex:
        print(str(ex))
        return False


# start
# check dataset exists or not
check_dynamodb_table_exists()
    
# show all files inside the bucket
for bucket_object in s3.list_objects(Bucket=bucketName)['Contents']:
    fileName = bucket_object['Key']
    # sort_files_based_on_time()
    # get file object
    obj = s3.get_object(Bucket=bucketName, Key=fileName) 
    # read file using pandas
    try:
        df = pd.read_csv(obj['Body']) 
    except:
        sns = boto3.client('sns')
        response = sns.publish(
        TopicArn='arn:aws:sns:us-east-1:484024138755:atmosfera_dynamodb',
        Message= fileName + ' is corrupted!',
        Subject= 'Lambda error!'
    )
    check_file(df, fileName)
    delete_file(fileName, bucketName)
