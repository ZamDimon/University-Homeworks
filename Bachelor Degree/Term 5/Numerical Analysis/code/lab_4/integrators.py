from typing import Callable, Tuple, TypeAlias
from abc import ABC, abstractmethod

# Define type alias for an interval type
Interval: TypeAlias = Tuple[float, float]

class Integrator(ABC):
    """
    Abstract class for classes that implement function integration
    """
    
    def __init__(self, fn: Callable[[float], float]) -> None:
        """ Initialize the integrator with a function to integrate

        Args:
            fn (Callable[[float], float]): Function to integrate
        """
        self._fn = fn
        pass
    
    @abstractmethod
    def evaluate(self, interval: Interval, accuracy: float = 1e-6) -> float:
        """
        Evaluate the integral of the function over the interval
        
        Args:
            interval (Interval): Interval to integrate over
            accuracy (float, optional): Desired accuracy of the integral. Defaults to `1e-6`.
        """
        pass
    
class TrapezoidalIntegrator(Integrator):
    """
    Class for trapezoidal integration
    """
    
    # Maximum number of iterations
    MAX_ITERATIONS: int = 20
    
    def __init__(self, fn: Callable[[float], float]) -> None:
        super().__init__(fn)
    
    def evaluate(self, interval: Interval, accuracy: float = 1e-6) -> float:
        MAX_VALUE: float = 1e12
        interval_size: float = interval[1] - interval[0]
        estimate: float = MAX_VALUE 
        error: float = MAX_VALUE
        k: int = 1 # Number of iterations
        
        while abs(error) > accuracy:
            intervals_number: int = 2**k
            step_size: float = interval_size / intervals_number
            k = k + 1
            
            nodes = [interval[0] + i * step_size for i in range(0, intervals_number+1)]
            current_esimate = (step_size / 2) * sum([(self._fn(nodes[i]) + self._fn(nodes[i+1])) for i in range(0, intervals_number)])
            
            error = current_esimate - estimate
            estimate = current_esimate
            if k > TrapezoidalIntegrator.MAX_ITERATIONS:
                raise RuntimeError("Maximum number of iterations reached")
            
        return estimate
    
class SimpsonIntegrator(Integrator):
    """
    Class for Simpson integration
    """
    
    # Maximum number of iterations
    MAX_ITERATIONS: int = 20
    
    def __init__(self, fn: Callable[[float], float]) -> None:
        super().__init__(fn)
    
    def evaluate(self, interval: Interval, accuracy: float = 1e-6) -> float:
        MAX_VALUE: float = 1e12
        interval_size: float = interval[1] - interval[0]
        estimate: float = MAX_VALUE 
        error: float = MAX_VALUE
        k: int = 1 # Number of iterations
        
        while abs(error) > accuracy:
            intervals_number: int = 2**k
            step_size: float = interval_size / intervals_number
            k = k + 1
            
            nodes = [interval[0] + i * step_size for i in range(0, intervals_number+1)]
            current_esimate = (step_size / 3) * (
                self._fn(nodes[0]) + 
                4*sum([self._fn(nodes[i]) for i in range(1, intervals_number, 2)]) +
                2*sum([self._fn(nodes[i]) for i in range(2, intervals_number, 2)]) +
                self._fn(nodes[-1])
            )
            
            error = current_esimate - estimate
            estimate = current_esimate
            if k > SimpsonIntegrator.MAX_ITERATIONS:
                raise RuntimeError("Maximum number of iterations reached")
            
        return estimate