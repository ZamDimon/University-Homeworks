from typing import Callable

# Some math-related imports
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve


def solve_pde(
    n: int, 
    a: float, 
    b: float, 
    f_func: Callable[[np.ndarray], np.ndarray], 
    g_func: Callable[[np.ndarray], np.ndarray]
) -> np.ndarray:
    """
    Solves the PDE:
        Δu + f(x,y)*u = g(x,y)
    with boundary conditions:
        (∂u/∂n + u)|_{x=0, y=0} = 0
        u|_{x=a, y=b} = 0
        
    Parameters:
        n: number of interior points per axis (grid is (n+1)x(n+1))
        a, b: domain size in x and y
        f_func: function f(x, y)
        g_func: function g(x, y)
        
    Returns:
        u: (n+1)x(n+1) array with solution values on the grid
    """
    
    h_x = a / n # Grid size in x direction
    h_y = b / n # Grid size in y direction
    N = (n+1) ** 2  # Total number of points (including boundaries)
    
    A = lil_matrix((N, N)) # Sparse matrix for the system
    b_vec = np.zeros(N) # Right-hand side vector

    def idx(i: int, j: int) -> int:
        """
        Returns the flattened index for the 2D grid.
        """
        return i * (n + 1) + j

    for i in range(n+1):
        for j in range(n+1):
            x, y = i * h_x, j * h_y # Calculate the coordinates
            k = idx(i, j) # Flattened index for the matrix
            f_val = f_func(x, y)
            g_val = g_func(x, y)

            # Boundary for x=a or y=b
            if i == n or j == n:
                A[k, k] = 1.0
                b_vec[k] = 0.0

            # Boundary for x=0 or y=0
            elif i == 0 and j < n:
                kp = idx(i + 1, j)
                A[k, k] = 1 + h_x
                A[k, kp] = -1
                b_vec[k] = 0.0
            elif j == 0 and i < n:
                kp = idx(i, j + 1)
                A[k, k] = 1 + h_y
                A[k, kp] = -1
                b_vec[k] = 0.0

            # Now, the main part of the grid
            else:
                xm = idx(i - 1, j)
                xp = idx(i + 1, j)
                ym = idx(i, j - 1)
                yp = idx(i, j + 1)

                A[k, k] = -2 / h_x**2 - 2 / h_y**2 + f_val
                A[k, xm] = 1 / h_x**2
                A[k, xp] = 1 / h_x**2
                A[k, ym] = 1 / h_y**2
                A[k, yp] = 1 / h_y**2

                b_vec[k] = g_val

    u_flat = spsolve(A.tocsr(), b_vec)
    return u_flat.reshape((n + 1, n + 1))
