"""
Main module for running the KANConv2d model on MNIST dataset.
"""

from __future__ import annotations

import os
import time
import random

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import torchvision.utils as vutils

from models.fully_kan_mnist import MNISTFullyCKAN
from models.kan_mnist import MNISTCKAN


# --- Training and Evaluation Functions ---
def train_epoch(model, device, train_loader, optimizer, criterion, epoch, log_interval=100):
    model.train()
    running_loss = 0.0
    samples_processed = 0
    start_time = time.time()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item() * data.size(0)
        samples_processed += data.size(0)
        
        if batch_idx % log_interval == 0 and batch_idx > 0:
            elapsed_time = time.time() - start_time
            speed = (batch_idx * train_loader.batch_size) / elapsed_time if elapsed_time > 0 else float('inf')
            print(f'Train Epoch: {epoch} [{batch_idx * len(data)}/{len(train_loader.dataset)} ({100. * batch_idx / len(train_loader):.0f}%)]\tLoss: {loss.item():.6f}\tSpeed: {speed:.2f} samples/sec')
    
    epoch_loss = running_loss / samples_processed
    epoch_time = time.time() - start_time
    print(f'====> Epoch: {epoch} Average loss: {epoch_loss:.4f}, Time: {epoch_time:.2f}s')


def evaluate(model, device, test_loader, criterion):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += criterion(output, target).item() * data.size(0)  # sum up batch loss
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    num_test_samples = len(test_loader.dataset)
    test_loss /= num_test_samples
    accuracy = 100. * correct / num_test_samples

    print(f'\nTest set: Average loss: {test_loss:.4f}, Accuracy: {correct}/{num_test_samples} ({accuracy:.2f}%)\n')
    return accuracy, test_loss

# --- Main script ---
def main():
    # Hyperparameters
    BATCH_SIZE = 64
    TEST_BATCH_SIZE = 100
    EPOCHS = 2 # KANConv2d is slow, so fewer epochs for a demo
    LEARNING_RATE = 0.001 # For Adam
    LOG_INTERVAL = 5 # How often to log training progress
    
    # Device configuration
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # MNIST dataset
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    try:
        train_dataset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
        test_dataset = torchvision.datasets.MNIST(root='./data', train=False, download=True, transform=transform)
    except Exception as e:
        print(f"Failed to download MNIST: {e}. Trying to load from local './data' directory.")
        try:
            train_dataset = torchvision.datasets.MNIST(root='./data', train=True, download=False, transform=transform)
            test_dataset = torchvision.datasets.MNIST(root='./data', train=False, download=False, transform=transform)
        except Exception as e_local:
            print(f"Failed to load MNIST from local directory: {e_local}. Exiting.")
            return

    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2, pin_memory=True if device=="cuda" else False)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=TEST_BATCH_SIZE, shuffle=False, num_workers=2, pin_memory=True if device=="cuda" else False)

    # Instantiate the model, optimizer, and loss function
    model = MNISTFullyCKAN().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    criterion = nn.CrossEntropyLoss()

    print("Starting training...")
    for epoch in range(1, EPOCHS + 1):
        train_epoch(model, device, train_loader, optimizer, criterion, epoch, LOG_INTERVAL)
        #evaluate(model, device, test_loader, criterion)
    
    print("Training finished.")

    # Save the trained model (optional)
    # os.makedirs("trained_models", exist_ok=True)
    # torch.save(model.state_dict(), "trained_models/mnist_ckan_final.pth")
    # print("Trained model state_dict saved to trained_models/mnist_ckan_final.pth")

    # --- Code to inspect a random element (can be run after training) ---
    print("\n--- Inspecting random element with trained model ---")
    # model.load_state_dict(torch.load("trained_models/mnist_ckan_final.pth")) # If loading
    model.eval()

    random_idx = random.randint(0, len(test_dataset) - 1)
    image, label = test_dataset[random_idx]
    image_unsqueezed = image.unsqueeze(0).to(device)

    print(f"Selected random image for inspection: Index {random_idx}, Label: {label}")

    activation_outputs = {}
    def get_activation(name):
        def hook(model, input, output):
            activation_outputs[name] = output.detach()
        return hook

    hook_conv1 = model.conv1.register_forward_hook(get_activation('conv1'))
    hook_conv2 = model.conv2.register_forward_hook(get_activation('conv2'))

    with torch.no_grad():
        _ = model(image_unsqueezed)

    hook_conv1.remove()
    hook_conv2.remove()

    os.makedirs("conv1_channel_outputs_trained", exist_ok=True)
    os.makedirs("conv2_channel_outputs_trained", exist_ok=True)

    # --- Save/Visualize conv1 outputs ---
    if 'conv1' in activation_outputs:
        conv1_out = activation_outputs['conv1'].cpu() # Shape: (1, out_channels, H, W)
        print(f"conv1 output shape: {conv1_out.shape}")
        num_channels_conv1 = conv1_out.shape[1]
        original_h_conv1, original_w_conv1 = conv1_out.shape[2], conv1_out.shape[3]

        for channel_idx in range(num_channels_conv1):
            # Extract single channel image: shape (H, W)
            channel_img = conv1_out[0, channel_idx, :, :]
            
            # Reshape for F.interpolate: (1, 1, H, W)
            # (Batch_size=1, Channels=1, Height, Width)
            img_to_upscale = channel_img.unsqueeze(0).unsqueeze(0)
            
            # Upscale using nearest-neighbor interpolation
            upscaled_img = F.interpolate(img_to_upscale, 
                                         size=(256, 256), 
                                         mode='nearest') # or 'nearest-exact' for newer PyTorch
            
            # Remove batch dimension for save_image if needed, it expects (C,H,W) or (B,C,H,W)
            # upscaled_img is (1, 1, 256, 256), squeeze to (1, 256, 256) for save_image
            vutils.save_image(upscaled_img.squeeze(0), 
                              f"conv1_channel_outputs_trained/channel_{channel_idx+1}_256x256.png",
                              normalize=True)
        print(f"Saved {num_channels_conv1} upscaled (256x256) channel images from conv1 to 'conv1_channel_outputs_trained'")

    # --- Save/Visualize conv2 outputs ---
    if 'conv2' in activation_outputs:
        conv2_out = activation_outputs['conv2'].cpu() # Shape: (1, out_channels, H, W)
        print(f"conv2 output shape: {conv2_out.shape}")
        num_channels_conv2 = conv2_out.shape[1]
        original_h_conv2, original_w_conv2 = conv2_out.shape[2], conv2_out.shape[3]

        for channel_idx in range(num_channels_conv2):
            # Extract single channel image: shape (H, W)
            channel_img = conv2_out[0, channel_idx, :, :]
            
            # Reshape for F.interpolate: (1, 1, H, W)
            img_to_upscale = channel_img.unsqueeze(0).unsqueeze(0)
            
            # Upscale using nearest-neighbor interpolation
            upscaled_img = F.interpolate(img_to_upscale, 
                                         size=(256, 256), 
                                         mode='nearest')
            
            # Save the upscaled image
            vutils.save_image(upscaled_img.squeeze(0), 
                              f"conv2_channel_outputs_trained/channel_{channel_idx+1}_256x256.png",
                              normalize=True)
        
        print(f"Saved {num_channels_conv2} upscaled (256x256) channel images from conv2 to 'conv2_channel_outputs_trained'")


if __name__ == '__main__':
    main()