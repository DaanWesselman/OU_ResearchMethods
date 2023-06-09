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
Perform simulations
"""
cars = [10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200]
Ltn = [0,2,3,4,5]
outputa = pd.DataFrame(index=cars,columns=['LTN0','LTN2','LTN3','LTN4','LTN5']) 
outputb = pd.DataFrame(index=cars,columns=['LTN0','LTN2','LTN3','LTN4','LTN5']) 
for ii in np.arange(0,len(cars)):
    for jj in np.arange(0,len(Ltn)):
        print('Cars: '+str(ii+1)+' from '+str(len(cars))+' and LTN zones: '+str(jj+1)+' from '+str(len(Ltn)))
        outputa['LTN'+str(Ltn[jj])][cars[ii]],outputb['LTN'+str(Ltn[jj])][cars[ii]] = run(cars[ii],Ltn[jj],1)

outputa.to_excel('Output RQ1.xlsx')
outputb.to_excel('Output RQ1b.xlsx')
#outputa = pd.read_excel('Output RQ1.xlsx',index_col=0)
#outputb = pd.read_excel('Output RQ1b.xlsx',index_col=0)

"""
Make relative to NO-LTN situation
"""
output2 = pd.DataFrame(index=cars,columns=['LTN0','LTN2','LTN3','LTN4','LTN5']) 
output2['LTN0'] = 100
output2['LTN2'] = np.round(outputa['LTN2'] / outputa['LTN0'] * 100,1)
output2['LTN3'] = np.round(outputa['LTN3'] / outputa['LTN0'] * 100,1)
output2['LTN4'] = np.round(outputa['LTN4'] / outputa['LTN0'] * 100,1)
output2['LTN5'] = np.round(outputa['LTN5'] / outputa['LTN0'] * 100,1)

Road_Capacity = [100,98,93,85,75]

""" 
Plots
"""
def fig_percar(outputa,savepath):
        fs = 40
        fig = plt.figure(figsize=(30,13))
        ax1 = fig.add_axes([.1,.1,.8,.8])
        ax1.plot(outputa.index,outputa['LTN0'],label='No LTN')
        ax1.plot(outputa.index,outputa['LTN2'],label='2x2 LTN')
        ax1.plot(outputa.index,outputa['LTN3'],label='3x3 LTN')
        ax1.plot(outputa.index,outputa['LTN4'],label='4x4 LTN')
        ax1.plot(outputa.index,outputa['LTN5'],label='5x5 LTN') 
        ax1.plot([0,200],[14.51,14.51],color='black',linewidth=5)
        ax1.tick_params(axis='x',labelsize=fs)
        ax1.tick_params(axis='y',labelsize=fs)
        ax1.set_ylabel('Number of cars leaving grid',fontsize=fs) 
        ax1.set_xlabel('Number of cars',fontsize=fs)
        ax1.legend(fontsize=fs)
        ax1.grid()  
        ax1.set_xlim(0,200)        
        fig.savefig(os.path.join(savepath,'RQ1_notinreport'+'.png'))
        
fig_percar(outputa,figPath1)

def fig_perLTN(outputa,savepath):
        fs = 40
        fig = plt.figure(figsize=(30,13))
        ax1 = fig.add_axes([.08,.1,.9,.68])
        for ii in np.arange(0,len(outputa)):
            if outputa.index[ii] in [10,20,40,60,80,100,120,150]:
                ax1.plot(['NO LTN','2x2','3x3','4x4','5x5'],outputa.iloc[ii],label=str(outputa.index[ii])+' cars',linestyle='--',linewidth=3,marker='o',markersize=30) 
        ax1.plot(['NO LTN','2x2','3x3','4x4','5x5'],[14.51]*5,color='black',linewidth=5,label='Theoretical Maximum')
        ax1.tick_params(axis='x',labelsize=fs)
        ax1.tick_params(axis='y',labelsize=fs)
        ax1.set_ylabel('Number of cars leaving grid',fontsize=fs) 
        ax1.set_xlabel('LTN zone',fontsize=fs)
        handles, labels = ax1.get_legend_handles_labels()
        def flip(items, ncols):
            return itertools.chain(*[items[i::ncols] for i in range(ncols)])
        ax1.legend(flip(handles,4),flip(labels, 4),ncol=4,loc='upper center', bbox_to_anchor=(.5,1.35),fontsize=fs)
        ax1.grid()  
        ax1.set_ylim(0,15)
        ax1.text('NO LTN',.5,'Number of cars leaving grid',fontsize=fs,weight='bold')        
        fig.savefig(os.path.join(savepath,'RQ1_absoluteFig'+'.png'))
        
fig_perLTN(outputa,figPath1)

def fig_perLTN2(output2,Road_Capacity,savepath):
        fs = 40
        fig = plt.figure(figsize=(30,13))
        ax1 = fig.add_axes([.08,.1,.9,.68])
        for ii in np.arange(0,len(output2)):
            if output2.index[ii] in [10,20,40,60,80,100,120,150]:
                ax1.plot(['NO LTN','2x2','3x3','4x4','5x5'],output2.iloc[ii],label=str(output2.index[ii])+' cars',linestyle='--',linewidth=3,marker='o',markersize=30)
        ax1.plot(['NO LTN','2x2','3x3','4x4','5x5'],Road_Capacity,color=[.2,.2,.2],label='Road Capacity',linestyle='--',linewidth=5,marker='*',markersize=50)
        ax1.tick_params(axis='x',labelsize=fs)
        ax1.tick_params(axis='y',labelsize=fs)
        ax1.set_ylabel('Relative number of cars leaving grid [%]',fontsize=fs) 
        ax1.set_xlabel('LTN zone',fontsize=fs)
        handles, labels = ax1.get_legend_handles_labels()
        def flip(items, ncols):
            return itertools.chain(*[items[i::ncols] for i in range(ncols)])
        ax1.legend(flip(handles,4),flip(labels, 4),ncol=4,loc='upper center', bbox_to_anchor=(.5,1.35),fontsize=fs)
        ax1.grid()  
        ax1.set_ylim(50,102)  
        ax1.text('NO LTN',58,'Relative number of cars leaving grid',fontsize=fs,weight='bold') 
        ax1.text('NO LTN',53,'Compared with road capacity',fontsize=fs,weight='bold') 
        fig.savefig(os.path.join(savepath,'RQ1_relativeFig'+'.png'))
        
fig_perLTN2(output2,Road_Capacity,figPath1)

def fig_braking(outputb,savepath):
        fs = 40
        fig = plt.figure(figsize=(30,13))
        ax1 = fig.add_axes([.08,.1,.9,.68])
        for ii in np.arange(0,len(outputb)):
            if outputb.index[ii] in [10,20,40,60,80,100,120,150]:
                ax1.plot(['NO LTN','2x2','3x3','4x4','5x5'],outputb.iloc[ii],label=str(outputb.index[ii])+' cars',linestyle='--',linewidth=3,marker='o',markersize=30)
        ax1.tick_params(axis='x',labelsize=fs)
        ax1.tick_params(axis='y',labelsize=fs)
        ax1.set_ylabel('Braking cars',fontsize=fs) 
        ax1.set_xlabel('LTN zone',fontsize=fs)
        handles, labels = ax1.get_legend_handles_labels()
        def flip(items, ncols):
            return itertools.chain(*[items[i::ncols] for i in range(ncols)])
        ax1.legend(flip(handles,4),flip(labels, 4),ncol=4,loc='upper center', bbox_to_anchor=(.5,1.35),fontsize=fs)
        ax1.grid()  
        #ax1.set_ylim(50,102)  
        ax1.text('3x3',13,'Average number of times that cars brake',fontsize=fs,weight='bold') 
        ax1.text('3x3',1,'Vmax = 1',fontsize=fs,weight='bold') 
        fig.savefig(os.path.join(savepath,'RQ1_braking'+'.png'))
        
fig_braking(outputb,figPath1)

