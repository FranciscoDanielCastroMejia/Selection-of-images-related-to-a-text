#Prueba para abrir las imagenes por categoria
#--------------Import libraries-----------------
import os 
import json
import numpy as np
import requests
import torch
import PIL.Image
from transformers import AutoProcessor, PaliGemmaForConditionalGeneration
device = "cuda" if torch.cuda.is_available() else "cpu"
#___________________Libraries for the progress bar_____________________
import time
from progressbar import ProgressBar

#____________________Loading the model______________________________

model_id = "gokaygokay/sd3-long-captioner-v2"
print('pasa')
model = PaliGemmaForConditionalGeneration.from_pretrained(model_id).eval()#.to(device)
print('pasa0')

image_processor = AutoProcessor.from_pretrained(model_id)

# ___________Accesssing images from the web or the files___________

#Headers for wikimedia

headers = {
  'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI1ZGNmOWIxYTBlNDFmZTE3ZjYxMjYwMTY3NDM2ZmNjYSIsImp0aSI6ImZmMDVkYjIxOWFlMTJhNWRiOWY0ZTU4NTFlNWI3NTEzY2QwM2JhYTkyM2NmZjNkZTdjMWJlYTc4YTUzODg2ZGFkMWZjNjY5Y2EyZGY4Yjc4IiwiaWF0IjoxNzEzODE1Mjk4LjIyNzIwMiwibmJmIjoxNzEzODE1Mjk4LjIyNzIwNSwiZXhwIjozMzI3MDcyNDA5OC4yMjU1OSwic3ViIjoiNzUyMjAwOTQiLCJpc3MiOiJodHRwczovL21ldGEud2lraW1lZGlhLm9yZyIsInJhdGVsaW1pdCI6eyJyZXF1ZXN0c19wZXJfdW5pdCI6NTAwMCwidW5pdCI6IkhPVVIifSwic2NvcGVzIjpbImJhc2ljIiwiY3JlYXRlZWRpdG1vdmVwYWdlIl19.klqz-hpRMnLhqORQAOY7QNxash20FAM9wX3IxsV7_QtLRBLx83VUIb_22oJG9_w-gi0A_cQ9fw8GCKp4Hfp0Z7fJsT9ragbs2bJp6o9ztowx4BrN32QhPEXAU9C-pjC6WsbpnFUzKRnZwz3_Kj4NxCXVQMsB6kKhyjTX-KutdoAE7YVvl-g13AviUhFjitNMVW7KZIJkK9hd1N2GI5gtc75gkjvDSRjr1pTubJXl8lzqWfpi9IjovoujhKe_0N8_i0dOlwLoRhcNaWoTJ22O7o4Fcku4aWFgnlLJF7Q0ZjVsHiCr9h1_OX7xlduApuj0m6qaCokU2PEwKdgfEKHRm1V9mjY7ANl3BJrT9JDMo_BvJiKkuhheyJY6RENEqLwvWinfW87aWPdp-9kn07i6o-vytLnEC093YdwYARdvZhftUHgdsmE0LsMWBWoKIUcux8FXcRtgTKCZ3AHNJ2ik3Gu5vQWzl4jKd6cKuAOp-jvgLkuUUR-ateSFrmx9gyPhjWVPkl4jSekGqRHYJE3no8yAbk4v5yYjRvfWbvYKKLtmQ4GuLMhLxfJX6WOfnzzDHpq2LXKjUpIMhdFxcpebVEKtY7mPfoeZCvYSkMZQB10Kbk4XiWUPUJ125xKr4A3r4Ai8Nxyk-DbJzxjo-POfUSMm9UO_2WLWCIYbCrEahwo',
  'User-Agent': 'MithozZfg'
}

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



if __name__=='__main__':


    #path of the folder
    folder = '/media/mitos/nuevo ssd/BASE DE DATOS LINKS/Astronomy'

    #Iterate over files in folder 

    images = 0
    cont = 0


    for file in os.listdir(folder): #file es el nombre de cada archivo de la carpeta 
        if file.endswith('.json'):
            filepath = os.path.join(folder, file) #filepath es la direccion COMPLETA del archivo json
            with open(filepath, 'r') as f: 
                subcategory = json.load(f) #subcategory es el diccionario con los links de las subcategorias

                if(len(subcategory) == 0): #si la base de datos esta vacia no se hacen captions
                    #print(f"{file} Tiene 0 elementos")
                    cont = cont +1
                else:
                    #aqui se hace el codigo de caption
                    print(f'Cantidad de imagenes de {file[:-5]}: {len(subcategory)}') #numero de imagenes por subcategoria
                    images = images + len(subcategory)

                    captions = {} #lista para guardar todos los captions
                    print("START")
                    barra = ProgressBar(maxval=len(subcategory)).start()

                    for i, link in enumerate(subcategory):
                        imagen_path = link
                        #se descarga en catche la imagen
                        image = load_image(imagen_path)

                        prompt = "Caption en"
                        model_inputs = image_processor(text=prompt, images=image, return_tensors="pt").to(device)
                        input_len = model_inputs["input_ids"].shape[-1]
                        with torch.inference_mode():

                            generated_tokens = model.generate(**model_inputs, repetition_penalty=1.10, max_new_tokens=256, do_sample=False).to(device) #aqui se genera un tensor con tokens 
                            
                            with torch.no_grad():
                                output = model(**model_inputs, output_hidden_states=True)

                            generated_tokens_word = generated_tokens[0][input_len:]
                            decoded = image_processor.decode(generated_tokens_word, skip_special_tokens=True)
                            CAPTION = decoded  
                            #CAPTION = get_caption(model, image_processor, tokenizer, imagen_path)
                            captions[link] = CAPTION    
                        
                        barra.update(i) #increment the counter

                        with open(f'Links_captions_{file[:-5]}.json', 'w')as file:
                            json.dump(captions, file, indent=4)
                    
                    barra.finish()

    print(f'Cantidad de imagenes: {images}')
    print(f'Catnidad de DB vacias: {cont}')



        

    
        