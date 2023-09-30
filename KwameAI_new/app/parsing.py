from elasticsearch import Elasticsearch, helpers
import elasticsearch
import pandas as pd
import csv
from model import *
import csv


es = Elasticsearch([{'host': 'localhost', 'port': 9200}], timeout=50)
index_name= 'question_answers'
import numpy as np
model_emb= Model()

def question_es_search(question,size=3):
    #question = ['What is a valid offer']
    question = [question]
    question_embeddings = np.array(list(map(float,model_emb.generate_embeddings(question))))


    es.indices.refresh(index=index_name)
    doc_count = es.count(index=index_name)['count']
    print(doc_count)
    body2 = {
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": question_embeddings}
                }
            }
        },
        "size": size # We want the top 3 most relevant passages
    }

    try:
        response = es.search(index=index_name, body=body2)
        #print(response)
    except elasticsearch.exceptions.RequestError as e:
        print("Detailed Error Information:", e.info)

    return response, question





#extracting results and saving it 

def retrieving_answers(response,question):
            
            row={}
       
            
            row['Question'] = question

            for idx, hit in enumerate(response['hits']['hits']):

                idx += 1  # We are going to use it for string formatting, so increment by 1 to start from 1 instead of 0
                row[f'Passage {idx}'] = hit['_source']['passage']  # Assuming the fieldname in Elasticsearch is 'passage'
                row[f'Relevance Score {idx}'] = hit['_score']
                row[f'Passage {idx} Metadata'] = hit['_source']['metadata']  # Assuming the fieldname in Elasticsearch is 'metadata'
            
        
           
   
            return row

'''
this was created to test how one could retrieve an answer based on question provided
'''

if __name__ == "__main__":
    question ="What is a valid offer?"
    response,_ = question_es_search(question,size=3)
    output =retrieving_answers(response,question)
   
    df = pd.DataFrame.from_dict([output])
    
    filename = 'D:\KwameAI\docs\question_answers.csv'
    df.to_csv(filename,index=False)
    