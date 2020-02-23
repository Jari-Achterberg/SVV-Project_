# Calculating Aerodynamic Loading
from Coordinates import d, Nx, Nz, x_list


def integral(x1, x2, y1, y2):
    # Calculating parameters for linear equation y = ax + b
    a = (y2 - y1) / (x2 - x1)
    b = y1 - ((y2 - y1) / (x2 - x1)) * x1

    # Integration scheme for f(x)=ax+b
    intaxbvar = (a / 2) * (x2 ** 2 - x1 ** 2) + b * (x2 - x1)
    # should be similar to: (y1 + y2)*(x2 - x1)/2

    # Integration scheme for f(x)=(ax+b)*x
    intxaxbvar = (1 / 3) * a * (x2 ** 3 - x1 ** 3) + 0.5 * b * (x2 ** 2 - x1 ** 2)

    return intaxbvar, intxaxbvar


def double_integral(x1, x2, y1, y2):
    # Calculating parameters for linear equation y = ax + b
    a = (y2 - y1) / (x2 - x1)
    b = y1 - ((y2 - y1) / (x2 - x1)) * x1

    # Integration scheme for f(x)=ax+b
    intaxbvar = (a / 6) * (x2 ** 3 - x1 ** 3) + (b / 2) * (x2 ** 2 - x1 ** 2)
    # should be similar to: (y1 + y2)*(x2 - x1)/2

    return intaxbvar

index = 0
line_load, torques = [], []

for i in range(0, Nx):

    load = 0  # kN / m (both variables are integrated once,
    torque = 0  # kN      they become a 2D representation of the 3D distributed load)

    for j in range(0, Nz - 1):
        intaxb, intxaxb = integral(d[index][1], d[index + 1][1], float(d[index][2]), float(d[index + 1][2]))

        load += intaxb
        torque += intxaxb
        index += 1

    # loads and torques are integrated from 0 to Chord length, but it should be the other way around
    # that's why a minus is inserted here
    line_load.append(-load)  # Correction because all z-coordinates are negative
    torques.append(-torque)  # Correction because all z-coordinates are negative

# for total torque calculate sum of found torques ( for torque/Mx)
# for moment in z- direction integrate the line load once again to obtain the moment

force, moment = 0, 0
force_lst, moment_lst = [], []

# steps taken to estimate integral, can be changed
steps = 100

# define length from first known value to last known value (what to do with the unknown part???
length = x_list[-1] - x_list[0]
stepsize = length / steps

# define func list
func_lst = []
for q in range(len(x_list) - 1):
    x1 = x_list[q]
    x2 = x_list[q + 1]
    y1 = line_load[q]
    y2 = line_load[q + 1]

    # define a and b
    a = (y2 - y1) / (x2 - x1)
    b = (y1 - a * x1)

    func_lst.append((a, b))

def aerodynamicloading(x):

    inx = 0                             # Just a temporary value to index
    x_value = 0                         # Initial starting value
    force, moment = 0, 0                # Initial starting value
    force_lst, moment_lst = [], []      # Initialise lst

    for j in range(steps):
        print(j)
        x_value = stepsize * j + x_list[0]

        if x_value>x:
            break

        if x_value>x_list[inx]:
            inx =+ 1

        force = force + (func_lst[inx][0]*x_value)*stepsize + func_lst[inx][1]
        moment = moment + (func_lst[inx][0]*(x_value-(stepsize/2)) + func_lst[inx][1])*((stepsize**2)/2)

        force_lst.append(force)
        moment_lst.append(moment)

    return force_lst, moment_lst

#
