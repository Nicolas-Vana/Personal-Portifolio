# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 16:45:52 2021

@author: nicol
"""

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

os.chdir(r'D:\Projeto CM\Versões do Modelo\V25 correcao em como o ge é calculado')


df_contrast = pd.read_csv('Spike-Contrast dataframe.csv', sep = ';')
df_spc = pd.read_csv('SPC dataframe passband 30-50.csv', sep = ';')
df_sc = pd.read_csv('Spike-Count dataframe.csv', sep = ';')
df_heatmap = pd.read_csv('Heatmap Stats dataframe passband 30-50.csv', sep = ';') ### Modificada


os.chdir(r'D:\Projeto CM\Versões do Modelo\V25 correcao em como o ge é calculado\Standard Error Plots')
path = os.getcwd()

fig, ax = plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(15)

mean_list = []
se_list = []

sigmas = df_contrast['sigma'].unique().tolist()
del sigmas[-1]

#Spike contrast Standard Error Plot

#tmp = df_contrast.groupby(['sigma']).mean().reset_index()
sns.pointplot('sigma', 'Spike-Contrast', data=df_contrast, linestyles='', scale = 1, marker="$\circ$", ec="face", s=100)

ax.set_title('Standard-Error Spike-Contrast', fontsize = 20)
ax.set_xlabel('Sigma', fontsize=16)
ax.set_ylabel('Spike-Contrast', fontsize=16)
ax.tick_params(axis='x', labelsize=16, rotation = 45)
ax.tick_params(axis='y', labelsize=16)

fig.savefig('Standard Error Plot Spike Contrast.png', dpi = 300)
plt.close(fig)

#Spike Count Standard Error Plot

fig, ax = plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(15)

sns.pointplot('sigma', 'Total spikes', data=df_sc, linestyles='', scale = 1, marker="$\circ$", ec="face", s=100)

ax.set_title('Standard-Error Spike Count', fontsize = 20)
ax.set_xlabel('Sigma', fontsize=16)
ax.set_ylabel('Total spikes', fontsize=16)
ax.tick_params(axis='x', labelsize=16, rotation = 45)
ax.tick_params(axis='y', labelsize=16)

fig.savefig('Standard Error Plot Spike Count.png', dpi = 300)
plt.close(fig)

#Spike Count Standard Error Plot

metrics = ['mean_abs','std_abs','mean_angle','std_angle']

for locality in df_heatmap['local'].unique().tolist():
    for metric in metrics:
        tmp = df_heatmap[df_heatmap['local'] == locality]
        fig, ax = plt.subplots()
        fig.set_figheight(10)
        fig.set_figwidth(15)
        
        sns.pointplot('sigma', metric, data=tmp, linestyles='', marker="$\circ$", scale = 1)
        
        ax.set_title('Standard-Error ' + metric + ' ' + locality , fontsize = 20)
        ax.set_xlabel('Sigma', fontsize=16)
        ax.set_ylabel(metric, fontsize=16)
        ax.tick_params(axis='x', labelsize=16, rotation = 45)
        ax.tick_params(axis='y', labelsize=16)
        
        if 'std' in metric:
            os.chdir(r'D:\Projeto CM\Versões do Modelo\V25 correcao em como o ge é calculado\Standard Error Plots\Heatmap SE\STD')
        if 'mean' in metric:
            os.chdir(r'D:\Projeto CM\Versões do Modelo\V25 correcao em como o ge é calculado\Standard Error Plots\Heatmap SE\Mean')
        fig.savefig('Standard Error Plot ' + metric + ' ' + locality + ' filt freq 50.png', dpi = 300) ### Modificada
        plt.close(fig)

# =============================================================================
# 
# ax = sns.boxplot(x="sigma", y="Spike-Contrast", data=df_contrast)
# ax.tick_params(axis='x', labelsize=16, rotation = 20)
# ax.set_title('Boxplot Spike-Contrast')
# 
# fig.savefig('Boxplot Spike-Contrast.png')
# plt.close(fig)
# 
# fig, ax = plt.subplots()
# fig.set_figheight(7.5)
# fig.set_figwidth(10)
# 
# ax.set_title('Boxplot Spike-Count')
# ax = sns.boxplot(x="sigma", y='Total spikes', data=df_sc)
# 
# os.chdir(r'D:\Projeto CM\Versões do Modelo\V25 correcao em como o ge é calculado\Boxplots')
# fig.savefig('Boxplot Spike-Count.png', dpi = 300)
# 
# 
# centers = [49, 109, 169, 53, 113, 173, 57, 117, 177]
# 
# for center in centers:
#     os.chdir(path)
#     os.chdir(str(center))
#     for local in [True, False]:
#         for metric in ['mean vec absolute value', 'mean vec absolute angle']:
#         
# 
#             temp = df_spc[(df_spc['locality'] == local) & (df_spc['center'] == center)]
#             
#             fig, ax = plt.subplots()
#             fig.set_figheight(7.5)
#             fig.set_figwidth(10)
#             if local:
#                 ax.set_title('Boxplot SPC local ' + metric)
#             else:
#                 ax.set_title('Boxplot SPC non-local ' + metric)
#             
#             ax = sns.boxplot(x="sigma", y=metric, data=temp)
#             ax.tick_params(axis='x', labelsize=12, rotation = 20)
#             
#             if local:
#                 fig.savefig('Boxplot SPC local ' + metric + '.png')
#             else:
#                 fig.savefig('Boxplot SPC non-local ' + metric + '.png')
#             plt.close(fig)
#             
# 
# =============================================================================










