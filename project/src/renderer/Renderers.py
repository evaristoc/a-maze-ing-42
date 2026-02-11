# """
# TODO
# - [ ] reset the optimizations (walls, background) to be more cell based
# - [ ] include a hall drawer
# - [ ] prepare for the use of triangles to indicate path
# - [ ] refine the use of padding for the hall painting (use options instead of a single color arg)
# - [ ] evaluate the use of generators for a better control of streams
# - [ ] cell renderer class?
# - [ ] solve the origin issue, probably moving everything to the very top left corner?
# - [ ] treating the whole wall as a single block instead of separated walls? Facilitate animations and pattern strokes
# """


from src.maze_factory.cells import (ExitCell,
                                    EntryCell, FourtyTwoCell)
from src.renderer.Image import Image

class Renderer:
    # """Abstract/generic renderer: only knows ImageBuffer"""
    def draw(self, target: any, state: any, elements: list[str] = None) -> None:
        """Show the image; MLX handled in boundary layer"""
        pass


class MazeRenderer(Renderer):
    """Maze-specific renderer"""
    DEFAULT_COLORS = {
        "background": 0xFF2200FF,
        "fourtytwo": 0xFFFFFFFF,
        "entrance": 0xFF00FF00,
        "exit": 0xFFFF00FF,
        "walls": 0xFF00AAAA,
        "path": 0xFF00FF00,
    }
    
    def __init__(self, total_cell_size: int = 50) -> None:
        self.__total_cell_size = total_cell_size
        self.__wall_thickness = int(self.__total_cell_size * .2)
        self.__interior_cell_size = self.__total_cell_size - 2 * self.__wall_thickness
        self.__padding = int(self.__interior_cell_size * .1)
        self.__cell_center = self.__interior_cell_size - 2 * self.__padding

    def draw(self,
    target_img: any,
    state: any,
    elements: dict[str, int] = None) -> None:
    # """
    # - background will paint all the image, including under walls, with a single color (not led by cell)
    # - fortytwo, entrance and exit will paint a padded interior (led by cell)
    # - walls will be painted by cell if east / south; north / west will be painted as a single line
    #   - the way walls are painted constrains customization
    # - padding is not painted (it is the color of background)
    # - open channels between cells are background coloured
    # """
        elements = elements or self.DEFAULT_COLORS
        # we paint everything with background if background (almost like clearing)
        if "background" in elements:
            print("background")
            self.__draw_background(target_img, state, elements["background"])
            # for x_img in range(pix_totw):
            #     for y_img in range(pix_toth):
            #         target_img.put_pixel(x_img, y_img, elements["background"])
        
        for r in state:
            for c in r:
                # let's paint the walls already...
                if "walls" in elements: 
                    # east south of each cell first
                    self.__cell_walls(target_img, c.cell_position_x, c.cell_position_y, c, elements["walls"])
                    # the rest is top and left border
                    #self.__topleft_borders(target_img, state, options["walls"])
                # we paint fortytwo, then walls, then entrance / exit cell by cell
                if "fourtytwo" in elements and isinstance(c, FourtyTwoCell):
                    self.__draw_cell_interior(target_img, c.cell_position_x, c.cell_position_y, elements["fourtytwo"])
                if "entrance" in elements and isinstance(c, EntryCell):
                    self.__draw_cell_interior(target_img, c.cell_position_x, c.cell_position_y, elements["entrance"])
                if "exit" in elements and isinstance(c, ExitCell):
                    self.__draw_cell_interior(target_img, c.cell_position_x, c.cell_position_y, elements["exit"])
                # if "path" in elements:
                #     self._path(target_img, state, elements["path"])

    def __get_total_size(self, num_cells_x: int, num_cells_y: int): # utils
        total_w = num_cells_x * self.__total_cell_size - self.__wall_thickness * (num_cells_x - 1)
        total_h = num_cells_y * self.__total_cell_size - self.__wall_thickness * (num_cells_y - 1)
        return total_w, total_h


    def __draw_background(self, target_img, state, color):
        pix_tot_w, pix_tot_h = self.__get_total_size(len(state[0]), len(state))
        print(pix_tot_w, pix_tot_h)
        for y in range(pix_tot_h):
            for x in range(pix_tot_w):
                target_img.put_pixel(x, y, 0xFF5500FF)


    def __draw_cell_interior(self, target_img: Image, x_cell: int, y_cell: int, color: int) -> None:
        # map through translation formula x_cell, y_cell coordinates to the position 
        # of the corner of the renderered interior to be painted
        start_x = self.__wall_thickness + x_cell * (self.__interior_cell_size + self.__wall_thickness) + self.__padding
        start_y = self.__wall_thickness + y_cell * (self.__interior_cell_size + self.__wall_thickness) + self.__padding
        

        # paint the interior
        for dy in range(self.__cell_center):
            for dx in range(self.__cell_center):
                target_img.put_pixel(start_x + dx, start_y + dy, color)


    def __cell_walls(self, target_img, x_cell: int, y_cell: int, cell, color: int):
        #TODO find a solution when x_cell and y_cell are 0 for cell north and west

        start_x = x_cell * (self.__total_cell_size - self.__wall_thickness)
        start_y = y_cell * (self.__total_cell_size - self.__wall_thickness)

        if cell.has_north_wall():
            for dx in range(self.__total_cell_size): # width (has to cover not 1 but two walls)
                for dy in range(self.__wall_thickness): # height (just one wall)
                    target_img.put_pixel(start_x + dx, start_y + dy, color)

        if cell.has_west_wall():
            for dx in range(self.__wall_thickness): # this is the wall width
                for dy in range(self.__total_cell_size): # this is the wall height
                    target_img.put_pixel(start_x + dx, start_y + dy, color) # paint between range witdh and start height
            
        # East wall (vertical)
        if cell.has_east_wall():
            wall_x = start_x + self.__interior_cell_size + self.__wall_thickness # walk right
            for dx in range(self.__wall_thickness): # this is the wall width
                for dy in range(self.__total_cell_size): # this is the wall height
                    target_img.put_pixel(wall_x + dx, start_y + dy, color) # paint between range width and start height

        # South wall (horizontal)
        if cell.has_south_wall():
            wall_y = start_y + self.__interior_cell_size + self.__wall_thickness # walk down
            for dy in range(self.__wall_thickness): # this is the the wall height
                for dx in range(self.__total_cell_size): # this is the wall width
                    target_img.put_pixel(start_x + dx, wall_y + dy, color) # paint between start width and range height


