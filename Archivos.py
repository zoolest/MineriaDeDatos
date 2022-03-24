#@Autor: Amezaga Campos Salvador
#@Avance Proyecto Minería de Datos
#@Lectura de Archivos

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd 
import numpy as np

Transacciones=[]

#Indicas ruta del archivo a utilizar
def AbrirArch(labelArchivo):
	nombreArchivo= filedialog.askopenfilename(
		initialdir="Archivos_CSV/",	#Ruta inicial donde empiezas a buscar
		title="Selecciona un archivo", #Nombre de instruccion
		filetype=(("All Files", "*.*"),("xlsx files", "*.xlsx"))	#Tipos de archivos que puedes abrir
		)
	labelArchivo["text"]= nombreArchivo
	return None

#Muestra el archivo xlsx o csv en la ventana
def CargarArch(labelArchivo,tabla):
    rutaArchivo = labelArchivo["text"]
    try:
        nombreArchivo = r"{}".format(rutaArchivo)
        if nombreArchivo[-4:] == ".csv":
            df = pd.read_csv(nombreArchivo,header=None) #No debe tener headers
        else:
            df = pd.read_excel(nombreArchivo)
    #Errores de función
    except ValueError:
        tk.messagebox.showerror("Informacion", "El archivo no tiene el formato requerido")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Informacion", f"Archivo no encontrado ")
        return None

    clear_data(tabla)
    tabla["column"] = list(df.columns)
    tabla["show"] = "headings"

    for column in tabla["columns"]:
        tabla.heading(column, text=column) # let the column heading = column name

    df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tabla.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
    return None


def clear_data(tabla):
    tabla.delete(*tabla.get_children())
    return None