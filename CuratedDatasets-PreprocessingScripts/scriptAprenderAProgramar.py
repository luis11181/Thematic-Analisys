import os
import pandas as pd # importa pandas
import numpy as np
import csv
import unidecode
import unicodedata
import re

cwd = "./Aprender a programar"
raw_folder = "./raw_csv_data"

encabezadoString = "comment;ambiente;bondadesPlataforma;CbondadesPlataformaCcasosPrueba;CbondadesPlataformaCconocerErrores;CbondadesPlataformaCconsejosFormativos;CbondadesPlataformaCdisponibilidadLinea;CbondadesPlataformaCespacioTrabajo;CbondadesPlataformaCfacilidadUso;CbondadesPlataformaClenguajes;CbondadesPlataformaCPracticaconstante;CherramientasUNcodeCcustomInput;CherramientasUNcodeClinter;CherramientasUNcodeCpythonTutor;ClogrosPedagogicosCaprendizajeAutonomo;ClogrosPedagogicosCejerciciosEstimulantes;ClogrosPedagogicosCevalluacionEstimulante;ClogrosPedagogicosCEvaluacionOptimizada;ClogrosPedagogicosChabilidadesProgramacion;ClogrosPedagogicosCresolucionProblemas;CMejorableAprenderProgramarCfallasGenerales;CMejorableAprenderProgramarCinflexibilidad;CMejorableAprenderProgramarCobjetivoEducativo;CMejorableAprenderProgramarCretroalimentacionInsuficiente;CMejorableAprenderProgramarCsustituible;colab;HerramientasUNcode;logrosPedagogicos;MejorableAprenderProgramar"
encabezado = ["ambiente","bondadesPlataforma","CbondadesPlataformaCcasosPrueba","CbondadesPlataformaCconocerErrores","CbondadesPlataformaCconsejosFormativos","CbondadesPlataformaCdisponibilidadLinea","CbondadesPlataformaCespacioTrabajo","CbondadesPlataformaCfacilidadUso","CbondadesPlataformaClenguajes","CbondadesPlataformaCPracticaConstante","CherramientasUNcodeCcustomInput","CherramientasUNcodeClinter","CherramientasUNcodeCpythonTutor","ClogrosPedagogicosCaprendizajeAutonomo","ClogrosPedagogicosCejerciciosEstimulantes","ClogrosPedagogicosCevalluacionEstimulante","ClogrosPedagogicosCEvaluacionOptimizada","ClogrosPedagogicosChabilidadesProgramacion","ClogrosPedagogicosCresolucionProblemas","CMejorableAprenderProgramarCfallasGenerales","CMejorableAprenderProgramarCinflexibilidad","CMejorableAprenderProgramarCobjetivoEducativo","CMejorableAprenderProgramarCretroalimentacionInsuficiente","CMejorableAprenderProgramarCsustituible","colab","HerramientasUNcode","logrosPedagogicos","MejorableAprenderProgramar"]

#! funcion agregar items a los que pertenece una frase
def funcionCeros(numero):
  variable = "" 
  for i in range(len(encabezado)-1): #encabezado.len
    if i == numero:
      variable +=  str(1) +";"
      continue
    else: variable += str(0) +";"
  # aditional for the last item to avoid the ";" at the end
  if len(encabezado)-1 == numero:
    variable +=  str(1) 
  else: variable += str(0) 
  return variable

#! quitar tildes
# Aqui se concatenan cadenas para formar una sola cadena con todas las vocales que tengan tildes.
# La \ significa "esta suma sigue en la siguiente linea".
# Esto genera "àáâãäåèéêëìíîïòóôõöùúûü"

tildes = ("àáâãäå" + \
          "èéêë" + \
          "ìíîï" + \
          "òóôõöÓ" + \
          "ùúûü"+ \
          "ñÑ"+ \
            "§¡"+ \
            '"'+ \
            ";"+ \
            "¿" + \
            "°")

# Cada letra aquí corresponde a una vocal acentuada.
# Por ejemplo la primera "a" corresponde a "à", la segunda con "á" y asi sucesivamente.

vocales = ("aaaaaa" + \
           "eeee" + \
           "iiii" + \
           "oooooO" + \
           "uuuu"+ \
            "nN"+ \
            "x!"+ \
           ' '+ \
           ","+ \
            " " + \
            " ")

