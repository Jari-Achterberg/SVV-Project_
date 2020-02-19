# Making the integration_scheme

from Coordinates import d
# Input variables
x1 = 4
x2 = 6
y1 = 3
y2 = 8

# Calculating parameters for linear equation y = ax + b
a = (y2-y1)/(x2-x1)
b = y1-((y2-y1)/(x2-x1))*x1

# Integration scheme for f(x)=ax+b
intaxb = (a/2)*(x2**2 - x1**2) + b*(x2-x1)

# Integration scheme for f(x)=(ax+b)*x
intxaxb = (1/3)*a*(x2**3 - x1**3) + 0.5*b*(x2**2-x1**2)
