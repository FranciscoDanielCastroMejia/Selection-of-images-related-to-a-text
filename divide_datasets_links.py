#In this program we will create 8 groups of image links from the dataset that contain all the image 
# links, but we will only take the links that have not been captioned

import json
import os
import numpy as np


#Aqui se crearan los conjuntos de 8

folder_path = 'ANALYSIS/BASE DE DATOS LINKS PARTIDOS 8'

categories = os.listdir(folder_path) #lista con los archivos JSON de cada categoria partida en 8

#creamos un diccionario, en donde estaran los 8 contenedores de imagenes

contenedor_total = {'part_1':[],
                    'part_2':[],
                    'part_3':[],
                    'part_4':[],
                    'part_5':[],
                    'part_6':[],
                    'part_7':[],
                    'part_8':[],
                    }


cont_links_total = 0
#categories = ['Computer Science and Informatics.json', 'Chemistry.json']
for cat in categories:

    cat_json_path = os.path.join(folder_path, cat)
    with open(cat_json_path, 'r') as file:
        category_in_parts = json.load(file)

    for i in range(8):#se itera sobre las 8 partes
        contenedor_total[f'part_{i+1}'] = list(set(category_in_parts[f'parte_{i+1}'] + contenedor_total[f'part_{i+1}']))
        #print(len(contenedor_total[f'part_{i+1}']))
        if cat == 'Sociology and Anthropology.json':
            cont_links_total += len(contenedor_total[f'part_{i+1}'])

for i in range(8):
    
    contenedor_individual = contenedor_total[f'part_{i+1}']
    with open(f'ANALYSIS/BASE DE DATOS CONTENEDOR TOTAL/contenedor_individual_{i+1}.json','w')as file:
        json.dump(contenedor_individual, file, indent=4)

print(cont_links_total)



#En este Codigo se dividen las listas de cada categoria en 8 partes

"""folder_path = 'ANALYSIS/BASE DE DATOS LINKS SIN SUBCATEGORIAS'

categories = os.listdir(folder_path)

for cat in categories:
    print(cat)
    category_path = os.path.join(folder_path, cat)
    with open(category_path, 'r') as file:
            categoria_json = json.load(file) #lista de links 

    partes = np.array_split(categoria_json, 8)
    partes = [list(parte) for parte in partes]


    partes_dict = {f'parte_{i+1}': parte for i, parte in enumerate(partes)}


    with open(f'ANALYSIS/BASE DE DATOS LINKS PARTIDOS 8/{cat}','w')as file:
            json.dump(partes_dict, file, indent=4)"""




#En esta parte de codigo se juntan todas las subcategorias (archivos json) en una sola categoria
#(un solo archivo json por categoria), eliminando imagenes repetidas. 
"""
folder_path = 'ANALYSIS/BASE DE DATOS LINKS'

#Categories that has been captured
cat_captured = ['Physics','Geography and Earth Sciences','Energy and Resources','Business', 'Astronomy' ]

#_________________CATEGORIES_______________________________
categories = [nombre for nombre in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, nombre)) and nombre not in cat_captured ]
print(categories)
print(len(categories))



categorias_num_img = {}

for cat in categories:
    
    cont_imgs_per_cat = 0 
    cat_folder_path = os.path.join(folder_path, cat)
    list_subcat = os.listdir(cat_folder_path)
    print(f'Analizando datos de la categoria: {cat}')
    archivo_json_categoria = []
    

    for subcat in list_subcat:#aqui se itera por cada archivo json de cada categoria


        sub_cat_folder_path = os.path.join(cat_folder_path, subcat)
        with open(sub_cat_folder_path, 'r') as file:
            links = json.load(file)
            for link in links:
                if link in archivo_json_categoria: #si el link se encuentra en el arreglo no lo guardes
                    continue
                else:
                    archivo_json_categoria.append(link)
                    cont_imgs_per_cat += 1
                
    with open(f'ANALYSIS/BASE DE DATOS LINKS SIN SUBCATEGORIAS/{cat}.json','w')as file:
        json.dump(archivo_json_categoria, file, indent=4)
    
    categorias_num_img[cat] = cont_imgs_per_cat

print(categorias_num_img)

with open(f'ANALYSIS/categorias_num_img.json','w')as file:
        json.dump(categorias_num_img, file, indent=4)"""


            

            
    