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


def heatmap(data,row_labels,col_labels,ax=None,cbar_kw={},cbarlabel="",**kwargs):
    if not ax:
        ax = plt.gca()

    # Plot the heatmap    
    im = ax.imshow(data,**kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im,ax=ax,**cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom",rotation_mode="anchor")
    #cbar.set_clim(-0.5,1)

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_xticklabels(labels=col_labels)
    ax.set_yticks(np.arange(data.shape[0]))
    ax.set_yticklabels(labels=row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-45, ha="right",rotation_mode="anchor")

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}", textcolors=("black", "white"),threshold=None, **textkw):
    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2

    # Set default alignment to center, but allow it to be overwritten by textkw.
    kw = dict(horizontalalignment="center",verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts



if __name__ == '__main__':

    df = pd.read_csv(sys.argv[1],index_col=0)
    names = []
    for name in df.columns:
        names.append(name.split('-')[0][5:])

    fig, ax = plt.subplots()
    im, cbar = heatmap(df, df.index, names, ax=ax, cmap ='Blues',cbarlabel='RMSD',vmax=1)
    #im, cbar = heatmap(hbond, res_unique, res_unique, ax=ax, cmap ='Spectral',cbarlabel='distance')
    #texts = annotate_heatmap(im, valfmt="{x:.2f}")

    fig.tight_layout()
    #plt.show()
    outname = sys.argv[1].replace('csv','png')
    plt.savefig(outname,dpi=150)
