# Give Lambda Function Access to the DynamoDB Table
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    
    cite = {
        "DOI": "https://doi.org/10.6084/m9.figshare.19613889.v1",
        "email": "yusriy@usm.my",
        "citation": "Yusup, Yusri; Jolous Jamshidi, Ehsan (2022): Atmosfera USM Muka Head Dataset. figshare. Dataset. https://doi.org/10.6084/m9.figshare.19613889.v1" 
    }
        
    station = { 
        "name": "Muka Head Station",
        "location": {
            "latitude": "5.468040",
            "longitude": "100.200258",
            "ASL": "4m"
        }
        
    }
            
    print(event)
    start = event['params']['querystring']['start'] + " 00:00"
    end = event['params']['querystring']['end'] + " 23:30"
    category = event['params']['querystring']['category']
    category = category.split('--')[:-1]
    
        
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ec_mukaHead')
    response = table.query(KeyConditionExpression= Key('station').eq('mukahead') & Key('dateTime').between(start, end))
    
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items']) 
        
    body = []
    temperature, radiation, water_cycle, carbon_cycle, turbulence = {}, {}, {}, {}, {}
    for item in data:
        for cat in category:
            dateTime = item['dateTime']
            if cat == 'temperature':
                temperature = {}
                if 'TA_1_1_1' in item['biomet']['met'].keys():
                    temperature.update({'TA': item['biomet']['met']['TA_1_1_1']})
                if 'TS_1_1_1' in item['biomet']['met'].keys():
                    temperature.update({'TS': item['biomet']['met']['TS_1_1_1']}) 
            if cat == 'radiation':
                radiation = {}
                if 'RN_1_1_1' in item['biomet']['met'].keys():
                    radiation.update({'RN': item['biomet']['met']['RN_1_1_1']})
                if 'RG_1_1_1' in item['biomet']['met'].keys():
                    radiation.update({'RG': item['biomet']['met']['RG_1_1_1']})
                if 'PPFD_1_1_1' in item['biomet']['met'].keys():
                    radiation.update({'PPFD': item['biomet']['met']['PPFD_1_1_1']})
                        
            if cat == 'water cycle':
                water_cycle = {}
                if 'RH_1_1_1' in item['biomet']['met'].keys():
                    water_cycle.update({'RH': item['biomet']['met']['RH_1_1_1']})
                if 'P_RAIN_1_1_1' in item['biomet']['met'].keys():
                    water_cycle.update({'P-Rain': item['biomet']['met']['P_RAIN_1_1_1']})
                if 'LE' in item['full_output']['corrected_fluxes_and_quality_flags'].keys():
                    water_cycle.update({'LE': item['full_output']['corrected_fluxes_and_quality_flags']['LE']})
                if 'qc_LE' in item['full_output']['corrected_fluxes_and_quality_flags'].keys():
                    water_cycle.update({'qc_LE': item['full_output']['corrected_fluxes_and_quality_flags']['qc_LE']})
                if 'co2_mixing_ratio' in item['full_output']['gas_densities_concentrations_and_timelags'].keys():
                    water_cycle.update({'H2O mixing ratio': item['full_output']['gas_densities_concentrations_and_timelags']['co2_mixing_ratio']})
                if 'H' in item['full_output']['corrected_fluxes_and_quality_flags'].keys():
                    water_cycle.update({'H': item['full_output']['corrected_fluxes_and_quality_flags']['H']})
                if 'bowen_ratio' in item['full_output']['turbulence'].keys():
                    water_cycle.update({'Bowen ratio': item['full_output']['turbulence']['bowen_ratio']})
                        
            if cat == 'carbon cycle':
                carbon_cycle = {}
                if 'co2_flux' in item['full_output']['corrected_fluxes_and_quality_flags'].keys():
                    carbon_cycle.update({'CO2 flux': item['full_output']['corrected_fluxes_and_quality_flags']['co2_flux']})
                if 'qc_co2_flux' in item['full_output']['corrected_fluxes_and_quality_flags'].keys():
                    carbon_cycle.update({'qc CO2 flux': item['full_output']['corrected_fluxes_and_quality_flags']['qc_co2_flux']})
                if 'co2_mixing_ratio' in item['full_output']['gas_densities_concentrations_and_timelags'].keys():
                    carbon_cycle.update({'CO2 mixing ratio': item['full_output']['gas_densities_concentrations_and_timelags']['co2_mixing_ratio']})
    
            if cat == 'turbulence':
                turbulence = {}
                if 'wind_speed' in item['full_output']['rotated_wind'].keys():
                    turbulence.update({'wind speed': item['full_output']['rotated_wind']['wind_speed']})
                if 'wind_dir' in item['full_output']['rotated_wind'].keys():
                    turbulence.update({'wind direction': item['full_output']['rotated_wind']['wind_dir']})
                if 'air_pressure' in item['full_output']['air_properties'].keys():
                    turbulence.update({'air pressure': item['full_output']['air_properties']['air_pressure']})
                    
            data = {**{'dateTime': dateTime}, **{'Temperature': temperature}, **{'Radiation': radiation}, **{'Water Cycle': water_cycle}, **{'Carbon Cycle': carbon_cycle}, **{'Turbulence': turbulence}}
            unit={
                'dateTime': 'yyyy-mm-dd HH:MM',
                'Temperature': { 
                    'TA': 'K',
                    'TS': 'K'
                },
                'Radiation': {
                    'RN': 'W/m^2',
                    'RG': 'W/m^2',
                    'PPFD': 'Âµmol/m^2/s'
                    },
                'Water Cycle': { 
                    'RH': '%',
                    'P-Rain': 'm', # should not be mm? it is 'm' in biomet file
                    'LE': 'W+1m-2',
                    'qc_LE': '#',
                    'H2O mixing ratio': 'mmol+1mol_d-1',
                    'H': 'W+1m-2',
                    'Bowen ratio': '#'
                },
                'Carbon Cycle': { 
                    'CO2 flux': 'Âµmol+1s-1m-2',
                    'qc CO2 flux': '#',
                    'CO2 mixing ratio': 'Âµmol+1mol_d-1'
                },
                'Turbulence': {
                    'wind speed': 'm+1s-1',
                    'wind direction': 'deg_from_north',
                    'air pressure': 'Pa'
                }
            }
            # delete empty dict (not selected category)
            if not len(temperature):
                del data['Temperature']
                del unit['Temperature']
            if not len(radiation):
                del data['Radiation']
                del unit['Radiation']
            if not len(water_cycle):
                del data['Water Cycle']
                del unit['Water Cycle']
            if not len(carbon_cycle):
                del data['Carbon Cycle']
                del unit['Carbon Cycle']
            if not len(turbulence):
                del data['Turbulence']
                del unit['Turbulence']
                
        body.append(data)
    return {
        'statusCode': 200,
        'cite': cite,
        'station': station,
        'unit': unit,
        'body': body
    }
