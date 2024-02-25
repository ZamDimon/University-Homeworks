# Internal imports
from grid import Grid

# External imports
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from rich.progress import Progress

# CLI client
import typer
from typing_extensions import Annotated
app = typer.Typer(help="CLI client for Homework 1")

# Setting high DPI for Matplotlib
plt.rcParams['figure.dpi'] = 300

@app.command()
def instant_fill(
        size: Annotated[int, typer.Option(help='Size of a grid')] = 30,
        p: Annotated[float, typer.Option(help='Probability of a cell being an obstacle')] = 0.5
    ) -> None:
    """
    Fills a grid and displays it instantly
    
    Args:
        size (int): The size of the board
        p (float): The probability of a tile being an obstacle. Must be between 0 and 1.
    """
    
    grid = Grid(size, p)
    grid.fill_instantly(figsize=(12,6))
    
@app.command()
def animation_fill(
        size: Annotated[int, typer.Option(help='Size of a grid')] = 30,
        p: Annotated[float, typer.Option(help='Probability of a cell being an obstacle')] = 0.5
    ) -> None:
    """
    Fills a grid and displays it through an animation
    
    Args:
        size (int): The size of the board
        p (float): The probability of a tile being an obstacle. Must be between 0 and 1.
    """
    
    grid = Grid(size, p)
    grid.fill_with_animation(figsize=(12,6))
    
@app.command()
def analyze_depth(
    size: Annotated[int, typer.Option(help='Size of a grid')] = 30,
    min_p: Annotated[float, typer.Option(help='Minimum probability of a cell being an obstacle')] = 0.0,
    max_p: Annotated[float, typer.Option(help='Maximum probability of a cell being an obstacle')] = 1.0,
    steps: Annotated[int, typer.Option(help='Number of steps to analyze')] = 100,
    experiments: Annotated[int, typer.Option(help='Number of experiments to run')] = 100,
    fig_save_path: Annotated[Path, typer.Option(help='Path to save the figure')] = 'depths.png'
    ) -> None:
    """
    Analyzes the depth of the grid
    
    Args:
        size (int): The size of the board
        min_p (float): The minimum probability of a tile being an obstacle. Must be between 0 and 1.
        max_p (float): The maximum probability of a tile being an obstacle. Must be between 0 and 1.
        steps (int): The number of steps to analyze
        fig_save_path (Path): Path to save the figure
    """
    
    depths = np.empty((steps, experiments)) # Results of all experiments
    ps = np.linspace(min_p, max_p, num=steps) # Probabilities to check for
    
    with Progress() as progress:
        depths_calc_task = progress.add_task("[cyan]Calculating depths...", total=len(ps))
        
        for i, p in enumerate(ps):
            # Running the experiments
            depths[i,:] = np.array([Grid(size, p)._instant_fill() for _ in range(experiments)], 
                                dtype=np.float32)
            progress.update(depths_calc_task, advance=1)
    
    # Getting the percolation rates and average depths
    percolation_rates = (depths == size).astype(int).sum(axis=1) / experiments
    avg_depths = depths.mean(axis=1)

    # Plotting the results and storing the figure
    fig, ax = plt.subplots(1, 2, figsize=(12,6))
    ax[0].set_title('Average depth')
    ax[0].xaxis.set_label_text('Probability p')
    ax[0].yaxis.set_label_text('Average max depth reached')
    ax[0].grid()
    ax[0].plot(ps, avg_depths, 'r')
    ax[1].set_title('Percolation rate')
    ax[1].xaxis.set_label_text('Probability p')
    ax[1].yaxis.set_label_text('Percentage of percolations')
    ax[1].grid()
    ax[1].plot(ps, percolation_rates, 'b')
    plt.savefig(fig_save_path)
    plt.show()
        

if __name__ == "__main__":
    app()
    
