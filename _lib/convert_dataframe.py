import pandas as pd
import re

#Hace la ponderación de horas
def ponderar_a_100(valores):
    suma_total = sum(valores)
    
    if suma_total == 0:
        return [0] * len(valores)  # Para evitar la división por cero
    
    factor_escala = 100 / suma_total
    
    ponderaciones = [int(round(valor * factor_escala)) for valor in valores]
    
    return ponderaciones

#Elimina los proyectos que tienen un patron de 202X-XX.XX en el nombre y asigna los registros de este como si fuese el principal. 
def delete_point_proyects(user_records,projects,unique_projects):
    
    # Patrón para 202X-XX-XX.XX donde X es cualquier número
    PATRON_PREFIJO = r'^202\d-\d{2}\.\d{2}'

    #Itera por los proyectos
    for proj in unique_projects:
        if re.match(PATRON_PREFIJO, proj):
            #Elimina el proyecto en la lista de proyectos 
            unique_projects.remove(proj)
            #Nombre del proyecto sin .XX
            project = [pos for pos in projects if pos["name"].startswith(proj[0:7] + " ")][0]["name"]
            #Itera por los registros de los usuarios
            for r in user_records:
                if r["projectName"] == proj:
                    r["projectName"] = project
    
    return user_records, unique_projects
        

#Convierte el registro de ponderación a un datfarame
def convert_dataframe(records:object,employees:dict,fecha_inicio:str,fecha_fin:str,projects:list):

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

            #T.TRANS lo arregla por TTRANSF
            if "T.TRANS" in unique_projects:
                unique_projects = ["TTRANSF" if item == "T.TRANS" else item for item in unique_projects]

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

            #Verifica los registros de los proyectos que tienen el patrón P-202X-XX.XX
            user_records, unique_projects = delete_point_proyects(user_records,projects,unique_projects)

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