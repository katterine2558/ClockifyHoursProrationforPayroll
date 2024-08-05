"""
CREATED BY
KA
"""

#importar librerias
import pandas as pd
import configparser
import pickle
import requests
import json
import xlwings as wx
import re 
import os
from f_readEmployeesDB import f_readEmployeesDB

main_path  = os.path.join(os.path.dirname(os.path.realpath(__file__)))

#Obtener workspace
def get_workspace_id():

    # URL para generar reporte
    url = f'https://api.clockify.me/api/v1/workspaces'
    # Lectura de la clave de la API
    config = configparser.ConfigParser()
    config.read(os.path.join(main_path, "config.ini")) 
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
        if w["name"] == "WORKsPACE MATCH":
            workspaceId = w["id"]
            break

    return workspaceId

def get_records(fecha_inicio:str,fecha_fin:str,workspaceId:str):

    # URL para generar reporte
    url_base = f'https://reports.api.clockify.me/v1'
    url_report = f'/workspaces/{workspaceId}/reports/detailed'
    url = url_base  + url_report
    # Lectura de la clave de la API 
    config = configparser.ConfigParser()
    config.read(os.path.join(main_path, "config.ini")) 
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

def convert_dataframe(records:object,employees:dict,fecha_inicio:str,fecha_fin:str):

    #Cambia el formato de aaaa-mm-dd a dd-mm-aaaa
    fecha_inicio = f"{fecha_inicio.split('-')[2]}-{fecha_inicio.split('-')[1]}-{fecha_inicio.split('-')[0]}"
    fecha_fin =  f"{fecha_fin.split('-')[2]}-{fecha_fin.split('-')[1]}-{fecha_fin.split('-')[0]}"

    dataframe = {
        "Id colaborador": [],
        "Proyecto Id": [],
        "Fecha inicio": [],
        "Fecha fin": [],
        "Prorrateo": []
    }

    # Lista única de correos de los colaboradores
    unique_emails = list({record['userEmail'] for record in records})

    #Itera por cada correo unico para ver las actividades desarrolladas por ese usuario
    for email in unique_emails:
        try:
            #Identificación del usuario
            id_Colaborador=employees["IDENTIFICACIÓN"][employees["CORREOS"].index(email)]
            if type(id_Colaborador) == str:
                if "CE" in id_Colaborador:
                    id_Colaborador = int(id_Colaborador.split("CE ")[1])
                    
            # Registros de un usuario en particular
            user_records = [record for record in records if record['userEmail'] == email]

            #Proyectos en los que ha trabajado el colaborador
            unique_projects = list({record['projectName'] for record in user_records})

            #Borra los proyectos que no se tienen en cuenta
            try:
                unique_projects.remove("INCAPACIDAD MÉDICA")
            except ValueError:
                pass
            try:
                unique_projects.remove("COMPENSATORIO")
            except ValueError:
                pass
            try:
                unique_projects.remove("FESTIVO")
            except ValueError:
                pass
            try:
                unique_projects.remove("VACACIONES")
            except ValueError:
                pass
            try:
                unique_projects.remove("LICENCIAS MATERNIDAD O PATERNIDAD")
            except ValueError:
                pass
            try:
                unique_projects.remove("PUENTES")
            except ValueError:
                pass
            try:
                unique_projects.remove("REHABILITACIONES")
            except ValueError:
                pass
            try:
                unique_projects.remove("INFRAS")
            except ValueError:
                pass
            try:
                unique_projects.remove("EDIF")
            except ValueError:
                pass

            #Itera sobre los proyectos para sumar las horas
            horas = []
            for project in unique_projects:

                #Registros asociados a un único proyecto
                project_records = [record for record in user_records if record['projectName'] == project]

                sum_horas=0
                for r in project_records:
                    sum_horas+=(r["timeInterval"]["duration"] / 3600)

                horas.append(sum_horas)

                #Almacena la identificación del usuario
                dataframe["Id colaborador"].append(id_Colaborador)
                #Almacena el identificador del proyecto
                if "PM-" in project: #Proyectos de méxico
                    coincidencias = re.findall(r'\bPM-\d{4}-\d{2}', project)
                    coincidencias[0] = coincidencias[0].split('-')[0]+ '-' + coincidencias[0].split('-')[1][2:] + '-' + coincidencias[0].split('-')[-1]
                else:
                    coincidencias = re.findall(r'\d{4}-\d{2}', project)

                
                if len(coincidencias) >0:
                    dataframe["Proyecto Id"].append(coincidencias[0])
                else:
                    dataframe["Proyecto Id"].append(project)
                    
                #Almacena la fecha de inicio y fin
                dataframe["Fecha inicio"].append(fecha_inicio)
                dataframe["Fecha fin"].append(fecha_fin)

            #Ponderacion
            ponderaciones = ponderar_a_100(horas)
            dataframe["Prorrateo"].extend(ponderaciones)
        
        except ValueError:
            pass
    
    return dataframe

