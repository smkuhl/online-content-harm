import statsmodels.api as sm
from statsmodels.stats import inter_rater as irr
import pandas as pd
from patsy import dmatrices
import argparse
import numpy as np
from collections import defaultdict
import json
from sklearn.metrics import cohen_kappa_score


def main(input=None, return_type='yes', subject_type=None, tweet='no', dimension='no', num_tweets=6):
    
    mode = subject_type
    '''
    if mode == 'lay':
        df = pd.read_csv("data/fleiss_kappa_lay_data.csv")
    elif mode == 'expert':
        df = pd.read_csv("data/fleiss_kappa_expert_data.csv")
    elif mode == 'both':
        df = pd.read_csv("data/both_data.csv")
    else:
        df = input
        
    table = df.values  
    # print(table.shape) 
     
    data, cats = irr.aggregate_raters(table)
    kappa = irr.fleiss_kappa(data, method='fleiss')
    print(kappa)

    # calculate per tweet
    if tweet == 'yes':
        tweet_df = pd.DataFrame()
        num_sections = num_tweets
        sections = np.array_split(df, num_sections)
        for i in range(0, num_sections):
            table = sections[i].values
            data, cats = irr.aggregate_raters(table)
            kappa = irr.fleiss_kappa(data, method='fleiss')
            tweet_df[str(i + 1)] = [kappa]
            # Tweet 6 had very low agreement so I want to calculate the expert and lay agreement separately
            
            if i == 5:
                print(table.shape)
                expert_table = table[:, :2]
                lay_table = table[:, 2:]
                expert_data, _ = irr.aggregate_raters(expert_table)
                lay_data, _ = irr.aggregate_raters(lay_table)
                expert_kappa = irr.fleiss_kappa(expert_data, method='fleiss')
                lay_kappa = irr.fleiss_kappa(lay_data, method='fleiss')
                print("expert kappa for tweet 6: " + str(expert_kappa))
                print("lay kapp for tweet 6: " + str(lay_kappa))
                  
        print(tweet_df)
        # tweet_df.to_csv("results/per_tweet_results.csv", index=False)
        
    # calculate per dimension (believability, likelihood of spread, etc.)
    
    num questions per section:
    arr0 actionability: 9
    arr1 exploitability: 10
    arr2 likelihood of spread: 14
    arr3 believability: 12
    arr4 social fragmentation: 6
    
    if dimension == 'yes':
        dim_df = pd.DataFrame()
        sections = []
        section_sizes = [9, 10, 14, 12, 6] * 6  # Define the number of rows for each section for 6 repetitions
        start_index = 0
        for size in section_sizes:
            section = df.iloc[start_index:start_index+size]
            sections.append(section)
            start_index += size
            
        dict = {'arr0': sections[0],
                'arr1': sections[1],
                'arr2': sections[2],
                'arr3': sections[3],
                'arr4': sections[4]}
    
        for i in range(5, 30):
            arr = 'arr' + str(i % 5)
            dict[arr] = pd.concat([dict[arr], sections[i]])
      
        dim_df = pd.DataFrame()
        for key, val in dict.items():
            table = val.values
            data, cats = irr.aggregate_raters(table)
            kappa = irr.fleiss_kappa(data, method='fleiss')
            dim_df[key] = [kappa]
        
        print(dim_df)
        # dim_df.to_csv("results/per_dimension_results.csv", index=False)   
    
    kappa = irr.fleiss_kappa(data, method='fleiss')
    if return_type == 'yes':
        return kappa
    else:
        print(kappa) 
        
    '''
    '''
    lay_df = pd.read_csv("data/key_questions/lay_key.csv")
    expert_df = pd.read_csv("data/key_questions/expert_key.csv")
    get_cross_agreement(expert_df, lay_df)
    # print(lay_df.head())
    # print(lay_df.columns)
    
    both_df = pd.read_csv("data/key_questions/both_key.csv")
    get_key_by_dimension(both_df)
    '''
    # get agreement for xinyi and jim
    doc_df = pd.read_csv("data/expert_part_2.csv")
    expert_df = pd.read_csv("data/key_questions/expert_key.csv")
    lay_df = pd.read_csv("data/key_questions/lay_key.csv")
    expert_df = expert_df.drop(expert_df.columns[0], axis=1)
    lay_df = lay_df.drop(lay_df.columns[0], axis=1)
    doc_df.rename(columns={'Xinyi': '0', 'Jim': '1'}, inplace=True)
    
    # agreement between two post docs:
    kappa = cohen_kappa_score(doc_df['0'].values, doc_df['1'].values)
    print("xinyi - jim:" + str(kappa))
    
    # post docs w/ the other experts
    get_cross_agreement(doc_df, expert_df)
    
    # post docs w/ lay people
    get_cross_agreement(doc_df, lay_df)
    
    # fleiss kappa for all 4 experts
    table = pd.concat([expert_df, doc_df], axis=1)
    data, cats = irr.aggregate_raters(table)
    kappa = irr.fleiss_kappa(data, method='fleiss')
    print("fleiss kappa score for all experts: " + str(kappa))
    
    table = pd.concat([table, lay_df], axis=1)
    data, cats = irr.aggregate_raters(table)
    kappa = irr.fleiss_kappa(data, method='fleiss')
    print("fleiss kappa score for all 8 participants: " + str(kappa))
    
    
