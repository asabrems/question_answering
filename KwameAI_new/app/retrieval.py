#document parsing logic 
#kwame-legal-EL-1680770407105_Metadata
import os
import json
import re
import pandas as pd

class Retrieval():
  '''def __init__(self):
      x =0'''


  def read_txt(self,txt_file):
    with open(txt_file,mode='r',encoding='utf-8-sig') as f:
            lines = f.readlines()
    f.close()

    return lines




  def parsing_metadata(self,file_path):
    data =' '
    try:
      with open(file_path, 'r') as file:
          #data = json.load(file)
          try:
            data =json.loads(file.read())
          except Exception as e:
                  print(f"An unexpected error occurred: {str(e)}")
    except Exception as e:
                  print(f"An unexpected error occurred: {str(e)}")
      # Now 'data' contains the contents of the JSON file as a Python data structure (dict, list, etc.)
    #print(data)
    return data



  def get_passage(self,paragraph):
      #print("parap",paragraph)
      combined_passage= " ".join(paragraph)
      sentences = re.split(r'(?<=[.!?])\s+', combined_passage)
      #sentences = combined_passage.split('\n')
      #print(sentences)
      passage = []
      for i in range(0,len(sentences),5):
          
            passage.append(" ".join(sentences[i:i+5]))
            #print('...........................')

      return passage

      

  def parse_technicaltxt(self,file_path):
      with open(file_path, mode='r',encoding='utf-8-sig') as file:
          content = file.read()

      # Check whether the file is within a __section__
      sections = content.split('__section__')[1:]  # We skip the first part as it may not be a complete section
      #print(sections)
      # Extract passages within __paragraph__ markers in each section
      retrieved_paragraph = []
      for section in sections:
          
          paragraphs = section.split('__paragraph__')[1:]  # We skip the first part as it may not be a complete paragraph
          for paragraph in paragraphs:
              
              # Cleanup and standardize the extracted text
              cleaned_paragraph = paragraph.strip().replace('\n', ' ').replace('  ', ' ')
              retrieved_paragraph.append(cleaned_paragraph)
      
      return retrieved_paragraph

  def generate_id(self,file_):
        id = ''
        for chucks in file_.split('-'):
              if chucks.find('_')>-1:
                  id = chucks.split('_')[0]
                  break
        return id
              
            
      
'''
the main functtion demonstrates 
how the technical file and metadata for each provided document was parsed to generate the required csv file

'''     


if __name__ == "__main__":
    file_retrieval = Retrieval()
    #file_path = 'F:\personal\KwameAI\Corpus\kwame-legal-EL-1680770407105_Technical.txt'  # Replace with the actual path to your
    file_path = '/mnt/f/personal/KwameAI/Corpus'
    legal_files = {}
    for subdir, dirs, files in os.walk(file_path):
        for file_ in files:
             if os.path.exists(file_path):
                

                id = file_retrieval.generate_id(file_)
                if file_.endswith('Metadata.json'):
                     
                     legal_files[id] = [os.path.join(subdir,file_)]
                     
                elif file_.endswith("Technical.txt"):
                     if id in legal_files:
                          legal_files[id].append(os.path.join(subdir,file_))
                     else:
                        legal_files[id] = [os.path.join(subdir,file_)]
                     
             else:
                print(f"File not found: {file_path}")
    
    #parsing the dictionary and reading files 
    result = []
    
    
    for y in legal_files.values():
        try:
           
            
            passages = file_retrieval.get_passage(file_retrieval.parse_technicaltxt(y[1]))
           
           
            metadata =  [file_retrieval.parsing_metadata(y[0]).copy() for _ in range(len(passages))]
            
          
            if len(passages) >1:
                 
            
              result.extend([{'passage': passage, 'metadata': metadata} for passage, metadata in zip(passages, metadata)])
           
        except Exception as e:
            print('error',e)



    df = pd.DataFrame(result)
    
    
    df.to_csv('/mnt/f/personal/KwameAI/docs/passage_metadata1.csv',index=False)
    