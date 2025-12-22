import numpy as np
import matplotlib.pyplot as plt

from solver import solve_fredholm

if __name__ == "__main__":
    # Problem parameters
    a, b = 0.0, 1.0
    n = 20 # Number of grid points
    f_func = lambda x: np.sqrt(1 + x**2)
    kernel = lambda x, y: np.cos(0.5 * x * y)
    
    # Solve the Fredholm integral equation
    y_solution = solve_fredholm(n, a, b, kernel, f_func)
    
    # Plot the solution
    x_vals = np.linspace(a, b, n)
    y_vals = np.array([y_solution(x_vals[i]) for i in range(n)], dtype=np.float64)
    
    plt.plot(x_vals, y_vals, label="Numerical Solution", color='blue', linewidth=3)
    plt.title("Solution to the Fredholm Integral Equation")
    plt.xlabel("x")
    plt.ylabel("y(x)")
    plt.legend()
    plt.grid()
    plt.savefig("fredholm_solution.pdf", dpi=300)
    plt.show()
    