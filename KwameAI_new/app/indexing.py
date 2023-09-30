from elasticsearch import Elasticsearch, helpers
import elasticsearch
import pandas as pd
import csv
from model import *
import csv
import torch
import numpy as np

print(elasticsearch.__version__)
# Connect to the ElasticSearch instance.
es = Elasticsearch(["localhost:9200"], timeout=50)
es.indices.delete(index='question_answers', ignore=[400, 404])

print(es.ping())



class Indexing():
    def __init__(self,index_name):
        self.index_name = index_name
          # Index structure
        self.mappings = {
            'settings':{
                'number_of_shards':1,
                'number_of_replicas':0
            },
            'mappings': {
                'properties': {
                    'passage': {'type': 'text'},
                    'metadata': {'type': 'object'}, 
                    'embedding': {'type': 'dense_vector', 'dims': 384}  
                }
            }
        }



    def index_document(self,index_name, doc_id, document):
        es.index(index=index_name, id=doc_id, body=document)
    
    def index_bulk_document(self,index_name,document):
        helpers.bulk(es,document)


    # Define a function to create an index.
    def create_index(self,index_name):
        es.indices.create(index=index_name,body=self.mappings)# ignore=400)

    def index_param(self,passage: str,metadata: object,embedding: list()):
        document_param = {
                "_op_type": "index",
                "_index": self.index_name,
                "_source": {
                    'passage':passage,
                    'metadata': metadata,
                    'embedding': np.array(embedding)
                }
            }
        return document_param
              


#https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_creating_an_index




# Read CSV file and index documents
'''this code can be commented out

it illustrates how i created a sample index using the data provided


'''
if __name__ == "__main__":
    es = Elasticsearch(["localhost:9200"], timeout=50)
    index_name= 'question_answers'
    indexing = Indexing(index_name)
    
    indexing.create_index(index_name)
    
    df =pd.read_csv('D:\KwameAI\docs\passage_metadata_emb.csv')
    actions=[]
    for i in df.index:
        
            embedding = df['embeddings'][i]
            emb =len(list(map(float, embedding[1:-1].split())))
        
            if emb != 384:
                print(f"Skipping row due to invalid embedding dimension: {len(embedding)}")
                continue  # skip this row
            passage = df['passage'][i]
            metadata= eval(df['metadata'][i])
            embedding= list(map(float, embedding[1:-1].split()))
            
            actions.append(indexing.index_param(passage,metadata,embedding))
            
    print(len(actions))
            
    if actions:
        
        indexing.index_bulk_document(index_name,actions)
    
    

    #.................................................
