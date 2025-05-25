"""
Module for MNIST classification architecture specification using KANConv2d
layer.
"""

from __future__ import annotations

import torch
import torch.nn as nn
from ckan_layer import KANConv2d


class MNISTFullyCKAN(nn.Module):
    """
    A simple CNN model for MNIST classification using the KANConv2d layer.
    """
    
    def __init__(self) -> None:
        """
        Initializes the KANConv2d model for MNIST classification.
        """
        
        super(MNISTFullyCKAN, self).__init__()
        
        self.conv1 = KANConv2d(in_channels=1, out_channels=4, kernel_size=3, stride=1, padding=1, spline_points=5, spline_degree=3)
        self.maxpool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = KANConv2d(in_channels=4, out_channels=8, kernel_size=3, stride=1, padding=1, spline_points=5, spline_degree=3)
        self.maxpool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv3 = KANConv2d(in_channels=8, out_channels=16, kernel_size=3, stride=1, padding=1, spline_points=5, spline_degree=3)
        self.maxpool3 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv4 = KANConv2d(in_channels=16, out_channels=32, kernel_size=2, stride=1, padding=1, spline_points=5, spline_degree=3)
        self.global_pooling = nn.AdaptiveAvgPool2d((1, 1))
        self.fc1 = nn.Linear(32, 10)  # Adjusted for 2 max pooling layers


    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Computes the forward pass of the model.
        """
        x = self.conv1(x)
        x = self.maxpool1(x)
        x = self.conv2(x)
        x = self.maxpool2(x)
        x = self.conv3(x)
        x = self.maxpool3(x)
        x = self.conv4(x)
        x = self.global_pooling(x)
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        
        return x