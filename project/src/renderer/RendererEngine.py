from typing import cast
from src.maze_factory.cells import (
                                        Cell,
                                        ExitCell,
                                        EntryCell,
                                        FourtyTwoCell
                                    )
from src.renderer.Image import Image


class Renderer:
    """Base renderer managing draw / animations state."""

    _renderer_queue: list
    _animations: dict[str, dict]

    @property
    def renderer_queue(self) -> list:
        return self._renderer_queue

    @renderer_queue.setter
    def renderer_queue(self, rend_q: list = []) -> None:
        self._renderer_queue = rend_q

    @property
    def animations(self) -> dict[str, dict]:
        return self._animations

    @animations.setter
    def animations(self, a: dict[str, dict]) -> None:
        self._animations = a

    def draw(
        self,
        target: Image,
        state: list[list[Cell | tuple[Cell, str]]],
        els: dict[str, int] | None
    ) -> None:
        """generic drawer: only knows image buffer"""
        pass


class MazeRenderer(Renderer):
    """Maze-specific renderer"""

    DEFAULT_COLORS = {
        "background": 0xFF5500FF,
        "fourtytwo": 0xFFFFFFFF,
        "entrance": 0xFF00FF00,
        "exit": 0xFFFF00FF,
        "walls": 0xFF00AAAA,
        "path": 0xFF00FF00,
    }

    def __init__(
        self,
        total_cell_size: int = 50,
        perc_wall: float = .2,
        perc_padding: float = .2
    ) -> None:
        """Initialize maze rendering geometry and sizing parameters."""

        self.__perc_wall = perc_wall
        self.__perc_padding = perc_padding
        self.__total_cell_size = total_cell_size
        # above is not private because we want to adjust them
        # when reloading the maze.
        self.__wall_thickness = int(self.__total_cell_size * self.__perc_wall)
        self.__interior_cell_size = self.__total_cell_size - 2 * \
            self.__wall_thickness
        self.__padding = int(self.__interior_cell_size * self.__perc_padding)
        self.__cell_center = self.__interior_cell_size - 2 * self.__padding
        print(
            "renderer: successfully instantiated; "
            "set maze rendering properties"
        )

    def draw(
        self,
        target_img: Image,
        state: list[list[Cell | tuple[Cell, str]]],
        els: dict[str, int] | None
    ) -> None:
        """Render maze cells, walls, and overlays onto target image."""

        # - background will paint all the image, including under walls,
        # with a single color (not led by cell)
        # - fortytwo, entrance and exit will paint a padded
        # interior (led by cell)
        # - walls will be painted by cell
        # - padding is not painted (it is the color of background)
        # - open channels between cells are background coloured
        if not els:
            elements = self.DEFAULT_COLORS
        else:
            elements = els
        # we paint everything with background
        # if background (almost like clearing)
        if "background" in elements:
            self.__draw_all_background(
                target_img,
                cast(list[list[Cell]], state),
                elements["background"]
            )
        for r in state:
            for c in r:
                if "walls" in elements:
                    self.__cell_walls(
                        target_img,
                        cast(Cell, c),
                        elements["walls"]
                    )
                if "fourtytwo" in elements and isinstance(c, FourtyTwoCell):
                    self.__draw_cell_interior(
                        target_img,
                        cast(Cell, c),
                        elements["fourtytwo"]
                    )
                if "entrance" in elements and isinstance(c, EntryCell):
                    self.__draw_cell_interior(
                        target_img,
                        cast(Cell, c),
                        elements["entrance"]
                    )
                if "exit" in elements and isinstance(c, ExitCell):
                    self.__draw_cell_interior(
                        target_img,
                        cast(Cell, c),
                        elements["exit"]
                    )
                if "path" in elements:
                    self.__draw_triangle_in_cell(
                        target_img,
                        cast(tuple[Cell, str], c),
                        elements["path"]
                    )

    def __get_total_size(self, num_cells_x: int, num_cells_y: int):
        """Compute total pixel size from maze grid dimensions."""

        total_w = num_cells_x * self.__total_cell_size - \
            self.__wall_thickness * (num_cells_x - 1)
        total_h = num_cells_y * self.__total_cell_size - \
            self.__wall_thickness * (num_cells_y - 1)
        return total_w, total_h

    def __draw_all_background(
        self,
        target_img: Image,
        state: list[list[Cell]],
        color: int
    ) -> None:
        """Fill entire maze render area with background color."""

        pix_tot_w, pix_tot_h = self.__get_total_size(len(state[0]), len(state))
        for y in range(pix_tot_h):
            for x in range(pix_tot_w):
                target_img.put_pixel(x, y, color)

    def __draw_cell_interior(
        self,
        target_img: Image,
        cell: Cell,
        color: int
    ) -> None:
        """Draw interior area of a cell using computed geometry."""

        # map through translation formula x_cell, y_cell coordinates to
        # the position of the corner of the renderered interior to
        # be painted
        x_cell = cell.cell_position_x
        y_cell = cell.cell_position_y
        x_area = 0
        y_area = 0
        if isinstance(cell, FourtyTwoCell):
            start_x = self.__wall_thickness + x_cell * \
                (self.__interior_cell_size + self.__wall_thickness) + \
                self.__padding * 2
            start_y = self.__wall_thickness + y_cell * \
                (self.__interior_cell_size + self.__wall_thickness) + \
                self.__padding // 2
            x_area = self.__cell_center
            y_area = self.__cell_center
        elif isinstance(cell, ExitCell) or isinstance(cell, EntryCell):
            start_x = self.__wall_thickness + x_cell * \
                (self.__interior_cell_size + self.__wall_thickness) + \
                self.__padding
            start_y = self.__wall_thickness + y_cell * \
                (self.__interior_cell_size + self.__wall_thickness) + \
                self.__padding
            x_area = self.__cell_center
            y_area = self.__cell_center
        else:
            start_x = self.__wall_thickness + x_cell * \
                (self.__interior_cell_size + self.__wall_thickness)
            start_y = self.__wall_thickness + y_cell * \
                (self.__interior_cell_size + self.__wall_thickness)
            x_area = self.__interior_cell_size
            y_area = self.__interior_cell_size

        # paint the interior
        for dy in range(y_area):
            for dx in range(x_area):
                target_img.put_pixel(start_x + dx, start_y + dy, color)

    def __cell_walls(
        self,
        target_img: Image,
        cell: Cell,
        color: int
    ) -> None:
        """Draw visible walls of a cell based on wall flags."""

        # TODO find a solution when x_cell and y_cell are
        # 0 for cell north and west
        x_cell = cell.cell_position_x
        y_cell = cell.cell_position_y

        start_x = x_cell * (self.__total_cell_size - self.__wall_thickness)
        start_y = y_cell * (self.__total_cell_size - self.__wall_thickness)

        if cell.has_north_wall():
            # width (inter+2*walls)
            for dx in range(self.__total_cell_size):
                # height (just one wall)
                for dy in range(self.__wall_thickness):
                    target_img.put_pixel(start_x + dx, start_y + dy, color)

        if cell.has_west_wall():
            # this is the wall width
            for dx in range(self.__wall_thickness):
                # this is the wall height
                for dy in range(self.__total_cell_size):
                    # paint between range witdh and start height
                    target_img.put_pixel(start_x + dx, start_y + dy, color)

        # East wall (vertical)
        if cell.has_east_wall():
            wall_x = start_x + self.__interior_cell_size + \
                self.__wall_thickness  # walk right
            # this is the wall width
            for dx in range(self.__wall_thickness):
                # this is the wall height
                for dy in range(self.__total_cell_size):
                    # paint between range width and start height
                    target_img.put_pixel(wall_x + dx, start_y + dy, color)

        # South wall (horizontal)
        if cell.has_south_wall():
            wall_y = start_y + self.__interior_cell_size + \
                self.__wall_thickness  # walk down
            # this is the the wall height
            for dy in range(self.__wall_thickness):
                # this is the wall width
                for dx in range(self.__total_cell_size):
                    # paint between start width and range height
                    target_img.put_pixel(start_x + dx, wall_y + dy, color)

    def __draw_filled_triangle(
        self,
        img: Image,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        x3: int,
        y3: int,
        color: int
    ):
        """Rasterize and fill triangle using scanline algorithm."""
        min_y = min(y1, y2, y3)
        max_y = max(y1, y2, y3)

        for y in range(min_y, max_y + 1):
            intersections = []
            # E: the followind defines the direction of
            # the painting within the bounderies
            # - check edge 1 -
            if y1 != y2 and min(y1, y2) <= y <= max(y1, y2):
                # E: this formula is KEY:
                # it is a canonical representation of two intersected lines!
                x = x1 + (x2 - x1) * (y - y1) // (y2 - y1)
                intersections.append(x)
            # - check edge 2 -
            if y2 != y3 and min(y2, y3) <= y <= max(y2, y3):
                x = x2 + (x3 - x2) * (y - y2) // (y3 - y2)
                intersections.append(x)
            # - check edge 3 -
            if y3 != y1 and min(y3, y1) <= y <= max(y3, y1):
                x = x3 + (x1 - x3) * (y - y3) // (y1 - y3)
                intersections.append(x)
            if len(intersections) == 2:
                x_start = min(intersections)
                x_end = max(intersections)
                for x in range(x_start, x_end + 1):
                    img.put_pixel(x, y, color)

    def __draw_triangle_in_cell(
        self,
        img: Image,
        state: tuple[Cell, str],
        color: int
    ) -> None:
        """Draw directional triangle overlay inside a cell."""

        cell, direction = state[0], state[1]
        x_cell = cell.cell_position_x
        y_cell = cell.cell_position_y

        start_x = self.__wall_thickness + x_cell * \
            (self.__interior_cell_size + self.__wall_thickness) + \
            self.__padding

        start_y = self.__wall_thickness + y_cell * \
            (self.__interior_cell_size + self.__wall_thickness) + \
            self.__padding

        size = self.__interior_cell_size
        margin = self.__padding

        left = start_x + margin
        right = start_x + size - margin
        top = start_y + margin
        bottom = start_y + size - margin
        center_x = start_x + size // 2
        center_y = start_y + size // 2

        if direction == "NORTH":
            x1, y1 = center_x, top
            x2, y2 = left, bottom
            x3, y3 = right, bottom

        elif direction == "SOUTH":
            x1, y1 = center_x, bottom
            x2, y2 = left, top
            x3, y3 = right, top

        elif direction == "WEST":
            x1, y1 = left, center_y
            x2, y2 = right, top
            x3, y3 = right, bottom

        elif direction == "EAST":
            x1, y1 = right, center_y
            x2, y2 = left, top
            x3, y3 = left, bottom

        else:
            return

        self.__draw_filled_triangle(img, x1, y1, x2, y2, x3, y3, color)
