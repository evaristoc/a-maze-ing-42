#from abc import ABC
from src.maze_factory.cells import (Cell, ExitCell,
                                    EntryCell, FourtyTwoCell)

class Renderer:
    # """Abstract/generic renderer: only knows ImageBuffer"""
    def draw(self, target: any, state: any, elements: list[str] = None) -> None:
        """Show the image; MLX handled in boundary layer"""
        pass


class MazeRenderer(Renderer):
    """Maze-specific renderer"""
    DEFAULT_COLOURS = {
        "background": 0x00222222,
        "fortytwo": 0x00FFFFFF,
        "entrance": 0x0000FF00,
        "exit": 0x00FF00FF,
        "walls": 0x00AAAAAA,
        "path": 0x0000FF00}
    
    def __init__(self, cell_size: int) -> None:
        self.cell_size = cell_size #one direction
        self.padding  = 2
        self.wall_stroke = 1
        # self.interior = cell_size - 2 #one direction
        # self.num_walls = 2 #one direction

    def draw(self,
    target_img: any,
    state: any,
    elements: dict[str, int] = None) -> None:
        elements = elements or self.DEFAULT_COLOURS
        if "background" in elements:
            self._background(target_img, state, elements["background"])
        if "fortytwo" in elements:
            self._fortytwo(target_img, state, elements["fortytwo"])
        # if "entrance" in elements:
        #     self._entrance(target_img, state, elements["entrance"])
        # if "exit" in elements:
        #     self._exit(target_img, state, elements["exit"])
        # if "walls" in elements:
        #     self._walls(target_img, state, elements["walls"])  
        #     self._border_walls(target_img, state, elements["walls"])       
        # if "path" in elements:
        #     self._path(target_img, state, elements["path"])
    
    def _fortytwo(self, target_img: any, state: any, color: int):
        """
        Draw all FortyTwo cells in the maze.
        Each cell is 7x7 pixels:
        - walls included
        - interior: 3x3 pixels
        - padding: 2px from top-left corner of cell
        """
        cell_size = self.cell_size
        padding = self.padding
        interior_size = cell_size - padding - self.wall_stroke * 2

        # Iterate over all cells in the maze
        for y, row in enumerate(state):
            for x, cell in enumerate(row):
                if not isinstance(cell, FourtyTwoCell):
                    continue

                # Calculate top-left corner of the cell in pixels
                start_x = x * cell_size + padding
                start_y = y * cell_size + padding

                # Paint interior
                for dy in range(interior_size):
                    for dx in range(interior_size):
                        px = start_x + dx
                        py = start_y + dy
                        #print("inside fortytwo")
                        target_img.put_pixel(px, py, 0x00FF00FF)

    def _walls(self, target_img, state, color):
        for y, row in enumerate(state):
            for x, cell in enumerate(row):
                # cell = state.cells[y][x]

                base_x = x * self.cell_size
                base_y = y * self.cell_size

                # South wall (horizontal)
                if cell.has_south_wall():
                    wall_y = base_y + self.cell_size - self.wall_stroke
                    for dx in range(self.cell_size):
                        target_img.put_pixel(base_x + dx, wall_y, color)

                # East wall (vertical)
                if cell.has_east_wall():
                    wall_x = base_x + self.cell_size - self.wall_stroke
                    for dy in range(self.cell_size):
                        target_img.put_pixel(wall_x, base_y + dy, color)


    def _border_walls(self, target_img, state, color):
        # Top border
        for x in range(state.width):
            base_x = x * self.cell_size
            for dx in range(self.cell_size):
                target_img.put_pixel(base_x + dx, 0, color)

        # Left border
        for y in range(state.height):
            base_y = y * self.cell_size
            for dy in range(self.cell_size):
                target_img.put_pixel(0, base_y + dy, color)

    def _background(self, target_img, state, color):
        cell_size = self.cell_size
        height_in_cells = len(state)
        width_in_cells = len(state[0])

        H = height_in_cells * cell_size
        W = width_in_cells * cell_size

        for y in range(H):
            for x in range(W):
                target_img.put_pixel(x, y, color) 

    # TODO finish the following functions
    def _path():
        pass

    def _entrance():
        pass

    def _exit():
        pass
   