#En este programa desplegamos las imagenes de los resultados de los diferentes embeddings y los guardamos

import matplotlib.pyplot as plt
import json
import PIL.Image
from PIL import ImageEnhance
import requests
import matplotlib.patches as patches
import torch
import urllib.parse as parse
import os
from look_dict2 import look_dict2


#_________________initialize the device______________________________

device = "cuda" if torch.cuda.is_available() else "cpu"
 

#Headers for wikimedia

headers = {
  'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI1ZGNmOWIxYTBlNDFmZTE3ZjYxMjYwMTY3NDM2ZmNjYSIsImp0aSI6ImZmMDVkYjIxOWFlMTJhNWRiOWY0ZTU4NTFlNWI3NTEzY2QwM2JhYTkyM2NmZjNkZTdjMWJlYTc4YTUzODg2ZGFkMWZjNjY5Y2EyZGY4Yjc4IiwiaWF0IjoxNzEzODE1Mjk4LjIyNzIwMiwibmJmIjoxNzEzODE1Mjk4LjIyNzIwNSwiZXhwIjozMzI3MDcyNDA5OC4yMjU1OSwic3ViIjoiNzUyMjAwOTQiLCJpc3MiOiJodHRwczovL21ldGEud2lraW1lZGlhLm9yZyIsInJhdGVsaW1pdCI6eyJyZXF1ZXN0c19wZXJfdW5pdCI6NTAwMCwidW5pdCI6IkhPVVIifSwic2NvcGVzIjpbImJhc2ljIiwiY3JlYXRlZWRpdG1vdmVwYWdlIl19.klqz-hpRMnLhqORQAOY7QNxash20FAM9wX3IxsV7_QtLRBLx83VUIb_22oJG9_w-gi0A_cQ9fw8GCKp4Hfp0Z7fJsT9ragbs2bJp6o9ztowx4BrN32QhPEXAU9C-pjC6WsbpnFUzKRnZwz3_Kj4NxCXVQMsB6kKhyjTX-KutdoAE7YVvl-g13AviUhFjitNMVW7KZIJkK9hd1N2GI5gtc75gkjvDSRjr1pTubJXl8lzqWfpi9IjovoujhKe_0N8_i0dOlwLoRhcNaWoTJ22O7o4Fcku4aWFgnlLJF7Q0ZjVsHiCr9h1_OX7xlduApuj0m6qaCokU2PEwKdgfEKHRm1V9mjY7ANl3BJrT9JDMo_BvJiKkuhheyJY6RENEqLwvWinfW87aWPdp-9kn07i6o-vytLnEC093YdwYARdvZhftUHgdsmE0LsMWBWoKIUcux8FXcRtgTKCZ3AHNJ2ik3Gu5vQWzl4jKd6cKuAOp-jvgLkuUUR-ateSFrmx9gyPhjWVPkl4jSekGqRHYJE3no8yAbk4v5yYjRvfWbvYKKLtmQ4GuLMhLxfJX6WOfnzzDHpq2LXKjUpIMhdFxcpebVEKtY7mPfoeZCvYSkMZQB10Kbk4XiWUPUJ125xKr4A3r4Ai8Nxyk-DbJzxjo-POfUSMm9UO_2WLWCIYbCrEahwo',
  'User-Agent': 'MithozZfg'
}

#____________________________________________________________________________________
# ____________________________Verify url_____________________________________________
#____________________________________________________________________________________
def check_url(string):
    try:
        result = parse.urlparse(string)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False
#____________________________________________________________________________________
#_____________________________Load an image________________________________________
#__________________________________________________________________________________
def load_image(image_path):
    if check_url(image_path):
        respuesta = requests.get(image_path, headers=headers, stream=True)#.raw
        return PIL.Image.open(requests.get(image_path, headers=headers, stream=True).raw)
    elif os.path.exists(image_path):
        return PIL.Image.open(image_path)
#____________________________________________________________________________________
#______function to create a rectangle in the imagen depending of the time that is repeated
#___________________________________________________________________________________________________________

