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
Paths to load Netlogo data and to save plots
"""
figPath = r'C:\Users\gdawe2\OneDrive - GiGA\Mijn Documenten\Open Universiteit\Research Methods for AI\Assignment\Figuren\Compare with NetLogo'
dataPath = r'C:\Users\gdawe2\OneDrive - GiGA\Mijn Documenten\Open Universiteit\Research Methods for AI\Assignment\Output Netlogo'

"""
Load NetLogo data
"""
Vmean50        = pd.read_excel(os.path.join(dataPath,'Average Speed 50 cars.xlsx'))
Vmean100       = pd.read_excel(os.path.join(dataPath,'Average Speed 100 cars.xlsx'))
Vmean200       = pd.read_excel(os.path.join(dataPath,'Average Speed 200 cars.xlsx'))

""" 
Run Python model
"""
sim50 = nb(50,0,1)
sim50.run_model()
sim100 = nb(100,0,1)
sim100.run_model()
sim200 = nb(200,0,1)
sim200.run_model()

""" 
Plot
"""
def fig(sim50,sim100,sim200,Vmean50,Vmean100,Vmean200,savepath):
        fs = 40
        fig = plt.figure(figsize=(30,20))
        ax1 = fig.add_axes([.1,.72,.8,.25])
        ax1.plot(Vmean50['default'],label='NetLogo output')
        ax1.plot(sim50.vmean,label='Python output')
        ax1.set_title('Average Speed - 50 cars',fontsize=fs)
        ax1.tick_params(axis='x',labelsize=fs)
        ax1.tick_params(axis='y',labelsize=fs)
        ax1.set_ylabel('Average Speed',fontsize=fs)
        ax1.legend(fontsize=fs)
        ax1.grid()  
        ax1.set_ylim(0,1)
        ax1.set_xlim(0,2000)
        ax1.tick_params(axis='x', colors='w')
        
        ax2 = fig.add_axes([.1,.42,.8,.25])
        ax2.plot(Vmean100['default'],label='NetLogo output')
        ax2.plot(sim100.vmean,label='Python output')
        ax2.set_title('Average Speed - 100 cars',fontsize=fs)
        ax2.tick_params(axis='x',labelsize=fs)
        ax2.tick_params(axis='y',labelsize=fs)
        ax2.set_ylabel('Average Speed',fontsize=fs)
        ax2.grid()
        ax2.set_ylim(0,1)
        ax2.set_xlim(0,2000)
        ax2.tick_params(axis='x', colors='w')
        
        ax3 = fig.add_axes([.1,.12,.8,.25])
        ax3.plot(Vmean200['default'],label='NetLogo output')
        ax3.plot(sim200.vmean,label='Python output')
        ax3.set_title('Average Speed - 200 cars',fontsize=fs)
        ax3.tick_params(axis='x',labelsize=fs)
        ax3.tick_params(axis='y',labelsize=fs)
        ax3.set_xlabel('Iterations',fontsize=fs)
        ax3.set_ylabel('Average Speed',fontsize=fs)
        ax3.grid()   
        ax3.set_xlim(0,2000)
        ax3.set_ylim(0,1)
        
        fig.savefig(os.path.join(savepath,'Compare with NetLogo'+'.png'))
        
fig(sim50,sim100,sim200,Vmean50,Vmean100,Vmean200,figPath)
