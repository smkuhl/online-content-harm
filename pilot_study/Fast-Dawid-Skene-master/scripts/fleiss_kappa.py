import statsmodels.api as sm
from statsmodels.stats import inter_rater as irr
import pandas as pd
from patsy import dmatrices
import argparse
import numpy as np
from collections import defaultdict
import json


def main(input=None):
    parser = argparse.ArgumentParser(description='Calculate Fleiss Kappa')
    parser.add_argument('--return_type', '-r', choices=['yes', 'no'], default='yes', help='Processing mode.')
    parser.add_argument('--subject_type', '-s', choices=['expert', 'lay', 'both', 'none'], default='none', help='Processing mode.')
    parser.add_argument('--tweet', '-t', choices=['yes', 'no'], default='no', help='Processing mode.')
    parser.add_argument('--dimension', '-d', choices=['yes', 'no'], default='no', help='Processing mode.')
    args = parser.parse_args()
    mode = args.subject_type
    tweet = args.tweet
    dimension = args.dimension
    ret = args.return_type
    
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
    
    if ret == 'yes':
        return kappa
    
    # calculate per tweet
    if tweet == 'yes':
        tweet_df = pd.DataFrame()
        num_sections = 6
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
                
        
        tweet_df.to_csv("results/per_tweet_results.csv", index=False)
        
    # calculate per dimension (believability, likelihood of spread, etc.)
    '''
    num questions per section:
    arr0 actionability: 9
    arr1 exploitability: 10
    arr2 likelihood of spread: 14
    arr3 believability: 12
    arr4 social fragmentation: 6
    '''
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
        
        dim_df.to_csv("results/per_dimension_results.csv", index=False)    
        

        
    

if __name__ == '__main__':
    main()

