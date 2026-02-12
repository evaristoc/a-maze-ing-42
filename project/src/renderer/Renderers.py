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
        self.__padding = int(self.__interior_cell_size * .15)
        self.__cell_center = self.__interior_cell_size - 2 * self.__padding
        print("renderer: successfully instantiated; set maze rendering properties")

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
            self.__draw_background(target_img, state, elements["background"])    
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
                self.__draw_triangle_in_cell(target_img, 4, 4, 0xFFFFFFFF, "right")
                # if "path" in elements:
                #     self._path(target_img, state, elements["path"])

    def __get_total_size(self, num_cells_x: int, num_cells_y: int): # utils
        total_w = num_cells_x * self.__total_cell_size - self.__wall_thickness * (num_cells_x - 1)
        total_h = num_cells_y * self.__total_cell_size - self.__wall_thickness * (num_cells_y - 1)
        return total_w, total_h


    def __draw_background(self, target_img, state, color):
        pix_tot_w, pix_tot_h = self.__get_total_size(len(state[0]), len(state))
        for y in range(pix_tot_h):
            for x in range(pix_tot_w):
                target_img.put_pixel(x, y, color)


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

    def __draw_filled_triangle(self, img, x1, y1, x2, y2, x3, y3, color):
        min_y = min(y1, y2, y3)
        max_y = max(y1, y2, y3)

        for y in range(min_y, max_y + 1):
            intersections = []

            # check edge 1
            if y1 != y2 and min(y1, y2) <= y <= max(y1, y2):
                x = x1 + (x2 - x1) * (y - y1) // (y2 - y1)
                intersections.append(x)

            # check edge 2
            if y2 != y3 and min(y2, y3) <= y <= max(y2, y3):
                x = x2 + (x3 - x2) * (y - y2) // (y3 - y2)
                intersections.append(x)

            # check edge 3
            if y3 != y1 and min(y3, y1) <= y <= max(y3, y1):
                x = x3 + (x1 - x3) * (y - y3) // (y1 - y3)
                intersections.append(x)

            if len(intersections) == 2:
                x_start = min(intersections)
                x_end = max(intersections)

                for x in range(x_start, x_end + 1):
                    img.put_pixel(x, y, color)
   
    def __draw_triangle_in_cell(self, img, x_cell, y_cell, color, direction):

        start_x = self.__wall_thickness + x_cell * \
            (self.__interior_cell_size + self.__wall_thickness) + self.__padding

        start_y = self.__wall_thickness + y_cell * \
            (self.__interior_cell_size + self.__wall_thickness) + self.__padding

        size = self.__interior_cell_size
        margin = size // 5

        left = start_x + margin
        right = start_x + size - margin
        top = start_y + margin
        bottom = start_y + size - margin
        #bottom = start_y + size
        center_x = start_x + size // 2
        center_y = start_y + size // 2

        if direction == "up":
            x1, y1 = center_x, top
            x2, y2 = left, bottom
            x3, y3 = right, bottom

        elif direction == "down":
            x1, y1 = center_x, bottom
            x2, y2 = left, top
            x3, y3 = right, top

        elif direction == "left":
            x1, y1 = left, center_y
            x2, y2 = right, top
            x3, y3 = right, bottom

        elif direction == "right":
            x1, y1 = right, center_y
            x2, y2 = left, top
            x3, y3 = left, bottom

        else:
            return

        self.__draw_filled_triangle(img, x1, y1, x2, y2, x3, y3, color)