"""
Module implementing the 2nd-order Adams-Moulton method for solving ODEs.
"""

from typing import Callable, Tuple

import numpy as np
import matplotlib.pyplot as plt

def adams_moulton_2nd_order(
    f: Callable[[float, float], float],
    x0: float, 
    y0: float, 
    h: float, 
    n_steps: int
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Solves y' = f(t,y) using the 2nd-order Adams-Moulton method.
    
    Arguments:
        f: Function f(t, y)
        x0: Initial time
        y0: Initial value y(t0)
        h: Step size
        n_steps: Number of steps

    Returns:
        t_vals: Array of time values
        y_vals: Array of y values
    """
    
    x = np.zeros(n_steps + 1)
    y = np.zeros(n_steps + 1)

    x[0] = x0
    y[0] = y0

    for n in range(n_steps):
        # Predictor step
        y_predict = y[n] + h * f(x[n], y[n])

        # Corrector step
        y_corrected = y[n] + (h / 2) * (f(x[n], y[n]) + f(x[n] + h, y_predict))  # one iteration

        x[n + 1] = x[n] + h
        y[n + 1] = y_corrected

    return x, y


def rk4_step(f: Callable[[float, float], float], x: float, y: float, h: float) -> float:
    """
    Implements the 4th-order Runge-Kutta method for a single step.
    
    Arguments:
        f: Function f(t, y)
        x: Current time
        y: Current value y(t)
        h: Step size
        
    Returns:
        y_next: Value of y at the next time step
    """
    
    k1 = f(x, y)
    k2 = f(x + h/2, y + h*k1/2)
    k3 = f(x + h/2, y + h*k2/2)
    k4 = f(x + h, y + h*k3)
    return y + (h/6)*(k1 + 2*k2 + 2*k3 + k4)


def adams_moulton_hard(
    f: Callable[[float, float], float],
    x0: float, 
    y0: float, 
    h: float, 
    n_steps: int
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Solves y' = f(t,y) using the 2nd-order Adams-Moulton method.
    
    Arguments:
        f: Function f(t, y)
        x0: Initial time
        y0: Initial value y(t0)
        h: Step size
        n_steps: Number of steps

    Returns:
        t_vals: Array of time values
        y_vals: Array of y values
    """
    
    x = np.zeros(n_steps + 1)
    y = np.zeros(n_steps + 1)

    x[0] = x0
    y[0] = y0
    
    # Bootstrap using RK4
    for n in range(3):
        y[n + 1] = rk4_step(f, x[n], y[n], h)
        x[n + 1] = x[n] + h

    # Main loop
    for n in range(3, n_steps):
        # Predictor step
        y_predict = y[n] + (h/24)*(55*f(x[n],y[n]) - 59*f(x[n-1],y[n-1]) + 37*f(x[n-2],y[n-2]) - 9*f(x[n-3],y[n-3]))

        # Corrector step
        y_corrected = y[n] + (h/24)*(9*f(x[n]+h,y_predict) + 19*f(x[n],y[n]) - 5*f(x[n-1],y[n-1]) + f(x[n-2],y[n-2]))

        x[n + 1] = x[n] + h
        y[n + 1] = y_corrected

    return x, y


if __name__ == '__main__':
    # Example: y' = -2y^2*log(x) - y/x with y(1) = 1
    f = lambda x, y: -2*y**2*np.log(x)-y/x # Function from the problem statement
    r = lambda x: 1/(x*(1+np.log(x)**2))  # Exact solution for comparison
    x0, y0 = 1, 1 # Initial conditions
    x1 = 2 # Final x value
    n_steps = 6 # Number of steps

    x_vals, y_vals = adams_moulton_2nd_order(f, x0=x0, y0=y0, h=(x1-x0)/n_steps, n_steps=n_steps)
    x_vals_2, y_vals_2 = adams_moulton_hard(f, x0=x0, y0=y0, h=(x1-x0)/n_steps, n_steps=n_steps)
    print(x_vals_2, y_vals_2)
    
    plt.plot(x_vals, y_vals, label="Adams-Moulton", color='blue')
    plt.plot(x_vals_2, y_vals_2, label="Adams-Moulton Hard", color='green')
    plt.plot(x_vals, r(x_vals), '--', label="Exact", color='red')
    plt.legend()
    plt.xlabel("t")
    plt.ylabel("y")
    plt.title("Adams-Moulton Method (2nd-order)")
    plt.grid(True)
    plt.show()