def get_key_by_dimension(df):
    '''
    num questions per section:
    arr0 actionability: 3
    arr1 exploitability: 4
    arr2 likelihood of spread: 2
    arr3 believability: 3
    arr4 social fragmentation: 3
    '''
    dim_df = pd.DataFrame()
    sections = []
    section_sizes = [3, 4, 2, 3, 3] * 6  # Define the number of rows for each section for 6 repetitions
    start_index = 0
    for size in section_sizes:
        section = df.iloc[start_index:start_index+size]
        sections.append(section)
        start_index += size
        
    dict = {'arr0': sections[0],
            'arr1': sections[1],
            'arr2': sections[2],
            'arr3': sections[3],
            'arr4': sections[4]}

    for i in range(5, 30):
        arr = 'arr' + str(i % 5)
        dict[arr] = pd.concat([dict[arr], sections[i]])
    
    dim_df = pd.DataFrame()
    for key, val in dict.items():
        expert_df = val.iloc[:, :3]
        lay_df = val.iloc[:, 3:]
        # print(lay_df.head())
        new_columns = ['0', '1', '2', '3']  # Provide new names for all columns
        lay_df.columns = new_columns
        if key == 'arr3':
            print(lay_df.tail())
        expert_kappa, arr1, arr2 = get_cross_agreement(expert_df, lay_df)
        # print(expert_kappa)
        dim_df[key] = expert_kappa # tuple: expert_kappa, expert v lay array, lay v lay array
    
    # print(dim_df)
    # dim_df.to_csv("temp/corss_key_per_dimension_results.csv")   
    
            


            
def get_cross_agreement(expert_df, lay_df): 
    e1 = expert_df['0']
    e2 = expert_df['1']
    e_col = expert_df.columns
    expert_kappa = cohen_kappa_score(e1.values, e2.values)
    print("expert x - y: " + str(expert_kappa))
    
    # between each expert and each lay person
    arr1 = np.zeros((2, 4))
    for i in range(0,2):
        column = str(i)
        expert = expert_df[column]
        print(range(len(lay_df.columns)))
        for j in range(len(lay_df.columns)):
            column = str(j)
            lay = lay_df[column]
            kappa = cohen_kappa_score(expert.values, lay.values)
            # UNCOMMENT THIS FOR SCORES print("(" + str(i) + ", " + str(j) + "): " + str(kappa))
            arr1[i][j] = kappa
    print(arr1)
    
    '''
    # between each lay person
    arr2 = np.zeros((4,4))
    for i in range(0,4):
        column = str(i)
        lay1 = lay_df[column]
        for j in range(len(lay_df.columns)):
            column = str(j)
            lay2 = lay_df[column]
            kappa = cohen_kappa_score(lay1.values, lay2.values)
            # UNCOMMENT print("(" + str(i) + ", " + str(j) + "): " + str(kappa))
            arr2[i][j] = kappa
            
    # print((lay_df['0'].values) == (lay_df['3'].values))  # check that participants a and d answered everything the same
    # print(arr2)
    
    return expert_kappa, arr1, arr2
    '''
        

        
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate Fleiss Kappa')
    parser.add_argument('--return_type', '-r', choices=['yes', 'no'], default='yes', help='return score or print')
    parser.add_argument('--subject_type', '-s', choices=['expert', 'lay', 'both', 'none'], default='none', help='use pilot lay people or expert datasets')
    parser.add_argument('--tweet', '-t', choices=['yes', 'no'], default='no', help='separate kappa score by tweet (1-6)')
    parser.add_argument('--dimension', '-d', choices=['yes', 'no'], default='no', help='separate kappa score by dimension')
    args = parser.parse_args()
    
    main(input=None, return_type=args.return_type, subject_type=args.subject_type, tweet=args.tweet, dimension=args.dimension)

