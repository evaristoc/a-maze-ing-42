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

class XVar:
    """Structure for main vars"""
    def __init__(self):
        self._mlx = None
        self._mlx_ptr = None
        self._screen_w = 0
        self._screen_h = 0
        self._win_1 = None
        self._img_1 = ImgData()
        self._imgidx = 0

class MazeRenderer(XVar):
    def __init__(self, mlx_instance, cell_size):
        super().__init__()
        try:
            self._mlx = mlx_instance()
        except Exception as e:
            print(f"Error: Can't initialize MLX: {e}", file=sys.stderr)
            sys.exit(1)
        self._mlx_ptr = self._mlx.mlx.mlx_init() 
        self._cell_size = cell_size

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


    

