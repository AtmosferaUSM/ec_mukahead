import json
import plotly.express as px
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot  # download_plotlyjs, init_notebook_mode, , iplot
import plotly.express as px
import numpy as np
  

    
def degToCompass(num):
    try:
        val=int((num/22.5)+.5)
        arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
        return arr[(val % 16)]
    except:
        return None


def kelvinToCelsius(temp):
    try:
        return round((temp - 273.15),2)
    except:
        pass
    
    
def lambda_handler(event, context):
    bucket = 'ec-mukahead-visualization'

    # create a connection to S3
    s3 = boto3.client('s3')  
    
    # create a connection to DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ec_mukaHead')
    
    # find Last item and 
    response = table.query(ScanIndexForward=False ,KeyConditionExpression= Key('station').eq('mukahead'),Limit = 1)
    # get last item dateTime
    last_date = None;
    for item in response['Items']:
        last_date = item['dateTime']
    
    # convert string to dateTime | "2022-04-20 22:30" need to be matched-> '%Y-%m-%d %H:%M'
    end = datetime.strptime(last_date, '%Y-%m-%d %H:%M')
    
    # calculating past date
    start = end - timedelta(days = 365)
    print(f'last: {end}, start: {start}')
    
    # get data from start to end date
    response = table.query(KeyConditionExpression= Key('station').eq('mukahead') & Key('dateTime').between(str(start), str(end)))
    
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])   
    
    # get all data that is required and remove -9999 values 
    dateTime, TA_1_1_1, TS_1_1_1, PPFD_1_1_1, RG_1_1_1, RN_1_1_1, P_RAIN_1_1_1, RH_1_1_1, co2_flux, LE, H, wind_speed, wind_dir = [], [], [], [], [], [], [], [], [], [], [], [], []
    for item in data:
        #####  dateTime
        dateTime.append(item['dateTime'])
        
        ##### Atmospheric Temperature
        if 'TA_1_1_1' in item['biomet']['met'].keys():
            # change data type from string to float and remove some data points
            temp = float(item['biomet']['met']['TA_1_1_1']) 
            if (temp > 310)|(temp < 295) :
                temp = None
                
            # Kelvin to Celsius 
            temp = kelvinToCelsius(temp)
            TA_1_1_1.append(temp)
            
        ##### water temperature 
        if 'TS_1_1_1' in item['biomet']['met'].keys():
            # change data type from string to float and remove some data points
            temp = float(item['biomet']['met']['TS_1_1_1'])
            if (temp > 310)|(temp < 290) :
                temp = None
            
            # Kelvin to Celsius 
            temp = kelvinToCelsius(temp)
            TS_1_1_1.append(temp)
            
        ##### Photosynthetic Active Radiation (PAR)
        if 'PPFD_1_1_1' in item['biomet']['met'].keys():
            # change data type from string to float and remove some data points
            temp = float(item['biomet']['met']['PPFD_1_1_1'])
            if (temp > 2500)|(temp < 0) :
                temp = None
                
            PPFD_1_1_1.append(temp)
        
        
        ##### Global and Net Radiation
        if 'RG_1_1_1' in item['biomet']['met'].keys():
            # change data type from string to float and remove some data points
            temp = float(item['biomet']['met']['RG_1_1_1'])
            if (temp > 1100)|(temp < -100) :
                temp = None
                
            RG_1_1_1.append(temp)
            
        if 'RN_1_1_1' in item['biomet']['met'].keys():
            # change data type from string to float and remove some data points
            temp = float(item['biomet']['met']['RN_1_1_1'])
            if (temp > 1100)|(temp < -100) :
                temp = None
                
            RN_1_1_1.append(temp)
        
        ##### Precipitation 
        if 'P_RAIN_1_1_1' in item['biomet']['met'].keys():
            # change data type from string to float and remove some data points
            temp = float(item['biomet']['met']['P_RAIN_1_1_1']) * 1000 
            if (temp > 0.08 * 1000)|(temp < 0) :
                temp = None
                
            P_RAIN_1_1_1.append(temp)
        
        ##### Relative Humidity
        if 'RH_1_1_1' in item['biomet']['met'].keys():
            # change data type from string to float and remove some data points
            temp = float(item['biomet']['met']['RH_1_1_1'])
            if (temp > 100)|(temp < 40) :
                temp = None
                
            RH_1_1_1.append(temp)
        
        ##### Carbon Dioxide
        
        if 'co2_flux' in item['full_output']['corrected_fluxes_and_quality_flags'].keys():
            # change data type from string to float and remove some data points
            temp = float(item['full_output']['corrected_fluxes_and_quality_flags']['co2_flux'])
            if (temp > 5)|(temp < -5) :
                temp = None
                
            co2_flux.append(temp)
            
        ##### Latent Heat
        if 'LE' in item['full_output']['corrected_fluxes_and_quality_flags'].keys():
            # change data type from string to float and remove some data points
            temp = float(item['full_output']['corrected_fluxes_and_quality_flags']['LE'])
            if (temp > 300)|(temp < -50) :
                temp = None
                
            LE.append(temp)
    
        ##### Sensible Heat
        if 'H' in item['full_output']['corrected_fluxes_and_quality_flags'].keys():
            # change data type from string to float and remove some data points
            temp = float(item['full_output']['corrected_fluxes_and_quality_flags']['H'])
            if (temp > 50)|(temp < -10) :
                temp = None
                
            H.append(temp)
        
        ##### Wind Speed
        if 'wind_speed' in item['full_output']['rotated_wind'].keys():
            # change data type from string to float and remove some data points
            temp = float(item['full_output']['rotated_wind']['wind_speed'])
            if (temp > 4)|(temp < 0) :
                temp = None
               
            wind_speed.append(temp)
        
        ##### Wind Direction
        if 'wind_dir' in item['full_output']['rotated_wind'].keys():
            # change data type from string to float and remove some data points
            temp = float(item['full_output']['rotated_wind']['wind_dir'])
                
            wind_dir.append(temp)
    
    
    dict_data = {
        0 : { 
            'data': [TA_1_1_1],
            'title': ['Atmospheric Temperature'],
            'unicode': u'T<sub>A</sub> (\N{DEGREE SIGN}C)',
            'file': 'TA_1_1_1.html',
            'color': ['#607d8b']
        },
        1 : { 
            'data': [TS_1_1_1],
            'title': ['Seawater Temperature'],
            'unicode': u'T<sub>S</sub> (\N{DEGREE SIGN}C)',
            'file': 'water_temperature.html',
            'color': ['#2196F3']
        },
        2 : { 
            'data': [PPFD_1_1_1],
            'title': ['PAR'],
            'unicode': u'PPFD (\u03BCmol m<sup>-2</sup> s<sup>-1</sup>)',
            'file': 'PPFD_1_1_1.html',
            'color': ['#E91E63']
        },
        3 : { 
            'data': [RG_1_1_1, RN_1_1_1],
            'title': ['RG', 'RN'],
            'unicode': 'RG and RN (W m<sup>-2</sup>)',
            'file': 'RG_1_1_1.html',
            'color': ['#33CFA5', '#F06A6A']
        },
        4 : { 
            'data': [P_RAIN_1_1_1],
            'title': ['P_RAIN'],
            'unicode': '30-min cumulative rain (mm)',
            'file': 'P_RAIN_1_1_1.html',
            'color': ['#2196F3']
        },
        5 : { 
            'data': [RH_1_1_1],
            'title': ['RH'],
            'unicode': 'RH (%)',
            'file': 'RH_1_1_1.html',
            'color': ['#607d8b']
        },
        6 : { 
            'data': [co2_flux],
            'title': ["CO2 Flux"],
            'unicode': u'CO<sub>2</sub> Flux (\u03BCmol m<sup>-2</sup> s<sup>-1</sup>)',
            'file': 'co2_flux.html',
            'color': ['#F06A6A']
        },
        7 : { 
            'data': [LE],
            'title': ["LE"],
            'unicode': 'LE (W m<sup>-2</sup>)',
            'file': 'LE.html',
            'color': ['#2196F3']
        },
        8 : { 
            'data': [H],
            'title': ["H"],
            'unicode': 'H (W m<sup>-2</sup>)',
            'file': 'H.html',
            'color': ['#33CFA5']
        },
        9 : { 
            'data': [wind_speed],
            'title': ["wind_speed"],
            'unicode': 'Wind Speed (m s<sup>-1</sup>)',
            'file': 'wind_speed.html',
            'color': ['#2196F3']
        }
    }    
    
    
    for item in dict_data:
        # create the plot
        fig = go.Figure()
        
        for i in range(len(dict_data[item]['data'])):
            fig.add_trace(go.Scatter(
                x=dateTime, y=dict_data[item]['data'][i], name=dict_data[item]['title'][i],
                mode='lines',connectgaps=False, line_color=dict_data[item]['color'][i]
                ))
                
        # we replace 2d array to one array similar to rest otherwise we need to pass somethin like item[0][2] that does not match with others
        fig.update_layout(title_text= '',xaxis_title='Date', template="plotly_white",
                           yaxis_title= dict_data[item]['unicode'],
                          xaxis_rangeslider_visible=False,margin=dict(
                l=50,
                r=50,
                b=50,
                t=50,
                pad=0
            ))
        
        fig.update_xaxes(
            rangeslider_visible=False,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=7, label="7d", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward")
                ])
            )
        )
        
        # save it in lambda tmp folder
        fig.write_html("/tmp/"+ dict_data[item]['file'])
        
        # upload on s3
        s3.upload_file("/tmp/" + dict_data[item]['file'], bucket, dict_data[item]['file'])
    
    
    

    wind_dir_compass=[]
    for val in wind_dir:
        wind_dir_compass.append(degToCompass(val))
        
    strength = []
    for val in wind_speed:
        if val == None:
            strength.append(None)
        elif val < 0.5:
            strength.append("0-0.5")
        elif val >= 0.5 and val < 1:
            strength.append("0.5-1")
        elif val >= 1 and val < 1.5:
            strength.append("1-1.5")
        elif val >= 1.5 and val < 2:
            strength.append("1.5-2")
        elif val >= 2 and val < 2.5:
            strength.append("2-2.5")
        elif val >= 2.5 and val < 3:
            strength.append("2.5-3")
        else:
            strength.append("+3")
    
    month = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    show_date = []
    for val in dateTime:
        show_date.append(month[int(val.split("-")[1])]  + " "  + val.split("-")[0])
    
    
    df = pd.DataFrame({'wind_speed': wind_speed, 'wind_dir_compass': wind_dir_compass, 'Wind Speed (m s<sup>-1</sup>)': strength, 'date': show_date})
    df365 = df.copy()
    incomplete_start = show_date[0]
    incomplete_end = show_date[-1]
    print(incomplete_start)
    print(incomplete_end)
    df = df[df["date"].str.contains(incomplete_end + "|" +  incomplete_start)==False]
    df.dropna(inplace=True)
    
    compass = ["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    add_dummy=True;
    new = pd.DataFrame(columns = ['wind_speed', 'wind_dir_compass', 'Wind Speed (m s<sup>-1</sup>)', 'date'])
    for i in range(len(df)):
        if (df['date'].iloc[i] != df['date'].iloc[i-1]):
            add_dummy=True;
        if(add_dummy):
            for data in compass:
                new = new.append({'wind_speed' : 0, 'wind_dir_compass' : data, 'Wind Speed (m s<sup>-1</sup>)' : '0-0.5', 'date': df['date'].iloc[i]}, ignore_index = True)
            add_dummy=False;
        new = new.append({'wind_speed' : df['wind_speed'].iloc[i], 'wind_dir_compass' : df['wind_dir_compass'].iloc[i], 'Wind Speed (m s<sup>-1</sup>)' : df['Wind Speed (m s<sup>-1</sup>)'].iloc[i], 'date': df['date'].iloc[i]}, ignore_index = True)
    print("****************")
    print(new.head())
    fig = px.bar_polar(new, r="wind_speed" ,template="none", theta="wind_dir_compass", color= 'Wind Speed (m s<sup>-1</sup>)', color_discrete_sequence= px.colors.sequential.Plasma_r, animation_frame="date")
    fig.update_layout(
        polar=dict(radialaxis=dict(showticklabels=False, ticks='', linewidth=0)
        )
    )
    
    # save it in lambda tmp folder
    file = 'windrose.html'
    fig.write_html("/tmp/"+ file)
        
    # upload on s3
    s3.upload_file("/tmp/" + file, bucket, file)
    
    
    # windrose -365
    
    df365.dropna(inplace=True)
    print(df365.head())
    dummy = pd.DataFrame({'wind_dir_compass': ["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"],
                'wind_speed': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                'Wind Speed (m s<sup>-1</sup>)': ["0-0.5", "0-0.5", "0-0.5", "0-0.5","0-0.5","0-0.5", "0-0.5", "0-0.5","0-0.5","0-0.5","0-0.5","0-0.5","0-0.5","0-0.5","0-0.5","0-0.5"]})
    
    df365 = dummy.append(df365, ignore_index=True)
    
    
    fig = px.bar_polar(df365, r="wind_speed" , template="none", theta="wind_dir_compass", color="Wind Speed (m s<sup>-1</sup>)", color_discrete_sequence= px.colors.sequential.Plasma_r)
    fig.update_layout(
        polar=dict(radialaxis=dict(showticklabels=False, ticks='', linewidth=0)
        )
    )
    
    # save it in lambda tmp folder
    file = 'windrose365.html'
    fig.write_html("/tmp/"+ file)
        
    # upload on s3
    s3.upload_file("/tmp/" + file, bucket, file)
    print(df365.head())
    
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Done!')
    }
