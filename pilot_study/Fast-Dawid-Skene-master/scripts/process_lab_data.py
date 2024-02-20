import os
import pandas as pd



def kappa_columns(row):
    if pd.notna(row['Yes']):
        return 1
    elif pd.notna(row['No']):
        return 0
    elif pd.notna(row['Cannot Answer']):
        return 2
    else:
        return None

def fds_columns(row):
    if pd.notna(row['Yes']):
        return "A1"
    elif pd.notna(row['No']):
        return "A0"
    elif pd.notna(row['Cannot Answer']):
        return "A2"
    else:
        return None

annotator = 0
questions = []
num_tweets = 1

for i in range(0, 51 * num_tweets):
    questions.append('Q'+ str(i))
    
start_dir = 'data/lab_data'  # Change this to your folder path

for folder_name in os.listdir(start_dir):
    # initialize new dataframes for the new tweet
    kappa_df = pd.DataFrame()
    fds_df = pd.DataFrame(columns=['Participant', 'Question', 'Annotation'])
    tweet_num = folder_name[6]
    # print(folder_name)
    sub_path = os.path.join(start_dir, folder_name)
    for filename in os.listdir(sub_path):
        temp_df = pd.read_excel(os.path.join(sub_path, filename), skiprows=1, header=0)
        temp_df.drop(temp_df.index[-1], inplace=True)
        
        # prep data for fast_dawid_skene.py
        temp_fds_df = pd.DataFrame()
        arr = ["P" + str(annotator)] * 51
        temp_fds_df['Annotation'] = temp_df.apply(fds_columns, axis=1)
        temp_fds_df['Participant'] = pd.Series(arr)
        temp_fds_df['Question'] = pd.Series(questions)
        fds_df = pd.concat([fds_df, temp_fds_df], axis=0, ignore_index=True)
        
        # prep data for fleiss_kappa.py
        kappa_df[annotator] = temp_df.apply(kappa_columns, axis=1)
        annotator += 1      
                
    annotator = 0   
    fds_df.to_csv("data/lab_data_processed/" + str(tweet_num) + "_crowd.csv", ",")      
    kappa_df.to_csv("data/lab_data_processed/" + str(tweet_num) + "_fleiss_kappa.csv", ",")



