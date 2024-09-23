#In this program is created the database that will contain the links of the images and its embedding associated. 
#----------------------------------------------------------------------------------------

from transformers import AutoTokenizer, RobertaModel
import torch
import torch.nn.functional as F
import numpy as np
import json

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

type_of_embedder = types[3]



#________________________________________________
#________________________________________________

#we load the data base and create the new one

with open('BD Sistema Img Caption/links_article_TS.json', 'r') as file:
    data_base = json.load(file)

new_database = {}

#________________________________________________
#________________________________________________
#________________________________________________

print('START')

indice = 0 #contador para la barra de progreso
barra = ProgressBar(maxval=len(data_base.keys())).start()

for link, text in data_base.items():

    embedding = embedder.embedder(text, type_of_embedder) #ya regresa el embedding normalizado // AQUI ELEGIMOS QUE EMBEDDING USAR
    embedding = embedding.tolist()
    new_database[link] = embedding
    barra.update(indice) #increment the counter
    indice = indice + 1

barra.finish()

#________________________________________________
#________________________________________________
#Here we save the new database with the links and the embbedings

path = embedder.path(type_of_embedder, "article")


with open(path,'w') as file:
    json.dump(new_database, file, indent=4)
