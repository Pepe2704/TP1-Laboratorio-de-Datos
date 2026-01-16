
"""
Created on Fri May 16 12:56:36 2025

@author: Walid
"""




#Sanchez Richani Walid
#Blumenthal Hernan
#Soldatich Pedro






# %%

import pandas as pd
from inline_sql import sql
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np 




######################################
########## CRUDOS ####################
######################################

departamentos_original_df = pd.read_excel("codigo_departamento.xlsx")
df = pd.read_excel("poblacion.xlsx")
bp_df_original = pd.read_csv("bibliotecas.csv")
ee_df_cortado = pd.read_csv("df_educativos.csv") # agregar a la entrega el archivo cortado??????
# departamentos_FINAL_definitivo.csv"
# provincias_FINAL.csv"


#############################################################################################################################################################
############################################################## LIMPIEZA Y TRANSFORMACION DE DATOS ###########################################################
#############################################################################################################################################################


####################################  
######### TABLA POBLACION ##########  
####################################



df_sin_primera_col = df.drop(df.columns[0],axis=1) #elimine la primera columna estaba al pedo
df_filtrado = df_sin_primera_col.dropna() # NO HAY AREA NI LOCALIDAD
nueva_columna = []
area_actual = None
nombre_actual = None
        
nombre_de_departamentos = df['Unnamed: 2'].astype(str)    
  
#En el siguiente ciclo, lo que hacemos es matchear(dividir en dos con (.split) el area de la columna 'Unnamed: 1'), y agregar solamente los caracteres despues del # a una lista a una lista
# Esto nos sirve porque despues hacemos un nuevo dataFrame donde relacionamos por codigo de Area en nuestro DER es id_departamento 
for valor in df['Unnamed: 1']:
    if type(valor) == str and 'AREA #' in valor and '#' in valor:
        partes = valor.split('#')
        if len(partes) == 2:
            area_actual = partes[1].strip()
            nombre_actual = partes[0].strip ()
            
    if valor in ['Edad', 'Total', 'Casos', 'Comuna', 'Localidad']:# borre el total
        nueva_columna.append(None)

    else:
        nueva_columna.append(area_actual)
        

df['AREA'] = nueva_columna #Agregamos  a df 

df = df.drop(df.columns[0], axis=1)

df_filtrado = df.dropna() #eliminamos nulls

df_filtrado.columns = ['Edad', 'Casos', '%', 'Acumulado %', 'AREA'] # nos quedamos unicamente con las columnas necesarias segun nuestro DER


df_filtrado = df_filtrado.drop (df_filtrado.columns[2],axis =1 )
df_filtrado = df_filtrado.drop (df_filtrado.columns[2],axis =1 )
############################ POBLACIONES DE PRIMARIOS,SECUNDARIOS,JARDINES ######################

#rango de edad entre 0 a 5
df_jardines = df_filtrado[df_filtrado['Edad'].between(0,5)]
df_poblacion_jardin = df_jardines.groupby('AREA')['Casos'].sum().reset_index()  #calculamos el total de casos por área y guardándolo en df_poblacion_jardin. 



#rango de edad entre 6 a 11
df_primarios = df_filtrado[df_filtrado['Edad'].between(6,11)] 
df_poblacion_primarios = df_primarios.groupby('AREA')['Casos'].sum().reset_index()  #calculando el total de casos por área y guardándolo en df_poblacion_primario 



#rango de edad entre 12 a 18
df_secundario = df_filtrado[df_filtrado['Edad'].between(12,18)]
df_poblacion_secundario = df_secundario.groupby('AREA')['Casos'].sum().reset_index() # calculando el total de casos por área y guardándolo en df_poblacion_secundario. 


######################################
#agrupamos poblaciones por área en una sola tabla para facilitar el análisis.


df_jardin_idx = df_poblacion_jardin.set_index('AREA')
df_primario_idx = df_poblacion_primarios.set_index('AREA')
df_secundario_idx = df_poblacion_secundario.set_index('AREA')


df_poblacion= pd.concat([df_jardin_idx, df_primario_idx, df_secundario_idx], axis=1)


df_poblacion = df_poblacion.reset_index()

df_poblacion.columns = ['id_departamento','poblacion_jardin','poblacion_primario','poblacion_secundario']
######################## TOTALES #######################
#como antes habiamos eliminado la columna total decidimos filtrar las filas donde 'Unnamed: 1' es 'Total' y eliminando columnas innecesarias. 
#Luego, sumamos los primeros 15 registros y los convierto en un DataFrame (suma_df), pues los primeros 15 son las comunas de ciudad y tienen el mismo codigo
# También limpiamos el identificador de departamento eliminando ceros a la izquierda

df_totales = df[df['Unnamed: 1'] == 'Total' ]

df_totales = df_totales.drop(df_totales.columns[2], axis=1)
df_totales = df_totales.drop(df_totales.columns[2], axis=1)
df_totales = df_totales.drop(df_totales.columns[2], axis=1)

suma = df_totales.head(15).sum()
suma_df = pd.DataFrame([suma])
df_restante = df_totales[15:]

