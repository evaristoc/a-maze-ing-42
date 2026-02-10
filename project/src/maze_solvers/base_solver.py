from abc import ABC, abstractmethod
from src.maze_factory import Maze
from src.maze_factory import Cell


class MazeSolver(ABC):

    def __init__(self, maze: Maze):
        self.maze = maze

    @abstractmethod
    def solve(self) -> list[list[Cell]]:
        """
        Returns a list of paths.
        Each path is a list of Cells.
        """
        pass
