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

def get_mean_credible_interval(dataset: np.ndarray, 
                               variance: float,
                               credibility_prob: float) -> [float, float]:
    """
    Given a dataset, consisting of an array of floats, and variance 
    this function returns the credible interval for the mean of the dataset.
    """
    
    mu = np.mean(dataset) # Getting the mean
    n = len(dataset) # Getting the number of data points
    z_alpha = inverse_laplace_function(credibility_prob/2) # Getting the z_alpha value

    return (mu - z_alpha * np.sqrt(variance/n), mu + z_alpha * np.sqrt(variance/n))
    
dataset = [2.15]*2 + [2.25]*8 + [2.35]*22 + [2.45]*40 + [2.55]*12 + [2.65]*10
print(get_mean_credible_interval(dataset, 0.01**2, 0.96))