# Aqui con el método maketrans relacionamos las dos cadenas antes creadas.
# Esto devuelve un diccionario compatible con el método translate.
transMap = str.maketrans(tildes, vocales)
#cadena = "existen plataformas con un ambiente un poco más amigable como lo es colab"
# Teniendo ese diccionario generado (solo hace falta crearlo una vez)
# podemos usar el método translate para cambiar las vocales acentuadas con vocales sin acentuar.
#cadena = cadena.translate(transMap)


#! apertura de los archivos, y unificacion en un dataframe

f = open("aprenderAProgramarGeneratedTexts.csv","a+") 
f.truncate(0)
f.write(encabezadoString )
f.write("\n")
orden =0
for filename in os.listdir(cwd):
  print(filename)
  categorias = funcionCeros(orden)
  if filename.endswith(".txt"): 
    file = open(cwd+"/"+filename, 'r', encoding="utf-8")
    for lineWithSpaces in file.readlines():
      #print(unidecode.unidecode(line))
      line = lineWithSpaces
      if line.startswith("<") or line.startswith("Reference") or line.startswith("References") or len(line)<=1:
        continue    
      line = lineWithSpaces.strip().replace("\n","").translate(transMap).strip()
      #variable = line.join(["'","'"])
      # f.write("'")
      #print(categorias)
      f.write('"'+f"{line}"+'"')  #f.write(f"{line}")
      #print(line)
      f.write(";")
      f.write(categorias)
      f.write("\n")
  orden+=1
f.close()
#open raw files to get the agreement with each question, calificacion is the last column
f_calificacion = open("aprenderAProgramarCalificacion.csv","a+") 
f_calificacion.truncate(0)
f_calificacion.write("comment;calificacion")
f_calificacion.write("\n")
for filename in os.listdir(raw_folder):
  temp_counter = 0
  print(filename, "filename calificacion")
  if filename.endswith(".csv"): 
    raw_f = open(raw_folder+"/"+filename, 'r', encoding="utf-8")
    reader = csv.reader(raw_f)
    for row in reader:
      if temp_counter == 0:
        temp_counter+=1
        continue
      comment = row[8].strip().replace("\n","").translate(transMap).strip()
      calificacion = row[7].strip().replace("\n","").translate(transMap).strip()
      #print(comment)
      f_calificacion.write('"'+f"{comment}"+'"')  #f.write(f"{line}")
      #print(line)
      f_calificacion.write(";")
      f_calificacion.write('"'f"{calificacion}"+'"')
      f_calificacion.write("\n")
f_calificacion.close()

excel_file_path_calificacion = r'aprenderAProgramarCalificacion.csv' #! toca dejar la r para que sea raw string y lea la url
df_calificacion = pd.read_csv(excel_file_path_calificacion,sep=';', encoding='utf-8') # los rows inician en 0  #,  encoding='utf-8' encoding='iso-8859-1' encoding='latin-1'
print(df_calificacion)


# csv to dataframe with gouping for comments and categories
excel_file_path = r'aprenderAProgramarGeneratedTexts.csv' #! toca dejar la r para que sea raw string y lea la url
df = pd.read_csv(excel_file_path,sep=';', encoding='utf-8') # los rows inician en 0  #,  encoding='utf-8'
grouped_df = df.groupby(["comment"]).sum().reset_index()
grouped_df['comment'] = grouped_df['comment'].str.strip('"')
print("grouped_df")
print(grouped_df)

# created dataframe to csv with grouping for comments and categories
grouped_df.to_csv('aprenderAProgramarDataFrameWithoutCalificacion.csv',sep=';',index=False,quoting=csv.QUOTE_NONE, quotechar='',escapechar="\\") #

# # read csv to dataframe
# df2 = pd.read_csv(r'aprenderAProgramarfinalDataFrame.csv',sep=';') 
# print(df2)

# merge two dataframes
merged_df = pd.merge(grouped_df, df_calificacion, on='comment', how='left')

# fill missing values in the 'calificacion' column with a default message
merged_df['calificacion'] = merged_df['calificacion'].fillna('NO CALIFICADO')

print("merged_df")
print(merged_df)

# created dataframe to csv with grouping for comments and categories
merged_df.to_csv('aprenderAProgramarFinalDataFrameWithCalificacion.csv',sep=';',index=False,quoting=csv.QUOTE_NONE, quotechar="",escapechar="\\") #


print("zzzz")
#print(df_calificacion[comment][279])