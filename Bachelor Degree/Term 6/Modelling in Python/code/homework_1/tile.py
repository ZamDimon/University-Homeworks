from __future__ import annotations
from typing import List, Tuple
from enum import IntEnum

class TileType(IntEnum):
    """
    Class responsible for storing information about a tile on the grid
    """
    
    EMPTY = 0 # The tile is empty
    OBSTACLE = 1 # The tile is an obstacle
    MATERIAL = 2 # The tile is a material (e.g., water or electricity)
    FUTURE = 3 # The tile which is about to be filled
    
    @staticmethod
    def from_int(value: int) -> TileType:
        """
        Converts an integer to a TileType
        
        Args:
            value (int): The integer to convert
        
        Returns:
            TileType: The corresponding TileType
        """
        return TileType(value)
    
    @classmethod
    def to_color(cls, value: int) -> str:
        """
        Converts a TileType to a color
        
        Args:
            value (int): The integer to convert
        
        Returns:
            str: The corresponding color
        """
        
        return {
            cls.EMPTY: 'whitesmoke',
            cls.OBSTACLE: 'dimgrey',
            cls.MATERIAL: 'blue',
            cls.FUTURE: 'cornflowerblue'
        }[value]
        
    @staticmethod
    def list_colors() -> List[str]:
        """
        Returns a list of colors for each TileType
        
        Returns:
            List[str]: A list of colors
        """
        
        return [TileType.to_color(t.value) for t in TileType]
    
    @staticmethod
    def limits() -> Tuple[int, int]:
        """
        Returns minimum and maximum values for TileType
        
        Returns:
            List[int]: A list of limits
        """
        
        return (min(TileType), max(TileType))