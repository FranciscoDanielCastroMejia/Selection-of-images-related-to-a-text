from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F

#_________________initialize the device______________________________

device = "cuda" if torch.cuda.is_available() else "cpu"

#first we load the model that we will use to make the embeddings of th articles, we will use the database that is translated and summarized

tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = model.to(device)


#____________________funcion to make the mean pooling_________________

def mean_pooling_st(model_output, attention_mask):

        token_embeddings = model_output[0] #se pone [0] para acceder a los embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float() #expander la capa de attention mask a la de los embeddings
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


#__________________________Function embeddings with mean_pooling__________________________

def embedding_mp_st(text):

        input = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512).to(device)
        
        with torch.no_grad():
                output = model(**input)

        embedding = mean_pooling_st(output, input['attention_mask'])
        embedding =F.normalize(embedding, p=2, dim=0)

        return embedding


#__________________________Funciton embeddings with CLS vector__________________________


def embedding_cls_st(text):

        input = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512).to(device)
        with torch.no_grad():
                output = model(**input)

        embedding = output.last_hidden_state[:, 0, :] #se utiliza [:,0,:] para acceder al token CLS
        embedding =F.normalize(embedding, p=2, dim=0)

        return embedding





        
if __name__=='__main__':

        #aqui va el texto de la base de datos 
        text1 = "The woman is playing in the park"
        text2 = "the woman is playing in the park"


        #__________________________embeddings with mean_pooling__________________________

        embedding1_mp = embedding_mp_st(text1)
        embedding2_mp = embedding_mp_st(text2)
        print(embedding2_mp.size())

        producto = torch.dot(embedding1_mp[0], embedding2_mp[0]).to(device)
        similarity = F.cosine_similarity(embedding1_mp[0], embedding2_mp[0], dim=0)
        print(f"Similitud coseno Mean_poolin: {similarity}")
        print(f"Producto punto Mean_poolin: {producto.item()}")

        #__________________________embeddings with CLS vector__________________________


        embedding1_cls = embedding_cls_st(text1)
        embedding2_cls = embedding_cls_st(text2)

        producto = torch.dot(embedding1_cls[0], embedding2_cls[0]).to(device)
        similarity = F.cosine_similarity(embedding1_cls[0], embedding2_cls[0], dim=0)
        print(f"Similitud coseno CLS vector: {similarity}")
        print(f"Producto punto CLS vector: {producto.item()}")




