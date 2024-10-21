#In this program we will have the information about all the datasets using pandas
import streamlit as st
import pandas as pd
import json
import os
from PIL import Image
import plotly.express as px


#Crear un dataframe de la base de datos de los links con la informacion siguiente:
#Categorias, Numero de Subcategorias (con imagenes), Cantidad de links, Se realizo caption o no a esa subcategoria


folder_path = 'ANALYSIS/BASE DE DATOS LINKS'
logo_path = 'database_logo.png'

st.set_page_config(page_title='Datasets', page_icon=logo_path, layout='wide', 
                   initial_sidebar_state='collapsed')

#_________________CATEGORIES_______________________________
Categories = [nombre for nombre in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, nombre))]

#_______________SUBCATEGORIES with images__________________________

cat_with_number_subcat = {} # name_of_categorie:number_of_subcategories
Number_img_per_cat = {} #number of images per category (category:#images)

for cat in Categories:
    
    cont_subcat_with_img = 0 #counter of subcategories that have images
    cont_imgs_per_cat = 0 #
    cat_folder_path = os.path.join(folder_path, cat)
    list_subcat = os.listdir(cat_folder_path)

    for subcat in list_subcat:#here we have all .json files

        sub_cat_folder_path = os.path.join(cat_folder_path, subcat)
        with open(sub_cat_folder_path, 'r') as file:
            links = json.load(file)
            cont_imgs_per_cat += len(links)
            if len(links) != 0:
                cont_subcat_with_img += 1
    
    cat_with_number_subcat[cat] = cont_subcat_with_img
    Number_img_per_cat[cat] = cont_imgs_per_cat


    
#_____________VERIFYING IF THE CAT HAS CAPTIONS_____________

caption_made = []
cont = 0
for cat in Categories:
    
    folder_path = 'ANALYSIS/IMG Captions'
    cat_folder_path = os.path.join(folder_path, cat)
    
    #list_subcat = os.listdir(cat_folder_path)

    if not os.listdir(cat_folder_path):
        caption_made.append(False) #Imagenes sin caption
    else:
        caption_made.append(True) #Imagenes con caption
        cont +=1
        print(cat_folder_path)


print(len(caption_made))
    


#_________CREATING DATAFRAMES________
data = {
    'Categories':Categories,
    'Number of Subcategories':list(cat_with_number_subcat.values()),
    'Number of Images per Category':list(Number_img_per_cat.values()),
    'Imagenes con caption':caption_made
}

df_without_total = pd.DataFrame(data)


Larger_number_of_images = df_without_total['Number of Images per Category'].max()
Larger_number_of_subcat = df_without_total['Number of Subcategories'].max()


def max(s):
    if s.name == 'Number of Images per Category':    
        return ['background-color: gray' if v == Larger_number_of_images else '' for v in s]
    elif s.name == 'Number of Subcategories':
        return ['background-color: blue' if v == Larger_number_of_subcat else '' for v in s]
    elif s.name == 'Imagenes con caption':
        return ['background-color: green' if v == True else 'background-color: red' for v in s]  
    else:
        return ['' for _ in s]



total_subcat = df_without_total['Number of Subcategories'].sum()
total_img_per_cat = df_without_total['Number of Images per Category'].sum()

new_row = pd.DataFrame({'Categories':['TOTAL'],
    'Number of Subcategories':[total_subcat],
    'Number of Images per Category':[total_img_per_cat],
    'Imagenes con caption':[' ']})
    


df = pd.concat([df_without_total,new_row], ignore_index=True)

df_styled = df.style.apply(max, subset=['Number of Images per Category', 'Number of Subcategories','Imagenes con caption'], axis=0)

#_______datafame de los 8 grupso de imagenes con todas las categorias_______
with open('ANALYSIS/BASE DE DATOS CONTENEDOR TOTAL/prueba.json', 'r')as file:
    groups_images = json.load(file)


data = {group:len(list_links) for group, list_links in groups_images.items()}
df_groups = pd.DataFrame.from_dict(data, orient='index', columns=['values']).reset_index()
df_groups.columns = ['Parts', 'Number of Images']
total_images = df_groups['Number of Images'].sum()
new_row = pd.DataFrame({'Parts':'Total','Number of Images':[total_images]})

df_groups = pd.concat([df_groups,new_row], ignore_index=True)




def main_analysis():
    
    st.title("Analisis de datos")
    st.divider()
    st.markdown('### Data frame')
    st.dataframe(df_styled)
    st.caption("Table 1: Contains all images links in categories that are used to obtein their captions")

    st.divider()#add a divider line
    #_______________Data frame of image with captions and without captions ____________________
    st.markdown('### Data frame of images with captions and without captions')
    df_yes_no_caption = df_without_total.groupby('Imagenes con caption')['Number of Images per Category'].sum().reset_index()
    st.dataframe(df_yes_no_caption)
    st.caption("Table 2: The number images links that have been captioned")
    

    st.divider()#add a divider line
    #_______________Plot and dataframe of the number of SUBCATEGORIES in each category ____________________
    st.markdown('### Plot and dataframe of the number of SUBCATEGORIES in each category')
    df2 = df_without_total[['Categories', 'Number of Subcategories']]
    st.dataframe(df2)
    st.caption('Table 3: Categories with the number of subcatgories that have images links in them')

    fig = px.bar(df2, 'Categories', 'Number of Subcategories', color='Categories')
    st.plotly_chart(fig)
    st.caption('Figure 1: Graphic of the Table 3')

    
    st.divider()#add a divider line
    #_______________Plot of the number of IMAGES in each category ____________________
    st.markdown('### Plot of the number of IMAGES in each category')
    df3 = df_without_total[['Categories', 'Number of Images per Category']]
    st.dataframe(df3)
    st.caption('Table 4: Categories with the number of images')

    fig = px.bar(df3, 'Categories', 'Number of Images per Category', color='Categories')
    st.plotly_chart(fig)
    st.caption('Figure 2: Graphic of the Table 4')


    st.divider()#add a divider line
    #_______________Dataframe of 8 groups of images with all categories ____________________
    st.markdown('### Dataframe of 8 images groups with all categories')
    st.dataframe(df_groups)
    st.caption('Table 5: Image groups containing all categories in each group, there are fewer images, because we eliminated the repeated ones')

    




if __name__=="__main__":

    main_analysis()



