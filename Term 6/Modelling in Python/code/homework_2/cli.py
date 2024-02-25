# Numpy + matplotlib
import numpy as np
import matplotlib.pyplot as plt

# For loading progress bar
from rich.progress import Progress


# Setting high DPI for Matplotlib
plt.rcParams['figure.dpi'] = 150

# CLI Client
import typer
from typing_extensions import Annotated
app = typer.Typer()

@app.command()
def show_random_walk(
        steps_number: Annotated[int, typer.Option(help='Size of a random walk')] = 10000,
    ) -> None:
    """
    Displays a 1D random walk using matplotlib and numpy
    
    Args:
        steps_number (int): The number of steps to be taken in the random walk
    """
    
    def show_random_walk(color: str = 'red') -> None:
        """
        Shows the random walk by picking {+1, -1} randomly n times and 
        finding the cumulative sum of the steps
        
        Args:
            color (str): The color of the line to be drawn
        """
        
        steps = np.random.choice(a=[-1, 1], size=steps_number)
        path = np.concatenate([[0], steps]).cumsum()
        ax.plot(path, c=color, alpha=0.5, lw=1.0, ls='-')

    fig = plt.figure(figsize=(8,4))
    ax = fig.add_subplot(111)
    ax.grid()

    plt.title('1D Random Walk')
    for color in ['red', 'green', 'blue']:
        show_random_walk(color=color)

    plt.savefig('random_walk.png')
    plt.show()
    
@app.command()
def positive_y_experiment(
    steps_number: Annotated[int, typer.Option(help='Size of a random walk')] = 10000,
    experiments_number: Annotated[int, typer.Option(help='Number of experiments to be conducted')] = 1000,
    histogram_density: Annotated[int, typer.Option(help='Number of segments to divide results into to show the histogram')] = 20,
    show_histogram: Annotated[bool, typer.Option(help='Show histogram of the results')] = True,
) -> None:
    """
    Conducts a random walk and calculates the portion of the steps that are above the Ox axis
    
    Args:
        steps_number (int): The number of steps to be taken in each random walk
        experiments_number (int): The number of experiments to be conducted
        histogram_density (int): The number of segments to divide results into to show the histogram
        show_histogram (bool): Whether to show the histogram of the results
    """
    
    # Defining the experiment
    def conduct_random_walk() -> float:
        steps = np.random.choice(a=[-1, 1], size=steps_number)
        path = steps.cumsum()
        p = np.sum(path >= 0)
        return p / steps_number
    
    # Conducting the experiments    
    results = np.zeros(experiments_number)
    for i in range(experiments_number):
        results[i] = conduct_random_walk()

    # Showing the bar plot
    bar = np.zeros(histogram_density)
    for i in range(histogram_density-1):
        bar[i] = np.sum(np.logical_and(results >= i/histogram_density, results <= (i+1)/histogram_density))/experiments_number
    bar[histogram_density-1] = np.sum(results >= (histogram_density-1)/histogram_density) / experiments_number
    
    print('Portion of steps above the Ox axis:\n', bar)
    if show_histogram:
        _, ax = plt.subplots(1, 1, figsize=(6,3))
        ax.bar(
            range(histogram_density), 
            bar,
            linewidth=0.7,
            edgecolor='white', 
            color='blue', 
            align='center'
        )
        ax.set_ylabel('Ratio of steps above the Ox axis')
        ax.grid()
        # Setting x limit
        ax.set_xlim(-1, histogram_density)
        ax.set_ylim(0, max(bar)+0.01)
        
        plt.savefig('positive_y_experiment.png')
        plt.show()
        
@app.command()
def switches_number_experiment(
    steps_number: Annotated[int, typer.Option(help='Size of a random walk')] = 10000,
    experiments_number: Annotated[int, typer.Option(help='Number of experiments to be conducted')] = 1000,
    histogram_density: Annotated[int, typer.Option(help='Number of segments to divide results into to show the histogram')] = 20,
    show_histogram: Annotated[bool, typer.Option(help='Show histogram of the results')] = True,
) -> None:
    """
    Conducts a random walk and calculates the portion of steps when the leadership changes
    
    Args:
        steps_number (int): The number of steps to be taken in each random walk
        experiments_number (int): The number of experiments to be conducted
        histogram_density (int): The number of segments to divide results into to show the histogram
        show_histogram (bool): Whether to show the histogram of the results
    """
    
    # Defining the experiment
    def conduct_random_walk() -> float:
        steps = np.random.choice(a=[-1, 1], size=steps_number)
        path = steps.cumsum()
        p = 0
        for i in range(1, steps_number-1):
            if path[i] == 0 and path[i-1]*path[i+1] < 0:
                p += 1
        return p / steps_number
    
    # Conducting the experiments    
    results = np.zeros(experiments_number)
    with Progress() as progress:
        random_walk_task = progress.add_task("[green]Conducting random walks...", total=experiments_number)
        for i in range(experiments_number):
            results[i] = conduct_random_walk()
            progress.update(random_walk_task, advance=1)

    # Showing the bar plot
    right_edge = 0.1
    
    bar = np.zeros(histogram_density)
    for i in range(histogram_density-1):
        bar[i] = np.sum(np.logical_and(results >= i * right_edge/histogram_density, results <= (i+1)*right_edge/histogram_density))/experiments_number
    bar[histogram_density-1] = np.sum(results >= (histogram_density-1)*right_edge/histogram_density) / experiments_number
    
    print('Portion of changed:\n', bar)
    if show_histogram:
        _, ax = plt.subplots(1, 1, figsize=(6,3))
        ax.bar(range(histogram_density), bar, width=1, edgecolor='white', color='blue', linewidth=0.7, align='edge')
        plt.savefig('switches_number_experiment.png')
        plt.show()

if __name__ == "__main__":
    app()