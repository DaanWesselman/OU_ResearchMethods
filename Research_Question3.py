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
Perform simulations - vmax = 1
"""
cars = [10,20,40,60,80,100,120,150]
Ltn = [0,2,3,4,5]
outputa = pd.DataFrame(index=cars,columns=['LTN0','LTN2','LTN3','LTN4','LTN5']) 
outputb = pd.DataFrame(index=cars,columns=['LTN0','LTN2','LTN3','LTN4','LTN5']) 
for ii in np.arange(0,len(cars)):
    for jj in np.arange(0,len(Ltn)):
        print('Cars: '+str(ii+1)+' from '+str(len(cars))+' and LTN zones: '+str(jj+1)+' from '+str(len(Ltn)))
        outputa['LTN'+str(Ltn[jj])][cars[ii]],outputb['LTN'+str(Ltn[jj])][cars[ii]]= run(cars[ii],Ltn[jj],1)

outputa.to_excel('Output RQ3a.xlsx')
outputb.to_excel('Output RQ3b.xlsx')
#outputa = pd.read_excel('Output RQ3a.xlsx',index_col=0)
#outputb = pd.read_excel('Output RQ3b.xlsx',index_col=0)

"""
Perform simulations - vmax = 0.7
"""
cars = [10,20,40,60,80,100,120,150]
Ltn = [0,2,3,4,5]
outputc = pd.DataFrame(index=cars,columns=['LTN0','LTN2','LTN3','LTN4','LTN5']) 
outputd = pd.DataFrame(index=cars,columns=['LTN0','LTN2','LTN3','LTN4','LTN5']) 
for ii in np.arange(0,len(cars)):
    for jj in np.arange(0,len(Ltn)):
        print('Cars: '+str(ii+1)+' from '+str(len(cars))+' and LTN zones: '+str(jj+1)+' from '+str(len(Ltn)))
        outputc['LTN'+str(Ltn[jj])][cars[ii]],outputd['LTN'+str(Ltn[jj])][cars[ii]]= run(cars[ii],Ltn[jj],0.7)

outputc.to_excel('Output RQ3c.xlsx')
outputd.to_excel('Output RQ3d.xlsx')
# outputc = pd.read_excel('Output RQ3c.xlsx',index_col=0)
# outputd = pd.read_excel('Output RQ3d.xlsx',index_col=0)

"""
Perform simulations - vmax = 0.5
"""
cars = [10,20,40,60,80,100,120,150]
Ltn = [0,2,3,4,5]
outpute = pd.DataFrame(index=cars,columns=['LTN0','LTN2','LTN3','LTN4','LTN5']) 
outputf = pd.DataFrame(index=cars,columns=['LTN0','LTN2','LTN3','LTN4','LTN5']) 
for ii in np.arange(0,len(cars)):
    for jj in np.arange(0,len(Ltn)):
        print('Cars: '+str(ii+1)+' from '+str(len(cars))+' and LTN zones: '+str(jj+1)+' from '+str(len(Ltn)))
        outpute['LTN'+str(Ltn[jj])][cars[ii]],outputf['LTN'+str(Ltn[jj])][cars[ii]]= run(cars[ii],Ltn[jj],0.5)

outpute.to_excel('Output RQ3e.xlsx')
outputf.to_excel('Output RQ3f.xlsx')
# outpute = pd.read_excel('Output RQ3e.xlsx',index_col=0)
# outputf = pd.read_excel('Output RQ3f.xlsx',index_col=0)

"""
Reshape output for plot
"""
leavingGrid = []
braking = []
leavingGrid_rel = []
braking_rel = []
cols = ['LTN0','LTN2','LTN3','LTN4','LTN5']
for ii in np.arange(0,len(cars)):
    output1 = pd.DataFrame(index=[0.5,0.7,1],columns=cols)
    output1.iloc[0] = outpute.iloc[ii]
    output1.iloc[1] = outputc.iloc[ii]
    output1.iloc[2] = outputa.iloc[ii]
    output1b = output1.copy()
    n100 = output1['LTN0'][1]
    for jj in np.arange(0,len(cols)):
        output1b[cols[jj]] = output1[cols[jj]] / n100 *100
    leavingGrid.append(output1.copy())
    leavingGrid_rel.append(output1b.copy())
    
    output2 = pd.DataFrame(index=[0.5,0.7,1],columns=cols)
    output2.iloc[0] = outputf.iloc[ii]
    output2.iloc[1] = outputd.iloc[ii]
    output2.iloc[2] = outputb.iloc[ii]
    output2b = output2.copy()
    n100 = max(output2['LTN0'][1],0.1)
    for jj in np.arange(0,len(cols)):
        output2b[cols[jj]] = output2[cols[jj]] / n100 * 100
    braking.append(output2.copy())
    braking_rel.append(output2b.copy())

""" 
Plots
"""

def fig_perLTN(leavingGrid_rel,braking_rel,cars,savepath):
        clrs = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        colnames=['NO LTN','2x2','3x3','4x4','5x5']
        colnames_plot = [''] + colnames
        cols = braking_rel[0].columns
        ylims = ['','',400,170,140,130,130,130]
        fs = 40
        fig = plt.figure(figsize=(40,30))
        ax =[]
        ax.append(fig.add_axes([.06,.7,.44,.28]))
        ax.append(fig.add_axes([.06,.4,.44,.28]))
        ax.append(fig.add_axes([.06,.1,.44,.28]))
        ax.append(fig.add_axes([.55,.7,.44,.28]))
        ax.append(fig.add_axes([.55,.4,.44,.28]))
        ax.append(fig.add_axes([.55,.1,.44,.28]))
        
        for ii in np.arange(2,len(cars)):
            for jj in np.arange(0,len(colnames)):
                ax[ii-2].fill_between([jj+.7,jj+1],[0]*2,[leavingGrid_rel[ii][cols[jj]][1]]*2,color=clrs[0],)
                ax[ii-2].fill_between([jj+.7,jj+1],[0]*2,[leavingGrid_rel[ii][cols[jj]][0.7]]*2,color=clrs[1])
                ax[ii-2].fill_between([jj+.7,jj+1],[0]*2,[leavingGrid_rel[ii][cols[jj]][0.5]]*2,color=clrs[2])
                ax[ii-2].fill_between([jj+1,jj+1.3],[0]*2,[braking_rel[ii][cols[jj]][1]]*2,color='none',hatch='//\\',edgecolor=clrs[0])
                ax[ii-2].fill_between([jj+1,jj+1.3],[0]*2,[braking_rel[ii][cols[jj]][0.7]]*2,color='none',hatch='//\\',edgecolor=clrs[1])
                ax[ii-2].fill_between([jj+1,jj+1.3],[0]*2,[braking_rel[ii][cols[jj]][0.5]]*2,color='none',hatch='//\\',edgecolor=clrs[2]) 
            if ii == 2:
                r = .9
                u = 50
                ax[ii-2].fill_between([2.1+r,2.4+r],[290+u]*2,[310+u]*2,color=clrs[0])
                ax[ii-2].fill_between([2.1+r,2.4+r],[262+u]*2,[282+u]*2,color=clrs[1])
                ax[ii-2].fill_between([2.1+r,2.4+r],[234+u]*2,[254+u]*2,color=clrs[2])
                ax[ii-2].text(1.55+r,320+u,'Cars leaving grid',fontsize=fs)
                ax[ii-2].fill_between([3.40+r,3.70+r],[290+u]*2,[310+u]*2,color='none',hatch='//\\',edgecolor=clrs[0])
                ax[ii-2].fill_between([3.40+r,3.70+r],[262+u]*2,[282+u]*2,color='none',hatch='//\\',edgecolor=clrs[1])
                ax[ii-2].fill_between([3.40+r,3.70+r],[234+u]*2,[254+u]*2,color='none',hatch='//\\',edgecolor=clrs[2])
                ax[ii-2].text(3+r,320+u,'Cars braking',fontsize=fs)        
                ax[ii-2].text(.5+r,293+u,'Vmax = 1.0',fontsize=fs)
                ax[ii-2].text(.5+r,265+u,'Vmax = 0.7',fontsize=fs)
                ax[ii-2].text(.5+r,237+u,'Vmax = 0.5',fontsize=fs)
                ax[ii-2].plot([1.35,4.95],[280,280],color='black',linewidth=3)
                ax[ii-2].plot([1.35,4.95],[397,397],color='black',linewidth=3)
                ax[ii-2].plot([1.35,1.35],[280,397],color='black',linewidth=3)
                ax[ii-2].plot([4.95,4.95],[280,397],color='black',linewidth=3) 
                ax[ii-2].plot([3.85,3.85],[280,397],color='black',linewidth=3)
                ax[ii-2].plot([2.40,2.40],[280,397],color='black',linewidth=3)
                ax[ii-2].plot([1.35,4.95],[365,365],color='black',linewidth=3)
            ax[ii-2].tick_params(axis='x',labelsize=fs)
            ax[ii-2].tick_params(axis='y',labelsize=fs)
            if ii == 3:
                ax[ii-2].set_ylabel('Cars leaving grid (fully coloured) and braking cars (striped) - relative scale',fontsize=fs) 
            if ii in [4,7]:
                ax[ii-2].set_xlabel('LTN zone',fontsize=fs) 
            else:
                ax[ii-2].tick_params(axis='x', colors='white')
            ax[ii-2].grid()  
            ax[ii-2].set_ylim(0,ylims[ii])
            ax[ii-2].text(.6,ylims[ii]*0.93,str(cars[ii])+' cars',fontsize=fs,weight='bold')    
            ax[ii-2].set_xticklabels(colnames_plot)
        fig.savefig(os.path.join(savepath,'RQ3_relativeFig'+'.png'))
        
fig_perLTN(leavingGrid_rel,braking_rel,cars,figPath1)














