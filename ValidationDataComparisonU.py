# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 12:47:38 2020

@author: Matte
"""

import matplotlib.pyplot as plt
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



    #Load case 1 U values
def UMagnitude():
    file = open("B737L2U.txt","r")
    lst =[]
    for line in file:
        lst.append([float(x) for x in line.split()])          
        column1 = [ x[0] for x in lst]
        column2 = [ x[1] for x in lst]
        column3 = [ x[2] for x in lst]
        column4 = [ x[3] for x in lst]
        column5 = [ x[4] for x in lst]
    
    file.close
    #Values U
    arrayUmag = np.array(column2)
    arrayU1 = np.array(column3)
    arrayU2 = np.array(column4)
    arrayU3 = np.array(column5)
    arrayNodeLabel = np.array(column1)  
    
    
    return arrayNodeLabel, arrayUmag, arrayU1, arrayU2, arrayU3
    
#---------------------------------------------------------------        

    #code:
arrayNodeLabel, arrayUmag, arrayU1, arrayU2, arrayU3 = UMagnitude()
xloc, yloc, zloc = ElementLabelLocations()

    #separating z == 0
xlocnew = []
ylocnew =[]
zlocnew =[]
arrayU2new = []
arrayU1new = []
arrayU3new = []
n = 0


for n in range(0,6587):
    n = n+1
    if zloc[n] == 0:
        if yloc[n] == 0:
            xlocnew.append(xloc[n])
            ylocnew.append(yloc[n])
            zlocnew.append(zloc[n])
            arrayU2new.append(arrayU2[n])
            arrayU1new.append(arrayU1[n])
            arrayU3new.append(arrayU3[n])

#print(arrayU3new)


    #Plot figures
fig, ax = plt.subplots()


    #PLot Umag 
#ax.scatter(xlocnew, arrayU2new, s=2, color='r')
#ax.set_xlabel("X coordinates [mm]")
#ax.set_ylabel("Displacement in y [mm]")
    
ax.scatter(xlocnew, arrayU2new, s=2, color='b')
ax.set_xlabel("X coordinates [mm]")
ax.set_ylabel("Displacement in y [mm]")
    

    #Graph elements
ax.grid(True, zorder=5)


plt.show