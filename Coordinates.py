# This program calculates the coordinates of the discrete aerodynamic loading
import csv
import math

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

for j in range(1, Nx + 1):
    theta_xi = (j - 1) / Nx * math.pi
    theta_xi_next = j / Nx * math.pi
    x = 0.5 * ((la / 2) * (1 - math.cos(theta_xi)) + (la/2)*(1 - math.cos(theta_xi_next)))
    x_list.append(x)
    for i in range(1, Nz + 1):
        theta_zi = (i - 1) / Nz * math.pi
        theta_zi_next = i / Nz * math.pi
        # minus sign removed, because different coordinate system of the z-axis
        z = 0.5 * ((Ca / 2) * (1 - math.cos(theta_zi)) + (Ca / 2) * (1 - math.cos(theta_zi_next)))

        d[index] = (x, z, -float(loading[i - 1][j - 1]))
        index += 1

# dictionary x -> (z, load)
# print(d[80])
# print(d[81])
