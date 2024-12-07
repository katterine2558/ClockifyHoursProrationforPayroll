import configparser
import requests
import os 
import sys
from _lib.get_config_path import get_config_path

# Obtener workspace  Pedelta Colombia
def get_workspace_id():

    # URL para generar reporte
    url = f'https://api.clockify.me/api/v1/workspaces'
    # Lectura de la clave de la API
    config_path = get_config_path()
    print(config_path)
    config = configparser.ConfigParser()
    config.read(config_path)
    X_Api_Key = config.get('clockify', 'API_KEY')
    # Get al servidor
    headers = { 'X-Api-Key': X_Api_Key}
    response = requests.get(url, headers=headers)
    decoded_content = response.content.decode('utf-8')
    decoded_content = decoded_content.replace("null","None")
    decoded_content = decoded_content.replace("true","True")
    decoded_content = decoded_content.replace("false","False")
    decoded_content = eval(decoded_content)

    for w in decoded_content:
        if w["name"] == "PEDELTA COLOMBIA":
            workspaceId = w["id"]
            break

    return workspaceId