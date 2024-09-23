import json 
import numpy as np
import torch.nn.functional as F


def compute_dot_product(vector1, vector2):
    """Calcula el producto punto entre dos vectores."""
    return np.dot(vector1, vector2)



# Rutas a los archivos JSON
file_path_1 = '/home/mitos/Documentos/Models for caption/embedding.json'
file_path_2 = '/home/mitos/Documentos/Models for caption/embedding1.json'


with open(file_path_1, 'r') as file:
    data1 = json.load(file)


with open(file_path_2, 'r') as file:
    data2 = json.load(file)


data1 = np.array(data1)
data2 = np.array(data2)

print(data1.shape)

# Calcular el producto punto
dot_product = np.dot(data1[0], data2[0])
print(f"Producto punto: {dot_product}")