df_totales_sinCiudad = pd.concat([suma_df, df_restante], ignore_index=True)

lista_de_totales = df_totales_sinCiudad['Unnamed: 2'].tolist()

df_poblacion["poblacion_total"] = lista_de_totales


df_poblacion['id_departamento'] = df_poblacion['id_departamento'].str.lstrip('0')





#######################################################
########## TABLA ESTABLECIMIENTOS EDUCATIVOS ##########
#######################################################

# Filtrado de establecimientos educativos según modalidad
ee_df_modalidad_comun = ee_df_cortado.loc[ee_df_cortado['Común'] == '1']

ee_df_modalidad_primario = ee_df_modalidad_comun.loc[ee_df_modalidad_comun['Primario'] == '1']
ee_df_modalidad_secundario = ee_df_modalidad_comun.loc[ee_df_modalidad_comun["Secundario"] == '1']
ee_df_modalidad_jardin_maternal = ee_df_modalidad_comun.loc[ee_df_modalidad_comun["Nivel inicial - Jardín maternal"] == '1']
ee_df_modalidad_jardin_infantes = ee_df_modalidad_comun.loc[ee_df_modalidad_comun["Nivel inicial - Jardín de infantes"] == '1']

# Creación de DataFrames con identificadores de modalidad
ee_df_modalidad_jardin_maternal_ids_copia = ee_df_modalidad_jardin_maternal["Cueanexo"]
ee_df_modalidad_jardin_maternal_ids = pd.DataFrame(ee_df_modalidad_jardin_maternal_ids_copia)
ee_df_modalidad_jardin_maternal_ids["id_modalidad"] = 1

ee_df_modalidad_jardin_infantes_ids_copia = ee_df_modalidad_jardin_infantes["Cueanexo"]
ee_df_modalidad_jardin_infantes_ids = pd.DataFrame(ee_df_modalidad_jardin_infantes_ids_copia)
ee_df_modalidad_jardin_infantes_ids["id_modalidad"] = 1

ee_df_modalidad_primario_ids_copia = ee_df_modalidad_primario["Cueanexo"]
ee_df_modalidad_primario_ids = pd.DataFrame(ee_df_modalidad_primario_ids_copia)
ee_df_modalidad_primario_ids["id_modalidad"] = 2

ee_df_modalidad_secundario_ids_copia = ee_df_modalidad_secundario["Cueanexo"]
ee_df_modalidad_secundario_ids = pd.DataFrame(ee_df_modalidad_secundario_ids_copia)
ee_df_modalidad_secundario_ids["id_modalidad"] = 3

#### Relaciones para trabajar con SQL ###

# Relación modalidad_escuela
df_modalidad_escuela = pd.DataFrame(pd.concat([
    ee_df_modalidad_jardin_maternal_ids,
    ee_df_modalidad_jardin_infantes_ids,
    ee_df_modalidad_primario_ids,
    ee_df_modalidad_secundario_ids
], ignore_index=True, axis=0))

# Relación modalidad_comun
modalidad_comun_ref = {
    'id_modalidad': [1, 2, 3],
    'nombre_modalidad': ["Jardin", "Primario", "Secundario"]
}
df_modalidad_comun_ref = pd.DataFrame(modalidad_comun_ref)

# Relación establecimientos educativos
df_ee_final = pd.DataFrame(ee_df_modalidad_comun[["Código de localidad", "Cueanexo", "Nombre"]])
df_ee_conProvincia = pd.DataFrame(ee_df_modalidad_comun[["Código de localidad", "Cueanexo", "Nombre", "Jurisdicción"]])


#######################################
########## TABLA BIBLIOTECAS ##########
#######################################

# Relación bibliotecas populares
bp_df_filtrado = bp_df_original[["nro_conabip", "nombre", "id_departamento", "fecha_fundacion", "mail"]]
df_bp_final = pd.DataFrame(bp_df_filtrado)
df_bp_final["dominio"] = df_bp_final["mail"].str.extract(r'@([^.@]+)\.')

#### Saco el último dígito a la columna "Código de localidad" solo aquellos que tienen longitud 6
df_ee_FINAL = df_ee_final.copy()  # Crear una copia completa para no modificar el original
df_ee_FINAL["Código de localidad"] = df_ee_FINAL["Código de localidad"].astype(str)  # Convertir a string

df_ee_FINAL.loc[df_ee_FINAL["Código de localidad"].str.startswith("6"), "Código de localidad"] = df_ee_FINAL["Código de localidad"].str[:-1]  # Le saco el último dígito a los que empiezan por 6
df_ee_FINAL.loc[df_ee_FINAL["Código de localidad"].str.len() == 6, "Código de localidad"] = df_ee_FINAL["Código de localidad"].str[:-1]  # Modificar solo los códigos de longitud 6

df_ee_FINAL.columns = ["id_departamento", "Cueanexo", "Nombre"]




