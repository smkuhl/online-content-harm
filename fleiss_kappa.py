import statsmodels.api as sm
from statsmodels.stats import inter_rater as irr
import pandas as pd
from patsy import dmatrices
import argparse
import numpy as np


def main():
    parser = argparse.ArgumentParser(description='Calculate Fleiss Kappa')

    parser.add_argument('--subject_type', '-s', choices=['expert', 'lay', 'both'], default='both', help='Processing mode.')
    args = parser.parse_args()
    mode = args.subject_type
    
    if mode == 'lay':
        df = pd.read_csv("../data/fleiss_kappa_lay_data.csv")
    elif mode == 'expert':
        df = pd.read_csv("../data/fleiss_kappa_expert_data.csv")
    else:
        df = pd.read_csv("../data/both_data.csv")
        
    table = df.values  
    print(table.shape) 
     
    data, cats = irr.aggregate_raters(table)
    kappa = irr.fleiss_kappa(data, method='fleiss')
    print(kappa)
    
    arr = []
    # calculate per question
    i = 0
    for index, row in df.iterrows():
        # print(row)
        table = row.values.reshape(6,1)
        print(table.shape)
        data, cats = irr.aggregate_raters(table)
        kappa = irr.fleiss_kappa(data, method='fleiss')
        arr.append(kappa)
        if i % 5 == 0:
            arr. append(np.average(arr[i-5:i]))
    
    np_array = np.array(arr)
    np_array.resize((51, 7))
    
    np.savetxt("../results/per_tweet_results.csv", np_array, delimiter=',')
    

if __name__ == '__main__':
    main()

