import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from typing import List

# Rich logging
from rich import print
from rich.console import Console
from rich.table import Table

from solver import LeastSquaresSolver, Dataset

def _show_predictions(dataset: Dataset, solver: LeastSquaresSolver) -> None:
    """ Shows the predictions of the fitted polynomial

    Args:
        dataset (Dataset): A list of points
        solver (LeastSquaresSolver): A LeastSquaresSolver instance
    """
    
    # Initializing an instance of rich.Table to make an attractive table in the console
    console = Console()
    table = Table(title='Degree vs real values for a linear regression')
    table.add_column('x', justify='center', style='white')
    table.add_column('y', justify='center', style='green')
    table.add_column('f(x)', justify='center', style='blue')
    table.add_column('|y - f(x)|', justify='center', style='red')
    
    # Adding rows to the table
    for (x, y) in dataset:
        x_label = '{:.8f}'.format(x)
        y_label = '{:.8f}'.format(y)
        prediction_label = '{:.8f}'.format(float(solver.predict(x)))
        difference_label = '{:.8f}'.format(np.abs(y - solver.predict(x)))
        
        table.add_row(x_label, y_label, prediction_label, difference_label)
    
    console.print(table)

def _print_predicted_polynomial(coefficients: np.ndarray) -> None:
    """ Prints the predicted polynomial
    
    Args:
        coefficients (np.ndarray): A list of coefficients for the polynomial of the given degree (degree + 1)
    """
    
    # Initializing an instance of rich.Table to make an attractive table in the console
    console = Console()
    table = Table(title='Predicted polynomial')
    table.add_column('Degree', justify='center', style='white')
    table.add_column('Coefficient', justify='center', style='green')
    
    # Adding rows to the table
    for i, coefficient in enumerate(coefficients):
        degree_label = f'x^{i}'
        coefficient_label = '{:.4f}'.format(float(coefficient))
        
        table.add_row(degree_label, coefficient_label)
    
    console.print(table)

def _show_plot(dataset: Dataset, solver: LeastSquaresSolver) -> None:
    """ Shows a plot of the dataset and the fitted polynomial
    
    Args:
        dataset (Dataset): A list of points
        solver (LeastSquaresSolver): A LeastSquaresSolver instance
    """
    
    # Finding a range of values for x
    min_x = min([point[0] for point in dataset])
    max_x = max([point[0] for point in dataset])
    
    # Drawing the plot
    t = np.arange(min_x, max_x, 0.01)
    _, ax = plt.subplots()
    ax.grid()
    ax.scatter([point[0] for point in dataset], [point[1] for point in dataset], marker='x', color='red')
    ax.plot(t, [solver.predict(x) for x in t], color='blue')
    plt.tight_layout()
    plt.savefig('images/plot.png', dpi=300)
    plt.show()
    
def _show_plot_of_different_degrees(dataset: Dataset) -> None:
    """ Shows a plot of the dataset and the fitted polynomial of different degrees
    
    Args:
        dataset (Dataset): A list of points
    """
    
    # Finding a range of values for x
    min_x = min([point[0] for point in dataset])
    max_x = max([point[0] for point in dataset])
    
    # Fitting the dataset with different degrees
    solvers = [LeastSquaresSolver(degree=i) for i in range(1, 8)]
    for solver in solvers:
        solver.fit(dataset)
    
    # Drawing the plot
    t = np.arange(min_x, max_x, 0.01)
    colors = ['cornflowerblue', 'royalblue', 'blue', 'mediumblue', 'darkblue', 'navy', 'midnightblue']
    
    _, ax = plt.subplots()
    ax.grid()
    
    handles: List[mpatches.Patch] = []
    ax.scatter([point[0] for point in dataset], [point[1] for point in dataset], marker='x', color='red')
    for solver, color in zip(solvers, colors):
        ax.plot(t, [solver.predict(x) for x in t], color=color)
        handles.append(mpatches.Patch(color=color, label=f'Degree {solver._degree}'))
    ax.legend(handles=handles)
    plt.tight_layout()
    plt.savefig('images/degrees.png', dpi=300)
    plt.show()

def _estimate_relative_error(dataset: Dataset, solver: LeastSquaresSolver) -> np.floating:
    """ Estimates the relative error of the fitted polynomial

    Args:
        dataset (Dataset): A list of points
        solver (LeastSquaresSolver): A LeastSquaresSolver instance

    Returns:
        np.floating: Relative error
    """
    # Set of y real values
    y = np.array([point[1] for point in dataset])
    # Set of y predicted values
    y_hat = np.array([solver.predict(point[0]) for point in dataset])
    
    return np.linalg.norm(y - y_hat) / np.linalg.norm(y)

if __name__ == '__main__':
    dataset = [
        (0.8, 1.97),
        (1.2, 3.53),
        (1.6, 3.57),
        (2.0, 2.42),
        (2.4, 2.44),
        (2.8, 1.30),
        (3.2, 0.71),
        (3.6, 2.12),
        (4.0, 3.08),
        (4.4, 5.99)
    ]
    
    # Using Least Squares Solver to find the coefficients of the polynomial
    solver = LeastSquaresSolver(degree=3)
    coefficients = solver.fit(dataset)
    
    # Showing the plot of the dataset and the fitted polynomial of different degrees
    _show_plot_of_different_degrees(dataset)
    
    # Showing the predictions of the fitted polynomial
    _show_predictions(dataset, solver)
    
    # Showing the coefficients of the fitted polynomial
    _print_predicted_polynomial(coefficients)
    
    # Showing the plot with the dataset and the fitted polynomial
    _show_plot(dataset, solver)
    
    # Estimating the relative error of the fitted polynomial
    relative_error = _estimate_relative_error(dataset, solver)
    print('Relative error: {:.4f}'.format(float(relative_error)))