from math import cos, pi
from typing import Tuple, TypeAlias, List
from abc import ABC, abstractmethod

Interval: TypeAlias = Tuple[float, float]

class IDataPointsGenerator(ABC):
    """Interface for generating data points"""
    
    def __init__(self, interval: Interval, number: int) -> None:
        """
        Function initializing the generator

        ### Args:
        - interval (`Interval`): Interval on which the data points will be generated
        - number (`int`): Number of data points to generate
        """
        
        assert number > 0, "Number of data points must be greater than 0"
        assert interval[0] < interval[1], "Lower bound must be less than upper bound"
        
        self._lower, self._upper = interval
        self._number = number
    
    @abstractmethod
    def generate_nodes(self) -> List[float]:
        """
        Function generating data points

        ### Returns:
            `List[float]`: List of generated x coordinates
        """
        pass
    
    @abstractmethod
    def generate_test_points(self, alpha: float = 0.1) -> List[float]:
        """
        Function generating test points for evaluating the polynomial
        ### Args:
        - alpha (`float`): We will evaluate the polynomial at points x_i + alpha*h

        Returns:
        - List[float]: List of x coordinates
        """
        
        nodes = self.generate_nodes()
        h = (self._upper - self._lower) / self._number
        return [node + alpha*h for node in nodes]
    
class LinearDataPointsGenerator(IDataPointsGenerator):
    """Class for generating linearly spaced data points"""
    
    def __init__(self, interval: Interval, number: int) -> None:
        super().__init__(interval, number)
    
    def generate_nodes(self) -> List[float]:
        fn = lambda i: self._lower + i * (self._upper - self._lower) / (self._number)
        return [fn(i) for i in range(self._number + 1)]
    
    def generate_test_points(self, alpha: float = 0.1) -> List[float]:
        return super().generate_test_points(alpha)
    
class CosineDataPointsGenerator(IDataPointsGenerator):
    """Class for generating cosine spaced data points"""
    
    def __init__(self, interval: Interval, number: int) -> None:
        super().__init__(interval, number)
        
    def generate_nodes(self) -> List[float]:
        fn = lambda i: 0.5*(self._lower+self._upper-(self._upper-self._lower)*cos((2*i+1)*pi/(2*(self._number+1))))
        return [fn(i) for i in range(self._number + 1)]

    def generate_test_points(self, alpha: float = 0.1) -> List[float]:
        return super().generate_test_points(alpha)
    
