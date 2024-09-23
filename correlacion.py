#In this program we will measure de correlation of the data of the weights 

import matplotlib.pyplot as plt
import numpy as np 
import json

with open("BD pesos look dict desordenados/pesos_desorder_rta_cls.json", "r") as file:
    pesos_desorder_rta_cls = json.load(file)

with open("BD pesos look dict desordenados/pesos_desorder_rta_mp.json", "r") as file:
    pesos_desorder_rta_mp = json.load(file)

with open("BD pesos look dict desordenados/pesos_desorder_st_cls.json", "r") as file:
    pesos_desorder_st_cls = json.load(file)

with open("BD pesos look dict desordenados/pesos_desorder_st_mp.json", "r") as file:
    pesos_desorder_st_mp = json.load(file)

#aqui se tienen las listas solo de los pesos

pesos_desorder_rta_cls = list(pesos_desorder_rta_cls.values())
pesos_desorder_rta_mp = list(pesos_desorder_rta_mp.values())
pesos_desorder_st_cls = list(pesos_desorder_st_cls.values())
pesos_desorder_st_mp = list(pesos_desorder_st_mp.values())

#se hacer arreglos de numpy

pesos_desorder_rta_cls = np.array(pesos_desorder_rta_cls)
pesos_desorder_rta_mp = np.array(pesos_desorder_rta_mp)
pesos_desorder_st_cls = np.array(pesos_desorder_st_cls)
pesos_desorder_st_mp = np.array(pesos_desorder_st_mp)

pesos = [pesos_desorder_rta_cls, pesos_desorder_rta_mp, pesos_desorder_st_cls, pesos_desorder_st_mp]


for i in range(4):
    for j in range(4):
        correlacion = np.corrcoef(pesos[i], pesos[j])[0,1]
        print(f"Image {i+1} {correlacion}")
    print("\n")
    
fig, axs = plt.subplots(2, 2, figsize=(10, 8))
x = [i for i in range(len(pesos_desorder_rta_cls))]


#primera grafica
axs[0, 0].plot(x, pesos_desorder_rta_cls, color='red')
axs[0, 0].set_title('Grafica Roberta-CLS')
axs[0, 0].set_xlabel('Valores')
axs[0, 0].set_ylabel('Pesos')

#segunda grafica
axs[0, 1].plot(x, pesos_desorder_rta_mp, color='blue')
axs[0, 1].set_title('Grafica Roberta-Mean poolin')
axs[0, 1].set_xlabel('Valores')
axs[0, 1].set_ylabel('Pesos')

#tercera grafica
axs[1, 0].plot(x, pesos_desorder_st_cls, color='green')
axs[1, 0].set_title('Grafica ST-CLS')
axs[1, 0].set_xlabel('Valores')
axs[1, 0].set_ylabel('Pesos')

#cuarta grafica
axs[1, 1].plot(x, pesos_desorder_st_mp, color='orange')
axs[1, 1].set_title('Grafica ST-Mean poolin')
axs[1, 1].set_xlabel('Valores')
axs[1, 1].set_ylabel('Pesos')

# Ajustar el espacio entre las gráficas
plt.tight_layout()

plt.show()

