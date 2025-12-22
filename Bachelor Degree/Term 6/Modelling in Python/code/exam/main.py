import numpy as np
import matplotlib.pyplot as plt

from typing import Tuple, List

def draw_streamplot(ax: plt.axes, 
                    title: str,
                    f: callable, 
                    stationary_points: List[Tuple[float, float]] = [],
                    normal_vectors: np.ndarray = None) -> None:
    """
    Draws a streamplot on the provided axes based on the vector field provided.
    
    Args:
    - `ax` - the axes object to draw the streamplot on
    - `title` - title of the plot
    - `f` - the vector field function
    - `stationary_points` - a list of stationary points to be marked on the plot. Empty by default.
    
    Output:
    `None`, modifies the provided ax
    """
    
    # Some fancy customizations
    ax.set_aspect('equal')
    ax.grid()
    ax.set_title(title)
    
    # Drawing the streamplot
    x = np.linspace(-3.0, 3.0, 50) # Choosing the range of x 
    y = np.linspace(-3.0, 3.0, 50) # Choosing the range of y
    xx, yy = np.meshgrid(x,y) # Creating a meshgrid
    f1, f2 = f(xx,yy) # Calculating the vector field
    ax.streamplot(xx, yy, f1, f2, density=1.8, color='b') # Drawing a phase portrait
    
    if normal_vectors is not None:
        x = np.linspace(-1.5, 1.5, 50) # Choosing the range of x 
        for normal_vector in normal_vectors:
            slope = normal_vector[0,0] / normal_vector[0,1]
            intercept = 0.0
            ax.plot(x, slope * x + intercept, color='red', linestyle='dashed')
    
    # Drawing the stationary points
    for point in stationary_points:
        ax.scatter(point[0], point[1], color='red', marker='x', alpha=1.0, s=100, linewidths=3.0, zorder=10)
    

if __name__ == '__main__':
    # Define a matrix that will be used to make the matrix of the
    # linear system less obvious by taking A^{-1}diag(lambda_1, lambda_2)A
    # Here, this is just a rotational matrix by pi/6
    A = np.matrix([[np.cos(np.pi/6), -np.sin(np.pi/6)], [np.sin(np.pi/6), np.cos(np.pi/6)]]) 
    A_inv = np.linalg.inv(A)
    
    # Defining the vector field functions for each of the cases
    def stable_node(x: np.ndarray, y: np.ndarray) -> callable:
        # Here, both eigenvalues are negative
        lambda_1 = -1
        lambda_2 = -1.5
        matrix = A_inv @ np.matrix([[lambda_1, 0], [0, lambda_2]]) @ A
        return matrix[0, 0] * x + matrix[0, 1] * y, matrix[1, 0] * x + matrix[1, 1] * y
    
    def saddle(x: np.ndarray, y: np.ndarray) -> callable:
        # Here, one eigenvalue is negative and one is positive
        lambda_1 = -1.0
        lambda_2 = 4.0
        matrix = A_inv @ np.matrix([[lambda_1, 0], [0, lambda_2]]) @ A
        return matrix[0, 0] * x + matrix[0, 1] * y, matrix[1, 0] * x + matrix[1, 1] * y
    
    def center(x: np.ndarray, y: np.ndarray) -> callable:
        # Here, both eigenvalues are pure complex
        v = 4.0
        matrix = A_inv @ np.matrix([[0, v], [-v, 0]]) @ A
        return matrix[0, 0] * x + matrix[0, 1] * y, matrix[1, 0] * x + matrix[1, 1] * y
    
    def unstable_focus(x: np.ndarray, y: np.ndarray) -> callable:
        # Here, both eigenvalues are complex with positive real part
        u = 3.0
        v = 6.0
        matrix = A_inv @ np.matrix([[u, v], [-v, u]]) @ A
        return matrix[0, 0] * x + matrix[0, 1] * y, matrix[1, 0] * x + matrix[1, 1] * y
    
    # Plotting all phase portraits
    fig, axs = plt.subplots(1, 1)
    fig.set_figheight(10)
    fig.set_figwidth(10)
    
    # Modifying subplots
    #draw_streamplot(axs[0, 0], 'Stable node\n(λ1=-1.0, λ2=-1.5)', stable_node, stationary_points=[(0.0, 0.0)])
    draw_streamplot(axs, 'Saddle point\n(λ1=-1.0, λ2=4.0)', saddle, normal_vectors=[A @ np.array([0.0, 1.0]), A @ np.array([1.0, 0.0])], stationary_points=[(0.0, 0.0)])
    #draw_streamplot(axs[1, 0], 'Center\n(λ1=4.0i, λ2=-4.0i)', center, stationary_points=[(0.0, 0.0)])
    #draw_streamplot(axs[1, 1], 'Focus\n(λ1=3.0+6.0i, λ2=3.0-6.0i)', unstable_focus, stationary_points=[(0.0, 0.0)])
    
    # Saving the figure
    fig.savefig(f'exam_problem_2_2.pdf')
    