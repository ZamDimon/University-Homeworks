import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    omega = 1.25

    for k in [0.01, 0.1, 0.3, 0.6, 1.0, 1.5, 2.0, 3.0, 5.0]:
        def f(x,y):
            return y, -omega**2*np.sin(x) - k*y
        
        fig = plt.figure(figsize=(10,5))
        ax = fig.add_subplot()
        ax.grid()
        ax.set_aspect('equal')

        x = np.linspace(-2*np.pi,2*np.pi,50)  
        y = np.linspace(-3,3,50)  
        xx, yy = np.meshgrid(x,y)

        f1,f2 = f(xx,yy)	
        ax.streamplot(xx,yy,f1,f2,density=1.8)
        
        fig.savefig(f'phase_{k}.png')
    