###############################################################################
################ DEPARTAMENTOS + CONSULTA SQL #################################
###############################################################################
consulta_genera_depto = """
                        SELECT DISTINCT *
                        FROM "departamentos_FINAL_definitivo.csv"
                        LEFT OUTER JOIN "provincias_FINAL.csv"
                        ON departamentos_FINAL_definitivo.PROV = provincias_FINAL.Código ;
                        """

df_departamentos_provincia_PRE = sql^ consulta_genera_depto

df_departamentos_provincia_PRE.to_csv("df_departamentos_provincia_PRE.csv", index=False)
                        

consulta_genera_depto_FINAL = """
                        SELECT PROV, Provincia, DPTO, NOMDPTO 
                        FROM "df_departamentos_provincia_PRE.csv"
                        ORDER BY Provincia;
                        """
df_departamentos_provincia_FINAL = sql^ consulta_genera_depto_FINAL
df_departamentos_provincia_FINAL.to_csv("df_departamentos_provincia_FINAL.csv", index=False)
# Cargar el DataFrame original
df_departamentos_provincia_FINAL_2 = pd.read_csv("df_departamentos_provincia_FINAL.csv")

# Filtrar solo las filas donde PROV == 2 y unificar datos
df_filtrado = df_departamentos_provincia_FINAL_2[df_departamentos_provincia_FINAL_2["PROV"] == 2]
df_unificado = df_filtrado.groupby("PROV").agg("first").reset_index()

# Mantener el resto del DataFrame sin modificar
df_modificado = df_departamentos_provincia_FINAL_2[df_departamentos_provincia_FINAL_2["PROV"] != 2].copy()

# Unir el DataFrame original con la fila unificada
df_unificado2 = pd.concat([df_modificado, df_unificado], ignore_index=True)

# Modificar "NOMDPTO" para PROV == 2
df_unificado2.loc[df_unificado2["PROV"] == 2, "NOMDPTO"] = "Promedio Comunas"
df_unificado2.loc[df_unificado2["PROV"] == 2, "DPTO"] = 2000
# **Mover la última fila al inicio**
ultima_fila = df_unificado2.iloc[-1:]  # Seleccionar la última fila
resto_df = df_unificado2.iloc[:-1]  # Todas las demás filas sin la última
df_DEPARTAMENTOS_final = pd.concat([ultima_fila, resto_df], ignore_index=True)  # Reordenar DataFram


###############################################################################
####################DATA FRAMES LIMPIOS ######################################
###############################################################################

# a continuacion dejo los nombres de los datas frames ya limpios.....

# 1) poblacion = df_poblacion
# 2) establecimientos educativos = df_ee_FINAL
# 3) bibliotecas_populares = df_bp_final
# 4) departamentos = df_DEPARTAMENTOS_final
# 5) modalidad_comun = df_modalidad_comun_ref
# 6) modalidad escuela = df_modalidad_escuela 

###############################################################################
################### EXPORTACION DE ARCHIVOS ###################################
###############################################################################

df_bp_final.to_csv("df_bp_FIINAL_definitivo.csv", index=False)
df_poblacion.to_csv("df_poblacion_FINAL_definitivo.csv", index=False)
df_ee_conProvincia.to_csv("df_ee_conP_previo.csv", index=False)
df_ee_FINAL.to_csv("df_ee_FINAL_definitivo.csv", index=False)
df_modalidad_escuela.to_csv("df_modalidad_escuela_FINAL.csv", index=False)
df_modalidad_comun_ref.to_csv("df_modalidad_comun_ref_FINAL.csv", index=False)
departamentos_original_df = pd.read_excel("codigo_departamento.xlsx")
departamentos_original_df.to_csv("departamentos_FINAL_definitivo.csv", index=False)
df_DEPARTAMENTOS_final.to_csv("df_departamentos_FINAL_DEFINITIVO_.csv",index = False) 


#############################################################################################################################################################
################################################################### SQL ##################################################################################
#############################################################################################################################################################


# i)


## relacionamos la tabla departamentos con tabla poblacion
consulta_1_i =  """
                SELECT DISTINCT *
                FROM "df_departamentos_FINAL_DEFINITIVO_.csv"
                INNER JOIN "df_poblacion_FINAL_definitivo.csv"
                ON df_departamentos_FINAL_DEFINITIVO_.DPTO = df_poblacion_FINAL_definitivo.id_departamento;
                """
df_res_ejercicio_1_i = sql^ consulta_1_i

df_res_ejercicio_1_i.to_csv("df_res_ejercicio_1_i.csv", index=False)


#relacionamos el id_escuela con el identificador de la modalidad y su correspondiente nombre

consulta_1_ii = """
                SELECT DISTINCT *
                FROM "df_modalidad_escuela_FINAL.csv"
                NATURAL JOIN "df_modalidad_comun_ref_FINAL.csv";
                """
df_res_ejercicio_1_ii = sql^ consulta_1_ii

df_res_ejercicio_1_ii.to_csv("df_res_ejercicio_1_ii.csv", index=False)

#relacionamos la tabla anterior con el id departamento y el nombre de la escuela
consulta_1_iii ="""
                SELECT DISTINCT *
                FROM "df_ee_FINAL_definitivo.csv"
                NATURAL JOIN "df_res_ejercicio_1_ii.csv";
                """
