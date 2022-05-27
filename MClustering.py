
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb #Biblioteca para visualizacion de datos basado en matplotlib
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from kneed import KneeLocator
from mpl_toolkits.mplot3d import Axes3D

ListaParametros=[]
IndicesUsuario=[]

def OpClustering(rutaArchivo):
	#Borrando parametros
	for i in range(len(ListaParametros)):
		ListaParametros.pop()
	#Borrando parametros
	for i in range(len(IndicesUsuario)):
		IndicesUsuario.pop()
	datos = pd.read_csv(rutaArchivo) #Conseguimos ruta
	Matriz= datos.corr(method='pearson') #Expresado en matriz por pearson

	ListaOpciones=[]
	for columna in Matriz.columns:
		ListaOpciones.append(columna)

	VentanaCluster=tk.Tk()
	VentanaCluster.title("Clustering")
	VentanaCluster.geometry("800x500")

	#SECCION MATRIZ DE CORRELACION
	FramePearson= tk.LabelFrame(VentanaCluster, text="Matriz")
	FramePearson.place(height=240,width=780,rely=0.50,relx=0)

	#Treeview para la vista del archivo csv
	tablaCluster = ttk.Treeview(FramePearson)
	tablaCluster.place(relheight=1, relwidth=1)
	tablascrolly = tk.Scrollbar(tablaCluster, orient="vertical", command=tablaCluster.yview) # command means update the yaxis view of the widget
	tablascrollx = tk.Scrollbar(tablaCluster, orient="horizontal", command=tablaCluster.xview) # command means update the xaxis view of the widget
	tablaCluster.configure(xscrollcommand=tablascrollx.set, yscrollcommand=tablascrolly.set) # assign the scrollbars to the Treeview Widget
	tablascrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
	tablascrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget

	#SECCION MATRIZ DE CORRELACION
	FrameParametros= tk.LabelFrame(VentanaCluster, text="Selección de Parámetros")
	FrameParametros.place(height=230,width=780,rely=0.0,relx=0)

	ElegirOpcion= ttk.Combobox(FrameParametros)
	ElegirOpcion.place(relx=0.1,rely=0.1)
	ElegirOpcion['values']=ListaOpciones

	buttonAgregar = tk.Button(FrameParametros, text="Agregar", command=lambda: agregar(ElegirOpcion,FrameParametros,datos))
	buttonAgregar.place(relx=0.5,rely=0.08)
	buttonLimpiar = tk.Button(FrameParametros, text="Limpiar", command=lambda: limpiar(ElegirOpcion,FrameParametros))
	buttonLimpiar.place(relx=0.8,rely=0.08)


	labelN_Cluster = ttk.Label(FrameParametros, text="Numero de Clusters", font=("Helvetica", 9 ))
	labelN_Cluster.place(relx=0.05,rely=0.6)
	ElegirN_Cluster= ttk.Combobox(FrameParametros)
	ElegirN_Cluster.place(relx=0.3,rely=0.6)
	ElegirN_Cluster['values']=[2,3,4,5,6,7,8,9,10,11,12,13,14,15]

	buttonCluster = tk.Button(FrameParametros, text="Cluster",font=("Helvetica",11), command=lambda: cluster(ListaParametros,datos,ElegirN_Cluster))
	buttonCluster.place(relx=0.6,rely=0.6)


	clear_data(tablaCluster)
	tablaCluster["column"] = list(Matriz.columns)
	tablaCluster["show"] = "headings"

	for column in tablaCluster["columns"]:
		tablaCluster.heading(column, text=column) 

	Matriz_rows = Matriz.to_numpy().tolist() 
	for row in Matriz_rows:
		tablaCluster.insert("", "end", values=row) 
	return None

def clear_data(tablaCluster):
    tablaCluster.delete(*tablaCluster.get_children())
    return None

def agregar(ElegirOpcion,FrameParametros,datos):
	labelParametro = ttk.Label(FrameParametros, text="", font=("Helvetica", 9 ))
	labelParametro.place(relx=0.05,rely=0.4)

	if (str(ElegirOpcion.get()) not in ListaParametros):
		ListaParametros.append( ElegirOpcion.get() )
	if( len(ListaParametros)>2 ):
		funcionCodo(ListaParametros,datos,FrameParametros)
	labelParametro = ttk.Label(FrameParametros, text=str(ListaParametros), font=("Helvetica", 9 ))
	labelParametro.place(relx=0.05,rely=0.4)

def limpiar(ElegirOpcion,FrameParametros):
	labelParametro = ttk.Label(FrameParametros, text="", font=("Helvetica", 9 ))
	
	#Borrando parametros
	for i in range(len(ListaParametros)):
		ListaParametros.pop()

	labelParametro = ttk.Label(FrameParametros, text=str(ListaParametros), font=("Helvetica", 9 ))
	labelParametro.place(relx=0.05,rely=0.4)

def funcionCodo(ListaParametros,datos,FrameParametros):
	#En una lista agregamos columnas
	ListaColumnas=[]
	for i in datos.columns:
		ListaColumnas.append(i)

    #Lista para obtener indices que solicitó usuario
	for elemento in ListaParametros:
		IndicesUsuario.append(ListaColumnas.index(elemento))

	labelParametro = ttk.Label(FrameParametros, text="", font=("Helvetica", 9 ))
	labelParametro.place(relx=0.05,rely=0.2)

	#
	VariablesModelo=datos.iloc[:,IndicesUsuario].values
	#Funcion Codo
	SSE = []
	for i in range(2, 16):
	    km = KMeans(n_clusters=i, random_state=0)
	    km.fit(VariablesModelo)
	    SSE.append(km.inertia_)
	
	kl = KneeLocator(range(2, 16), SSE, curve="convex", direction="decreasing")

	labelParametro = ttk.Label(FrameParametros, text="Cluster Sugeridos "+str(kl.elbow), font=("Helvetica", 9 ))
	labelParametro.place(relx=0.05,rely=0.2)


def cluster(ListaParametros,datos,ElegirN_Cluster):

	VariablesModelo=datos.iloc[:,IndicesUsuario].values
	tamanoCluster=int(ElegirN_Cluster.get())

	#Se crean los clusters 
	#random_state se utiliza para inicializar el generador interno de números aleatorios (mismo resultado)
	MParticional = KMeans(n_clusters=tamanoCluster, random_state=0).fit(VariablesModelo)

	datos['clusterP'] = MParticional.labels_

	CentroidesP = MParticional.cluster_centers_

	# Gráfica de los elementos y los centros de los clusters	
	plt.rcParams['figure.figsize'] = (10, 7)
	plt.style.use('ggplot')
	coloresTotal=['red', 'blue', 'cyan', 'green', 'yellow','black','orange','pink','brown','purple','grey','golden']
	colores=coloresTotal[0:tamanoCluster]
	#colores=['red', 'blue', 'cyan', 'green', 'yellow']
	asignar=[]
	for row in MParticional.labels_:
	    asignar.append(colores[row])

	fig = plt.figure()
	ax = Axes3D(fig)
	ax.scatter (VariablesModelo[:, 0], VariablesModelo[:, 1], VariablesModelo[:, 2], marker='o', c=asignar, s=60)
	ax.scatter(CentroidesP[:, 0], CentroidesP[:, 1], CentroidesP[:, 2], marker='*', c=colores, s=1000)
	plt.show()


