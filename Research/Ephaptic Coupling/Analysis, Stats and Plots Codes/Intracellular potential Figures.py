# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 16:14:16 2022

@author: nicol
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from sklearn.neighbors import KernelDensity

#from scipy import stats

def get_vext(folder, cell, path):
    os.chdir(path)
    try :
        os.chdir(folder + '/external_potentials/')
        vext = open("Potencial extracelular da celula basic_neuron[" + str(cell) +"].soma segmento 0.txt").read().splitlines()
        del vext[-1]
        del vext[-1]
        vext = [float(i) for i in vext]
    except:
        print(folder + '/external_potentials/ not found')
        return [], 0

    return vext

def get_v(folder, cell, path):
    os.chdir(path)
    
    try :
        #print(path + folder + '/intracelullar_potentials/')
        os.chdir(folder + '/intracelullar_potentials/')
        v = open("Potencial intracelular da celula basic_neuron[" + str(cell) +"].soma segmento 0.txt").read().splitlines()
        del v[-1]
        #del v[-1]
        v = [float(i) for i in v]
    except:
        print(folder + '/internal_potentials/ not found')
        return [], 0

    return v

def get_raster_kde(folder, path):
    raster = []
    os.chdir(path)
    
    #Raise errors for lacking or improper folders
    try :
        os.chdir(folder)
        
        # Obtain required model parameters
        params = pd.read_csv('parameters.csv', sep = ';')
        params.set_index('parameter', inplace = True)
        finish_time = int(params.loc['Simulation duration', 'value'])
        num_neurons  = int(params.loc['number of excitatory neurons', 'value'])
    except:
        print(folder + ' nao existe')
        
        return [], 0
        
    
    try:
        os.chdir(os.getcwd() + '/rasters/')
    except:
        print(folder + ' nao contem rasters')
    
    #Obtain the raster plots
    for i in range(num_neurons):
        lines = open("Raster points " +  str(i) + ".txt").read().splitlines()
        del lines[-1]
        raster.append(lines)
    
    for element in range(len(raster)):
        tmp_list = [float(i) for i in raster[element]]
        raster[element] = np.array(tmp_list)
    
    raster = [item for sublist in raster for item in sublist]
    raster = np.array(raster).reshape(-1,1)
    
    return raster, finish_time

def calculate_kde_stats(raster, finish_time):
    # Transform raster into KDE metric
    kde = KernelDensity(kernel='gaussian', bandwidth = 2)
    kde.fit(raster)
    #print(len(raster))
    
    precision_bins = finish_time
    
    x_plot = np.linspace(0, finish_time, precision_bins).reshape(-1, 1)
    log_dens = np.exp(kde.score_samples(x_plot))
    log_dens = log_dens/np.sum(log_dens)

    return log_dens


os.chdir(r'D:\Projeto CM\Versões do Modelo\V26 Testes da influencia do sigma sobre celulas')

root_path = os.getcwd()

for i in range(4):

    fig, ax = plt.subplots(1)

    v = get_v('Resultados_subversao_V' + str(i), 112, root_path)
    
    raster_kde, sim_time = get_raster_kde('Resultados_subversao_V' + str(i), root_path)
    #raster_kde = raster_kde.flatten()
    
    log_dens = calculate_kde_stats(raster_kde, sim_time)
    
    baseline = np.ones(len(v))*v[1999]
    ax.plot(np.arange(0, len(v)*0.025, 0.025), v, label = 'potencial intracelular',)
    ax.plot( np.arange(0, len(v)*0.025, 0.025), baseline, label = 'baseline')
    
    ax2 = ax.twinx()
    ax2.plot(log_dens, label = 'KDE raster', color = 'red')
    if i == 0:
        ax.set_title('Potencial intracelular tau baixo delay baixo')
    elif i == 1:
        ax.set_title('Potencial intracelular tau baixo delay alto')
    elif i == 2:
        ax.set_title('Potencial intracelular tau alto delay baixo')
    else:
        ax.set_title('Potencial intracelular tau alto delay alto')
    
    ax.legend()
    #ax2.legend()
    os.chdir(root_path)
    fig.savefig('internal potential para versao ' + str(i) + '.png', dpi = 300)
    plt.close(fig)
    


