#     def __get_safe_cell_anchors(target_img, cols, rows, wall_thick, padding, cell_size):
#         unit_size = wall_thick + (2 * padding) + cell_size
#         sl = target_img.stride
#         max_mem = target_img.height * sl
        
#         # Pre-calculate jumps
#         v_jump = unit_size * sl
#         h_jump = unit_size * 4
        
#         start_y = (wall_thick + padding) * sl
#         start_x = (wall_thick + padding) * 4

#         for r in range(rows):
#             row_mem = start_y + (r * v_jump)
#             # STOP 1: If the start of the row is already outside the image
#             if row_mem >= max_mem:
#                 break
#             for c in range(cols):
#                 col_mem = start_x + (c * h_jump)
#                 # STOP 2: Ensure the entire square fits horizontally within the stride
#                 if (col_mem + (cell_size * 4)) > sl:
#                     continue # Skip this column, it's in the padding zone
#                 # STOP 3: Ensure the entire square fits vertically
#                 if (row_mem + (cell_size * sl)) > max_mem:
#                     break
#                 yield (row_mem, col_mem)

# def __draw_cell_interior(self, target_img, x_cell: int, y_cell: int, color: int):
#     # 1. Calculate Logical Start Coordinates
#     start_x = self.wall_thickness + x_cell * (self.cell_size + self.wall_thickness) + self.padding
#     start_y = self.wall_thickness + y_cell * (self.cell_size + self.wall_thickness) + self.padding
#     interior_size = self.cell_size - 2 * self.padding

