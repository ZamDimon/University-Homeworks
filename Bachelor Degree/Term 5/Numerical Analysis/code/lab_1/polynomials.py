from math import prod
from abc import ABC, abstractmethod
from typing import List, Tuple, TypeAlias

Point: TypeAlias = Tuple[float, float]

class IPolynomial(ABC):
    """Interface any polymial should implement"""
    
    def __init__(self, points: List[Point]) -> None:
        """ 
        Initializes the polynomial
        ### Args:
        - points (`List[Point]`): List of points to interpolate on
        """
        assert len(points) > 1, "At least two points are required"
        self._points = points
    
    @abstractmethod
    def evaluate(self, x: float) -> float:
        """
        Evaluates the polynomial at x
        ### Args:
        - x (`float`): Point to evaluate the polynomial at
        ### Returns:
            `float`: Value of the polynomial at x
        """
        pass
    
class LagrangePolynomial(IPolynomial):
    """Polynomial implementing Lagrange interpolation"""
    
    def __init__(self, points: List[Point]) -> None:
        super().__init__(points)
        
    def _lagrange_coefficient(self, i: int, x: float) -> float:
        """ Calculates the i-th Lagrange coefficient at x

        ### Args:
        - i (`int`): Number of the Lagrange coefficient to calculate
        - x (`float`): Point to calculate the Lagrange coefficient at

        ### Returns:
            float: Value of the i-th Lagrange coefficient at x
        """
        # Finding the i-th point's x coordinate
        x_i, _ = self._points[i]
        # Forming an array of product terms
        terms = [(x-x_j) / (x_i-x_j) for (j, (x_j,_)) in enumerate(self._points) if i!=j]
        # Finding their product
        return prod(terms)
        
    def evaluate(self, x: float) -> float:
        # Finding the y coordinate of each point and multiplying it by the corresponding Lagrange coefficient
        terms = [self._lagrange_coefficient(i, x) * y for (i, (_, y)) in enumerate(self._points)]
        # Summing the terms
        return sum(terms)
    
class NewtonForwardPolynomial(IPolynomial):
    """Polynomial implementing Newton's upper interpolation"""
    
    def __init__(self, points: List[Point]) -> None:
        # Calculating all differential differences beforehand
        super().__init__(points)
        self._differences = [self._differential_difference(0, i) for i in range(len(points))]
        
    def _differential_difference(self, i: int, j: int) -> float:
        """ Finds the differential difference y[i:j] at given x

        ### Args:
        - x (`float`): Point to find the differential difference at
        - i (`int`): From which index to start
        - j (`int`): At which index to stop

        ### Returns:
            `float`: Value of a differential difference at x
        """
        assert i >= 0, "i must be greater than 0"
        assert j <= len(self._points), "j must not exceed the number of points"
        
        # It is easier to deal with indices i,...,i+k
        k = j - i
        
        sum_terms: List[float] = [] # Defining a list of terms to sum
        for j in range(k+1):
            # Finding the denominator product terms
            denominator_terms = [self._points[i+j][0] - self._points[i+l][0] for l in range(k+1) if l!=j]
            # Dividing the numerator (self._points[i+j][1]) by the product of denominator terms
            sum_terms.append(self._points[i+j][1] / prod(denominator_terms))
        
        return sum(sum_terms)
    
    def evaluate(self, x: float) -> float:
        # Defining a list of terms to sum
        sum_terms: List[float] = []
        for i in range(len(self._points)):
            product_terms = [x - x_j for (x_j, _) in self._points[:i]]
            # Finding the differential difference y[0:i+1] at x
            sum_terms.append(self._differences[i] * prod(product_terms))
        
        return sum(sum_terms)
    
class NewtonBackwardsPolynomial(IPolynomial):
    """Polynomial implementing Newton's lower interpolation"""
    
    def __init__(self, points: List[Point]) -> None:
        # Calculating all differential differences beforehand
        super().__init__(points)
        n = len(points)
        self._differences = [self._differential_difference(n-1, i) for i in reversed(range(n))]
        
    def _differential_difference(self, i: int, j: int) -> float:
        """ Finds the differential difference y[i:j] at given x

        ### Args:
        - x (`float`): Point to find the differential difference at
        - i (`int`): From which index to start
        - j (`int`): At which index to stop

        ### Returns:
            `float`: Value of a differential difference at x
        """
        assert i >= 0, "i must be positive"
        assert j <= len(self._points), "j must be less than the number of points"

        # It is easier to deal with indices i,...,i-k
        k = i - j
        sum_terms: List[float] = [] # Defining a list of terms to sum
        for j in range(k+1):
            # Finding the denominator product terms
            denominator_terms = [self._points[i-j][0] - self._points[i-l][0] for l in range(k+1) if l!=j]
            # Dividing the numerator (self._points[i+j][1]) by the product of denominator terms
            sum_terms.append(self._points[i-j][1] / prod(denominator_terms))
        
        return sum(sum_terms)
    
    def evaluate(self, x: float) -> float:
        # Defining a list of terms to sum
        n = len(self._points)
        sum_terms: List[float] = []
        for i in reversed(range(n)):
            product_terms = [x - X for (X, _) in self._points[i+1:n]]
            # Finding the differential difference y[0:i+1] at x
            sum_terms.append(self._differences[n-1-i] * prod(product_terms))
        
        return sum(sum_terms)
        
