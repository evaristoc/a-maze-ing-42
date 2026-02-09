from abc import ABC, abstractmethod
from src.maze_factory import Maze


class MazePathGenerator(ABC):
    """
    Base interface for all maze generation algorithms.
    """

    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    @abstractmethod
    def generate(self) -> None:
        """
        Modifies the maze in-place.
        """
        pass
