# -*- coding: utf-8 -*-
"""
Created on Sat May  6 15:19:24 2023

@author: gdawe2
"""

import numpy as np
import pandas as pd
import random

class Neighbourhood():
    def __init__(self, ncars,LTN,vmax):        
        """ Input """        
        self.ncars = ncars
        self.vmax = vmax
        self.accelaration = 0.09999
        self.LTN = LTN
        self.LTNcorners = []
        """ Make 9x9 grid """
        self.patches = self.make_patches()
        self.patches = self.patches_LTN()
        self.intersections_changedir,self.intersections_changedir2 = self.intersections_LTN()        
        """ Dynamic variables during simulation """
        self.patchesOccupied = random.sample(list(self.patches['patch']),self.ncars)
        self.cars = self.carsIni()
        self.turnback = [''] * ncars
        """ Output """        
        self.vmean = []
        self.stoppedCars = []
        self.leavingGrid = []
        self.braking = []
            
    def make_patches(self):
        """
        Makes initial grid without LTN zone
        """
        length = 37
        patches = pd.DataFrame()
        name = []
        Type = []
        x = []
        y = []         
        for ii in [3,7,11,15,19,23,27,31,36]:
            for jj in np.arange(0,length):
                name.append('p'+str(jj)+'_'+str(ii))
                x.append(jj+0.5)
                y.append(ii+0.5)
                if jj in [3,8,12,16,20,24,28,32,36]:
                    Type.append('int')
                else:
                    Type.append('lr')
        for ii in np.arange(0,length):
            for jj in [3,8,12,16,20,24,28,32,36]:
                if not ii in [3,7,11,15,19,23,27,31,36]:
                    name.append('p'+str(jj)+'_'+str(ii))
                    Type.append('ud')
                    x.append(jj+0.5)
                    y.append(ii+0.5)                                 
        patches['patch'] = name
        patches['type'] = Type  
        patches['x'] = x
        patches['y'] = y
        return patches
    
    def patches_LTN(self):
        """
        Deletes parts of the grid that is within LTN zone
        """
        LTNs = {2:[13,20,16,23],
                3:[13,24,12,23],
                4:[9,24,12,27],
                5:[9,28,8,27]}
        if self.LTN > 0:
            c = LTNs[self.LTN] 
            self.LTNcorners = c
        else:
            c = [18,18,18,18]
            self.LTNcorners = c
        indxs = []
        for ii in np.arange(0,len(self.patches)):
            if self.patches['x'][ii] > c[0] and self.patches['x'][ii] < c[1] and self.patches['y'][ii] > c[2] and self.patches['y'][ii] < c[3]:
                indxs.append(ii)
        df_temp = self.patches.drop(indxs).reset_index(drop=True)
        return df_temp         
    
    def carsIni(self):
        """
        Randomly determine initial position of cars
        """
        cars = pd.DataFrame()
        Type = [np.nan] * len(self.patchesOccupied)
        x = [np.nan] * len(self.patchesOccupied)
        y = [np.nan] * len(self.patchesOccupied)
        for ii in np.arange(0,len(self.patchesOccupied)):
            indx = list(self.patches['patch']).index(self.patchesOccupied[ii])
            Type[ii] = random.sample(['lr','ud'],1)[0] if self.patches['type'][indx] == 'int' else self.patches['type'][indx]
            if self.LTN == 2:
                if self.patchesOccupied[ii] in ['p16_15','p16_23']:
                    Type[ii] = 'lr'
                if self.patchesOccupied[ii] in ['p12_19','p20_19']:
                    Type[ii] = 'ud'
            if self.LTN == 3:
                if self.patchesOccupied[ii] in ['p16_11','p20_11','p16_23','p20_23']:
                    Type[ii] = 'lr'
                if self.patchesOccupied[ii] in ['p12_15','p12_19','p24_15','p24_19']:
                    Type[ii] = 'ud'
            if self.LTN == 4:
                if self.patchesOccupied[ii] in ['p12_11','p16_11','p20_11','p12_27','p16_27','p20_27']:
                    Type[ii] = 'lr'
                if self.patchesOccupied[ii] in ['p8_15','p8_19','p8_23','p24_15','p24_19','p24_23']:
                    Type[ii] = 'ud'
            if self.LTN == 5:
                if self.patchesOccupied[ii] in ['p12_7','p16_7','p20_7','p24_7','p12_27','p16_27','p20_27','p24_27']:
                    Type[ii] = 'lr'
                if self.patchesOccupied[ii] in ['p8_11','p8_15','p8_19','p8_23','p28_11','p28_15','p28_19','p28_23']:
                    Type[ii] = 'ud'                    
            x[ii] = self.patches['x'][indx]
            y[ii] = self.patches['y'][indx]
        cars['patch'] = self.patchesOccupied
        cars['patchIni'] = self.patchesOccupied
        cars['type'] = Type
        cars['type_LTN'] = Type
        cars['x'] = x
        cars['y'] = y
        cars['x_ini'] = x
        cars['y_ini'] = y
        cars['speed'] = 0
        cars['nextPatch'] = self.nextpatch(cars)
        return cars
    
    def intersections_LTN(self):
        """
        Determine at which intersections the cars must change direction due to LTN zone
        """
        if self.LTN == 2:
            int1 = [['p16_15'],['p12_19']]
            int2 = [['p20_15','p24_15','p28_15'],['p12_23','p12_27','p12_31']]
        if self.LTN == 3:
            int1 = [['p16_11','p20_11'],['p12_15','p12_19']]
            int2 = [['p24_11','p28_11','p32_11'],['p12_23','p12_27','p12_31']]
        if self.LTN == 4:
            int1 = [['p12_11','p16_11','p20_11'],['p8_15','p8_19','p8_23']]
            int2 = [['p24_11','p28_11','p32_11'],['p8_27','p8_31','p8_36']]
        if self.LTN == 5:
            int1 = [['p12_7','p16_7','p20_7','p24_7'],['p8_11','p8_15','p8_19','p8_23']]
            int2 = [['p28_7','p32_7','p36_7'],['p8_27','p8_31','p8_36']]
        if self.LTN == 0:
            int1 = []
            int2 = []
        return int1,int2
    
    def run_model(self,iters=1500):
        """
        Run model a number of iterations
        """
        for ii in np.arange(0,iters):
            self.move_cars()            
            self.check_LTN()
            self.cars['nextPatch'] = self.nextpatch(self.cars)
            self.vmean.append(np.mean(self.cars['speed']))
            self.stoppedCars.append(len(self.cars[self.cars['speed']==0]))               
    
    def nextpatch(self,Cars):
        """
        Every timestep: Determine the potential next patch for every car
        """
        names = []
        for ii in np.arange(0,len(Cars)):
            split = Cars['patch'][ii].split('_')
            if Cars['type'][ii] == 'lr':
                nr = int(split[0][1:])
                if nr == 36:
                    split2 = Cars['patchIni'][ii].split('_')
                    names.append('p0_'+split2[1])
                else:
                    nr += 1
                    names.append('p'+str(nr)+'_'+split[1])
            elif Cars['type'][ii] == 'ud':
                nr = int(split[1])
                if nr == 36:
                    split2 = Cars['patchIni'][ii].split('_')
                    names.append(split2[0]+'_0')
                else:
                    nr += 1
                    names.append(split[0]+'_'+str(nr))
        return names    
               
    def move_cars(self): 
        """
        Every timestep: Move cars if possible and adapt their speed
        """
        Occ_t1 = []
        speed = []
        patch = []
        x = []
        y = []
        leavinggrid = 0
        braking = 0
        for ii in np.arange(0,len(self.cars)):
           if self.cars['nextPatch'][ii] in self.patchesOccupied or self.cars['nextPatch'][ii] in Occ_t1:
               speed.append(0)
               patch.append(self.cars['patch'][ii])
               x.append(self.cars['x'][ii])
               y.append(self.cars['y'][ii])
               Occ_t1.append(patch[-1])
               if self.cars['speed'][ii] > 0:
                   braking += 1
           elif not self.cars['nextPatch'][ii] in Occ_t1:
               speed.append(min(self.cars['speed'][ii] + self.accelaration, self.vmax))
               xy = 'x' if self.cars['type'][ii] == 'lr' else 'y'
               xy_t1 = self.cars[xy][ii] + speed[-1]
               if xy_t1 > 37 :
                   leavinggrid += 1 
               xy_t1 = xy_t1 if xy_t1 < 37 else xy_t1 - 37
               patch.append(self.cars['patch'][ii] if np.floor(self.cars[xy][ii]) == np.floor(xy_t1) else self.cars['nextPatch'][ii])
               if xy == 'x':
                   x.append(xy_t1)
                   if xy_t1 < 1:
                       y.append(self.cars['y_ini'][ii])
                   else:
                       y.append(self.cars['y'][ii])
               elif xy == 'y':
                   y.append(xy_t1)
                   if xy_t1 < 1:
                       x.append(self.cars['x_ini'][ii])
                   else:
                       x.append(self.cars['x'][ii])            
               Occ_t1.append(patch[-1])         
        self.cars['speed'] = speed
        self.cars['patch'] = patch
        self.cars['x'] = x
        self.cars['y'] = y
        self.patchesOccupied = Occ_t1
        if len(self.leavingGrid) > 0:
            self.leavingGrid += [leavinggrid + self.leavingGrid[-1]]
        else:
            self.leavingGrid = [leavinggrid] 
        if len(self.braking) > 0:
            self.braking += [braking + self.braking[-1]]
        else:
            self.braking = [braking]
            
    def check_LTN(self):
        """
        Every timestep: Adapt coordinates and direction of cars when needed (due to LTN zone)
        """
        if self.LTN > 0:
            Type = self.cars['type'].copy()
            speed = self.cars['speed'].copy()
            x = self.cars['x'].copy()
            y = self.cars['y'].copy()  
            braking = 0
            for ii in np.arange(0,len(self.cars)):
                if self.cars['type'][ii] == 'ud' and self.cars['type_LTN'][ii] == 'ud' and self.cars['patch'][ii] in self.intersections_changedir[0]:
                    Type[ii] = 'lr'
                    speed[ii] = 0
                    braking += 1
                    x[ii] = np.floor(x[ii]) + 0.5
                    y[ii] = np.floor(y[ii]) + 0.5
                    self.turnback[ii] = random.sample(self.intersections_changedir2[0],1)[0]
                if self.cars['type'][ii] == 'lr' and self.cars['type_LTN'][ii] == 'lr' and self.cars['patch'][ii] in self.intersections_changedir[1]:
                    Type[ii] = 'ud'
                    speed[ii] = 0
                    braking += 1
                    x[ii] = np.floor(x[ii]) + 0.5
                    y[ii] = np.floor(y[ii]) + 0.5
                    self.turnback[ii] = random.sample(self.intersections_changedir2[1],1)[0]
            for ii in np.arange(0,len(self.cars)):
                if self.cars['type'][ii] == 'lr' and self.cars['type_LTN'][ii] == 'ud' and self.cars['patch'][ii] == self.turnback[ii]:
                    Type[ii] = 'ud'
                    speed[ii] = 0
                    braking += 1
                    x[ii] = np.floor(x[ii]) + 0.5
                    y[ii] = np.floor(y[ii]) + 0.5
                    self.turnback[ii] = ''
                if self.cars['type'][ii] == 'ud' and self.cars['type_LTN'][ii] == 'lr' and self.cars['patch'][ii] == self.turnback[ii]:
                    Type[ii] = 'lr'
                    speed[ii] = 0
                    braking += 1
                    x[ii] = np.floor(x[ii]) + 0.5
                    y[ii] = np.floor(y[ii]) + 0.5
                    self.turnback[ii] = ''            
            self.cars['type'] = Type
            self.cars['speed'] = speed
            self.cars['x'] = x
            self.cars['y'] = y
            self.braking[-1] = self.braking[-1] + braking
                
                
            
              
               
              
               
               
               
                
            
        
        
        
        
            
            
            
        
        
        
        
        
        
        
        
        
    
 
        
    
        
        
        
    