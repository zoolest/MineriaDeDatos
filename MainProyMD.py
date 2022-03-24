#@Autor: Amezaga Campos Salvador
#@Avance Proyecto Minería de Datos
#@Descripción: INTERFAZ GRAFICA DEL PROYECTO


#Librerias utilizadas
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd 
import numpy as np
import apyori

#Programas externos
import Archivos
import MetodoMetricas

#Ventana Inicial
Inicio= tk.Tk()

Inicio.title("Avance Proyecto Final")	#Titulo Programa
Inicio.geometry("690x520") 			#Dimensiones ventana

#SECCIÓN OPCIONES
seccionOpciones= tk.LabelFrame(Inicio, text="Opciones  ")
seccionOpciones.place(height=90,width=220,rely=0,relx=0.6)



button1 = tk.Button(seccionOpciones, text="Abrir", command=lambda: Archivos.AbrirArch(labelArchivo))
button1.place(rely=0.4, relx=0.20)
button2 = tk.Button(seccionOpciones, text="Cargar", command=lambda: Archivos.CargarArch(labelArchivo,tabla))
button2.place(rely=0.4, relx=0.57)

#Ruta del archivo
labelArchivo = ttk.Label(seccionOpciones, text="No se ha seleccionado ningún archivo")
labelArchivo.place(rely=0, relx=0)

#SECCION METODOS
seccionMetodos= tk.LabelFrame(Inicio, text="Métodos")
seccionMetodos.place(height=90,width=360,rely=0,relx=0.05)

#Metodos
labelMetodos = ttk.Label(seccionMetodos, text="Seleccione el metodo que desea utilizar")
labelMetodos.place(rely=0, relx=0)

button = tk.Button(seccionMetodos, text="Métricas", command=lambda: MetodoMetricas.Metricas(labelArchivo["text"]) )
button.place(rely=0.45, relx=0.39)

#SECCION TABLA ARCHIVO
contenidoArchivo= tk.LabelFrame(Inicio, text="Información del CVS")
contenidoArchivo.place(height=350,width=610,rely=0.20,relx=0.05)

#Treeview para la vista del archivo csv
tabla = ttk.Treeview(contenidoArchivo)
tabla.place(relheight=1, relwidth=1)

tablascrolly = tk.Scrollbar(contenidoArchivo, orient="vertical", command=tabla.yview) # command means update the yaxis view of the widget
tablascrollx = tk.Scrollbar(contenidoArchivo, orient="horizontal", command=tabla.xview) # command means update the xaxis view of the widget
tabla.configure(xscrollcommand=tablascrollx.set, yscrollcommand=tablascrolly.set) # assign the scrollbars to the Treeview Widget
tablascrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
tablascrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget



#Iniciar Programa
Inicio.mainloop()

def File_dialog():
	pass