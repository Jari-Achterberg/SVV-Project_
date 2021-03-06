# This program calculates the coordinates of the discrete aerodynamic loading
import csv
import math
from matplotlib import pyplot as plt
# Input variables
Nz = 81
Nx = 41
Ca = 0.484  # m
la = 1.691  # m

##
# read the file first
loading = []
with open('aerodynamicloadcrj700.dat') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    # line_count = 0
    for row in csv_reader:
        loading.append(row)

# print(len(loading))         # Check if equal to Nz
# print(len(loading[0]))      # Check if equal to Nx

# calculate coordinates and append to dictionary as  d[index] = [x,z,load]
d = dict()
index = 0
x_list = []
z_list = []
xstep = []
xzx_list, xzz_list, xzload_list = [], [], []

for j in range(1, Nx + 1):
    theta_xi = (j - 1) / Nx * math.pi
    theta_xi_next = j / Nx * math.pi
    x = 0.5 * ((la / 2) * (1 - math.cos(theta_xi)) + (la/2)*(1 - math.cos(theta_xi_next)))
    x_list.append(x)
    if j > 2:
       xstep.append(x - x_list[-2])
    for i in range(1, Nz + 1):
        theta_zi = (i - 1) / Nz * math.pi
        theta_zi_next = i / Nz * math.pi
        # minus sign removed, because different coordinate system of the z-axis
        z = 0.5 * ((Ca / 2) * (1 - math.cos(theta_zi)) + (Ca / 2) * (1 - math.cos(theta_zi_next)))
        z_list.append(z)

        d[index] = (x, z, -float(loading[i - 1][j - 1]))    # Aerodynamic loading is negative in our coordinate system
        xzx_list.append(x)
        xzz_list.append(z)
        xzload_list.append(-float(loading[i - 1][j - 1]))
        index += 1

# dictionary x -> (z, load)
# check x, z values
print(d[80])
print(d[81])

# print max min values
print("minimum x: ", min(x_list))
print("minimum z: ", min(z_list))
print("maximum x: ", max(x_list))
print("maximum z: ", max(z_list))
print("maximum step size in x direction: ", max(xstep))
print(sum(xstep)/len(xstep))
avg_load = sum(xzload_list)/len(xzload_list)
print("average loading: ", avg_load)
# plot coordinates
#x_list.extend(x_list)
# plt.scatter(xzx_list, xzz_list, c=xzload_list)
# plt.scatter(xzx_list, xzload_list, c=xzload_list)
# plt.xlabel('x')
# plt.ylabel('z')
# plt.colorbar()
# plt.show()

# verify magnitude order for Mz, Sy, T, etc
print("SY magnitude:", avg_load*la*Ca)
print("T magnitude: ", avg_load*Ca*Ca/2*la)
print("Mz magnitude: ", avg_load*Ca*la*la/2)
print("T int magnitude: ", avg_load*Ca*Ca/2*la*la)
print("Mz 2x int magnitude: ", avg_load*Ca*la*la/2*(la/2)**2)
# print("")