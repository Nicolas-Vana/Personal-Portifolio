# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 17:27:33 2021

@author: nicol
"""

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

os.chdir(r'D:\Projeto CM\Versões do Modelo\V25 correcao em como o ge é calculado')


df_contrast = pd.read_csv('Spike-Contrast dataframe.csv', sep = ';')
df_spc = pd.read_csv('SPC dataframe.csv', sep = ';')
df_sc = pd.read_csv('Spike-Count dataframe.csv', sep = ';')


os.chdir(r'D:\Projeto CM\Versões do Modelo\V25 correcao em como o ge é calculado\Boxplots')
path = os.getcwd()

fig, ax = plt.subplots()
fig.set_figheight(7.5)
fig.set_figwidth(10)

ax = sns.boxplot(x="sigma", y="Spike-Contrast", data=df_contrast)
ax.tick_params(axis='x', labelsize=16, rotation = 20)
ax.set_title('Boxplot Spike-Contrast')

fig.savefig('Boxplot Spike-Contrast.png')
plt.close(fig)

fig, ax = plt.subplots()
fig.set_figheight(7.5)
fig.set_figwidth(10)

ax.set_title('Boxplot Spike-Count')
ax = sns.boxplot(x="sigma", y='Total spikes', data=df_sc)

os.chdir(r'D:\Projeto CM\Versões do Modelo\V25 correcao em como o ge é calculado\Boxplots')
fig.savefig('Boxplot Spike-Count.png', dpi = 300)


centers = [49, 109, 169, 53, 113, 173, 57, 117, 177]

for center in centers:
    os.chdir(path)
    os.chdir(str(center))
    for local in ['True', 'False']:
        for metric in ['mean vec absolute value', 'mean vec absolute angle']:
        

            temp = df_spc[(df_spc['locality'] == local) & (df_spc['center'] == center)]
            
            fig, ax = plt.subplots()
            fig.set_figheight(7.5)
            fig.set_figwidth(10)
            
            if local:
                ax.set_title('Boxplot SPC local ' + metric)
            else:
                ax.set_title('Boxplot SPC non-local ' + metric)
            
            ax = sns.boxplot(x="sigma", y=metric, data=temp)
            ax.tick_params(axis='x', labelsize=12, rotation = 20)
            
            if local:
                fig.savefig('Boxplot SPC local ' + metric + '.png')
            else:
                fig.savefig('Boxplot SPC non-local ' + metric + '.png')
            plt.close(fig)
            











