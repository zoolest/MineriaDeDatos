#@Autor: Amezaga Campos Salvador
#@Avance Proyecto Minería de Datos
#@Descripción: INTERFAZ GRAFICA DEL PROYECTO


#Librerias utilizadas
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd 
import numpy as np
import apyori


import Archivos
import MReglas
import MClustering
import MDistancias
#Ventana Inicial
Inicio= tk.Tk()

Inicio.title("Proyecto Final")	#Titulo Programa
Inicio.geometry("690x520") 			#Dimensiones ventana

#Eqtiqueta de opciones
seccionOpciones= tk.LabelFrame(Inicio, text="Opciones")
seccionOpciones.place(height=90,width=220,rely=0,relx=0.6)



button1 = tk.Button(seccionOpciones, text="Abrir", command=lambda: Archivos.AbrirArch(labelArchivo))
button1.place(rely=0.4, relx=0.20)
button2 = tk.Button(seccionOpciones, text="Cargar", command=lambda: Archivos.CargarArch(labelArchivo,tabla))
button2.place(rely=0.4, relx=0.57)

#Etiqueta de ruta del archivo
labelArchivo = ttk.Label(seccionOpciones, text="Archivo no seleccionado")
labelArchivo.place(rely=0, relx=0)

#Eqtiqueta Metodos
seccionMetodos= tk.LabelFrame(Inicio, text="Metodos")
seccionMetodos.place(height=90,width=360,rely=0,relx=0.05)

#Etiqueta de botones de metodos
labelMetodos = ttk.Label(seccionMetodos, text="Seleccione el metodo que desea utilizar")
labelMetodos.place(rely=0, relx=0)

button3 = tk.Button(seccionMetodos, text="Reglas de asociación", command=lambda: MReglas.OpReglas(labelArchivo["text"]) )
button3.place(rely=0.45, relx=0.05)
button4 = tk.Button(seccionMetodos, text="Clustering", command=lambda: MClustering.OpClustering(labelArchivo["text"]) )
button4.place(rely=0.45, relx=0.43)
button5 = tk.Button(seccionMetodos, text="Distancias", command=lambda: MDistancias.OpDistancias(labelArchivo["text"]) )
button5.place(rely=0.45, relx=0.65)

#Etiueta de datos del archivo
contenidoArchivo= tk.LabelFrame(Inicio, text="CVS Data")
contenidoArchivo.place(height=350,width=610,rely=0.20,relx=0.05)

#Treeview vista del archivo csv
tabla = ttk.Treeview(contenidoArchivo)
tabla.place(relheight=1, relwidth=1)

tablascrolly = tk.Scrollbar(contenidoArchivo, orient="vertical", command=tabla.yview) 
tablascrollx = tk.Scrollbar(contenidoArchivo, orient="horizontal", command=tabla.xview) 
tabla.configure(xscrollcommand=tablascrollx.set, yscrollcommand=tablascrolly.set) 
tablascrollx.pack(side="bottom", fill="x")
tablascrolly.pack(side="right", fill="y")



#Inicio programa
Inicio.mainloop()

def File_dialog():
	pass