import matplotlib.pyplot as plt
import numpy as np
#INPUTS
Ca = 0.484  # m
la = 1.691  # m
x1 = 0.149  # m
x2 = 0.554  # m
x3 = 1.541  # m
xa = 27.2/100   # m
ha = 17.3/100  # m
tsk = 1.1/1000  # m
tsp = 2.5/1000  # m
tst = 1.2/1000  # m
hst = 14./1000   # m
wst = 18./1000   # m
nst = 13  # AMOUNT
G = 28*(10**9)
#Useful parameters for later
diagbar = np.sqrt((ha/2)**2 + (Ca - ha/2)**2) #length of one of the diagional parts to the right of the spar (starting at top of airfoil going to trailing edge)
lengthsk = np.pi * ha/2 + 2 * diagbar         #Total length of skin
space = lengthsk / nst                        #Spacing between stringer with regard to skinlength
cenarc = ha/2-(2*(ha/2)/(np.pi))                 #Centroid of the half arc
Areastringer = tst *(hst + wst)               #Area of stringer
AREAcs = (1/2)*np.pi*(ha/2)**2+(ha/2)*(Ca-ha/2) #Area of the cross section (NOT ONLY SKIN/STRINGERS)
angle = np.arctan((Ca - ha/2)/(ha/2))         #Top left angle of the triangular part of the airfoil section 
arcspace = np.pi* ha / 4 - space              #Skin length of the arc that remains after the first stringer
barspace= space - arcspace                    #Skin length that determines first location of stringer on diagonal bar
hz = ha/2
hy = 0.0
hingecoordinate = [hz,hy]
#%%
#Coordiante system for the creation of geometric map and eventual MOI calculation 
#Entire system is rotated to make symmetry axis equal to z-axis
#Coordinate system has (0,0) coordinate at the leading edge of the airfoil (postive z-direction is towards trailing edge/ positive y-direction is towards top of airfoil)
#Stringers locations start at Leading edge and move to trailing edge throught the top part first and then return to leading edge through bottom part
stringerz = np.zeros([nst])
stringery = np.zeros([nst])
stringerz[0] = 0.0
stringery[0] = 0.0
stringerz[1] = np.cos(2*space/ ha) * (ha/2)
stringery[1] = np.sin (2*space / ha) * (ha/2)
stringerz[2] = ha/2 + np.sin(angle)*(barspace)
stringery[2] = ha/2 - np.cos(angle)*(barspace)
stringerz[3] = ha/2 + np.sin(angle)*(barspace+ space)
stringery[3] = ha/2 - np.cos(angle)*(barspace+ space)
stringerz[4] = ha/2 + np.sin(angle)*(barspace+ 2*space)
stringery[4] = ha/2 - np.cos(angle)*(barspace+ 2*space)
stringerz[5] = ha/2 + np.sin(angle)*(barspace+ 3*space)
stringery[5] = ha/2 - np.cos(angle)*(barspace+ 3*space)
stringerz[6] = ha/2 + np.sin(angle)*(barspace+ 4*space)
stringery[6] = ha/2 - np.cos(angle)*(barspace+ 4*space)
# From this point the y coordinates becomes negative as they are under the symmetry axis
stringerz[7] = ha/2 + np.sin(angle)*(barspace+ 4*space)
stringery[7] = -(ha/2 - np.cos(angle)*(barspace+ 4*space))
stringerz[8] = ha/2 + np.sin(angle)*(barspace+ 3*space)
stringery[8] = -(ha/2 - np.cos(angle)*(barspace+ 3*space))
stringerz[9] = ha/2 + np.sin(angle)*(barspace+ 2*space)
stringery[9] = -(ha/2 - np.cos(angle)*(barspace+ 2*space))
stringerz[10] = ha/2 + np.sin(angle)*(barspace+ space)
stringery[10] = -(ha/2 - np.cos(angle)*(barspace+ space))
stringerz[11] = ha/2 + np.sin(angle)* barspace
stringery[11] = -(ha/2 - np.cos(angle)* barspace)
stringerz[12] = np.cos(2*space/ha)*(ha/2)
stringery[12] = -np.sin(2*space/ha)*(ha/2)
#%%
# CENTROID CALCULATION
# Centroid-y due to symmetry on symmetry axis 
yc = 0.0
# Centroid-z calculation in order: spar, arc, daigonal bar, stringers
zc = ((ha * tsp * ha/2) + (np.pi * ha/2 * tsk) * (cenarc) + (2* diagbar * tsk * (ha/2+(Ca - ha/2)/2)) + (Areastringer * sum(stringerz[:])))  / (nst* Areastringer + ha* tsp + 2*diagbar* tsk+np.pi * ha/2 * tsk)                
centroidzy = [zc , yc]
#%% MOI CALCULATION
# MOI of the spar
Izz_spar = (tsp*(ha**3))/12            #No Steiner term 
Iyy_spar =  tsp*ha*((zc-ha/2)**2)      #Steiner term only - thin walled assumption
# MOI of the arc
Izz_skin_arc = np.pi * (ha/2)**3 * tsk / 2                                          #No Steiner term 
Iyy_skin_arc = Izz_skin_arc + np.pi * ha/2 * tsk * ((zc-(cenarc))**2)               #Steiner term included 
# MOI of the diagonal barsI
Izz_skin_diagbar = (tsk * (2*diagbar)**3 * ((ha/2)/diagbar)**2) / 12                                                #No Steiner term 
Iyy_skin_diagbar = 2*(tsk * (diagbar)**3 * ((Ca-ha/2)/diagbar)**2) / 12 + 2 *(diagbar * tsk)*(((Ca-ha/2)/2-zc)**2)  #Steiner term included 
# MOI of the stringers
Izz_stringer = Areastringer * sum((stringery[:])**2)            #Only Steiner term of stringers
Iyy_stringer = Areastringer * sum((stringerz[:]-zc)**2)         #Only Steiner term of stringers
# TOTAL MOI
Izz = Izz_stringer + Izz_skin_diagbar + Izz_spar + Izz_skin_arc 
Iyy = Iyy_stringer + Iyy_skin_diagbar + Iyy_spar + Iyy_skin_arc