def rectange(peso, width, height, marco_ancho): #los parametros de entrada son las veces que se repite la imagen, su ancho y alto. 
    
    color_result = ['red', 'orange', 'yellow', 'green']
    rect = patches.Rectangle(
        (0, 0), 
        width, 
        height, 
        linewidth=marco_ancho, 
        edgecolor=color_result[peso], 
        facecolor='none'
    )
    return rect



#-En esta parte crearemos las bases de datos donde vienen los productos cosenos con el texto qeu queremos ingresar
text = "The number of motor vehicles in San Luis Potos\u00ed is growing rapidly. In 1988 little more than 66,000 vehicles were circulating in our city, this one year. This increase is in sharp contrast to the corresponding increase in the population of the city of less than 100% in the same period."
#dataset = "caption_art" #elegir el dataset para los captions con el articulo
#dataset = "caption_wiki" #elegir el dataset para los captions con el dataset wikimedia
dataset = "GLOBAL" #elegir el dataset para los captions con el dataset GLOBAL (wikimedia + articulo)
look_dict2(text,dataset ) #funcion para crear las bases de datos



#_______here we load all the data bases of the links with their product cosine_______


with open('BD pesos look dict/lnk_pesos_emb_rta-cls.json', 'r') as file:
    pesos_rb_cls = json.load(file)
with open('BD pesos look dict/lnk_pesos_emb_rta-mp.json', 'r') as file:
    pesos_rb_mp = json.load(file)
with open('BD pesos look dict/lnk_pesos_emb_st-cls.json', 'r') as file:
    pesos_st_cls = json.load(file)
with open('BD pesos look dict/lnk_pesos_emb_st-mp.json', 'r') as file:
    pesos_st_mp = json.load(file)

#____importaremos la base de datos donde es encuentran lso articulos con su resumen correspondiente

with open('BD Dataset Articles/links_article_TS.json', 'r') as file:
    art = json.load(file)

#invertimos las llaves por los valores del diccionario para que la busqueda sea mas eficiente, sabiendo qeu los articulos no se repiten
articles = {valor: llave for llave, valor in art.items()}

#ahora buscaremos el link de la imagen dependiendo el texto que se ingreso para generar los pesos
if text in articles:
    link_acticle = articles[text]
    print(f'Link de la imagen del articulo: {link_acticle}')
else:
    link_acticle = 'Article not found'
    print(link_acticle)


#_______here we count the images that are repeated ____
#vamos a crear un diccionario en donde se ordenaran las 40 o menos imagenes en dado que se repitan

#choose the number of images
#n_datos = 626
n_img = 20

#seleccionamos los primeros elementos de cada base
pesos_rb_cls = dict(list(pesos_rb_cls.items())[:n_img])
pesos_rb_mp = dict(list(pesos_rb_mp.items())[:n_img])
pesos_st_cls = dict(list(pesos_st_cls.items())[:n_img])
pesos_st_mp = dict(list(pesos_st_mp.items())[:n_img])



#Imagenes es un arreglo de cada diccionario de los mejores 20 pesos de cada embedding
imagenes = [pesos_rb_cls, pesos_rb_mp, pesos_st_cls, pesos_st_mp]



img_repetitions = {} #diccionario donde se guardaran solo las imagenes que se reptien donde las llaves es el link y el valor la cantidad que se repiten
img_rep_and_not_rep = {} #diccionario donde se guardan las imagenes qeu se reptines y las qeu no se repiten


#Se crearan dos arreglos:
# Primero crearemos una arreglo en donde se guardara especificamente las imagens que estan repetidas minimo 1 vez.


