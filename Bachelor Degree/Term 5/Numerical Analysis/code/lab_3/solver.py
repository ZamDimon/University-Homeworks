from typing import TypeAlias, Tuple, List
import numpy as np

Point: TypeAlias = Tuple[float, float]
Dataset: TypeAlias = List[Point]

class LeastSquaresSolver:
    """
    A class to solve the least squares problem
    """
    
    def __init__(self, degree: int) -> None:
        """
        Args:
            dataset (Dataset): A list of points
            degree (int): The degree of the polynomial to fit
        """
        
        self._degree = degree

    def _generate_power_vector(self, x: float) -> List[float]:
        """ Generates a row consisting of powers of x
        
        Args:
            x (float): The x value of the point
        
        Returns:
            List[float]: A row for the dataset matrix
        """
        
        return [x**i for i in range(self._degree + 1)]

    def fit(self, dataset: Dataset) -> np.ndarray:
        """ Returns a list of coefficients for the polynomial of the given degree
        
        Returns:
            np.ndarray: A list of coefficients for the polynomial of the given degree (degree + 1)
        """
        
        X = np.empty((len(dataset), self._degree + 1))
        Y = np.empty((len(dataset), 1))
        
        for i in range(len(dataset)):
            x, y = dataset[i]
            X[i] = self._generate_power_vector(x)
            Y[i] = y
                
        self._coefficients = np.linalg.inv(X.T @ X) @ X.T @ Y
        self._coefficients = np.squeeze(self._coefficients, axis=-1)
        return self._coefficients
    
    def predict(self, x: float) -> np.floating:
        """ Predicts the y value for the given x value
        
        Args:
            x (float): The x value to predict the y value for
        
        Returns:
            float: The predicted y value
        """
        
        return self._coefficients @ self._generate_power_vector(x)