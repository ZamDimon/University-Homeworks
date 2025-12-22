# Importing necessary libraries
import numpy as np 
from scipy.special import erf, erfinv

def laplace_function(x: float) -> float:
    """
    Given a float x, this function returns the value of the Laplace function at x, which
    is an integral of exp(-t^2/2)/sqrt(2\pi) from 0 to x.
    """
    
    return erf(x/np.sqrt(2))/2.0

def inverse_laplace_function(x: float) -> float:
    """
    Given a float x, this function returns the inverse of the Laplace function at x
    """
    r = 1
    STEPS_FOR_FINDING_INVERSE = 10000
    
    for _ in range(STEPS_FOR_FINDING_INVERSE):
        r = r * x / laplace_function(r)
    
    return r

def test_hypothesis(dataset: np.ndarray, 
                    std: float,
                    expected_mean: float,
                    alpha: float = 0.95) -> bool:
    """
    Given a dataset, consisting of an array of floats, and standard deviation, 
    tests whether the expected mean is true or not.
    """
    
    mu = np.mean(dataset) # Getting the mean
    n = len(dataset) # Getting the number of data points
    normed_diff = (mu - expected_mean) / (std/np.sqrt(n)) # Getting the normalized difference
    z_alpha = inverse_laplace_function(alpha/2) # Getting the z_alpha value
    
    print(f"Got normalized difference: {normed_diff}, z_alpha is: {z_alpha}")
    return np.abs(normed_diff) < z_alpha
    
dataset = [2130, 2090, 2030, 2080, 1920, 2020, 2015, 2000, 2045, 1940, 1980, 1970]
result = test_hypothesis(dataset, 5, 2000, 0.95)
print("Hypothesis is true" if result else "Hypothesis is false")