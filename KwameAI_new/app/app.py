from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from elasticsearch import Elasticsearch
from config import DevelopmentConfig
import logging
import os
from parsing import *
from retrieval import *
from indexing import *
from dotenv import load_dotenv
import json

#setup variables
load_dotenv()

# Setup Logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
api = Api(app)

# Load environment-specific configurations
app.config.from_object('config.' + os.getenv('FLASK_ENV', 'DevelopmentConfig'))

#instatiating various objects
document_retrieval = Retrieval()
model_embeddings = Model()
index_name ='question_answers'
indexing = Indexing(index_name)



class Question(Resource):
    def post(self):
        # Validate request
        data = request.get_json(force=True)
        if not data or not 'question' in data:
            return {'message': 'Invalid Request'}, 400

        # Process question
        size=6
        question = data['question']
        logging.info(f'Received Question: {question}')
        response,_ =question_es_search(question,size)
        answer = retrieving_answers(response,question)
        

        
        x =json.dumps(answer)
        return x,200

#this function can only process one file
class Document(Resource):
    def post(self): 
        # Handle Document Upload
        index_name = request.form.get('index_name')  # getting a string parameter
        uploaded_file = request.form.get('file_path')#request.files['file'] 
        logging.info(f'Received Document: {uploaded_file}')
        #if uploaded_file.filename != '':
        if uploaded_file != '':
            # Handle File Upload
            #logging.info(f'Received Document: {uploaded_file.filename}')
            logging.info(f'Received Document: {uploaded_file}')
 
            paragraphs= document_retrieval.parse_technicaltxt(uploaded_file)
            list_passages = document_retrieval.get_passage(paragraphs)
            #embeddings = model_embeddings.generate_embeddings(passage)
            embeddings = [model_embeddings.generate_embeddings([passage]) for passage in list_passages]
            
            #creating index
            indexing.create_index(index_name)
            if len(embeddings) == len(list_passages):
                actions = [indexing.index_param(list_passages[i],{},embeddings[i]) for i in range(len(embeddings))]
                if actions:
                    indexing.index_bulk_document(indexing.index_name,actions)          

        return json.dumps({'status': 'success'}), 200


api.add_resource(Question, '/question')
api.add_resource(Document, '/document')


if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv('PORT', 5001)))
