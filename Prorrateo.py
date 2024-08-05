"""
CREATED BY: KA
"""

import subprocess
import os

a = os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")
subprocess.call(["pip", "install", "-r", a])

#Importa librerias
from customtkinter import *
from datetime import datetime, date
from PIL import Image, ImageTk
import re
import tkinter
from f_generar_reporte import f_generar_reporte
import pickle


global fecha_inicio, fecha_fin, Entry_FechaInicio, Entry_FechaFin, main_window, Boton_Reporte, Boton_Agregar, add_window, Entry_identificación, identificacion, primer_nombre, Entry_nombre1, segundo_nombre, Entry_nombre2, primer_apellido, Entry_apellido1, segundo_apellido, Entry_apellido2, Entry_correo, correo, Boton_Agregar_OK,Boton_Volver, bd_path
bd_path = "BD_PATH"


#%% -------- VERIFICAR FECHA INICIO ------------
def verificar_fecha_inicio():
    
    global fecha_inicio

    fecha_inicio = Entry_FechaInicio.get()

    if re.match(r"^\d{4}-\d{2}-\d{2}$", fecha_inicio):
        try:
            datetime.strptime(fecha_inicio, '%Y-%m-%d')
        except ValueError:
            mensaje_alerta = "El mes debe estar entre 1 y 12.\nEl día debe estar entre 1 y 31."
            titulo_alerta = "Error: Fecha de inicio"
            nombre_ico = "Error.ico"
            x_place_button, y_place_button =180, 65
            x_place_text, y_place_text =110, 20
            command = [f"Entry_FechaInicio.delete(0,\"end\")"]
            generar_ventana_alerta(mensaje_alerta,titulo_alerta,nombre_ico,x_place_text, y_place_text,x_place_button, y_place_button,command)
    elif fecha_inicio == "":
        pass
    else:
        mensaje_alerta = "Se espera el formato de fecha aaaa-mm-dd.\nPor ejemplo: 2022-12-19."
        titulo_alerta = "Error: Fecha de inicio"
        nombre_ico = "Error.ico"
        x_place_button, y_place_button =180, 65
        x_place_text, y_place_text =70, 20
        command = [f"Entry_FechaInicio.delete(0,\"end\")"]
        generar_ventana_alerta(mensaje_alerta,titulo_alerta,nombre_ico,x_place_text, y_place_text,x_place_button, y_place_button,command)
        fecha_inicio = ""

#%% ------------ VERIFICAR FECHA FIN ------------
def verificar_fecha_fin():
    
    global fecha_fin

    fecha_fin = Entry_FechaFin.get()

    if re.match(r"^\d{4}-\d{2}-\d{2}$", fecha_fin):
        try:
            datetime.strptime(fecha_fin, '%Y-%m-%d')
        except ValueError:
            mensaje_alerta = "El mes debe estar entre 1 y 12.\nEl día debe estar entre 1 y 31."
            titulo_alerta = "Error: Fecha fin"
            nombre_ico = "Error.ico"
            x_place_button, y_place_button =180, 65
            x_place_text, y_place_text =110, 20
            command = [f"Entry_FechaFin.delete(0,\"end\")"]
            generar_ventana_alerta(mensaje_alerta,titulo_alerta,nombre_ico,x_place_text, y_place_text,x_place_button, y_place_button,command)
            fecha_fin = ""
    elif fecha_fin == "":
        pass
    else:
        mensaje_alerta = "Se espera el formato de fecha aaaa-mm-dd.\nPor ejemplo: 2022-12-19."
        titulo_alerta = "Error: Fecha fin"
        nombre_ico = "Error.ico"
        x_place_button, y_place_button =180, 65
        x_place_text, y_place_text =70, 20
        command = [f"Entry_FechaFin.delete(0,\"end\")"]
        generar_ventana_alerta(mensaje_alerta,titulo_alerta,nombre_ico,x_place_text, y_place_text,x_place_button, y_place_button,command)
        fecha_fin = ""
        
    if fecha_fin != "" and fecha_inicio !="":

        if (datetime.strptime(fecha_fin, "%Y-%m-%d") - datetime.strptime(fecha_inicio, "%Y-%m-%d")).days < 0:
            mensaje_alerta = "La fecha fin debe ser mayor que la fecha de inicio."
            titulo_alerta = "Error: Fecha fin"
            nombre_ico = "Error.ico"
            x_place_button, y_place_button =180, 65
            x_place_text, y_place_text =55, 20
            command = [f"Entry_FechaFin.delete(0,\"end\")"]
            generar_ventana_alerta(mensaje_alerta,titulo_alerta,nombre_ico,x_place_text, y_place_text,x_place_button, y_place_button,command)

