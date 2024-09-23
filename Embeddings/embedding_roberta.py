
from transformers import AutoTokenizer, RobertaModel
import torch
import torch.nn.functional as F

#_________________initialize the device______________________________
device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)

#first we load the model that we will use to make the embeddings of th articles, we will use the database that is translated and summarized

tokenizer = AutoTokenizer.from_pretrained("FacebookAI/roberta-base")
model = RobertaModel.from_pretrained("FacebookAI/roberta-base")
model = model.to(device)

#____________________funcion to make the mean pooling_________________

def mean_pooling_rta(model_output, attention_mask):

        token_embeddings = model_output[0] #se pone [0] para acceder a los embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float() #expander la capa de attention mask a la de los embeddings
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


#__________________________Function embeddings with mean_pooling__________________________

def embedding_mp_rta(text):

        input = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512).to(device)
        
        with torch.no_grad():
                output = model(**input)

        embedding = mean_pooling_rta(output, input['attention_mask'])
        embedding =F.normalize(embedding, p=2, dim=0)

        return embedding


#__________________________Funciton embeddings with CLS vector__________________________


def embedding_cls_rta(text):

        input = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512).to(device)
        with torch.no_grad():
                output = model(**input)

        embedding = output.last_hidden_state[:, 0, :] #se utiliza [:,0,:] para acceder al token CLS
        embedding =F.normalize(embedding, p=2, dim=0)

        return embedding





        
if __name__=='__main__':

        #aqui va el texto de la base de datos 
        text1 = "an outdoor view of a rooftop garden with a pool and green grass. the roof is covered in plants, flowers, and trees. there are two buildings on the left side of the image that are made up of a gray concrete structure. there are windows on the right side of the building. there is a small black flag on the top of the building. there are people walking on the roof."
        text2 = "Building with a rooftop garden with a pool"


        #__________________________embeddings with mean_pooling__________________________

        embedding1_mp = embedding_mp_rta(text1)
        embedding2_mp = embedding_mp_rta(text2)

        print(embedding2_mp.size())


        producto = torch.dot(embedding1_mp[0], embedding2_mp[0]).to(device)
        similarity = F.cosine_similarity(embedding1_mp[0], embedding2_mp[0], dim=0)
        print(f"Similitud coseno Mean_poolin: {similarity}")
        print(f"Producto punto Mean_poolin: {producto.item()}")

        print("\n")

        #__________________________embeddings with CLS vector__________________________


        embedding1_cls = embedding_cls_rta(text1)
        embedding2_cls = embedding_cls_rta(text2)

        producto = torch.dot(embedding1_cls[0], embedding2_cls[0]).to(device)
        similarity = F.cosine_similarity(embedding1_cls[0], embedding2_cls[0], dim=0)
        print(f"Similitud coseno CLS vector: {similarity}")
        print(f"Producto punto CLS vector: {producto.item()}")

