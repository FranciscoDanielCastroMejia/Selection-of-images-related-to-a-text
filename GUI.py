#In this program will be the interface of the proyect

import streamlit as st
import pandas as pd
import json
import os
from PIL import Image
import plotly.express as px
import matplotlib.pyplot as plt
import PIL.Image
from PIL import ImageEnhance
import requests
import matplotlib.patches as patches
import torch
import urllib.parse as parse
import os
from look_dict2 import look_dict2
import analysis #program with all de data analisis
import Imagenes

url = 'https://tse1.mm.bing.net/th?id=OIP.2OBWIwCM1FTn8Ql54pGNigHaHa&pid=Api&P=0&h=180'
    


if __name__=="__main__":

    st.title("SELECTION OF IMAGES RELATED TO A TEXT")
    st.divider()#add a divider line

    #_______________TEXT INPUT____________________
    text = st.text_area('Input your text', height=100)
    st.write(text)
    st.divider()#add a divider line

    #_____________Select the dataset______________
    st.markdown('### Select the dataset of images that you want to work')
    dataset = st.selectbox(
        'Select the dataset of images',
        ['Select...', 'GLOBAL', 'caption_art', 'caption_wiki']
    )
    st.divider()#add a divider line

    if text and dataset != 'Select...':
        #__________process to get te image
        look_dict2(text,dataset) #funcion para crear las bases de datos
        pesos_rb_cls, pesos_rb_mp, pesos_st_cls, pesos_st_mp = Imagenes.load_pesos()

        #__________Display the image of the article______________

        st.markdown('### Image of the article')
        link_article = Imagenes.look_article_img(text)
        if(link_article == 'Article not found'):
            st.image(url, caption='Imagen desde URL', width=300)
        else:
            st.image(link_article, caption='Imagen desde URL', width=300)
        st.divider()#add a divider line

        #__________Display the image of the article______________

        st.markdown('### Best Images related to the text')

        repeated_imgs = Imagenes.count_repeated_img(pesos_rb_cls, pesos_rb_mp, pesos_st_cls, pesos_st_mp)
        fig = Imagenes.display_images(repeated_imgs, link_article)
        st.pyplot(fig)