df_res_ejercicio_1_iii = sql^ consulta_1_iii

df_res_ejercicio_1_iii.to_csv("df_res_ejercicio_1_iii.csv", index=False)

#de la consulta anterior contamos del atributo nombre_modalidad solo los valores jardin y los agrupamos por depto
consulta_1_jardines =  """  
                       SELECT id_departamento, nombre_modalidad, COUNT(*) AS Jardines
                       FROM "df_res_ejercicio_1_iii.csv"
                       WHERE nombre_modalidad = 'Jardin'
                       GROUP BY nombre_modalidad, id_departamento;
                       """

df_res_ejercicio_1_jardines = sql^ consulta_1_jardines

# analogo al anterior
consulta_1_primarios = """  
                       SELECT id_departamento, nombre_modalidad, COUNT(*) AS Primarios
                       FROM "df_res_ejercicio_1_iii.csv"
                       WHERE nombre_modalidad = 'Primario'
                       GROUP BY nombre_modalidad, id_departamento;
                       """

df_res_ejercicio_1_primarios = sql^ consulta_1_primarios


# analago al anterior
consulta_1_secundarios = """  
                       SELECT id_departamento, nombre_modalidad, COUNT(*) AS Secundarios
                       FROM "C:\\Users\\Walid\\OneDrive\\Documentos\\LaboDatos\\TP1\\COPIA\\df_res_ejercicio_1_iii.csv"
                       WHERE nombre_modalidad = 'Secundario'
                       GROUP BY nombre_modalidad, id_departamento;
                       """

df_res_ejercicio_1_secundarios = sql^ consulta_1_secundarios



df_res_ejercicio_1_jardines.to_csv("df_res_ejercicio_1_jardines.csv", index=False)

df_res_ejercicio_1_primarios.to_csv("df_res_ejercicio_1_primarios.csv", index=False)

df_res_ejercicio_1_secundarios.to_csv("df_res_ejercicio_1_secundarios.csv", index=False)


#########

#relacionamos la tabla generada en la primera consulta con la consulta de jardines agrupadas con departamento
consulta_1_v_jardin =  """
                SELECT DISTINCT *
                FROM "df_res_ejercicio_1_i.csv"
                NATURAL JOIN "df_res_ejercicio_1_jardines.csv";
                """
df_res_ejercicio_1_v_jardin = sql^ consulta_1_v_jardin

df_res_ejercicio_1_v_jardin.to_csv("df_res_ejercicio_1_v_jardin.csv", index=False)

# analogo al anterior pero agregando cantidad de primarios por depto
consulta_1_v_primario =  """
                SELECT DISTINCT *
                FROM "df_res_ejercicio_1_i.csv"
                NATURAL JOIN "df_res_ejercicio_1_primarios.csv";
                """
df_res_ejercicio_1_v_primario = sql^ consulta_1_v_primario

df_res_ejercicio_1_v_primario.to_csv("df_res_ejercicio_1_v_primario.csv", index=False)


# analogo al anterior pero agregando cantidad de secundarios por depto
consulta_1_v_secundario =  """
                SELECT DISTINCT *
                FROM "df_res_ejercicio_1_i.csv"
                NATURAL JOIN "df_res_ejercicio_1_secundarios.csv";
                """
df_res_ejercicio_1_v_secundario = sql^ consulta_1_v_secundario

df_res_ejercicio_1_v_secundario.to_csv("df_res_ejercicio_1_v_secundario.csv", index=False)




####

# unimos las tablas de las tres consultas anteriores 
consulta_1_join_jardin_primario = """
                SELECT DISTINCT *
                FROM "df_res_ejercicio_1_v_jardin.csv"
                LEFT OUTER JOIN "df_res_ejercicio_1_v_primario.csv"
                ON df_res_ejercicio_1_v_jardin.id_departamento = df_res_ejercicio_1_v_primario.id_departamento;
                """
df_res_ejercicio_1_jardin_primario = sql^ consulta_1_join_jardin_primario

df_res_ejercicio_1_jardin_primario.to_csv("df_res_ejercicio_1_jardin_primario.csv", index=False)

consulta_1_join_primario_secundario = """
                SELECT DISTINCT *
                FROM "df_res_ejercicio_1_jardin_primario.csv"
                LEFT OUTER JOIN "df_res_ejercicio_1_v_secundario.csv"
                ON df_res_ejercicio_1_jardin_primario.id_departamento = df_res_ejercicio_1_v_secundario.id_departamento;
                """
df_res_ejercicio_1_primario_secundario = sql^ consulta_1_join_primario_secundario

df_res_ejercicio_1_primario_secundario.to_csv("df_res_ejercicio_1_primario_secundario.csv", index=False)



#####

# seleccionamos las columnas relevante para el reporte de la tabla generada en el punto anterior
# las ordenamos segun el enunciado
# "CABA" no tiene el promedio. 
consulta_1_final = """ 
                   SELECT DISTINCT provincia, NOMDPTO, Jardines, poblacion_jardin, Primarios, poblacion_primario, Secundarios, poblacion_secundario
                   FROM "df_res_ejercicio_1_primario_secundario.csv"
                   ORDER BY provincia, Primarios DESC;
                   """
                