#%%
##veri data
#z coordinate -0.19406263838748938
#5.81593895759915e-06 Izz
#4.363276766019503e-05 Iyy
#assumption: thin walled, evenly spaced, symmetric airfoil
#%%SHEAR FLOW
#cuts made at stringer 1 and half of spar
#Booms (booms match up with stringer locations except spar ones!)
B0 = (1/2)*Areastringer + (1/2)*space*tsk               #boom0 (half of stringer due to cut)
B1 = Areastringer + (1/2)*space*tsk + arcspace*tsk      #boom1 on arc (left of spar)
B2 = Areastringer + (1/2)*space*tsk + barspace*tsk      #boom2 on bar (right of spar)
Bgen = Areastringer + space*tsk                         #boom area in general
Bspar = (ha/2)*tsp                                      #boom at top and bottom of spar 
AREAcell1 =  0.5*np.pi*(ha/2)**2                        #Area of the cross section cell 1 LEFT OF SPAR (NOT ONLY SKIN/STRINGERS)
AREAcell2 = (Ca - (ha/2))*(ha/2)                           #Area of the cross section cell 2 RIGHT OF SPAR (NOT ONLY SKIN/STRINGERS)
#%% Shear flow due to Sy
airfoilx = 0.5
Sy = -48625.85466784
#Sy = 1
#obtained from graph of interpolation sheme 
steps = 100
#region 1 
theta1 = np.linspace(0,np.pi/2,steps)
intr1 = sum(((ha/2)**2)*np.sin(theta1)*((np.pi/2)/steps))*tsk #riemann sum
qyb1 = (-Sy/Izz)*(intr1 +stringery[0]*B0+stringery[1]*B1) 
#region 2
h2 = np.linspace(0,ha/2,steps)
intr2 = sum(h2*((ha/2)/steps))*tsp #riemann sum
qyb2 = (-Sy/Izz)*(intr2+ (ha/2)*Bspar) + qyb1
#region 3
s3 = np.linspace(0,diagbar,steps)
intr3 = sum(((ha/2)-(((ha/2)/diagbar)*s3))*(diagbar/steps))*tsk #riemann sum
qyb3 = (-Sy/Izz)*(intr3+ stringery[2]*B2 + stringery[3]*Bgen + stringery[4]*Bgen +stringery[5]*Bgen + stringery[6]*Bgen) + qyb1 + qyb2
#region 4
s4 = np.linspace(0,diagbar,steps)
intr4 = sum(-((ha/2)*s4/diagbar)*(diagbar/steps))*tsk #riemann sum
qyb4 = (-Sy/Izz)*((intr4)+ stringery[7]*B2 + stringery[8]*Bgen + stringery[9]*Bgen +stringery[10]*Bgen + stringery[11]*Bgen) + qyb3
#region 5 
h5 = np.linspace(-ha/2,0,steps)
intr5 = sum(h5*((ha/2)/steps))*tsp #riemann sum
qyb5 = (-Sy/Izz)*(intr5+ (-ha/2)*Bspar) + qyb4
#region 6 
theta6 = np.linspace(-np.pi/2,0,steps)
intr6 = sum(((ha/2)**2)*np.sin(theta6)*((np.pi/2)/steps))*tsk #riemann sum
qyb6 = (-Sy/Izz)*((intr6)+stringery[0]*B0+stringery[12]*B1) - qyb5 + qyb4
#%% Shear flow due to Sz
airfoilx = 0.5
Sz = 247535.26084513
#Sz = 1
#obtained from graph of interpolation sheme 
#region 1 
thetaz1 = np.linspace(0,np.pi/2,steps)
intrz1 = (sum(((1-np.cos(thetaz1))*ha/2-zc)*((np.pi*ha/4)/steps)))*tsk #riemann sum
qzb1 = (-Sz/Iyy)*(intrz1 +(stringerz[0]-zc)*B0+(stringerz[1]-zc)*B1) 
#region 2
hz2 = np.linspace(0,ha/2,steps)
intrz2 = (ha/2-zc)*ha/2*tsp #riemann sum
qzb2 = (-Sz/Iyy)*(intrz2+ (ha/2)*Bspar) + qzb1
#region 3
sz3 = np.linspace(0,diagbar,steps)
intrz3 = sum(((ha/2-zc)-(((Ca-ha/2)/diagbar)*sz3))*(diagbar/steps))*tsk #riemann sum
qzb3 = (-Sz/Iyy)*(intrz3+ (stringerz[2]-zc)*B2 + (stringerz[3]-zc)*Bgen + (stringerz[4]-zc)*Bgen +(stringerz[5]-zc)*Bgen + (stringerz[6]-zc)*Bgen) + qzb1 + qzb2
#region 4
sz4 = np.linspace(0,diagbar,steps)
intrz4 = sum(((Ca-zc)+sz4*((Ca-ha/2)/diagbar))*(diagbar/steps))*tsk #riemann sum
qzb4 = (-Sz/Iyy)*((intrz4)+ (stringerz[7]-zc)*B2 + (stringerz[8]-zc)*Bgen + (stringerz[9]-zc)*Bgen +(stringerz[10]-zc)*Bgen + (stringerz[11]-zc)*Bgen) + qzb3
#region 5 
hz5 = np.linspace(-ha/2,0,steps)
intrz5 = (ha/2-zc)*-ha/2*tsp #riemann sum
qzb5 = (-Sz/Iyy)*(intrz5+ (-ha/2)*Bspar) + qzb4
#region 6 
thetaz6 = np.linspace(-np.pi/2,0,steps)
intrz6 = sum(((1-np.cos(thetaz1))*ha/2-zc)*((np.pi*ha/4)/steps))*tsk #riemann sum
qzb6 = (-Sz/Iyy)*((intrz6)+(stringerz[0]-zc)*B0+(stringerz[12]-zc)*B1) - qzb5 + qzb4
#%% TOTAL BASE FLOWS
qtb1 = qyb1 + qzb1
qtb2 = qyb2 + qzb2
qtb3 = qyb3 + qzb3
qtb4 = qyb4 + qzb4
qtb5 = qyb5 + qzb5
qtb6 = qyb6 + qzb6
#%%
#matrix system for shear flow
#rate of twist kept equal to zero
#Left cell
th_z1lq1 = (ha*np.pi)/(8*AREAcell1*tsk) #region 1 q01
th_z6lq1 = (ha*np.pi)/(8*AREAcell1*tsk) #region 6 q01
th_z2lq1 = (-ha)/(4*AREAcell1*tsp)      #region 2 q01
th_z2lq2 = (ha)/(4*AREAcell1*tsp)       #region 2 q02
th_z5lq1 = (-ha)/(4*AREAcell1*tsp)      #region 5 q01
th_z5lq2 = (ha)/(4*AREAcell1*tsp)       #region 5 q02
#Right cell
th_z2rq1 = (-ha)/(4*AREAcell2*tsp)      #region 2 q01
th_z2rq2 = (ha)/(4*AREAcell2*tsp)       #region 2 q02
th_z5rq1 = (-ha)/(4*AREAcell2*tsp)      #region 5 q01
th_z5rq2 = (ha)/(4*AREAcell2*tsp)       #region 5 q02
th_z3rq2 = (diagbar)/(2*AREAcell2*tsk)  #region 3 q02
th_z4rq2 = (diagbar)/(2*AREAcell2*tsk)  #region 4 q02
#Deflection compatibility
BMAT1 = -qyb1*(np.pi*ha/4)/(2*AREAcell1*tsk)-qyb2*(ha/2)/(2*AREAcell1*tsp)-qyb5*(ha/2)/(2*AREAcell1*tsp)-qyb6*(np.pi*ha/4)/(2*AREAcell1*tsk)
BMAT2 = -qyb2*(ha/2)/(2*AREAcell2*tsp)-qyb3*diagbar/(2*AREAcell2*tsk)-qyb4*diagbar/(2*AREAcell2*tsk)-qyb5*(ha/2)/(2*AREAcell2*tsp)
#MATRIX
AMAT = [[th_z1lq1 + th_z6lq1 + th_z2lq1 + th_z5lq1, th_z2lq2 +th_z5lq2 ],[th_z2rq1+th_z5rq1,th_z2rq2+th_z5rq2+th_z3rq2+th_z4rq2]]
BMAT = [[BMAT1],[BMAT2]]
invA = np.linalg.inv(AMAT)
solution = np.dot(invA,BMAT)
q01 = solution[0]
q02 = solution[1]
#moment equilibrium (Sy neglected since Sy=1)
#shear centre denoted as sc
#assumed vector of the arc is pointed upwards and turns as one moves over the arc (arm remains the same) - always tangent to arc surface
#only horizontal component used of the spar shear flow 
#spar shear directed towards hinge thus = 0
scy = 0.0
# z coordinate is determined wrt hinge point (at ha/2) 
scz =  (ha/2)-(q01*2*AREAcell1 + q02*2*AREAcell2 + qyb3*(ha/2)*np.sqrt((diagbar**2)-(ha/2)**2) + qyb4*(ha/2)*np.sqrt((diagbar**2)-(ha/2)**2)  + (ha/2)* qyb1*(np.pi*ha/4) + (ha/2)* qyb6*(np.pi*ha/4))/Sy
sc = [scy, scz]
#%% TORQUE SHEAR FLOW CONTRIBUTION 
#at x = 0.5
#Sy_veri
#-48625.85466784
#Sz_veri
#247535.26084513
#T_veri
#9849.6772966
# Formula used is T= A1*qt01+A2* qt02
#Both torque shear flows assumed to be clockwise direction 
T = 2*q01*AREAcell1 + 2*q02 * AREAcell2
#qt01 = (T/(2*AREAcs))*AREAcell1
#qt02 = (T/(2*AREAcs))*AREAcell2
#%% SHEAR FLOW DISTRIBUTIONS
#assumption: shear flow is linearly distributed (distributed wrt to area covered) along region 
#everytime a boom is encountered a new subsection is created and the encountered area of boom is included
#NAMES OF VARIABLES USED CAN BE TRANSLATED USING THE FOLLLOWING:
#qx"start location section""end location section" moves along the section in # of steps
#q"region"dis_"start location section""end location section"
# assummed in total every region has 100 array points 
figure, axes = plt.subplots(nrows=2, ncols=3)
### region 1 
sfr1 = []
q1 = (qtb1 + q01)/10
for qxb0b1 in range (0,66):
    q1dis_b0b1 = q1/((space+arcspace)*tsk+B1+B0) * (qxb0b1*(space/66)*tsk) # stringer 0 to stringer 1 
    sfr1.append(q1dis_b0b1)
