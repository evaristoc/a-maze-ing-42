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
        "background": 0xFF222222,
        "fortytwo": 0xFFFFFFFF,
        "entrance": 0xFF00FF00,
        "exit": 0xFFFF00FF,
        "walls": 0xFFAAAAAA,
        "path": 0xFF00FF00}
    
    def __init__(self, cell_size: int = 25, padding: int = 5, wall_thickness: int = 10) -> None:
        self.cell_size = cell_size
        self.wall_thickness = wall_thickness
        self.padding = padding

    def __get_total_size(self, num_cells_x: int, num_cells_y: int):
        total_w = num_cells_x * self.cell_size + self.wall_thickness * (num_cells_x + 1)
        total_h = num_cells_y * self.cell_size + self.wall_thickness * (num_cells_y + 1)
        return total_w, total_h

    def draw(self,
    target_img: any,
    state: any,
    elements: dict[str, int] = None) -> None:
        elements = elements or self.DEFAULT_COLOURS
        pixel_totwidth, pixel_totheight = __get_total_size(len(state[0], len(state)))
        if "background" in elements:
            self.__background(target_img, pixel_totwidth, pixel_totheight, elements["background"])
        if "fortytwo" in elements:
            self.__draw_cells_interior(target_img, pixel_totwidth, pixel_totheight, elements["fortytwo"])
        # if "entrance" in elements:
        #     self._entrance(target_img, state, elements["entrance"])
        # if "exit" in elements:
        #     self._exit(target_img, state, elements["exit"])
        # if "walls" in elements:
        #     self._walls(target_img, state, elements["walls"])  
        #     self._border_walls(target_img, state, elements["walls"])       
        # if "path" in elements:
        #     self._path(target_img, state, elements["path"])
    
    def __get_safe_cell_anchors(target, cols, rows, wall_thick, padding, cell_size):
        unit_size = wall_thick + (2 * padding) + cell_size
        sl = target.stride
        max_mem = target.height * sl
        
        # Pre-calculate jumps
        v_jump = unit_size * sl
        h_jump = unit_size * 4
        
        start_y = (wall_thick + padding) * sl
        start_x = (wall_thick + padding) * 4

        for r in range(rows):
            row_mem = start_y + (r * v_jump)
            # STOP 1: If the start of the row is already outside the image
            if row_mem >= max_mem:
                break
            for c in range(cols):
                col_mem = start_x + (c * h_jump)
                # STOP 2: Ensure the entire square fits horizontally within the stride
                if (col_mem + (cell_size * 4)) > sl:
                    continue # Skip this column, it's in the padding zone
                # STOP 3: Ensure the entire square fits vertically
                if (row_mem + (cell_size * sl)) > max_mem:
                    break
                yield (row_mem, col_mem)

    def __draw_cell_interior(self, target_img, x_cell: int, y_cell: int, color: int):
        start_x = self.wall_thickness + x_cell * (self.cell_size + self.wall_thickness) + self.padding
        start_y = self.wall_thickness + y_cell * (self.cell_size + self.wall_thickness) + self.padding
        interior_size = self.cell_size - 2 * self.padding

        for dy in range(interior_size):
            for dx in range(interior_size):
                target_img.put_pixel(start_x + dx, start_y + dy, color)

    def __draw_cells():
        for cell in __get_safe_cell_anchors(target, len(state[0]), len(state), wall_thick, padding, cell_size)
            __draw_cell_interior(self, target_img, x_cells: int, y_cells: int, color: int)

    # def _fortytwo(self, target_img: any, state: any, color: int):
    #     """
    #     Draw all FortyTwo cells in the maze.
    #     Each cell is n x n pixels:
    #     - walls included
    #     - interior: (n-wallstroke-padding) x (n-wallstroke-padding) pixels
    #     - padding: padding (px) from top-left corner of cell
    #     """
    #     cell_size = self.cell_size
    #     padding = self.padding
    #     interior_size = cell_size - padding - self.wall_stroke * 2

    #     # Iterate over all cells in the maze
    #     for y, row in enumerate(state):
    #         for x, cell in enumerate(row):
    #             if not isinstance(cell, FourtyTwoCell):
    #                 continue

    #             # Calculate top-left corner of the cell in pixels
    #             start_x = x * cell_size + padding
    #             start_y = y * cell_size + padding

    #             # Paint interior
    #             for dy in range(interior_size):
    #                 for dx in range(interior_size):
    #                     px = start_x + dx
    #                     py = start_y + dy
    #                     #print("inside fortytwo")
    #                     target_img.put_pixel(px, py, color)


    def __draw_walls(self, target_img, x_cell: int, y_cell: int, cell, color: int):
        base_x = x_cell * (self.cell_size + self.wall_thickness)
        base_y = y_cell * (self.cell_size + self.wall_thickness)

        # East wall (vertical)
        if cell.has_east_wall():
            wall_x = base_x + self.cell_size
            for dx in range(self.wall_thickness):
                for dy in range(self.cell_size + self.wall_thickness):
                    target_img.put_pixel(wall_x + dx, base_y + dy, color)

        # South wall (horizontal)
        if cell.has_south_wall():
            wall_y = base_y + self.cell_size
            for dy in range(self.wall_thickness):
                for dx in range(self.cell_size + self.wall_thickness):
                    target_img.put_pixel(base_x + dx, wall_y + dy, color)

   def _border_walls(self, target_img, state, color):
        """
        Draw north and west border walls for the first row and column.
        """
        # height_in_cells = len(state)
        # width_in_cells = len(state[0])

        # Top border (north)
        for x in range(width_in_cells):
            base_x = x * self.cell_size
            for dx in range(self.cell_size):
                for t in range(self.wall_thickness):
                    target_img.put_pixel(base_x + dx, t, color)

        # Left border (west)
        for y in range(height_in_cells):
            base_y = y * self.cell_size
            for dy in range(self.cell_size):
                for t in range(self.wall_thickness):
                    target_img.put_pixel(t, base_y + dy, color)

    # def _walls(self, target_img, state, color):
    #     for y, row in enumerate(state):
    #         for x, cell in enumerate(row):
    #             # cell = state.cells[y][x]

    #             base_x = x * self.cell_size
    #             base_y = y * self.cell_size

    #             # South wall (horizontal)
    #             if cell.has_south_wall():
    #                 wall_y = base_y + self.cell_size - self.wall_stroke
    #                 for dx in range(self.cell_size):
    #                     target_img.put_pixel(base_x + dx, wall_y, color)

    #             # East wall (vertical)
    #             if cell.has_east_wall():
    #                 wall_x = base_x + self.cell_size - self.wall_stroke
    #                 for dy in range(self.cell_size):
    #                     target_img.put_pixel(wall_x, base_y + dy, color)


    # def _border_walls(self, target_img, state, color):
    #     # Top border
    #     for x in range(state.width):
    #         base_x = x * self.cell_size
    #         for dx in range(self.cell_size):
    #             target_img.put_pixel(base_x + dx, 0, color)

    #     # Left border
    #     for y in range(state.height):
    #         base_y = y * self.cell_size
    #         for dy in range(self.cell_size):
    #             target_img.put_pixel(0, base_y + dy, color)

    def _background(self, target_img, color):
        # cell_size = self.cell_size
        # height_in_cells = len(state)
        # width_in_cells = len(state[0])

        # H = height_in_cells * cell_size
        # W = width_in_cells * cell_size

        # for y in range(H):
        #     for x in range(W):
        #         target_img.put_pixel(x, y, 0x00FF00FF)
        # Add some red pixels
        # pixel_positions = [
        #     0 * 200 * 4,                   # top left
        #     (1 * 200 + 1) * 4,             # top left + 1
        #     (199 * 200 + 199) * 4,         # bottom right
        #     (198 * 200 + 198) * 4,          # bottom right - 1
        #     (197 * 200 + 197) * 4,          # bottom right - 1
        #     (196 * 200 + 196) * 4,          # bottom right - 1
        # ]
        # print(len(target_img.data))
        # for pos in pixel_positions:
        #     if pos < len(target_img.data) - 3:
        #         print(target_img.data[pos:pos+4])
        #         target_img.data[pos:pos+4] = (0xFFFF0000).to_bytes(4, 'little')
        #         print(target_img.data[pos:pos+4])

        #TODO: move this to Image:
        for pixel in range(0, len(target_img.data), 4):
            target_img.data[pixel:pixel+4] = (color).to_bytes(4, 'little')

    # TODO finish the following functions
    def _path():
        pass

    def _entrance():
        pass

    def _exit():
        pass
   