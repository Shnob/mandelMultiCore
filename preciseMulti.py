import numpy as np
from random import random

lim = 1000

z = np.complex128((0, 0))
c = np.complex128((-0.7499999999999999999999999999999999999999, 0))#(random(), random()))

for i in range(lim):
    z = z**2 + c

print(z)