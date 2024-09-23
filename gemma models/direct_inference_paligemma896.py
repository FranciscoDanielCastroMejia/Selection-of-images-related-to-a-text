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

model_id = "google/paligemma-3b-pt-896"
device = "cpu"
#device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.bfloat16


print("PAAAAASAAAAAAA2")
print('\n')


model = PaliGemmaForConditionalGeneration.from_pretrained(
    model_id,
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
        return PIL.Image.open(requests.get(image_path, headers=headers, stream=True).raw)
    elif os.path.exists(image_path):
        return PIL.Image.open(image_path)
    

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
    imagen_path = '/home/mitos/Documentos/AVANCE JULIO/exponiendo.jpg'

    
            
    #se descarga en catche la imagen
    image = load_image(imagen_path)
    print("pasa3")

    prompt = "What does this image show?"
    model_inputs = image_processor(text=prompt, images=image, return_tensors="pt").to(model.device)
    input_len = model_inputs["input_ids"].shape[-1]

    print("pasa4")
    with torch.inference_mode():
        generation = model.generate(**model_inputs, repetition_penalty=1.10, max_new_tokens=256, do_sample=False)
        generation = generation[0][input_len:]
        decoded = image_processor.decode(generation, skip_special_tokens=True)
        CAPTION = decoded  
        #CAPTION = get_caption(model, image_processor, tokenizer, imagen_path)
        captions.append(CAPTION)

    print(captions)