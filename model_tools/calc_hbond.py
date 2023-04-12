"""
This is a program written by Qianyi Cheng
at University of Memphis.
"""

import numpy as np
import pandas as pd
import sys, re, argparse

def atoi(text):
        return int(text) if text.isdigit() else text


def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


def extract_hbond(df,out,dfr):
    names = df.columns
    #for i in range(len(names)):
    #    print(names[i])
    num = len(names)
    res_unique = np.unique(df['chain-resid'])
    res_unique = sorted(res_unique,key=natural_keys)
    
    res_r_unique = np.unique(dfr['chain-resid'])
    res_r_unique = sorted(res_r_unique,key=natural_keys)
    ### Typical hydrogen bond length less than 3.5 A ###
    
    num_res = len(res_unique)
    num_r_res = len(res_r_unique)
    hbond = pd.DataFrame(0,columns=res_r_unique,index=res_r_unique)
    
    for i in range(num-2):
        if df['atom'][i][0] == 'H':
            for j in range(2,num):
                if df.iloc[i,j].astype(float) <= 3.5 and df.iloc[i,j] > 0 and df['atom'][j-2][0] != 'H':
                    idx1 = res_r_unique.index(df['chain-resid'][i])
                    idx2 = res_r_unique.index(df['chain-resid'][j-2])
                    hbond.iloc[idx1,idx2] += 1
    hbond.to_csv(out)
    return hbond


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Read distmat csv file, write hbond csv files')
    parser.add_argument('-csv1', dest='csv1', default=None, help='opt_csv1')
    parser.add_argument('-csv2', dest='csv2', default=None, help='opt_csv2')

    args = parser.parse_args()
    csv1 = args.csv1
    csv2 = args.csv2

    dfr = pd.read_csv(csv1,header=0)
    df  = pd.read_csv(csv2,header=0)

    out = csv2.replace('distmat','hbond')
    hbond = extract_hbond(df, out, dfr)
    
