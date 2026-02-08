from abc import ABC, abstractmethod
#from dataclasses import dataclass
import sys


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

    def create_new_image(self, factory: any, w: int, h: int) -> None:
        img = factory()
        img.img_ptr = self.mlx.mlx_new_image(self.mlx_ptr, w, h)
        #TODO error handing
        img.width = w
        img.height = h
        img.data = self.mlx.mlx_get_data_addr(
            img.img_ptr,
            img.bytes_per_pixel,
            img.stride,
            img.endian)
        return img

#         self.addr = self.screen._mlx.mlx_get_data_addr(
#             self.img_ptr,
#             self.bbp,
#             self.sl,
#             self.edian

    def clear_window():
        #TODO
        pass
    
    def clear_image():
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
        self.context.mlx.mlx_put_to_window(
            self.context.mlx_ptr(),
            self._win,
            self.main_buffer.img_ptr,
            0,
            0
        )
    ## might not be required
    # def clear(self) -> None:
    #     self.context.mlx_clear_window(
    #         self.context.mlx_ptr,
    #         self._win)


class Image():
    width: int
    height: int

    def __init__(self) -> None:
        self._img = None
        self._addr = None
        self._data = None
        self._bpp = 0
        self._sl = 0
        self._endian = 0
        self.width = 0
        self.height = 0

    #getters
    @property
    def addr(self):
        return self._addr

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
        return self.width

    @property
    def height(self):
        return self.height

    #setters
    @addr.setter
    def addr(self, addr: any) -> None:
        self._addr = addr

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
        self.width = width

    @height.setter
    def height(self, height: int) -> None:
        self.height = height

    def put_pixel(self, x: int, y: int, color: int) -> None:
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return
        offset = y * self._sl + x * self._bbp
        self._write_color(offset, color)

    #TODO: BE CAREFUL WITH THIS ONE NOW...
    def _write_color(self, offset: int, color: int) -> None:
        self._data[offset + 0] = color & 0xFF
        self._data[offset + 1] = (color >> 8) & 0xFF
        self._data[offset + 2] = (color >> 16) & 0xFF
        self._data[offset + 3] = (color >> 24) & 0xFF

    # @abstractmethod
    # def put_pixel(self, x: int, y: int, color: int) -> None:
    #     pass

    # # too concrete
    # def clear(self, color: int = 0x00000000):
    #     """
    #     Clear framebuffer to a solid color.
    #     Default: black (or transparent, depending on MLX build).
    #     """
    #     for y in range(self.height):
    #         row_start = y * self._sl
    #         for x in range(self.width):
    #             offset = row_start + x * self.bytes_per_pixel
    #             self._write_color(offset, color)

    # def _write_color(self, offset: int, color: int):
    #     # assumes 32bpp
    #     self._data[offset + 0] = color & 0xFF
    #     self._data[offset + 1] = (color >> 8) & 0xFF
    #     self._data[offset + 2] = (color >> 16) & 0xFF
    #     self._data[offset + 3] = (color >> 24) & 0xFF


        # self._data, self._bpp, self._sl, self._endian = \
        #     self.context.mlx.mlx_get_data_addr(self._img)

    #same as above but simpler
    def clear(self, color: int = 0x00000000):
        pixel_count = self.width * self.height
        self._data[:] = (color.to_bytes(4, byteorder="little")) * pixel_count


class MlxImageBuffer(Image):
    def __init__(self) -> None:
        super().__init__()

    # def put_pixel(self, x: int, y: int, color: int) -> None:
    #     if x < 0 or y < 0 or x >= self.width or y >= self.height:
    #         return
    #     offset = y * self._sl + x * self._bbp
    #     self._write_color(offset, color)

    # #TODO: BE CAREFUL WITH THIS ONE NOW...
    # def _write_color(self, offset: int, color: int) -> None:
    #     self._data[offset + 0] = color & 0xFF
    #     self._data[offset + 1] = (color >> 8) & 0xFF
    #     self._data[offset + 2] = (color >> 16) & 0xFF
    #     self._data[offset + 3] = (color >> 24) & 0xFF


class Renderer:
    # """Abstract/generic renderer: only knows ImageBuffer"""
    # def draw_pixel(self, target, x: int, y: int, color: int):
    #     target.put_pixel(x, y, color)

    def draw(self, target: any, state: any, elements: list[str] = None) -> None:
        """Show the image; MLX handled in boundary layer"""
        pass


