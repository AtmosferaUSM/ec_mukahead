import os
from shutil import copy2
import glob
import sys
import pandas as pd

tempFolder = '/home/eddy_cov/Downloads/DB/aws/temp'
transferredCSV = '/home/eddy_cov/Downloads/DB/aws/code/transferred_files.csv'
resultFolder = '/home/eddy_cov/Downloads/ec_data/results/*csv'

# Reading the date of previous stored files 
try:
    data = pd.read_csv(transferredCSV)
    lastFileName = data.iloc[-1][1]
    print("last file name: ", lastFileName)

except:
    print("transferred_files.csv does not exist! Go to aws folder/fixed_files/2015 then copy the files and paste them in temp folder. Then run the transfer_to_s3 python file.")
    sys.exit(None)


# Reading the list of all files in the results folder and store them in a list
filesName = list(filter(os.path.isfile, glob.glob(resultFolder)))
filesName.sort(key=lambda x: os.path.getmtime(x))

# Find biomet and full_output files name and store them 
Biomet = []
full_output= []
for i in range(len(filesName)):
    if "eddypro_muka_head01_biomet" in filesName[i]:
        Biomet.append(filesName[i])
    elif "eddypro_muka_head01_full_output" in filesName[i]:
        full_output.append(filesName[i])


# check the csv file 
for i in range(len(Biomet)):
     if lastFileName in Biomet[i]:
        Biomet = Biomet[i+1:]
        full_output = full_output[i+1:]         
        break

# Copy new files in folder to be added to DB later    
for i in range(len(Biomet)):
    copy2(Biomet[i],tempFolder)
    copy2(full_output[i],tempFolder)
    print(Biomet[i], '  &  ', full_output[i]," ***  Copied!")
