import matplotlib.pyplot as plt
import json

with open('BD pesos look dict/lnk_pesos_emb_rta-cls.json', 'r') as file:
    pesos_rb_cls = json.load(file)

with open('BD pesos look dict/lnk_pesos_emb_rta-mp.json', 'r') as file:
    pesos_rb_mp = json.load(file)

with open('BD pesos look dict/lnk_pesos_emb_st-cls.json', 'r') as file:
    pesos_st_cls = json.load(file)

with open('BD pesos look dict/lnk_pesos_emb_st-mp.json', 'r') as file:
    pesos_st_mp = json.load(file)

#n_datos = 626
n_datos = 626

#datos = [valor for valor in list(pesos.values())[:100]]
datos_rb_cls = [valor for valor in list(pesos_rb_cls.values())[:n_datos]]
datos_rb_mp = [valor for valor in list(pesos_rb_mp.values())[:n_datos]]
datos_st_cls = [valor for valor in list(pesos_st_cls.values())[:n_datos]]
datos_st_mp = [valor for valor in list(pesos_st_mp.values())[:n_datos]]

imagen = 'Faraon'

#se crea el panle con 2 filas y 2 columnas
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

x = [i for i in range(len(datos_rb_cls))]

#primera grafica
axs[0, 0].plot(x, datos_rb_cls, color='red')
axs[0, 0].set_title('Grafica Roberta-CLS')
axs[0, 0].set_xlabel('Valores')
axs[0, 0].set_ylabel('Pesos')


#segunda grafica
axs[0, 1].plot(x, datos_rb_mp, color='blue')
axs[0, 1].set_title('Grafica Roberta-Mean poolin')
axs[0, 1].set_xlabel('Valores')
axs[0, 1].set_ylabel('Pesos')

#tercera grafica
axs[1, 0].plot(x, datos_st_cls, color='green')
axs[1, 0].set_title('Grafica ST-CLS')
axs[1, 0].set_xlabel('Valores')
axs[1, 0].set_ylabel('Pesos')

#cuarta grafica
axs[1, 1].plot(x, datos_st_mp, color='orange')
axs[1, 1].set_title('Grafica ST-Mean poolin')
axs[1, 1].set_xlabel('Valores')
axs[1, 1].set_ylabel('Pesos')

# Ajustar el espacio entre las gráficas
plt.tight_layout()

"""#plt.plot(x, datos, color='red', label='Datos')
plt.scatter(x, datos, s=5)

plt.xlabel('Valores')
plt.ylabel('Pesos')
plt.title(f'Grafica del producto coseno con la imagen {imagen}')
plt.legend()"""



plt.savefig(f'graficos pesos/grafico_{imagen}.png', dpi=300, format='png', bbox_inches='tight')

plt.show()


