# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 15:57:16 2021

@author: nicol
"""
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from statsmodels.tsa.api import SimpleExpSmoothing

os.chdir(r'D:\Projeto CM\Versões do Modelo\V25 correcao em como o ge é calculado')
df_multitaper = pd.read_csv('dataframe multitaper.csv', sep = ';')
df_multitaper['multitaper'] = 10*np.log10(df_multitaper['multitaper'])

df_multitaper_more_cells = pd.read_csv('dataframe multitaper more cells.csv', sep = ';')
df_multitaper_more_cells['multitaper'] = 10*np.log10(df_multitaper_more_cells['multitaper'])

os.chdir(r'D:\Projeto CM\Versões do Modelo\V25 correcao em como o ge é calculado\Multitaper CI')

fig, ax = plt.subplots()
fig.set_figheight(3)
fig.set_figwidth(5)

ax.set_xlim(10, 100)
ax.set_ylim(13, 35)
skip_bool = False

for sigma in df_multitaper['sigma'].unique().tolist():
    print(sigma)
    
    if skip_bool == True:
        skip_bool = False
        continue
    else:
        skip_bool = True
    
    tmp = df_multitaper[df_multitaper['sigma'] == sigma]
    
    sns.lineplot(data=tmp, x="freq", y="multitaper", ci='sd', ax = ax, label = str(sigma))
    #sns.set_palette(cmap, n_colors=len(df_multitaper['sigma'].unique().tolist()))

ax.set_ylabel('Power (dB)')
ax.set_xlabel('Frequency')
ax.set_title('Multitaper comparison with CI')

ax.legend()
fig.savefig('Multitaper for center cell.png', dpi = 300) ### Modificada
plt.close(fig)

# More cells

fig, ax = plt.subplots()
fig.set_figheight(7.5)
fig.set_figwidth(10)

ax.set_xlim(10, 80)
ax.set_ylim(-0, 35)
skip_bool = False

for sigma in df_multitaper_more_cells['sigma'].unique().tolist():
    print(sigma)
    
    if skip_bool == True:
        skip_bool = False
        continue
    else:
        skip_bool = True
    
    tmp = df_multitaper_more_cells[df_multitaper_more_cells['sigma'] == sigma]
    
    sns.lineplot(data=tmp, x="freq", y="multitaper", ci='sd', ax = ax, label = str(sigma))
    #sns.set_palette(cmap, n_colors=len(df_multitaper['sigma'].unique().tolist()))

ax.set_ylabel('Power (dB)')
ax.set_xlabel('Frequency')
ax.set_title('Multitaper comparison with CI')

ax.legend()
fig.savefig('Multitaper for more cells.png', dpi = 300) ### Modificada
plt.close(fig)


# More cells plots for each sigma

for sigma in df_multitaper['sigma'].unique().tolist():
    fig, ax = plt.subplots()
    fig.set_figheight(7.5)
    fig.set_figwidth(10)

    ax.set_xlim(10, 150)
    ax.set_ylim(-10, 50)

    #print(sigma)
    tmp = df_multitaper[df_multitaper['sigma'] == sigma]
    
    sns.lineplot(data=tmp, x="freq", y="multitaper", ci='sd', ax = ax, label = str(sigma))
    #sns.set_palette(cmap, n_colors=len(df_multitaper['sigma'].unique().tolist()))
    
    ax.legend()
    fig.savefig('Multitaper for center cell sigma = ' + str(sigma) + ' .png', dpi = 300) ### Modificada
    plt.close(fig)

# Boxplots for the maximum powers and corresponding frequencies for single cell

multitaper_maxs = []

os.chdir(r'D:\Projeto CM\Versões do Modelo\V25 correcao em como o ge é calculado\Multitaper CI\Smoothing')

for sigma in df_multitaper['sigma'].unique().tolist():
    for seed in df_multitaper['seed'].unique().tolist():
        
        tmp = df_multitaper[(df_multitaper['sigma'] == sigma) & (df_multitaper['seed'] == seed)]
        tmp.drop(columns = ['sigma', 'seed'], inplace = True)
        tmp.set_index('freq', inplace = True)
        
        smoothed = SimpleExpSmoothing(tmp, initialization_method="estimated").fit(smoothing_level=0.2, optimized=False)
        
        # Plots to check the level of smoothing
        
        '''fig, ax = plt.subplots()
        fig.set_figheight(7.5)
        fig.set_figwidth(10)
        
        ax.set_xlim(10, 150)
        ax.set_ylim(10, 45)
        
        
        ax.plot(tmp, marker="o", color="black", label = 'Raw')
        ax.plot(smoothed.fittedvalues, marker="x", color="blue", label = 'smoothed')
        
        plt.legend()        
        fig.savefig('Raw vs Smoothed comparison ' + str(sigma) + ' ' +  str(seed) + '.png', dpi = 300)'''
        
        # For smoothed data
        
        max_pow = np.max(smoothed.fittedvalues)
        max_freq = np.argmax(smoothed.fittedvalues)
        
        # For Raw data
        
        #max_pow = np.max(tmp['multitaper'])
        #max_freq = np.argmax(tmp['multitaper'])
        
        multitaper_maxs.append([sigma, seed, max_pow, max_freq])
    



maxs_df = pd.DataFrame(multitaper_maxs, columns = ['sigma', 'seed', 'max_pow', 'max_freq'])

os.chdir(r'D:\Projeto CM\Versões do Modelo\V25 correcao em como o ge é calculado\Boxplots\Multitaper')

for metric in ['max_pow', 'max_freq']:
    fig, ax = plt.subplots()
    fig.set_figheight(7.5)
    fig.set_figwidth(10)
    
    sns.boxplot(x="sigma", y=metric, data=maxs_df)
    sns.stripplot(x="sigma", y=metric, data=maxs_df)
    
    fig.savefig('Smoothed multitaper ' + metric +  ' for center cell.png', dpi = 300)

# Boxplots for the maximum powers and corresponding frequencies for more cells

multitaper_maxs = []

for sigma in df_multitaper_more_cells['sigma'].unique().tolist():
    for seed in df_multitaper_more_cells['seed'].unique().tolist():
        for cell in df_multitaper_more_cells['cell'].unique().tolist():
            
            tmp = df_multitaper[(df_multitaper['sigma'] == sigma) & (df_multitaper['seed'] == seed)]
            tmp.drop(columns = ['sigma', 'seed'], inplace = True)
            tmp.set_index('freq', inplace = True)
            
            smoothed = SimpleExpSmoothing(tmp, initialization_method="estimated").fit(smoothing_level=0.2, optimized=False)
            
            # For smoothed data
            
            max_pow = np.max(smoothed.fittedvalues)
            max_freq = np.argmax(smoothed.fittedvalues)
            
            # For Raw data
            
            #max_pow = np.max(tmp['multitaper'])
            #max_freq = np.argmax(tmp['multitaper'])
            
            multitaper_maxs.append([sigma, seed, max_pow, max_freq])
            
            
            multitaper_maxs.append([sigma, seed, cell, max_pow, max_freq])
    

maxs_df = pd.DataFrame(multitaper_maxs, columns = ['sigma', 'seed', 'cell', 'max_pow', 'max_freq'])

os.chdir(r'D:\Projeto CM\Versões do Modelo\V25 correcao em como o ge é calculado\Boxplots\Multitaper')

for metric in ['max_pow', 'max_freq']:
    fig, ax = plt.subplots()
    fig.set_figheight(7.5)
    fig.set_figwidth(10)
    
    sns.boxplot(x="sigma", y=metric, data=maxs_df)
    sns.stripplot(x="sigma", y=metric, data=maxs_df)
    
    fig.savefig('Smoothed multitaper ' + metric +  ' for more cells.png', dpi = 300)


















