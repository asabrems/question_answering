
import pandas as pd
df =pd.read_csv('C:/Users/freea/Desktop/KwameAI_new/docs/evaluation_rated.csv')
performance=[]
for i in df.index:
            #idx += 1  # We are going to use it for string formatting, so increment by 1 to start from 1 instead of 0
            #'Is Passage 1 Relevant? (Yes/No)
            count_ =[]
            count_.append(df['Is Passage 1 Relevant? (Yes/No)'][i])
        
            count_.append(df[' Is Passage 2 Relevant? (Yes/No)'][i])
            count_.append(df[' Is Passage 3 Relevant? (Yes/No)'][i])
            yes_count = count_.count('yes')
            top_1_acc = (yes_count/1)*100
            top_3_acc = (yes_count/3)*100
            #print(yes_count,top_1_acc,top_3_acc)
            performance.append({
                "Question":df['Question'][i],
                "top_1_acc":top_1_acc,
                "top_3_acc":top_3_acc
            })
df= pd.DataFrame(performance)
file_path = 'C:/Users/freea/Desktop/KwameAI_new/docs/performance.csv'
df.to_csv(file_path,index=False)
 
            
            