for qxb1sp in range (0,34):
    q1dis_b1sp = q1/((space+arcspace)*tsk+B1+B0) * (qxb1sp*(arcspace/34)*tsk+tsk*space+B1) # stringer 1 to spar
    sfr1.append(q1dis_b1sp)
axes[0, 0].plot(sfr1)
ssr1 = sfr1/tsk
### region 2
sfr2 = []
q2 = (qtb2 + q01 - q02)/10
for qxsp2 in range(0,100):
    q2dis_sp2 = q2/((ha/2)*tsp) * (qxsp2*ha/(2*steps)*tsp) #spar top to spar center
    sfr2.append(q2dis_sp2)
axes[0, 1].plot(sfr2)
ssr2 = sfr2/tsp
### region 3
sfr3 = []
q3 = (qtb3 + q02)/10
for qxspb2 in range (0,10):
    q3dis_spb2 = q3/((barspace+4.5*space)*tsk + 5*Bgen) * (qxspb2*barspace/10*tsk) # spar to stringer 2 
    sfr3.append(q3dis_spb2)
for qxb2b3 in range (0,20):
    q3dis_b2b3 = q3/((barspace+4.5*space)*tsk + 5*Bgen) * (qxb2b3*space/20*tsk+barspace*tsk+1*Bgen) # stringer 2 to stringer 3
    sfr3.append(q3dis_b2b3)
