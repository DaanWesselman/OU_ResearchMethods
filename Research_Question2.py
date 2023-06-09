# -*- coding: utf-8 -*-
"""
Created on Sat May  6 15:50:25 2023

@author: Daan Wesselman
"""

from neighbourhood_LTN import Neighbourhood as nb
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import itertools

"""
Path to save plot
"""
figPath1 = r'C:\Users\gdawe2\OneDrive - GiGA\Mijn Documenten\Open Universiteit\Research Methods for AI\Assignment\Figuren\Research Questions'

"""
Function to perform simulations
""" 
def run(ncar,ltn,vmax,numberSim=20):
    count = []
    count2 = []
    for ii in np.arange(0,numberSim):
        sim = nb(ncar,ltn,vmax)
        sim.run_model()
        count.append(sim.leavingGrid[1499] - sim.leavingGrid[999])
        count2.append(sim.braking[1499] - sim.braking[999])
    result1 = np.round(np.mean(count) / ncar,2)
    result2 = np.round(np.mean(count2) / ncar,2)
    return result1,result2
        
"""
Perform simulations - full traffic evaporation
"""
Road_Capacity = [100,98,93,85,75]
cars1 = [10,20,40,60,80,100,120,150]
cars2 = list(np.round(np.array(cars1)*Road_Capacity[1]/100))
cars3 = list(np.round(np.array(cars1)*Road_Capacity[2]/100))
cars4 = list(np.round(np.array(cars1)*Road_Capacity[3]/100))
cars5 = list(np.round(np.array(cars1)*Road_Capacity[4]/100))
cars = np.array([cars1,cars2,cars3,cars4,cars5])

Ltn = [0,2,3,4,5]
outputa = pd.DataFrame(index=cars1,columns=['LTN0','LTN2','LTN3','LTN4','LTN5']) 
outputb = pd.DataFrame(index=cars1,columns=['LTN0','LTN2','LTN3','LTN4','LTN5']) 
for ii in np.arange(0,len(cars1)):
    for jj in np.arange(0,len(Ltn)):
        print('Cars: '+str(ii+1)+' from '+str(len(cars1))+' and LTN zones: '+str(jj+1)+' from '+str(len(Ltn)))
        outputa['LTN'+str(Ltn[jj])][cars1[ii]],outputb['LTN'+str(Ltn[jj])][cars1[ii]] = run(int(cars[jj,ii]),Ltn[jj],1)

outputa.to_excel('Output RQ2a.xlsx')
#outputa = pd.read_excel('Output RQ2a.xlsx',index_col=0)

"""
Make relative to NO-LTN situation
"""
output2 = pd.DataFrame(index=cars1,columns=['LTN0','LTN2','LTN3','LTN4','LTN5']) 
output2['LTN0'] = 100
output2['LTN2'] = np.round(outputa['LTN2'] / outputa['LTN0'] * 100,1)
output2['LTN3'] = np.round(outputa['LTN3'] / outputa['LTN0'] * 100,1)
output2['LTN4'] = np.round(outputa['LTN4'] / outputa['LTN0'] * 100,1)
output2['LTN5'] = np.round(outputa['LTN5'] / outputa['LTN0'] * 100,1)     

def fig_perLTN2(output2,Road_Capacity,cars,savepath):
        fs = 40
        fig = plt.figure(figsize=(30,13))
        ax1 = fig.add_axes([.08,.1,.9,.68])
        for ii in np.arange(0,len(output2)):
            if output2.index[ii] in [10,20,40,60,80,100,120,150]:
                lbl = str(int(cars[0][ii]))+'/'+str(int(cars[1][ii]))+'/'+str(int(cars[2][ii]))+'/'+str(int(cars[3][ii]))+'/'+str(int(cars[4][ii]))+' cars'
                ax1.plot(['NO LTN','2x2','3x3','4x4','5x5'],output2.iloc[ii],label=lbl,linestyle='--',linewidth=3,marker='o',markersize=30)
        ax1.plot(['NO LTN','2x2','3x3','4x4','5x5'],Road_Capacity,color=[.2,.2,.2],label='Road Capacity',linestyle='--',linewidth=5,marker='*',markersize=50)
        ax1.tick_params(axis='x',labelsize=fs)
        ax1.tick_params(axis='y',labelsize=fs)
        ax1.set_ylabel('Relative number of cars leaving grid [%]',fontsize=fs) 
        ax1.set_xlabel('LTN zone',fontsize=fs)
        handles, labels = ax1.get_legend_handles_labels()
        def flip(items, ncols):
            return itertools.chain(*[items[i::ncols] for i in range(ncols)])
        ax1.legend(flip(handles,3),flip(labels, 3),ncol=3,loc='upper center', bbox_to_anchor=(.5,1.35),fontsize=fs)
        ax1.grid()  
        ax1.set_ylim(50,102)  
        ax1.text('NO LTN',63,'Relative number of cars leaving grid',fontsize=fs,weight='bold') 
        ax1.text('NO LTN',58,'Compared with road capacity',fontsize=fs,weight='bold')
        ax1.text('NO LTN',53,'Car density remains equal due to traffic evaporation',fontsize=fs,weight='bold')
        fig.savefig(os.path.join(savepath,'RQ2_relativeFig'+'.png'))
        
fig_perLTN2(output2,Road_Capacity,cars,figPath1)