def ponderar_a_100(valores):
    suma_total = sum(valores)
    
    if suma_total == 0:
        return [0] * len(valores)  # Para evitar la división por cero
    
    factor_escala = 100 / suma_total
    
    ponderaciones = [int(round(valor * factor_escala)) for valor in valores]
    
    return ponderaciones

def write_excel(dataframe):

    #Escribir excel 
    app = wx.App(visible=False)
    wb = wx.Book()
    #Selecciona la hoja
    sheet_names = wb.sheets
    wb.sheets[0].name = dataframe["Nombre Prorrateo"][0]
    ws = wb.sheets[dataframe["Nombre Prorrateo"][0]]

    row = 1
    for i in range(len(dataframe["Id colaborador"])):

        #Escribe el id del colaborador
        ws.range(row,1).value = dataframe["Id colaborador"][i]
        #Escribe el nombre del proyecto
        ws.range(row,2).value = dataframe["Proyecto Id"][i]
        #Escribe fecha de inicio
        ws.range(row,3).value = f"'{dataframe['Fecha inicio'][i]}"
        #Escribe fecha fin
        ws.range(row,4).value = f"'{dataframe['Fecha fin'][i]}"
        #Escribe Prorrateo
        ws.range(row,5).value = dataframe["Prorrateo"][i]
        #Escribe nombre prorrateo
        ws.range(row,6).value = dataframe["Nombre Prorrateo"][i]

        row+=1

    #Modifica el ancho de columna
    ws.range(f"A1:A{len(dataframe['Id colaborador'])+1}").column_width = 15
    ws.range(f"B1:B{len(dataframe['Id colaborador'])+1}").column_width = 15
    ws.range(f"C1:C{len(dataframe['Id colaborador'])+1}").column_width = 10
    ws.range(f"D1:D{len(dataframe['Id colaborador'])+1}").column_width = 10
    ws.range(f"E1:E{len(dataframe['Id colaborador'])+1}").column_width = 5
    ws.range(f"F1:F{len(dataframe['Id colaborador'])+1}").column_width = 20
    ws.range(f"1:{len(dataframe['Id colaborador'])+1}").row_height = 15

    #Guarda el documento
    documentsPath = os.path.expanduser("~\Documents")
    filename = dataframe["Nombre Prorrateo"][0]
    wb.save(f"{documentsPath}\\{filename}.xlsx")
    wb.close()
    app.quit()

    return filename

    
def f_generar_reporte(fecha_inicio:str,fecha_fin:str,bd_path:str):

    #WorkspaceId 
    workspaceId = get_workspace_id()

    #Contenido de reporte
    records = get_records(fecha_inicio,fecha_fin,workspaceId)

    #Obtiene la base de datos de colaboradores
    employees = f_readEmployeesDB(bd_path)
    
    #convierte todos los correos que estén en mayuscula a minuscula
    for i in range(len(employees["CORREOS"])):
        if employees["CORREOS"][i].islower():
            pass
        else:
            employees["CORREOS"][i] = employees["CORREOS"][i].lower()

    #Obtener todo como un dataframe
    dataframe = convert_dataframe(records,employees,fecha_inicio,fecha_fin)

    #Asigna el nombre del prorrateo
    if fecha_inicio.split('-')[1] == "01":
        prorrateo_nombre = "PRORRATEO_ENE"
    elif fecha_inicio.split('-')[1] == "02":
        prorrateo_nombre = "PRORRATEO_FEB"
    elif fecha_inicio.split('-')[1] == "03":
        prorrateo_nombre = "PRORRATEO_MAR"
    elif fecha_inicio.split('-')[1] == "04":
        prorrateo_nombre = "PRORRATEO_ABR"
    elif fecha_inicio.split('-')[1] == "05":
        prorrateo_nombre = "PRORRATEO_MAY"
    elif fecha_inicio.split('-')[1] == "06":
        prorrateo_nombre = "PRORRATEO_JUN"
    elif fecha_inicio.split('-')[1] == "07":
        prorrateo_nombre = "PRORRATEO_JUL"
    elif fecha_inicio.split('-')[1] == "08":
        prorrateo_nombre = "PRORRATEO_AGO"
    elif fecha_inicio.split('-')[1] == "09":
        prorrateo_nombre = "PRORRATEO_SEP"
    elif fecha_inicio.split('-')[1] == "10":
        prorrateo_nombre = "PRORRATEO_OCT"
    elif fecha_inicio.split('-')[1] == "11":
        prorrateo_nombre = "PRORRATEO_NOV"
    elif fecha_inicio.split('-')[1] == "12":
        prorrateo_nombre = "PRORRATEO_DIC"

    dataframe["Nombre Prorrateo"] = [prorrateo_nombre] * len(dataframe["Id colaborador"])
    
    #Escribe el excel
    filename=write_excel(dataframe)

    #Genera el log
    with open(os.path.join(os.path.expanduser("~\\Documents"),"generar_reporte.log"),"w") as f:
        f.write(f"{filename}.xlsx")
    f.close()