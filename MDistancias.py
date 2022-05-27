#@Autor: Amezaga Campos Salvador
#@Avance Proyecto Minería de Datos

#Seleccionar dos renglones
#Que el usuario especifica los 4 tipos de metricas

#Librerias utilizadas
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from math import sqrt
from scipy.spatial import distance

ListaOpciones=[]

def OpDistancias(rutaArchivo):
	datos = pd.read_csv(rutaArchivo) #Lee archivo
	Renglones=datos.values.tolist()
	#Borrando parametros
	for i in range(len(ListaOpciones)):
		ListaOpciones.pop()
	
	for elemento in range(len(Renglones)):
		ListaOpciones.append(str( Renglones[elemento][0]) )
	
	VentanaMetricas=tk.Tk()
	VentanaMetricas.title("Algoritmos de Distancias")
	VentanaMetricas.geometry("850x600")

	#SECCION MATRIZ DE CORRELACION
	FrameMetricas= tk.LabelFrame(VentanaMetricas, text="Data seleccionada")
	#FrameMetricas.place(height=300,width=840,rely=0,relx=0)
	FrameMetricas.place(height=300,width=840,rely=0.12,relx=0)

	#Treeview para la vista del archivo csv
	tablaMetricas = ttk.Treeview(FrameMetricas)
	tablaMetricas.place(relheight=1, relwidth=1)
	tablascrolly = tk.Scrollbar(tablaMetricas, orient="vertical", command=tablaMetricas.yview) # command means update the yaxis view of the widget
	tablascrollx = tk.Scrollbar(tablaMetricas, orient="horizontal", command=tablaMetricas.xview) # command means update the xaxis view of the widget
	tablaMetricas.configure(xscrollcommand=tablascrollx.set, yscrollcommand=tablascrolly.set) # assign the scrollbars to the Treeview Widget
	tablascrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
	tablascrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget

	#SECCION Seleccionar
	FrameOpciones= tk.LabelFrame(VentanaMetricas, text="Selección de parametros")
	#FrameOpciones.place(height=70,width=840,rely=0.50,relx=0)
	FrameOpciones.place(height=70,width=840,rely=0,relx=0)

	labelParametro1 = ttk.Label(FrameOpciones, text="Parametro1", font=("Helvetica", 9 ))
	labelParametro1.place(relx=0.25,rely=0.05)
	ListaX= ttk.Combobox(FrameOpciones)
	ListaX.place(relx=0.21,rely=0.4)
	ListaX['values']=ListaOpciones

	labelParametro2 = ttk.Label(FrameOpciones, text="Parametro2", font=("Helvetica", 9 ))
	labelParametro2.place(relx=0.5,rely=0.05)
	ListaY= ttk.Combobox(FrameOpciones)
	ListaY.place(relx=0.46,rely=0.4)
	ListaY['values']=ListaOpciones

	buttonSubmit = tk.Button(FrameOpciones, text="Calcular", command=lambda: calculos(datos,ListaX,ListaY,FrameValores) )
	buttonSubmit.place(relx=0.75,rely=0.06)

	#SECCION VALORES
	FrameValores= tk.LabelFrame(VentanaMetricas, text="Resultados")
	#FrameValores.place(height=200,width=840,rely=0.62,relx=0)
	FrameValores.place(height=200,width=840,rely=0.62,relx=0)

	labelEuclidiana = ttk.Label(FrameValores, text="Euclidiana", font=("Helvetica", 9 ))
	labelEuclidiana.place(relx=0.1,rely=0.65)
	labelChebyshev = ttk.Label(FrameValores, text="Chebyshev", font=("Helvetica", 9 ))
	labelChebyshev.place(relx=0.1,rely=0.2)
	labelManhattan = ttk.Label(FrameValores, text="Manhattan", font=("Helvetica", 9 ))
	labelManhattan.place(relx=0.53,rely=0.65)
	labelMinkowski = ttk.Label(FrameValores, text="Minkowski", font=("Helvetica", 9 ))
	labelMinkowski.place(relx=0.53,rely=0.2)

	


	clear_data(tablaMetricas)
	tablaMetricas["column"] = list(datos.columns)
	tablaMetricas["show"] = "headings"

	for column in tablaMetricas["columns"]:
		tablaMetricas.heading(column, text=column) 

	datos_rows = datos.to_numpy().tolist() 
	for row in datos_rows:
		tablaMetricas.insert("", "end", values=row) 
	return None

def clear_data(tablaMetricas):
    tablaMetricas.delete(*tablaMetricas.get_children())
    return None

def calculos(datos,ListaX,ListaY,FrameValores):
	labelR_Euclidiana = ttk.Label(FrameValores, text="", font=("Helvetica", 9 ))
	labelR_Euclidiana.place(relx=0.3,rely=0.2)
	labelR_Chebyshev = ttk.Label(FrameValores, text="", font=("Helvetica", 9 ))
	labelR_Chebyshev.place(relx=0.3,rely=0.65)
	labelR_Manhattan = ttk.Label(FrameValores, text="", font=("Helvetica", 9 ))
	labelR_Manhattan.place(relx=0.73,rely=0.2)
	labelR_Minkowski = ttk.Label(FrameValores, text="",background="red",font=("Helvetica", 9 ))
	labelR_Minkowski.place(relx=0.73,rely=0.65)

	Renglones=datos.values.tolist()
	indice1 =ListaOpciones.index(str(ListaX.get()))
	indice2 =ListaOpciones.index(str(ListaY.get()))

	Renglon1=Renglones[indice1][1:]
	Renglon2=Renglones[indice2][1:]

	#Euclidiana
	Met1_EU=np.array(Renglon1)
	Met2_EU=np.array(Renglon2)
	Res_EU=np.sqrt(np.sum((Met1_EU-Met2_EU)**2))

	#Chebyshev
	Res_Che=distance.chebyshev(Renglon1,Renglon2)

	#Manhattan
	Res_Man=distance.cityblock(Renglon1,Renglon2)

	#Minkowski
	Res_Min=distance.minkowski(Renglon1,Renglon2)


	labelR_Euclidiana = ttk.Label(FrameValores, text=str(Res_EU), font=("Helvetica", 9 ))
	labelR_Euclidiana.place(relx=0.3,rely=0.2)
	labelR_Chebyshev = ttk.Label(FrameValores, text=str(Res_Che), font=("Helvetica", 9 ))
	labelR_Chebyshev.place(relx=0.3,rely=0.65)
	labelR_Manhattan = ttk.Label(FrameValores, text=str(Res_Man), font=("Helvetica", 9 ))
	labelR_Manhattan.place(relx=0.73,rely=0.2)
	labelR_Minkowski = ttk.Label(FrameValores, text=str(Res_Min),font=("Helvetica", 9 ))
	labelR_Minkowski.place(relx=0.73,rely=0.65)