#     # 2. Pre-calculate the absolute starting byte offset
#     # This is the ONLY time we do the full coordinate math.
#     base_offset = (start_y * target_img.sl) + (start_x * 4)

#     for dy in range(interior_size):
#         # 3. Jump to the start of the current row using the stride
#         row_ptr = base_offset + (dy * target_img.sl)
        
#         for dx in range(interior_size):
#             # 4. Direct memory write using the offset
#             # We add (dx * 4) to move across the row 4 bytes at a time
#             target_img.set_pixel_at_offset(row_ptr + (dx * 4), color)

#     def __draw_cells():
#         for cell in __get_safe_cell_anchors(target, len(state[0]), len(state), wall_thick, padding, cell_size)
#             __draw_cell_interior(self, target_img, x_cells: int, y_cells: int, color: int)

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

    # def _background(self, target_img, color):
    #     # cell_size = self.cell_size
    #     # height_in_cells = len(state)
    #     # width_in_cells = len(state[0])

    #     # H = height_in_cells * cell_size
    #     # W = width_in_cells * cell_size

    #     # for y in range(H):
    #     #     for x in range(W):
    #     #         target_img.put_pixel(x, y, 0x00FF00FF)
    #     # Add some red pixels
    #     # pixel_positions = [
    #     #     0 * 200 * 4,                   # top left
    #     #     (1 * 200 + 1) * 4,             # top left + 1
    #     #     (199 * 200 + 199) * 4,         # bottom right
    #     #     (198 * 200 + 198) * 4,          # bottom right - 1
    #     #     (197 * 200 + 197) * 4,          # bottom right - 1
    #     #     (196 * 200 + 196) * 4,          # bottom right - 1
    #     # ]
    #     # print(len(target_img.data))
    #     # for pos in pixel_positions:
    #     #     if pos < len(target_img.data) - 3:
    #     #         print(target_img.data[pos:pos+4])
    #     #         target_img.data[pos:pos+4] = (0xFFFF0000).to_bytes(4, 'little')
    #     #         print(target_img.data[pos:pos+4])

    #     #TODO: move this to Image:
    #     for pixel in range(0, len(target_img.data), 4):
    #         target_img.data[pixel:pixel+4] = (color).to_bytes(4, 'little')

    #     def __eastsouth_cell_walls(self, target_img, x_cell: int, y_cell: int, cell, color: int):
#         start_x = x_cell * (self.cell_size + self.wall_thickness)
#         start_y = y_cell * (self.cell_size + self.wall_thickness)
            
#         # East wall (vertical)
#         if cell.has_east_wall():
#             wall_x = start_x + self.cell_size
#             for dx in range(self.wall_thickness):
#                 for dy in range(self.cell_size + self.wall_thickness):
#                     target_img.put_pixel(wall_x + dx, start_y + dy, color)

#         # South wall (horizontal)
#         if cell.has_south_wall():
#             wall_y = start_y + self.cell_size
#             for dy in range(self.wall_thickness):
#                 for dx in range(self.cell_size + self.wall_thickness):
#                     target_img.put_pixel(start_x + dx, wall_y + dy, color)

#    def __topleft_borders(self, target_img, state, color):
#         """
#         Draw north and west border walls for the first row and column.
#         """
#         # height_in_cells = len(state)
#         # width_in_cells = len(state[0])

#         # Top border (north)
#         for x in range(width_in_cells):
#             base_x = x * self.cell_size
#             for dx in range(self.cell_size):
#                 for t in range(self.wall_thickness):
#                     target_img.put_pixel(base_x + dx, t, color)

#         # Left border (west)
#         for y in range(height_in_cells):
#             base_y = y * self.cell_size
#             for dy in range(self.cell_size):
#                 for t in range(self.wall_thickness):
#                     target_img.put_pixel(t, base_y + dy, color)

   