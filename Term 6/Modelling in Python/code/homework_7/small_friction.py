import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def f(_, x):
    """
    Returns the derivative of the state vector.
    """
    
    x1, x2 = x
    y1 = x2
    thetas = x2 < v0
    y2 = -omega**2*x1 + mu*g*thetas
    return y1, y2

def draw_trajectory(ax, x_0: float, y_0: float, color='red', alpha=1.0):
    """
    Draws the trajectory of a given initial condition.
    """
    
    x0 = [x_0, y_0]
    dt = 0.05
    T = 15.0
    t = np.arange(0, T, dt)
    res = solve_ivp(f, [0, T], x0, dense_output=True)
    x = res.sol(t)
    ax.plot(x[0], x[1], linewidth=2.5, color=color, alpha=alpha)
    ax.plot(x0[0], x0[1], color=color, marker='o', alpha=alpha)
    
def draw_ellipse(ax, x: float, y: float, a: float, b: float, color='black'):
    """
    Draws an ellipse with the given parameters.
    """
    
    t = np.linspace(0, 2*np.pi, 100)
    ax.plot(x + a*np.cos(t), y + b*np.sin(t), linewidth=2.0, color=color, linestyle='dashed')

def draw_streamplot(ax, a_min: float, a_max: float, b_min: float, b_max: float, x0: float, f: callable):
    """
    Draws the streamplot of a given vector field.
    """
    
    x1 = np.linspace(a_min, a_max, 31)  
    x2 = np.linspace(b_min, b_max, 31)  
    xx1, xx2 = np.meshgrid(x1, x2)
    ff1, ff2 = f(0, [xx1, xx2])
    ax.streamplot(xx1, xx2, ff1, ff2, color='gray', density=1.8, linewidth=1)
    ax.plot(x0, 0, color='red', marker='o', alpha=1.0)
    #ax.plot(-x0, 0, color='red', marker='o', alpha=1.0)
    ax.streamplot(xx1, xx2, ff1, ff2, color='gray', density=1.8, linewidth=1)

if __name__ == '__main__':
    # Constants
    omega = 2.0
    mu = 0.1
    g = 9.81
    v0 = 1.1
    x0 = mu * g / omega**2
    
    # Setting limits
    a_min, a_max = -8*x0 if v0 > 0 else 8*x0, -8*x0 if v0 < 0 else 10*x0
    b_min, b_max = -4, 4

    # Setting parameters
    fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    ax.set_xlim([a_min, a_max])
    ax.set_ylim([b_min, b_max])
    plt.suptitle('Small friction (mu=0.1)')
    
    # Drawing trajectories
    draw_trajectory(ax, 2.0, 1.5, color='blue', alpha=1.0)
    draw_trajectory(ax, 0.5, 1.8, color='blue', alpha=0.6)
    draw_trajectory(ax, 2.0, 0.0, color='blue', alpha=0.3)
    
    # Drawing streamplot
    draw_streamplot(ax, a_min, a_max, b_min, b_max, x0, f)
    draw_ellipse(ax, x0, 0.0, v0/omega, v0, color='red')

    plt.savefig('small_friction.pdf')
