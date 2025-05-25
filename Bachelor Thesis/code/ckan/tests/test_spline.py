"""
Tests for the B-spline class.
"""

import torch
import torch.nn as nn
import torch.optim as optim

import unittest
import numpy as np
import matplotlib.pyplot as plt

from spline import BSpline


class TestBSpline(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case.
        """
        
        self.knots = 15
        self.degree = 3
        self.spline = BSpline(self.knots, self.degree)

    def test_b_spline_visualize(self) -> None:
        """
        Plots the B-spline basis functions.
        """
        
        for i in range(self.knots+1):
            x = torch.linspace(-1, 1, 1000)
            y = self.spline.b_spline_basis(x)[i]
            plt.plot(x.numpy(), y.numpy(), label=f'Basis {i}')
            
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid()
        plt.title('B-Spline Basis Functions')
        plt.show()
        
        
    def test_b_spline_training(self) -> None:
        """
        Manually tests and visualizes the B-spline function.  This is not an automated test.
        This function trains a BSpline module and plots the resulting spline function.
        """
        
        # Create some dummy data and optimizer
        x_data = torch.linspace(-1, 1, 100)
        # Example target function with noise
        y_real = x_data**2 * torch.sin(2 * np.pi * x_data) * torch.exp(x_data/8.0)
        y_data = y_real + 0.03 * torch.randn_like(y_real)
        optimizer = optim.Adam(self.spline.parameters(), lr=0.01)
        criterion = nn.MSELoss()

        # Train the spline module to approximate the data
        epochs = 2000
        for epoch in range(epochs):
            optimizer.zero_grad()
            y_pred = self.spline(x_data)
            loss = criterion(y_pred, y_data)
            loss.backward()
            optimizer.step()
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

        # Plot the trained spline function
        plt.plot(x_data, self.spline(x_data).detach().numpy(), linewidth=3, color='blue', label='Trained Spline')
        plt.plot(x_data, y_real, color='red', linewidth=2, linestyle='dashed', label='Target Function')
        plt.scatter(x_data, y_data, s=20.0, marker='x', color='red', label='Data Points')
       # plt.scatter(self.spline.knots.detach().numpy(), torch.zeros_like(self.spline.knots), marker='x', color='red', label='Knots') #show the knots
       # plt.scatter(torch.linspace(-1,1,self.knots), self.spline.coeffs.numpy(), marker='o', color='green', label='Control Points')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid()
        plt.title('Trained B-Spline Function')
        plt.legend()
        plt.savefig('trained_spline.pdf')