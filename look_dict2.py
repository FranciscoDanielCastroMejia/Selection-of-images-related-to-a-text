#In this program we will look for the most representative image
#for doing that, we will import the data base that contain the link of the image with its 
#embedding vector.

from transformers import AutoTokenizer, RobertaModel
import torch
import torch.nn.functional as F
import json 
import numpy as np
from Embeddings import embedder


#___________________Libraries for the progress bar_____________________
import time
from progressbar import ProgressBar

#_________________initialize the device______________________________

device = "cuda" if torch.cuda.is_available() else "cpu"


def look_dict2(text, dataset):

    #________________here we choose which embedder we will use_____________

    types = ["rta_cls", "rta_mp", "st_cls", "st_mp"]
    #type_of_embedder = types[3]
    cont = 0

    for type_of_embedder in types:


        #________________here we choose the path of the database_____________
        path = embedder.path(type_of_embedder, dataset)
        print(path)

        with open(path, 'r')as file:
            DBC_embedings = json.load(file) #Data Base of the specific embedding Captions it can be "rta_cls", "rta_mp", "st_cls", "st_mp"
        

        

        embedding_t = embedder.embedder(text, type_of_embedder) #ya regresa el embedding normalizado


        #-----initializate a new data base, that will have the links and the result of the product cosine
        links_pesos_embeddings = {}


        #now, we make the cosine operation with all the database anda find the best images, we made the operation with the data vase of captions!
        for link, vector in DBC_embedings.items():

            embedding_C = DBC_embedings[link]#agarramos el embedding del primer caption
            embedding_C = torch.tensor(embedding_C).to(device) #covertimos el embedding en tensor, ya estan normalizados
            
            #se hace el producto coseno con el embedding del texto ingresado, en este caso seria el resumen del articulo
            
            similarity = F.cosine_similarity(embedding_t[0], embedding_C[0], dim=0)
            links_pesos_embeddings[link] = similarity.tolist()
            #print(f"Similitud coseno promedios: {similarity}")
        
        #se guardarán los vectores de los pesos SIN ORDENAR, esto para hacer una correlacion
        with open(f"BD pesos look dict desordenados/pesos_desorder_{types[cont]}.json", "w") as file:
            json.dump(links_pesos_embeddings, file, indent=4)
        
        #primero se ordenará de mayor a menor los pesos y despues se guardarán
        links_pesos_embeddings = dict(sorted(links_pesos_embeddings.items(), key=lambda item: item[1], reverse=True ))

        path_pesos = embedder.path(type_of_embedder, "pesos")
        print(path_pesos)

        with open(path_pesos,'w') as file:
            json.dump(links_pesos_embeddings, file, indent=4)

        cont = cont + 1