for qxb3b4 in range (0,20):
    q3dis_b3b4 = q3/((barspace+4.5*space)*tsk + 5*Bgen) * (qxb3b4*space/20*tsk+(barspace+space*1)*tsk+1*Bgen+2*Bgen) # stringer 3 to stringer 4
    sfr3.append(q3dis_b3b4)
for qxb4b5 in range (0,20):
    q3dis_b4b5 = q3/((barspace+4.5*space)*tsk + 5*Bgen) * (qxb4b5*space/20*tsk+(barspace+space*2)*tsk+1*Bgen+3*Bgen) # stringer 4 to stringer 5
    sfr3.append(q3dis_b4b5)
for qxb5b6 in range (0,20):
    q3dis_b5b6 = q3/((barspace+4.5*space)*tsk + 5*Bgen) * (qxb5b6*space/20*tsk+(barspace+space*3)*tsk+1*Bgen+4*Bgen) # stringer 5 to stringer 6
    sfr3.append(q3dis_b5b6)
for qxb6TE in range (0,10):
    q3dis_b6TE = q3/((barspace+4.5*space)*tsk + 5*Bgen) * (qxb6TE*space/20*tsk+(barspace+space*4)*tsk+1*Bgen+5*Bgen) # stringer 6 to TE
    sfr3.append(q3dis_b6TE)
