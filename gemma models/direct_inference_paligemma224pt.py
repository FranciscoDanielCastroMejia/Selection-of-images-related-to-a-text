#In this program you will find a image captioning program that use images
#from the wikimedia commons API.

#____________General libraries______________________________
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import spacy 
import numpy as np
from transformers import pipeline
import requests
import argparse

#_____________libraries for wikibot_________________________________
import json
import pywikibot
from pywikibot import pagegenerators
from pathlib import Path
from wikibot import * #importamos todas las funciones del wikibot
import urllib

#_____________libraries for create hash tables_________________________________
from create_hash_dict import *


#______________libraries for text classification__________________
#from Text_classification import *
from Text_classification2 import *

#______________libraries for Image Captioning______________________
# Backend
import torch
# Image Processing
#from PIL import Image
import PIL.Image
# Transformer and pre-trained Model
from transformers import AutoProcessor, PaliGemmaForConditionalGeneration
# Managing loading processing
from tqdm import tqdm
# Assign available GPU


#___________________Libraries for the progress bar_____________________
import time
from progressbar import ProgressBar

#___________________________________________________________________

#____________________Loading the model______________________________


print("PAAAAASAAAAAAA1")
print('\n')
access_token = "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"

model_id = "google/paligemma-3b-pt-224"
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.bfloat16



print("PAAAAASAAAAAAA2")
print('\n')


model = PaliGemmaForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=dtype,
    device_map=device,
    revision="bfloat16",
    token=access_token
).eval()

print("PAAAAASAAAAAAA3")
print('\n')


image_processor = AutoProcessor.from_pretrained(model_id, token=access_token)

print("PAAAAASAAAAAAA4")
print('\n')



# ___________Accesssing images from the web or the files___________

#Headers for wikimedia

headers = {
  'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI1ZGNmOWIxYTBlNDFmZTE3ZjYxMjYwMTY3NDM2ZmNjYSIsImp0aSI6ImZmMDVkYjIxOWFlMTJhNWRiOWY0ZTU4NTFlNWI3NTEzY2QwM2JhYTkyM2NmZjNkZTdjMWJlYTc4YTUzODg2ZGFkMWZjNjY5Y2EyZGY4Yjc4IiwiaWF0IjoxNzEzODE1Mjk4LjIyNzIwMiwibmJmIjoxNzEzODE1Mjk4LjIyNzIwNSwiZXhwIjozMzI3MDcyNDA5OC4yMjU1OSwic3ViIjoiNzUyMjAwOTQiLCJpc3MiOiJodHRwczovL21ldGEud2lraW1lZGlhLm9yZyIsInJhdGVsaW1pdCI6eyJyZXF1ZXN0c19wZXJfdW5pdCI6NTAwMCwidW5pdCI6IkhPVVIifSwic2NvcGVzIjpbImJhc2ljIiwiY3JlYXRlZWRpdG1vdmVwYWdlIl19.klqz-hpRMnLhqORQAOY7QNxash20FAM9wX3IxsV7_QtLRBLx83VUIb_22oJG9_w-gi0A_cQ9fw8GCKp4Hfp0Z7fJsT9ragbs2bJp6o9ztowx4BrN32QhPEXAU9C-pjC6WsbpnFUzKRnZwz3_Kj4NxCXVQMsB6kKhyjTX-KutdoAE7YVvl-g13AviUhFjitNMVW7KZIJkK9hd1N2GI5gtc75gkjvDSRjr1pTubJXl8lzqWfpi9IjovoujhKe_0N8_i0dOlwLoRhcNaWoTJ22O7o4Fcku4aWFgnlLJF7Q0ZjVsHiCr9h1_OX7xlduApuj0m6qaCokU2PEwKdgfEKHRm1V9mjY7ANl3BJrT9JDMo_BvJiKkuhheyJY6RENEqLwvWinfW87aWPdp-9kn07i6o-vytLnEC093YdwYARdvZhftUHgdsmE0LsMWBWoKIUcux8FXcRtgTKCZ3AHNJ2ik3Gu5vQWzl4jKd6cKuAOp-jvgLkuUUR-ateSFrmx9gyPhjWVPkl4jSekGqRHYJE3no8yAbk4v5yYjRvfWbvYKKLtmQ4GuLMhLxfJX6WOfnzzDHpq2LXKjUpIMhdFxcpebVEKtY7mPfoeZCvYSkMZQB10Kbk4XiWUPUJ125xKr4A3r4Ai8Nxyk-DbJzxjo-POfUSMm9UO_2WLWCIYbCrEahwo',
  'User-Agent': 'MithozZfg'
}

print("pasa2")

import urllib.parse as parse
import os
# Verify url
def check_url(string):
    try:
        result = parse.urlparse(string)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False


# Load an image
def load_image(image_path):
    if check_url(image_path):
        respuesta = requests.get(image_path, headers=headers, stream=True)#.raw
        #respuesta = urllib.request.Request(image_path)#, stream=True)
        #print('El request da:{}'.format(respuesta.status_code))
        #print('El request da:{}'.format(respuesta))
        #print('\n')
        return PIL.Image.open(requests.get(image_path, headers=headers, stream=True).raw)
        #return PIL.Image.open(urllib.request.urlopen(respuesta).read(), "rb")
        #return PIL.Image.open(image_path)
    elif os.path.exists(image_path):
        return PIL.Image.open(image_path)
    
