# Making the integration_scheme
from Coordinates import d, Nx, Nz


def integral(x1, x2, y1, y2):
    # Calculating parameters for linear equation y = ax + b
    a = (y2-y1)/(x2-x1)
    b = y1-((y2-y1)/(x2-x1))*x1

    # Integration scheme for f(x)=ax+b
    intaxbvar = (a/2)*(x2**2 - x1**2) + b*(x2-x1)

    # Integration scheme for f(x)=(ax+b)*x
    intxaxbvar = (1/3)*a*(x2**3 - x1**3) + 0.5*b*(x2**2-x1**2)

    return intaxbvar, intxaxbvar


index = 0
for x in range(0, Nx):

    for j in range(0, Nz-1):

        intaxb, intxaxb = integral(d[index][1], d[index+1][1], d[index][2], d[index+1][2])
        index += 1