axes[0, 2].plot(sfr3)
ssr3 = sfr3/tsk
### region 4
sfr4 = []
q4 = (qtb4 + q02)/10
for qxTEb7 in range (0,10):
    q4dis_TEb7 = q4/((barspace+4.5*space)*tsk + 5*Bgen) * (qxTEb7*tsk*space/20) # stringer TE to stringer 7
    sfr4.append(q4dis_TEb7)
for qxb7b8 in range (0,20):
    q4dis_b7b8 = q4/((barspace+4.5*space)*tsk + 5*Bgen) * (qxb7b8*tsk*space/20+space*0.5*tsk+ 1*Bgen) # stringer 7 to stringer 8
    sfr4.append(q4dis_b7b8)
for qxb8b9 in range (0,20):
    q4dis_b8b9 = q4/((barspace+4.5*space)*tsk + 5*Bgen) * (qxb8b9*tsk*space/20+space*1.5*tsk+ 2*Bgen) # stringer 8 to stringer 9
    sfr4.append(q4dis_b8b9)
for qxb9b10 in range (0,20):
    q4dis_b9b10 = q4/((barspace+4.5*space)*tsk + 5*Bgen) * (qxb9b10*tsk*space/20+space*2.5*tsk+ 3*Bgen) # stringer 9 to stringer 10
    sfr4.append(q4dis_b9b10)
