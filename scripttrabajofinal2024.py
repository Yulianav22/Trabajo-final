# -*- coding: utf-8 -*-
"""ScriptTrabajoFinal2024.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18qRrVGk1k_3ZeivZxXUoIrX9rPIWo7ZU
"""

# region Importaciones
import os
import random as rnd
import pandas as pd
import time
import datetime
import logging
import tqdm
import warnings
warnings.filterwarnings('ignore')
print('*'*100)
print(f'{"Inicio del proceso":>15}')
inicio = time.time() #Inicio contador de ejecucion
hoy = datetime.date.today().strftime('%Y%m%d') #Captura de fecha de ejecucion
nombre_archivo_log = f"log_{hoy}.log" # Inicializacion del log
#Configuracion de almacenamiento y niveles del log
logging.basicConfig(filename=nombre_archivo_log, level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#Primer registro del log
logging.info("Iniciando el proceso, por SPCII de Sebas y Juli😃👀✔")

#importamos los archivos que contienen los nombres y apellidos de Argentina desde github
NombresArgentina =pd.read_csv("https://raw.githubusercontent.com/Yulianav22/Trabajo-final/f2e8070d8c3db059021eca101c77c354ca2fbea3/Datos/NombresArgentina.csv", encoding= 'latin1')
ApellidosArgentina=pd.read_csv("https://raw.githubusercontent.com/Yulianav22/Trabajo-final/f2e8070d8c3db059021eca101c77c354ca2fbea3/Datos/ApellidosArgentina.csv")
Pensum=pd.read_csv("https://raw.githubusercontent.com/Yulianav22/Trabajo-final/main/Datos/pensum.csv", encoding = 'latin1',  sep=';')
logging.info('Nombres completos generados, pensum ingresado')      ######
# region funciones
def GenerarNombre(Nombres: list, Apellidos: list) -> str:
    Nombre = rnd.choice(Nombres)
    Apellido = rnd.choice(Apellidos)
    return f'{Nombre} {Apellido}'

def GenerarEdad() -> int:
    r = rnd.random()
    if r < 0.5:
        return rnd.randint(16, 25)
    elif r < 0.75:
        return rnd.randint(26, 33)
    elif r < 0.9:
        return rnd.randint(34, 40)
    else:
        return rnd.randint(41, 85)


def GenerearSemestre() -> int:
    r = rnd.random()
    if r < 0.14:
        return 1
    elif r < 0.27:
        return 2
    elif r < 0.39:
        return 3
    elif r < 0.5:
        return 4
    elif r < 0.6:
        return 5
    elif r < 0.7:
        return 6
    elif r < 0.79:
        return 7
    elif r < 0.87:
        return 8
    elif r < 0.94:
        return 9
    else:
        return 10
logging.info('Se reliza la creacion de edades y la generacion de los semestres')      #######
# Región donde se realizan las operaciones y funciones necesarias para unir el dataframe de nombres con el de apellidos tomado del codigo del profe
Nombres = NombresArgentina['name'].tolist()
for i in tqdm.trange(len(Nombres)):
    if ' ' in Nombres[i]:
        Nombres[i]=Nombres[i].replace(' ', '_')

Apellidos = ApellidosArgentina['lastname'].tolist()
for i in tqdm.trange(len(Apellidos)):
    if ' ' in Apellidos[i]:
        Apellidos[i]=Apellidos[i].replace(' ', '_')


df = pd.DataFrame(columns=['NOMBRE', 'Semestre', 'EDAD', 'FECHA '])
for i in tqdm.trange(1000):
    vector = []
    nombre = GenerarNombre(Nombres, Apellidos).upper()
    semestre = GenerearSemestre()
    edad = GenerarEdad()
    fecha = datetime.date.today().strftime('%Y-%m-%d')
    vector = [nombre, semestre, edad, fecha]
    df.loc[len(df)] = vector
logging.info('Nuevo directorio creado con el orden de nombre, smestre, edad y fecha')  ####
#Dependiendo en que semestre este arroja el cupo para cada aula
def cupos_por_semestre(semestre):
    if semestre in [1, 2, 3]:
        return 30
    elif semestre in [4, 5, 6]:
        return 25
    elif semestre in [7, 8, 9]:
        return 20
    elif semestre == 10:
        return 10
    else:
        return None
logging.info("Se asignan los cupos de aula para cada semestre")   #####
#canridad de estudiantes en cada semestre
def numero_estudiantes(semestres):
    if semestre == 1:
        return 140
    elif semestre == 2:
        return 130
    elif semestre == 3:
        return 120
    elif semestres == 4:
        return 110
    elif semestre in [5, 6]:
        return 100
    elif semestre == 7:
        return 90
    elif semestre == 8:
        return 80
    elif semestre == 9:
        return 70
    elif semestre == 10:
        return 60
    else:
        return None
logging.info("Se establece la cantidad de estudiantes para cada semestre academico")  ####
# Funciones  del programa
def horas_docente(creditos): #falta el de las practicas
    if creditos == 1:
        return 16
    elif creditos == 2:
        return 32
    elif creditos == 3:
        return 64
    elif creditos == 4:
        return 96
    elif creditos == 12:   ###############
        return 192
    else:
        return None
Pensum['HTD'] = Pensum['CREDITOS'].apply(horas_docente)
logging.info("se establecen las horas de trabajo de cada docente dependiendo a los creditos")
def horas_independiente(creditos): #falta definir el de las parcticas
    if creditos == 1:
        return 32
    elif creditos == 2:
        return 64
    elif creditos == 3:
        return 80
    elif creditos == 4:
        return 120
    elif creditos == 12:       #######
        return 384
    else:
        return None

Pensum['HTI'] = Pensum['CREDITOS'].apply(horas_independiente)
logging.info("se definen las horas indepenientes de estudio dependiendo los creditos")  #####

def cantidad_grupos(row):
  cociente = row['CUPOS TOTALES']//row['CUPOS POR GRUPO'] # Divide la cantidad de estudiantes entre los cupos por grupo para tener la cantidad mínima de grupos
  residuo = row['CUPOS TOTALES']%row['CUPOS POR GRUPO'] # Arroja el residuo de la división anterior para saber si la cantidad mínima de grupos es insuficiente para matricular a todos los estudiantes
  if residuo != 0:
    return cociente + 1 # Si el residuo es diferente de 0 se crea otro grupo para que todos los estudiantes puedan ser matriculados en un grupo
  else:
    return cociente

Pensum['CUPOS TOTALES'] = Pensum['SEMESTRE'].apply(numero_estudiantes)
Pensum['CUPOS POR GRUPO'] = Pensum['SEMESTRE'].apply(cupos_por_semestre)
Pensum['CANTIDAD DE GRUPOS'] = Pensum.apply(lambda row: cantidad_grupos(row), axis = 1)
logging.info("Se establecen las cantidades de grupos por cada asignatura")   ########

#Creamos un dataframe nuevo uniendo el dataframe que tiene toda la info de las materias con el dataframe que contiene los nombres edad y fecha proporcionado por el profe
df['Semestre'] = df['Semestre'].astype(str)
Pensum['SEMESTRE'] = Pensum['SEMESTRE'].astype(str)

# Unir los DataFrames
Dcompleto = pd.merge(Pensum, df, left_on='SEMESTRE', right_on='Semestre')
Dcompleto.drop('Semestre', axis=1, inplace=True)#para eliminar la que estaba repetida ya que comparten semestre
logging.info("se compila la informacion en un solo DataFrame")

# Creamos una columna nueva para asignar al estudiamte a un grupo de cada materia
Dcompleto['GRUPO'] = Dcompleto.apply(lambda row: ((row.name // row['CUPOS POR GRUPO']) % row['CANTIDAD DE GRUPOS']) + 1, axis=1)
logging.info("Se asigna grupo a cada estudiando creando una columna nueva en el Dataframe")  ######

# Se crea una función que genera el codigo de la materia tomando las dos primeras letras de la primera palabra del nombre de la materia  y la primera letra de la segunda palabra, le añade el numero de semestre al que pertenece la materia y el grupo al que pertenece
def  generar_codigo_asignatura(row):
    try:
        Asignatura = row['ASIGNATURA'].split() # para que separe cada palabra de la columna y lo convierta en una lista de str
        codigo = ''.join([Asignatura[0][:2].upper(), Asignatura[1][0].upper(), str(row['SEMESTRE']), str(row['GRUPO'])]) #para que elija las primeras dos letras de la primera palabra , la primera letra de la segunda palabra, el número del SEMESTRE y el GRUPO
        return codigo
    except IndexError: # ESi se presenta algun error si no puedo tomar alguna de las palabras genra un error y para eso hacemos un codigo alternativo
        codigo_alternativo = ''
        if Asignatura:
          codigo_alternativo = ''.join([Asignatura[0][:3].upper(), str(row['SEMESTRE']), str(row['GRUPO'])])
        return codigo_alternativo or None

#Se le aplica la función al dataframe para crear una nueva columna con el codigo
Dcompleto['CODIGO'] = Dcompleto.apply(generar_codigo_asignatura, axis=1)
#Creamos una carpeta donde almacenamos los resultados
# region Gestion de archivos y ubicaciones
#Creamos el directorio (carpeta) en donde se crearan los archivos
Directorio = os.getcwd()
textemp = f'El directorio  del trabajo es: \n\t--> {Directorio}, \nEsta carpeta contendrá los archivos del trabajo final'
print(textemp)
logging.info(textemp)
Carpeta = "CarpetaArchivosTrabajoFinal"
logging.info("Se crea el directorio {}".format(Carpeta)) ##########
os.makedirs(Carpeta, exist_ok=True)
#Para la ruta del trabajo final vamos agrupar la columna de ASIGNATURA Y SEMESTRE
Dcompleto_Agrupado = Dcompleto.groupby(['ASIGNATURA', 'SEMESTRE'])
# creamos las carpetas para cada semestre
logging.info('se lleva a cabo la agrupacion de las columnas asignatura y semestre')
for semestre, grupo in Dcompleto_Agrupado:
    carpeta_semestre = os.path.join(Carpeta, str(semestre[1]))
    os.makedirs(carpeta_semestre, exist_ok=True)


    for Asignatura, subgrupo in grupo.groupby('ASIGNATURA'):
        # Quita los espacios y capitaliza el nombre de la materia
        Nombre_Asignatura = ''.join(word.capitalize() for word in Asignatura.split())
        # Obtiene la cantidad de estudiantes y el código alfanumérico
        cantidad_estudiantes = subgrupo['CUPOS TOTALES'].iloc[0]
        codigo = subgrupo['CODIGO'].iloc[0]

        # Crea el nombre del archivo
        archivo = f'{Nombre_Asignatura}-{codigo}-{cantidad_estudiantes}.xlsx'
        subgrupo.to_excel(os.path.join(carpeta_semestre, archivo), index=False)
        archivo = f'{Nombre_Asignatura}-{codigo}-{cantidad_estudiantes}.csv'
        subgrupo.to_csv(os.path.join(carpeta_semestre, archivo), index=False)
logging.info('Generacion alfanumerica del codigo y cantidad de estudiantes por grupo')   #####
logging.info('se realiza la creacion de la carpeta para cada semestre')     #########
logging.info("Exportando a Excel")
excel = 'Matriculador.xlsx'
logging.info("Exportando a csv")
csv= 'Matriculador.csv'
print(f"El archivo {excel} ha sido creado en la carpeta {Directorio}")
print(f"El archivo {csv} ha sido creado en la carpeta {Directorio}")
final = time.time()
retardo = final-inicio
print(f'el tiempo que se ha tomado para realizar el proceso es {retardo}')
print('FIN DEL PROCESO')
print('*'*100)