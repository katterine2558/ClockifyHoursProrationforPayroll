#importa librerías
import configparser
import requests
import os
import sys
import json
from _lib.get_config_path import get_config_path

def get_records(fecha_inicio:str,fecha_fin:str,workspaceId:str):

    # URL para generar reporte
    url_base = f'https://reports.api.clockify.me/v1'
    url_report = f'/workspaces/{workspaceId}/reports/detailed'
    url = url_base  + url_report
    # Lectura de la clave de la API - karias@pedelta.com.co - cada usuario tiene su clave API
    config_path = get_config_path()
    print(config_path)
    config = configparser.ConfigParser()
    config.read(config_path)
    X_Api_Key = config.get('clockify', 'API_KEY')
    # Post al servidor
    headers = {'content-type': 'application/json', 'X-Api-Key': X_Api_Key}
    records =[]
    continuar=True
    i = 1
    while continuar:

        data = {
        "dateRangeStart": f"{fecha_inicio}T00:00:00.000",
        "dateRangeEnd": f"{fecha_fin}T23:59:59.000",
        "detailedFilter": {
            "page": i,
            "pageSize": 1000,
        },
        "exportType": "JSON",
        "users": {
        "status": "ACTIVE"
            }

        }
        response = requests.post( url, headers=headers, data=json.dumps(data))
        decoded_content = response.content.decode('utf-8')
        decoded_content = decoded_content.replace("null","None")
        decoded_content = decoded_content.replace("true","True")
        decoded_content = decoded_content.replace("false","False")
        decoded_content = eval(decoded_content)

        if decoded_content["timeentries"]:
            records.extend(decoded_content["timeentries"])
            i+=1
        else:
            continuar = False

    return records