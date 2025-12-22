#Множина Мандельброта
import numpy as np
import matplotlib.pyplot as plt

def mandelbrot(xmin, xmax, Nx, ymin, ymax, Ny, steps=150):
    x = np.linspace(xmin,xmax,Nx)
    y = np.linspace(ymin,ymax,Ny)
    c = x[np.newaxis,:] + 1j*y[:,np.newaxis]
    z = c
    image = np.zeros((Nx, Ny)) 
    
    for k in range(steps):
        z = z*z + c
        mask = (np.abs(z) > 2) 
        image[mask] = k + 5
        z[mask] = np.nan
    return image[::-1,:] 
      
fig, ax = plt.subplots()
ax.set_aspect('equal')
# ax.grid()#сітка

N = 2000
#xmin,xmax = -2.2,0.8
#ymin,ymax = -1.5,1.5

#xmin,xmax = -0.3, -0.2
#ymin,ymax = -0.75, -0.9

xmin,xmax = -0.22, -0.20
ymin,ymax = -0.80, -0.78

ax.imshow(mandelbrot(xmin,xmax,N,ymin,ymax,N), cmap='jet',interpolation='none',
          extent=[xmin,xmax,ymin,ymax])

plt.tight_layout()
fig.savefig('mandelbrot_2.jpg', dpi=1000)