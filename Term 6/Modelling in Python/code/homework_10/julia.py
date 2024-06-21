import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps

def julia(xmin, xmax, Nx, ymin, ymax, Ny, steps=150):
    x = np.linspace(xmin,xmax,Nx)
    y = np.linspace(ymin,ymax,Ny)
    z = x[np.newaxis,:] + 1j*y[:,np.newaxis]
    c = 0.12 + 1j*0.62
    image = np.zeros((Nx, Ny)) 
    M = max(2,abs(c))
    
    for k in range(steps):
        z = z*z + c
        mask = (np.abs(z) > M) 
        image[mask] = k + 5
        z[mask] = np.nan
    return image[::-1,:] 
      
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.grid()

N = 2000
xmin,xmax = -1.5,1.5
ymin,ymax = -1,1

jul = julia(xmin,xmax,N,ymin,ymax,N)
ax.imshow(jul, 
        cmap='flag', 
        interpolation='none',
        extent=[xmin,xmax,ymin,ymax])

plt.tight_layout()
fig.savefig(f'julia_3.jpg', dpi=1000)