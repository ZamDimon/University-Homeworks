"""
Implementation of the KANConv2d layer as described in my
Bachelor's thesis. This layer is a convolutional layer that
uses a spline-based approach to learn the convolutional
kernel weights. The layer is designed to work with 2D input
data, such as images.
"""
from __future__ import annotations

from typing import Tuple, Union

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class KANConv2d(nn.Module):
    """
    Implementation of the KANConv2d layer as described in my 
    Bachelor's thesis. This layer is a convolutional layer that
    uses a spline-based approach to learn the convolutional
    kernel weights. The layer is designed to work with 2D input
    data, such as images.
    """
    
    def __init__(
        self,
        in_channels: int, 
        out_channels: int, 
        kernel_size: Union[Tuple[int, int], int], 
        stride: int = 1,
        padding: int = 1,
        spline_points: int = 5, 
        spline_degree: int = 3,
        spline_coefficients_variance: float = 0.1,
    ) -> None:
        """
        - `in_channels`: Number of input channels
        - `out_channels`: Number of output channels
        - `kernel_size`: Size of the convolutional kernel (assumes to be square if of type `int`)
        - `stride`: Stride of the convolution
        - `padding`: Padding added to all sides of the input
        - `spline_points`: Number of points for the spline basis functions
        - `spline_coefficients_variance`: Variance of the spline coefficients initialization
        - `spline_degree`: Degree of the spline basis functions
        """
        
        super(KANConv2d, self).__init__()
        
        if isinstance(kernel_size, int):
            kernel_size = (kernel_size, kernel_size)
        if isinstance(stride, int):
            stride = (stride, stride)
        if isinstance(padding, int):
            padding = (padding, padding)
        
        # Set the internal parameters
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.knots = spline_points
        self.degree = spline_degree
        
        # Learnable weights for beta(x) and spine basis functions
        self.beta_weights = nn.Parameter(torch.randn(out_channels, in_channels, kernel_size[0], kernel_size[1]))
        self.spline_weights = nn.Parameter(torch.randn(out_channels, in_channels, kernel_size[0], kernel_size[1]))

        # Setting up the grid
        grid = torch.linspace(-1, 1, self.knots) # Knot vector of length knots + degree + 1
        grid = KANConv2d.extend_grid(grid, d=self.degree) # Extend the grid on either side by degree steps
        self.register_buffer('grid', grid)
        
        # Prepare trainable parameters
        spline_coefficients = self.knots + 2 * self.degree - 1 # Number of coefficients for the spline representation
        self.spline_coefficients = spline_coefficients
        # Initialize the spline coefficients according to the normal distribution
        # with the specified variance
        std = np.sqrt(spline_coefficients_variance)
        self.coeffs = nn.Parameter(std * torch.randn(spline_coefficients, out_channels, in_channels, kernel_size[0], kernel_size[1])) # Learnable coefficients


    @staticmethod
    def extend_grid(grid: np.ndarray, d: int) -> np.ndarray:
        """
        Extends the grid on either size by d steps

        Args:
            grid: number of splines x number of control points
            d: spline order

        Returns:
            new_grid: number of splines x (number of control points + 2*d)
        """
        
        n_intervals = len(grid) - 1
        bucket_size = (grid[-1] - grid[0]) / n_intervals
        
        for _ in range(d):
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
        Computes the forward pass of the KANConv2d layer.
        """
        
        # First, figure out the input/output dimensions
        batch_size, _, height, width = x.shape
        x = F.pad(x, 
                (self.padding[1], 
                self.padding[1], 
                self.padding[0], 
                self.padding[0]))
        out_height = (height + 2 * self.padding[0] - self.kernel_size[0]) // self.stride[0] + 1
        out_width = (width + 2 * self.padding[1] - self.kernel_size[1]) // self.stride[1] + 1
        output = torch.zeros(
            batch_size, 
            self.out_channels, 
            out_height, 
            out_width, 
            device=x.device
        )
        
        for i in range(out_height):
            for j in range(out_width):
                patch = x[:, :, 
                        i*self.stride[0]:i*self.stride[0]+self.kernel_size[0],
                        j*self.stride[1]:j*self.stride[1]+self.kernel_size[1]]
                
                # Evaluate the beta function with weights
                beta = F.silu(patch)
                beta = beta.unsqueeze(1).repeat(1, self.out_channels, 1, 1, 1)
                beta_weights = self.beta_weights.unsqueeze(0).repeat(batch_size, 1, 1, 1, 1)
                beta = beta_weights * beta
                beta = beta.permute(1, 0, 2, 3, 4)
                
                # Evaluate the B-spline basis functions
                basis_values = self.b_spline_basis(patch)
                
                # Extend all the shapes to be compatible
                coeffs = self.coeffs.unsqueeze(2).repeat(1, 1, batch_size, 1, 1, 1)
                basis_values = basis_values.unsqueeze(1).repeat(1, self.out_channels, 1, 1, 1, 1)
                
                # Compute the linear combination of the basis functions
                splines = torch.sum(coeffs*basis_values, dim=0) # [batch_size, out_channels, in_channels, kernel_size[0], kernel_size[1]]
                spline_weights = self.spline_weights.unsqueeze(1).repeat(1, batch_size, 1, 1, 1)
                splines = spline_weights * splines
                
                # Find sum of the splines and beta values
                activations = splines + beta
                
                # Finally, compute the output part of the convolution
                result = torch.sum(activations, dim=(2, 3, 4)) # [batch_size, out_channels, in_channels, kernel_size[0], kernel_size[1]]
                result = result.permute(1, 0)
                output[:, :, i, j] = result

        return output