df_res_ejercicio_1_final = sql^ consulta_1_final

df_res_ejercicio_1_final.to_csv("df_res_ejercicio_1_final.csv", index=False)

#se genero la fila con caba donde sacamos el promedio
consulta_1_final_comuna_prom =  """
                                SELECT Provincia, NOMDPTO, Jardines / 15, poblacion_jardin / 15, Primarios / 15, poblacion_primario / 15, Secundarios / 15, poblacion_secundario / 15
                                FROM "df_res_ejercicio_1_final.csv"
                                WHERE NOMDPTO = 'Promedio Comunas';
                                """
                                
df_res_ejercicio_1_final_comuna_prom = sql^ consulta_1_final_comuna_prom

df_res_ejercicio_1_final_comuna_prom.to_csv("df_res_ejercicio_1_final_comuna_prom.csv", index=False)


#Esta es la consulta para eliminar la fila vieja con valores absolutos de CABA
consulta_1_final_comuna_agg =   """
                                SELECT Provincia, NOMDPTO, Jardines, poblacion_jardin, Primarios, poblacion_primario, Secundarios, poblacion_secundario
                                FROM "df_res_ejercicio_1_final.csv"
                                WHERE NOMDPTO != 'Promedio Comunas';
                                """

df_res_ejercicio_1_final_comuna_agg = sql^ consulta_1_final_comuna_agg

df_res_ejercicio_1_final_comuna_agg.to_csv("df_res_ejercicio_1_final_comuna_agg.csv", index=False)



#Esta es la consulta para pegar la fila nueva con valores promediados de CABA
# esta es la consulta final entregada.
consulta_1_final_comuna_agg_FINAL = """
                                    SELECT *
                                    FROM "df_res_ejercicio_1_final_comuna_agg.csv"
                                    UNION 
                                    SELECT *
                                    FROM "df_res_ejercicio_1_final_comuna_prom.csv";
                                    """
df_res_ejercicio_1_final_comuna_agg_FINAL = sql^ consulta_1_final_comuna_agg_FINAL

df_res_ejercicio_1_final_comuna_agg_FINAL.to_csv("df_res_ejercicio_1_final_comuna_agg_FINAL.csv", index=False)




################## 
# ii)
# unimos el dataframe final de biblioteca con el dataframe final de departamentos
consulta_2_i =  """
                SELECT DISTINCT *
                FROM "df_bp_FIINAL_definitivo.csv"
                LEFT OUTER JOIN "df_departamentos_FINAL_DEFINITIVO_.csv"
                ON df_bp_FIINAL_definitivo.id_departamento = df_departamentos_FINAL_DEFINITIVO_.DPTO;
                """
df_res_ejercicio_2_i = sql^ consulta_2_i


df_res_ejercicio_2_i.to_csv("df_res_ejercicio_2_i.csv", index=False)

# seleccionamos del anterior seleccionamos solo los departamentos que tienen fecha_fundacion >= 1950
consultaSQL_bps_fundadas_1950 = """
                    SELECT DISTINCT NOMDPTO, provincia, fecha_fundacion
                    FROM "df_res_ejercicio_2_i.csv"
                    WHERE fecha_fundacion >= '1950-01-01';
                    """
dataframeResultado_bps_fundadas_1950 = sql^ consultaSQL_bps_fundadas_1950
    

dataframeResultado_bps_fundadas_1950.to_csv("dataframeResultado_bps_fundadas_1950.csv", index=False)

# Generamos la columna cantidad de bp y agrupamos por depto de forma ordenada
consulta_2_ii = """  
               SELECT provincia, NOMDPTO, COUNT(*) AS "Cantidad de BP fundadas de 1950"
               FROM "dataframeResultado_bps_fundadas_1950.csv"
               GROUP BY provincia, NOMDPTO
               ORDER BY provincia, "Cantidad de BP fundadas de 1950" DESC;
               """
df_res_ejercicio_2_ii = sql^ consulta_2_ii

df_res_ejercicio_2_ii.to_csv('df_res_ejercicio_2_ii.csv', index=False)


########################

# iii)
# tomamos la tabla del item 1 final y  sumamos todos los establecimientos educativos
consulta_3_i =  """
                SELECT provincia, NOMDPTO, COALESCE(Jardines) + COALESCE(Primarios) + COALESCE(Secundarios) AS "Cant_EE"
                FROM "df_res_ejercicio_1_final.csv";
                """
                
df_res_ejercicio_3_i = sql^ consulta_3_i

df_res_ejercicio_3_i.to_csv('df_res_ejercicio_3_i.csv', index=False)

# contamos la cantidad de bibliotecas de departamentos y las ordenamos

consulta_3_ii = """  
               SELECT provincia, NOMDPTO, COUNT(*) AS "Cant_BP"
               FROM "df_res_ejercicio_2_i.csv"
               GROUP BY provincia, NOMDPTO
               ORDER BY provincia, "Cant_bp" DESC;
               """
