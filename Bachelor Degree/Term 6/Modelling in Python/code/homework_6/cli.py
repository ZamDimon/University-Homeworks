import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

if __name__ == '__main__':
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(polar=True)

    plt.xlim([0, 2*np.pi])  
    plt.ylim([0, 4])  

    def f(t, x):
        return x[0]*(1-x[0])*(x[0]-2)*(x[0]-3)**2/15, 1

    N = 1000
    T = 60
    t = np.linspace(0, T, N)

    # Point inside r = 1
    x0 = [0.8, np.pi/4]
    res = solve_ivp(f, [0, T], x0, dense_output=True)
    s = res.sol(t)
    ax.plot(s[1], s[0], color='blue', alpha=1.0)
    ax.plot(x0[1], x0[0], color='blue', marker='o', alpha=1.0)

    # Point inside r = 2 but outside r = 1
    x0 = [1.35, np.pi/4]
    res = solve_ivp(f, [0, T], x0, dense_output=True)
    s = res.sol(t)
    ax.plot(s[1], s[0], color='blue', alpha=0.8)
    ax.plot(x0[1], x0[0], 'blue', marker='o', alpha=0.8)
    
    # Point outside r = 2 but inside r = 3
    x0 = [2.5, np.pi/4]
    res = solve_ivp(f, [0, T], x0, dense_output=True)
    s = res.sol(t)
    ax.plot(s[1], s[0], color='blue', alpha = 0.6)
    ax.plot(x0[1], x0[0], 'blue', marker='o', alpha=0.6)
    
    # Point outside r = 3
    x0 = [3.5, np.pi/4]
    res = solve_ivp(f, [0, T], x0, dense_output=True)
    s = res.sol(t)
    ax.plot(s[1], s[0], color='blue', alpha=0.4)
    ax.plot(x0[1], x0[0], 'blue', marker='o', alpha=0.4)
    
    # Some customizations
    ax.set_rmax(4)
    ax.set_rticks([0.5, 1, 1.5, 2, 2.5, 3.0, 3.5, 4.0])  # Less radial ticks
    ax.grid(True)
    ax.plot(np.linspace(0, 2*np.pi, N), np.ones(N), color='red', linestyle='dashed')
    ax.plot(np.linspace(0, 2*np.pi, N), 2*np.ones(N), color='red', linestyle='dashed')
    ax.plot(np.linspace(0, 2*np.pi, N), 3*np.ones(N), color='red', linestyle='dashed')
    mpl.rcParams['figure.dpi'] = 600 
    ax.set_title("Problem 3 Phase Portrait", va='bottom') 
    plt.savefig('problem_3.pdf')    