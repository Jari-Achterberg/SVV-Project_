# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 22:46:44 2020

@author: Matte
"""

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np


#Find X,y,z locations of elements 
def ElementLabelLocations():

    file = open("ElementLabel.txt","r")
 
    lst =[]

    for line in file:
        #line.strip(',') 
        lst.append([float(x.strip(',')) for x in line.split()])
                    
        column1 = [ x[0] for x in lst]
        column2 = [ x[1] for x in lst]
        column3 = [ x[2] for x in lst]
        column4 = [ x[3] for x in lst]
   
    
    file.close

    ElementLabel = np.array(column1)
    xloc = np.array(column2)
    yloc = np.array(column3)
    zloc = np.array(column4)

    return xloc, yloc, zloc



#Region 1 Von Mises stress and S12

def StressLoad1Region1():
    file = open("B737L1R1Stress.txt","r")
 
    lst =[]

    for line in file:
        lst.append([float(x) for x in line.split()])
                
        column1 = [ x[0] for x in lst]
        column2 = [ x[1] for x in lst]
        column3 = [ x[2] for x in lst]
        column4 = [ x[3] for x in lst]
        column5 = [ x[4] for x in lst]
        column6 = [ x[5] for x in lst]
    
    file.close

    #print(column1)


    #Average Von Mises Stress (inside, outside?)
    array3 = np.array(column3)
    array4 = np.array(column4)
    array5 = np.array(column5)
    array6 = np.array(column6)

    #outputs
    L1R1ElementLabel = np.array(column1)
    L1R1AvVonMises = (array3 + array4)/2
    L1R1AvS12 = (array5 + array6)/2
    
    file.close
    
    return L1R1ElementLabel, L1R1AvVonMises, L1R1AvS12
    
    


#Region 2 Von Mises stress and S12

def StressLoad1Region2():
    file = open("B737L1R2Stress.txt","r")
 
    lst =[]

    for line in file:
        lst.append([float(x) for x in line.split()])
                
        column1 = [ x[0] for x in lst]
        column2 = [ x[1] for x in lst]
        column3 = [ x[2] for x in lst]
        column4 = [ x[3] for x in lst]
        column5 = [ x[4] for x in lst]
        column6 = [ x[5] for x in lst]
    
    file.close

    #print(column1)


    #Average Von Mises Stress (inside, outside?)
    array3 = np.array(column3)
    array4 = np.array(column4)
    array5 = np.array(column5)
    array6 = np.array(column6)
    
    #outputs55
    L1R2ElementLabel = np.array(column1)
    L1R2AvVonMises = (array3 + array4)/2
    L1R2AvS12 = (array5 + array6)/2
    
    file.close
    
    return L1R2ElementLabel, L1R2AvVonMises, L1R2AvS12


#----------------------------------------------------------------
#code:
L1R1ElementLabel, L1R1AvVonMises, L1R1AvS12 = StressLoad1Region1()
L1R2ElementLabel, L1R2AvVonMises, L1R2AvS12 = StressLoad1Region2()
xloc, yloc, zloc = ElementLabelLocations()



#Plot figures
fig, ax = plt.subplots()

#3D plot
#ax = plt.axes(projection='3d')
zline = zloc
xline = xloc
yline = yloc
#ax.plot3D(xline, zline, yline, 'bd')

#PLot 3D graph
ax = plt.axes(projection='3d')
ax.scatter(xline, yline, zline, cmap='viridis', edgecolor='none');


#Plot average Von Mises stress
#plt.plot(L1R1ElementLabel,L1R1AvVonMises)

#Plot average S12 stress
#plt.plot(L1R2ElementLabel,L1R2AvVonMises)

#Graph elements
ax.grid(True, zorder=5)
ax.set_xlabel("xloc")
ax.set_ylabel("yloc")

plt.show
