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


def find_nul(t,f):
    current = np.sign(f[0])
    result = []
    for idx,i in enumerate(f[1::]):
        if np.sign(i) != current:
            current = np.sign(i)
            result.append([t[1::][idx-1],t[1::][idx]])
    return result

    
print(find_nul(t,f))