# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 12:46:20 2020

@author: Matte
"""

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import time


print("Start Program")
print("    ")
time_start = time.process_time()



print("Start: Definitions")
#Region 1 Von Mises stress and S12
def StressLoad2Region1():
    file = open("B737L2R1Stress.txt","r")
 
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
    L2R1ElementLabel = np.array(column1)
    L2R1AvVonMises = (array3 + array4)/2
    L2R1AvS12 = (array5 + array6)/2
    
    file.close
    
    return L2R1ElementLabel, L2R1AvVonMises, L2R1AvS12

def StressLoad2Region2():
    file = open("B737L2R2Stress.txt","r")
 
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
    L2R2ElementLabel = np.array(column1)
    L2R2AvVonMises = (array3 + array4)/2
    L2R2AvS12 = (array5 + array6)/2
    
    file.close
    
    return L2R2ElementLabel, L2R2AvVonMises, L2R2AvS12
    
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

    return ElementLabel, xloc, yloc, zloc

    

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    #Find Nodes of Elements 
def ElementNodeLink():

    file = open("ElementNodeLink.txt","r")
 
    lst =[]

    for line in file:
        #line.strip(',') 
        lst.append([float(x.strip(',')) for x in line.split()])
                    
        column1 = [ x[0] for x in lst]
        column2 = [ x[1] for x in lst]
        column3 = [ x[2] for x in lst]
        column4 = [ x[3] for x in lst]
        column5 = [ x[4] for x in lst]
   
    
    file.close

    ElementLabelLink = np.array(column1)
    node1 = np.array(column2)
    node2 = np.array(column3)
    node3 = np.array(column4)
    node4 = np.array(column5)

    return ElementLabelLink, node1, node2, node3, node4


    #Link nodes with locations
def NodeLocations():

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

    Node = np.array(column1)
    Nodexloc = np.array(column2)
    Nodeyloc = np.array(column3)
    Nodezloc = np.array(column4)

    return Node, Nodexloc, Nodeyloc, Nodezloc

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
print("    Completed: Definitions")
time_elapsed1 = (time.process_time() - time_start)
print("Computing time: ", time_elapsed1)
print("   ")
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

print("Start: Element Label Link & Node Locations Recovery")
ElementLabelLink, node1, node2, node3, node4 = ElementNodeLink()
Node, Nodexloc, Nodeyloc, Nodezloc = NodeLocations()

print("    Completed: Element Label Link & Node Locations Recovery")
time_elapsed2 = (time.process_time() - time_start)
print("Computing time: ", time_elapsed2)
print("   ")

print("Start: Field Average Calculations")
    #Find average of field
ElementLabelAvgx = []
ElementLabelAvgy = []
ElementLabelAvgz = []
ElementLabelElem = []
c = 0 
for c in range(6587):
    k = node1[c] 
    l = node2[c] 
    m = node3[c]
    n = node4[c] 

    XLocNode1 = Nodexloc[int(k-1)]
    YLocNode1 = Nodeyloc[int(k-1)]
    ZLocNode1 = Nodezloc[int(k-1)]
    
    XLocNode2 = Nodexloc[int(l-1)]
    YLocNode2 = Nodeyloc[int(l-1)]
    ZLocNode2 = Nodezloc[int(l-1)]
    
    XLocNode3 = Nodexloc[int(m-1)]
    YLocNode3 = Nodeyloc[int(m-1)]
    ZLocNode3 = Nodezloc[int(m-1)]
    
    XLocNode4 = Nodexloc[int(n-1)]
    YLocNode4 = Nodeyloc[int(n-1)]
    ZLocNode4 = Nodezloc[int(n-1)]
    
    ElementLabelElem.append(c)
    ElementLabelAvgx.append((XLocNode1 + XLocNode2 +XLocNode3 + XLocNode4)/4)
    ElementLabelAvgy.append((YLocNode1 + YLocNode2 +YLocNode3 + YLocNode4)/4)
    ElementLabelAvgz.append((ZLocNode1 + ZLocNode2 +ZLocNode3 + ZLocNode4)/4)
    
    c = c + 1
    
print("    Completed: Field Average Calculation")
time_elapsed3 = (time.process_time() - time_start)
print("Computing time: ", time_elapsed3)
print("   ")
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

print("Start: Stresses and Element location Recovery")
L2R1ElementLabel, L2R1AvVonMises, L2R1AvS12 = StressLoad2Region1()
L2R2ElementLabel, L2R2AvVonMises, L2R2AvS12 = StressLoad2Region2()
ElementLabel, xloc, yloc, zloc = ElementLabelLocations()
print("    Completed: Stresses and Element location Recovery")
time_elapsed4 = (time.process_time() - time_start)
print("Computing time: ", time_elapsed4)
print("   ")

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
print("Start: Region 1, Region 2 Merging")
L2R1ElementLabel = list(L2R1ElementLabel)
L2R1AvVonMises = list(L2R1AvVonMises)
L2R1AvS12 = list(L2R1AvS12)

L2R2ElementLabel = list(L2R2ElementLabel)
L2R2AvVonMises = list(L2R2AvVonMises)
L2R2AvS12 = list(L2R2AvS12)

L2ElementLabel = []
L2AvVonMises = []
L2AvS12 = []

c2 = 0
c3 = 0


for v in range(len(ElementLabel) -1):
    if ElementLabel[v] == L2R1ElementLabel[c2]:
        L2ElementLabel.append(L2R1ElementLabel[c2])
        L2AvVonMises.append(L2R1AvVonMises[c2])
        L2AvS12.append(L2R1AvS12[c2])
        c2 = c2 + 1
    else: # if ElementLabel[v] != L2R1ElementLabel[c3]:
        L2ElementLabel.append(L2R2ElementLabel[c3])
        L2AvVonMises.append(L2R2AvVonMises[c3])
        L2AvS12.append(L2R2AvS12[c3])
        c3 = c3 + 1 
        



print("    Completed: Region 1, Region 2 Merging")
time_elapsed5 = (time.process_time() - time_start)
print("Computing time: ", time_elapsed5)

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
print("    ")
#find Value and Element label of mx von mises stress
print("--Value and Element label of maximum Von Mises stress: --")
print("Max Von Mises Stress:", max(L2AvVonMises))
print("Position in list",np.argmax(L2AvVonMises))
print("Element Label at position", L2ElementLabel[2390])
print("Von Mises Stress at location max V.M.:",L2AvVonMises[np.argmax(L2AvVonMises)])
print("Min Von Mises Stress",min(L2AvVonMises))

print("    ")

#Find coordinates
print("--Coordinates: --")
print("Element Label at position", ElementLabelElem[2390])
print("X Location ", ElementLabelAvgx[2390])
print("Y Location ", ElementLabelAvgy[2390])
print("Z Location ", ElementLabelAvgz[2390])

print("    ")
print("    ")
print("    ")
#find Value and Element label of max S12
print("--Value and Element label of maximum S12: --")
print("Max S12:", max(L2AvS12))
print("Position in list",np.argmax(L2AvS12))
print("Element Label at position", L2ElementLabel[2389])
print("S12 at location max S12:",L2AvS12[np.argmax(L2AvS12)])
print("Min Von Mises Stress",min(L2AvS12))

print("    ")

#Find coordinates
print("--Coordinates max S12: --")
print("Element Label at position", ElementLabelElem[2390])
print("X Location ", ElementLabelAvgx[2390])
print("Y Location ", ElementLabelAvgy[2390])
print("Z Location ", ElementLabelAvgz[2390])
print("    ")

#Relative locations of maximum stresses
print("Relative locations Max Von Mises and S12")
print("max&min xloc")
print(max(Nodexloc))
print(min(Nodexloc))
print(1223.5/2661.0)
print("max&min yloc")
print(max(Nodezloc))
print(min(Nodezloc))
print((490.559204+102.5)/(102.5+502.5))
print("max&min zloc")
print(max(Nodeyloc))
print(min(Nodeyloc))
print((102.5+2.4357)/(102.5+102.5))
print("    ")


#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

        

print("Start Plotting Sequence")

        #Plot figures

fig = plt.figure()
ax = fig.gca(projection='3d')


ElementLabelAvgxRESTR = ElementLabelAvgx
ElementLabelAvgyRESTR = ElementLabelAvgy
ElementLabelAvgzRESTR = ElementLabelAvgz

# plot 3D graph using c (data)
ax.scatter(ElementLabelAvgxRESTR, ElementLabelAvgyRESTR, ElementLabelAvgzRESTR, cmap='viridis', c=L2AvS12)


#Graph elements
ax.grid(True, zorder=5)
ax.set_xlabel("x-location [mm]")
ax.set_ylabel("z-location [mm]")
ax.set_zlabel("y-location [mm]")


plt.show()
print("Completed: PLotting Sequence")
print("   ")
print("   ")
print("   ")
print("End Program")
time_elapsed = (time.process_time() - time_start)
print("Computing time: ", time_elapsed)