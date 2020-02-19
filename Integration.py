# this program calculates the integration and interpolation schemes
# x = 0
import csv
import math
Nz = 81
i = 3342
theta_z = i - 1 / Nz * math.pi
####
loading = []
with open('aerodynamicloadcrj700.dat') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    # line_count = 0
    for row in csv_reader:
        loading.append(row)
    # print(f'Processed {line_count} lines.')
print(loading)
