# Math imports
from math import exp, sin, cos
import numpy as np

# Internal imports
from generators import Interval, IDataPointsGenerator, LinearDataPointsGenerator, CosineDataPointsGenerator
from spline import CubicSpline

# Rich logging
from rich.console import Console
from rich.table import Table

import matplotlib.pyplot as plt
from typing import Callable

def plot_polynomial(
    fn: Callable[[float], float],
    interval: Interval,
    segments_number: int = 2,
) -> None:
    """
    Plots the polynomial and the spline on the same plot
    
    ### Args:
    - fn (`Callable[[float], float]`): Function to plot
    - interval (`Interval`): Interval on which to plot the polynomial
    - segments_number (`int`): Number of segments to use for the spline
    
    ### Returns:
    Displayed polynomial and spline
    """
    
    # Defining the spline
    generator = LinearDataPointsGenerator(interval, segments_number)
    node_x = generator.generate_nodes()
    node_points = [(x, fn(x)) for x in node_x]
    spline = CubicSpline(node_points)
    
    x = np.arange(*interval, 0.02)
    plt.figure()
    plt.subplot(211)
    plt.plot(x, [fn(x) for x in x], 'b', x, [spline.evaluate(x) for x in x], 'r--')
    plt.show()

def evaluate_accuracy(
    fn: Callable[[float], float],
    interval: Interval,
    segments_number: int = 20,
    alpha: float = 0.2,
) -> None:
    """Evaluates the accuracy of the spline

    ### Args:
    - fn (Callable[[float], float]): Function to interpolate
    - interval (`Interval`): Interval on which to plot the polynomial
    - segments_number (int, optional): _description_. Defaults to 20.
    - alpha (float, optional): Alpha parameter for the test points. Defaults to 0.2.
    """
    
    # Defining the generator and defining a set of points
    generators: dict[str, IDataPointsGenerator] = {
        "linear generation": LinearDataPointsGenerator(interval, segments_number),
        "cosine generation": CosineDataPointsGenerator(interval, segments_number)
    }
    
    # For rich logging
    console = Console()
    
    for generator_name, generator in generators.items():
        # Defining the points on which to interpolate the polynomial
        node_x = generator.generate_nodes()
        node_points = [(x, fn(x)) for x in node_x]
        
        # Defining the spline
        spline = CubicSpline(node_points)
        
        # Defining the test points
        test_x = generator.generate_test_points(alpha=alpha)
        test_points = [(x, fn(x)) for x in test_x]
        
        table = Table(title=f"Spline evaluation using {generator_name}")
        table.add_column("x", justify="center", style="cyan", no_wrap=True)
        table.add_column("f(x)", justify="center", style="magenta")
        table.add_column("S(x)", justify="center", style="green")
        table.add_column("|f(x)-S(x)|", justify="center", style="blue")
    
        for test_point in test_points[:-1]:
            x_label = "{:.18f}".format(test_point[0])
            f_x_label = "{:.18f}".format(test_point[1])
            p_x_label = "{:.18f}".format(spline.evaluate(test_point[0]))
            difference_label = "{:.18f}".format(abs(test_point[1] - spline.evaluate(test_point[0])))
            
            table.add_row(x_label, f_x_label, p_x_label, difference_label)

        console.print(table)

if __name__ == "__main__":
    # Defining the task parameters
    interval = (0.0, 1.0)
    segments_number = 20
    alpha = 0.0
    fn = lambda x: x**3 + cos(x) + exp(x / 10.0) * sin(x)
    
    # Evaluating the accuracy
    evaluate_accuracy(fn, interval, segments_number=segments_number, alpha=alpha)
    
    # Plotting the polynomial
    plot_polynomial(fn, interval, segments_number=3)
    
    