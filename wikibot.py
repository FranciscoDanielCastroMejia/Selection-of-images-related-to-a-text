#With this program you will be able to download or open images from wikimedia commons
#using a bot from that page

from IPython.display import display
from IPython.display import HTML, Image
import pywikibot
from pywikibot import pagegenerators
import argparse
from pathlib import Path
import os


# With this function you can control the format of the file that you want
# to use, because in some cases the files that the wikibot choose, they are
# audios or gifs.


def check_format(file):
    extension = os.path.splitext(file)[1].lower()
    allowed_extensions = ['.jpg', '.jpeg']#, '.png']
    if extension in allowed_extensions:
        return True
    else:
        return False
    

def wikibot(CATEGORY, ITERATIONS, download_path): 
    site = pywikibot.Site("commons", "commons") #here you choose site of wikimedia commons, you can use others
    cat = pywikibot.Category(site, CATEGORY) #pass the category to the bot
    gen = pagegenerators.CategorizedPageGenerator(cat, recurse=True)
    counter1 = 0
    counter2 = 0
    

    for indice, page in enumerate(gen):
        print("page: {}".format(page))

        if check_format(page.title()): #check if the format of the image is correct
            counter1 = counter1 + 1
            #print(dir(page)) #here we can see all the elements in page
            #print(page.permalink()) 
            #print(page.title()[5:]) #with this we can know the name of the image
            print(page.get_file_url()) 
            #print(page.full_url())
            #print(page.categories())
            try:
                filename = page.title()[5:]
                #print(f'{download_path}/{filename}')
                page.download(f'{download_path}/{filename}') #here we download the image
            #if the file has "" here we clean that
            #con esto limpiamos el archivo
            except Exception as e:
                filename = page.title()[5:]
                filename = filename.replace('"', '%22')
                page.download(f'{download_path}/{filename}')

        else: 
            #print("\n")
            #print("NOT A IMAGE FORMAT: {}".format(page.title()[5:]))
            #print("\n")
            counter2 = counter2 + 1
            print(page.full_url())
            print("Diferente format: {}".format(page.title()))
            print("\n")

        if indice>=ITERATIONS:
            break
    print('\n')
    print("Images founded with correct format: {}".format(counter1))
    print("Images founded with incorrect format: {}".format(counter2))
    


if __name__=='__main__':

    # Here you create the folder for the images that you want to download 

    download_path = "./images wikibot"
    Path(download_path).mkdir(parents=True, exist_ok=True)  

    # Generate new caption from input image
    parser = argparse.ArgumentParser(description="Images")
    parser.add_argument('--category', help="Categort of the images")
    parser.add_argument('--iteration', type=int, default=10, help="Number of the images")

    CATEGORY = parser.parse_args().category
    ITERATIONS = parser.parse_args().iteration 

    wikibot(CATEGORY, ITERATIONS, download_path)
    print("\n")
    
    