#________________Image Inference________________________________________

def get_caption(model, image_processor, tokenizer, image_path):
    image = load_image(image_path)
    # Preprocessing the Image
    img = image_processor(image, return_tensors="pt").to(device)
    # Generating captions
    output = model.generate(**img).to(device)
    # decode the output
    caption = tokenizer.batch_decode(output, skip_special_tokens=True)[0]
    return caption

#______________________Open the program from terminal_____________________

# Generate new caption from input image
parser = argparse.ArgumentParser(description="Image Captioning")
parser.add_argument('--category', help="Category you want to work")
parser.add_argument('--iteration', type=int, default=10, help="Number of the images to work")

CATEGORY = parser.parse_args().category
ITERATIONS = parser.parse_args().iteration 




if __name__=='__main__':
    

    #________________________________________________________________________________
    #________________________________________________________________________________
    #_________A continuación se generarán los CAPTIONS de cada imagen________________
    #________________________________________________________________________________
    #________________________________________________________________________________


     
    
    captions = [] #lista para guardar todos los captions
    #imagen_path = '/home/mitos/Documentos/AVANCE JULIO/exponiendo.jpg'
    imagen_path = "https://upload.wikimedia.org/wikipedia/commons/9/9d/NYC_Montage_2014_4_-_Jleon.jpg"
    
            
    #se descarga en catche la imagen
    image = load_image(imagen_path)
    print("pasa3")

    prompt = "caption en"
    #prompt = "what does the text say?"
    model_inputs = image_processor(text=prompt, images=image, return_tensors="pt").to(model.device)
    input_len = model_inputs["input_ids"].shape[-1]

    print("pasa4")
    with torch.inference_mode():
        generation = model.generate(**model_inputs, repetition_penalty=1.10, max_new_tokens=130, do_sample=False)
        generation = generation[0][input_len:]
        decoded = image_processor.decode(generation, skip_special_tokens=True)
        CAPTION = decoded  
        #CAPTION = get_caption(model, image_processor, tokenizer, imagen_path)
        captions.append(CAPTION)

    print(captions)
    
    """
    #________________________________________________________________________________
    #________________________________________________________________________________
    #____________En esta parte se hará el text clasification_________________________ 
    #________________________________________________________________________________
    #________________________________________________________________________________


    barra3 = ProgressBar(maxval=len(captions)).start()  # Inicializar la barra de progreso
    
    #definimos las tablas a crear:
    hash_paths = {}
    hash_diccionario = {}


    for indice3, caps in enumerate(captions):
        


        text = caps
        #________________________________________________________________________________
        #________________________________________________________________________________
        #_________Aqui se clasifica el caption generado por el modelo____________________
        #________________________________________________________________________________

        POS = image_classification2(text) 
        #"prueba" es un diccionario donde se tiene almacenado el POS de cada caption
        #por individual

        #________________________________________________________________________________
        #________________________________________________________________________________
        #__________Here we make the sentiment analysis___________________________________
        #________________________________________________________________________________


        doc = nlp(text)
        text_tokens = [token.text for token in doc]
        preprocessed_sentence = " ".join(text_tokens)
        sentiment = sentiment_analysis(preprocessed_sentence)# AQUI FALTA CORREGIR
        
        #________________________________________________________________________________
        #________________________________________________________________________________
        #_____________________Here we create the hash table for paths_____________________________
        #________________________________________________________________________________

        agregar_link(hash_paths, imagen_path,captions[indice3], POS["NOUN"], POS["VERB"], POS["ADJ"], POS["ADV"], POS["PROPN"], "POSITIVE" )

        
        #incremento de la barra de progreso
        
        barra3.update(indice3) #increment the counter

    barra3.finish()

    #Teniendo la tabla hash con los paths, se crea la segunda tabla hash para el diccionario


    #________________________________________________________________________________
    #________________________________________________________________________________
    #_________________________here we create the hash for dictionary___________
    #________________________________________________________________________________


    for link, items in hash_paths.items():
        
        for item in items:

            #En esta parte accedemos al elemento del subdiccionario
            if(item == 'caption' or item == 'sentiment'):
                continue

            for word in hash_paths[link][item]:

                if( hash_diccionario.get(word) == None):
                    hash_diccionario[word] = [link]
                    
                else:
                    hash_diccionario[word].append(link)


    #Primero se busca si existen las bases de datos (diccionarios), si existe se carga, si no se 
    #se guardan los nuevos datos sin agregar al otro diccionario.

    try:
        with open('hash_diccionario_paligemma.json', 'r') as archivo:
            diccionario = json.load(archivo)
        diccionario.update(hash_diccionario) #actualizamos los nuevos del programa

        with open('hash_paths_paligemma.json', 'r') as archivo:
            direcciones = json.load(archivo) 
        direcciones.update(hash_paths)

    except FileNotFoundError:
        # Si el archivo no existe, creamos un diccionario vacío y le agregamos los valores nuevos
        diccionario = {}
        diccionario.update(hash_diccionario)
        direcciones = {}
        direcciones.update(hash_paths)

    #En esta parte guardamos las bases de datos con los valores actualizados
    with open('hash_diccionario_paligemma.json', 'w') as file:
        json.dump(diccionario, file, indent=4)

    with open('hash_paths_paligemma.json', 'w') as file:
        json.dump(direcciones, file, indent=4)


"""
    print("FIN")