for qxb10b11 in range (0,20):
    q4dis_b10b11 = q4/((barspace+4.5*space)*tsk + 5*Bgen) * (qxb10b11*tsk*space/20+space*3.5*tsk+ 4*Bgen) # stringer 10 to stringer 11
    sfr4.append(q4dis_b10b11)
for qxb11sp in range (0,10):
    q4dis_b11sp = q4/((barspace+4.5*space)*tsk + 5*Bgen) * (qxb11sp*tsk*barspace/10+space*4.5*tsk+ 5*Bgen) # stringer 11 to spar
    sfr4.append(q4dis_b11sp)
axes[1, 0].plot(sfr4)
ssr4 = sfr4/tsk
#region 5 
sfr5 = []
q5 = (qtb5 + q01 - q02)/10
for qxsp5 in range (0,100):
    q5dis_sp5 = q5/((ha/2)*tsp) * (qxsp5*ha/(2*steps)*tsp) #spar bottom to spar center
    sfr5.append(q5dis_sp5)
axes[1, 1].plot(sfr5)
ssr5 = sfr5/tsp
### region 6 
sfr6 = []
q6 = (qtb6 + q01)/10
for qxspb12 in range (0,34):
    q6dis_spb12 = q6/((space+arcspace)*tsk+B1+B0) * (qxspb12*tsk*(arcspace/34)) # spar to stringer 12 
    sfr6.append(q6dis_spb12)
for qxb12b0 in range (0,66):
    q6dis_b12b0 = q6/((space+arcspace)*tsk+B1+B0) * (qxb12b0*tsk*space/66+arcspace*tsk+B1) # spar 12 to stringer 0
    sfr6.append(q6dis_b12b0)
ssr6 = sfr6/tsk
axes[1, 2].plot(sfr6)
figure.tight_layout()
plt.show
#%% Torsional constant calculated at cell1 
AREA1 = 0.5*np.pi*(ha/2)**2
AREA2 = (Ca - (ha/2))*(ha/2)
GMAT = np.array([[2*AREA1,2*AREA2,0],[(1/(2*AREA1))*(((np.pi*(ha/2))/tsk) + (ha/tsp)),(-1/(2*AREA1))*(ha/tsp),-1],[(-1/(2*AREA2))*(ha/tsp),(1/(2*AREA2))*(((2*diagbar)/tsk) + (ha/tsp)),-1]])
TMAT = [1,0,0]
solutiong = np.linalg.solve(GMAT,TMAT)
#qg1 = solutiong[0]
#qg2 = solutiong[1]
Gtheta = solutiong[2]
J = 1/Gtheta
#cell1
t1q1 = (ha*np.pi)/(8*AREAcell1*tsk)*q1  #region 1 q01
t1q2 = (ha)/(4*AREAcell1*tsp)*q2        #region 6 q01
t1q5 = (ha)/(4*AREAcell1*tsp)*q5        #region 2 q01
t1q6 = (ha*np.pi)/(8*AREAcell1*tsk)*q6          #region 2 q02

#cell2
t2q2 = (ha)/(4*AREAcell2*tsp)*q2      #region 2 q01
t2q3 = (diagbar)/(2*AREAcell2*tsk)*q3       #region 2 q02
t2q4 = (diagbar)/(2*AREAcell2*tsk)*q4     #region 5 q01
t2q5 = (ha)/(4*AREAcell2*tsp)*q5      #region 5 q02

rotc1 = (t1q1 +t1q6+t1q5+t1q2)/G
rotc2 = (t2q3 +t2q4+t2q5+t2q2)/G
Tj = J*rotc1*G

#%% IMPORTANT DATA 
print("Izz =", Izz)
print("Iyy =", Iyy)
print("centroidzy =", centroidzy)
print("shear center =", sc)
plt.figure()
plt.plot(stringerz,stringery,'bs')
plt.plot(zc,yc,'g^')    #CENTROID
plt.plot(scz,scy,'r+')  #SHEAR CENTER
plt.plot(hz,hy,'bo')    #Midspar
plt.show()