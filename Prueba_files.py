#programa prueba par ver que carpetas contienen datos y cuales no contienen
#al igual que contabilizar todas las imagenes que existen.

import os 
import json

path_folder = '/media/mitos/nuevo ssd/IMG Captions'
#path_folder = '/media/mitos/nuevo ssd/BASE DE DATOS LINKS'

cont_imagenes_totales = 0
cont_imagenes_subcat = 0
cont_carpetas_llenas = 0
cont = 0

for carpeta_cat in os.listdir(path_folder):#carpetas donde vienen categorias (animales, matematicas etc)
    path_folder_cat = os.path.join(path_folder, carpeta_cat)
    if os.listdir(path_folder_cat): #verificar si la carpeta cuenta con archivos en ella
        print(f'La carpeta {carpeta_cat} tiene archivos')
        cont_carpetas_llenas = cont_carpetas_llenas + 1
        for archivo_sub in os.listdir(path_folder_cat): #archivos JSON con la subcategorias: (perros, gatos)
            
            file_path = os.path.join(path_folder_cat,archivo_sub)
            with open(file_path, 'r') as file:
                subcategory = json.load(file)
            
            cont_imagenes_subcat = cont_imagenes_subcat + len(subcategory)
            if carpeta_cat == 'Geography and Earth Sciences':
                #print(len(subcategory))
                cont = cont +1
            

        print(f'Cantidad de imagenes de {carpeta_cat}: {cont_imagenes_subcat}')
        print('\n')
        
        cont_imagenes_totales = cont_imagenes_totales + cont_imagenes_subcat
        cont_imagenes_subcat = 0


print('\n')
print(f'Imagenes Totales: {cont_imagenes_totales}')
print(f'Carpetas con imagenes: {cont_carpetas_llenas}')
print(cont)
