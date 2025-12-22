"""
Class for B-spline interpolation using PyTorch.
This class allows for the creation of B-spline curves with a specified number of control points and degree.
The B-spline curve is defined by a set of control points and a knot vector.
The B-spline basis functions are computed using the Cox-de Boor recursion formula.
"""
from __future__ import annotations

import torch
import torch.nn as nn

import numpy as np


class BSpline(nn.Module):
    """
    Class for B-spline interpolation using PyTorch.
    This class allows for the creation of B-spline curves with a specified number of control points and degree.
    The B-spline curve is defined by a set of control points and a knot vector.
    The B-spline basis functions are computed using the Cox-de Boor recursion formula.
    """
    
    def __init__(
        self, 
        knots: int, 
        degree: int = 3
    ) -> None:
        """
        Initializes the B-spline object.
        Args:
            knots (int): Number of control points.
            degree (int): Degree of the B-spline. Default is 3 (cubic B-spline).
        """
        
        super(BSpline, self).__init__()
        
        self.knots = knots
        self.degree = degree
        
        # Setting up the grid
        grid = torch.linspace(-1, 1, knots) # Knot vector of length knots + degree + 1
        grid = BSpline.extend_grid(grid, k=degree) # Extend the grid on either side by degree steps
        self.register_buffer('grid', grid)
        
        # Prepare trainable parameters
        self.spline_coefficients = knots + 2 * degree - 1
        self.coeffs = nn.Parameter(torch.randn(self.spline_coefficients)) # Learnable coefficients
        

    @staticmethod
    def extend_grid(grid: np.ndarray, k: int) -> np.ndarray:
        """
        Extends the grid on either size by k steps

        Args:
            grid: number of splines x number of control points
            k: spline order

        Returns:
            new_grid: number of splines x (number of control points + 2 * k)
        """
        
        n_intervals = len(grid) - 1
        bucket_size = (grid[-1] - grid[0]) / n_intervals
        
        for i in range(k):
            grid = torch.cat([grid[:1] - bucket_size, grid])
            grid = torch.cat([grid, grid[-1:] + bucket_size])

        return grid
    

    def b_spline_basis(self, x: torch.Tensor) -> torch.Tensor:
        """
        Evaluates the B-spline basis functions at position x.
        """
        
        tensor_shape = x.shape

        # Using x.device for basis, assuming grid will be used accordingly or is on the same device
        basis = torch.zeros((self.knots+2*self.degree-1, self.degree+1, *tensor_shape), dtype=x.dtype, device=x.device)
        
        # Ensure grid is on the same device as x for operations involving both
        grid_local = self.grid.to(x.device)

        for i in range(self.spline_coefficients):
            # Ensure operations are between tensors on the same device
            condition = (x >= grid_local[i]) & (x < grid_local[i+1])
            basis[i, 0, ...] = torch.where(
                condition,
                torch.ones_like(x), 
                torch.zeros_like(x)
            )
        
        for d in range(1, self.degree+1):
            for i in range(self.spline_coefficients-d):
                # Clone the slices of `basis` from the previous degree (d-1) before using them.
                # This prevents the inplace modification of `basis` (via .copy_ below)
                # from affecting the versions of these tensors needed by autograd.
                basis_i_prev_d = basis[i, d-1, ...].clone()
                basis_i_plus_1_prev_d = basis[i+1, d-1, ...].clone()

                # Denominators
                den1 = grid_local[i+d] - grid_local[i]
                den2 = grid_local[i+d+1] - grid_local[i+1]

                # Calculate b1
                # Note: Original code divides directly. If den1 can be zero, this can lead to inf/nan.
                # This fix focuses on the autograd error, not numerical stability of division by zero.
                if den1 == 0: # Avoid division by zero; result of this term is effectively 0 if numerator is finite.
                              # Or handle as per specific B-spline convention for coincident knots.
                              # For now, if den1 is 0, b1 will be 0 assuming basis_i_prev_d is not inf/nan.
                    b1 = torch.zeros_like(x)
                else:
                    b1 = (x - grid_local[i]) * basis_i_prev_d / den1
                
                # Calculate b2
                if den2 == 0: # Similar handling for den2
                    b2 = torch.zeros_like(x)
                else:
                    b2 = (grid_local[i+d+1] - x) * basis_i_plus_1_prev_d / den2
                
                # The inplace copy operation was the source of the autograd error.
                # By using cloned inputs for b1 and b2, the original `basis` tensor's
                # versions are not an issue for *their* gradient computation.
                basis[i, d, ...].copy_(b1 + b2)
        
        return basis[:, self.degree, ...]


    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Computes the forward pass of the B-spline.
        """
        
        basis_values = self.b_spline_basis(x)
        return basis_values.T @ self.coeffs
    