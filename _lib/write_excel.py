import xlwings as wx
import os

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