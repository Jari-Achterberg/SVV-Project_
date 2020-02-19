# This program calculates the coordinates of the discrete aerodynamic loading
import csv
import math
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


# calculate coordinates and append to dictionary as  d[x] = [(z, load),(z, load), etc]
d = dict()

for j in range(1, Nx + 1):
    theta_xi = (j - 1) / Nz * math.pi
    theta_xi_next = j / Nz * math.pi
    x = 0.5 * ((la / 2) * (1 - math.cos(theta_xi)) + (la/2)*(1 - math.cos(theta_xi_next)))
    for i in range(1, Nz + 1):
        theta_zi = (i - 1) / Nz * math.pi
        theta_zi_next = i / Nz * math.pi
        z = - 0.5 * ((Ca / 2) * (1 - math.cos(theta_zi)) + (Ca / 2) * (1 - math.cos(theta_zi_next)))
        if x in d:
            d[x].append((z, loading[i - 1][j - 1]))
        else:
            d[x] = [(z, loading[i - 1][j - 1])]

# dictionary x -> (z, load)
