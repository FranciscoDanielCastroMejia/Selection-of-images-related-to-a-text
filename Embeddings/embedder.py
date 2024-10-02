#in this program you wil find all the embedders (roberta, BERT, ans sentence transformer)

from transformers import AutoTokenizer, RobertaModel, AutoModel
import torch
import torch.nn.functional as F

#_________________initialize the device______________________________

device = "cuda" if torch.cuda.is_available() else "cpu"

#first we load the diferent models pretrained 

#model sentence trasnformers
tokenizer_st = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model_st = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model_st = model_st.to(device)

tokenizer_rta = AutoTokenizer.from_pretrained("FacebookAI/roberta-base")
model_rta = RobertaModel.from_pretrained("FacebookAI/roberta-base")
model_rta = model_rta.to(device)

tokenizer_brt = "aqui ira lo de bert"
model_brt = "aqui ira lo de bert"
model_brt = "aqui ira lo de bert"


def embedder(text, type):
        
        if type=="rta_cls":
                return embedding_cls(text, model_rta, tokenizer_rta)
        
        elif type=="rta_mp":
                return embedding_mp(text, model_rta, tokenizer_rta)
        
        elif type=="st_cls":
                return embedding_cls(text, model_st, tokenizer_st)
        
        elif type=="st_mp":
                return embedding_mp(text, model_st, tokenizer_st)
        
        elif type=="brt_cls":
                return embedding_cls(text, model_brt, tokenizer_brt)
        
        elif type=="brt_mp":
                return embedding_mp(text, model_brt, tokenizer_brt)
        
        result = "embedding doesnt exist"
        return result

    
#____________________funcion to make the mean pooling_________________

def mean_pooling(model_output, attention_mask):

        token_embeddings = model_output[0] #se pone [0] para acceder a los embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float() #expander la capa de attention mask a la de los embeddings
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


#__________________________Function embeddings with mean_pooling__________________________

def embedding_mp(text, model, tokenizer):

        input = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512).to(device)
        
        with torch.no_grad():
                output = model(**input)

        embedding = mean_pooling(output, input['attention_mask'])
        embedding =F.normalize(embedding, p=2, dim=0)

        return embedding


#__________________________Funciton embeddings with CLS vector__________________________


def embedding_cls(text, model, tokenizer):

        input = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512).to(device)
        with torch.no_grad():
                output = model(**input)

        embedding = output.last_hidden_state[:, 0, :] #se utiliza [:,0,:] para acceder al token CLS
        embedding =F.normalize(embedding, p=2, dim=0)

        return embedding


#_________________________________________________________________________________________________________________________  
#_____________________Esta parte es solo para crear las bases de datos de los articulos y los captions_____________________
#_________________________________________________________________________________________________________________________  


def path(type, action):
        
        #_________________captions article____________________________________(falta bert)
        #_____________________________________________________________  

        if type=="rta_cls" and action=="caption_art":
                path = 'BD Embeddings Articles/lnk_cap_emb_rta-cls.json'
                return path
        
        elif type=="rta_mp" and action=="caption_art":
                path = 'BD Embeddings Articles/lnk_cap_emb_rta-mp.json'
                return path
        
        elif type=="st_cls" and action=="caption_art":
                path = 'BD Embeddings Articles/lnk_cap_emb_st-cls.json'
                return path
        
        elif type=="st_mp" and action=="caption_art":
                path = 'BD Embeddings Articles/lnk_cap_emb_st-mp.json'
                return path
        
        #_________________captions WIKIMEDIA____________________________________(falta bert)
        #_____________________________________________________________  

        if type=="rta_cls" and action=="caption_wiki":
                path = 'BD Embeddings New Dataset/lnk_cap_emb_rta-cls.json'
                return path
        
        elif type=="rta_mp" and action=="caption_wiki":
                path = 'BD Embeddings New Dataset/lnk_cap_emb_rta-mp.json'
                return path
        
        elif type=="st_cls" and action=="caption_wiki":
                path = 'BD Embeddings New Dataset/lnk_cap_emb_st-cls.json'
                return path
        
        elif type=="st_mp" and action=="caption_wiki":
                path = 'BD Embeddings New Dataset/lnk_cap_emb_st-mp.json'
                return path
        #_________________articles____________________________________(falta bert)
        #_____________________________________________________________  

        elif type=="rta_cls" and action=="article":
                path = 'BD Embeddings Articles/lnk_art_emb_rta-cls.json'
                return path
        
        elif type=="rta_mp" and action=="article":
                path = 'BD Embeddings Articles/lnk_art_emb_rta-mp.json'
                return path
        
        elif type=="st_cls" and action=="article":
                path = 'BD Embeddings Articles/lnk_art_emb_st-cls.json'
                return path
        
        elif type=="st_mp" and action=="article":
                path = 'BD Embeddings Articles/lnk_art_emb_st-mp.json'
                return path
        
        #_________________pesos article____________________________________(falta bert)
        #_____________________________________________________________  

        elif type=="rta_cls" and action=="pesos":
                path = 'BD pesos look dict/lnk_pesos_emb_rta-cls.json'
                return path
        
        elif type=="rta_mp" and action=="pesos":
                path = 'BD pesos look dict/lnk_pesos_emb_rta-mp.json'
                return path
        
        elif type=="st_cls" and action=="pesos":
                path = 'BD pesos look dict/lnk_pesos_emb_st-cls.json'
                return path
        
        elif type=="st_mp" and action=="pesos":
                path = 'BD pesos look dict/lnk_pesos_emb_st-mp.json'
                return path
        
        result = "embedding doesnt exist"
        return result
        
#___________________________________________________________________________   
#___________________________________________________________________________    



        
if __name__=='__main__':

        #aqui va el texto de la base de datos 
        text1 = "The woman is playing in the park"
        text2 = "the woman is playing in the park"


        #__________________________embeddings with mean_pooling__________________________

        embedding1_mp = embedder(text1, "st_mp")
        embedding2_mp = embedder(text2, "st_mp")
        print(embedding2_mp.size())

        producto = torch.dot(embedding1_mp[0], embedding2_mp[0]).to(device)
        similarity = F.cosine_similarity(embedding1_mp[0], embedding2_mp[0], dim=0)
        print(f"Similitud coseno Mean_poolin: {similarity}")
        print(f"Producto punto Mean_poolin: {producto.item()}")

        #__________________________embeddings with CLS vector__________________________


        embedding1_cls = embedder(text1, "st_cls")
        embedding2_cls = embedder(text2, "st_cls")

        producto = torch.dot(embedding1_cls[0], embedding2_cls[0]).to(device)
        similarity = F.cosine_similarity(embedding1_cls[0], embedding2_cls[0], dim=0)
        print(f"Similitud coseno CLS vector: {similarity}")
        print(f"Producto punto CLS vector: {producto.item()}")