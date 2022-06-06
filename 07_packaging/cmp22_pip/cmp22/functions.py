
from numpy import *

def function1(x):
    "y = x*(x - 3)*(x + 3)"
    y = x*(x - 3)*(x + 3)
    return y

def function2(x):
    "y = abs(x)"
    y = abs(x)
    return y

def function3(x):
    "y = sin(x * 2.1) * (-x / 2.0)"
    y = sin(x * 2.1) * (-x / 2.0)
    return y

def function4(x):
    "y = 1.6**x - 1.5 * x"
    y = 1.6**x - 1.5 * x
    return y

def function5(x,y):
    "z = sin(x + y) * tan(0.1 * x)"
    z = sin(x + y) * tan(0.1 * x)
    return z

def function6(x,y):
    "z = sin(sqrt(5) + x) * y"
    z = sin(sqrt(5) + x) * y
    return z