df_res_ejercicio_3_ii = sql^ consulta_3_ii

df_res_ejercicio_3_ii.to_csv('df_res_ejercicio_3_ii.csv', index=False)

# unimos las dos consultas previas para obtener una unica tabla
consulta_3_iii = """
                 SELECT DISTINCT *
                 FROM "df_res_ejercicio_3_i.csv"
                 NATURAL JOIN "df_res_ejercicio_3_ii.csv";
                 """
                 
df_res_ejercicio_3_iii = sql^ consulta_3_iii

df_res_ejercicio_3_iii.to_csv('df_res_ejercicio_3_iii.csv', index=False)

# unimos las tabla del punto anterior con la tabla generada del ejercicio 1  que contiene los atributos poblacion total con id_departamento 
consulta_3_iv = """
                 SELECT DISTINCT *
                 FROM "df_res_ejercicio_3_iii.csv"
                 NATURAL JOIN "df_res_ejercicio_1_i.csv";
                 """
                 
df_res_ejercicio_3_iv = sql^ consulta_3_iv

df_res_ejercicio_3_iv.to_csv('df_res_ejercicio_3_iv.csv', index=False)

#seleccionamos las columnas relevantes y ordenamos para el reporte final
consulta_3_v =  """
                SELECT provincia, NOMDPTO, Cant_EE, Cant_BP, poblacion_total
                FROM "df_res_ejercicio_3_iv.csv"
                ORDER BY provincia ASC, "Cant_bp" DESC, "Cant_ee" DESC, NOMDPTO ASC;
                """
                
df_res_ejercicio_3_v = sql^ consulta_3_v

df_res_ejercicio_3_v.to_csv('df_res_ejercicio_3_v.csv', index=False)
#### promedio ####
consulta_3_v_final_comuna_prom =  """
                                SELECT Provincia, NOMDPTO, Cant_EE / 15, Cant_BP / 15,poblacion_total / 15
                                FROM "df_res_ejercicio_3_v.csv"
                                WHERE NOMDPTO = 'Promedio Comunas';
                                """
                                
df_res_ejercicio_3_v_final_comuna_prom = sql^consulta_3_v_final_comuna_prom
df_res_ejercicio_3_v_final_comuna_prom.to_csv("df_res_ejercicio_3_v_final_comuna_prom.csv", index=False)


#Esta es la consulta para eliminar la fila vieja con valores absolutos de CABA
consulta_3_final_comuna_agg =   """
                                SELECT *
                                FROM "df_res_ejercicio_3_v.csv"
                                WHERE NOMDPTO != 'Promedio Comunas';
                                """

df_res_ejercicio_3_final_comuna_agg = sql^consulta_3_final_comuna_agg 

df_res_ejercicio_3_final_comuna_agg.to_csv("df_res_ejercicio_3_final_comuna_agg.csv", index=False)



#Esta es la consulta para pegar la fila nueva con valores promediados de CABA
consulta_3_final_comuna_agg_FINAL = """
                                    SELECT *
                                    FROM "df_res_ejercicio_3_final_comuna_agg.csv"
                                    UNION 
                                    SELECT *
                                    FROM "df_res_ejercicio_3_v_final_comuna_prom.csv";
                                    """
df_res_ejercicio_3_final_comuna_agg_FINAL = sql^ consulta_3_final_comuna_agg_FINAL

df_res_ejercicio_3_final_comuna_agg_FINAL.to_csv("df_res_ejercicio_3_final_comuna_agg_FINAL.csv", index=False)



# iv)
# cantidad de dominios gmail por departamentos
consulta_4_i =  """  
                SELECT id_departamento, dominio, COUNT(*) AS gmail
                FROM "df_bp_FIINAL_definitivo.csv"
                WHERE dominio = 'gmail'
                GROUP BY dominio, id_departamento;
                """

df_res_ejercicio_4_i = sql^ consulta_4_i

df_res_ejercicio_4_i.to_csv('df_res_ejercicio_4_i.csv', index=False)

# analogo pero con hotmail
consulta_4_ii =  """  
                SELECT id_departamento, dominio, COUNT(*) AS hotmail
                FROM "df_bp_FIINAL_definitivo.csv"
                WHERE dominio = 'hotmail'
                GROUP BY dominio, id_departamento;
                """

df_res_ejercicio_4_ii = sql^ consulta_4_ii

df_res_ejercicio_4_ii.to_csv('df_res_ejercicio_4_ii.csv', index=False)

# analago con yahoo
consulta_4_iii =  """  
                SELECT id_departamento, dominio, COUNT(*) AS yahoo
                FROM "df_bp_FIINAL_definitivo.csv"
                WHERE dominio = 'yahoo'
                GROUP BY dominio, id_departamento;
                """

df_res_ejercicio_4_iii = sql^ consulta_4_iii

df_res_ejercicio_4_iii.to_csv('df_res_ejercicio_4_iii.csv', index=False)



#unimos las consultas anteriores entre si

