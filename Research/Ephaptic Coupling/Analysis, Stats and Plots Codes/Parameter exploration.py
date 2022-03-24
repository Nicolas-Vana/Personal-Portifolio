# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 17:42:27 2021

@author: nicol
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import os
import time

def run_model(params, ephaptic_type, extracell, ephaptic_switch):
    #print(params)
    
    f = open("Parameter_input.txt", 'w+')
    f.write(str(params['conductance']) + '\n' + str(params['extracell_correction_xg']) + '\n' + str(params['seed']) + '\n' + str(params['ephaptic_switch']) + '\n' + str(params['ge_correction']))
    f.close()
    
    f = open("Parameter_input_LFPsim.txt", 'w+')
    f.write(str(params['conductance']))
    f.close()
    
    f = open('foldernames.txt', 'w+')
    global foldername_list
    for foldernames in foldername_list:
        f.write(foldernames + '\n')
    f.close()
    
    #p = subprocess.Popen('init.hoc', shell = True)
    #p.wait()
    os.startfile('init.hoc')
    
    f = open('Current Run.txt', 'w+')
    time.sleep(10)
    while f.read() == '1':
        f.seek(0)
        #print(f.read())
        #f.seek(0)
        time.sleep(2)
    
    global version_counter 
    #print('rename ' + '"' + 'Resultados_subversao_V' + str(version_counter) +  '"' + ' "' + 'Resultados_' + sync_type + '_' + ephaptic_type + '_' + extracell + '_' + str(params['seed']) + '"')
    #os.system('rename ' + '"' + 'Resultados_subversao_V' + str(version_counter) +  '"' + ' "' + 'Resultados_no_extracell_' + sync_type + '_' + ephaptic_type + '_' + extracell + '_' + str(params['seed']) + '"')
    os.system('rename ' + '"' + 'Resultados_subversao_V' + str(version_counter) +  '"' + ' "' + foldername + '"')
    
    #print('xcopy "D:\Projeto CM\Versões do Modelo\V15 variação extracel\LFP_traces" ' + '"D:\Projeto CM\Versões do Modelo\V15 variação extracel' + '\Resultados_' + sync_type + '_' + ephaptic_type + '_' + extracell + '_' + str(params['seed']) + '"')
    #os.system('xcopy "D:\Projeto CM\Versões do Modelo\V15 variação extracel\LFP_traces" ' + '"D:\Projeto CM\Versões do Modelo\V15 variação extracel' + '\Resultados_no_extracell_' + sync_type + '_' + ephaptic_type + '_' + extracell + '_' + str(params['seed']) + '"')
    os.system('xcopy "D:\Projeto CM\Versões do Modelo\V25 correcao em como o ge é calculado\LFP_traces" ' + '"D:\Projeto CM\Versões do Modelo\V25 correcao em como o ge é calculado\\' + foldername + '"')
    os.system('xcopy "D:\Projeto CM\Versões do Modelo\V25 correcao em como o ge é calculado\Parameter_input_LFPsim.txt" ' + '"D:\Projeto CM\Versões do Modelo\V25 correcao em como o ge é calculado\\' + foldername + '"')
    
    
    version_counter += 1
    
    
def set_params(ephaptic, extracell, seed, ephaptic_switch):
    
    #ephaptic params
    parameters['conductance'] = ephaptic
    parameters['extracell_correction_xg'] = 1
        
    #extracel params
    parameters['extracell_correction_ephaptic'] = 1
    
        
    if ephaptic_switch == 'Yes_Ephaptic':
        parameters['ephaptic_switch'] = 1
    else:
        parameters['ephaptic_switch'] = 0
        
    parameters['seed'] = seed
    parameters['ge_correction'] = extracell

def define_params(ephaptic, perturbation):
    
    #base_value = (0.7/ephaptic)**3*0.01
    base_value = 1
    extracell =  perturbation*base_value

    extracell = str(f"{extracell:.8f}")
    ephaptic = str(f"{ephaptic:.8f}")
    
    return ephaptic[:8], str(extracell)

os.chdir(r'D:\Projeto CM\Versões do Modelo\V25 correcao em como o ge é calculado')
path = os.getcwd()

np.set_printoptions(suppress=True)
sync_types = ['Mid_Sync']#['Low_Sync', 'Mid_Sync', 'High_Sync']#
ephaptic_types =  [0.00625, 0.0125, 0.025, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 100, 250, 500, 1000, 2500, 5000, 10000, 100000000]#[0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1]#[0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]#[0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
perturbations = [0.25]#[0.125, 0.25, 0.5, 0.75, 1, 1.5, 2, 4, 16]#[0.0625, 0.125, 0.25, 0.33, 0.5, 0.75, 1, 1.5, 2, 3, 4, 8, 16]#[0.25, 0.33, 0.5, 0.75, 1, 1.5, 2, 3, 4]
#extracell_types = ['Low_Potential', 'Mid_Potential', 'High_Potential']#['Mid_Potential']#
ephaptic_switchs = ['Yes_Ephaptic']#['Yes_Ephaptic', 'No_Ephaptic']#['No_Ephaptic']#

parameters = {'conductance': 0, 'external weight': 0.003, 'excit weight': 0.001, 'seed': 1, 'extracell_correction_ephaptic': 1, 'extracell_correction_xg': 2, 'ephaptic_switch': 1, 'ge_correction': 1}

version_counter_file = open('Version counter.txt', 'r')
version_counter = int(version_counter_file.read())
version_counter_file.close()

foldername_list = []
f = open('foldernames.txt', 'a')

for seed in range(1,11):            
    for perturbation in perturbations:
            for ephaptic in ephaptic_types:
                ephaptic, extracell = define_params(ephaptic, perturbation)
                for ephaptic_switch in ephaptic_switchs:
                        
    
                            
                        #if extracell == 'No_Extracell':
                        #    foldername = 'Resultados_' + sync + '_' + ephaptic + '_' + extracell + '_' + str(seed) #'Resultados_no_extracell_' + sync_type + '_' + ephaptic_type + '_' + extracell + '_' + str(params['seed'])
                        if float(ephaptic) > 10000:
                            foldername = 'Resultados_No_Potential_' + str(seed)
                        else:
                            foldername = 'Resultados_' + ephaptic + '_' + extracell + '_' + str(seed)
                        
# =============================================================================
#                         if ephaptic == 'No_Potential':
#                             foldername = 'Resultados_No_Potential_' + '_' + str(seed)
#                         else:
#                             if ephaptic_switch == 'No_Ephaptic':
#                                 foldername = 'Resultados_baseline_' + '_' + ephaptic + '_' + extracell + '_' + str(seed)
#                             else:
#                                 foldername = 'Resultados_' + ephaptic + '_' + extracell + '_' + str(seed)
# =============================================================================
                        
                        
                        
                        try:
                            os.chdir(path)
                            #print(foldername)
                            os.chdir(foldername)
                            #print(os.getcwd())
                            os.chdir(path)
                        except:
                            print(foldername)
                            foldername_list.append(foldername)
                            set_params(ephaptic, extracell, seed, ephaptic_switch)
                            f.write(foldername + '\n')
                            run_model(parameters, ephaptic, extracell, ephaptic_switch)
                            os.chdir(path)
                    

f = open('foldernames.txt', 'w+')

for foldername in foldername_list:
    f.write(foldername + '\n')
    print(foldername)

















