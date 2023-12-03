from typing import Callable
from rich import print
from math import cos
from integrators import Interval, TrapezoidalIntegrator, SimpsonIntegrator

if __name__ == '__main__':
    fn: Callable[[float], float] = lambda x: (1 - cos(x)) / x
    # We define the left endpoint of the interval to be EPSILON instead of 0 to avoid division by zero
    EPSILON: float = 1e-12
    interval: Interval = (EPSILON, 1.0) 
    
    trapezoidal_integrator: TrapezoidalIntegrator = TrapezoidalIntegrator(fn)
    trapezoidal_integral_estimate = trapezoidal_integrator.evaluate(interval, accuracy=1e-6)
    
    simpson_integrator: SimpsonIntegrator = SimpsonIntegrator(fn)
    simpson_integrator_estimate = simpson_integrator.evaluate(interval, accuracy=1e-6)
    
    print("Trapezoidal integral estimate: {:.20f}".format(trapezoidal_integral_estimate))
    print("Simpson integral estimate: {:.20f}".format(simpson_integrator_estimate))
    