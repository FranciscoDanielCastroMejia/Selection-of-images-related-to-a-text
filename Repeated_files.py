#programa prueba para ver que carpetas contienen datos y cuales no contienen
#al igual que contabilizar todas las imagenes que existen.
#Funcion para Juntar todas las categorias en una base de datos GLOBAL
#Unir la base de datos de los articulos con la GLOBAL

import os 
import json



#______________Function to know the number of images_____________
def count_images(path_folder):

    cont_imagenes_totales = 0
    cont_imagenes_subcat = 0
    cont_carpetas_llenas = 0
    cont = 0

    for carpeta_cat in os.listdir(path_folder):#carpetas donde vienen categorias (animales, matematicas etc)
        path_folder_cat = os.path.join(path_folder, carpeta_cat)
        if os.listdir(path_folder_cat): #verificar si la carpeta cuenta con archivos en ella
            print(f'La carpeta {carpeta_cat} tiene archivos')
            cont_carpetas_llenas = cont_carpetas_llenas + 1
            for archivo_sub in os.listdir(path_folder_cat): #archivo_sub: JSON de las subcategorias: (perros, gatos)
                
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


#_____________Function to join all the images-captions in one dataset__________

#tres ciclos for: 
#El primero itera sobre las categorias (animals, physics, astronomi, etc)
#El segundo itera sobre cada subcategoria (dogs, cats, elephants, etc)
#El tercero itera sobre cada archivo .json 



def join_captions(path_folder):

    repeated_imgs = 0 

    DB_all_captions = {}

    for carpeta_cat in os.listdir(path_folder):#carpetas donde vienen categorias (animales, matematicas etc)
        path_folder_cat = os.path.join(path_folder, carpeta_cat)
        if os.listdir(path_folder_cat): #verificar si la carpeta contiene captions en ella
            
            for archivo_sub in os.listdir(path_folder_cat): #archivo_sub: name of JSON file of the subcategorias: (perros, gatos)
                
                file_path = os.path.join(path_folder_cat,archivo_sub)#create the path of the specific json file.
                with open(file_path, 'r') as file:
                    subcategory = json.load(file) #subcategory: json file transformed to a dictionary
                
                #here we create the dictionary
                for link, caption in subcategory.items():
                #for link in subcategory:
                    #here we verify if the link of the image has been added before 
                    if link in DB_all_captions:
                        print(f"Link previamente agregado: {link}")
                        repeated_imgs = repeated_imgs + 1
                    else: #if the link has not been added before, we add it to the new database
                        DB_all_captions[link] = caption
    
    with open('BD New Dataset/DB_wiki_links_captions.json', 'w')as file:
        json.dump(DB_all_captions, file, indent=4)
            

    
    print(f"Size of the DB with all captions: {len(DB_all_captions)}")
    print(f"Number of repeated_img: {repeated_imgs}")



def combine_datasets(path_dataset1:str, path_dataset2:str): #El dataset1 se unira al dataset2 
    
    with open(path_dataset1, 'r') as file:
        dataset1 = json.load(file) 
    with open(path_dataset2, 'r') as file:
        dataset2 = json.load(file)
    
    print(f'Size of Dataset1: {len(dataset1)}')
    print(f'Size of Dataset2: {len(dataset2)}')

    cont_img_repeated = 0
    #dataset1 and dataset2 are dicctionariesm their format is link:"caption"

    for link, caption in dataset1.items():

        if link not in dataset2: #if the link doesnt exist in the dataset2 add all the element in the dataset 2
            dataset2[link] = caption
        else:
            cont_img_repeated += 1  
    
    

    with open('BD New Dataset/DB_GLOBAL_links_captions.json','w')as file:
        json.dump(dataset2, file, indent=4)
        
    print(f'Nummber of images repeated: {cont_img_repeated}')
    print(f'Size of the new Dataset3: {len(dataset2)}')






if __name__=='__main__':


    path_captions = '/media/mitos/nuevo ssd/IMG Captions' #Data bases with links and captions
    path_all_images = '/media/mitos/nuevo ssd/BASE DE DATOS LINKS' #data bases with all the links of the images
    
    
    path_dataset1 = 'BD Dataset Articles/only_links_captions.json'
    path_dataset2 = 'BD New Dataset/DB_wiki_links_captions.json'


    #count_images(path_captions) 
    #join_captions(path_captions)
    combine_datasets(path_dataset1,path_dataset2)

    





