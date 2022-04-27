# Give Lambda Function Access to the DynamoDB Table
import json
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

    unit={
        "full_output": {
                "storage_fluxes": {
                    "H_strg": "W+1m-2",
                    "LE_strg": "W+1m-2",
                    "co2_strg": "Âµmol+1s-1m-2",
                    "h2o_strg": "mmol+1s-1m-2"
                },
                "rotation_angles_for_tilt_correction": {
                    "roll": "deg",
                    "yaw": "deg",
                    "pitch": "deg"
                },
                "air_properties": {
                    "e": "Pa",
                    "Tdew": "K",
                    "VPD": "Pa",
                    "air_molar_volume": "m+3mol-1",
                    "es": "Pa",
                    "air_density": "kg+1m-3",
                    "ET": "mm+1hour-1",
                    "sonic_temperature": "K",
                    "air_temperature": "K",
                    "RH": "%",
                    "air_heat_capacity": "J+1kg-1K-1",
                    "water_vapor_density": "kg+1m-3",
                    "air_pressure": "Pa",
                    "specific_humidity": "kg+1kg-1"
                },
                "diagnostic_flags_LI-7500": {
                    "pll_LI-7500": "#_flagged_recs",
                    "sync_LI-7500": "#_flagged_recs",
                    "chopper_LI-7500": "#_flagged_recs",
                    "detector_LI-7500": "#_flagged_recs"
                },
                "custom_variables": {
                    "dew_point_mean": "--",
                    "vin_sf_mean": "--",
                    "co2_mean": "--",
                    "h2o_mean": "--",
                    "co2_signal_strength_7500_mean": "--"
                },
                "statistical_flags": {
                    "discontinuities_hf": "8u/v/w/ts/co2/h2o/ch4/none",
                    "skewness_kurtosis_sf": "8u/v/w/ts/co2/h2o/ch4/none",
                    "discontinuities_sf": "8u/v/w/ts/co2/h2o/ch4/none",
                    "amplitude_resolution_hf": "8u/v/w/ts/co2/h2o/ch4/none",
                    "drop_out_hf": "8u/v/w/ts/co2/h2o/ch4/none",
                    "absolute_limits_hf": "8u/v/w/ts/co2/h2o/ch4/none",
                    "timelag_hf": "8co2/h2o/ch4/none",
                    "spikes_hf": "8u/v/w/ts/co2/h2o/ch4/none",
                    "skewness_kurtosis_hf": "8u/v/w/ts/co2/h2o/ch4/none",
                    "attack_angle_hf": "8aa",
                    "non_steady_wind_hf": "8U",
                    "timelag_sf": "8co2/h2o/ch4/none"
                },
                "RSSI_LI-7500": {
                    "mean_value_RSSI_LI-7500": "100"
                },
                "turbulence": {
                    "L": "m",
                    "u*": "m+1s-1",
                    "(z-d)/L": "#",
                    "T*": "K",
                    "TKE": "m+2s-2",
                    "bowen_ratio": "#"
                },
                "unrotated_wind": {
                    "w_unrot": "m+1s-1",
                    "u_unrot": "m+1s-1",
                    "v_unrot": "m+1s-1"
                },
                "vertical_advection_fluxes": {
                    "co2_v-adv": "Âµmol+1s-1m-2",
                    "h2o_v-adv": "mmol+1s-1m-2"
                },
                "rotated_wind": {
                    "u_rot": "m+1s-1",
                    "max_wind_speed": "m+1s-1",
                    "wind_speed": "m+1s-1",
                    "wind_dir": "deg_from_north",
                    "v_rot": "m+1s-1",
                    "w_rot": "m+1s-1"
                },
                "footprint": {
                    "x_90%": "m",
                    "x_peak": "m",
                    "x_70%": "m",
                    "x_50%": "m",
                    "x_30%": "m",
                    "x_10%": "m",
                    "model": "0=KJ/1=KM/2=HS",
                    "x_offset": "m"
                },
                "spikes": {
                    "co2_spikes": "#",
                    "h2o_spikes": "#",
                    "w_spikes": "#",
                    "u_spikes": "#",
                    "v_spikes": "#",
                    "ts_spikes": "#"
                },
                "covariances": {
                    "w/ts_cov": "m+1K+1s-1",
                    "w/h2o_cov": "--",
                    "w/co2_cov": "--"
                },
                "file_info": {
                    "file_records": "#",
                    "used_records": "#",
                    "filename": "",
                    "daytime": "1=daytime",
                    "DOY": "ddd.ddd"
                },
                "corrected_fluxes_and_quality_flags": {
                    "qc_LE": "#",
                    "h2o_flux": "mmol+1s-1m-2",
                    "qc_h2o_flux": "#",
                    "co2_flux": "Âµmol+1s-1m-2",
                    "qc_Tau": "#",
                    "H": "W+1m-2",
                    "Tau": "kg+1m-1s-2",
                    "LE": "W+1m-2",
                    "qc_co2_flux": "#",
                    "qc_H": "#"
                },
                "gas_densities_concentrations_and_timelags": {
                    "h2o_def_timelag": "1=default",
                    "co2_mixing_ratio": "Âµmol+1mol_d-1",
                    "h2o_mole_fraction": "mmol+1mol_a-1",
                    "co2_molar_density": "mmol+1m-3",
                    "co2_time_lag": "s",
                    "h2o_mixing_ratio": "mmol+1mol_d-1",
                    "co2_def_timelag": "1=default",
                    "co2_mole_fraction": "Âµmol+1mol_a-1",
                    "h2o_time_lag": "s",
                    "h2o_molar_density": "mmol+1m-3"
                },
                "variances": {
                    "u_var": "m+2s-2",
                    "ts_var": "K+2",
                    "v_var": "m+2s-2",
                    "w_var": "m+2s-2",
                    "co2_var": "--",
                    "h2o_var": "--"
                },
                "uncorrected_fluxes": {
                    "Tau_scf": "#",
                    "un_Tau": "kg+1m-1s-2",
                    "un_H": "W+1m-2",
                    "un_co2_flux": "Âµmol+1s-1m-2",
                    "un_h2o_flux": "mmol+1s-1m-2",
                    "LE_scf": "#",
                    "un_LE": "W+1m-2",
                    "H_scf": "#",
                    "co2_scf": "#",
                    "h2o_scf": "#"
                }
            },
            "biomet": {
                "met": {
                    "TA_1_1_1": "K",
                    "RN_1_1_1": "W/m^2",
                    "P_RAIN_1_1_1": "m", #??????????
                    "RH_1_1_1": "%",
                    "TS_1_1_1": "K",
                    "PPFD_1_1_1": "Âµmol/m^2/s",
                    "RG_1_1_1": "W/m^2"
                },
                "others": {
                    "VIN_1_1_1": "V",
                    "UNNAMED_0_0_1": "OTHER",
                    "LOGGERTEMP_0_0_1": "C",
                    "DOY": "ddd.ddd"
                }
            },
            "dateTime": "yyyy-mm-dd HH:MM"
        }
    print(event)
    
    start = event['start'] + " 00:00"
    end = event['end'] + " 23:30"
    data = event['data']
    fileName = event['fileName']

    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ec_mukaHead')
    response = table.query(KeyConditionExpression= Key('station').eq('mukahead') & Key('dateTime').between(start, end))
    dataItems = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        dataItems.extend(response['Items']) 
    

    body = []
    for item in dataItems:
        if data == 'all':
            body.append(item)
        elif data == 'biomet':
            body.append({**{'dateTime': item['dateTime']}, **{'biomet': item['biomet']}})
        elif data == 'fulloutput':
            body.append({**{'dateTime': item['dateTime']}, **{'full_output': item['full_output']}})
            
    if data == "biomet":
        del unit['full_output']
    elif data == 'full_output':
        del unit['biomet']

    
    jsonFile = {
        'cite': cite,
        'station': station,
        'unit': unit,
        'body': body
    }
    
    # create a connection to S3
    s3 = boto3.client('s3')  
    # upload on s3
    s3.put_object(Bucket= "ec-mukahead-temp-data", Key= fileName + ".json", Body= (bytes(json.dumps(jsonFile).encode('UTF-8'))))
    
    # TODO implement
    return {
        'statusCode': 200
    }
