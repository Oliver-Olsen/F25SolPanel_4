def solar_elevation_angle(theta):
    
    
    return theta


import numpy as np
import sympy as sym
import matplotlib.pyplot as plt
figurstr = (15, 7)

t = np.linspace(0, 2 * np.pi, 1000)
f = np.cos(t)

plt.figure(figsize=figurstr)
plt.plot(t, f, color='b', linestyle='-')
plt.xlabel('t')
plt.ylabel('cos(t)')
plt.show()

#print(t,f)  # uncomment to see the values of t and f

idx1 = (f <= 0.05)
idx2 = (f >= -0.05)
print(idx1)
print(idx2)
print(idx1 == idx2)
print(f[idx1 == idx2])
print(t[idx1 == idx2])

#fioerhgiuehniur