consulta_4_iv =  """
                SELECT DISTINCT *
                FROM "df_res_ejercicio_4_i.csv"
                LEFT OUTER JOIN "df_res_ejercicio_4_ii.csv"
                ON df_res_ejercicio_4_i.id_departamento = df_res_ejercicio_4_ii.id_departamento;
                """
df_res_ejercicio_4_iv = sql^ consulta_4_iv

df_res_ejercicio_4_iv.to_csv("df_res_ejercicio_4_iv.csv", index=False)


#unimos las tablas con todos los dominios 
consulta_4_v =  """
                SELECT DISTINCT *
                FROM "df_res_ejercicio_4_iv.csv"
                LEFT OUTER JOIN "df_res_ejercicio_4_iii.csv"
                ON df_res_ejercicio_4_iv.id_departamento = df_res_ejercicio_4_iii.id_departamento;
                """
df_res_ejercicio_4_v = sql^ consulta_4_v

df_res_ejercicio_4_v.to_csv("df_res_ejercicio_4_v.csv", index=False)


# vinculamos a la tabla anterior el departamento y provincia
consulta_4_vi =  """
                SELECT DISTINCT *
                FROM "df_res_ejercicio_4_v.csv"
                LEFT OUTER JOIN "df_departamentos_FINAL_DEFINITIVO_.csv"
                ON df_res_ejercicio_4_v.id_departamento = df_departamentos_FINAL_DEFINITIVO_.DPTO;
                """
df_res_ejercicio_4_vi = sql^ consulta_4_vi

df_res_ejercicio_4_vi.to_csv("df_res_ejercicio_4_vi.csv", index=False)


# seleccion de las columnas relevantes para el ejercicio para la comparacion del ejercicio
consulta_4_vii =  """
                SELECT DISTINCT Provincia, NOMDPTO, gmail, hotmail, yahoo
                FROM "df_res_ejercicio_4_vi.csv";
                """
df_res_ejercicio_4_vii = sql^ consulta_4_vii

df_res_ejercicio_4_vii.to_csv("df_res_ejercicio_4_vii.csv", index=False)

#generamos la columna del dominio mas frecuente en bp 
consulta_4_viii =  """
                SELECT *,
                CASE 
                WHEN gmail = GREATEST(gmail, hotmail, yahoo) THEN 'gmail'
                WHEN hotmail = GREATEST(gmail, hotmail, yahoo) THEN 'hotmail'
                WHEN yahoo = GREATEST(gmail, hotmail, yahoo) THEN 'yahoo'
                END AS "Dominio mas frecuente en BP"
                FROM "df_res_ejercicio_4_vii.csv";
                """
df_res_ejercicio_4_viii = sql^ consulta_4_viii

df_res_ejercicio_4_viii.to_csv("df_res_ejercicio_4_viii.csv", index=False)

# organizamos para la consulta final
consulta_4_ix =  """
                SELECT DISTINCT Provincia, NOMDPTO, "Dominio mas frecuente en BP"
                FROM "df_res_ejercicio_4_viii.csv";
                """
df_res_ejercicio_4_ix = sql^ consulta_4_ix

df_res_ejercicio_4_ix.to_csv("df_res_ejercicio_4_ix.csv", index=False)


############################################################################################################################################################
############################################################################ VISUALIZACION #################################################################
############################################################################################################################################################


tabla_SQL_ej_3 = pd.read_csv("df_res_ejercicio_3_v.csv") # Este archivo se uso en el ejercicio i) y iii)  


# i) Cantidad de Bibliotecas Populares por provincia

df_cantBP_x_provincia = tabla_SQL_ej_3[["Provincia","NOMDPTO","Cant_BP"]]  # Seleccionamos las columnas relevantes
bp_por_provincia = df_cantBP_x_provincia.groupby("Provincia", as_index=False)["Cant_BP"].sum()  # Agrupamos por provincia y sumamos la cantidad de BP
bp_por_provincia = bp_por_provincia.sort_values(by="Cant_BP", ascending=False)  # Ordenamos de mayor a menor

plt.figure(figsize=(12, 6))  # Ajustamos el tamaño del gráfico
sns.barplot(data=bp_por_provincia, x="Provincia", y="Cant_BP", palette="viridis")  # Creamos el gráfico de barras con la paleta viridis
plt.title("Cantidad de BP por Provincia (ordenado de mayor a menor)", fontsize=14)  # Agregamos título
plt.xlabel("Provincia")  # Etiqueta del eje X
plt.ylabel("Cantidad de BP")  # Etiqueta del eje Y
plt.xticks(rotation=45, ha="right")  # Rotamos las etiquetas para mejor legibilidad
plt.tight_layout()  # Ajustamos el diseño del gráfico
plt.show()  # Mostramos el gráfico


# ii) Cargar datos para analizar establecimientos educativos según nivel

df_ejercicioI = pd.read_csv("df_res_ejercicio_1_final_comuna_agg_FINAL.csv")  # Cargamos el archivo CSV con datos

# Establecer estilo de Seaborn
sns.set_style("whitegrid")  # Fondo de cuadrícula blanca para mejorar la legibilidad
sns.set_palette("muted")  # Colores suaves para el gráfico