for n, BD_img_pesos in enumerate(imagenes):#en el primer for iteraremos sobre la lista de los diferentes diccionarios de imagenes-pesos 
    #n sera la base de datos en la que se encuentra actualmente
    print(f"Base: {n}")

    for img in list(BD_img_pesos.keys()): #Se agarra una por una de las imagenes de la base de datos que se este iterando en el primer for

        #img = seran las imagenes de la base de datos actual 
        
        if img in imagenes[n]: #si la imagen existe en la base de datos actual, se pasa a verificar si se repite o no
            
            #ahora veremos si la imagen ya fue agregada al diccionario
            if img in img_rep_and_not_rep: # si la imagen ya habia sido agregada, se incrementa su valor con una unidad
                img_rep_and_not_rep[img] = img_rep_and_not_rep[img] + 1 
                

            else:   #si la imagen no habia sido agregada, se inicializa con 0
                img_rep_and_not_rep[img] = 0

#Se tomaran solo las imagenes que se repiten por lo menos 1 vez

#hacemos arreglos los diccionarios donde contienen las n_img con sus pesos asociados



for link, repetitions in img_rep_and_not_rep.items():
    if repetitions > 0:
        img_repetitions[link] = repetitions
    else:
        continue
print(len(img_repetitions))

#Ahora crearemos una base de datos donde no contenga ninguna de las imagenes de la base de datos "img_repetitions"

#La manera en como se ira creando la base de datos sera agarrando la primera imagen de cada base de datos de los embeddings
#y asi consecutivamente.

links_rb_cls = list(pesos_rb_cls.keys()) 
links_rb_mp = list(pesos_rb_mp.keys())  
links_st_cls = list(pesos_st_cls.keys())  
links_st_mp = list(pesos_st_mp.keys()) 

img_links = [links_rb_cls, links_rb_mp, links_st_cls, links_st_mp]


#print(img_links[0][0]) #asi se accede al primer link de la primera lista de links

img_0_rep_ordenadas = {} #Diccionario en donde se agregan las imagenes que no se repiten ninguna vez y con ORDEN de importancia


for i in range(n_img): #Se itera n_img, en este caso 20 veces
    for m in range(4):#4 por que son 4 bases de datos
        if img_links[m][i] in img_repetitions: #si la imagen esta en la lista de las qeu se repiten por lo menos una vez, no la agregamos
            continue
        else:
            img_0_rep_ordenadas[img_links[m][i]] = 0

with open('img_0_rep_ordenadas.json', 'w') as file:
    json.dump(img_0_rep_ordenadas, file, indent=4)


#primero se ordenará de mayor a menor los pesos y despues se guardarán
img_repetitions = dict(sorted(img_repetitions.items(), key=lambda item: item[1], reverse=True ))



#ahora le agregaremos los datos al diccionario donde ya se tienen las imagenes repetidas
        
for link, value in img_0_rep_ordenadas.items():
    img_repetitions[link] = value


with open('img_repetitions.json', 'w') as file:
    json.dump(img_repetitions, file, indent=4)

    

n_rows = 4
n_columns = 5
marco_ancho = 4

#aqui se eligen las mejores imagenes
top_img = [key for key in list(img_repetitions.keys())[:(n_img)]]
pesos = [valor for valor in list(img_repetitions.values())[:(n_img)]]

fig, axs = plt.subplots(n_rows, n_columns, figsize=(6, 3)) #se haran 15 imagenes

for i, link in enumerate(top_img):

    img = load_image(link)

    # Determinar la posición de la subgráfica
    ax = axs[i // n_columns, i % n_columns]
    ax.imshow(img)
    ax.axis('off')  # Ocultar los ejes
    if link == link_acticle:
        ax.set_title('Article Image', fontsize = 4, fontweight='bold')
    
    # Agregar un rectángulo alrededor de la imagen
    width, height = img.size

    rect = rectange(pesos[i], width, height, marco_ancho)
    
    #se agrega el rectangulo a cada imagen
    ax.add_patch(rect)

# Ajustar el espacio entre las gráficas
plt.tight_layout()

plt.savefig(f'Img resultados/top images.png', dpi=300, format='png', bbox_inches='tight')
print(f"Image saved!")

#plt.show()

plt.close(fig)
