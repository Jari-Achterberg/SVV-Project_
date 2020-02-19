# Making the integration_scheme
from Coordinates import d, Nx, Nz


def integral(x1, x2, y1, y2):
    # Calculating parameters for linear equation y = ax + b
    a = (y2-y1)/(x2-x1)
    b = y1-((y2-y1)/(x2-x1))*x1

    # Integration scheme for f(x)=ax+b
    intaxbvar = (a/2)*(x2**2 - x1**2) + b*(x2-x1)
    # should be similar to: (y1 + y2)*(x2 - x1)/2

    # Integration scheme for f(x)=(ax+b)*x
    intxaxbvar = (1/3)*a*(x2**3 - x1**3) + 0.5*b*(x2**2-x1**2)

    return intaxbvar, intxaxbvar


index = 0
line_load, torques = [], []

for i in range(0, Nx):

    load = 0        # kN / m (both variables are integrated once,
    torque = 0      # kN      they become a 2D representation of the 3D distributed load)

    for j in range(0, Nz-1):

        intaxb, intxaxb = integral(d[index][1], d[index+1][1], float(d[index][2]), float(d[index+1][2]))
        load += intaxb
        torque += intxaxb
        index += 1

    line_load.append(load)
    torques.append(torque)

# check if found loads and torques have reasonable numbers
print(line_load[3])
print(torques[3])