"""
CREATED BY: KATERINE ARIAS
"""
#Importa librerías
import configparser
import requests
import re
import pickle
import os
import sys
from _lib.get_config_path import get_config_path

def get_projects(workspace):

    #inicializa el diccionario para almacenar
    worskpace_projects = []
    
    # URL para obtener los proyectos del workspace
    url_base = f'https://api.clockify.me/api/v1/workspaces/{workspace}/projects'

    # Lectura de la clave de la API
    config_path = get_config_path()
    config = configparser.ConfigParser()
    config.read(config_path)
    X_Api_Key = config.get('clockify', 'API_KEY')

    # Get al servidor
    headers = { 'X-Api-Key': X_Api_Key}
    continuar = True
    i = 1
    while continuar:
        data = {
                "page-size": 200,
                "page": i,
                "archived": False
            }
        response = requests.get(url_base, headers=headers, params=data)
        decoded_content = response.content.decode('utf-8')
        decoded_content = decoded_content.replace("null","None")
        decoded_content = decoded_content.replace("true","True")
        decoded_content = decoded_content.replace("false","False")
        decoded_content = eval(decoded_content)

        if len(decoded_content) > 0:

            if i == 1:
                for j in range(len(decoded_content)):
                    worskpace_projects.append(decoded_content[j])
            else:
                cons_id = len(worskpace_projects)
                for j in range(cons_id,len(decoded_content)+cons_id): 
                    worskpace_projects.append(decoded_content[j-cons_id])

            i+=1

        else:

            continuar = False

    #Lista con lo que empiezan por el prefijo
    projects = []
    for proj in worskpace_projects:
            projects.append(proj)

    return projects
