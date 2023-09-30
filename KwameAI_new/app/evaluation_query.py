#python file created to generate answers for each question provided in user_query.txt
from parsing import  *
import tqdm
from tqdm import tqdm
textfile= ''
file_path = "D:/KwameAI/user_queries.txt"
with open(file_path,'r',encoding='utf-8') as f:
    lines = f.readlines()

responses = []

for question in tqdm(lines):
    response,_ = question_es_search(question)
    answers =retrieving_answers(response,question)
    answers['Question']= question
    responses.append(answers)

df = pd.DataFrame(responses,columns=['Question', 'Passage 1', 'Relevance Score 1', 'Passage 1 Metadata', 'Is Passage 1 Relevant? (Yes/No)',
                    'Passage 2', 'Relevance Score 2', 'Passage 2 Metadata', ' Is Passage 2 Relevant? (Yes/No)',
                    'Passage 3', 'Relevance Score 3', 'Passage 3 Metadata',' Is Passage 3 Relevant? (Yes/No)'])
file_path = 'D:\KwameAI\docs\evaluation.csv'
df.to_csv(file_path,index=False)