# Crear la figura y los ejes
fig, ax = plt.subplots(figsize=(10, 6))  # Tamaño del gráfico

# Graficar Jardín
sns.scatterplot(
    x=df_ejercicioI['poblacion_jardin'],  # Población de nivel jardín
    y=df_ejercicioI['Jardines'],  # Cantidad de jardines
    color='tab:red',  # Color rojo para jardín
    label='Jardin 0-5',  
    s=40,  # Tamaño de los puntos aumentado para mejor visibilidad
    edgecolor='black',  # Borde negro para mayor contraste
    alpha=0.7  # Transparencia
)

# Graficar Primario
sns.scatterplot(
    x=df_ejercicioI['poblacion_primario'],  # Población de nivel primario
    y=df_ejercicioI['Primarios'],  # Cantidad de escuelas primarias
    color='tab:blue',  # Color azul para primario
    label='Primario 6-11',
    s=40,
    edgecolor='black',
    alpha=0.7
)

# Graficar Secundario
sns.scatterplot(
    x=df_ejercicioI['poblacion_secundario'],  # Población de nivel secundario
    y=df_ejercicioI['Secundarios'],  # Cantidad de escuelas secundarias
    color='tab:green',  # Color verde para secundario
    label='Secundario 12-18',
    s=40,
    edgecolor='black',
    alpha=0.7
)

# Ajustes de título y etiquetas
ax.set_title('Cantidad de EE por población, separados por grupo etario', fontsize=14, fontweight='bold')
ax.set_xlabel('Población', fontsize=12)
ax.set_ylabel('Cantidad de establecimientos educativos', fontsize=12)

# Configuración de leyenda y cuadrícula
ax.legend(title='Nivel Educativo')  # Agregamos leyenda con título
ax.grid(True, linestyle='--', alpha=0.7)  # Líneas de cuadrícula más sutiles
plt.xticks(fontsize=10)  # Ajustamos tamaño de etiquetas en eje X
plt.yticks(fontsize=10)  # Ajustamos tamaño de etiquetas en eje Y

plt.show()  # Mostramos el gráfico


# iii) Cantidad de EE por provincia y departamentos

# Selección de columnas relevantes
cantidad_escuelas_por_deptos_y_provincias = tabla_SQL_ej_3[["Provincia", "NOMDPTO", "Cant_EE"]]

# Calcular la mediana de cantidad de EE por provincia
mediana = cantidad_escuelas_por_deptos_y_provincias.groupby("Provincia")["Cant_EE"].median().sort_values()

# Obtener lista ordenada de provincias según la mediana
mediana_en_lista_ordenada = mediana.index.tolist()

# Graficar los boxplots por provincia
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(
    data=cantidad_escuelas_por_deptos_y_provincias,
    x="Provincia",
    y="Cant_EE",
    order=mediana_en_lista_ordenada,  # Ordenamos por la mediana calculada
    palette="pastel"  # Usamos una paleta de colores suaves
)

# Personalización del gráfico
ax.set_title("Cantidad de EE de cada departamento por provincia")
ax.set_xlabel("Provincias")
ax.set_ylabel("Cantidad de EE")
ax.set_yticks(np.arange(0, 2250, 200))  # Configuración de los valores del eje Y
ax.grid(True, axis="y")  # Agregamos líneas de cuadrícula en el eje Y
ax.tick_params(axis="x", rotation=90)  # Rotamos las etiquetas en el eje X para mayor legibilidad


# iv) Relación entre BP y EE por cada mil habitantes

# Cargar datos
res_sql3 = pd.read_csv("df_res_ejercicio_3_final_comuna_agg_FINAL.csv")

# Inicializar listas
relacion_BP = []
relacion_EE = []

# Calcular relación de EE y BP por cada mil habitantes
for indice, fila in res_sql3.iterrows():
    relacion_cantEE = (int(fila["Cant_EE"]) * 1000) / fila["poblacion_total"]
    relacion_EE.append(relacion_cantEE)
    
    relacion_cantBP = (int(fila["Cant_BP"]) * 1000) / fila["poblacion_total"]
    relacion_BP.append(relacion_cantBP)

# Agregar columnas al DataFrame
res_sql3["Relacion EE"] = relacion_EE
res_sql3["Relacion BP"] = relacion_BP

# Generación del gráfico de dispersión
plt.figure(figsize=(10, 7))

sns.set(style="whitegrid")  # Establecer fondo con grilla clara
scatter = sns.scatterplot(
    data=res_sql3,
    x="Relacion EE",
    y="Relacion BP",
    color="magenta",  # Color del gráfico
    edgecolor="black",
    s=40,
    alpha=0.7
)

# Configurar título y etiquetas
plt.title("Relación entre la cantidad de BP cada mil habitantes y de EE cada mil habitantes por departamento", fontsize=13)
plt.xlabel("Establecimientos Educativos cada mil habitantes", fontsize=11)
plt.ylabel("Bibliotecas Populares cada mil habitantes", fontsize=11)

# Ajustes de diseño
plt.tight_layout()
plt.show()



