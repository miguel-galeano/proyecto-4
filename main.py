#Manejo de rutas y archivos
from pathlib import Path
import os
import shutil
import sys
import time
import string
from datetime import datetime
#fx start:
#input: cantidad de bytes
#output: string con formato
def size_format(b):
    if b < 1000:
              return '%i' % b + ' B'
    elif 1000 <= b < 1000000:
        return '%.1f' % float(b/1000) + ' KB'
    elif 1000000 <= b < 1000000000:
        return '%.1f' % float(b/1000000) + ' MB'
    elif 1000000000 <= b < 1000000000000:
        return '%.1f' % float(b/1000000000) + ' GB'
    elif 1000000000000 <= b:
        return '%.1f' % float(b/1000000000000) + ' TB'

#fx end: funcion "size_format"

#fx start: calculo % de proceso cada 100 archivos leidos
#input: file_size del directorio, file_acumulado, cantidad_archivos_leidos
#output: % transferido
#(input_size, input_size_read,cantidad_archivos_leidos)
def avance_lectura(input_len,cantidad_archivos_leidos):
    retorno = int((cantidad_archivos_leidos*100)/input_len)
    print("Procesando -------> " + str(retorno) + "%  ")
    return retorno
#fx end: funcion "avance_lectura"

#fx start: Convierte segundos a HH:MM:SS
def conversion_time(segundos):
    horas = int(segundos / 60 / 60)
    segundos -= horas*60*60
    minutos = int(segundos/60)
    segundos -= minutos*60
    segundos = int(segundos)
    tf = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
    return tf
#fx end: función "conversion_time"

# fx start: Determina existencia de folder/carpeta de trabajo. Busca en Home_directory
#Input: Str file_input con el nombre del directorio origen para ordenar
#Ouput: Str retorno = "" cuando no existe el folder/carpeta
#Output: Str retorno != "" con la cadena válida
def valida_carpeta(file_input):
    p = Path.home()
    retorno = {}
    retorno1 = ""
    cant = 0
    file_note = "facilito"
    for x in p.iterdir():
        dummy = str(x).lower()
        if (str(x).lower().find(file_input.lower()) != -1):
            retorno[cant]= dummy
            cant = cant + 1
        else:
            pass
        lista = list(retorno)
        for x in lista:
            a = retorno[x]
            if (str(a).lower().find(file_note.lower()) != -1):
                pass
            else:
                retorno1= a
    return retorno1
# fx end: Funcion "valida_carpeta"

#main.py
texto = "Codigo Facilito - BootCamp"
texto1 = "Proyecto - Ordenamiento de Archivos"
print("--".center(50))
print(texto.center(50))
print(texto1.center(50))
ph = Path.home()
print("Path.home ---> " + str(ph))
# ingreso directorio/carpeta de trabajo
file_input = input( "Ingrese nombre de la carpeta a procesar (Debe estar ubicado en Path.home): ")
file_input = file_input.lower()
dummy = valida_carpeta(file_input) # Valida existencia de carpeta/folder de trabajo
if dummy == "":
    print("Carpeta/Folder de trabajo No existe/No se encontro")
    print("")
    print("Se detiene la aplicacion")
    sys.exit()
else:
    pass
fechaahora_inicio = time.time() #Inicio de proceso
# crea Path de trabajo
current_input = dummy # carpeta/directorio/folder seleccionado
#construye Path de salida
p = str(Path.home())
#st2 ='\\''' es una barra invertida
s = p + '\\''' +file_input+ "_facilito"
current_output = Path(s)
#current_output se elimina siempre
shutil.rmtree(current_output,ignore_errors=True)
#input_size = os.path.getsize(current_input)
content_files =  os.listdir(current_input )
input_len = len(content_files)
input_size_read = 0
cantidad_archivos = 0
cantidad_archivos_leidos = 0
dic_proceso = {}
dic_size = {}
for content in content_files:
    if Path(content).suffix == "":
        pass
    else:
        file_input = Path(current_input) / content
        if Path(file_input).is_file:
            cantidad_archivos = cantidad_archivos + 1
            sufijo = Path(file_input).suffix
            dummy = sufijo.replace(".","")
            dummy = dummy.lower()
            sufijo_dic = dummy
            sufijo_new = dummy +"s"
            current_new_output = Path(current_output) / str(sufijo_new)
            file_output = Path(current_new_output) / content
            if not Path(current_new_output).exists():
                #Path(current_new_output).mkdir()
                os.makedirs(current_new_output)
            else:
                pass
            shutil.copy(file_input, file_output)
            file_size = os.path.getsize(file_output)
            #actualizar dic
            if dic_proceso.get(sufijo_dic) == None:
                dic_proceso[sufijo_dic] = 0
                dic_size[sufijo_dic] = 0
            else:
                pass
            dic_proceso[sufijo_dic] = dic_proceso[sufijo_dic] + 1
            dic_size[sufijo_dic] = dic_size[sufijo_dic] + file_size
            input_size_read = input_size_read + file_size
            cantidad_archivos = cantidad_archivos + 1
            cantidad_archivos_leidos = cantidad_archivos_leidos + 1
            if cantidad_archivos > 70:
                cantidad_archivos = 0
                retorno = avance_lectura(input_len, cantidad_archivos_leidos)
            else:
                pass
        else:
            pass
fechaahora_fin = time.time() # fin de proceso
tf = conversion_time(fechaahora_fin - fechaahora_inicio)
texto = "Resultado del proceso"
print(texto.center(50))
texto = "--------------------------"
print(texto.center(50))
print("Directorio creado : " + str(current_output))
print("Sub Directorios creados : ")
dummy = list(dic_proceso)
for element in dummy:
    dummy1 = str(dic_proceso[element])
    dummy2 = int(str(dic_size[element]))
    dummy2 = size_format(dummy2)
    dummy1= dummy1.rjust(10," ")
    dummy2 = dummy2.rjust(15," ")
    dummy3 = str(element)
    dummy3 = dummy3.ljust(15," ")
    dummy3 = dummy3[0:10]
    print("Directorio : " + dummy3 + "  "+ str(dummy1) + " Files "+ str(dummy2))
print("Tiempo de proceso = " + str(tf))
print("Fin proceso")
 
