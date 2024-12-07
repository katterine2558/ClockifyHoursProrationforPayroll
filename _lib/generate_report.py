#Importa librerías
import os
import tkinter
import tkinter.messagebox
from _lib.read_database import read_database
from _lib.get_workspaces_id import get_workspace_id
from _lib.get_projects import get_projects
from _lib.get_records import get_records
from _lib.convert_dataframe import convert_dataframe
from _lib.write_excel import write_excel
import time

#ACTUALIZA LA BARRA DE PROGRESO
def update_progress_bar(contador,mensaje,barra_progreso,texto_progreso,ventana_progreso):
    barra_progreso.set(contador / 8)  # Actualizar progreso
    texto_progreso.set(mensaje)
    ventana_progreso.update_idletasks()  # Forzar actualización de la ventana

#GENERA EL REPORTE DE CLOCKIFY
def f_generate_report(ventana_progreso, barra_progreso, texto_progreso,fecha_inicio,fecha_fin):

    #Verifica si existe la unidad G://
    if not os.path.exists("G:"):
        ventana_progreso.destroy()
        tkinter.messagebox.showerror("Error", "No se encuentra la unidad G:")
        return 

    #Lee la base de datos de los colaboradores
    update_progress_bar(1,"1/8 leyendo base de datos...",barra_progreso,texto_progreso,ventana_progreso)
    employees = read_database()
    
    #Obtiene el ID del workspace de PEDELTA-COLOMBIA
    update_progress_bar(2,"2/8 extrayendo espacio de trabajo...",barra_progreso,texto_progreso,ventana_progreso)
    workspace_ID = get_workspace_id()

    #Obtiene los proyectos
    update_progress_bar(3,"3/8 obteniendo proyectos...",barra_progreso,texto_progreso,ventana_progreso)
    projects = get_projects(workspace_ID)

    #Obtiene todos los registros entre las fechas establecidas
    update_progress_bar(4,"4/8 extrayendo registros...",barra_progreso,texto_progreso,ventana_progreso)
    records = get_records(fecha_inicio,fecha_fin,workspace_ID)

    #convierte todos los correos que estén en mayuscula a minuscula
    update_progress_bar(5,"5/8 parseando correos...",barra_progreso,texto_progreso,ventana_progreso)
    for i in range(len(employees["CORREOS"])):
        if employees["CORREOS"][i].islower():
            pass
        else:
            employees["CORREOS"][i] = employees["CORREOS"][i].lower()
    
    #Obtener todo como un dataframe
    update_progress_bar(6,"6/8 convirtiendo registros en dataframe...",barra_progreso,texto_progreso,ventana_progreso)
    dataframe = convert_dataframe(records,employees,fecha_inicio,fecha_fin,projects)

    #Asigna el nombre del prorrateo
    update_progress_bar(7,"7/8 asignando nombre a reporte...",barra_progreso,texto_progreso,ventana_progreso)
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
    update_progress_bar(8,"8/8 escribiendo el reporte...",barra_progreso,texto_progreso,ventana_progreso)
    time.sleep(3)
    write_excel(dataframe)

    #Genera el log
    ventana_progreso.destroy()
    tkinter.messagebox.showinfo("Éxito", "Se ha creado el reporte con éxito.")
    
    



    

    
    
    

