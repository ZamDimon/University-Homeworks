from __future__ import annotations
from typing import List, Tuple, Any

# NumPy and Matplotlib imports
import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Internal imports
from tile import TileType

class Grid:
    """
    Class responsible for interacting with a grid
    """
    
    def __init__(self, size: int, probability: float) -> None:
        """
        Initializes the board.
        
        Args:
            size (int): The size of the board
            probability (float): The probability of a tile being an "obstacle". Must be between 0 and 1.
        """
        
        assert 0 <= probability <= 1, "Not a valid probability: value must be between 0 and 1"
        
        self._size = size
        self._probability = probability
        self._grid = Grid._init_board(size, probability)
    
    @staticmethod
    def _init_board(size: int, probability: float) -> List[List[TileType]]:
        """
        Randomly initializes a board of size `size` with a probability `probability` of a tile being an obstacle.
        
        Args:
            size (int): The size of the board
            probability (float): The probability of a tile being an "obstacle". Must be between 0 and 1.
            
        Returns:
            List[List[TileType]]: The initialized board
        """
        
        np_grid = np.random.choice(
            a=[TileType.OBSTACLE, TileType.EMPTY], 
            size=(size, size), 
            p=[probability,1-probability]
        )
        
        # Converting np_grid to a list of lists
        grid = [[TileType.from_int(int(tile)) for tile in row] for row in np_grid]
        return grid
    
    def _instant_fill(self) -> int:
        """
        Fills the board according to the percolation rules instantly. 
        Returns the maximum number of filled cells in a column.
        
        Returns:
            int: The maximum number of filled cells in a column
        """
        
        self._prepare()
        self._fill_step()
        
        while True: 
            if self._fill_step(): break
            
        return self._get_max_depth()
    
    def _get_max_depth(self) -> int:
        """
        Returns the maximum number of filled cells in a column.
        
        Returns:
            int: The maximum number of filled cells in a column
        """
        
        candidates = [i for i in range(self._size) if TileType.MATERIAL in self._grid[i]]
        return max(candidates) + 1 if len(candidates) > 0 else 0
    
    def _prepare(self) -> None:
        """
        Starts the animation of the grid
        """
        
        for j in range(self._size):
            if self._grid[0][j] == TileType.EMPTY:
                self._grid[0][j] = TileType.FUTURE
    
    def _fill_step(self) -> bool:
        """
        Makes a step in the filling process. 
        
        Returns:
            True if the filling is complete, False otherwise.
        """
        s = [(i,j) for i in range(self._size) for j in range(self._size) if self._grid[i][j] == TileType.FUTURE]
        if len(s) == 0:
            return True
        
        for i, j in s:
            self._grid[i][j] = TileType.MATERIAL
            if i >= 1 and self._grid[i-1][j] == 0:
                self._grid[i-1][j] = TileType.FUTURE
            if i <= self._size-2 and self._grid[i+1][j] == 0:
                self._grid[i+1][j] = TileType.FUTURE
            if j >= 1 and self._grid[i][j-1] == 0:
                self._grid[i][j-1] = TileType.FUTURE
            if j <= self._size-2 and self._grid[i][j+1] == 0:
                self._grid[i][j+1] = TileType.FUTURE
        
        return False
    
    def fill_instantly(self, figsize: Tuple[int, int] = (12,6)) -> None:
        """
        Fills the grid with an animation.
        
        Args:
            figsize (Tuple[int, int]): The size of the figure
        """
        
        cmap = colors.ListedColormap(TileType.list_colors()) 
        _, ax = plt.subplots(1, 2, figsize=figsize)
        _vmin, _vmax = TileType.limits()
        ax[0].imshow(self._grid, cmap=cmap,vmin=_vmin,vmax=_vmax)

        self._instant_fill()
        ax[1].imshow(self._grid, cmap=cmap,vmin=_vmin,vmax=_vmax)

        plt.show()
    
    def fill_with_animation(self, figsize: Tuple[int, int] = (12,6)) -> None:
        """
        Fills and displays the grid.
        
        Args:
            figsize (Tuple[int, int]): The size of the figure
        """
        
        cmap = colors.ListedColormap(TileType.list_colors()) 
        fig, ax = plt.subplots(1, 2, figsize=figsize)
        _vmin, _vmax = TileType.limits()
        ax[0].imshow(self._grid, cmap=cmap,vmin=_vmin,vmax=_vmax)

        # Defining the animation
        def anim_start() -> None:
            self._prepare()
            l = ax[1].imshow(self._grid, cmap=cmap, vmin=_vmin, vmax=_vmax)
            return l

        def anim_step(_i) -> None:
            ax[1].clear()
            self._fill_step()
            l = ax[1].imshow(self._grid, cmap=cmap, vmin=_vmin, vmax=_vmax)
            return l
        
        _anim = animation.FuncAnimation(
            fig=fig,
            init_func=anim_start,
            func=anim_step,
        )
        
        plt.show()
        print(f"Maximum depth: {self._get_max_depth()}")