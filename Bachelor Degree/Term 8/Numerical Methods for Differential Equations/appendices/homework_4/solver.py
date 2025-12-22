from typing import Callable

# Some math-related imports
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve


def solve_fredholm(
    n: int, 
    a: float, 
    b: float, 
    kernel: Callable[[np.ndarray, np.ndarray], np.ndarray],
    f_func: Callable[[np.ndarray], np.ndarray],
) -> Callable[[np.ndarray], np.ndarray]:
    """
    Solves the Fredholm integral equation of the second kind:
    ```
    y(x) = ∫_a^b K(x,ξ)y(ξ)dξ + f(x), x ∈ [a, b]
    ```
    Args:
        n: Number 
        a, b: Domain size in x
        kernel: Kernel function K(x, ξ)
        f_func: Function f(x)
    """
    
    h = (b - a) / n  # Step size
    xs = np.linspace(a, b, n+1)  # Grid points
    
    weights = h * np.ones(n+1)  # Coefficients for the integral trapezoid approximation
    weights[0] = weights[n] = 0.5 * h # Trapezoidal rule for endpoints
    
    b = np.zeros(n+1) # Initialize the solution vector
    M = np.zeros((n+1, n+1)) # Coefficient matrix
    
    # Now, we fill the matrix A and the vector v
    for i in range(n+1):
        b[i] = f_func(xs[i]) # Free term is easy to compute
        
        for j in range(n+1):
            delta = 1.0 if i == j else 0.0
            M[i,j] = delta - kernel(xs[i], xs[j]) * weights[j]

    v = np.linalg.solve(M, b) # Solve the linear system
    
    def resultant_fn(x: np.ndarray) -> np.ndarray:
        """
        Returns the resultant function y(x).
        """
    
        return f_func(x) + np.sum(weights * kernel(xs, x) * v)
    
    return resultant_fn