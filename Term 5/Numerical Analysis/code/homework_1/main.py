# Some packages for decoration
import typing
from typing import Any
from collections.abc import Callable

# Math packages
import math
import scipy
import sympy as sym

from rich import print # Just for better printing

# Include package from the subdirectory
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import utils.logger as my_logger

def get_lagrange_product(interpolation_points: list[float], term_id: int, x: Any, verbose=True) -> Any:
    """
    Finds the product (x - x_j) / (x_i - x_j) for all j != i.
    """
    # Find the number of interpolation points
    n = len(interpolation_points)
    # Defining result
    result = None

    # Ranging over all n expect for term_id
    terms = [(x - interpolation_points[i]) / (interpolation_points[term_id] - interpolation_points[i]) for i in range(n) if i != term_id]

    # Finding a product
    result = sym.Mul(*terms)

    # Printing all terms if in verbose mode
    if verbose:
        my_logger.print_list_rich_with_result(terms, result, term_prefix="Product term")

    return result

def lagrange_polynomial(interpolation_points: list[float], f: Callable[[float], float], verbose=True) -> Any:
    """
    Based on interpolation points and function f, return a list of terms for the Lagrange polynomial.
    """

    # Define the symbolic variable x
    x = sym.Symbol("x")

    # Find function values at interpolation points
    function_values = [f.subs(x, point) for point in interpolation_points]

    # Find the number of interpolation points
    n = len(interpolation_points)

    # Find all terms in a sum
    terms = [function_values[i] * get_lagrange_product(interpolation_points, i, x, verbose=verbose) for i in range(n)]

    # Finding a sum
    result = sym.simplify(sym.Add(*terms))

    # Printing all terms if in verbose mode
    if verbose:
        my_logger.print_list_rich_with_result(terms, result, term_prefix="Sum term")

    return sym.simplify(result)

def print_example_values(interpolation_points: list[float], lagrange_polynomial: Any, verbose=True) -> None:
    """
    Get example values for the Lagrange polynomial by finding the average
    between each of the interpolation_points and then evaluating
    the lagrange_polynomial at each of them.
    """

    assert len(interpolation_points) >= 3, "At least 3 interpolation points are required."
    x = sym.Symbol("x")

    points = [(previous + current) / 2.0 for previous, current in zip(interpolation_points, interpolation_points[1:])]
    my_logger.print_list_rich([f"L({point}) = {lagrange_polynomial.subs(x, point)}" for point in points], term_prefix="Example point")

def get_nth_derivative(f: Callable[[float], float], k: int):
    """
    Returns the k-th derivative of function f.
    """
    x = sym.symbols('x')
    return sym.diff(f, *[x]*k)

# Define the function
x = sym.symbols('x')
tasks = [
    (sym.sin(2.0 * sym.pi * x), [0.0, 0.125, 0.25]),
    (sym.exp(x), [-1.0, 0.0, 1.0]),
    (sym.sqrt(x), [100.0, 121.0, 144.0]),
    (sym.exp(-x**2)/sym.sqrt(2.0*sym.pi), [0.2, 0.5, 0.7])
]

for (f, interpolation_points) in tasks:
    n = len(interpolation_points)
    my_logger.print_panel("Deriving Lagrange Polynomial")
    polynomial = lagrange_polynomial(interpolation_points, f)

    my_logger.print_panel("Lagrange Polynomial")
    print(polynomial)

    my_logger.print_panel("Example Values")
    print_example_values(interpolation_points, polynomial)

    my_logger.print_panel("nth derivative")
    print(polynomial)
    print(get_nth_derivative(f, n))
