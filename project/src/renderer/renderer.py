from dataclasses import dataclass
import sys


#@dataclass(frozen=True)
class ImgData:
    """Structure for image data"""
    def __init__(self):
        self.img = None
        self.width = 0
        self.height = 0
        self.data = None
        self.sl = 0  # size line
        self.bpp = 0  # bits per pixel
        self.iformat = 0


@dataclass
class XVar:
    """Structure for main screen vars using dataclass"""
    self._mlx = None
    self._mlx_ptr = None
    self._screen_w = 0
    self._screen_h = 0


class Screen(XVar):
    """Screen singleton class"""
    _instance = None
    def __new__(cls, mlx_lib: any) -> None:
        if cls._instance is None:
            # the singleton is instantiated
            cls._instance = super(Screen, cls).__new__(cls)
            # the super is instantiated
            XVar.__init__(cls._instance)
            try:
                # the minilibx is instantiated
                cls._instance._mlx = mlx_lib
                # the pointer is instantiated
                cls._instance._mlx_ptr = cls._instance._mlx.mlx_init()
                if not cls._instance._mlx_ptr:
                    raise RuntimeError("mlx_init() failed to return a pointer")
            except Exception as e:
                print(f"Error: Can't initialize MLX: {e}", file=sys.stderr)
                sys.exit(1)
        return cls._instance

    @property
    def size(self) -> tuple:
        return self._mlx.get_screen_size(self._mlx_ptr)

    @property
    def mlx_ptr(self) -> any:
        return self._mlx_ptr


class XWindowVar:
    """Structure for window vars"""
    def __init__(self):        
        self._win = None
        self._img = ImgData()
        self._imgidx = 0


class Window(XWindowVar):
    def __init__(self, s: Screen, w: int, h: int, title: str) -> None:
        super().__init__()        
        self.engine = Screen()
        try:
            self._win = self.engine.mlx_new_window(self.engine.mlx_ptr, w, h, title)
            if not self._win:
                raise Exception(f"Can't create {title} window")
        except Exception as e:
            print(f"Error: Win create: {e}", file=sys.stderr)
            sys.exit(1)

class Renderer():
    def __init__(self, screen: Screen) -> None:
        window.

        print()

    @classmethod
    def draw_pixel(self, x: int, w: int, y: int, h: int):
        for ry in range(y, y + h):
            for rx in range(x, x + w):



class CellRenderer(Renderer):
    def __init__(self):
        super().__init__()     

    def draw_cell():
        print()
# pixel_step = bpp // 8

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


    

