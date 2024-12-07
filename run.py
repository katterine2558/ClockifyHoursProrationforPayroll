"""
VENTANA PRINCIPAL
"""
#############################
#     IMPORTAR Y DECLARAR
#############################

#Importa librerías
import subprocess
import os
import sys
from datetime import datetime

sys.path.append(os.getcwd())

if "requirements.log" not in os.listdir(os.path.dirname(os.path.realpath(sys.argv[0]))):
    subprocess.call(["pip", "install", "-r", 
                    os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                    "requirements.txt")])
    with open(os.path.dirname(os.path.realpath(sys.argv[0]))+"\\requirements.log","w") as f:
        print("lo creó")
        f.write("")
    f.close()

from customtkinter import *
from PIL import Image, ImageTk
import tkinter
from _lib.generate_report import f_generate_report

#############################
#           FUNCIONES
#############################
# CENTRAR BOTONES
def f_center_button(window, button, pos_y):

    # Espera a que la ventana y el botón se dibujen antes de obtener su tamaño
    window.update_idletasks()
    # Obtener dimensiones de la ventana y el botón
    window_width = window.winfo_width()
    button_width = button.winfo_reqwidth()
    # Calcular posiciones X e Y para centrar
    center_x = (window_width - button_width) // 2
    # Colocar el botón en la posición centrada
    button.place(x=center_x, y=pos_y)

# VERIFICACIÓN FECHAS
def verificacion_fechas(fecha_inicio,fecha_fin):

    # Formato aaaa-mm-dd
    formato = "%Y-%m-%d"  

    # Verificar que las fechas tengan el formato correcto y sean fechas reales
    try:
        # Intentar convertir las fechas a objetos datetime
        fecha_inicio_dt = datetime.strptime(fecha_inicio, formato)
        fecha_fin_dt = datetime.strptime(fecha_fin, formato)
    except ValueError:
        return False, "Formato de fecha inválido o fecha inexistente."
    
     # Verificar que fecha_fin no sea menor que fecha_inicio
    if fecha_fin_dt < fecha_inicio_dt:
        return False, "La fecha de fin no puede ser menor que la fecha de inicio."
    
    return True, ""

# CREAR VENTANA DE PROGRESO DEL REPORTE
def create_progress_window():

    # Crear una nueva ventana de progreso
    ventana_progreso = tkinter.Toplevel()
    ventana_progreso.title("Generando reporte...")
    ventana_progreso.resizable(False, False)
    width = 400
    height = 100
    screen_width = ventana_progreso.winfo_screenwidth()
    screen_height = ventana_progreso.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    ventana_progreso.geometry(f"{width}x{height}+{x}+{y}")
    ventana_progreso.iconbitmap(os.path.join(images_path, "notas.ico"))  
    
    # Ventana esté encima de la ventana principal
    ventana_progreso.lift()
    ventana_progreso.attributes('-topmost', True)  
    ventana_progreso.after(100, lambda: ventana_progreso.attributes('-topmost', False))  

    #Crear la barra de progreso en la nueva ventana
    barra_progreso = CTkProgressBar(master=ventana_progreso, 
                                    width=350,
                                    progress_color="green")
    barra_progreso.set(0)
    barra_progreso.pack(pady=20)

    # Crear texto de progreso
    texto_progreso = tkinter.StringVar(value="0/8 conectándose al módulo...")
    label_progreso = CTkLabel(master=ventana_progreso, 
                              textvariable=texto_progreso,
                              text_color="black", 
                              bg_color='white',
                              font=('Gothic A1',15))
    label_progreso.pack(pady=2)

    #Actualiza la ventana
    ventana_progreso.update_idletasks()

    # Retornar los elementos necesarios para actualizar el progreso
    return ventana_progreso, barra_progreso, texto_progreso

#GENERAR REPORTE
def generar_reporte():

    # Obtener los valores de las fechas
    fecha_inicio = entry_fecha_inicio.get()
    fecha_fin = entry_fecha_fin.get()

    #Verifica las fechas
    verificacion, mensaje = verificacion_fechas(fecha_inicio,fecha_fin)
    if verificacion == False:
        tkinter.messagebox.showerror("Error", mensaje)
    else:
        #Ventana de progreso
        ventana_progreso, barra_progreso, texto_progreso = create_progress_window()
        #Genera el reporte
        f_generate_report(ventana_progreso, barra_progreso, texto_progreso,fecha_inicio,fecha_fin)
        
#############################
#     VENTANA PRINCIPAL
#############################
#Inicializa la ventana
main_window= CTk()
#Geometría
width = 300
height = 180
screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()
x = (screen_width - width) // 2
y = (screen_height - height) // 2
main_window.geometry(f'{width}x{height}+{x}+{y}')
#Nombre de la ventana
main_window.title("Prorrateo Clockify")
#Resizable
main_window.resizable(False,False)
#Tema de la ventana
set_appearance_mode("Dark")
set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
#Ícono ventana
images_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "_images")
main_window.after(201, lambda :main_window.iconbitmap(os.path.join(images_path, "logo.ico")))
#ENTRY FECHA INICIAL 
fecha_inicio_label = CTkLabel(master=main_window,text="Fecha inicio",font=('Gothic A1',15) )
fecha_inicio_label.place(x=35,y=25)
entry_fecha_inicio=CTkEntry(master=main_window, width=100, placeholder_text='aaaa-mm-dd')
entry_fecha_inicio.place(x=35, y=55)
#ENTRY FECHA FINAL 
fecha_inicio_label = CTkLabel(master=main_window,text="Fecha fin",font=('Gothic A1',15) )
fecha_inicio_label.place(x=175,y=25)
entry_fecha_fin=CTkEntry(master=main_window, width=100, placeholder_text='aaaa-mm-dd')
entry_fecha_fin.place(x=175, y=55)

#BOTON MEMORIA DE CÁLCULO
reporte_image = Image.open(os.path.join(images_path, "notas.png"))
reporte_image = reporte_image.resize((30, 30), Image.LANCZOS)
reporte_image_tk = ImageTk.PhotoImage(reporte_image)
reporte_image= CTkButton(master=main_window, 
                    text="Generar reporte", 
                    image = reporte_image_tk,
                    width=180, 
                    height=40, 
                    compound="left",
                    font=('Gothic A1',15),
                    fg_color="#3A3A3A",
                    hover_color="#4C4C4C",
                    text_color="#E0E0E0",
                    corner_radius=5,
                    border_width=2,
                    border_color="#606060",
                    command=generar_reporte) 
f_center_button(main_window, reporte_image, 115)

#Ejecuta la ventana
main_window.mainloop()