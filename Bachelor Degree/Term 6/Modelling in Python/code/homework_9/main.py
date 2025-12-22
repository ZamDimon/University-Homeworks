import numpy as np
import matplotlib.pyplot as plt

def stationary_points() -> None:
    c = -0.2

    f = lambda x: x**2 + c
    
    fig, ax = plt.subplots()
    ax.set_aspect('equal', 'box')
    ax.grid()

    x = np.linspace(-1.1, 1.1, 100)
    ax.plot(x, f(x), linestyle='dashed', color='gray')
    ax.plot([-3, 3], [-3, 3], linestyle='dashed', color='gray')
    ax.set_xlim(-1, 1)
    ax.set_ylim(c - 0.1, 1)
    plt.axvline(x = (1 - np.sqrt(1 - 4*c)) / 2, linestyle='dashed', color = 'green', label = 'axvline - full height')

    x = 0.8
    y = f(x)

    for _ in range(1,100):
        z = f(y)
        ax.plot([x,y,y], [y,y,z], color='b', alpha=0.8)
        x, y = y, z
        
    plt.savefig('1.pdf')
    
def cycle_length_two() -> None:
    c = -0.85
    f = lambda x: x**2 + c
    
    fig, ax = plt.subplots()
    ax.set_aspect('equal', 'box')
    ax.grid()

    x = np.linspace(-1.1, 1.1, 100)
    ax.plot([-3, 3], [-3, 3], linestyle='dashed', color='black', alpha=0.3)
    ax.plot(x, f(x), linestyle='dashed', color='black', alpha=0.3)
    ax.plot(x, f(f(x)), linestyle='dashed', color='black')
    ax.set_xlim(-1, 1)
    ax.set_ylim(c - 0.1, 1)
    plt.axvline(x = (-1-np.sqrt(-3-4*c))/2.0, linestyle='dashed', color = 'green', label = 'axvline - full height')
    plt.axvline(x = (-1+np.sqrt(-3-4*c))/2.0, linestyle='dashed', color = 'green', label = 'axvline - full height')

    x = -0.35
    y = f(x)

    # Skipping first 100 iterations
    for _ in range(1,100):
        z = f(y)
        x, y = y, z
    
    for _ in range(1,100):
        z = f(y)
        ax.plot([x,y,y], [y,y,z], color='b', alpha=0.8)
        x, y = y, z
        
    plt.savefig('2.pdf')
    
def cool_picture() -> None:
    c = -1.87

    f = lambda x: x**2 + c
    
    fig, ax = plt.subplots()
    ax.set_aspect('equal', 'box')
    ax.grid()

    x = np.linspace(-2.1, 2.1, 100)
    ax.plot([-3, 3], [-3, 3], linestyle='dashed', color='black', alpha=0.3)
    ax.plot(x, f(x), linestyle='dashed', color='black', alpha=0.3)
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2.1, 2.1)

    x = 0.8
    y = f(x)
    
    for _ in range(1,100):
        z = f(y)
        ax.plot([x,y,y], [y,y,z], color='b', alpha=0.8)
        x, y = y, z
        
    plt.savefig('3.pdf')
    
def bifurcation_diagram() -> None:
    N0 = 200
    N = 300
    P = 5000
    a, b = -2, 0.25
    
    def f(c, x):
        return x**2 + c
    
    fig, ax = plt.subplots()
    ax.grid()
    r = np.linspace(a, b, P)
    x = 0.5 * np.ones((P,))
    
    for _ in range(N0) :
        x = f(r, x)
        
    for _ in range(N):
        x = f(r, x)
        ax.plot(r, x, marker ='o', markersize=0.01, color ='blue', linestyle='None')
        
    plt.savefig('4.png', dpi=1000)
    
if __name__ == '__main__':
    # stationary_points()
    # cycle_length_two()
    # cool_picture()
    bifurcation_diagram()