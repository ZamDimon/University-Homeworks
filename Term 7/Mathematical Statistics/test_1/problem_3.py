# Importing necessary libraries
import numpy as np 
from scipy.stats import chi2

def get_variance_credible_interval(dataset: np.ndarray,
                                   alpha: float) -> [float, float]:
    """
    Given a dataset, consisting of an array of floats, 
    this function returns the credible interval for the variance of the dataset.
    """
    
    mu = np.mean(dataset) # Getting the mean
    variance = np.mean(dataset**2) - mu**2 # Getting the variance
    n = len(dataset) # Getting the number of data points
    
    q = 1 - alpha # Getting the q value
    beta = chi2.isf(q/2, n-1)
    gamma = chi2.isf(1-q/2, n-1)
    
    return (n*variance/beta, n*variance/gamma)
    
dataset = np.array([
    196, 208, 196, 208, 208, 222, 216, 227, 222, 216, 222, 216,
    216, 222, 227, 240, 240, 240, 240, 240, 240, 240, 227, 227, 227
])

print(get_variance_credible_interval(dataset, 0.9))