#%% ------------ GENERAR VENTANA ALERTA ------------
def generar_ventana_alerta(mensaje_alerta:str,titulo_alerta:str,nombre_ico:str,x_place_text:int,y_place_text:int,x_place_button:int,y_place_button:int,command:list):

    #Creación de ventana
    alerta = CTkToplevel()
    #Nombre de la ventana
    alerta.title(titulo_alerta)
    #Resizable
    alerta.resizable(False,False)
    alerta.transient(main_window)
    alerta.grab_set()
    #icono
    alerta.after(201, lambda :alerta.iconbitmap(os.path.join(images_path,nombre_ico )))
    #Geometría
    width = 400
    height = 100
    screen_width = alerta.winfo_screenwidth()
    screen_height = alerta.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    alerta.geometry(f"{width}x{height}+{x}+{y}")
    #Label de aviso
    Label1_window_alert1 = CTkLabel(master=alerta,text=mensaje_alerta,font=('Gothic A1',13))
    Label1_window_alert1.place(x=x_place_text,y=y_place_text)
    #Botón de ok
    OKBoton_window_alert1 = CTkButton(master= alerta, text="OK", width=40, height=20, compound="left",font=('Gothic A1',15), command=alerta.destroy)
    OKBoton_window_alert1.place(x=x_place_button,y=y_place_button)
    for line in command:
        try:
            eval(line)
        except SyntaxError:
            pass

#%% ------------ GENERAR VENTANA LOG GENERAR REPORTE ------------
def generar_ventana_log_reporte():

    def abrir_excel():
        
        #Obtiene el nombre del archivo
        with open(os.path.join(os.path.expanduser("~\\Documents"),"generar_reporte.log"),"r") as f:
            line = f.read()
        f.close()

        #Destruye la ventana del log y abre el archivo de excel
        window_logs.destroy()
        full_path = os.path.join(os.path.expanduser("~\\Documents"),line)
        os.system(f'start excel "{full_path}"')
        Boton_Reporte.configure(state=tkinter.NORMAL)

    #Creación de progreso
    window_logs = CTkToplevel()
    #Nombre de la ventana
    window_logs.title("Éxito")
    #Resizable
    window_logs.resizable(False,False)
    window_logs.transient(main_window)
    window_logs.grab_set()
    #Geometría
    width = 200
    height = 90
    screen_width = window_logs.winfo_screenwidth()
    screen_height = window_logs.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window_logs.geometry(f"{width}x{height}+{x}+{y}")
    #Ícono ventana
    window_logs.after(201, lambda :window_logs.iconbitmap(os.path.join(images_path, "exito.ico")))
    #Label
    label_log = CTkLabel(master=window_logs,text=f"Reporte generado con éxito.",font=('Gothic A1',13))
    label_log.place(x=20,y=18)
    #Botón de ok
    OKBoton_window_log = CTkButton(master= window_logs, text="OK", width=40, height=20, compound="left",font=('Gothic A1',15), command=abrir_excel)
    OKBoton_window_log.place(x=80,y=55)
    
#%% ------------ GENERAR VENTANA PROGRESO GENERAR REPORTE ------------
def generar_ventana_progreso_generar_reporte(main_window):
    
    #Creación de progreso
    progress_window = CTkToplevel()
    #Nombre de la ventana
    progress_window.title("Generando reporte")
    #Resizable
    progress_window.resizable(False,False)
    progress_window.transient(main_window)
    progress_window.grab_set()
    #Geometría
    width = 400
    height = 50
    screen_width = progress_window.winfo_screenwidth()
    screen_height = progress_window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    progress_window.geometry(f"{width}x{height}+{x}+{y}")
    #Ícono ventana
    progress_window.after(2, lambda :progress_window.iconbitmap(os.path.join(images_path, "reporte.ico")))
    #Barra de progreso
    progressbar1 = CTkProgressBar(master=progress_window, orientation="horizontal",mode="indeterminate",width=360,height=10, progress_color="green",indeterminate_speed=1.5)
    progressbar1.place(x=20,y=20)
    progressbar1.start()

    def destruir_ventana_progreso():

        lista_archivos = os.listdir(os.path.expanduser("~\\Documents"))
        if "generar_reporte.log" in lista_archivos:
            
            progress_window.after(1000, progress_window.destroy)  # Cierra la ventana después de 1 segundo
            generar_ventana_log_reporte()
        else:
            progress_window.after(1000, destruir_ventana_progreso)  # Verifica nuevamente después de 1 segundo

    destruir_ventana_progreso()

#%% ------------ HABILITAR BOTÓN DE GENERAR REPORTE ------------
def habilitar_boton_generar_reporte():

    global Boton_Reporte

    if fecha_inicio and fecha_fin:
        
        Boton_Reporte.configure(state=tkinter.NORMAL)
    else:
        Boton_Reporte.configure(state=tkinter.DISABLED)


