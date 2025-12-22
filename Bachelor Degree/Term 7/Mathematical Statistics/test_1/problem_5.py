# Importing necessary libraries
import numpy as np 
from scipy.stats import t
from scipy.special import stdtr, stdtrit

def test_hypothesis(dataset_1: np.ndarray,
                    dataset_2: np.ndarray, 
                    alpha: float = 0.95) -> bool:
    """
    Given a dataset, consisting of an array of floats, and standard deviation, 
    tests whether the expected mean is true or not.
    """
    
    mu_1 = np.mean(dataset_1) # Getting the mean of the first dataset
    mu_2 = np.mean(dataset_2) # Getting the mean of the second dataset
    n_1 = len(dataset_1) # Getting the number of data points in the first dataset
    n_2 = len(dataset_2) # Getting the number of data points in the second dataset
    variance_1 = np.mean(dataset_1**2) - mu_1**2 # Getting the variance of the first dataset
    variance_2 = np.mean(dataset_2**2) - mu_2**2 # Getting the variance of the second dataset
    
    statistics = (mu_1-mu_2)*np.sqrt(n_1*n_2*(n_1+n_2-2)/(n_1+n_2))/np.sqrt(variance_1*n_1 + variance_2*n_2) # Getting the statistics
    threshold = t.isf(1-alpha, n_1+n_2-2)
    print(f"Got statistics: {statistics} and threshold is {threshold}")
    return np.abs(statistics) < threshold
    
print(stdtrit(8, 0.2))    

dataset_1 = np.array([431, 397, 462, 457, 251, 221, 548, 478, 299, 541])
dataset_2 = np.array([322, 250, 225, 315, 399, 348, 192, 375, 381, 538, 198, 317, 293])
result = test_hypothesis(dataset_1, dataset_2, alpha=0.95)
print("Hypothesis is true" if result else "Hypothesis is false")