from abc import ABC, abstractmethod
from dataclasses import dataclass
import sys


@dataclass
class XVar:
    """Structure for main screen vars using dataclass"""
    _mlx: any = None
    _mlx_ptr: any = None
    _screen_w: int = 0
    _screen_h: int = 0


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

    @property
    def mlx_ptr(self) -> any:
        return self._mlx_ptr

    @property
    def size(self) -> tuple:
        return self._mlx.get_screen_size(self._mlx_ptr)


# class XWindowVar:
#     """Structure for window vars"""
#     def __init__(self):   
#         self._win = None
#         # self._img = ImgData()
#         # self._imgidx = 0


# class Window(XWindowVar):
#     def __init__(self, s: Screen, w: int, h: int, title: str) -> None:
#         XWindowVar.__init__(self)        
#         self.screen = Screen()
#         try:
#             self._win = self.screen.mlx_new_window(self.screen.mlx_ptr, w, h, title)
#             if not self._win:
#                 raise Exception(f"Can't create {title} window")
#         except Exception as e:
#             print(f"Error: Win create: {e}", file=sys.stderr)
#             sys.exit(1)
#         self.main_buffer = Image(w, h)
    

class Image(ABC):
    @abstractmethod
    def put_pixel(self, x: int, y: int, color: int) -> None:
        pass
    
    @abstractmethod
    def present(self) -> None:
        pass

class MlxImageBuffer(Image):
    def __init__(self, mlx: any, mlx_ptr: any, win, w: int, h: int) -> None:
        self._mlx = mlx
        self._img = mlx.mlx_new_image(mlx_ptr, w, h)
        self._data, self._bpp, self._sl, self._endian = \
            mlx.mlx_get_data_addr(self._img)
    ## for buffering a single, modifiable image
    def render(self):
        self.screen.mlx_ptr.mlx_put_to_window(
            self.screen.mlx_ptr,
            self.win,
            self.main_buffer.img_ptr,
            0,
            0
        )

    ## for different, separated images
    # def render(self, image_obj, x, y):
    #     self.screen.mlx_ptr.mlx_put_to_window(
    #         self.screen.mlx_ptr,
    #         self.win,
    #         image_obj.img_ptr,
    #         x,
    #         y
    #     )

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

class Renderer:
    """Abstract/generic renderer: only knows ImageBuffer"""
    def draw_pixel(self, target, x: int, y: int, color: int):
        target.put_pixel(x, y, color)

    # def present(self, target):
    #     """Show the image; MLX handled in boundary layer"""
    #     pass


# class MazeRenderer(Renderer):
#     def draw(self, maze):
#         self.draw_cells_into_image()
#         self.present(self.maze_img)
class MazeRenderer(Renderer):
    """Maze-specific renderer"""
    def __init__(self, cell_size: int):
        self.cell = cell_size

    def draw(self, target, x: int, y: int, color: int):
        """Draw a maze cell as a block of pixels"""
        for dy in range(self.cell):
            for dx in range(self.cell):
                self.draw_pixel(target, x * self.cell + dx, y * self.cell + dy, color)


class UIRenderer(Renderer):
    def draw(self, ui_state):
        self.draw_buttons()
        #self.present(self.ui_img, y=maze_height)

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


    

