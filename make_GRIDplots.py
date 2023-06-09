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

"""
Paths to save plots
"""
figPath1 = r'C:\Users\gdawe2\OneDrive - GiGA\Mijn Documenten\Open Universiteit\Research Methods for AI\Assignment\Figuren\Movie_noLTN'
figPath2 = r'C:\Users\gdawe2\OneDrive - GiGA\Mijn Documenten\Open Universiteit\Research Methods for AI\Assignment\Figuren\Movie_LTN'

""" 
Plots for movie
"""
def fig(sim,savepath,kk):
    fig = plt.figure(figsize=(20,20))
    ax1 = fig.add_axes([.05,.05,.9,.9])
    for ii in [3,7,11,15,19,23,27,31,36]:         
        ax1.fill_between([0,37],[ii,ii],[ii+1,ii+1],color='grey') 
    for jj in [3,8,12,16,20,24,28,32,36]:
        ax1.fill_between([jj,jj+1],[0,0],[37,37],color='grey')
    ax1.fill_between([sim.LTNcorners[0],sim.LTNcorners[1]],[sim.LTNcorners[2],sim.LTNcorners[2]],[sim.LTNcorners[3],sim.LTNcorners[3]],color='green')
    ax1.scatter(sim.cars[sim.cars['type_LTN']=='ud']['x'],sim.cars[sim.cars['type_LTN']=='ud']['y'],color='blue',s=300)
    ax1.scatter(sim.cars[sim.cars['type_LTN']=='lr']['x'],sim.cars[sim.cars['type_LTN']=='lr']['y'],color='red',s=300)        
    ax1.set_xlim(0,37)
    ax1.set_ylim(0,37)
    ax1.invert_yaxis()
    ax1.axis('off')
    fig.savefig(os.path.join(savepath,'Iteration'+str(kk)+'.png'))
    
        
""" 
Run Python model and save plot every iteration
"""
sim_noLTN = nb(80,0,1)
sim_LTN = nb(80,4,1)

fig(sim_noLTN,figPath1,0)
fig(sim_LTN,figPath2,0)
for ii in np.arange(0,500):
     print('iterations '+str(ii+1)+' van '+str(500))
     sim_noLTN.run_model(1)
     sim_LTN.run_model(1)
     fig(sim_noLTN,figPath1,ii+1)
     fig(sim_LTN,figPath2,ii+1)
         
         

