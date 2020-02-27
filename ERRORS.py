import numpy as np
import matplotlib.pyplot as plt
from SVV_MOI_SHEAR import steps
from SVV_MOI_SHEAR import ha
# for x = 0.5
#Sy_veri
#-48625.85466784
#Sz_veri
#247535.26084513
#T_veri
#9849.6772966
#%% MOMENT OF INERTIA error
from SVV_MOI_SHEAR import Izz
from SVV_MOI_SHEAR import Iyy
from SVV_MOI_SHEAR import zc
from SVV_MOI_SHEAR import yc
from main import Izzveri
from main import Iyyveri
from main import zcveri
from main import ycveri
MOIERROR_Iyy = abs(Izz-Izzveri)
MOIERROR_Izz = abs(Iyy-Iyyveri)
#Centroid error
YCERROR = abs(yc-ycveri)
ZCERROR = abs(zc-zcveri)
#%% redundant shear flows error
from SVV_MOI_SHEAR import Tj
from main import Tveri
ERROR_T = abs(Tj-Tveri)

#%% Shear flow errors
from SVV_MOI_SHEAR import sfr1
from main import sfveri1
from SVV_MOI_SHEAR import sfr2
from main import sfveri2
from SVV_MOI_SHEAR import sfr3
from main import sfveri3
from SVV_MOI_SHEAR import sfr4
from main import sfveri4
from SVV_MOI_SHEAR import sfr5
from main import sfveri5
from SVV_MOI_SHEAR import sfr6
from main import sfveri6
#%% 
### Region 1 
ERROR_R1 = []
SFR1_MSER = 0
SFR1_Error = [0]*len(sfr1)
figure1, axes = plt.subplots(nrows=2, ncols=3)
for i in range (0,len(sfr1)):
    SFR1_MSER += 1/(steps)*((abs(sfr1[i])-abs(sfveri1[i]))**2)  #mean squared error
    SFR1_Error[i] = abs((sfr1[i])-(sfveri1[i]))                  #errorplot
    ERROR_R1.append(SFR1_Error[i])
figure1, axes[0, 0].plot(ERROR_R1)       
#axes[0, 1].plot(sfr1) # = 1 means correct /= -1 means incorrect
#figure.tight_layout()
#plt.show()
#SFR1_locmaxr1=[sfr1.index(max(sfr1))*((np.pi*ha/2)/steps),max(sfr1)]             # location of the max & max value
#SFR1_locminr1=[sfr1.index(min(sfr1))*((np.pi*ha/2)/steps),min(sfr1)]             # Location of the min & max value

### Region 2 
ERROR_R2 = []
SFR2_MSER = 0
SFR2_Error = [0]*len(sfr2)
#figure, axes = plt.subplots(nrows=1, ncols=2)
for i in range (0,len(sfr2)):
    SFR2_MSER += 1/(steps)*((abs(sfr2[i])-abs(sfveri2[i]))**2)  #mean squared error
    SFR2_Error[i] = abs((sfr2[i])-(sfveri2[i]))                  #errorplot
    ERROR_R2.append(SFR2_Error[i])
figure1,axes[0, 1].plot(ERROR_R2)           
### Region 3 
ERROR_R3 = []
SFR3_MSER = 0
SFR3_Error = [0]*len(sfr3)
#figure, axes = plt.subplots(nrows=1, ncols=2)
for i in range (0,len(sfr3)):
    SFR3_MSER += 1/(steps)*((abs(sfr3[i])-abs(sfveri3[i]))**2)  #mean squared error
    SFR3_Error[i] = abs((sfr3[i])-(sfveri3[i]))                  #errorplot
    ERROR_R3.append(SFR3_Error[i])
figure1,axes[0, 2].plot(ERROR_R3)    
### Region 4 
ERROR_R4 = []
SFR4_MSER = 0
SFR4_Error = [0]*len(sfr4)
#figure, axes = plt.subplots(nrows=1, ncols=2)
for i in range (0,len(sfr4)):
    SFR4_MSER += 1/(steps)*((abs(sfr4[i])-abs(sfveri4[i]))**2)  #mean squared error
    SFR4_Error[i] = abs((sfr4[i])-(sfveri4[i]))                  #errorplot
    ERROR_R4.append(SFR4_Error[i])
figure1,axes[1, 0].plot(ERROR_R4)          
### Region 5 
ERROR_R5 = []
SFR5_MSER = 0
SFR5_Error = [0]*len(sfr5)
#figure, axes = plt.subplots(nrows=1, ncols=2)
for i in range (0,len(sfr5)):
    SFR5_MSER += 1/(steps)*((abs(sfr5[i])-abs(sfveri5[i]))**2)  #mean squared error
    SFR5_Error[i] = (abs(sfr5[i])-abs(sfveri5[i]))                  #errorplot
    ERROR_R5.append(SFR5_Error[i])
figure1,axes[1, 1].plot(ERROR_R5)     
### Region 6
ERROR_R6 = []
SFR6_MSER = 0
SFR6_Error = [0]*len(sfr6)
for i in range (0,len(sfr6)):
    SFR6_MSER += 1/(steps)*((abs(sfr6[i])-abs(sfveri6[i]))**2)  #mean squared error
    SFR6_Error[i] = abs((sfr6[i])-(sfveri6[i]))                  #errorplot
    ERROR_R6.append(SFR6_Error[i])
figure1,axes[1, 2].plot(ERROR_R6)         

#%% region 1 to 6 direction graphs
figure2, axes = plt.subplots(nrows=2, ncols=3)
DIRECTION_R1 = []
for i in range (0,len(sfr1)):        
    SFR1_direction = (np.sign(sfr1[i]))/(np.sign(sfveri1[i]))  
    DIRECTION_R1.append(SFR1_direction)
figure2, axes[0, 0].plot(DIRECTION_R1) 
DIRECTION_R2 = []
for i in range (0,len(sfr2)):        
    SFR2_direction = (np.sign(sfr2[i]))/(np.sign(sfveri2[i]))  
    DIRECTION_R2.append(SFR2_direction)
figure2, axes[0, 1].plot(DIRECTION_R2)
DIRECTION_R3 = []
for i in range (0,len(sfr3)):        
    SFR3_direction = (np.sign(sfr3[i]))/(np.sign(sfveri3[i]))  
    DIRECTION_R3.append(SFR3_direction)
figure2, axes[0, 2].plot(DIRECTION_R2)
DIRECTION_R4 = []
for i in range (0,len(sfr4)):        
    SFR4_direction = (np.sign(sfr4[i]))/(np.sign(sfveri4[i]))  
    DIRECTION_R4.append(SFR4_direction)
figure2, axes[1, 0].plot(DIRECTION_R2)
DIRECTION_R5 = []
for i in range (0,len(sfr5)):        
    SFR5_direction = (np.sign(sfr5[i]))/(np.sign(sfveri5[i]))  
    DIRECTION_R5.append(SFR5_direction)
figure2, axes[1, 1].plot(DIRECTION_R2)
DIRECTION_R6 = []
for i in range (0,len(sfr6)):        
    SFR6_direction = (np.sign(sfr6[i]))/(np.sign(sfveri6[i]))  
    DIRECTION_R6.append(SFR6_direction)
figure2, axes[1, 2].plot(DIRECTION_R6)