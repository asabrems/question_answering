import pandas as pd
from sentence_transformers import SentenceTransformer
from ast import literal_eval
model = SentenceTransformer('all-MiniLM-L6-v2')


class Model():
  

    def generate_embeddings(self,text):
        sentence_embeddings = model.encode(text)[0]#, convert_to_tensor=True)[0]
        
        return sentence_embeddings





'''
the main functtion demonstrates how embeddings were generated for Corpus provided

'''
if __name__ == "__main__":
    #df = pd.read_csv('F:\personal\KwameAI\docs\passage_metadata.csv')
    df =pd.read_csv('/mnt/f/personal/KwameAI/docs/passage_metadata1.csv')
    
    sentence_Trans= []

    for i in df.index:
          
        try:
            
            sentence_embeddings = model.encode([df['passage'][i]])[0]

            
          
            x= {'passage':df['passage'][i],'embeddings':sentence_embeddings,'metadata':df['metadata'][i]}
            sentence_Trans.append(x)
        except Exception as e:
            print(df['passage'][i], e)
    
    df = pd.DataFrame(sentence_Trans)
   
    df.to_csv('/mnt/f/personal/KwameAI/docs/passage_metadata_emb1.csv',index=False)
