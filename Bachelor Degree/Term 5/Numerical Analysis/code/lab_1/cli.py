# Math imports
from math import exp, sin, cos

# Internal imports
from generators import IDataPointsGenerator, LinearDataPointsGenerator, CosineDataPointsGenerator
from polynomials import LagrangePolynomial, NewtonForwardPolynomial, NewtonBackwardsPolynomial

# Rich logging
from rich.console import Console
from rich.table import Table

if __name__ == "__main__":
    # Defining the task parameters
    interval = (-2.0, 2.0)
    segments_number = 3
    alpha = 0.1
    fn = lambda x: exp(x / 10.0) * sin(x) + x**3 + cos(x)
    
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
        
        # Defining the polynomials
        polynomials = {
            "Lagrange Polynomial": LagrangePolynomial(node_points),
            "Newton Forward Polynomial": NewtonForwardPolynomial(node_points),
            "Newton Backwards Polynomial": NewtonBackwardsPolynomial(node_points)
        }
        
        # Defining the test points
        test_x = generator.generate_test_points(alpha=alpha)
        test_points = [(x, fn(x)) for x in test_x]
        
        for polynomial_name, polynomial in polynomials.items():
            table = Table(title=f"{polynomial_name} evaluation using {generator_name}")
            table.add_column("x", justify="center", style="cyan", no_wrap=True)
            table.add_column("f(x)", justify="center", style="magenta")
            table.add_column("P(x)", justify="center", style="green")
            table.add_column("|f(x)-P(x)|", justify="center", style="blue")
        
            for test_point in test_points:
                x_label = "{:.18f}".format(test_point[0])
                f_x_label = "{:.18f}".format(test_point[1])
                p_x_label = "{:.18f}".format(polynomial.evaluate(test_point[0]))
                difference_label = "{:.18f}".format(abs(test_point[1] - polynomial.evaluate(test_point[0])))
                
                table.add_row(x_label, f_x_label, p_x_label, difference_label)

            console.print(table)