# class MazeRenderer(Renderer):
#     def draw(self, maze):
#         self.draw_cells_into_image()
#         self.present(self.maze_img)
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
        if "path" in elements:
            self._path(target_img, state, elements["path"])
    
    def _entrance(self, target, cx: int, cy: int, color: int):
        """
        maze is a domain object (state because it might change):
        - maze.width
        - maze.height
        - maze.cells[y][x] or equivalent
        """
        # I need to translate incoming information into something that the graphical lib can read
        # so first, let's get how large it must be. Let's get the h and w in number of cells
        # I have to account for the number of walls: they are shared, so it means that some walls
        # have a wall less because it was already painted
        H = len(state) * self.cell_size
        W = len(state[0]) * self_cell_size
        padding = 2
        special_col_range = 3

        #now, let's translate this pixels to be drawn 
        # but first, let fill all the space with a background color
        for cell_y in range(H):
            for cell_x in range(W):
                cell = state[cell_y][cell_x]
                start_drawer_x = cell_x * self.cell_size
                start_drawer_y = cell_y * self.cell_size
                # Interior
                if isinstance(cell, FourtyTwoCell):
                    rang = padding + special_col
                    for d_y in range(start_drawer_y + padding, start_drawer_y + rang):
                        for d_x in range(start_drawer_x + padding, start_drawer_x + rang):
                            target_img.put_pixel(d_x, d_y, 0x00222222)

    def _draw_cell(self, target, cx: int, cy: int, color: int):
        px = cx * self.cell
        py = cy * self.cell

        for dy in range(self.cell):
            for dx in range(self.cell):
                target.put_pixel(px + dx, py + dy, color)

    def _cell_color(self, cell):
        if cell.is_wall:
            return 0x00FFFFFF
        return 0x00000000


# class UIRenderer(Renderer):
#     def draw(self, ui_state):
#         self.draw_buttons()
#         #self.present(self.ui_img, y=maze_height)

# class Renderer:
#     """Abstract base for any renderer"""
#     def draw(self, state):
#         """Polymorphic method: subclasses implement drawing logic"""
#         raise NotImplementedError


# class MazeRenderer(Renderer):
#     def __init__(self, maze_image, cell_size):
#         self.image = maze_image
#         self.cell_size = cell_size

#     def draw(self, maze):
#         """Draw maze cells into the image"""
#         for y, row in enumerate(maze.cells):
#             for x, cell in enumerate(row):
#                 color = 0xFFFFFF if cell.is_open else 0x000000
#                 self.draw_cell(self.image, x, y, color)

#     def draw_cell(self, image, x, y, color):
#         for dy in range(self.cell_size):
#             for dx in range(self.cell_size):
#                 image.put_pixel(x * self.cell_size + dx, y * self.cell_size + dy, color)


# class UIRenderer(Renderer):
#     def __init__(self, ui_image):
#         self.image = ui_image

#     def draw(self, ui_state):
#         """Draw buttons, panels, etc."""
#         for button in ui_state.buttons:
#             self.draw_button(button)

#     def draw_button(self, button):
#         x, y, w, h, color = button.x, button.y, button.width, button.height, button.color
#         for dy in range(h):
#             for dx in range(w):
#                 self.image.put_pixel(x + dx, y + dy, color)


# for y in range(height):
#     for x in range(width):
#         # The Handshake Formula
#         offset = (y * sl) + (x * pixel_step)
        
#         # Writing bytes manually to the memory buffer
#         # Using Little Endian: Blue, Green, Red, Alpha
#         data[offset] = (color & 0xFF)          # Blue
#         data[offset + 1] = (color >> 8) & 0xFF # Green
#         data[offset + 2] = (color >> 16) & 0xFF# Red
#         data[offset + 3] = 0                   # Alpha

                # elif isinstance(cell, EntryCell):
                #     print(ENTRY, end="")
                # elif isinstance(cell, ExitCell):
                #     print(EXIT, end="")
                # put_pixel(x, y, color: 0x00FFFFFF)

        #we are ready with the background, now the special interiors
        #they should fit the following rule:
        # - they should be between the walls
        # - have a padding of 1 pixel
        # we need to locate the exact place of the painting of each subspace
        # pseudo code is:
        # for cell in cells.generator:
        #     #get position in state:
        #     position = cell.position
        #     #jump always the first line
        #     for i, row in enumerate(target.data, len(state) + self._sl):
        #         #get position in image
        #         if position.x != i:
        #             continue
        #         for j, col in enumerate(row, 4):
        #             if position.y != j:
        #                 continue

                


        # for y in range(state.height):
        #     for x in range(state.width):
        #         cell = state.cells[y][x]

        #         color = self._cell_color(cell)
        #         self._draw_cell(target, x, y, color)

        # """Draw a maze cell as a block of pixels"""
        # for dy in range(self.cell):
        #     for dx in range(self.cell):
        #         self.draw_pixel(target, x * self.cell + dx, y * self.cell + dy, color)

# @dataclass
# class ImgData:
#     """Structure for image data"""
#     img_ptr: any = None
#     addr: any = None
#     width: int = 0
#     height: int = 0
#     data: int = None
#     sl: int = 0  # size line
#     bpp: int = 0  # bits per pixel
#     edian: int = 0

# class Image(ImgData):
#     def __init__(self, w: int, h: int) -> None:
#         super().__init__(self)
#         self.screen = Screen()
#         self.width = w
#         self.height = h
#         self.img_ptr = self.screen.mlx_ptr.mlx_new_image(
#             self.screen.mlx_ptr,
#             self.width,
#             self.height
#         )
#         self.addr = self.screen._mlx.mlx_get_data_addr(
#             self.img_ptr,
#             self.bbp,
#             self.sl,
#             self.edian
#         )

#     def put_pixel(self, x: int, y: int, color: int):
#         offset = y * self._sl + x * (self._bpp // 8)
#         self._data[offset:offset+4] = color.to_bytes(4, "little")

#     def present(self):
#         self._mlx.mlx_put_image_to_window(
#             self._mlx_ptr, self._win, self._img, 0, 0
#         )