import numpy as np
import matplotlib.pyplot as plt
from typing import Callable

def plot_vector_field(field: Callable[[float, float], [float, float]], file_name='portrait.png') -> None:
    """
    Plots the vector field of a given function.
    """
    
    # Defining the matplotlib figure and axis.
    fig = plt.figure(figsize=(14, 7))
    ax = fig.add_subplot()
    
    # Turn grid on for both major and minor ticks and style minor slightly
    # differently.
    ax.grid()
    ax.set_aspect('equal')

    x = np.linspace(-2.15*np.pi, 2.15*np.pi, 100)  
    y = np.linspace(-1.15*np.pi, 1.15*np.pi, 100)  
    xx, yy = np.meshgrid(x, y)

    f1,f2 = field(xx,yy)	
    ax.streamplot(xx, yy, f1, f2, density=1.8, color='b')
    
    # Set high DPI
    fig.set_dpi(300)
    fig.savefig(file_name)

if __name__ == '__main__':
    def f(omega, k):
        return lambda x1, x2: (x2, -omega**2*np.sin(x1) - k*x2)

    omega = 1.25
    for n in [0.4, 1, 2, 3]:
        plot_vector_field(f(omega, n*omega), f'with_friction_{n}.png')