"""
This is a program written by Qianyi Cheng
at University of Memphis.
"""

import os, sys, re
import argparse
import pandas as pd
import numpy as np
import sys, re
import matplotlib.pyplot as plt
import matplotlib
import matplotlib as mpl
from plot_heatmap import *

def atoi(text):
        return int(text) if text.isdigit() else text


def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


df1 = pd.read_csv(sys.argv[1],header=0,index_col=0)
df2 = pd.read_csv(sys.argv[2],header=0,index_col=0)

#delta_df = df1.sub(df2, fill_value=0)
#print(delta_df)                

delta = df1.to_numpy() - df2.to_numpy()
names = []
for name in df1.columns:
    names.append(name.split('-')[0][5:])
#print(names)

fig, ax = plt.subplots()
im, cbar = heatmap(delta, df1.index, names, ax=ax, cmap ='RdBu',vmin=-1.0,vmax=1.0,cbarlabel='RMSD')
#im, cbar = heatmap(hbond, res_unique, res_unique, ax=ax, cmap ='Spectral',cbarlabel='distance')
#texts = annotate_heatmap(im, valfmt="{x:.2f}")

fig.tight_layout()
plt.savefig('diff.png',dpi=150)
