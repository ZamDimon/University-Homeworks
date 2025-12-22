import numpy as np
import matplotlib.pyplot as plt

from typing import Callable, Tuple, List

def gen_streamplot_params(f: Callable[[float], callable], mu: float = 1.0) -> List[np.ndarray]:
    """
    Based on the vector field parameterization function and mu parameter provided, 
    generates the meshgrid and vector field needed to build the streamplot.
    
    Args:
    - `f` - the vector field function parameterization. Returns the callable vector field function
    based on the mu parameter provided.
    - `mu` - the mu parameter in the system of ODEs
    
    Output:
    - `[xx, yy, f1, f2]` - a list of numpy arrays needed to build the streamplot (x, y) coordinates
    and the corresponding vector field (f1, f2)
    """

    x = np.linspace(-3.0, 3.0, 50)  
    y = np.linspace(-3.0, 2.0, 50)  
    xx, yy = np.meshgrid(x,y)
    f = f(mu) # Choosing correct vector field function based on mu
    f1, f2 = f(xx,yy)
    return [xx, yy, f1, f2]

def draw_streamplot(ax: plt.axes, 
                    f: callable, 
                    stationary_points: List[Tuple[float, float]] = [], 
                    mu: float = 1.0) -> None:
    """
    Draws a streamplot on the provided axes based on the mu parameter and vector field provided.
    
    Args:
    - `ax` - the axes object to draw the streamplot on
    - `f` - the vector field function
    - `stationary_points` - a list of stationary points to be marked on the plot. Empty by default.
    - `mu` - the mu parameter in the system of ODEs
    
    Output:
    `None`, modifies the provided ax
    """
    
    # Some fancy customizations
    ax.set_aspect('equal')
    ax.grid()
    ax.set_title(f'mu = {mu}')
    
    # Drawing the streamplot
    xx, yy, f1, f2 = gen_streamplot_params(f, mu=mu)
    ax.streamplot(xx, yy, f1, f2, density=1.8, color='b')
    
    # Drawing the stationary points
    for point in stationary_points:
        ax.scatter(point[0], point[1], color='red', marker='x', alpha=1.0, s=100, linewidths=3.0, zorder=10)
    

if __name__ == '__main__':
    # Defining the vector field function for problem (a)
    def fn_problem_a(mu: float) -> callable:
        def fn(x: np.ndarray, y: np.ndarray) -> np.ndarray:
            return mu*x - x**2, y
        
        return fn
    
    # Defining the vector field function for problem (b)
    def fn_problem_b(mu: float) -> callable:
        def fn(x: np.ndarray, y: np.ndarray) -> np.ndarray:
            return mu - x**2, y
        
        return fn
    
    # Plotting problem (a)
    fig, axs = plt.subplots(2, 2)
    fig.set_figheight(10)
    fig.set_figwidth(10)
    
    draw_streamplot(axs[0, 0], fn_problem_a, stationary_points=[(-1.0, 0.0), (0.0, 0.0)], mu=-1.0)
    draw_streamplot(axs[0, 1], fn_problem_a, stationary_points=[(0.0, 0.0)], mu=0.0)
    draw_streamplot(axs[1, 0], fn_problem_a, stationary_points=[(1.0, 0.0), (0.0, 0.0)], mu=1.0)
    draw_streamplot(axs[1, 1], fn_problem_a, stationary_points=[(2.0, 0.0), (0.0, 0.0)], mu=2.0)
    fig.savefig(f'problem_1a.pdf')
    
    # Plotting problem (b)
    fig, axs = plt.subplots(2, 2)
    fig.set_figheight(10)
    fig.set_figwidth(10)
    
    draw_streamplot(axs[0, 0], fn_problem_b, mu=-1.0)
    draw_streamplot(axs[0, 1], fn_problem_b, stationary_points=[(0.0, 0.0)], mu=0.0)
    draw_streamplot(axs[1, 0], fn_problem_b, stationary_points=[(-1.0, 0.0), (1.0, 0.0)], mu=1.0)
    draw_streamplot(axs[1, 1], fn_problem_b, stationary_points=[(-np.sqrt(2.0), 0.0), (np.sqrt(2.0), 0.0)], mu=2.0)
    fig.savefig(f'problem_1b.pdf')
    