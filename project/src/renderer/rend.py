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

# class XWindowVar:
#     """Structure for window vars"""
#     def __init__(self):   
#         self._win = None
#         # self._img = ImgData()
#         # self._imgidx = 0


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


class Image(ABC):
    width: int
    height: int

#     @property
#     @abstractmethod
#     def img_ptr(self):
#         """Backend image pointer (mlx image, texture handle, etc.)"""
#         pass

#     @property
#     @abstractmethod
#     def data(self):
#         """Raw pixel buffer"""
#         pass

#     @property
#     @abstractmethod
#     def bytes_per_pixel(self) -> int:
#         pass

#     @property
#     @abstractmethod
#     def stride(self) -> int:
#         """Bytes per row (line size)"""
#         pass

#     @property
#     @abstractmethod
#     def endian(self) -> int:
#         pass

#     @property
#     @abstractmethod
#     def width(self) -> int:
#         pass

#     @property
#     @abstractmethod
#     def height(self) -> int:
#         pass

    @abstractmethod
    def put_pixel(self, x: int, y: int, color: int) -> None:
        pass

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

    #same as above but simpler
    def clear(self, color: int = 0x00000000):
        pixel_count = self.width * self.height
        self._data[:] = (color.to_bytes(4, byteorder="little")) * pixel_count


class MlxImageBuffer(Image):
    def __init__(self, context: any, w: int, h: int) -> None:
        self.context = context
        self._img = self._create_new_img(w, h)
        #self._img = canvas.context.mlx_new_image(self._context.mlx_ptr(), w, h)
        self._data, self._bpp, self._sl, self._endian = \
            self.context.mlx.mlx_get_data_addr(self._img)
    
    def _create_new_img(self, w: int, h: int) -> None:
        #print(self.context)
        return self.context.mlx.mlx_new_image(self.context.get_mlx_ptr(), w, h)
    ## for different, separated images
    # def render(self, image_obj, x, y):
    #     self.screen.mlx_ptr.mlx_put_to_window(
    #         self.screen.mlx_ptr,
    #         self.win,
    #         image_obj.img_ptr,
    #         x,
    #         y
    #     )

    # @property
    # def img_ptr(self):
    #     return self._img

    # @property
    # def data(self):
    #     return self._data

    # @property
    # def bytes_per_pixel(self):
    #     return self._bpp

    # @property
    # def stride(self):
    #     return self._sl

    # @property
    # def endian(self):
    #     return self._endian

    # @property
    # def width(self):
    #     return self._width

    # @property
    # def height(self):
    #     return self._height
    
    def put_pixel(self, x: int, y: int, color: int) -> None:
        if x < 0 or y < 0 or x >= self._width or y >= self._height:
            return
        offset = y * self._sl + x * self._bbp
        self._write_color(offset, color)

    def _write_color(self, offset: int, color: int) -> None:
        self._data[offset + 0] = color & 0xFF
        self._data[offset + 1] = (color >> 8) & 0xFF
        self._data[offset + 2] = (color >> 16) & 0xFF
        self._data[offset + 3] = (color >> 24) & 0xFF


class Renderer:
    # """Abstract/generic renderer: only knows ImageBuffer"""
    # def draw_pixel(self, target, x: int, y: int, color: int):
    #     target.put_pixel(x, y, color)

    def draw(self, target: any, state: any) -> None:
        """Show the image; MLX handled in boundary layer"""
        pass


# class MazeRenderer(Renderer):
#     def draw(self, maze):
#         self.draw_cells_into_image()
#         self.present(self.maze_img)
class MazeRenderer(Renderer):
    """Maze-specific renderer"""
    def __init__(self, cell_size: int):
        self.cell = cell_size

    def draw(self, target: any, state: any) -> None:
        # """Draw a maze cell as a block of pixels"""
        # for dy in range(self.cell):
        #     for dx in range(self.cell):
        #         self.draw_pixel(target, x * self.cell + dx, y * self.cell + dy, color)
        """
        maze is a domain object:
        - maze.width
        - maze.height
        - maze.cells[y][x] or equivalent
        """
        for y in range(state.height):
            for x in range(state.width):
                cell = state.cells[y][x]

                color = self._cell_color(cell)
                self._draw_cell(target, x, y, color)

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