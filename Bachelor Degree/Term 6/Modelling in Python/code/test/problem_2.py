import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import random
from scipy.integrate import solve_ivp

if __name__ == '__main__':
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(polar=True)

    plt.xlim([0, 2*np.pi])  
    plt.ylim([0, 1.5])  

    def f(_t, x):
        return x[0]*(1-x[0]), np.sin(x[1])

    N = 1000
    T = 60
    t = np.linspace(0, T, N)

    POINTS_NUMBER = 50
    
    # Points inside r = 1
    for i, phi in enumerate(np.linspace(0, 2*np.pi, POINTS_NUMBER)):
        x0 = [0.5 + 0.5 * random.random(), phi]
        res = solve_ivp(f, [0, T], x0, dense_output=True)
        s = res.sol(t)
        
        # Drawing
        alpha = 0.5 + 0.5 * i / len(np.linspace(0, 2*np.pi, POINTS_NUMBER))
        ax.plot(s[1], s[0], color='blue', alpha=alpha)
        ax.plot(x0[1], x0[0], color='blue', marker='o', alpha=alpha)
    
    # Points outside r = 1
    for i, phi in enumerate(np.linspace(0, 2*np.pi, POINTS_NUMBER)):
        x0 = [1.0 + 0.75 * random.random(), phi]
        res = solve_ivp(f, [0, T], x0, dense_output=True)
        s = res.sol(t)
        
        # Drawing
        alpha = 0.5 + 0.5 * i / len(np.linspace(0, 2*np.pi, POINTS_NUMBER))
        ax.plot(s[1], s[0], color='green', alpha=alpha)
        ax.plot(x0[1], x0[0], color='green', marker='o', alpha=alpha)
    
    # Some customizations
    ax.set_rmax(1.5)
    ax.set_rticks([0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2.0])  # Less radial ticks
    ax.grid(True)
    ax.plot(np.linspace(0, 2*np.pi, N), np.ones(N), color='red', linestyle='dashed')
    mpl.rcParams['figure.dpi'] = 600 
    ax.set_title("Problem 2 Phase Portrait", va='bottom') 
    plt.savefig('problem_2.pdf')    