#%% ------------ GENERAR REPORTE ------------
def generar_reporte():

    #Elimina los logs 
    lista_archivos = os.listdir(os.path.expanduser("~\\Documents"))
    if "generar_reporte.log" in lista_archivos:
        os.remove(os.path.join(os.path.expanduser("~\\Documents"),"generar_reporte.log"))

    #Verifica si existe el archivo
    if os.path.exists(bd_path):
        if "BD_FILE.xlsx" not in os.listdir(bd_path):
            mensaje_alerta = "El archivo de la base de datos no existe."
            titulo_alerta = "Error"
            nombre_ico = "Error.ico"
            x_place_button, y_place_button =180, 65
            x_place_text, y_place_text =80, 20
            command = []
            generar_ventana_alerta(mensaje_alerta,titulo_alerta,nombre_ico,x_place_text,y_place_text,x_place_button,y_place_button,command)
        else:

            #Bloquea el botón 
            Boton_Reporte.configure(state=tkinter.DISABLED)

            def ejecutar_tarea():
                f_generar_reporte(fecha_inicio,fecha_fin,bd_path)

            #Ejecuta la transferencia de horas
            main_window.after(100,ejecutar_tarea)
            generar_ventana_progreso_generar_reporte(main_window)

    else:
        mensaje_alerta = "La ruta de almacenamiento de la base de datos\nno existe."
        titulo_alerta = "Error"
        nombre_ico = "Error.ico"
        x_place_button, y_place_button =180, 65
        x_place_text, y_place_text =65, 20
        command = []
        generar_ventana_alerta(mensaje_alerta,titulo_alerta,nombre_ico,x_place_text,y_place_text,x_place_button,y_place_button,command)
    
    

"""
INTERFAZ GRÁFICA
"""
#Inicializa la ventana
main_window = CTk()
#Geometría
# width = 350
# height = 220
width = 350
height = 180
screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()
x = (screen_width - width) // 5
y = (screen_height - height) // 4
main_window.geometry(f"{width}x{height}+{x}+{y}")
#Nombre de la ventana
main_window.title("Prorrateo: Clockify")
#Resizable
main_window.resizable(False,False)
#Tema de la ventana
set_appearance_mode("Dark")
set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
#Ícono ventana
images_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "WindowsImages")
main_window.after(201, lambda :main_window.iconbitmap(os.path.join(images_path, "logo.ico")))
# #Logo de EMPRESA
logo_image = CTkImage(Image.open(os.path.join(images_path, "EMPRESA.png")), size=(220, 80))
logo_label = CTkLabel(master=main_window,image=logo_image,text="",compound="center",fg_color="transparent")
logo_label.place(x=82, y=5)
#Label fecha de inicio
Fecha_inicio_label = CTkLabel(master=main_window,text="Fecha inicio",font=('Gothic A1',15) )
Fecha_inicio_label.place(x=50,y=70)
#Label fecha fin
Fecha_inicio_label = CTkLabel(master=main_window,text="Fecha fin",font=('Gothic A1',15) )
Fecha_inicio_label.place(x=205,y=70)
#Entry para fecha de inicio
fecha_inicio = ""
Entry_FechaInicio=CTkEntry(master=main_window, width=100, placeholder_text='aaaa-mm-dd')
Entry_FechaInicio.place(x=50, y=100)
Entry_FechaInicio.bind("<Leave>", lambda event: verificar_fecha_inicio())
#Entry para fecha de inicio 
fecha_fin = ""
Entry_FechaFin=CTkEntry(master=main_window, width=100, placeholder_text='aaaa-mm-dd')
Entry_FechaFin.place(x=205, y=100)
Entry_FechaFin.bind("<Leave>", lambda event: verificar_fecha_fin())
#Botón de ok
Boton_Reporte = CTkButton(master= main_window, text="Generar reporte", width=40, height=20, compound="left",font=('Gothic A1',13), command=generar_reporte,state=tkinter.DISABLED)
Boton_Reporte.place(x=125,y=145)
#Habilitar botón
Entry_FechaInicio.bind("<Leave>", lambda event: habilitar_boton_generar_reporte())
Entry_FechaFin.bind("<Leave>", lambda event: habilitar_boton_generar_reporte())
#Botón agregar colaborador
# Boton_Agregar = CTkButton(master= main_window, text="Agregar colaborador", width=40, height=20, compound="left",font=('Gothic A1',13), command=generar_ventana_agregar_colaborador)
# Boton_Agregar.place(x=30,y=180)

#Ejecuta la ventana
main_window.mainloop()