if __name__=='__main__':

    #Here is where we make the embedding of the text
    text = "The Antarctic continent is the coldest place on Earth. The lowest temperature ever recorded was observed in 1983: less than 89 degrees Celsius. The Antarctic ice layer is also interesting because under its surface a large number of underground lakes are located. The largest of them, Lake Vostok, is of dimensions equivalent to Lake Ontario and is the seventh largest lake on the planet."
    #text = "The Taj Mahal is a complex of buildings and gardens built in the 17th century during the Mogol Empire. It is recognized by UNESCO as a World Heritage Site. The change of color of the marble of the monument was attributed from a start to the air pollution in the vicinity."
    #text = "Isaac Asimov imagined a future in which robots carry out activities that are traditionally carried out by humans more efficiently. Asimov was a visionary who wrote his novel at a time when the first digital computer of general use had not yet been built. In his novels, Asimov became a well-known science fiction writer Isaac Asimov."
    #text = "Small magazine published an article on how microgravity affects brain connections. Researchers find that there are some changes in the organization of the brain immediately after the end of the mission. After eight months some astronauts were subjected to magnetic resonance studies. Of them, they remain, while others disappear, returning the brain to its original state."
    #text = "If extreme weather events make the planet uninhabitable, we would have to look for options to move to another planet. Our first choice might be the Moon, which is, say, a stone\u2019s throw away. The Moon, however, is an inhospitable, dry and atmosphereless place."
    #text = "In December 1971, the Soviet Union was the first country to gently pose a probe on the surface of the Martian surface. The first exploration probes on Mars, however, did not have mobility and only provided us with information from a fixed point of view. Subsequent NASA missions sent explorer robots to Mars that were able to move along its surface. Masahiro Ono says Mars needs to extend the mobility of future explorers."
    #text = "According to statistics from the World Health Organization, the number of new cases of coronavirus-baptized COVID-19 in China would be decreasing. On 22 February, 397 new cases were diagnosed, compared to the more than 3,000 daily cases that came to be diagnosed in the first days of February. outbreaks of the disease have appeared in other parts of the world whose rapid growth concerns experts."
    #text = "It is possible that the eve of the new year is not the best time to state our purposes of improvement, if we fail to look unconvincing. We must take into account that the start date is a convention that does not have a firm basis, to say astronomical. 2019 is apparently one of the lot, without features worthy of notice."
    #text = "An increase in ambient temperature of a degree centigrade above the monthly average raised the suicide rate in the United States by 0.7 per cent between 1970 and 1990. In the case of Mexico, researchers found that the. suicide rate rose by 2.1 per cent per cent for each degree of environmental. temperature increase, in the period 1980-2010."
    #text = "On September 6, 1977, the Voyager 1 space probe was launched from Cape Canaveral. The probe is located at a distance such that the signals it emits take about 17 hours to reach the Earth. Voyager 1 is also known because it carries on board a phonographic disc of gold-coated copper with 115 images of the Earth, as well as messages in 55 languages."
    #text = "Children and young people show a skill worthy of envy: to manipulate with skill gadgets that are not familiar to them. Researchers found that with certain unusual combinations of objects children outperform adults at the time of determining the correct combination. This is because children have greater flexibility to establish a cause-effect relationship in a novel situation compared to the flexibility of an adult."
    #text = "Cuban parents are giving their children invented names that are not rarely extravagant, to say the least. In some cases these are obtained by combining, more or less creatively, common names of their own. The most frequently used was \u201cRoentgenogram,\u201d which was replaced by the word X-ray."
    #text = "Russian ship Phobos-Grunt, launched into space on November 8, has trouble carrying out the mission entrusted to it. Another news about Mars was the successful launch yesterday \u2013 at a cost of $2.5 billion \u2013 of the explorer Curiosity to this planet. Curiosity is a NASA vehicle with a weight of about a ton, which will explore for a period of two years the Martian nuclear-powered surface."
    #text = "The number of motor vehicles in San Luis Potos\u00ed is growing rapidly. In 1988 little more than 66,000 vehicles were circulating in our city, this one year. This increase is in sharp contrast to the corresponding increase in the population of the city of less than 100% in the same period." 
    #text = "The Nobel Prize in Physics for this year was announced on 6 October. The prize was awarded to Charles Kao for his work on the transmission of light in optical fibers. Williard Boyle and George Smith for the invention of the CCD image sensor \u2013 the device that replaces the film roll in digital cameras."
    #text = "Jonathan Swift describes in \u2018The travels of Gulliver\u2019 the features of the protagonist in the country of the Liliputenses, similar to humans but only 15 centimeters high. According to Swift, the proportions of the body of dwarfs and giants would have been the same as those of our species."
    #text = "\"The Murders of Morgue Street\" was published by Poe in 1841, half a century before Juan Vucetich in Argentina first used fingerprints \u2013 which are unique to each person \u2013 to solve a criminal case. After a century Poe would have taken 150 years to be born, he would have known that each individual could also be identified by his genetic code."
    #text = "Gustavo Del Castillo, Potosino and chemical of formation, became interested in physics. He decided in 1951 to travel to the United States in search of a doctorate in this specialty. In parallel to the creation of the School of Physics, he began the construction of a \u201cmist chamber\u201d",
    #text = "The infrastructure of a city includes artificial concrete structures or other materials that have displaced natural elements such as trees or water ponds. These new elements interact with solar radiation differently than it did with the original vegetation or bodies of water, altering the environment and contributing to the so-called heat island effect. To mitigate this last effect, specialists consider the deployment of a green and blue urban infrastructure."
    #text = "The current pandemic has brought about changes that are expected to be permanent. The Plague of Justiniano was far from being an intra-scendent flu and had a significant social and economic impact. We would expect, of course, that an epidemic that ends with a substantial percentage of the population will lead to irreversible changes."
    #text = "The life of the Roman cities of Pompeii and Herculano reached an abrupt end. The two cities were buried by a thick layer of volcanic material in 79 C.E. Researchers find clear differences between diets followed by men and women. Women consumed less protein from cereals and seafood, and relatively more from animals and land products."


    #text = "The planets in our solar system are a fascinating and diverse group of celestial bodies, each with its own unique characteristics. From the scorching surface of Mercury, the closest planet to the Sun, to the gas giants like Jupiter and Saturn, whose massive sizes and intricate systems of rings and moons captivate scientists and stargazers alike. Earth, our home, stands out for its ability to support life, while Mars, the red planet, continues to intrigue with its potential for past or present microbial life. Farther out, Uranus and Neptune, the ice giants, hold secrets of the outer solar system, with their mysterious atmospheres and extreme conditions. Together, these planets provide a glimpse into the complexities and wonders of our cosmic neighborhood"
    #text = "Cars are an integral part of modern life, offering convenience, mobility, and freedom to travel. From sleek sports cars that embody speed and performance to reliable family sedans designed for comfort and safety, the variety of vehicles on the road reflects the diverse needs and preferences of drivers. Electric cars are becoming increasingly popular, representing a shift towards sustainability with their environmentally friendly designs and innovative technologies. Meanwhile, luxury cars continue to captivate with their sophisticated features and high-end craftsmanship. Whether it’s a compact car for city driving or a rugged SUV for off-road adventures, cars play a crucial role in shaping our daily experiences and the way we connect with the world around us."
    #text = "Ancient cultures offer a rich tapestry of history, traditions, and achievements that continue to influence the world today. From the grand pyramids of Egypt, which stand as a testament to the architectural prowess and spiritual beliefs of the ancient Egyptians, to the sophisticated city-planning and governance of the Romans, whose legal and political systems laid the foundation for many modern societies, these civilizations left an indelible mark on human history. The Maya and Aztecs of Mesoamerica developed intricate calendars and monumental architecture, reflecting their deep understanding of astronomy and cosmology. In Asia, the ancient Chinese civilization contributed innovations like papermaking, gunpowder, and the compass, which have had lasting global impacts. Each of these cultures, with their unique languages, art, and philosophies, shaped the course of history and enriched the human experience in profound ways"
    #text = "The coronavirus pandemic, caused by the COVID-19 virus, has had a profound impact on the world since it first emerged in late 2019. Spreading rapidly across the globe, it led to unprecedented public health measures, including widespread lockdowns, social distancing, and the use of face masks to prevent transmission. The virus has not only challenged healthcare systems but also disrupted economies, education, and daily life, forcing societies to adapt to a new normal. The development and distribution of vaccines brought hope and began to turn the tide against the pandemic, though variants of the virus continue to pose challenges. Beyond the immediate health effects, the pandemic has prompted reflections on global cooperation, the importance of public health infrastructure, and the resilience of communities in the face of adversity."
    #text = "Monkeys and gorillas are fascinating members of the primate family, each with distinct characteristics and behaviors that highlight their evolutionary significance. Monkeys, which include both Old World monkeys like baboons and macaques, and New World monkeys like capuchins and howler monkeys, are known for their diverse adaptations to various habitats. They exhibit a wide range of social structures, from complex troop hierarchies to cooperative foraging behaviors. Gorillas, on the other hand, are the largest of the great apes and are known for their impressive size and strength, as well as their gentle and social nature. Living primarily in the dense forests of Africa, gorillas are divided into two species: the Eastern gorillas and the Western gorillas. Both species face significant threats from habitat loss and poaching, making conservation efforts crucial for their survival. Studying these primates not only provides insights into their lives but also helps us understand the evolutionary connections shared with humans."


    #dataset = "caption_art" #elegir el dataset para los captions con el articulo
    dataset = "caption_wiki" #elegir el dataset para los captions con el datasett global
    look_dict2(text,dataset)