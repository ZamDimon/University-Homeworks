from math import prod
import numpy as np
import solver

from abc import ABC, abstractmethod
from typing import List, Tuple, TypeAlias

Point: TypeAlias = Tuple[float, float]

class IInterpolate(ABC):
    """Interface any interpolating function should implement"""
    
    def __init__(self, points: List[Point]) -> None:
        """ 
        Initializes the interpolating function
        ### Args:
        - points (`List[Point]`): List of points to interpolate on
        """
        assert len(points) > 1, "At least two points are required"
        self._points = points
    
    @abstractmethod
    def evaluate(self, x: float) -> float:
        """
        Evaluates the interpolating function at x
        ### Args:
        - x (`float`): Point to evaluate the polynomial at
        ### Returns:
            `float`: Value of the polynomial at x
        """
        pass
    
class CubicSpline(IInterpolate):
    """Cubic spline interpolating function"""
    
    def __init__(self, points: List[Point]) -> None:
        super().__init__(points)
        
        # Defining the number of points
        self._n = len(points)
        # Finding h_{i} = x_{i} - x_{i-1}
        self._differences = self._find_differences()
        # Finding m_{i} coefficients
        self._m = self._find_m_coefficients()
        
    def _find_differences(self) -> np.ndarray:
        """ Generates a list of pairwise differences between x coordinates of points

        Returns:
            np.ndarray: numpy array of length n-1 where n is the number of points
        """
        return np.array([self._points[i][0] - self._points[i-1][0] for i in range(1, self._n)])
        
    def _find_m_coefficients(self) -> np.ndarray:
        """ Generates a list of m coefficients needed for the evaluation

        Returns:
            np.ndarray: numpy array of length n where n is the number of points
        """
        l = np.array([self._differences[i] / 6.0 for i in range(1, self._n-2)]) # Initializing the lower diagonal
        u = np.array([self._differences[i+1] / 6.0 for i in range(self._n-3)]) # Initializing the upper diagonal
        d = np.array([(self._differences[i] + self._differences[i+1]) / 3.0 for i in range(self._n-2)]) # Initializing the main diagonal
        b = np.array([-(self._points[i][1] - self._points[i-1][1]) / self._differences[i-1]
             + (self._points[i+1][1] - self._points[i][1]) / self._differences[i] for i in range(1, self._n-1)]) # Initializing the right hand side

        m = solver.tridiagonal_matrix_algorithm(l, u, d, b)
        m = np.insert(m, 0, 0.0, axis=0) # Add zero to the beginning of the list
        m = np.append(m, 0.0) # Add zero to the end of the list
        return m
     
    def evaluate(self, x: float) -> float:
        # Defining a list of terms to sum
        for i in range(1, self._n):
            if self._points[i-1][0] <= x <= self._points[i][0]:
                return self._m[i-1] * (self._points[i][0] - x)**3 / (6.0 * self._differences[i-1]) \
                    + self._m[i] * (x - self._points[i-1][0])**3 / (6.0 * self._differences[i-1]) \
                    + (self._points[i-1][1] - self._m[i-1] * self._differences[i-1]**2 / 6.0) * (self._points[i][0] - x) / self._differences[i-1] \
                    + (self._points[i][1] - self._m[i] * self._differences[i-1]**2 / 6.0) * (x - self._points[i-1][0]) / self._differences[i-1]
                    
        raise ValueError("x is not in the interval")