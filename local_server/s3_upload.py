import logging
from botocore.exceptions import ClientError
import os
import sys
import boto3
import glob
import pandas as pd
from datetime import datetime
import csv


bucket = 'ec-mukahead1'
csvFilePath = '/home/eddy_cov/Downloads/DB/aws/code/transferred_files.csv'
resultFolder = '/home/eddy_cov/Downloads/DB/aws/temp/*.csv'

############# Upload to s3
def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        print(logging.error(e))
        return False
    print(file_name, ' ***** uploaded!')
    todayDate = datetime.today().strftime('%Y-%m-%d')
    if '_biomet_' in file_name:
        print(os.path.exists(file_name))
        if os.path.exists(csvFilePath):
            with open(csvFilePath, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([todayDate, file_name.split('/')[-1]])
        else:
            print('No')
            with open(csvFilePath, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "File_name"])
                writer.writerow([todayDate, file_name.split('/')[-1]])
    os.remove(file_name) 
    return True

            
############# Function sorting files for the linux
def sortFileName (filesName):
    filesName.sort(key=lambda x: os.path.getmtime(x))
    if ((len(filesName) % 2 ) == 0 ):
        temp = filesName[0]
        filesName[0] = filesName[1]
        filesName[1] = temp



filesNameList = glob.glob(resultFolder)

# while the temp folder is not empty 
while True:
    # get the file's name
    filesNameList = glob.glob(resultFolder)
    if (len(filesNameList) == 0):
        sys.exit("Folder is empty!") # stop the code

    # sort files    
    sortFileName(filesNameList)
    # print(filesNameList)
    upload_file(filesNameList[0], bucket)