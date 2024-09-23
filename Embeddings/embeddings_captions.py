#PROGRAMA PARA SACAR EMBEDDING DE LA BASE DE DATOS DE ONLY_LINKS_CAPTIONS.JSON
#CREANDO LA BASE DE DATOS DE LINKS CAPTION EMBEDDINGS


#este programa no se utilizara, en la version final, los embeddings se haran directo desde el programa prinicpal del image captioning
#este programa es para hacer la prueba en el avance, y se sacaran ,los embeddings de los captions que ya se tienen


from transformers import AutoTokenizer, RobertaModel
import torch
import torch.nn.functional as F
import numpy as np
import json
import os
##___________________Libraries of the embeddings_____________________
import embedder

#___________________Libraries for the progress bar_____________________
import time
from progressbar import ProgressBar

#_________________initialize the device______________________________

device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)


#________________here we choose which embedder we will use_____________

types = ["rta_cls", "rta_mp", "st_cls", "st_mp"]

type_of_embedder = types[0]


#we load the data base and create the new one f it doesnt exist

if os.path.exists('BD Sistema Img Caption/only_links_captions.json'):
    #if the data base exists, only open
    with open('BD Sistema Img Caption//only_links_captions.json', 'r') as file:
        data_base = json.load(file)
    
else:
    #if it doesnt exist we create
    with open('BD Sistema Img Caption//hash_paths_blog.json', 'r') as file:
        data = json.load(file)
    
    data_base = {link: values["caption"] for link, values in data.items()}#creamos una nueva base de datos donde solo tenga la forma de link:caption
    
    with open('BD Sistema Img Caption//only_links_captions.json','w') as file:
        json.dump(data_base, file, indent=4)



new_database = {}

#________________________________________________

print('START')

indice = 0 #contador para la barra de progreso
barra = ProgressBar(maxval=len(data_base.keys())).start()

for link, text in data_base.items():

    embedding = embedder.embedder(text,type_of_embedder) #ya regresa el embedding normalizado
    embedding = embedding.tolist()
    new_database[link] = embedding
    barra.update(indice) #increment the counter
    indice = indice + 1

barra.finish()

#Here we save the new database with the links and the embbedings

path = embedder.path(type_of_embedder, "caption")


with open(path,'w') as file:
    json.dump(new_database, file, indent=4)