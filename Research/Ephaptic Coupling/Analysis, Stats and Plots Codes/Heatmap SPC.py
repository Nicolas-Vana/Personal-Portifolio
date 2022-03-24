# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 22:54:20 2021

@author: nicol
"""

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

os.chdir(r'D:\Projeto CM\Versões do Modelo\V25 correcao em como o ge é calculado')


df = pd.read_csv('SPC heat map dataframe passband 30-50.csv', sep = ';') ### Modificada
df['x_pos'] = df['cell']%15
df['y_pos'] = df['cell']//15

heatmap_stats = []

os.chdir(r'D:\Projeto CM\Versões do Modelo\V25 correcao em como o ge é calculado\Heatmaps')

for seed in df['seed'].unique().tolist():
    for sigma in df['sigma'].unique().tolist():
        for perturbation in df['ge-xraxial ratio'].unique().tolist():
            for local in [True, False, 'exclude center']:
                print(seed, sigma, perturbation, local)
            
                df1 = df[(df['sigma'] == sigma) & (df['seed'] == seed) & (df['ge-xraxial ratio'] == perturbation) & (df['local'] == str(local))].copy()
                #df2 = df[(df['sigma'] == sigma) & (df['seed'] == seed) & (df['ge-xraxial ratio'] == sigma)].copy()
                
                df1.drop(['seed', 'ge-xraxial ratio', 'cell', 'sigma'], axis = 1, inplace = True)
                #df2.drop(['seed', 'ge-xraxial ratio', 'cell', 'sigma'], axis = 1, inplace = True)
                
                abs_heat_1 = df1.pivot('x_pos', 'y_pos', 'mean vec absolute value')
                angle_heat_1 = df1.pivot('x_pos', 'y_pos', 'mean vec absolute angle')
                
                for i in [0, 14]:
                    abs_heat_1.drop(i, inplace = True)
                    #abs_heat_2.drop(i, inplace = True)
                    angle_heat_1.drop(i, inplace = True)
                    #angle_heat_2.drop(i, inplace = True)
                    
                    abs_heat_1.drop(columns = i, inplace = True)
                    #abs_heat_2.drop(columns = i, inplace = True)
                    angle_heat_1.drop(columns = i, inplace = True)
                    #angle_heat_2.drop(columns = i, inplace = True)
                    
                fig, ax = plt.subplots(1,2)
                fig.set_figheight(10)
                fig.set_figwidth(17.5)
                
                ax[0].set_title('absolute value sigma = ' + str(sigma))
                sns.heatmap(abs_heat_1, ax=ax[0])
                
                ax[1].set_title('angle value sigma = ' + str(sigma))
                sns.heatmap(angle_heat_1, ax=ax[1])
                
                fig.savefig('Heat map SPC sigma = ' + str(sigma) + ' seed = ' + str(seed) + ' perturbation = ' + str(perturbation)+ ' local = ' + str(local) + 'filt freq 50.png', dpi = 300) ### Modificada
                plt.close(fig)
                
                # Get Stats from the Heatmap values
                
                tmp_abs = abs_heat_1.to_numpy()
                tmp_angle = angle_heat_1.to_numpy()
                
                mean_abs = np.mean(tmp_abs)
                std_abs = np.std(tmp_abs)
                
                mean_angle = np.mean(tmp_angle)
                std_angle = np.std(tmp_angle)
                
                heatmap_stats.append([seed, sigma, perturbation, local, mean_abs, std_abs, mean_angle, std_angle])
            
os.chdir(r'D:\Projeto CM\Versões do Modelo\V25 correcao em como o ge é calculado')
df_stats = pd.DataFrame(heatmap_stats, columns = ['seed', 'sigma', 'perturbation', 'local', 'mean_abs', 'std_abs', 'mean_angle', 'std_angle'])
df_stats.to_csv('Heatmap Stats dataframe passband 30-50.csv', sep = ';', index = False) ### Modificada


# Boxplots related to the heatmaps

os.chdir(r'D:\Projeto CM\Versões do Modelo\V25 correcao em como o ge é calculado\Boxplots\Heatmap')

for local in [True, False, 'exclude center']:
    for perturbation in df['ge-xraxial ratio'].unique().tolist():
        
        df1 = df[(df['ge-xraxial ratio'] == perturbation) & (df['local'] == str(local))].copy()
        df1.reset_index(inplace = True, drop = True)
        df1.drop(columns = ['ge-xraxial ratio', 'local', 'cell'], inplace = True)
        df1 = df1.groupby(['seed', 'sigma']).mean()
        df1.reset_index(inplace = True)
        
        df1.drop(df1.index[df1['x_pos'] == 0], inplace = True)
        df1.drop(df1.index[df1['x_pos'] == 14], inplace = True)
        df1.drop(df1.index[df1['y_pos'] == 0], inplace = True)
        df1.drop(df1.index[df1['y_pos'] == 14], inplace = True)
        #df1.drop(np.where(df1['y_pos'] == [0,14]), inplace = True)
        
        fig, ax = plt.subplots(1, 2)
        fig.set_figheight(5)
        fig.set_figwidth(15)
        
        sns.boxplot(x="sigma", y='mean vec absolute value', data=df1, ax = ax[0])
        sns.stripplot(x="sigma", y='mean vec absolute value', data=df1, ax = ax[0])
        
        sns.boxplot(x="sigma", y='mean vec absolute angle', data=df1, ax = ax[1])
        sns.stripplot(x="sigma", y='mean vec absolute angle', data=df1, ax = ax[1])
        ax[0].tick_params(axis='x', labelsize=12, rotation = 20)
        ax[1].tick_params(axis='x', labelsize=12, rotation = 20)
        ax[0].set_title('Mean Vec Absolute Value Boxplot')
        ax[1].set_title('Mean Vec Angle Boxplot')
        
        fig.savefig('Heat map SPC local = ' + str(local) + ' perturbation = ' + str(perturbation) + ' filt freq 30-50.png', dpi = 300) ### Modificada
        plt.close(fig)
        
        



            
            
            
            
'''df.drop(['seed', 'ge-xraxial ratio', 'cell'], axis = 1, inplace = True)

df1 = df[df['sigma'] == 0.00625].copy()
df2 = df[df['sigma'] == 0.8].copy()

df1.drop(['sigma'], axis = 1, inplace = True)
df2.drop(['sigma'], axis = 1, inplace = True)

# Heatmaps

abs_heat_1 = df1.pivot('x_pos', 'y_pos', 'mean vec absolute value')
abs_heat_2 = df2.pivot('x_pos', 'y_pos', 'mean vec absolute value')

angle_heat_1 = df1.pivot('x_pos', 'y_pos', 'mean vec absolute angle')
angle_heat_2 = df2.pivot('x_pos', 'y_pos', 'mean vec absolute angle')

for i in [0, 14]:
    abs_heat_1.drop(i, inplace = True)
    abs_heat_2.drop(i, inplace = True)
    angle_heat_1.drop(i, inplace = True)
    angle_heat_2.drop(i, inplace = True)
    
    abs_heat_1.drop(columns = i, inplace = True)
    abs_heat_2.drop(columns = i, inplace = True)
    angle_heat_1.drop(columns = i, inplace = True)
    angle_heat_2.drop(columns = i, inplace = True)

fig, ax = plt.subplots(2,2)
fig.set_figheight(10)
fig.set_figwidth(15)

ax[0,0].set_title('absolute value sigma = 0.00625')
sns.heatmap(abs_heat_1, ax=ax[0,0])

ax[0,1].set_title('absolute value sigma = 0.8')
sns.heatmap(abs_heat_2, ax=ax[0,1])

ax[1,0].set_title('angle value sigma = 0.00625')
sns.heatmap(angle_heat_1, ax=ax[1,0])

ax[1,1].set_title('angle value sigma = 0.8')
sns.heatmap(angle_heat_2, ax=ax[1,1])

fig.savefig('Heat map SPC.png', dpi = 300)'''





