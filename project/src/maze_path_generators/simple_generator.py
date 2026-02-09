from src.maze_path_generators.base_generator import MazePathGenerator

from src.maze_path_generators.perfect_dfs_generator import (
    PerfectMazeDFSGenerator)


class SimpleMazeGenerator(MazePathGenerator):
    """
    Generates a simple maze by adding loops to a perfect maze.
    """

    def generate(self) -> None:
        # Step 1: perfect maze
        perfect_generator = PerfectMazeDFSGenerator(self.maze)
        perfect_generator.generate()

        # Step 2: add random loops
        self.maze.randomly_remove_some_walls(
            0.15
        )
