
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import pandas as pd 
import numpy as np
from apyori import apriori

import Archivos

Transacciones = []

def OpReglas(rutaArchivo):
	datos = pd.read_csv(rutaArchivo,header=None)

	for fila in range(len(datos)):
		Transacciones.append([str(datos.values[fila,columna]) for columna in range(len(datos.columns))])

	sSupport = DoubleVar()
	sConfidence = DoubleVar()
	sLift= DoubleVar()

	VentanaApriori=tk.Tk()
	VentanaApriori.title("Reglas de asociación")
	VentanaApriori.geometry("350x350")

	#SECCION PARAMETROS
	parametros= tk.LabelFrame(VentanaApriori, text="Parámetros")
	parametros.place(height=125,width=275,rely=0,relx=0)

	#Especifica a que sección pertenece cada Spin
	labelSupport = ttk.Label(parametros, text="Support", font=("Helvetica", 10 ))
	labelSupport.place(rely=0, relx=0)

	labelConfidence = ttk.Label(parametros, text="Confidence", font=("Helvetica", 10 ))
	labelConfidence.place(rely=0.32, relx=0)

	labelLift = ttk.Label(parametros, text="Lift", font=("Helvetica", 10 ))
	labelLift.place(rely=0.68, relx=0)

	#Spin para metodo apriori
	sSupport = Spinbox(parametros, from_=0, to=1, width=6, font=("Helvetica", 10 ),format="%.4f",increment=0.0001)
	sSupport.pack(pady=0,padx=10)

	sConfidence = Spinbox(parametros, from_=0, to=1, width=6, font=("Helvetica", 10 ),format="%.2f",increment=0.01)
	sConfidence.pack(pady=15,padx=10)

	sLift = Spinbox(parametros, from_=2, to=5, width=5, font=("Helvetica", 10 ))
	sLift.pack(pady=0,padx=10)

	#Registramos los tres numeros anteriores
	buttonSubmit = tk.Button(parametros, text="Submit", command=lambda: OperacionApriori(sSupport,sConfidence,sLift,tablaApriori))
	buttonSubmit.place(rely=0.3, relx=0.7)

	#SECCION  DATAFRAME REGLAS
	FrameApriori= tk.LabelFrame(VentanaApriori, text="Contenido Reglas")
	FrameApriori.place(height=200,width=600,rely=0.40,relx=0)

	#Treeview para la vista del archivo csv
	tablaApriori = ttk.Treeview(FrameApriori)
	tablaApriori.place(relheight=1, relwidth=1)

	tablascrolly = tk.Scrollbar(tablaApriori, orient="vertical", command=tablaApriori.yview) # command means update the yaxis view of the widget
	tablascrollx = tk.Scrollbar(tablaApriori, orient="horizontal", command=tablaApriori.xview) # command means update the xaxis view of the widget
	tablaApriori.configure(xscrollcommand=tablascrollx.set, yscrollcommand=tablascrolly.set) # assign the scrollbars to the Treeview Widget
	tablascrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
	tablascrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget

	

	VentanaApriori.mainloop()

def OperacionApriori(spinSupport,spinConfidence,spinLift,tablaApriori):
	#Reglas = apriori(Archivos.Transacciones, min_support=0.0045, min_confidence=0.2, min_lift=3, min_length=2)

	#Asignamos valores de spin al metodo apriori
	Reglas = apriori(Transacciones, 
		min_support=float(sSupport.get()), 
		min_confidence=float(sConfidence.get()), 
		min_lift=float(sLift.get()), 
		min_length=2)
	
	#RESULTADO
	Resultado = list(Reglas)
	print(len(Resultado))

	#Ordenando los registros para ordenar por valor de
	Reglas=[]
	Soporte=[]
	Lift=[]

	for item in Resultado:
	    pair=item[0]
	    items= [x for x in pair]
	    
	    Reglas.append(str(items[0])+" -> "+str(items[1]))
	    Soporte.append(str(item[2][0][2]))
	    Lift.append(str(item[2][0][3]))

	dic_Resultados= {
    'Regla':Reglas,
    'Soporte':Soporte,
    'Lift':Lift    
	}

	df_Res= pd.DataFrame(dic_Resultados,columns=['Regla','Soporte','Lift'])

	clear_data(tablaApriori)
	tablaApriori["column"] = list(df_Res.columns)
	tablaApriori["show"] = "headings"

	for column in tablaApriori["columns"]:
		tablaApriori.heading(column, text=column) # let the column heading = column name

	df_Res_rows = df_Res.to_numpy().tolist() # turns the dataframe into a list of lists
	for row in df_Res_rows:
		tablaApriori.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
	return None

def clear_data(tablaApriori):
	tablaApriori.delete(*tablaApriori.get_children())
	return None