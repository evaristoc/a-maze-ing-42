from typing import (Any,
                    Optional)

from mazegen.map import (write_hexadecimal_map_to_file,
                         convert_cell_path_to_directions)

from mazegen.maze_factory import (Cell,
                                  Maze)

from mazegen.maze_solvers import (SinglePathSolver,
                                  ShortestPathSolver)


class MazeGenerator:
    def __init__(self,
                 width: Optional[int] = 10,
                 height: Optional[int] = 10,
                 seed: Optional[int] = 0):
        self.width = width
        self.height = height
        self.seed = seed
        self.maze_structure: Any = None
        self.solution: list = []
        self.maze: Maze
        self.packed_solution: list = []

    def generate(
        self,
        perfect: bool = True,
        entry: tuple = (0, 0),
        exit: tuple = (0, 0)
    ) -> None:
        """
        Coordinates the maze creation and solving.
        This will wrap your existing Maze, Builder, and Solver logic.
        """
        # 1. Logic to create the Maze instance with self.seed
        if self.width and self.height and self.seed:
            self.maze = Maze(self.width, self.height, self.seed)
        # 2. Logic to place the 42 glyph and entry/exit points
        self.maze.place_fourty_two_glyph_at_maze_center()
        self.maze.place_entry_and_exit_cells(entry, exit)
        self.entry = entry
        self.exit = exit

        # 3. Logic to trigger generate_perfect_maze or generate_simple_maze
        if perfect is True:
            self.maze.generate_perfect_maze()
            perfect_solver = SinglePathSolver(self.maze)
            self.solution = perfect_solver.solve()
        if perfect is False:
            self.maze.generate_simple_maze()
            simple_solver = ShortestPathSolver(self.maze)
            self.solution = simple_solver.solve()
        # 4. Logic to solve and store result in self.solution
        self.packed_solution = self.solution
        for path in self.solution:
            self.solution = path
        self.maze_structure = self.maze.two_dimensional_cell_grid

    def get_structure(self) -> Any:
        """Returns the maze structure (grid of cells)."""
        return self.maze_structure

    def get_solution(self) -> list:
        """Returns the calculated path for the solution."""
        return self.solution

    def get_directions(self) -> tuple[list[Cell],
                                      list[str]]:

        directions = convert_cell_path_to_directions(self.maze,
                                                     self.solution)

        sol_path = [(c, d) for c, d in zip(self.packed_solution[0][1:-1],
                                           directions[1:])]
        return sol_path

    def save(self, output_file: str) -> None:
        """Wraps the hexadecimal file writing logic."""
        write_hexadecimal_map_to_file(self.maze, self.entry, self.exit,
                                      self.solution,
                                      output_file
                                      )
