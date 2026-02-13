from src.maze_factory.cells import (Cell, ExitCell,
                                    EntryCell, FourtyTwoCell)
# from collect_config_variables import ConfigParser
import random
from abc import ABC
from src.collect_config_variables.error_handlers.config_errors import ConfigError


FOURTY_TWO_GLYPH = [
    [1, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1],
]


class Maze(ABC):
    """
    Represents the full maze structure and generation logic.
    """

    def __init__(
        self,
        maze_width_in_cells: int,
        maze_height_in_cells: int,
        random_generation_seed: int
    ):
        self.maze_width_in_cells = maze_width_in_cells
        self.maze_height_in_cells = maze_height_in_cells

        self.random_generation_seed = random_generation_seed
        self.random_number_generator = random.Random(
            random_generation_seed
        )

        self.default_wall_render_color = 0xFFFFFF

        self.two_dimensional_cell_grid: list[list[Cell]] = []
        self.maze_entry_cell: EntryCell | None = None
        self.maze_exit_cell: ExitCell | None = None
        self.maze_fourty_two_cell: FourtyTwoCell | None = None

        self._initialize_cell_grid()

    # ───────────── Grid Initialization ─────────────

    def _initialize_cell_grid(self) -> None:
        for y in range(self.maze_height_in_cells):
            row = []
            for x in range(self.maze_width_in_cells):
                row.append(Cell(x, y, 0b1111))
            self.two_dimensional_cell_grid.append(row)

    # ───────────── Utilities ─────────────

    def is_position_inside_maze_bounds(
        self,
        position_x: int,
        position_y: int
    ) -> bool:
        return (
            0 <= position_x < self.maze_width_in_cells
            and 0 <= position_y < self.maze_height_in_cells
        )

    def get_cell_at_position(
        self,
        position_x: int,
        position_y: int
    ) -> Cell:
        return self.two_dimensional_cell_grid[position_y][position_x]

    # ───────────── Wall Coherence ─────────────

    def remove_wall_between_two_adjacent_cells(
        self,
        first_cell: Cell,
        second_cell: Cell
    ) -> None:
        x1, y1 = first_cell.get_cell_position()
        x2, y2 = second_cell.get_cell_position()

        diffx = x2 - x1
        diffy = y2 - y1

        if diffx == 1:   # second is east
            first_cell.set_wall_bitmask(
                first_cell.get_wall_bitmask_binary() & ~0b0010
            )
            second_cell.set_wall_bitmask(
                second_cell.get_wall_bitmask_binary() & ~0b1000
            )

        elif diffx == -1:  # second is west
            first_cell.set_wall_bitmask(
                first_cell.get_wall_bitmask_binary() & ~0b1000
            )
            second_cell.set_wall_bitmask(
                second_cell.get_wall_bitmask_binary() & ~0b0010
            )

        elif diffy == 1:  # second is south
            first_cell.set_wall_bitmask(
                first_cell.get_wall_bitmask_binary() & ~0b0100
            )
            second_cell.set_wall_bitmask(
                second_cell.get_wall_bitmask_binary() & ~0b0001
            )

        elif diffy == -1:  # second is north
            first_cell.set_wall_bitmask(
                first_cell.get_wall_bitmask_binary() & ~0b0001
            )
            second_cell.set_wall_bitmask(
                second_cell.get_wall_bitmask_binary() & ~0b0100
            )

    # ───────────── Special Cells ─────────────

    def place_fourty_two_glyph_at_maze_center(self) -> None:
        """
        Places a 42 glyph made of fully-blocked FourtyTwoCell
        instances at the center of the maze.
        """

        glyph_height = len(FOURTY_TWO_GLYPH)
        glyph_width = len(FOURTY_TWO_GLYPH[0])

        center_x = self.maze_width_in_cells // 2
        center_y = self.maze_height_in_cells // 2

        top_left_x = center_x - glyph_width // 2
        top_left_y = center_y - glyph_height // 2

        try:
            if self.maze_height_in_cells < 7 or self.maze_width_in_cells < 7:
                raise ValueError
            for glyph_y in range(glyph_height):
                for glyph_x in range(glyph_width):
                    if FOURTY_TWO_GLYPH[glyph_y][glyph_x] == 1:
                        maze_x = top_left_x + glyph_x
                        maze_y = top_left_y + glyph_y

                        if not self.is_position_inside_maze_bounds(maze_x,
                                                                   maze_y):
                            continue

                        self.two_dimensional_cell_grid[maze_y][maze_x] = (
                            FourtyTwoCell(maze_x, maze_y)
                        )
        except ValueError:
            print("FourtyTwo Cells could not be placed.")
            return None

    def place_entry_and_exit_cells(self, entry_coords: tuple[int, int],
                                   exit_coords: tuple[int, int]) -> None:
        # Example: random boundary placement
        x_entry, y_entry = entry_coords
        x_exit, y_exit = exit_coords

        if self.is_position_inside_maze_bounds(x_entry, y_entry):
            self.maze_entry_cell = (EntryCell(x_entry, y_entry))
            self.two_dimensional_cell_grid[y_entry][x_entry] = (EntryCell
                                                                (x_entry,
                                                                 y_entry))
            if y_entry == self.maze_height_in_cells:
                self.remove_wall_between_two_adjacent_cells(
                    self.two_dimensional_cell_grid[y_entry]
                                                  [x_entry],
                    self.get_cell_at_position(x_entry, y_entry - 1)
                    )
            elif 0 >= y_entry < self.maze_height_in_cells:
                self.remove_wall_between_two_adjacent_cells(
                    self.two_dimensional_cell_grid[y_entry]
                                                  [x_entry],
                    self.get_cell_at_position(x_entry, y_entry + 1)
                    )

        if self.is_position_inside_maze_bounds(x_exit, y_exit):
            self.two_dimensional_cell_grid[y_exit][x_exit] = (ExitCell
                                                              (x_exit,
                                                               y_exit))
            self.maze_exit_cell = (ExitCell(x_exit, y_exit))
            if x_exit == self.maze_height_in_cells:
                self.remove_wall_between_two_adjacent_cells(
                    self.two_dimensional_cell_grid[y_exit]
                                                  [x_exit],
                    self.get_cell_at_position(x_exit - 1, y_exit)
                    )
            elif 0 >= x_exit < self.maze_width_in_cells:
                self.remove_wall_between_two_adjacent_cells(
                    self.two_dimensional_cell_grid[y_exit]
                                                  [x_exit],
                    self.get_cell_at_position(x_exit + 1, y_exit)
                    )

    def get_adjacent_cells(self, cell):
        """
        Returns a list of orthogonally adjacent cells (N, E, S, W)
        that are inside the maze bounds.
        """
        adjacent_cells = []

        x, y = cell.cell_position_x, cell.cell_position_y

        # North
        if self.is_position_inside_maze_bounds(x, y - 1):
            adjacent_cells.append(
                self.get_cell_at_position(x, y - 1)
            )

        # East
        if self.is_position_inside_maze_bounds(x + 1, y):
            adjacent_cells.append(
                self.get_cell_at_position(x + 1, y)
            )

        # South
        if self.is_position_inside_maze_bounds(x, y + 1):
            adjacent_cells.append(
                self.get_cell_at_position(x, y + 1)
            )

        # West
        if self.is_position_inside_maze_bounds(x - 1, y):
            adjacent_cells.append(
                self.get_cell_at_position(x - 1, y)
            )

        return adjacent_cells

    def get_adjacent_cells_with_directions(self, cell):
        """
        Returns a list of tuples:
        (adjacent_cell, direction_from_cell)
        """
        neighbors = []

        x, y = cell.cell_position_x, cell.cell_position_y

        if self.is_position_inside_maze_bounds(x, y - 1):
            neighbors.append(
                (self.get_cell_at_position(x, y - 1), "north")
            )

        if self.is_position_inside_maze_bounds(x + 1, y):
            neighbors.append(
                (self.get_cell_at_position(x + 1, y), "east")
            )

        if self.is_position_inside_maze_bounds(x, y + 1):
            neighbors.append(
                (self.get_cell_at_position(x, y + 1), "south")
            )

        if self.is_position_inside_maze_bounds(x - 1, y):
            neighbors.append(
                (self.get_cell_at_position(x - 1, y), "west")
            )

        return neighbors

    # ───────────── Abstract Generation ─────────────

    def generate_simple_maze(self) -> None:
        from src.maze_path_generators.simple_generator import (
            SimpleMazeGenerator
        )

        SimpleMazeGenerator(self).generate()

    def generate_perfect_maze(self) -> None:
        from src.maze_path_generators.perfect_dfs_generator import (
            PerfectMazeDFSGenerator
        )

        PerfectMazeDFSGenerator(self).generate()

    # ------------- Random Wall Remover/algorithm-------------

    def get_unvisited_neighbors(self, cell: Cell, visited: set) -> list:

        neighbors = []

        for neighbor in self.get_adjacent_cells(cell):
            if neighbor not in visited and neighbor.is_walkable():
                neighbors.append(neighbor)

        return neighbors

    def randomly_remove_some_walls(
        self,
        wall_removal_probability: float = 0.7
    ) -> None:
        """
        Randomly removes walls between adjacent cells
        with a given probability.

        This method:
        - preserves wall coherence
        - avoids removing walls next to blocked cells
        - is deterministic via the maze seed
        """

        for y in range(self.maze_height_in_cells):
            for x in range(self.maze_width_in_cells):
                current_cell = self.get_cell_at_position(x, y)

                if not current_cell.is_walkable():
                    continue

                # Only consider east and south to avoid duplicates
                directions = [
                    (1, 0),   # east
                    (0, 1),   # south
                ]

                for dx, dy in directions:
                    neighbor_x = x + dx
                    neighbor_y = y + dy

                    if not self.is_position_inside_maze_bounds(neighbor_x,
                                                               neighbor_y):
                        continue

                    neighbor_cell = self.get_cell_at_position(neighbor_x,
                                                              neighbor_y)

                    if not neighbor_cell.is_walkable():
                        continue

                    if self.random_number_generator.random(
                    ) < wall_removal_probability:

                        self.remove_wall_between_two_adjacent_cells(
                            current_cell,
                            neighbor_cell
                        )

    def print_maze_to_stdout(self, solution=None,
                             path_directions=None) -> None:
        """
        Prints an ASCII representation of the maze
        based on the wall bitmask of each cell.
        """

        solution = solution or []
        path_directions = path_directions or []

        width = self.maze_width_in_cells
        height = self.maze_height_in_cells

        FULL_BLOCK = "\033[91m███\033[0m"
        ENTRY = "\033[94mENT\033[0m"
        EXIT = "\033[95mEXT\033[0m"
        PATH = "\033[92m███\033[0m"
        EMPTY_BLOCK = "   "

        DIR_TO_ARROW = {
            "NORTH": "\033[92m ⟰ \033[0m",
            "EAST":  "\033[92m ⭆ \033[0m",
            "SOUTH": "\033[92m ⟱ \033[0m",
            "WEST":  "\033[92m ⭅ \033[0m",
        }

        # Build arrow map: cell -> arrow
        arrow_map = {}
        if path_directions and len(solution) >= 2:
            for cell, direction in zip(solution, path_directions):
                arrow_map[cell] = DIR_TO_ARROW.get(direction, PATH)

            # Final cell (no outgoing direction)
            arrow_map[solution[-1]] = PATH

        # ───────────── Top boundary ─────────────
        for _ in range(width):
            print("+---", end="")
        print("+")

        # ───────────── Rows ─────────────
        for y in range(height):
            print("|", end="")

            for x in range(width):
                cell = self.get_cell_at_position(x, y)

                if isinstance(cell, FourtyTwoCell):
                    print(FULL_BLOCK, end="")

                elif isinstance(cell, EntryCell):
                    print(ENTRY, end="")

                elif isinstance(cell, ExitCell):
                    print(EXIT, end="")

                elif cell in arrow_map:
                    print(arrow_map[cell], end="")

                elif cell in solution:
                    print(PATH, end="")

                else:
                    print(EMPTY_BLOCK, end="")

                print("|" if cell.has_east_wall() else " ", end="")

            print()

            for x in range(width):
                cell = self.get_cell_at_position(x, y)
                print("+", end="")
                print("---" if cell.has_south_wall() else "   ", end="")

            print("+")

    def get_hexadecimal_wall_map(self) -> list[list[str]]:
        """
        Returns a 2D list representing the maze walls in hexadecimal form.
        Each entry corresponds to a cell.
        """
        hexadecimal_map: list[list[str]] = []

        for row in self.two_dimensional_cell_grid:
            hexadecimal_row: list[str] = []
            for cell in row:
                hexadecimal_row.append(cell.get_wall_bitmask_hexadecimal())
            hexadecimal_map.append(hexadecimal_row)

        return hexadecimal_map
