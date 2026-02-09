#from abc import ABC, abstractmethod
#from dataclasses import dataclass
import sys
from typing import Type
#from typing import Callable


class MlxContext():
    def __init__(self, mlx_lib: any) -> None:
        try:
            # the minilibx is instantiated
            self.mlx = mlx_lib
            # the pointer is instantiated
            self.mlx_ptr = self.mlx.mlx_init()
            if not self.mlx_ptr:
                raise RuntimeError("mlx_init() failed to return a pointer")
        except Exception as e:
            print(f"Error: Can't initialize MLX: {e}", file=sys.stderr)
            sys.exit(1)

    def get_mlx_ptr(self) -> any:
        return self.mlx_ptr

    def get_size(self) -> tuple:
        return self.mlx.get_screen_size(self.mlx_ptr)

    def create_new_canvas(self, w: int, h: int, title: str) -> any:
        return self.mlx.mlx_new_window(self.mlx_ptr, w, h, title)

    def create_new_image(self, img_class: Type["Image"], w: int, h: int) -> "Image":
        img = img_class()
        img.img_ptr = self.mlx.mlx_new_image(self.mlx_ptr, w, h)
        #TODO error handing
        img.width = w
        img.height = h
        img.data, img.bytes_per_pixel, img.stride, img.endian = \
        self.mlx.mlx_get_data_addr(img.img_ptr)
        return img

    def destroy_window():
        #TODO
        pass
    
    def destroy_image():
        #TODO
        pass


class Canvas():
    def __init__(self, context: MlxContext, w: int, h: int, title: str) -> None:
        self.context = context
        try:
            self._win = self.context.create_new_canvas(w, h, title)
            if not self._win:
                raise Exception(f"Can't create {title} window")
        except Exception as e:
            print(f"Error: Win create: {e}", file=sys.stderr)
            sys.exit(1)
        self.main_buffer = Image(w, h)

    ## for buffering a single, modifiable image
    def present(self) -> None:
        self.context.mlx.mlx_put_image_to_window(
            self.context.mlx_ptr,
            self._win,
            self.main_buffer.img_ptr,
            0,
            0
        )


class Image():
    _width: int
    _height: int

    def __init__(self) -> None:
        self._img = None
        self._data = None
        self._bpp = 0
        self._sl = 0
        self._endian = 0
        self._width = 0
        self._height = 0

    #getters
    @property
    def img_ptr(self):
        return self._img

    @property
    def data(self):
        return self._data

    @property
    def bytes_per_pixel(self):
        return self._bpp

    @property
    def stride(self):
        return self._sl

    @property
    def endian(self):
        return self._endian

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    #setters
    @img_ptr.setter
    def img_ptr(self, img_ptr: any) -> None:
        self._img = img_ptr

    @data.setter
    def data(self, data: any) -> None:
        self._data = data

    @bytes_per_pixel.setter
    def bytes_per_pixel(self, bpp: int) -> None:
        self._bpp = bpp

    @stride.setter
    def stride(self, sl: int) -> None:
        self._sl = sl

    @endian.setter
    def endian(self, endian: int) -> None:
        self._endian = endian

    @width.setter
    def width(self, width: int) -> None:
        self._width = width

    @height.setter
    def height(self, height: int) -> None:
        self._height = height

    def put_pixel(self, x: int, y: int, color: int) -> None:
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return
        offset = y * self._sl + x * self._bpp
        self._write_color(offset, color)

    #TODO: BE CAREFUL WITH THIS ONE NOW...
    def _write_color(self, offset: int, color: int) -> None:
        self._data[offset + 0] = color & 0xFF
        self._data[offset + 1] = (color >> 8) & 0xFF
        self._data[offset + 2] = (color >> 16) & 0xFF
        self._data[offset + 3] = (color >> 24) & 0xFF

    #same as above but simpler
    def clear(self, color: int = 0x00000000):
        pixel_count = self.width * self.height
        self._data[:] = (color.to_bytes(4, byteorder="little")) * pixel_count


class MlxImageBuffer(Image):
    pass


class Renderer:
    # """Abstract/generic renderer: only knows ImageBuffer"""
    # def draw_pixel(self, target, x: int, y: int, color: int):
    #     target.put_pixel(x, y, color)

    def draw(self, target: any, state: any, elements: list[str] = None) -> None:
        """Show the image; MLX handled in boundary layer"""
        pass

    # def clear(self, target: any, state: any, color: int = 0x00000000):
    #     """
    #     Clear framebuffer to a solid color.
    #     Default: black (or transparent, depending on MLX build).
    #     """
    #     pass


class MazeRenderer(Renderer):
    """Maze-specific renderer"""
    DEFAULT_COLOURS = {
        "background": 0x00222222,
        "fortytwo": 0x00FFFFFF,
        "entrance": 0x0000FF00,
        "exit": 0x00FF00FF,
        "walls": 0x00AAAAAA,
        "path": 0x0000FF00}
    def __init__(self, cell_size: int):
        self.cell = cell_size #one direction
        self.interior = cell_size - 2 #one direction
        self.num_walls = 2 #one direction

    def draw(self,
    target_img: any,
    state: any,
    elements: dict[str, int] = None) -> None:
        elements = elements or self.DEFAULT_COLOURS
        if "background" in elements:
            self._background(target_img, state, elements["background"])
        if "fortytwo" in elements:
            self._fortytwo(target_img, state, elements["fortytwo"])
        if "entrance" in elements:
            self._entrance(target_img, state, elements["entrance"])
        if "exit" in elements:
            self._exit(target_img, state, elements["exit"])
        if "walls" in elements:
            self._walls(target_img, state, elements["walls"])  
            self._border_walls(target_img, state, elements["walls"])       
        if "path" in elements:
            self._path(target_img, state, elements["path"])

    # def clear(self, target: any, state: any, color) -> None:
    #     target._clear()
    
    def _fortytwo(self, target, cx: int, cy: int, color: int):
        """
        Draw all FortyTwo cells in the maze.
        Each cell is 7x7 pixels:
        - walls included
        - interior: 3x3 pixels
        - padding: 2px from top-left corner of cell
        """
        cell_size = 7
        interior_size = 3
        padding = 2

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
                        target_img.put_pixel(px, py, color)

    def _walls(self, target_img, state, color):
        for y, row in enumerate(state):
            for x, cell in enumerate(row):
                # cell = state.cells[y][x]

                base_x = x * 7
                base_y = y * 7

                # South wall (horizontal)
                if cell.has_south_wall():
                    wall_y = base_y + 6
                    for dx in range(7):
                        target_img.put_pixel(base_x + dx, wall_y, color)

                # East wall (vertical)
                if cell.has_east_wall():
                    wall_x = base_x + 6
                    for dy in range(7):
                        target_img.put_pixel(wall_x, base_y + dy, color)


    def _border_walls(self, target_img, state, color):
        # Top border
        for x in range(state.width):
            base_x = x * 7
            for dx in range(7):
                target_img.put_pixel(base_x + dx, 0, color)

        # Left border
        for y in range(state.height):
            base_y = y * 7
            for dy in range(7):
                target_img.put_pixel(0, base_y + dy, color)

    def _background(self, target_img, state, color):
        cell_size = 7
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
   
