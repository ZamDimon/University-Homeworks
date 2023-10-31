import numpy as np

def tridiagonal_matrix_algorithm(
    l: np.ndarray, 
    u: np.ndarray, 
    d: np.ndarray, 
    b: np.ndarray
) -> np.ndarray:
    """
    Solve a system of linear equations with the tridiagonal matrix algorithm.

    ### Args:
        l (List[float]): Lower diagonal
        u (List[float]): Upper diagonal
        d (List[float]): Main diagonal
        b (List[float]): Right hand side

    ### Returns:
        List[float]: Solution to the system of linear equations
    """
    
    assert len(l) == len(u) == len(d) - 1 == len(b) - 1, "Invalid input shapes"
    
    l = np.insert(l, 0, 0.0, axis=0) # Add zero to the beginning of the list
    u = np.append(u, 0.0) # Add zero to the end of the list
    n = len(d) # Number of equations
     
    # Forward substitution
    alpha, beta = np.zeros(n), np.zeros(n)
    for i in range(n):
        alpha[i] = -u[i] / (l[i] * alpha[i-1] + d[i])
        beta[i] = (b[i] - l[i] * beta[i-1]) / (l[i] * alpha[i-1] + d[i])
      
    # Backward substitution
    x = np.zeros(n) # Defining a solution
    x[n-1] = beta[n-1]
    for i in range(n-2, -1, -1):
        x[i] = alpha[i] * x[i+1] + beta[i]
        
    return x