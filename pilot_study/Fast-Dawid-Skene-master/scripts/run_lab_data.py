import os
import pandas as pd
import subprocess

import fleiss_kappa

start_dir = "data\lab_data_processed"

num_tweets = 6
k_score_df = pd.DataFrame()
k_score_df['Tweet'] = range(0, num_tweets)
kappa_scores = []
num_annotators = 2 # num participants per tweet
num_participants = 12 # total num participants

acc_df = pd.DataFrame()
acc = []

for filename in os.listdir(start_dir):
    if 'fleiss_kappa' in filename:
        df = pd.read_csv(os.path.join(start_dir, filename))
        df = df.iloc[:, 1:] # first column is the indices
        columns_with_nan = df.columns[df.isna().any()].tolist()
        df = df.drop(columns=columns_with_nan)
        args = ['-r', 'yes']
        kappa = fleiss_kappa.main(df)
        kappa_scores.append(kappa)
        
    if 'crowd' in filename:
        tweet_num = filename[0]
        command = 'python scripts/fast_dawid_skene.py --dataset_path data\lab_data_processed --output results/lab_results/' + tweet_num + '_true_labels.csv --algorithm FDS --dataset ' + tweet_num + '_crowd.csv'
        subprocess.run(command, shell=True)
        
        # calculate accuracy of each annotator
        true_labels = pd.read_csv('results/lab_results/' + tweet_num + '_true_labels.csv')
        crowd_df = pd.read_csv('data/lab_data_processed/' + tweet_num + '_crowd.csv')

        for i in range(num_annotators):
            condition = crowd_df['Participant'] == 'P' + str(i)
            p_df = crowd_df[condition]
            true_series = true_labels['Annotation'].reset_index(drop=True)
            pred_series = p_df['Annotation'].reset_index(drop=True)
            matches = true_series == pred_series
            accuracy = matches.mean()
            print(accuracy)
            acc.append(accuracy)
            
        
k_score_df['Score'] = kappa_scores
k_score_df.to_csv("results\lab_kappa_score.csv", ",")
acc_df['Participant'] = range(num_participants)
acc_df['Accuracy'] = acc
acc_df.to_csv("results\lab_fds.csv", ",")

        
    
    