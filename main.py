# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 23:41:38 2020

@author: Group A02
"""

import math as m
import numpy as np
import pickle

#  ===================== Input Parameters: ====================== 
#To be inputed in the indicated units.
aircraft = "B737" # Aircraft type, influences aerodynamic load
Ca     = 0.605         # aileron chord                                [m]
la     = 2.661         # span of aileron                              [m]
x1     = 0.172         # x-location of hinge 1                        [m]
x2     = 1.211         # x-location of hinge 2                        [m]
x3     = 2.591         # x-location of hinge 3                        [m]
xa     = .35           # distance between Actuator I and Actuator II  [m]
ha     = .205          # aileron height                               [m]
tsk = 1.1/1000         # skin thickness                               [m]
tsp = 2.8/1000         # spar thickness                               [m]
tst = 1.2/1000         # stiffener thickness                          [m]
hst = 0.016            # stiffener height                             [m]
wst = 0.019            # stiffener width                              [m]
nst = 15               # number of stiffeners                         [-]
d1 = 0.01154           # vertical deflection hinge 1                  [m]
d3 = 0.01840           # vertical deflection hinge 3                  [m]
theta = m.radians(28)  # aileron - wing angle                        [rad]
P = 97.4/1000          # actuator II load                             [N]

E       = 70        # material Young's modulus                       [GPa]
G       = 28.0        # material shear moduus                        [GPa]
# rho     = 2780        # material density                            [kg m^-3]


# ================= Functions ===========================
# MacCauley stepfunction
def MC(x, a, e):
    if max((x-a), 0) == (x-a) and e > 0:
        return (x-a)**e
    elif max((x-a), 0) > (x-a) and e == 0:
        return 1
    else:
        return 0

# ================ Aerodynamic Loading ==================
filename='aeroloading'
with open(filename, "rb") as f:
    force_list,moment_list,torque_list, moment_II_list, torque_I_list, stepsize = pickle.load(f)

def V_q(x):
    index = round(x/stepsize)
    Vq = force_list[index]
    return Vq

def M_q(x):
    index = round(x / stepsize)
    Mq = moment_list[index]
    return Mq

def T_q(x):
    index = round(x / stepsize)
    Tq = torque_list[index]
    return Tq

def M_qII(x):
    index = round(x / stepsize)
    M_qII = moment_II_list[index]
    return M_qII

def T_q_II(x):
    index = round(x / stepsize)
    T_q_II = torque_I_list[index]
    return T_q_II

# =================Geometrical properties of airfoil================
eta = Ca/4  # Preliminary value for shear center, input correct one or call function here.
Iyy = 1     # Preliminary values for MoI, input correct values or call functions here.
Izz = 1


# ========================================================================
# =========== Solve Reaction forces, moments and deflections:  =========== 
# ========================================================================
# Additional Parameters:
x_I     = x2-xa/2
x_II    = x2+xa/2
z_h     = eta-ha/2

# ================= Linear System Solver ===========================
# Set up Linear System:
A       = np.zeros((12, 12))
B       = np.zeros((12))

# Variables :  {var} = [Ry1, Rz1, Ry2, Rz2, Ry3, Rz3, R_I, C1, C2, C3, C4, C5]

# Each equation is set up and allocated to the matrix, on the left side of the equation,
# the coefficients of the variables on the {var} vector are inputed in an array
# and allocated to the respective line on the matrix A.
# Entries are done such as if everything was kept on one side of the equation
# -- right notation is not what it seems like (i.e its on the right), it is just the set of terms
# that are not affected by an unknown variable, ie: u({vec},x) = u_left({vec},x) + u_right(x).
# On the right side are the non-homogeneous terms (known scalars) from your compatibility/boundary equations.


v_left       = lambda X : -1/(E*Izz)  *  np.array([-1/6*MC(X, x1, 3), 0, -1/6*MC(X, x2, 3), 0, -1/6*MC(X, x3, 3), 0, -m.sin(theta)/6*MC(X, x_I, 3), X, 1, 0, 0, 0])
v_right      = lambda X : -1/(E*Izz)  *  (M_qII(X) + 1/6*MC(X, x_II, 3)*P*m.sin(theta)/6)


w_left      = lambda X : -1/(E*Iyy)  *  np.array([0,1/6*MC(X, x1, 3), 0, 1/6*MC(X, x2, 3), 0, 1/6*MC(X, x3, 3), 1/6*MC(X, x3, 3), 0, -m.cos(theta)/6*MC(X, x_I, 3), 0, 0, X, 1, 0])
w_right       = lambda X : -1/(E*Iyy_airfoil)*         (1/6*MC(X, x_II, 3)*P*m.cos(theta))
                                                                             

phi_left   = lambda X : 1/(G*J)           * np.array([(z_h)*MC(X, x1, 1), 0, (z_h)*MC(X, x2, 1), 0, z_h*MC(X, x3, 1), 0, -m.cos(theta)*ha/2*MC(X, x_I, 1), 0, 0, 0, 0, 1])
phi_right   = lambda X : 1/(G*J)           *         (P*(m.sin(theta)*eta*MC(X, x_II, 1)  - m.cos(theta)*ha/2*MC(X, x_II, 1))   + T_q_II(X))


T_left      = lambda X :                     np.array([z_h*MC(X, x1, 0), 0, -z_h*MC(X, x2, 0), 0, -z_h*MC(X, x3, 0), 0, m.sin(theta)*eta*MC(X, x_I, 0)-m.cos(theta)*ha/2*MC(X, x_I, 0), 0, 0, 0, 0, 0])
T_right      = lambda X :                             (- P*(m.sin(theta)*eta*MC(X, x_II, 0) - m.cos(theta)*ha/2*MC(X, x_II, 0)))
# Unknowns  :  {vec} = [Ry1, Ry2, Ry3, Rz1, Rz2, Rz3, Cu_p0, Cu0, Cv_p0, Cv0, Ctheta0, Py_I, Pz_I]
# Variables :  {var} = [Ry1, Rz1, Ry2, Rz2, Ry3, Rz3, R_I, C1, C2, C3, C4, C5]
My_left      = lambda X :                     np.array([0, MC(X, x1, 1), 0, MC(X, x2, 1), 0, MC(X, x3, 1), -m.cos(theta)*MC(X, x_I, 1), 0, 0, 0, 0, 0])
My_right      = lambda X :                             (P*m.cos(theta)*MC(X, x_II, 1))

Mz_left      = lambda X :                     np.array([-MC(X, x1, 1), 0, -MC(X, x2, 1), 0, -MC(X, x3, 1), 0,  -m.sin(theta)*MC(X, x_I, 1), 0, 0, 0, 0, 0])
Mz_right      = lambda X :                             (P*m.sin(theta)*MC(X, x_II, 1) + M_q(X))

# Row 1 -5  :  Force and Moment Equilibrium around x = la
# Row 6 -7  :  Hinge 1 Deflection Constraint
# Row 8 -9 :  Hinge 2 Deflection Constraint
# Row 10-11 :  Hinge 3 Deflection Constraint
# Row 12    :  Actuator Deflection Constraint

# A[0,11], A[0,12],   B[0]    =  -1, -m.tan(theta)                                       ,   0
A[0, :],            B[0]    = np.array([1, 0, 1, 0, 1, 0, m.sin(theta), 0, 0, 0, 0, 0])                                                     ,   0 + V_q(X) - P*m.sin(theta)
A[1, :],            B[1]    = np.array([0, 1, 0, 1, 0, 1, m.cos(theta), 0, 0, 0, 0, 0])                                                                                                  ,   0 -   Rz_right(la)
A[2, :],            B[2]    = T_left(la)                                                                                                  ,   0 -   T_right(la)
A[3, :],            B[3]    = My_left(la)                                                                                                  ,   0 -   My_right(la)
A[4, :],            B[4]    = Mz_left(la)                                                                                                  ,   0 -   Mz_right(la)
A[5, :],            B[5]    = v_left(x1) + phi_left(x1)*z_h                             , d1*m.cos(theta) - v_right(x1) - phi_right(x1)*z_h
A[6, :],            B[6]    = w_left(x1)                             , d1*m.sin(theta) - w_right(x1)
A[7, :],            B[7]    = v_left(x2) + phi_left(x2)*z_h                             , d2*m.cos(theta) - v_right(x2) - phi_right(x2)*z_h
A[8, :],            B[8]    = w_left(x2)                             , - w_right(x2)
A[9, :],            B[9]    = v_left(x3) + phi_left(x3)*z_h                             , d3*m.cos(theta) - v_right(x3) - phi_right(x3)*z_h
A[10, :],           B[10]   = w_left(x3)                             , d3*m.sin(theta) - w_right(x3)
A[11, :],           B[11]   = m.sin(theta)*(u_left(x_I) - phi_left(x_I) * eta) - m.cos(theta)*(w_left(x_I) - phi_left(x_I)*ha/2)    ,   0 - m.sin(theta)*(u_right(x_I) - phi_right(x_I) * eta) - m.cos(theta)*(w_right(x_I) - phi_right(x_I)*ha/2)

# Solve for A {var} = B
var = np.linalg.solve(A, B)
Ry1, Rz1, Ry2, Rz2, Ry3, Rz3, R_I, C1, C2, C3, C4, C5 = var        # Note: u0 = Cu0/(EIzz), v0 = Cv0/(EIyy), theta0 = Ctheta0/(GJ)

T      = np.sum(Mx_left(x)*var)         + T_right(x)
My      = np.sum(My_left(x)*var)         + My_right(x)
Mz      = np.sum(Mz_left(x)*var)         + Mz_right(x)
phi   = np.sum(phi_left(x)*var)      + phi_right(x)
v       = np.sum(v_left(x)*var)          + v_right(x)
w       = np.sum(w_left(x)*var)          + w_right(x)
V       = m.cos(theta)*(v(x) + phi(x)*z_h) + m.sin(theta)*(w(x)+ha/2*phi(x))
# W       = -m.sin(theta)*(u - theta*(z_h) ) + m.cos(theta)*v

